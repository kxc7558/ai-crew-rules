# Project Constitution: Layered Architecture

This project uses a four-layer architecture. Humans describe *what* they want;
AI implements and maintains it in this structure.

## Layer Map & Call Direction (the one iron rule)

```
api (interface layer)
 └─→ service (business layer)
        └─→ db (data layer)

shared (common layer): usable by everyone, depends on no one
```

1. Upper layers may call lower layers
2. Lower layers must never call upper layers
3. No skipping layers (api must go through service to reach db)
4. shared is available to all layers but calls none of them

## Layer Responsibilities

| Directory | Role | May do | Must not do |
|-----------|------|--------|-------------|
| api/ | Front desk | Receive requests, validate input, call service, return results | Business rules, direct data access |
| service/ | Brain | Business rules, workflow orchestration | Direct DB/file access, UI concerns |
| db/ | Warehouse keeper | Create/read/update/delete data | Business decisions (e.g. "discount over 100") |
| shared/ | Toolbox | Generic utilities | Business rules |

Detailed rules live in each layer's README.md.

## File Placement

Before creating a file, ask: which layer does it belong to? Put it there.
Misplaced files count as violations; prefer a new subdirectory over a wrong layer.

## Interface Contracts (the key to "fix where it broke")

- The "Public Interface List" table at the end of each layer's README.md
  registers the functions this layer exposes to other layers
- While the list is unchanged, changing one layer's implementation must not
  touch any other layer
- When an interface must change: update the list first, then the
  implementation, then check every caller

## Bug Location Cheat Sheet

| Symptom | Check first |
|---------|-------------|
| Wrong display / input not validated | api |
| Wrong result / wrong flow | service |
| Data lost / persistence errors | db |
| Utility misbehaving | shared |

Once located, only change that layer's directory. Never fix across layers.

## Growing the Project

When features multiply: split the top level by feature domain
(e.g. `orders/`, `users/`), each domain containing its own
api/service/db/shared. Domains talk to each other only through the other
domain's api layer.
