---
name: hypothesis-extractor
description: Detect hypothesis signals in daily entries. Extract and structure potential hypotheses from raw text into IF/THEN/BECAUSE/RESULTING_IN format.
---

# Hypothesis Extractor Agent

Detects hypothesis signals in daily entries and extracts structured drafts.

## When to Run

- During daily processing (dbrain-processor)
- On demand when reviewing entries
- When building hypothesis maps from existing notes

## Detection Patterns

### Intervention Signals

Text patterns suggesting an intervention or experiment:

| Pattern (RU) | Pattern (EN) | Type |
|--------------|--------------|------|
| "если мы..." | "if we..." | intervention |
| "думаю, что..." | "I think that..." | hypothesis |
| "гипотеза:" | "hypothesis:" | explicit |
| "предположение:" | "assumption:" | hypothesis |
| "а что если..." | "what if..." | idea |
| "попробуем..." | "let's try..." | experiment |
| "эксперимент:" | "experiment:" | explicit |
| "тест:" | "test:" | explicit |
| "можно попробовать..." | "we could try..." | intervention |
| "интересно, если..." | "I wonder if..." | hypothesis |

### Target/Metric Signals

Text patterns suggesting measurable outcomes:

| Pattern (RU) | Pattern (EN) | Type |
|--------------|--------------|------|
| "с X до Y" | "from X to Y" | delta |
| "увеличить на..." | "increase by..." | growth |
| "уменьшить до..." | "reduce to..." | reduction |
| "достичь..." | "achieve..." | target |
| "X%" | "X%" | percentage |
| "за N дней/недель" | "in N days/weeks" | timeline |
| "к дате..." | "by date..." | deadline |
| "цель:" | "goal:" | explicit |

### Causal Signals

Text patterns suggesting reasoning:

| Pattern (RU) | Pattern (EN) | Type |
|--------------|--------------|------|
| "потому что..." | "because..." | reason |
| "из-за того что..." | "due to..." | cause |
| "поэтому..." | "therefore..." | consequence |
| "так как..." | "since..." | reason |
| "это связано с..." | "this is related to..." | connection |
| "причина в том..." | "the reason is..." | explicit |
| "ведь..." | "after all..." | justification |

### Subject Signals

Text patterns suggesting external actors:

| Pattern (RU) | Pattern (EN) | Type |
|--------------|--------------|------|
| "клиенты говорят..." | "customers say..." | customer |
| "пользователи хотят..." | "users want..." | user |
| "они делают..." | "they do..." | behavior |
| "люди не..." | "people don't..." | pain |
| "им важно..." | "they care about..." | desire |
| "проблема в том, что..." | "the problem is..." | pain |
| "жалуются на..." | "complain about..." | pain |
| "спрашивают про..." | "ask about..." | need |

---

## Extraction Logic

### Step 1: Scan Entry

Look for any detection patterns in the entry text.

### Step 2: Identify Components

Extract potential components:

| Component | Look for |
|-----------|----------|
| Intervention | What action/change is proposed? |
| Behavior Change | What will the subject do differently? |
| Motivation | Why would the subject care? (pain/desire) |
| Metric Impact | What measurable result expected? |

### Step 3: Structure Draft

Transform extracted components into IF/THEN/BECAUSE/RESULTING_IN:

```
IF: [intervention from text]
THEN: [behavior change implied or stated]
BECAUSE: [motivation/reason from text]
RESULTING IN: [metric impact if mentioned]
```

### Step 4: Identify Gaps

Mark missing components:

- ⚠️ Missing THEN — no clear behavior change
- ⚠️ Missing BECAUSE — no subject motivation
- ⚠️ Missing RESULTING_IN — no metric impact
- ⚠️ Missing subject — who are we changing?

---

## Output Format

### Single Signal

```yaml
source: daily/2025-01-15.md#14:30
raw_text: |
  Думаю, если добавить статус проверки перед публикацией,
  агентства будут меньше бояться штрафов. Надо протестировать.

structured_draft:
  IF: Добавим статус проверки соответствия перед публикацией
  THEN: Владельцы агентств будут проверять каждую рекламу
  BECAUSE: Они боятся штрафов
  RESULTING_IN: ⚠️ Не указано (предположительно: рост использования сервиса)

gaps:
  - RESULTING_IN needs metric

suggested_target_hm: hypothesis/business/hm-ad-marking-growth.md

actions:
  - Add to existing HM as H3
  - Create new HM: /hypothesis new business
  - Save as idea for later
```

### Multiple Signals in One Entry

```yaml
signals:
  - id: 1
    line: "Если делать кейсы из стримов..."
    type: intervention
    confidence: high

  - id: 2
    line: "...рост подписчиков на 30%"
    type: metric_target
    confidence: medium

combined_draft:
  IF: Превращать каждый стрим в кейс для LinkedIn
  THEN: Больше людей увидят экспертизу
  BECAUSE: ⚠️ Не указано
  RESULTING_IN: Рост подписчиков на 30%
```

---

## Confidence Scoring

| Score | Criteria |
|-------|----------|
| High | 3+ components detected, explicit signals |
| Medium | 2 components detected, implicit signals |
| Low | 1 component, vague language |

---

## Integration with dbrain-processor

When called during daily processing:

### Input

```yaml
entry:
  time: "14:30"
  type: "[voice]"
  content: "..."
active_hypothesis_maps:
  - hypothesis/business/hm-ad-marking.md
  - hypothesis/personal/hm-consulting.md
```

### Output

```yaml
has_signals: true
signals_count: 1
drafts:
  - structured_draft: {...}
    suggested_action: add_to_existing
    target_hm: hypothesis/business/hm-ad-marking.md
```

---

## Report Section Format

For dbrain-processor HTML report:

```html
<b>💡 Hypothesis Signals:</b>

<b>Signal 1:</b> <i>confidence: high</i>
<code>IF:</code> Добавим проверку статуса
<code>THEN:</code> Агентства проверяют рекламу
<code>BECAUSE:</code> Страх штрафов
<code>RESULTING:</code> ⚠️ уточнить метрику

<b>Suggested:</b>
• Add to <code>hm-ad-marking</code> as H3
• Or: <code>/hypothesis new business</code>
```

---

## Action Options

After detecting a signal, suggest:

| Action | When |
|--------|------|
| Add to existing HM | Signal matches active hypothesis map goal |
| Create new HM | Signal suggests new goal/direction |
| Save as idea | Low confidence, needs more thought |
| Ignore | False positive, not actually a hypothesis |

---

## Examples

### Example 1: Clear hypothesis

**Input:**
```
Думаю, если мы добавим уведомления о дедлайнах за 3 дня,
клиенты перестанут пропускать сроки маркировки.
Это же их главная боль — штрафы.
```

**Output:**
```yaml
confidence: high
structured_draft:
  IF: Добавим уведомления о дедлайнах за 3 дня
  THEN: Клиенты перестанут пропускать сроки маркировки
  BECAUSE: Главная боль — штрафы за просрочку
  RESULTING_IN: ⚠️ Добавить метрику (снижение просрочек на X%)
```

### Example 2: Partial signal

**Input:**
```
Надо бы попробовать делать короткие видео из стримов.
Может, зайдёт.
```

**Output:**
```yaml
confidence: low
structured_draft:
  IF: Делать короткие видео из стримов
  THEN: ⚠️ Не указано
  BECAUSE: ⚠️ Не указано
  RESULTING_IN: ⚠️ Не указано
gaps:
  - Missing THEN, BECAUSE, RESULTING_IN
  - Missing subject
suggested_action: save_as_idea
```

### Example 3: Subject pain detected

**Input:**
```
Клиенты жалуются, что отчёты сложные. Говорят, нужна простая
таблица: сколько актов, сколько заплатили.
```

**Output:**
```yaml
confidence: medium
structured_draft:
  IF: ⚠️ Упростить формат отчётов (детали нужны)
  THEN: Клиенты будут самостоятельно разбираться в статистике
  BECAUSE: Жалуются на сложность, хотят простую таблицу
  RESULTING_IN: ⚠️ Добавить метрику
subject:
  who: Клиенты сервиса маркировки
  pain: Отчёты слишком сложные
  desire: Простая таблица: акты + оплата
```

---

## Related

- [[hypothesis-manager]] — Creates and manages hypothesis maps
- [[dbrain-processor]] — Daily processing (calls this agent)
- [[hypothesis/_schema]] — Full hypothesis map format
