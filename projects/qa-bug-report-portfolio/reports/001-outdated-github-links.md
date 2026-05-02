# Outdated GitHub Repository Links on Portfolio Homepage

## Title

Outdated GitHub repository links on the portfolio homepage

## Severity

Medium: The homepage still loads, but some links may send visitors to an outdated repository path instead of the current profile repository.

## Priority

Medium: These links support portfolio navigation, so they should be fixed soon after the issue is documented.

## Environment

- Device: Local repository review
- Browser: Not tested in browser yet
- Operating system: Windows
- Page or feature: `docs/index.html` GitHub Pages homepage links
- Date tested: 2026-05-02

## Steps to Reproduce

1. Open `docs/index.html`.
2. Review the GitHub links in the Learning Journey and Project Roadmap sections.
3. Compare the linked repository path with the current profile repository: `https://github.com/KintsugiKoko/KintsugiKoko`.

## Expected Result

The homepage links should point visitors to the current GitHub profile repository paths:

- `https://github.com/KintsugiKoko/KintsugiKoko/tree/master/learning-journey`
- `https://github.com/KintsugiKoko/KintsugiKoko/tree/master/projects`

## Actual Result

The Learning Journey and Project Roadmap links point to the outdated repository path `Kintsugi-Koko`:

- `https://github.com/KintsugiKoko/Kintsugi-Koko/tree/master/learning-journey`
- `https://github.com/KintsugiKoko/Kintsugi-Koko/tree/master/projects`

## Impact

A first-time visitor may click a portfolio link and land on an old or missing page. That could make the portfolio feel less polished and make it harder for someone to follow the learning journey or project roadmap.

## Notes

- The issue appears in `docs/index.html` around the Learning Journey and Project Roadmap links.
- The GitHub profile links still point to `https://github.com/KintsugiKoko`, which appears intentional.
- This report documents the issue only. The links should be fixed in a separate follow-up change so the QA reporting practice stays clear.
