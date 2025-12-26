"""Claude processing service."""

import json
import logging
import os
import subprocess
from datetime import date
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 1200  # 20 minutes


class ClaudeProcessor:
    """Service for triggering Claude Code processing."""

    def __init__(self, vault_path: Path, todoist_api_key: str = "") -> None:
        self.vault_path = Path(vault_path)
        self.todoist_api_key = todoist_api_key
        self._mcp_config_path = (self.vault_path.parent / "mcp-config.json").resolve()

    def _load_skill_content(self) -> str:
        """Load dbrain-processor skill content for inclusion in prompt.

        NOTE: @vault/ references don't work in --print mode,
        so we must include skill content directly in the prompt.
        """
        skill_path = self.vault_path / ".claude/skills/dbrain-processor/SKILL.md"
        if skill_path.exists():
            return skill_path.read_text()
        return ""

    def _load_todoist_reference(self) -> str:
        """Load Todoist reference for inclusion in prompt."""
        ref_path = self.vault_path / ".claude/skills/dbrain-processor/references/todoist.md"
        if ref_path.exists():
            return ref_path.read_text()
        return ""

    def _html_to_markdown(self, html: str) -> str:
        """Convert Telegram HTML to Obsidian Markdown."""
        import re

        text = html
        # <b>text</b> → **text**
        text = re.sub(r"<b>(.*?)</b>", r"**\1**", text)
        # <i>text</i> → *text*
        text = re.sub(r"<i>(.*?)</i>", r"*\1*", text)
        # <code>text</code> → `text`
        text = re.sub(r"<code>(.*?)</code>", r"`\1`", text)
        # <s>text</s> → ~~text~~
        text = re.sub(r"<s>(.*?)</s>", r"~~\1~~", text)
        # Remove <u> (no Markdown equivalent, just keep text)
        text = re.sub(r"</?u>", "", text)
        # <a href="url">text</a> → [text](url)
        text = re.sub(r'<a href="([^"]+)">([^<]+)</a>', r"[\2](\1)", text)

        return text

    def _save_weekly_summary(self, report_html: str, week_date: date) -> Path:
        """Save weekly summary to vault/summaries/YYYY-WXX-summary.md."""
        # Calculate ISO week number
        year, week, _ = week_date.isocalendar()
        filename = f"{year}-W{week:02d}-summary.md"
        summary_path = self.vault_path / "summaries" / filename

        # Convert HTML to Markdown for Obsidian
        content = self._html_to_markdown(report_html)

        # Add frontmatter
        frontmatter = f"""---
date: {week_date.isoformat()}
type: weekly-summary
week: {year}-W{week:02d}
---

"""
        summary_path.write_text(frontmatter + content)
        logger.info("Weekly summary saved to %s", summary_path)
        return summary_path

    def _update_weekly_moc(self, summary_path: Path) -> None:
        """Add link to new summary in MOC-weekly.md."""
        moc_path = self.vault_path / "MOC" / "MOC-weekly.md"
        if moc_path.exists():
            content = moc_path.read_text()
            link = f"- [[summaries/{summary_path.name}|{summary_path.stem}]]"
            # Insert after "## Previous Weeks" if not already there
            if summary_path.stem not in content:
                content = content.replace(
                    "## Previous Weeks\n",
                    f"## Previous Weeks\n\n{link}\n",
                )
                moc_path.write_text(content)
                logger.info("Updated MOC-weekly.md with link to %s", summary_path.stem)

    def process_daily(self, day: date | None = None) -> dict[str, Any]:
        """Process daily file with Claude.

        Args:
            day: Date to process (default: today)

        Returns:
            Processing report as dict
        """
        if day is None:
            day = date.today()

        daily_file = self.vault_path / "daily" / f"{day.isoformat()}.md"

        if not daily_file.exists():
            logger.warning("No daily file for %s", day)
            return {
                "error": f"No daily file for {day}",
                "processed_entries": 0,
            }

        # Load skill content directly (@ references don't work in --print mode)
        skill_content = self._load_skill_content()

        prompt = f"""Сегодня {day}. Выполни ежедневную обработку.

=== SKILL INSTRUCTIONS ===
{skill_content}
=== END SKILL ===

ПЕРВЫМ ДЕЛОМ: вызови mcp__todoist__user-info чтобы убедиться что MCP работает.

CRITICAL MCP RULE:
- ТЫ ИМЕЕШЬ ДОСТУП к mcp__todoist__* tools — ВЫЗЫВАЙ ИХ НАПРЯМУЮ
- НИКОГДА не пиши "MCP недоступен" или "добавь вручную"
- Для задач: вызови mcp__todoist__add-tasks tool
- Если tool вернул ошибку — покажи ТОЧНУЮ ошибку в отчёте

CRITICAL OUTPUT FORMAT:
- Return ONLY raw HTML for Telegram (parse_mode=HTML)
- NO markdown: no **, no ## , no ```, no tables
- Start directly with 📊 <b>Обработка за {day}</b>
- Allowed tags: <b>, <i>, <code>, <s>, <u>
- If entries already processed, return status report in same HTML format"""

        try:
            # Pass TODOIST_API_KEY to Claude subprocess
            env = os.environ.copy()
            if self.todoist_api_key:
                env["TODOIST_API_KEY"] = self.todoist_api_key

            result = subprocess.run(
                [
                    "/home/shima/.local/bin/claude",
                    "--print",
                    "--dangerously-skip-permissions",
                    "--mcp-config",
                    str(self._mcp_config_path),
                    "-p",
                    prompt,
                ],
                cwd=self.vault_path.parent,
                capture_output=True,
                text=True,
                timeout=DEFAULT_TIMEOUT,
                check=False,
                env=env,
            )

            if result.returncode != 0:
                logger.error("Claude processing failed: %s", result.stderr)
                return {
                    "error": result.stderr or "Claude processing failed",
                    "processed_entries": 0,
                }

            # Return human-readable output
            output = result.stdout.strip()
            return {
                "report": output,
                "processed_entries": 1,  # успешно обработано
            }

        except subprocess.TimeoutExpired:
            logger.error("Claude processing timed out")
            return {
                "error": "Processing timed out",
                "processed_entries": 0,
            }
        except FileNotFoundError:
            logger.error("Claude CLI not found")
            return {
                "error": "Claude CLI not installed",
                "processed_entries": 0,
            }
        except Exception as e:
            logger.exception("Unexpected error during processing")
            return {
                "error": str(e),
                "processed_entries": 0,
            }

    def execute_prompt(self, user_prompt: str) -> dict[str, Any]:
        """Execute arbitrary prompt with Claude.

        Args:
            user_prompt: User's natural language request

        Returns:
            Execution report as dict
        """
        today = date.today()

        # Load todoist reference for task operations
        todoist_ref = self._load_todoist_reference()

        prompt = f"""Ты - персональный ассистент d-brain.

CONTEXT:
- Текущая дата: {today}
- Vault path: {self.vault_path}

=== TODOIST REFERENCE ===
{todoist_ref}
=== END REFERENCE ===

ПЕРВЫМ ДЕЛОМ: вызови mcp__todoist__user-info чтобы убедиться что MCP работает.

CRITICAL MCP RULE:
- ТЫ ИМЕЕШЬ ДОСТУП к mcp__todoist__* tools — ВЫЗЫВАЙ ИХ НАПРЯМУЮ
- НИКОГДА не пиши "MCP недоступен" или "добавь вручную"
- Если tool вернул ошибку — покажи ТОЧНУЮ ошибку в отчёте

USER REQUEST:
{user_prompt}

CRITICAL OUTPUT FORMAT:
- Return ONLY raw HTML for Telegram (parse_mode=HTML)
- NO markdown: no **, no ##, no ```, no tables, no -
- Start with emoji and <b>header</b>
- Allowed tags: <b>, <i>, <code>, <s>, <u>
- Be concise - Telegram has 4096 char limit

EXECUTION:
1. Analyze the request
2. Call MCP tools directly (mcp__todoist__*, read/write files)
3. Return HTML status report with results"""

        try:
            env = os.environ.copy()
            if self.todoist_api_key:
                env["TODOIST_API_KEY"] = self.todoist_api_key

            result = subprocess.run(
                [
                    "/home/shima/.local/bin/claude",
                    "--print",
                    "--dangerously-skip-permissions",
                    "--mcp-config",
                    str(self._mcp_config_path),
                    "-p",
                    prompt,
                ],
                cwd=self.vault_path.parent,
                capture_output=True,
                text=True,
                timeout=DEFAULT_TIMEOUT,
                check=False,
                env=env,
            )

            if result.returncode != 0:
                logger.error("Claude execution failed: %s", result.stderr)
                return {
                    "error": result.stderr or "Claude execution failed",
                    "processed_entries": 0,
                }

            return {
                "report": result.stdout.strip(),
                "processed_entries": 1,
            }

        except subprocess.TimeoutExpired:
            logger.error("Claude execution timed out")
            return {"error": "Execution timed out", "processed_entries": 0}
        except FileNotFoundError:
            logger.error("Claude CLI not found")
            return {"error": "Claude CLI not installed", "processed_entries": 0}
        except Exception as e:
            logger.exception("Unexpected error during execution")
            return {"error": str(e), "processed_entries": 0}

    def generate_weekly(self) -> dict[str, Any]:
        """Generate weekly digest with Claude.

        Returns:
            Weekly digest report as dict
        """
        today = date.today()

        prompt = f"""Сегодня {today}. Сгенерируй недельный дайджест.

ПЕРВЫМ ДЕЛОМ: вызови mcp__todoist__user-info чтобы убедиться что MCP работает.

CRITICAL MCP RULE:
- ТЫ ИМЕЕШЬ ДОСТУП к mcp__todoist__* tools — ВЫЗЫВАЙ ИХ НАПРЯМУЮ
- НИКОГДА не пиши "MCP недоступен" или "добавь вручную"
- Для выполненных задач: вызови mcp__todoist__find-completed-tasks tool
- Если tool вернул ошибку — покажи ТОЧНУЮ ошибку в отчёте

WORKFLOW:
1. Собери данные за неделю (daily файлы в vault/daily/, completed tasks через MCP)
2. Проанализируй прогресс по целям (goals/3-weekly.md)
3. Определи победы и вызовы
4. Сгенерируй HTML отчёт

CRITICAL OUTPUT FORMAT:
- Return ONLY raw HTML for Telegram (parse_mode=HTML)
- NO markdown: no **, no ##, no ```, no tables
- Start with 📅 <b>Недельный дайджест</b>
- Allowed tags: <b>, <i>, <code>, <s>, <u>
- Be concise - Telegram has 4096 char limit"""

        try:
            env = os.environ.copy()
            if self.todoist_api_key:
                env["TODOIST_API_KEY"] = self.todoist_api_key

            result = subprocess.run(
                [
                    "/home/shima/.local/bin/claude",
                    "--print",
                    "--dangerously-skip-permissions",
                    "--mcp-config",
                    str(self._mcp_config_path),
                    "-p",
                    prompt,
                ],
                cwd=self.vault_path.parent,
                capture_output=True,
                text=True,
                timeout=DEFAULT_TIMEOUT,
                check=False,
                env=env,
            )

            if result.returncode != 0:
                logger.error("Weekly digest failed: %s", result.stderr)
                return {
                    "error": result.stderr or "Weekly digest failed",
                    "processed_entries": 0,
                }

            output = result.stdout.strip()

            # Save to summaries/ and update MOC
            try:
                summary_path = self._save_weekly_summary(output, today)
                self._update_weekly_moc(summary_path)
            except Exception as e:
                logger.warning("Failed to save weekly summary: %s", e)

            return {
                "report": output,
                "processed_entries": 1,
            }

        except subprocess.TimeoutExpired:
            logger.error("Weekly digest timed out")
            return {"error": "Weekly digest timed out", "processed_entries": 0}
        except FileNotFoundError:
            logger.error("Claude CLI not found")
            return {"error": "Claude CLI not installed", "processed_entries": 0}
        except Exception as e:
            logger.exception("Unexpected error during weekly digest")
            return {"error": str(e), "processed_entries": 0}
