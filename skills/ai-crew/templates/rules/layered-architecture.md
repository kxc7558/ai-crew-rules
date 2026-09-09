# Layered Architecture Rule

All new projects default to the four-layer architecture: humans describe
intent, AI implements and maintains in this structure.

## The Four Layers

| Layer | Directory | Role | May do | Must not do |
|---|---|---|---|---|
| Interface | api/ | Front desk | Receive requests, validate params, return results | Business rules, direct data access |
| Business | service/ | Brain | Business rules, orchestration | Direct DB access |
| Data | db/ | Warehouse keeper | Data CRUD | Business decisions |
| Common | shared/ | Toolbox | Generic utilities | Business rules, depending on other layers |

## Call Direction (iron rule)

- Downward only: api → service → db
- All layers may use shared; shared depends on nothing
- No reverse calls, no skipping layers (api never imports db directly)
- Directory names may map to project type (frontend: pages/store etc.),
  the direction rule stays unchanged

## Organization

Top level splits by feature domain (orders/, users/), each domain internally
layered; domains interact only through each other's api layer. This
complements — not conflicts with — organize-by-feature conventions.

## Interface Contracts

- Each layer directory's README.md ends with a "Public Interface List"
  registering what it exposes to other layers
- While the list is unchanged, changing a layer's implementation touches
  nothing else
- To change an interface: update the list first, then the implementation,
  then check all callers

## Bug Location

Display/entry wrong → api; result computed wrong → service; data access
wrong → db; utility wrong → shared. Fix only the located layer.

## New Projects

Start by copying the layered scaffold (constitution CLAUDE.md + per-layer
README rules), then `git init` and commit the scaffold before implementing.
