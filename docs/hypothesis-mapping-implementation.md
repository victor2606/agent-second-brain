# HYPOTHESIS_MAPPING_IMPLEMENTATION_PLAN

## META
```yaml
project: agent-second-brain
feature: hypothesis-mapping
source_methodology: https://github.com/Byndyusoft/hypothesismapping
total_tasks: 13
estimated_hours: 26-32
```

---

## PROGRESS

| Task | Title | Status | Completed |
|------|-------|--------|-----------|
| TASK_001 | Create vault/hypothesis/ directory structure | ✅ DONE | 2025-12-31 |
| TASK_002 | Create hypothesis-format.md rule | ✅ DONE | 2025-12-31 |
| TASK_003 | Create MOC-hypotheses.md index | ✅ DONE | 2025-12-31 |
| TASK_004 | Create hypothesis-manager agent | ✅ DONE | 2025-12-31 |
| TASK_005 | Create hypothesis-extractor agent | ✅ DONE | 2025-12-31 |
| TASK_006 | Update CLAUDE.md with hypothesis support | ✅ DONE | 2025-12-31 |
| TASK_007 | Update dbrain-processor with hypothesis detection | ✅ DONE | 2025-12-31 |
| TASK_008 | Update goal-aligner with hypothesis alignment | ✅ DONE | 2025-12-31 |
| TASK_009 | Update weekly-digest with hypothesis section | ✅ DONE | 2025-12-31 |
| TASK_010 | Create hypothesis.py Telegram handler | ✅ DONE | 2025-12-31 |
| TASK_011 | Register hypothesis router in main.py | ✅ DONE | 2025-12-31 |
| TASK_012 | Integration test - Telegram flow | ⏳ TODO | — |
| TASK_013 | Integration test - hypothesis detection | ⏳ TODO | — |

**Progress: 11/13 tasks completed (85%)**

---

## METHODOLOGY_REFERENCE

```yaml
elements:
  goal:
    - outcome_description
    - metrics: current → target + deadline
    - balancing_metrics: "≤ X" or "≥ Y"

  subject:
    - who: autonomous_agent (NOT executor)
    - pains: list
    - desires: list
    - current_behavior: string
    - personal_strategy_subjects: ["я", "я-предприниматель", "я-отец", "родственники"]

  hypothesis:
    structure:
      IF: our_intervention (principle, not details)
      THEN: subject_behavior_change
      BECAUSE: link_to_pain_or_desire
      RESULTING_IN: metric_impact
    statuses: [idea, testing, validated, invalidated, paused]
    validation_rules:
      validated: min_3_evidence
      invalidated: min_2_failed_experiments

  task:
    - always_linked_to_hypothesis
    - orphan_tasks = no_strategic_value

common_errors:
  - task_instead_of_goal
  - executor_instead_of_subject
  - because_not_about_subject
  - premature_specification
  - motivation_not_of_subject

techniques:
  - EKG: express_map_20-30_min
  - red_path: priority_chains_only
  - goal_shaking: clarification_via_exaggeration

personal_strategy:
  metrics_structure:
    upper_level: subjective (0-10)
    lower_level: objective (numbers)
    rule: NEVER_MIX_ON_SAME_LEVEL
```

---

## TASK_LIST

### TASK_001
```yaml
id: TASK_001
title: Create vault/hypothesis/ directory structure
estimated_hours: 1
priority: 1

description: |
  Create hypothesis directory with subdirectories for personal and business maps.
  Create _schema.md with full format documentation and examples.

actions:
  - mkdir vault/hypothesis/
  - mkdir vault/hypothesis/personal/
  - mkdir vault/hypothesis/business/
  - mkdir vault/hypothesis/archive/
  - create vault/hypothesis/_schema.md

context_files:
  read:
    - /Users/viktorprohorov/.claude/plans/vivid-squishing-stream.md
  reference:
    - vault/goals/0-vision-3y.md
    - vault/goals/1-yearly-2026.md

success_criteria:
  - EXISTS: vault/hypothesis/_schema.md
  - EXISTS: vault/hypothesis/personal/
  - EXISTS: vault/hypothesis/business/
  - EXISTS: vault/hypothesis/archive/
  - CONTAINS vault/hypothesis/_schema.md:
      - frontmatter_template
      - goal_section_with_subjective_and_objective_metrics
      - balancing_metrics_table
      - subject_template_with_pains_desires
      - hypothesis_IF_THEN_BECAUSE_RESULTING_structure
      - evidence_criteria_checklist
      - tasks_table
      - blockers_table
      - notes_section
      - review_log_table
      - business_example
      - personal_example

output_artifact: vault/hypothesis/_schema.md
```

### TASK_002
```yaml
id: TASK_002
title: Create hypothesis-format.md rule
estimated_hours: 1
priority: 2
depends_on: [TASK_001]

description: |
  Create Claude rule for validating hypothesis map format.
  Include error detection patterns from methodology.

actions:
  - create vault/.claude/rules/hypothesis-format.md

context_files:
  read:
    - vault/hypothesis/_schema.md
    - vault/.claude/rules/goals-format.md
    - vault/.claude/rules/daily-format.md
  reference:
    - /Users/viktorprohorov/.claude/plans/vivid-squishing-stream.md

success_criteria:
  - EXISTS: vault/.claude/rules/hypothesis-format.md
  - CONTAINS:
      - paths: "hypothesis/**/*.md"
      - required_frontmatter_fields: [type, domain, status, created, updated, review_cadence, next_review, linked_goals]
      - required_sections: [Goal, Subjects, Hypotheses, Tasks, Blockers, Notes, Review Log]
      - hypothesis_status_transitions
      - evidence_requirements_for_validated
      - evidence_requirements_for_invalidated
      - naming_convention
      - error_detection_patterns:
          - task_instead_of_goal
          - executor_instead_of_subject
          - because_not_about_subject
          - premature_specification

output_artifact: vault/.claude/rules/hypothesis-format.md
```

### TASK_003
```yaml
id: TASK_003
title: Create MOC-hypotheses.md index
estimated_hours: 0.5
priority: 3
depends_on: [TASK_001]

description: |
  Create Map of Content for hypothesis maps.
  Dynamic index that lists all active/paused/archived maps.

actions:
  - create vault/MOC/MOC-hypotheses.md

context_files:
  read:
    - vault/MOC/MOC-thoughts.md
    - vault/hypothesis/_schema.md

success_criteria:
  - EXISTS: vault/MOC/MOC-hypotheses.md
  - CONTAINS:
      - sections: [Active Maps, Paused Maps, Archived Maps]
      - instructions_for_adding_new_maps
      - link_format_examples

output_artifact: vault/MOC/MOC-hypotheses.md
```

### TASK_004
```yaml
id: TASK_004
title: Create hypothesis-manager agent
estimated_hours: 4
priority: 4
depends_on: [TASK_001, TASK_002]

description: |
  Create main agent for hypothesis map management.
  Implements EKG technique, error validation, experiment design, result analysis.

actions:
  - create vault/.claude/agents/hypothesis-manager.md

context_files:
  read:
    - vault/hypothesis/_schema.md
    - vault/.claude/rules/hypothesis-format.md
    - vault/.claude/agents/goal-aligner.md
    - vault/.claude/agents/weekly-digest.md
  reference:
    - /Users/viktorprohorov/.claude/plans/vivid-squishing-stream.md
    - vault/.claude/CLAUDE.md

success_criteria:
  - EXISTS: vault/.claude/agents/hypothesis-manager.md
  - CONTAINS:
      - frontmatter: name, description
      - commands:
          - /hypothesis: dashboard
          - /hypothesis new {domain}: create_map_EKG
          - /hypothesis review {name}: review_map
          - /hypothesis validate {name}: error_check
      - functions:
          - goal_formulation_with_shaking_technique
          - IF_THEN_BECAUSE_RESULTING_structure_check
          - error_validation:
              - task_instead_of_goal
              - executor_instead_of_subject
              - because_not_about_subject
              - premature_specification
          - experiment_design:
              - minimal_test
              - success_failure_criteria
              - sample_size
              - timeline
          - result_analysis:
              - evidence_sufficiency_check
              - scale_pivot_pause_recommendations
              - learnings_update
          - strategic_cadence:
              - weekly_review_workflow
              - red_path_prioritization
      - prompts:
          - goal_clarification_prompt
          - subject_identification_prompt
          - hypothesis_formulation_prompt
          - experiment_design_prompt
          - result_analysis_prompt
      - output_formats:
          - dashboard_html
          - review_html

output_artifact: vault/.claude/agents/hypothesis-manager.md
```

### TASK_005
```yaml
id: TASK_005
title: Create hypothesis-extractor agent
estimated_hours: 2
priority: 5
depends_on: [TASK_001]

description: |
  Create agent for detecting hypothesis signals in daily entries.
  Extracts and structures potential hypotheses from raw text.

actions:
  - create vault/.claude/agents/hypothesis-extractor.md

context_files:
  read:
    - vault/hypothesis/_schema.md
    - vault/.claude/agents/inbox-processor.md
    - vault/.claude/skills/dbrain-processor/SKILL.md
  reference:
    - /Users/viktorprohorov/.claude/plans/vivid-squishing-stream.md

success_criteria:
  - EXISTS: vault/.claude/agents/hypothesis-extractor.md
  - CONTAINS:
      - frontmatter: name, description
      - detection_patterns:
          - intervention_signals: ["если мы", "думаю что", "гипотеза:", "предположение"]
          - target_signals: ["с X до Y", "увеличить на", "достичь"]
          - causal_signals: ["потому что", "из-за того что", "поэтому"]
          - subject_signals: ["клиенты говорят", "пользователи хотят", "они делают"]
      - extraction_logic:
          - identify_intervention
          - identify_behavior_change
          - identify_motivation
          - identify_metric_impact
      - output_format:
          - source_reference
          - raw_text
          - structured_draft: IF_THEN_BECAUSE_RESULTING
          - suggested_target_hm
          - action_options

output_artifact: vault/.claude/agents/hypothesis-extractor.md
```

### TASK_006
```yaml
id: TASK_006
title: Update CLAUDE.md with hypothesis support
estimated_hours: 1
priority: 6
depends_on: [TASK_004, TASK_005]

description: |
  Update main system prompt to include hypothesis mapping.
  Add directory, commands, agent references.

actions:
  - edit vault/.claude/CLAUDE.md

context_files:
  read:
    - vault/.claude/CLAUDE.md
    - vault/.claude/agents/hypothesis-manager.md
    - vault/.claude/agents/hypothesis-extractor.md

success_criteria:
  - MODIFIED: vault/.claude/CLAUDE.md
  - CONTAINS:
      - directory_structure:
          - "hypothesis/": "Hypothesis Maps by domain"
      - quick_commands:
          - "/hypothesis": "Manage hypothesis maps"
      - available_agents:
          - "hypothesis-manager": "Create and review hypothesis maps"
          - "hypothesis-extractor": "Detect hypotheses in entries"

output_artifact: vault/.claude/CLAUDE.md (modified)
```

### TASK_007
```yaml
id: TASK_007
title: Update dbrain-processor with hypothesis detection
estimated_hours: 3
priority: 7
depends_on: [TASK_005]

description: |
  Integrate hypothesis signal detection into daily processing.
  Add hypothesis context loading and report section.

actions:
  - edit vault/.claude/skills/dbrain-processor/SKILL.md

context_files:
  read:
    - vault/.claude/skills/dbrain-processor/SKILL.md
    - vault/.claude/agents/hypothesis-extractor.md
    - vault/hypothesis/_schema.md

success_criteria:
  - MODIFIED: vault/.claude/skills/dbrain-processor/SKILL.md
  - CONTAINS:
      - step_0_hypothesis_context:
          - read_active_hypothesis_maps
          - extract_active_hypotheses
          - extract_current_experiments
      - classification_update:
          - hypothesis_signal_detection_branch
          - flag_for_hypothesis_extractor
      - html_report_section:
          - hypothesis_activity:
              - active_hm_count
              - hypotheses_in_testing
              - this_week_experiments
          - hypothesis_signals:
              - detected_signals_list
              - suggested_actions

output_artifact: vault/.claude/skills/dbrain-processor/SKILL.md (modified)
```

### TASK_008
```yaml
id: TASK_008
title: Update goal-aligner with hypothesis alignment
estimated_hours: 2
priority: 8
depends_on: [TASK_004]

description: |
  Add hypothesis-goal alignment checks.
  Detect stale hypotheses and orphan experiments.

actions:
  - edit vault/.claude/agents/goal-aligner.md

context_files:
  read:
    - vault/.claude/agents/goal-aligner.md
    - vault/hypothesis/_schema.md
    - vault/.claude/agents/hypothesis-manager.md

success_criteria:
  - MODIFIED: vault/.claude/agents/goal-aligner.md
  - CONTAINS:
      - hypothesis_alignment_check:
          - hypothesis_to_monthly_priority_link
          - hypothesis_to_weekly_task_link
          - active_experiment_to_weekly_task_link
      - stale_hypothesis_detection:
          - threshold: 14_days_without_activity
          - warning_format
      - report_section:
          - hypothesis_goal_alignment_status
          - stale_hypotheses_list

output_artifact: vault/.claude/agents/goal-aligner.md (modified)
```

### TASK_009
```yaml
id: TASK_009
title: Update weekly-digest with hypothesis section
estimated_hours: 2
priority: 9
depends_on: [TASK_004]

description: |
  Add hypothesis progress section to weekly digest.
  Include experiments, learnings, recommendations.

actions:
  - edit vault/.claude/agents/weekly-digest.md

context_files:
  read:
    - vault/.claude/agents/weekly-digest.md
    - vault/hypothesis/_schema.md
    - vault/.claude/agents/hypothesis-manager.md

success_criteria:
  - MODIFIED: vault/.claude/agents/weekly-digest.md
  - CONTAINS:
      - hypothesis_data_collection:
          - read_active_hypothesis_maps
          - check_experiments_completed
          - check_evidence_collected
          - evaluate_status_changes
      - report_section:
          - hypothesis_progress:
              - per_hm_summary: goal_current_target_delta
              - hypotheses_status_counts
              - this_week_experiments
          - validated_this_week
          - invalidated_this_week
          - next_week_experiments
          - recommendations

output_artifact: vault/.claude/agents/weekly-digest.md (modified)
```

### TASK_010
```yaml
id: TASK_010
title: Create hypothesis.py Telegram handler
estimated_hours: 4
priority: 10
depends_on: [TASK_004]

description: |
  Create Telegram handler for /hypothesis commands.
  Integrate with ClaudeProcessor for AI operations.

actions:
  - create src/d_brain/bot/handlers/hypothesis.py

context_files:
  read:
    - src/d_brain/bot/handlers/process.py
    - src/d_brain/bot/handlers/do.py
    - src/d_brain/bot/handlers/weekly.py
    - src/d_brain/services/processor.py
    - src/d_brain/bot/main.py
  reference:
    - vault/.claude/agents/hypothesis-manager.md

success_criteria:
  - EXISTS: src/d_brain/bot/handlers/hypothesis.py
  - CONTAINS:
      - router: Router()
      - commands:
          - /hypothesis: show_dashboard
          - /hypothesis new {domain}: create_new_hm
          - /hypothesis review {name}: review_hm
      - functions:
          - hypothesis_command_handler
          - parse_subcommand
          - call_claude_processor_with_hypothesis_manager_agent
          - format_response_for_telegram
      - imports:
          - aiogram
          - ClaudeProcessor
          - VaultStorage

output_artifact: src/d_brain/bot/handlers/hypothesis.py
```

### TASK_011
```yaml
id: TASK_011
title: Register hypothesis router in main.py
estimated_hours: 0.5
priority: 11
depends_on: [TASK_010]

description: |
  Register hypothesis handler router in bot main.py.

actions:
  - edit src/d_brain/bot/main.py

context_files:
  read:
    - src/d_brain/bot/main.py
    - src/d_brain/bot/handlers/hypothesis.py

success_criteria:
  - MODIFIED: src/d_brain/bot/main.py
  - CONTAINS:
      - import: from .handlers.hypothesis import router as hypothesis_router
      - registration: dp.include_router(hypothesis_router)

output_artifact: src/d_brain/bot/main.py (modified)
```

### TASK_012
```yaml
id: TASK_012
title: Integration test - create sample HM via Telegram
estimated_hours: 2
priority: 12
depends_on: [TASK_011]

description: |
  Test full flow: /hypothesis new business → create map → /hypothesis review.
  Verify all components work together.

actions:
  - test /hypothesis command
  - test /hypothesis new business
  - verify map created in vault/hypothesis/business/
  - test /hypothesis review {created_map}
  - verify HTML report in Telegram

context_files:
  read:
    - src/d_brain/bot/handlers/hypothesis.py
    - vault/.claude/agents/hypothesis-manager.md
    - vault/hypothesis/_schema.md

success_criteria:
  - COMMAND /hypothesis returns dashboard HTML
  - COMMAND /hypothesis new business:
      - prompts for goal
      - prompts for subjects
      - creates file in vault/hypothesis/business/
      - file matches _schema.md format
  - COMMAND /hypothesis review {name}:
      - returns review HTML
      - includes status, metrics, recommendations
  - NO_ERRORS in bot logs
  - NO_ERRORS in claude processor

output_artifact: test_results_log
```

### TASK_013
```yaml
id: TASK_013
title: Integration test - hypothesis detection in /process
estimated_hours: 2
priority: 13
depends_on: [TASK_007, TASK_012]

description: |
  Test hypothesis signal detection during daily processing.
  Verify signals appear in HTML report.

actions:
  - add test entry with hypothesis signal to daily file
  - run /process
  - verify hypothesis signal detected in report
  - verify suggestion to add to HM or create new

context_files:
  read:
    - vault/.claude/skills/dbrain-processor/SKILL.md
    - vault/.claude/agents/hypothesis-extractor.md
    - vault/daily/{today}.md

success_criteria:
  - TEST_ENTRY contains hypothesis signal pattern
  - REPORT contains "Hypothesis Signals" section
  - REPORT shows extracted IF_THEN_BECAUSE_RESULTING draft
  - REPORT suggests target HM or /hypothesis new

output_artifact: test_results_log
```

---

## DEPENDENCY_GRAPH

```
TASK_001 (structure)
    ├── TASK_002 (rule) ─────────────────┐
    ├── TASK_003 (MOC)                   │
    └── TASK_005 (extractor) ────────────┤
                                         │
TASK_001 + TASK_002 ─────────────────────┼── TASK_004 (manager)
                                         │       │
                                         │       ├── TASK_006 (CLAUDE.md)
                                         │       ├── TASK_008 (goal-aligner)
                                         │       ├── TASK_009 (weekly-digest)
                                         │       └── TASK_010 (telegram handler)
                                         │               │
TASK_005 ────────────────────────────────┼── TASK_007 (dbrain-processor)
                                         │               │
                                         │       TASK_011 (register router)
                                         │               │
                                         │       TASK_012 (test telegram)
                                         │               │
                                         └────── TASK_013 (test detection)
```

## EXECUTION_ORDER

```yaml
phase_1_foundation:
  parallel:
    - TASK_001  # 1h
  then:
    - TASK_002  # 1h
    - TASK_003  # 0.5h
    - TASK_005  # 2h

phase_2_core_agent:
  sequential:
    - TASK_004  # 4h (depends on TASK_001, TASK_002)

phase_3_integrations:
  parallel:
    - TASK_006  # 1h
    - TASK_007  # 3h
    - TASK_008  # 2h
    - TASK_009  # 2h
    - TASK_010  # 4h

phase_4_telegram:
  sequential:
    - TASK_011  # 0.5h

phase_5_testing:
  sequential:
    - TASK_012  # 2h
    - TASK_013  # 2h

total_estimated: 26-32h
```
