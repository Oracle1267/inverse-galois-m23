# LLM Wiki v2 Vault Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a full v2 LLM wiki scaffold for the Obsidian vault without modifying existing notes.

**Architecture:** The vault remains Markdown-first. `AGENTS.md` defines the agent operating schema, `governance/` defines policies and protocols, `templates/` gives reusable note shapes, and `index.md` plus `dashboards/` make the system navigable.

**Tech Stack:** Obsidian-compatible Markdown, YAML frontmatter, PowerShell verification commands.

---

## File Structure

- Create `AGENTS.md`: central operating schema for agents.
- Create `index.md`: human-readable catalog and entry point.
- Create `dashboards/llm-wiki-dashboard.md`: operating dashboard.
- Create governance docs under `governance/`.
- Create reusable templates under `templates/`.
- Create folder README files in otherwise empty operational folders.
- Preserve `llm-wiki.md` and `Riemann Notes.md`.

### Task 1: Create Vault Folders

**Files:**
- Create directories listed in the design spec.

- [ ] **Step 1: Create directories**

Run:

```powershell
$dirs = @(
  'sources',
  'wiki',
  'entities',
  'entities/concepts',
  'entities/projects',
  'entities/people',
  'entities/files',
  'entities/decisions',
  'memory',
  'memory/working',
  'memory/episodic',
  'memory/semantic',
  'memory/procedural',
  'logs',
  'logs/ingest',
  'logs/query',
  'logs/lint',
  'templates',
  'governance',
  'dashboards'
)
foreach ($dir in $dirs) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
```

Expected: all directories exist.

### Task 2: Add Operating Schema and Index

**Files:**
- Create `AGENTS.md`
- Create `index.md`
- Create `dashboards/llm-wiki-dashboard.md`

- [ ] **Step 1: Create the operating schema**

Write `AGENTS.md` with explicit rules for ingest, query, lint, confidence, supersession, privacy, graph updates, and audit trails.

- [ ] **Step 2: Create the index**

Write `index.md` with links to existing notes, governance docs, templates, memory tiers, entities, sources, and logs.

- [ ] **Step 3: Create the dashboard**

Write `dashboards/llm-wiki-dashboard.md` with quick links and maintenance checklists.

### Task 3: Add Governance Documents

**Files:**
- Create `governance/schema.md`
- Create `governance/ingest-protocol.md`
- Create `governance/query-protocol.md`
- Create `governance/lint-protocol.md`
- Create `governance/privacy-and-governance.md`
- Create `governance/lifecycle-policy.md`

- [ ] **Step 1: Define the schema**

Write the page types, entity types, relationship types, and frontmatter fields.

- [ ] **Step 2: Define workflows**

Write ingest, query, and lint protocols as operational checklists.

- [ ] **Step 3: Define governance**

Write privacy, audit, lifecycle, confidence, retention, and supersession policies.

### Task 4: Add Templates and Folder READMEs

**Files:**
- Create `templates/source.md`
- Create `templates/wiki-page.md`
- Create `templates/entity.md`
- Create `templates/decision.md`
- Create `templates/ingest-log.md`
- Create `templates/query-log.md`
- Create `templates/lint-log.md`
- Create README files in empty operational folders.

- [ ] **Step 1: Add templates**

Write frontmatter-rich templates that future agents can copy.

- [ ] **Step 2: Add folder READMEs**

Write short README files explaining what belongs in each major folder.

### Task 5: Verify the Scaffold

**Files:**
- Read all created scaffold files.

- [ ] **Step 1: Check expected files**

Run:

```powershell
$expected = @(
  'AGENTS.md',
  'index.md',
  'dashboards/llm-wiki-dashboard.md',
  'governance/schema.md',
  'governance/ingest-protocol.md',
  'governance/query-protocol.md',
  'governance/lint-protocol.md',
  'governance/privacy-and-governance.md',
  'governance/lifecycle-policy.md',
  'templates/source.md',
  'templates/wiki-page.md',
  'templates/entity.md',
  'templates/decision.md',
  'templates/ingest-log.md',
  'templates/query-log.md',
  'templates/lint-log.md'
)
$missing = $expected | Where-Object { -not (Test-Path $_) }
if ($missing) { $missing; exit 1 } else { 'All expected files exist.' }
```

Expected: `All expected files exist.`

- [ ] **Step 2: Check unresolved markers**

Run:

```powershell
rg -n "\b(TODO|TBD|FIXME)\b" AGENTS.md index.md governance templates dashboards
```

Expected: no matches.

- [ ] **Step 3: Check schema terms**

Run:

```powershell
rg -n "confidence|supersession|lifecycle|privacy|audit|typed relationships" AGENTS.md governance index.md
```

Expected: matches in operating schema and governance docs.

- [ ] **Step 4: Check existing notes**

Run:

```powershell
Test-Path 'llm-wiki.md'
Test-Path 'Riemann Notes.md'
```

Expected: both commands return `True`.
