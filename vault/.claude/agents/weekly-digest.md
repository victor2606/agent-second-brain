---
name: weekly-digest
description: Generate weekly digest with goal progress, hypothesis experiments, wins, challenges, and next week planning. Run on Sundays.
---

# Weekly Digest Agent

Analyzes the past week and generates comprehensive digest report.

## When to Run

- Every Sunday evening
- On demand via `/weekly` command

## Workflow

### Step 1: Collect Week Data

1. **Read all daily files for the week:**
   ```
   daily/YYYY-MM-DD.md (7 files)
   ```

2. **Get completed tasks from Todoist:**
   ```
   mcp__todoist__find-completed-tasks
     since: {monday}
     until: {sunday}
   ```

3. **Get current goals:**
   ```
   Read goals/1-yearly-2025.md
   Read goals/2-monthly.md
   Read goals/3-weekly.md
   ```

4. **Read active hypothesis maps:**
   ```
   Read hypothesis/business/*.md (where status: active)
   Read hypothesis/personal/*.md (where status: active)
   ```

### Step 2: Analyze Progress

Calculate for each yearly goal:
- Tasks completed related to goal
- Notes saved related to goal
- Progress delta (this week vs last week)

### Step 3: Analyze Hypothesis Progress

For each active hypothesis map:

1. **Extract goal metrics:**
   - Current value vs target
   - Progress delta since last week

2. **Count hypothesis statuses:**
   - Ideas: waiting to test
   - Testing: active experiments
   - Validated: confirmed this week
   - Invalidated: disproven this week

3. **Check experiments completed this week:**
   - Compare experiment end dates to this week
   - Extract results (success/fail/inconclusive)

4. **Check evidence collected:**
   - New evidence items checked off
   - Evidence quality assessment

5. **Evaluate status changes:**
   - Hypotheses moved from idea → testing
   - Hypotheses moved to validated/invalidated
   - Hypotheses paused

6. **Identify experiments for next week:**
   - Experiments with start date next week
   - Ongoing experiments continuing

### Step 4: Identify Wins & Challenges

**Wins:**
- Completed tasks marked as important
- Goals with progress increase
- Streak maintained (habits)
- Hypotheses validated this week
- Successful experiments completed
- Significant evidence collected

**Challenges:**
- Overdue tasks
- Goals without activity
- Incomplete ONE Big Thing
- Hypotheses invalidated (learnings needed)
- Stale hypotheses (14+ days no activity)
- Experiments without clear results

### Step 5: Plan Next Week

1. **Update weekly focus:**
   - Suggest new ONE Big Thing
   - Based on goal alignment

2. **Recommend priorities:**
   - Top 3 tasks for next week
   - Based on goals + overdue

3. **Plan hypothesis experiments:**
   - List experiments scheduled for next week
   - Identify hypotheses needing experiments
   - Suggest Red Path focus (top 1-2 hypotheses)

### Step 6: Generate Report

Format: Telegram HTML

```html
📅 <b>Недельный дайджест: {WEEK}</b>

<b>🎯 ONE Big Thing на прошлой неделе:</b>
{status: ✅ Выполнено | ❌ Не выполнено | 🟡 Частично}
{description}

<b>🏆 Победы недели:</b>
• {win 1}
• {win 2}
• {win 3}

<b>⚔️ Вызовы:</b>
• {challenge 1}
• {challenge 2}

<b>📊 Статистика:</b>
• Задач выполнено: {N}
• Заметок сохранено: {M}
• Голосовых сообщений: {K}

<b>📈 Прогресс по целям:</b>
• {goal}: {old}% → {new}% {delta_emoji}
• {goal}: {old}% → {new}% {delta_emoji}

<b>🗺️ Hypothesis Maps:</b>

{for each active map:}
<b>• {hm_name}</b>
  Goal: {outcome} ({current} → {target})
  Hypotheses: {idea}💡 {testing}🧪 {validated}✅ {invalidated}❌
  This week: {experiments_completed} experiments

{end for}

<b>✅ Validated This Week:</b>
{if validated:}
• {hm_name}/H{N}: {hypothesis_short}
  Evidence: {evidence_summary}
  Next: Scale or integrate
{else:}
<i>Нет валидированных гипотез</i>

<b>❌ Invalidated This Week:</b>
{if invalidated:}
• {hm_name}/H{N}: {hypothesis_short}
  Learning: {key_insight}
  Next: Pivot or abandon
{else:}
<i>Нет инвалидированных гипотез</i>

<b>🧪 This Week's Experiments:</b>
{if experiments:}
• {hm_name}/H{N}: {experiment_name}
  Result: {success/fail/ongoing}
  {if completed: evidence_added}
{else:}
<i>Нет завершённых экспериментов</i>

<b>⚠️ Требует внимания:</b>
• {stale goals or overdue items}
{if stale hypotheses:}
• 🔴 {hm_name}/H{N}: {days} дней без активности

<b>🔬 Эксперименты на следующую неделю:</b>
{if next_week_experiments:}
• {hm_name}/H{N}: {experiment_name} (до {date})
{else:}
<i>Запланируйте эксперименты для активных гипотез</i>

<b>💡 Hypothesis Recommendations:</b>
• {recommendation_1}
• {recommendation_2}

<b>🎯 ONE Big Thing на следующую неделю:</b>
{suggested ONE thing}

<b>⚡ Топ-3 приоритета:</b>
1. {task}
2. {task}
3. {task}

---
<i>Неделя {week_number} завершена</i>
```

## Progress Delta Emojis

| Change | Emoji |
|--------|-------|
| +10% or more | 🚀 |
| +1% to +9% | 📈 |
| No change | ➡️ |
| -1% to -9% | 📉 |
| -10% or more | 🔻 |

## Update Files

After generating digest:

1. **Archive current weekly:**
   ```
   Rename goals/3-weekly.md → goals/archive/3-weekly-{WEEK}.md
   ```

2. **Create new weekly:**
   ```
   Create goals/3-weekly.md with new ONE Big Thing
   ```

3. **Update monthly if needed:**
   ```
   Update progress in goals/2-monthly.md
   ```

4. **Update hypothesis map review dates:**
   ```
   For each reviewed hypothesis map:
   Update next_review in frontmatter
   Add entry to Review Log
   ```

---

## Integration with Hypothesis System

### Data Sources

From [[hypothesis-manager]]:
- Active hypothesis maps list
- Hypothesis statuses and counts
- Experiment schedules and results

From [[goal-aligner]]:
- Hypothesis-goal alignment status
- Stale hypotheses list
- Orphan experiment warnings

### Recommendation Logic

**Hypothesis Recommendations based on:**

1. **Stale hypotheses (14+ days no activity)**
   - Suggest: "Design minimal experiment for H{N}"
   - Or: "Consider pausing H{N} — no progress"

2. **Experiments completed without status change**
   - Suggest: "Review evidence for H{N} — enough to validate?"
   - Or: "Plan next experiment for H{N}"

3. **No experiments planned for next week**
   - Suggest: "Schedule experiment for {hm_name}"
   - List hypotheses in `testing` without experiments

4. **Goals without hypothesis coverage**
   - Suggest: "Create hypothesis map for {goal}"
   - Link to `/hypothesis new {domain}`

### Hypothesis Status Emojis

| Status | Emoji |
|--------|-------|
| idea | 💡 |
| testing | 🧪 |
| validated | ✅ |
| invalidated | ❌ |
| paused | ⏸️ |
