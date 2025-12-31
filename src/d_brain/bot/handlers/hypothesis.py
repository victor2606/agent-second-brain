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

    waiting_for_goal = State()
    waiting_for_metrics = State()
    waiting_for_subject = State()
    waiting_for_hypothesis = State()


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

    # Build appropriate prompt
    prompt = build_hypothesis_prompt(parsed)

    # Show progress message
    status_messages = {
        HypothesisSubcommand.DASHBOARD: "⏳ Загружаю hypothesis maps...",
        HypothesisSubcommand.NEW: "⏳ Подготавливаю создание hypothesis map...",
        HypothesisSubcommand.REVIEW: "⏳ Анализирую hypothesis map...",
        HypothesisSubcommand.VALIDATE: "⏳ Проверяю hypothesis map...",
    }
    status_msg = await message.answer(status_messages.get(parsed.subcommand, "⏳ Processing..."))

    # Run Claude with progress updates
    async def run_with_progress() -> dict:
        task = asyncio.create_task(call_claude_processor(prompt))

        elapsed = 0
        while not task.done():
            await asyncio.sleep(30)
            elapsed += 30
            if not task.done():
                try:
                    await status_msg.edit_text(
                        f"{status_messages.get(parsed.subcommand, '⏳ Processing...')} "
                        f"({elapsed // 60}m {elapsed % 60}s)"
                    )
                except Exception:
                    pass

        return await task

    report = await run_with_progress()

    # Commit changes if new map was created
    if parsed.subcommand == HypothesisSubcommand.NEW and "error" not in report:
        settings = get_settings()
        git = VaultGit(settings.vault_path)
        try:
            await asyncio.to_thread(git.commit_and_push, "feat: create hypothesis map")
        except Exception as e:
            logger.warning("Failed to commit hypothesis map: %s", e)

    # Format and send response
    formatted = format_response_for_telegram(report)
    try:
        await status_msg.edit_text(formatted)
    except Exception:
        # Fallback: send without HTML parsing
        await status_msg.edit_text(formatted, parse_mode=None)
