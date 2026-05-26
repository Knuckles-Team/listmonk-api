# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.13.0] - 2026-05-22

### Added
- **Bidirectional Concept Traceability**: Embedded concept trace tags (`CONCEPT:CE-012` Actionable Reporting, `CONCEPT:CE-014` SDD Handoff) in MCP registrations and core managers.
- **Detailed Environment Configurations**: Added comprehensive environment variable documentation in both `README.md` and `.env.example` to support OAuth/OIDC, Eunomia Policies, and OpenAPI credentials.
- **Robust Test Coverage**: Added intensive unit test suites for all client subclasses, FastMCP tools, argument parsing CLI utilities, and exception-handling paths, raising coverage to 98%.

### Changed
- **Modular Refactoring**: Split legacy monolithic `listmonk_api.py` client wrapper into specialized sub-API managers under `listmonk_api/api/` (`Campaigns`, `Subscribers`, `Lists`, `Media`, `Templates`, `Imports`, `Transactional`).
- **Unified Interface**: Combined all modular sub-clients into a clean, modern `ListmonkAPI` class via subclassing.
- **Documentation Realignment**: Re-wrote `docs/index.md` to prune legacy ServiceNow references and accurately document active Listmonk endpoints, tags, and tools.

### Fixed
- **Tool Toggle Typos**: Fixed mismatch where env vars documented as `LISTMONK_SUBSCRIBERS_TOOL` were actually parsed as `LISTMONK_SUBSCRIBERSTOOL` in Python.
- **Dependency Warnings**: Suppressed requests / urllib3 / chardet configuration mismatch logs.

---

## [0.6.0] - 2026-05-18

### Added
- **Initial FastMCP Server Integration**: Basic implementation of action-routed tools for subscriber, list, campaign, and template management.
- **Initial Docker Orchestration**: Containerized runtime with docker-compose mapping server and agent services.
