---
paths: "hypothesis/**/*.md"
---

# Hypothesis Map Format

Rules for hypothesis maps in `hypothesis/` folder.

## File Structure

```
hypothesis/
├── _schema.md           # Format reference (do not modify)
├── personal/            # Personal strategy maps
│   └── hm-*.md
├── business/            # Business/product maps
│   └── hm-*.md
└── archive/             # Archived maps
    └── hm-*.md
```

## Naming Convention

Files follow pattern: `hm-{short-name}.md`

Examples:
- `hm-consulting-growth.md`
- `hm-saas-monetization.md`
- `hm-fitness-routine.md`

## Required Frontmatter

```yaml
---
type: hypothesis-map
domain: personal | business
status: active | paused | archived
created: YYYY-MM-DD
updated: YYYY-MM-DD
review_cadence: weekly | biweekly | monthly
next_review: YYYY-MM-DD
linked_goals:
  - "[[goals/1-yearly-2026#Goal Name]]"
---
```

All fields are required.

## Required Sections

Every hypothesis map MUST contain these sections in order:

1. **Goal** — Outcome description with metrics
2. **Subjects** — Autonomous agents whose behavior we change
3. **Hypotheses** — IF/THEN/BECAUSE/RESULTING_IN structure
4. **Tasks** — Always linked to hypotheses
5. **Blockers** — What's preventing progress
6. **Notes** — Observations and raw thoughts
7. **Review Log** — Decision history

## Hypothesis Status Transitions

```
idea ──────────────► testing
                        │
                        ├──► validated (min 3 positive evidence)
                        │
                        └──► invalidated (min 2 failed experiments)

any status ──────────► paused (deprioritized, return later)
```

### Validation Requirements

**To mark as `validated`:**
- Minimum 3 independent evidence items
- Evidence shows behavior change (not just activity)
- Metric moved in predicted direction
- No conflicting evidence ignored
- Results reproducible

**To mark as `invalidated`:**
- Minimum 2 failed experiments
- Clear documentation of why it failed
- Learnings captured in Notes

## Hypothesis Structure

Every hypothesis MUST follow IF/THEN/BECAUSE/RESULTING_IN:

```markdown
**IF:** [Our intervention — principle, not details]
**THEN:** [Subject's behavior will change]
**BECAUSE:** [Link to subject's pain or desire]
**RESULTING IN:** [Impact on metric]
```

## Error Detection Patterns

When validating or reviewing hypothesis maps, detect these common errors:

### 1. Task Instead of Goal

**Pattern:** Goal describes an action to take, not an outcome to achieve.

```markdown
# WRONG
**Outcome:** Implement caching for API

# RIGHT
**Outcome:** API response time under 200ms for 95% of requests
```

**Detection:** Goal contains verbs like "implement", "create", "build", "write", "add".

### 2. Executor Instead of Subject

**Pattern:** Subject is someone who executes tasks, not an autonomous decision-maker.

```markdown
# WRONG
**Who:** Development team

# RIGHT
**Who:** New user trying the product for first time
```

**Detection:** Subject is internal team, employee role, or "we/us".

### 3. BECAUSE Not About Subject

**Pattern:** BECAUSE explains our motivation, not subject's pain/desire.

```markdown
# WRONG
**BECAUSE:** We need to hit revenue targets

# RIGHT
**BECAUSE:** User wants to save 2 hours weekly on manual work
```

**Detection:** BECAUSE contains "we need", "company wants", "to hit KPIs".

### 4. Premature Specification

**Pattern:** IF contains implementation details instead of principles.

```markdown
# WRONG
**IF:** We add Redis caching with TTL 300s and LRU eviction

# RIGHT
**IF:** We reduce page load time below 2 seconds
```

**Detection:** IF contains specific technologies, numbers, or technical details.

### 5. Motivation Not of Subject

**Pattern:** RESULTING_IN describes our goals, not subject's outcomes.

```markdown
# WRONG
**RESULTING IN:** Team hits Q1 targets

# RIGHT
**RESULTING IN:** User completes checkout 30% faster
```

**Detection:** RESULTING_IN mentions team, company, or internal metrics.

### 6. Orphan Tasks

**Pattern:** Tasks not linked to any hypothesis.

```markdown
# WRONG
| Task | Hypothesis | Status |
|------|------------|--------|
| Fix bug in login | — | todo |

# RIGHT
| Task | Hypothesis | Status |
|------|------------|--------|
| Fix bug in login | H1 | todo |
```

**Detection:** Tasks table has empty Hypothesis column.

### 7. Stale Hypothesis

**Pattern:** Hypothesis in `testing` status with no activity for 14+ days.

**Detection:** Last experiment date or last Notes entry > 14 days ago.

## Review Workflow

When reviewing a hypothesis map:

1. Check frontmatter completeness
2. Verify all sections present
3. Run error detection patterns
4. Check hypothesis status validity
5. Identify stale hypotheses
6. Verify tasks have hypothesis links
7. Update `next_review` date

## Links

- [[hypothesis/_schema.md]] — Full format reference with examples
- [[MOC-hypotheses]] — Index of all hypothesis maps
