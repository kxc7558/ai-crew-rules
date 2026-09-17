# Promo assets

Launch material for this repo. Not part of the plugin — nothing here is shipped to users.

```text
promo/
├── cards/                     9 × 1080×1440 PNG, publish in numeric order (01 is the cover)
├── posts.md                   post copy for 小红书 / 即刻·V2EX / X, plus a pacing note
└── content-aicrew-launch.json card content source (edit here, not the PNGs)
```

## Regenerate the cards

The renderer lives in a separate local workbench (`d:\douyin-cards`) — it is a zero-dependency
Chrome-headless pipeline (JSON → HTML → screenshot) and is deliberately not vendored here.

```bash
cd d:/douyin-cards
node render-aicrew.js --verify   # self-check: zoom >= 0.7, overflow <= 0
node render-aicrew.js            # write the PNGs to output/aicrew-launch/
```

Then copy the result back over `promo/cards/` and `promo/content-aicrew-launch.json`.

### The one gotcha

`douyin-cards/scripts/render.js` unconditionally overwrites the brand block from
`content/series.json`, which belongs to a different series (FDE course branding).
Rendering this series without handling that would stamp the wrong brand on the cover.

`render-aicrew.js` handles it: it backs `series.json` up, writes the AI Crew brand,
renders, and restores the original in a `finally` block — then verifies the restore
byte-for-byte and exits non-zero if it drifted. Do not render this series by calling
`scripts/render.js` directly.

## Editing the content

Card text lives in `content-aicrew-launch.json`. Two renderer rules worth knowing:

- **You cannot force a line break.** `\n` collapses to a space in HTML, so the cover title
  wraps wherever it fits. Keep it short enough to sit on one line, or long enough that the
  break lands on a phrase boundary. A title that breaks mid-word ("正在" split across lines)
  is the failure mode to watch for.
- **`note` over 12 characters gets truncated** with an ellipsis in the footer.

Always re-run `--verify` after editing, and look at the rendered PNG — the self-check
reports zoom and overflow, but it cannot tell you a line broke in an ugly place.
