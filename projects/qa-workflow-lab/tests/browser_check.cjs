/* Optional browser regression: requires Playwright and an installed Chrome. */
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');

const [pagePath, outputPath, homepagePath] = process.argv.slice(2);
if (!pagePath || !outputPath) throw new Error('Usage: node tests/browser_check.cjs <showcase.html> <new-output-dir> [homepage.html]');
fs.mkdirSync(outputPath, { recursive: false });
const widths = [320, 390, 414, 768, 1024, 1440, 2560];

async function noOverflow(page, label) {
  const size = await page.evaluate(() => ({ width: innerWidth, content: document.documentElement.scrollWidth }));
  assert.ok(size.content <= size.width, `${label}: ${JSON.stringify(size)}`);
}

(async () => {
  const browser = await chromium.launch({ headless: true, channel: process.env.BROWSER_CHANNEL || 'chrome' });
  const errors = [], network = [], checks = [];
  try {
    const page = await browser.newPage({ acceptDownloads: true });
    page.on('pageerror', error => errors.push(error.message));
    await page.route(/^https?:/, route => {
      network.push(route.request().url());
      return route.abort();
    });
    await page.goto(pathToFileURL(path.resolve(pagePath)).href);
    const saved = await page.locator('#run-data').textContent();
    const data = JSON.parse(saved);
    assert.equal(data.length, 3);
    for (const entry of data) {
      const ids = new Set(entry.run.records.map(record => record.id));
      for (const workflow of entry.run.workflows) {
        for (const finding of workflow.findings) {
          for (const id of finding.evidence) assert.ok(ids.has(id), `Missing evidence ${id}`);
        }
      }
    }
    for (const width of widths) {
      await page.setViewportSize({ width, height: 900 });
      for (let c = 0; c < 3; c++) {
        await page.selectOption('#case', String(c));
        for (let w = 0; w < 8; w++) {
          await page.locator('#workflows button').nth(w).click();
          assert.match(await page.locator('#workflow-title').textContent(), new RegExp(`AI${w + 1} /`));
          for (const view of ['Findings', 'Work product', 'Tool trace']) {
            await page.getByRole('tab', { name: view, exact: true }).click();
            await noOverflow(page, `${width}, case ${c}, AI${w + 1}, ${view}`);
          }
        }
      }
      await page.selectOption('#case', '0');
      await page.locator('#workflows button').nth(5).click();
      await page.getByRole('tab', { name: 'Findings', exact: true }).click();
      await page.screenshot({ path: path.join(outputPath, `showcase-${width}.png`), fullPage: true });
      const buttonSizes = await page.locator('.save-actions button').evaluateAll(buttons => buttons.map(button => {
        const rect = button.getBoundingClientRect();
        return { width: rect.width, height: rect.height, fits: button.scrollWidth <= button.clientWidth,
          font: parseFloat(getComputedStyle(button).fontSize) };
      }));
      assert.ok(buttonSizes.every(size => size.width >= 44 && size.height >= 42 && size.fits && size.font >= 14));
      const evidenceButton = page.locator('#findings .evidence-links button').first();
      await evidenceButton.click();
      assert.equal(await page.locator('#evidence-dialog').isVisible(), true);
      assert.match(await page.locator('#evidence-content').textContent(), /SUB-1/);
      await noOverflow(page, `dialog ${width}`);
      await page.keyboard.press('Escape');
      assert.equal(await evidenceButton.evaluate(button => button === document.activeElement), true);
      checks.push({ width, cases: 3, workflows: 8, views: 3, overflow: false, exportButtons: 'pass', dialog: 'pass' });
    }
    await page.fill('#search', 'incomplete');
    assert.equal(await page.locator('.finding').count(), 1);
    await page.fill('#search', 'no-such-match');
    assert.equal(await page.locator('.empty').count(), 1);
    await page.fill('#search', '');
    await page.selectOption('#risk', 'Info');
    assert.equal(await page.locator('.finding').count(), 0);
    await page.selectOption('#risk', 'All risks');
    await page.getByRole('tab', { name: 'Findings', exact: true }).focus();
    for (const [key, label] of [['ArrowRight', 'Work product'], ['End', 'Tool trace'], ['Home', 'Findings'], ['ArrowLeft', 'Tool trace']]) {
      await page.keyboard.press(key);
      assert.equal(await page.getByRole('tab', { name: label, exact: true }).getAttribute('aria-selected'), 'true');
    }
    await page.locator('#trace summary').nth(1).click();
    assert.match(await page.locator('#trace').textContent(), /review_submissions/);
    for (let c = 0; c < 3; c++) {
      await page.selectOption('#case', String(c));
      for (const [button, extension] of [['#export', 'md'], ['#json-export', 'json']]) {
        const pending = page.waitForEvent('download');
        await page.click(button);
        const download = await pending;
        const destination = path.join(outputPath, `case-${c}.${extension}`);
        await download.saveAs(destination);
        const text = fs.readFileSync(destination, 'utf8');
        if (extension === 'json') assert.deepEqual(JSON.parse(text), data[c].run);
        else assert.equal(text, data[c].markdown);
      }
    }
    await page.selectOption('#case', '1');
    await page.locator('#workflows button').nth(4).click();
    assert.match(await page.locator('#workflow-state').textContent(), /blocked/);
    assert.match(await page.locator('#verdict').textContent(), /unverified/);
    await page.selectOption('#case', '2');
    await page.locator('#workflows button').nth(6).click();
    assert.match(await page.locator('#verdict').textContent(), /ready for human review/);
    assert.deepEqual(network, [], 'Standalone showcase must not request remote resources.');
    if (homepagePath) {
      for (const width of widths) {
        await page.setViewportSize({ width, height: 900 });
        await page.goto(pathToFileURL(path.resolve(homepagePath)).href + '#projects');
        await noOverflow(page, `homepage ${width}`);
        const secondaryFills = await page.locator('.button.secondary').evaluateAll(buttons =>
          buttons.map(button => getComputedStyle(button).backgroundImage));
        assert.ok(secondaryFills.every(fill => fill === 'none'), 'Secondary buttons must keep their dark fill.');
        const grid = await page.locator('.project-grid').boundingBox();
        const supporting = await page.locator('.supporting-note').first().boundingBox();
        assert.ok(supporting.y >= grid.y + grid.height + 16, 'Supporting work needs separation from project cards.');
        const link = page.getByRole('link', { name: 'QA Workflow Lab', exact: true });
        assert.equal(await link.count(), 1);
        const href = await link.getAttribute('href');
        assert.ok(fs.existsSync(path.resolve(path.dirname(homepagePath), href)));
      }
    }
    assert.deepEqual(errors, []);
    const report = { browser: await browser.version(), viewportChecks: checks, layoutStates: widths.length * 3 * 8 * 3,
      interactions: 'pass', exactExports: 6, evidenceReferences: 'resolved', pageErrors: errors,
      homepage: homepagePath ? 'pass' : 'not requested', scope: 'Desktop browser with resized viewports; not physical-device or screen-reader certification.' };
    fs.writeFileSync(path.join(outputPath, 'browser-results.json'), JSON.stringify(report, null, 2));
    console.log(JSON.stringify(report, null, 2));
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
