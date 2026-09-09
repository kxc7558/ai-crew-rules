# Interface Layer (Front Desk)

## Ground Rules

**May do:**
- Receive external requests (web pages, API endpoints, button handlers)
- Validate input format
- Call the service layer for business processing
- Return results to the caller

**Must not:**
- Implement business rules (e.g. "10% off over 100" — that's service's job)
- Touch the database directly (always service → db)

**May call:** service, shared

## Public Interface List

(AI registers every entry point this layer exposes; update on every addition/change)

| Name | Purpose | Input | Output |
|------|---------|-------|--------|
| (none yet) | | | |
