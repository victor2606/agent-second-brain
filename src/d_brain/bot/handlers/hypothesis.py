"""Hypothesis command handler for managing hypothesis maps."""

import asyncio
import logging
from dataclasses import dataclass
from enum import Enum

from aiogram import Bot, Router
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from d_brain.bot.formatters import format_process_report
from d_brain.config import get_settings
from d_brain.services.git import VaultGit
from d_brain.services.processor import ClaudeProcessor
from d_brain.services.transcription import DeepgramTranscriber

router = Router(name="hypothesis")
logger = logging.getLogger(__name__)


class HypothesisSubcommand(Enum):
    """Supported hypothesis subcommands."""

    DASHBOARD = "dashboard"
    NEW = "new"
    REVIEW = "review"
    VALIDATE = "validate"


@dataclass
class ParsedCommand:
    """Parsed hypothesis subcommand."""

    subcommand: HypothesisSubcommand
    domain: str | None = None
    name: str | None = None


class HypothesisState(StatesGroup):
    """FSM states for hypothesis creation flow."""

    ekg_session = State()  # Multi-turn EKG conversation with Claude


def parse_subcommand(args: str | None) -> ParsedCommand:
    """Parse hypothesis subcommand from command arguments.

    Examples:
        None or "" -> dashboard
        "new business" -> new with domain=business
        "new personal" -> new with domain=personal
        "review consulting-growth" -> review with name=consulting-growth
        "validate saas-monetization" -> validate with name=saas-monetization
    """
    if not args:
        return ParsedCommand(subcommand=HypothesisSubcommand.DASHBOARD)

    parts = args.strip().split(maxsplit=1)
    cmd = parts[0].lower()

    if cmd == "new":
        domain = parts[1] if len(parts) > 1 else "business"
        if domain not in ("business", "personal"):
            domain = "business"
        return ParsedCommand(subcommand=HypothesisSubcommand.NEW, domain=domain)

    elif cmd == "review":
        name = parts[1] if len(parts) > 1 else None
        return ParsedCommand(subcommand=HypothesisSubcommand.REVIEW, name=name)

    elif cmd == "validate":
        name = parts[1] if len(parts) > 1 else None
        return ParsedCommand(subcommand=HypothesisSubcommand.VALIDATE, name=name)

    # Unknown subcommand - treat as dashboard
    return ParsedCommand(subcommand=HypothesisSubcommand.DASHBOARD)


def build_hypothesis_prompt(parsed: ParsedCommand) -> str:
    """Build Claude prompt based on parsed subcommand.

    Uses hypothesis-manager agent instructions for all operations.
    """
    base_context = """Ты - hypothesis-manager agent для управления hypothesis maps.

CONTEXT:
- Hypothesis maps находятся в vault/hypothesis/
- Schema в vault/hypothesis/_schema.md
- Правила в vault/.claude/rules/hypothesis-format.md
- Agent инструкции в vault/.claude/agents/hypothesis-manager.md

CRITICAL OUTPUT FORMAT:
- Return ONLY raw HTML for Telegram (parse_mode=HTML)
- NO markdown: no **, no ##, no ```, no tables
- Allowed tags: <b>, <i>, <code>, <s>, <u>
- Be concise - Telegram has 4096 char limit
"""

    if parsed.subcommand == HypothesisSubcommand.DASHBOARD:
        return f"""{base_context}

TASK: Сгенерируй dashboard всех hypothesis maps.

WORKFLOW:
1. Read vault/hypothesis/business/*.md (where status: active)
2. Read vault/hypothesis/personal/*.md (where status: active)
3. Read vault/hypothesis/archive/*.md for archived count
4. Extract from each: status, goal, metrics, hypothesis counts
5. Generate HTML dashboard

OUTPUT FORMAT:
🗺️ <b>Hypothesis Maps Dashboard</b>

<b>📊 Active Maps:</b>

<b>Business:</b>
• <b>map_name</b>
  Goal: outcome (current → target)
  Hypotheses: N🧪 M✅ K❌
  Next review: date

<b>Personal:</b>
• ...

<b>⏸️ Paused Maps:</b>
• map_name — paused N days ago

<b>⚠️ Attention Needed:</b>
• Overdue reviews
• Stale hypotheses (14+ days)

<b>Commands:</b>
<code>/hypothesis new business</code>
<code>/hypothesis new personal</code>
<code>/hypothesis review name</code>
"""

    elif parsed.subcommand == HypothesisSubcommand.NEW:
        domain = parsed.domain or "business"
        return f"""{base_context}

TASK: Начни создание нового hypothesis map для domain={domain}.

Используй EKG технику (Express Map 20-30 min):

STEP 1 - Goal Clarification:
Спроси пользователя о цели. Покажи примеры правильной и неправильной формулировки.

OUTPUT:
🎯 <b>Создание Hypothesis Map ({domain})</b>

<b>Шаг 1: Определим цель</b>

Опиши желаемый <b>РЕЗУЛЬТАТ</b> (не задачу).
Что изменится, когда цель достигнута?

<b>Примеры:</b>
❌ "Внедрить CRM" (это задача)
✅ "Менеджеры не теряют клиентов" (это результат)

❌ "Бегать по утрам" (это задача)
✅ "Чувствую энергию весь день" (это результат)

<i>Отправь описание цели следующим сообщением</i>

<b>Tip:</b> Goal Shaking — если достигнем в 10x больше, это всё ещё то, чего хочешь?
"""

    elif parsed.subcommand == HypothesisSubcommand.REVIEW:
        name = parsed.name or ""
        return f"""{base_context}

TASK: Сгенерируй review для hypothesis map "{name}".

WORKFLOW:
1. Find hypothesis map by name (search in business/ and personal/)
2. Read the map file
3. Analyze current state:
   - Goal progress (current vs target)
   - Hypothesis statuses
   - Active experiments
   - Evidence collected
   - Blockers
4. Apply Red Path prioritization
5. Generate recommendations

OUTPUT FORMAT:
📋 <b>Review: map_name</b>

<b>🎯 Goal:</b>
outcome
current → target (deadline: date)
Progress: N% ████░░░░░░

<b>📊 Metrics:</b>
• Subjective: X/10 → Y/10
• Objective: metric: current → target
• Balancing: metric ✅/⚠️

<b>🧪 Hypotheses:</b>

<b>H1: name</b> — 🧪 testing
Evidence: 2/3
Current experiment: description (ends date)
Recommendation: ...

<b>🔴 Red Path (Focus):</b>
→ hypothesis_name: next_action

<b>📋 Active Tasks:</b>
• task — hypothesis — status

<b>💡 Recommendations:</b>
• recommendation_1
• recommendation_2

<b>📅 Next Review:</b> date
"""

    elif parsed.subcommand == HypothesisSubcommand.VALIDATE:
        name = parsed.name or ""
        return f"""{base_context}

TASK: Validate hypothesis map "{name}" for errors.

WORKFLOW:
1. Find and read hypothesis map
2. Check frontmatter completeness
3. Verify all sections present
4. Run error detection patterns:
   - Task instead of Goal
   - Executor instead of Subject
   - BECAUSE not about Subject
   - Premature Specification
   - Motivation not of Subject
   - Orphan Tasks
   - Stale Hypotheses
5. Calculate validation score

OUTPUT FORMAT:
🔍 <b>Validation: map_name</b>

<b>✅ Passed:</b>
• Frontmatter complete
• All required sections present
• Hypothesis structure valid

<b>⚠️ Warnings:</b>
• H2: BECAUSE may be about us, not subject
  Current: "BECAUSE we need revenue"
  Suggest: "BECAUSE subject wants..."

<b>❌ Errors:</b>
• Goal looks like a task: "Implement feature X"
  Suggest: Reframe as outcome

<b>📊 Validation Score:</b> N/100

<b>Actions:</b>
• Fix N errors before proceeding
• Review M warnings
"""

    return parsed.subcommand.value


async def call_claude_processor(prompt: str) -> dict:
    """Call Claude processor with hypothesis prompt.

    Returns:
        Report dict with 'report' or 'error' key
    """
    settings = get_settings()
    processor = ClaudeProcessor(settings.vault_path, settings.todoist_api_key)

    return await asyncio.to_thread(processor.execute_prompt, prompt)


def format_response_for_telegram(report: dict) -> str:
    """Format Claude response for Telegram.

    Uses the standard format_process_report formatter.
    """
    return format_process_report(report)


@router.message(Command("hypothesis"))
async def hypothesis_command_handler(
    message: Message, command: CommandObject, state: FSMContext
) -> None:
    """Handle /hypothesis command with subcommands.

    Subcommands:
        /hypothesis - Show dashboard
        /hypothesis new {domain} - Create new map (business/personal)
        /hypothesis review {name} - Review specific map
        /hypothesis validate {name} - Validate map for errors
    """
    user_id = message.from_user.id if message.from_user else "unknown"
    logger.info("Hypothesis command triggered by user %s with args: %s", user_id, command.args)

    # Parse subcommand
    parsed = parse_subcommand(command.args)
    logger.info("Parsed subcommand: %s", parsed)

    # Special handling for NEW - start EKG session with Claude
    if parsed.subcommand == HypothesisSubcommand.NEW:
        domain = parsed.domain or "business"
        await state.set_state(HypothesisState.ekg_session)
        await state.update_data(domain=domain, history=[])

        status_msg = await message.answer("⏳ Запускаю EKG сессию...")

        # Call Claude to start the EKG session
        prompt = build_ekg_start_prompt(domain)
        report = await run_claude_with_progress(prompt, status_msg, "⏳ Запускаю EKG сессию...")

        # Store Claude's first message in history
        report_text = report.get("report", "")
        await state.update_data(history=[{"role": "assistant", "content": report_text}])

        formatted = format_response_for_telegram(report)
        try:
            await status_msg.edit_text(formatted + "\n\n<i>Для отмены: /cancel</i>")
        except Exception:
            await status_msg.edit_text(formatted, parse_mode=None)
        return

    # Build appropriate prompt
    prompt = build_hypothesis_prompt(parsed)

    # Show progress message
    status_messages = {
        HypothesisSubcommand.DASHBOARD: "⏳ Загружаю hypothesis maps...",
        HypothesisSubcommand.REVIEW: "⏳ Анализирую hypothesis map...",
        HypothesisSubcommand.VALIDATE: "⏳ Проверяю hypothesis map...",
    }
    status_msg = await message.answer(status_messages.get(parsed.subcommand, "⏳ Processing..."))

    report = await run_claude_with_progress(prompt, status_msg, status_messages.get(parsed.subcommand, "⏳ Processing..."))

    # Format and send response
    formatted = format_response_for_telegram(report)
    try:
        await status_msg.edit_text(formatted)
    except Exception:
        # Fallback: send without HTML parsing
        await status_msg.edit_text(formatted, parse_mode=None)


@router.message(Command("cancel"))
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """Cancel current hypothesis creation flow."""
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("Нет активного процесса для отмены.")
        return

    await state.clear()
    await message.answer("❌ Создание hypothesis map отменено.")


@router.message(HypothesisState.ekg_session)
async def handle_ekg_input(message: Message, bot: Bot, state: FSMContext) -> None:
    """Handle user input during EKG session - Claude drives the conversation."""
    user_input = None

    # Handle voice input
    if message.voice:
        await message.chat.do(action="typing")
        settings = get_settings()
        transcriber = DeepgramTranscriber(settings.deepgram_api_key)

        try:
            file = await bot.get_file(message.voice.file_id)
            if not file.file_path:
                await message.answer("❌ Не удалось скачать голосовое")
                return

            file_bytes = await bot.download_file(file.file_path)
            if not file_bytes:
                await message.answer("❌ Не удалось скачать голосовое")
                return

            audio_bytes = file_bytes.read()
            user_input = await transcriber.transcribe(audio_bytes)
        except Exception as e:
            logger.exception("Failed to transcribe voice in EKG session")
            await message.answer(f"❌ Не удалось транскрибировать: {e}")
            return

        if not user_input:
            await message.answer("❌ Не удалось распознать речь")
            return

        # Echo transcription to user
        await message.answer(f"🎤 <i>{user_input}</i>")

    # Handle text input
    elif message.text:
        user_input = message.text.strip()

    else:
        await message.answer("❌ Отправь текст или голосовое сообщение.")
        return

    # Get session data
    data = await state.get_data()
    domain = data.get("domain", "business")
    history = data.get("history", [])

    # Add user message to history
    history.append({"role": "user", "content": user_input})
    await state.update_data(history=history)

    status_msg = await message.answer("⏳ Анализирую...")

    # Build prompt with full conversation history
    prompt = build_ekg_continuation_prompt(domain, history)

    report = await run_claude_with_progress(prompt, status_msg, "⏳ Анализирую...")

    # Check if Claude created the file (session complete)
    report_text = report.get("report", "")
    session_complete = "[EKG_COMPLETE]" in report_text or "vault/hypothesis/" in report_text

    if session_complete:
        await state.clear()
        # Commit changes
        settings = get_settings()
        git = VaultGit(settings.vault_path)
        try:
            await asyncio.to_thread(git.commit_and_push, "feat: create hypothesis map via EKG")
        except Exception as e:
            logger.warning("Failed to commit hypothesis map: %s", e)
    else:
        # Add Claude response to history for next turn
        history.append({"role": "assistant", "content": report_text})
        await state.update_data(history=history)

    # Format and send response
    formatted = format_response_for_telegram(report)
    try:
        await status_msg.edit_text(formatted)
    except Exception:
        await status_msg.edit_text(formatted, parse_mode=None)


async def run_claude_with_progress(prompt: str, status_msg: Message, status_text: str) -> dict:
    """Run Claude processor with progress updates."""
    task = asyncio.create_task(call_claude_processor(prompt))

    elapsed = 0
    while not task.done():
        await asyncio.sleep(30)
        elapsed += 30
        if not task.done():
            try:
                await status_msg.edit_text(f"{status_text} ({elapsed // 60}m {elapsed % 60}s)")
            except Exception:
                pass

    return await task


def build_ekg_start_prompt(domain: str) -> str:
    """Build Claude prompt to start EKG session as authentic facilitator."""
    return f"""Ты — фасилитатор ЭКГ (Экспресс Карта Гипотез) по методологии hypothesismapping.com.

РОЛЬ ФАСИЛИТАТОРА:
- Ты НЕ эксперт, ты методист — следишь за форматом, не даёшь советов по содержанию
- Задаёшь вопросы, помогаешь структурировать мысли клиента
- Ловишь типичные ошибки и мягко направляешь к исправлению
- Не торопишь, даёшь время подумать

КОНТЕКСТ СЕССИИ:
- Domain: {domain}
- Формат: Telegram чат (короткие сообщения)
- Время: ~20-30 минут на всю карту

ПРОЧИТАЙ ДЛЯ КОНТЕКСТА:
1. vault/hypothesis/_schema.md — формат итогового файла
2. vault/goals/ — текущие цели клиента (для связей)
3. vault/hypothesis/{domain}/ — существующие карты (для контекста)

ЭКГ СТРУКТУРА:
1. ЦЕЛЬ — куда хотим прийти (результат, не задача)
2. МЕТРИКИ — как измерим (субъективные 0-10 + объективные числа)
3. СУБЪЕКТ — чьё поведение меняем (автономный агент, не исполнитель)
4. ГИПОТЕЗА — если → то → потому что → тогда
5. ЭКСПЕРИМЕНТ — минимальный тест для проверки

ТИПИЧНЫЕ ОШИБКИ (лови и исправляй):
1. Задача вместо цели: "Внедрить CRM" → спроси "А зачем? Что изменится?"
2. Исполнитель вместо субъекта: "Команда продаж" → "Кто принимает решение покупать?"
3. "Потому что" о нас: "нам нужна выручка" → "Какая боль/желание СУБЪЕКТА?"
4. Преждевременная конкретизация: "Redis с TTL 300" → "Какой принцип, механизм?"
5. Поверхностная мотивация → используй технику "5 ну и что?"

ТЕХНИКИ ФАСИЛИТАЦИИ:
• Goal Shaking (Шатание цели):
  - Преувеличение: "Если достигнем в 10 раз больше — это всё ещё то, чего хочешь?"
  - Вычитание: "Убери X — цель всё ещё важна?"
  - Границы: "До какого предела готов идти ради этого?"
• 5 ну и что?: углубляй мотивацию субъекта
• Red Path: фокус только на приоритетном

ФОРМАТ ОТВЕТА:
- ТОЛЬКО HTML для Telegram: <b>, <i>, <code>
- Никакого markdown: **, ##, ```
- Лаконично — это чат, не документ
- Один вопрос за раз
- Когда карта готова — создай файл и напиши [EKG_COMPLETE]

НАЧНИ СЕССИЮ:
Поприветствуй, объясни что будем делать за 20-30 минут.
Спроси про ЦЕЛЬ — что хочет изменить/достичь.
Не давай примеров сразу — сначала послушай клиента.
"""


def build_ekg_continuation_prompt(domain: str, history: list[dict]) -> str:
    """Build Claude prompt to continue EKG session as authentic facilitator."""
    history_text = "\n".join([
        f"{'КЛИЕНТ' if msg['role'] == 'user' else 'ФАСИЛИТАТОР'}: {msg['content']}"
        for msg in history
    ])

    return f"""Ты — фасилитатор ЭКГ, продолжаешь сессию.

РОЛЬ: Методист, не эксперт. Следишь за форматом, ловишь ошибки, помогаешь структурировать.

ИСТОРИЯ ДИАЛОГА:
{history_text}

КОНТЕКСТ:
- Domain: {domain}
- Читай vault/hypothesis/_schema.md для формата файла
- Читай vault/goals/ для связи с целями клиента

ЭКГ СТРУКТУРА (отслеживай прогресс):
1. ЦЕЛЬ — результат, не задача
2. МЕТРИКИ — субъективные (0-10) + объективные (числа)
3. СУБЪЕКТ — автономный агент, чьё поведение меняем
4. ГИПОТЕЗА — если → то → потому что → тогда
5. ЭКСПЕРИМЕНТ — минимальный тест

ОШИБКИ (ловишь в ответах клиента):
• Задача вместо цели → "А зачем? Что изменится когда сделаешь?"
• Исполнитель вместо субъекта → "Это кто выполняет. А на кого влияем?"
• "Потому что" о нас → "Это наша мотивация. А субъекту-то зачем?"
• Преждевременная конкретизация → "Это уже решение. Какой принцип за ним?"
• Поверхностная мотивация → "Ну и что? Что за этим стоит глубже?"

ТЕХНИКИ:
• Goal Shaking: "Если в 10x — всё ещё хочешь?", "Убери X — важно?", "До какого предела?"
• 5 ну и что?: копай мотивацию глубже
• Если клиент застрял — предложи варианты, но не навязывай

ТВОЯ ЗАДАЧА СЕЙЧАС:
1. Проанализируй последний ответ клиента
2. Если ошибка — мягко укажи, помоги переформулировать
3. Если ОК — подтверди коротко, переходи к следующему элементу
4. Если все элементы собраны:
   - Создай файл vault/hypothesis/{domain}/hm-<slug>.md по _schema.md
   - Обнови vault/MOC/MOC-hypotheses.md
   - Покажи краткое summary карты
   - Напиши [EKG_COMPLETE]

ФОРМАТ:
- HTML: <b>, <i>, <code> — никакого markdown
- Один вопрос/действие за раз
- Лаконично, это чат
"""
