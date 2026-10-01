cat << 'EOF' > SECURITY.md
# Security & Dependency Audit Report

## Audit Summary
- **Date:** October 2026
- **Tool:** `pip-audit`
- **Result:** No known vulnerabilities found.

## Execution Log
$ poetry run pip-audit
No known vulnerabilities found
Name           Skip Reason
-------------- -----------------------------------------------------------------------------
orders-service Dependency not found on PyPI and could not be audited: orders-service (0.1.0)
