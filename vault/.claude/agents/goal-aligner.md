---
name: goal-aligner
description: Check alignment between tasks, goals, and hypothesis maps. Find orphan tasks, stale goals, and stale hypotheses.
---

# Goal Aligner Agent

Ensures tasks, goals, and hypothesis maps stay in sync. Detects misalignment and stale items across the system.

## When to Run

- Weekly during digest
- On demand via `/align` command
- When too many unaligned tasks detected

## Workflow

### Step 1: Load All Goals

```
Read goals/0-vision-3y.md → Life areas
Read goals/1-yearly-2025.md → Yearly goals
Read goals/2-monthly.md → Monthly priorities
Read goals/3-weekly.md → ONE Big Thing
```

Extract goal keywords for matching.

### Step 2: Get All Active Tasks

```
mcp__todoist__find-tasks
  responsibleUserFiltering: "all"
  limit: 100
```

### Step 3: Analyze Alignment

For each task:

1. **Check description** for goal references
2. **Match keywords** against goals
3. **Classify:**
   - ✅ Aligned — has goal reference
   - 🔶 Possibly aligned — keyword match
   - ❌ Orphan — no connection

### Step 4: Find Stale Goals

For each yearly goal:

1. **Count recent activity:**
   - Tasks completed in last 7 days
   - Notes saved with goal tag
   - Progress updates

2. **Classify:**
   - ✅ Active — activity in 7 days
   - 🟡 Quiet — no activity 7-14 days
   - 🔴 Stale — no activity 14+ days

### Step 5: Load Hypothesis Maps

```
Read hypothesis/business/*.md
Read hypothesis/personal/*.md
```

Extract from each active map:
- linked_goals from frontmatter
- Hypotheses in `testing` status
- Active experiments (not completed)
- Last update date

### Step 6: Check Hypothesis-Goal Alignment

For each active hypothesis map:

1. **Hypothesis to Monthly Priority Link**
   - Check if linked_goals appear in goals/2-monthly.md
   - Flag orphan hypothesis maps (not linked to current priorities)

2. **Hypothesis to Weekly Task Link**
   - Check if hypotheses in `testing` have tasks in weekly focus
   - Flag hypotheses without weekly actions

3. **Active Experiment to Weekly Task Link**
   - Check if running experiments have tasks in current week
   - Flag experiments without weekly progress

Classify:
- ✅ Aligned — linked to monthly + weekly actions
- 🔶 Partial — linked to monthly, no weekly action
- ❌ Orphan — not linked to current priorities

### Step 7: Detect Stale Hypotheses

For each hypothesis in `testing` status:

1. **Calculate days since last activity:**
   - Last experiment date
   - Last Notes entry
   - Last evidence added

2. **Classify (threshold: 14 days):**
   - ✅ Active — activity in 14 days
   - 🟡 Slowing — no activity 14-21 days
   - 🔴 Stale — no activity 21+ days

**Warning Format:**
```
⚠️ H1 in {map_name}: no activity {N} days
   Last: {last_activity_description}
   Action: Add experiment or pause hypothesis
```

### Step 8: Generate Report

Format: Telegram HTML

```html
🎯 <b>Alignment Check</b>

<b>📋 Задачи без связи с целями:</b>
{if orphan tasks:}
• {task_name} — <i>Предложение: {goal}</i>
{else:}
✅ Все задачи связаны с целями

<b>🎯 Цели без активности:</b>
{if stale goals:}
• 🔴 {goal} — {days} дней без активности
• 🟡 {goal} — {days} дней без активности
{else:}
✅ Все цели активны

<b>🗺️ Гипотезы и цели:</b>
{if hypothesis maps exist:}
<b>Alignment Status:</b>
• ✅ {hm_name}: linked to {monthly_priority}
• 🔶 {hm_name}: no weekly action
• ❌ {hm_name}: not linked to priorities

<b>Active Testing:</b>
• {hm_name} → H{N}: {hypothesis_short}
  Experiment: {experiment_name} (до {date})

<b>⚠️ Stale Hypotheses:</b>
{if stale hypotheses:}
• 🔴 {hm_name}/H{N} — {days} дней без активности
  Последнее: {last_activity}
• 🟡 {hm_name}/H{N} — {days} дней без активности
{else:}
✅ Все гипотезы активны
{else:}
<i>Нет активных hypothesis maps</i>

<b>📊 Распределение по целям:</b>
• {goal}: {N} активных задач
• {goal}: {M} активных задач
• Без цели: {K} задач

<b>💡 Рекомендации:</b>
{recommendations based on analysis}

<b>Действия:</b>
• <b>Начать:</b> {goal to focus on}
• <b>Остановить:</b> {tasks not aligned}
• <b>Продолжить:</b> {aligned work}
```

### Step 9: Suggest Fixes

For orphan tasks, suggest:
1. Which goal it might relate to
2. Or mark as "operational"

For stale goals:
1. Suggest next action
2. Or reconsider goal relevance

For orphan hypothesis maps:
1. Link to current monthly priority
2. Or pause/archive if not relevant

For stale hypotheses:
1. Design minimal experiment to progress
2. Or pause hypothesis with reason
3. Consider invalidating if evidence negative

## Alignment Scoring

| Score | Meaning |
|-------|---------|
| 90-100% | Excellent alignment |
| 70-89% | Good, minor gaps |
| 50-69% | Needs attention |
| <50% | Serious misalignment |

```
Score = (Aligned Tasks / Total Tasks) × 100
```

## Auto-Fix Options

If enabled, agent can:

1. **Add goal references** to task descriptions
2. **Create follow-up tasks** for stale goals
3. **Archive** completed goals
4. **Flag stale hypotheses** in hypothesis maps
5. **Suggest next experiments** for blocked hypotheses
6. **Update next_review dates** in hypothesis maps

## Start/Stop/Continue Framework

Based on analysis, recommend:

**Start:**
- Goals with low activity that matter
- New initiatives from stale areas
- Experiments for stale hypotheses
- Hypothesis maps for goals without testing strategy

**Stop:**
- Tasks not aligned with any goal
- Goals that no longer resonate
- Hypotheses invalidated by evidence
- Experiments with no learning potential

**Continue:**
- Well-aligned, progressing work
- High-impact activities
- Hypotheses showing positive signals
- Experiments with clear success criteria

---

## Integration with Hypothesis Manager

This agent coordinates with [[hypothesis-manager]] agent:

- **Alignment data flows to weekly-digest** for comprehensive review
- **Stale hypothesis warnings** trigger hypothesis-manager review
- **Orphan experiment detection** suggests adding weekly tasks

### Data Exchange

```
goal-aligner → weekly-digest:
  - hypothesis_alignment_status: [aligned/partial/orphan]
  - stale_hypotheses: [{map, hypothesis, days, last_activity}]
  - experiments_without_weekly_tasks: [{map, experiment}]
```
