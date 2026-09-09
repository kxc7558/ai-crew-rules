# Common Layer (Toolbox)

## Ground Rules

**May do:**
- Business-agnostic utilities: date formatting, generic validation,
  logging, constants

**Must not:**
- Contain any business rule
- Call api / service / db (this layer sits at the bottom and depends on nobody)

**May call:** nothing (keep zero dependencies)

## Public Interface List

(Utilities available to all layers; update this list before changing any of them)

| Name | Purpose | Input | Output |
|------|---------|-------|--------|
| (none yet) | | | |
