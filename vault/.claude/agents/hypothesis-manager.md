---
name: hypothesis-manager
description: Create and manage hypothesis maps. Implements EKG technique for quick map creation, error validation, experiment design, and result analysis.
---

# Hypothesis Manager Agent

Main agent for hypothesis map lifecycle management.

## Commands

| Command | Action |
|---------|--------|
| `/hypothesis` | Show dashboard with all maps |
| `/hypothesis new {domain}` | Create new map using EKG technique |
| `/hypothesis review {name}` | Review specific map with recommendations |
| `/hypothesis validate {name}` | Run error detection on map |

## When to Run

- On demand via `/hypothesis` commands
- Weekly during digest (summary section)
- When hypothesis signal detected in daily processing

---

## Workflow: Dashboard

### Step 1: Collect All Maps

```
Read hypothesis/business/*.md
Read hypothesis/personal/*.md
Read hypothesis/archive/*.md
```

### Step 2: Extract Status

For each map:
- Status (active/paused/archived)
- Goal outcome + current metric value
- Count of hypotheses by status
- Next review date
- Days since last update

### Step 3: Generate Dashboard

Format: Telegram HTML

```html
🗺️ <b>Hypothesis Maps Dashboard</b>

<b>📊 Active Maps:</b>

<b>Business:</b>
• <b>{map_name}</b>
  Goal: {outcome} ({current} → {target})
  Hypotheses: {testing}🧪 {validated}✅ {invalidated}❌
  Next review: {date}

<b>Personal:</b>
• <b>{map_name}</b>
  Goal: {outcome} ({current} → {target})
  Hypotheses: {testing}🧪 {validated}✅ {invalidated}❌
  Next review: {date}

<b>⏸️ Paused Maps:</b>
• {map_name} — paused {days} days ago

<b>⚠️ Attention Needed:</b>
• {map_name} — review overdue by {days} days
• {map_name} — stale (no activity 14+ days)

<b>📈 This Week:</b>
• Experiments completed: {N}
• Hypotheses validated: {M}
• Hypotheses invalidated: {K}

<b>Commands:</b>
<code>/hypothesis new business</code> — Create business map
<code>/hypothesis new personal</code> — Create personal map
<code>/hypothesis review {name}</code> — Review specific map
```

---

## Workflow: Create New Map (EKG Technique)

EKG = Express Map in 20-30 minutes.

### Step 1: Goal Clarification

Use goal shaking technique to clarify the outcome.

**Prompt to user:**

```
🎯 Давай определим цель.

Опиши желаемый РЕЗУЛЬТАТ (не задачу).
Что изменится, когда цель достигнута?

Примеры:
❌ "Внедрить CRM" (это задача)
✅ "Менеджеры не теряют клиентов" (это результат)

❌ "Бегать по утрам" (это задача)
✅ "Чувствую энергию весь день" (это результат)

Твоя цель:
```

**Goal Shaking Questions:**
- "Если достигнем в 10 раз больше — это всё ещё то, чего хочешь?"
- "Если полностью провалим — что изменится в жизни?"
- "Представь, что цель достигнута. Что ты делаешь по-другому?"

### Step 2: Metrics Definition

**Prompt to user:**

```
📊 Теперь метрики.

Верхний уровень — субъективная оценка (0-10):
Например: "Удовлетворённость бизнесом: 4 → 8"

Нижний уровень — объективная метрика (числа):
Например: "MRR: 50k → 200k"

Субъективная метрика (0-10):
Текущее: ___ Цель: ___ Дедлайн: ___

Объективная метрика:
Название: ___
Текущее: ___ Цель: ___ Дедлайн: ___

Балансирующие метрики (ограничения):
Что НЕ ДОЛЖНО ухудшиться?
Например: "Время на семью ≥ 3 вечера/неделю"
```

### Step 3: Subject Identification

**Prompt to user:**

```
👤 Кто субъект?

Субъект — это АВТОНОМНЫЙ АГЕНТ, чьё поведение мы хотим изменить.
Не исполнитель (команда, сотрудник), а тот, кто сам принимает решения.

Для бизнеса: клиенты, пользователи, партнёры
Для личного: "Я", "Я-предприниматель", "Я-отец", близкие

Кто субъект твоей гипотезы?

Опиши его:
- Кто он?
- Что делает сейчас?
- Что его беспокоит (pains)?
- Чего он хочет (desires)?
```

### Step 4: Hypothesis Formulation

**Prompt to user:**

```
💡 Формулируем гипотезу.

Структура: IF → THEN → BECAUSE → RESULTING IN

IF: Наше вмешательство (принцип, не детали)
THEN: Как изменится поведение субъекта
BECAUSE: Связь с болью или желанием субъекта
RESULTING IN: Влияние на метрику

Пример:
IF: Мы покажем статус соответствия до публикации
THEN: Владельцы агентств будут проверять каждую рекламу
BECAUSE: Они боятся штрафов и хотят чувствовать себя защищёнными
RESULTING IN: Ежедневное использование → конверсия в платных

Твоя гипотеза:
IF: ___
THEN: ___
BECAUSE: ___
RESULTING IN: ___
```

### Step 5: First Experiment Design

**Prompt to user:**

```
🧪 Первый эксперимент.

Минимальный тест для проверки гипотезы.

1. Что конкретно сделаем?
2. Какой размер выборки? (сколько субъектов)
3. Сколько времени займёт?
4. Что будет означать успех?
5. Что будет означать неудачу?

Эксперимент:
Действие: ___
Выборка: ___
Срок: ___
Успех если: ___
Неудача если: ___
```

### Step 6: Create File

Based on collected information:

1. Generate file at `hypothesis/{domain}/hm-{short-name}.md`
2. Fill all sections from schema
3. Add to MOC-hypotheses.md
4. Confirm creation

```html
✅ <b>Hypothesis Map создана!</b>

Файл: <code>hypothesis/{domain}/hm-{name}.md</code>

<b>Цель:</b> {outcome}
<b>Метрика:</b> {current} → {target}
<b>Субъект:</b> {subject}
<b>Гипотеза H1:</b> {short_description}
<b>Первый эксперимент:</b> {experiment} (до {date})

<b>Следующий шаг:</b>
Начать эксперимент и записывать результаты.

<code>/hypothesis review {name}</code> — просмотреть карту
```

---

## Workflow: Review Map

### Step 1: Load Map

```
Read hypothesis/{domain}/hm-{name}.md
```

### Step 2: Analyze Current State

For each hypothesis:
- Status and days in current status
- Evidence collected (count and quality)
- Experiments (completed, ongoing, planned)
- Tasks linked and their status

### Step 3: Run Red Path Prioritization

Identify top 1-2 hypotheses to focus on:
- Highest expected impact
- Closest to validation/invalidation
- Least effort to next evidence

### Step 4: Generate Review Report

```html
📋 <b>Review: {map_name}</b>

<b>🎯 Goal:</b>
{outcome}
{current} → {target} (deadline: {date})
Progress: {percent}% {progress_bar}

<b>📊 Metrics:</b>
• Subjective: {current}/10 → {target}/10
• Objective: {metric_name}: {current} → {target}
• Balancing: {metric} {status_ok_or_warning}

<b>🧪 Hypotheses:</b>

<b>H1: {name}</b> — {status_emoji} {status}
Evidence: {collected}/{required}
{evidence_list}
Current experiment: {description} (ends {date})
Recommendation: {recommendation}

<b>H2: {name}</b> — {status_emoji} {status}
Evidence: {collected}/{required}
Recommendation: {recommendation}

<b>🔴 Red Path (Focus):</b>
→ {hypothesis_name}: {next_action}

<b>📋 Active Tasks:</b>
• {task} — {hypothesis} — {status}

<b>🚧 Blockers:</b>
• {blocker} — {resolution_plan}

<b>💡 Recommendations:</b>
• {recommendation_1}
• {recommendation_2}

<b>📅 Next Review:</b> {date}
```

---

## Workflow: Validate Map

Run error detection patterns on hypothesis map.

### Error Patterns

#### 1. Task Instead of Goal
**Check:** Goal contains action verbs (implement, create, build, add)
**Fix:** Reframe as outcome

#### 2. Executor Instead of Subject
**Check:** Subject is team, employee, or "we/us"
**Fix:** Identify autonomous decision-maker

#### 3. BECAUSE Not About Subject
**Check:** BECAUSE contains "we need", "company wants", "to hit KPIs"
**Fix:** Reframe around subject's pain/desire

#### 4. Premature Specification
**Check:** IF contains specific technologies, exact numbers
**Fix:** Abstract to principle level

#### 5. Motivation Not of Subject
**Check:** RESULTING_IN mentions team, company, internal metrics
**Fix:** Reframe around subject's outcome

#### 6. Orphan Tasks
**Check:** Tasks table has empty Hypothesis column
**Fix:** Link to hypothesis or remove

#### 7. Stale Hypothesis
**Check:** Testing status with no activity 14+ days
**Fix:** Add experiment or pause

### Validation Report

```html
🔍 <b>Validation: {map_name}</b>

<b>✅ Passed:</b>
• Frontmatter complete
• All required sections present
• Hypothesis structure valid

<b>⚠️ Warnings:</b>
• H2: BECAUSE may be about us, not subject
  Current: "BECAUSE we need revenue"
  Suggest: "BECAUSE {subject} wants..."

• Task "Fix bug" has no hypothesis link

<b>❌ Errors:</b>
• Goal looks like a task: "Implement feature X"
  Suggest: Reframe as outcome

<b>📊 Validation Score:</b> {score}/100

<b>Actions:</b>
• Fix {N} errors before proceeding
• Review {M} warnings
```

---

## Result Analysis Functions

### After Experiment Completion

When user reports experiment results:

1. **Evaluate Evidence Sufficiency**
   - Count positive vs negative signals
   - Check if meets threshold (3 for validated, 2 for invalidated)

2. **Recommend Status Change**
   - `testing → validated`: 3+ positive evidence
   - `testing → invalidated`: 2+ failed experiments
   - `testing → testing`: Continue, more data needed

3. **Suggest Next Steps**
   - **Scale:** Hypothesis validated, expand scope
   - **Pivot:** Hypothesis invalidated, try variation
   - **Pause:** Not priority now, return later
   - **Kill:** Fundamentally wrong, abandon

4. **Update Learnings**
   - Extract insights from experiment
   - Add to Notes section
   - Update Review Log

### Analysis Prompt

```
🧪 <b>Experiment Complete: {experiment_name}</b>

<b>Results:</b>
{user_provided_results}

<b>Analysis:</b>
• Hypothesis: {validated/invalidated/inconclusive}
• Evidence strength: {strong/moderate/weak}
• Confidence: {high/medium/low}

<b>Recommendation:</b>
{scale/pivot/pause/kill}

<b>Reason:</b>
{explanation}

<b>Next Steps:</b>
1. {action_1}
2. {action_2}

<b>Learnings to capture:</b>
{insights}
```

---

## Strategic Cadence

### Weekly Review Workflow

Every week:

1. Check all active maps
2. Identify overdue reviews
3. Check experiments due this week
4. Update hypothesis statuses
5. Prioritize using Red Path

### Red Path Prioritization

Focus on top 1-2 hypotheses:

```
Priority Score = (Impact × Confidence) / Effort

Impact: 1-5 (effect on metric)
Confidence: 1-5 (likelihood of success)
Effort: 1-5 (resources needed)
```

Only tasks for red path hypotheses; everything else → backlog.

---

## Integration Points

- **dbrain-processor:** Receives hypothesis signals, shows active experiments
- **weekly-digest:** Provides hypothesis progress summary
- **goal-aligner:** Checks hypothesis-goal alignment
