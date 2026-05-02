# Inventory count does not update after using potion

| Field | Details |
| --- | --- |
| Severity | Medium |
| Priority | Medium |
| Environment | Windows 11, Chrome, practice inventory page |
| Repro Rate | 3/3 |

## Steps to Reproduce

1. Open the inventory screen.
2. Use one health potion.
3. Look at the potion count.

## Expected Result

Potion count decreases by one.

## Actual Result

Potion count stays the same until the page refreshes.

## Evidence / Attachments

- screenshots/inventory-count-before-after.png
- logs/inventory-ui-refresh.log

## Notes

This could confuse a player because the UI suggests the item was not used.
