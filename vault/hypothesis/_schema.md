# Hypothesis Map Schema

Reference schema for creating hypothesis maps. Based on [Hypothesis Mapping methodology](https://github.com/Byndyusoft/hypothesismapping).

---

## Frontmatter Template

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

---

## Required Sections

### 1. Goal

Goal describes the OUTCOME, not a task to execute.

```markdown
## Goal

**Outcome:** [What we want to achieve — outcome, not task]

### Metrics

| Type | Metric | Current | Target | Deadline |
|------|--------|---------|--------|----------|
| Subjective | [Satisfaction/wellbeing 0-10] | X | Y | date |
| Objective | [Measurable number] | X | Y | date |

### Balancing Metrics

Constraints that must NOT be violated while pursuing the goal.

| Metric | Constraint | Current |
|--------|------------|---------|
| [Metric name] | ≤ X or ≥ Y | value |
```

**Important:**
- Subjective metrics (0-10) and objective metrics (numbers) NEVER mix on the same level
- Upper level: subjective (satisfaction, happiness)
- Lower level: objective (revenue, users, time)

---

### 2. Subjects

Subject is an AUTONOMOUS AGENT whose behavior we want to change. NOT an executor.

```markdown
## Subjects

### [Subject Name]

**Who:** [Description — someone who makes own decisions]

**Current Behavior:**
[What they do now]

**Pains:**
- [Pain 1 — what causes discomfort/loss]
- [Pain 2]

**Desires:**
- [Desire 1 — what they want to achieve/gain]
- [Desire 2]
```

**Personal Strategy Subjects:**
- "Я" (self)
- "Я-предприниматель" (self as entrepreneur)
- "Я-отец" (self as father)
- "Родственники" (family members)
- "Клиенты" (clients)

---

### 3. Hypotheses

Hypothesis describes INTERVENTION that changes SUBJECT'S BEHAVIOR.

```markdown
## Hypotheses

### H1: [Short Name]

**Status:** idea | testing | validated | invalidated | paused

**IF:** [Our intervention — principle, not implementation details]
**THEN:** [Subject's behavior will change how]
**BECAUSE:** [Link to subject's pain or desire]
**RESULTING IN:** [Impact on metric]

**Evidence:**
- [ ] [Evidence item 1]
- [ ] [Evidence item 2]
- [ ] [Evidence item 3]

**Experiments:**
| # | Description | Start | End | Result |
|---|-------------|-------|-----|--------|
| 1 | [Experiment] | date | date | pending/success/fail |
```

**Status Transitions:**
- `idea` → `testing`: Start first experiment
- `testing` → `validated`: Min 3 positive evidence items
- `testing` → `invalidated`: Min 2 failed experiments
- Any → `paused`: Deprioritized, return later

---

### 4. Evidence Criteria Checklist

Before marking hypothesis as `validated`:

```markdown
### Evidence Checklist for [Hypothesis Name]

- [ ] At least 3 independent evidence items collected
- [ ] Evidence shows behavior change, not just activity
- [ ] Metric moved in predicted direction
- [ ] No conflicting evidence ignored
- [ ] Results reproducible (not one-time luck)
```

---

### 5. Tasks

All tasks MUST be linked to a hypothesis. Orphan tasks = no strategic value.

```markdown
## Tasks

| Task | Hypothesis | Status | Due | Notes |
|------|------------|--------|-----|-------|
| [Task description] | H1 | todo/doing/done | date | |
```

---

### 6. Blockers

```markdown
## Blockers

| Blocker | Impact | Owner | Resolution |
|---------|--------|-------|------------|
| [What's blocking] | [Which hypothesis] | [Who can resolve] | [Plan] |
```

---

### 7. Notes

```markdown
## Notes

### YYYY-MM-DD
[Observations, insights, raw thoughts]
```

---

### 8. Review Log

```markdown
## Review Log

| Date | Status Summary | Key Decisions | Next Actions |
|------|----------------|---------------|--------------|
| YYYY-MM-DD | [Brief status] | [What decided] | [What to do] |
```

---

## Common Errors to Avoid

### 1. Task instead of Goal
- Wrong: "Implement feature X"
- Right: "Users complete onboarding successfully"

### 2. Executor instead of Subject
- Wrong: "Development team" (they execute, don't decide)
- Right: "New user" (autonomous, decides to use or not)

### 3. BECAUSE not about Subject
- Wrong: "BECAUSE we need revenue"
- Right: "BECAUSE user wants to save time"

### 4. Premature Specification
- Wrong: "IF we add Redis caching with TTL 300s"
- Right: "IF we speed up loading time below 2s"

### 5. Motivation not of Subject
- Wrong: "RESULTING IN: team hits KPIs"
- Right: "RESULTING IN: user completes task faster"

---

## Techniques

### EKG (Express Map in 20-30 min)
Quick hypothesis map creation:
1. What outcome? (5 min)
2. Who is the subject? (5 min)
3. Main hypothesis (10 min)
4. First experiment (10 min)

### Red Path
Focus on priority chains only:
1. Mark top 1-2 hypotheses
2. Only tasks for these hypotheses
3. Everything else — backlog

### Goal Shaking
Clarify goal via exaggeration:
- "If we achieve 10x of this, would it matter?"
- "If we fail completely, what changes?"

---

## Business Example

```markdown
---
type: hypothesis-map
domain: business
status: active
created: 2025-01-15
updated: 2025-01-20
review_cadence: weekly
next_review: 2025-01-27
linked_goals:
  - "[[goals/1-yearly-2026#SaaS — выйти на 100-200к/мес]]"
---

# HM: Ad Marking Service Growth

## Goal

**Outcome:** Users actively use and pay for ad marking service

### Metrics

| Type | Metric | Current | Target | Deadline |
|------|--------|---------|--------|----------|
| Subjective | My satisfaction with SaaS growth | 4 | 8 | 2026-06 |
| Objective | MRR (my share) | 0 | 100k | 2026-06 |
| Objective | Paying users | 5 | 50 | 2026-06 |

### Balancing Metrics

| Metric | Constraint | Current |
|--------|------------|---------|
| Support hours/week | ≤ 5 | 2 |
| Churn rate | ≤ 10% | 5% |

## Subjects

### Small Agency Owner

**Who:** Owner of small digital agency (5-15 people), makes decisions on tools

**Current Behavior:**
Uses Excel or manual marking, spends 2-3 hours weekly on bureaucracy

**Pains:**
- Fear of fines for incorrect marking
- Time wasted on manual work
- Confusion with ORD requirements

**Desires:**
- Automate routine
- Feel compliant and safe
- Focus on client work, not paperwork

## Hypotheses

### H1: Instant Compliance Check

**Status:** testing

**IF:** We show compliance status before publishing
**THEN:** Agency owners will check every ad through our service
**BECAUSE:** They fear fines and want to feel safe
**RESULTING IN:** Daily active usage → conversion to paid

**Evidence:**
- [x] 3 users mentioned "fear of fines" in interviews
- [x] Prototype test: 80% checked status before publishing
- [ ] Need to measure conversion after feature launch

**Experiments:**
| # | Description | Start | End | Result |
|---|-------------|-------|-----|--------|
| 1 | Add status indicator to dashboard | 2025-01-15 | 2025-01-22 | success |
| 2 | A/B test with/without instant check | 2025-01-25 | — | pending |

### H2: Per-Act vs Subscription

**Status:** idea

**IF:** We offer both per-act (19₽) and unlimited (2000₽/mo) pricing
**THEN:** Small agencies start with per-act, then upgrade
**BECAUSE:** They want to test before committing
**RESULTING IN:** Lower barrier → more trials → more upgrades

## Tasks

| Task | Hypothesis | Status | Due | Notes |
|------|------------|--------|-----|-------|
| Implement status indicator | H1 | done | 2025-01-22 | |
| Set up A/B test | H1 | doing | 2025-01-25 | |
| Design pricing page | H2 | todo | 2025-02-01 | |

## Blockers

| Blocker | Impact | Owner | Resolution |
|---------|--------|-------|------------|
| Partner approval for pricing | H2 | Partner | Meeting scheduled 01-28 |

## Notes

### 2025-01-20
Interviewed 3 users. All mentioned fear of fines as primary motivator. Compliance messaging resonates stronger than "save time".

## Review Log

| Date | Status Summary | Key Decisions | Next Actions |
|------|----------------|---------------|--------------|
| 2025-01-20 | H1 in testing, H2 idea | Focus on H1 first | Complete A/B test |
```

---

## Personal Example

```markdown
---
type: hypothesis-map
domain: personal
status: active
created: 2025-01-10
updated: 2025-01-18
review_cadence: weekly
next_review: 2025-01-25
linked_goals:
  - "[[goals/1-yearly-2026#Консалтинг — 300-400к/мес]]"
---

# HM: Consulting Growth via Content

## Goal

**Outcome:** Consulting income grows through inbound leads from content

### Metrics

| Type | Metric | Current | Target | Deadline |
|------|--------|---------|--------|----------|
| Subjective | Satisfaction with consulting setup | 5 | 8 | 2026-06 |
| Objective | Consulting MRR | 150k | 300k | 2026-06 |
| Objective | Inbound leads per month | 2 | 8 | 2026-06 |

### Balancing Metrics

| Metric | Constraint | Current |
|--------|------------|---------|
| Consulting hours/week | ≤ 7 | 5 |
| Content creation hours/week | ≤ 3 | 2 |

## Subjects

### Я-консультант

**Who:** Myself as consultant — decides how to spend time, which clients to take

**Current Behavior:**
Do weekly streams, occasional LinkedIn posts. Wait for referrals.

**Pains:**
- Income depends on referrals (unpredictable)
- Streams take time but unclear ROI
- Impostor syndrome about pricing

**Desires:**
- Predictable lead flow
- Work with interesting projects
- Charge premium without guilt

## Hypotheses

### H1: Streams → Cases → Leads

**Status:** testing

**IF:** I turn every stream into a case study on LinkedIn
**THEN:** I will get more profile views and DMs
**BECAUSE:** I want to show expertise without "selling"
**RESULTING IN:** More inbound leads from content

**Evidence:**
- [x] Last case post: 3x usual engagement
- [x] 2 DMs after case post
- [ ] Need 3 more data points

**Experiments:**
| # | Description | Start | End | Result |
|---|-------------|-------|-----|--------|
| 1 | Post 4 case studies in January | 2025-01-10 | 2025-01-31 | ongoing |

### H2: Raise Rate = Better Clients

**Status:** idea

**IF:** I raise rate from 15k to 20k/hour
**THEN:** I will attract more serious clients
**BECAUSE:** I want to work on challenging problems
**RESULTING IN:** Better projects, same income with fewer hours

## Tasks

| Task | Hypothesis | Status | Due | Notes |
|------|------------|--------|-----|-------|
| Write case from stream #24 | H1 | done | 2025-01-15 | |
| Write case from stream #25 | H1 | doing | 2025-01-22 | |
| Calculate break-even for rate increase | H2 | todo | 2025-02-01 | |

## Blockers

| Blocker | Impact | Owner | Resolution |
|---------|--------|-------|------------|
| None | | | |

## Notes

### 2025-01-18
Stream #25 about Claude Code got good engagement. Should be easy to turn into case.

## Review Log

| Date | Status Summary | Key Decisions | Next Actions |
|------|----------------|---------------|--------------|
| 2025-01-18 | H1 testing (2/4 posts done) | Continue experiment | 2 more case posts |
```

---

## Naming Convention

Files in `hypothesis/` follow this pattern:

```
{domain}/hm-{short-name}.md
```

Examples:
- `business/hm-ad-marking-growth.md`
- `personal/hm-consulting-content.md`
- `personal/hm-fitness-routine.md`

Archive by moving to `hypothesis/archive/`.

---

## Links

- [[MOC-hypotheses]] — Index of all hypothesis maps
- [[goals/1-yearly-2026]] — Current year goals
- [[goals/0-vision-3y]] — Long-term vision
