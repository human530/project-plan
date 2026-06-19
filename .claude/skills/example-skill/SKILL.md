---
name: example-skill
description: An example/template skill demonstrating the structure of a Claude Code skill. Use this as a starting point when creating new skills — copy the folder, rename it, and replace the instructions below. Triggers when the user asks to see a skill template or to scaffold a new skill.
---

# Example Skill

This is a template skill. It shows the minimal structure every Claude Code
skill needs and explains how the harness loads and runs it. Copy this folder
to create your own skill.

## What a skill is

A skill is a directory under `.claude/skills/<name>/` containing a `SKILL.md`
file. The file has:

1. **YAML frontmatter** — `name` and `description` (required). The `name` must
   match the directory name. The `description` is what Claude reads to decide
   when to invoke the skill, so make it specific about *what* the skill does
   and *when* to use it.
2. **Markdown body** — the instructions Claude follows once the skill is
   invoked. Write these as clear, imperative steps.

## How to use this template

1. Copy the directory: `cp -r .claude/skills/example-skill .claude/skills/my-skill`
2. Rename the skill in the frontmatter `name:` field to match the new
   directory (`my-skill`).
3. Rewrite the `description:` so it precisely captures when the skill should
   trigger.
4. Replace the steps below with your own workflow.

## Steps

When this skill is invoked:

1. Confirm the user's intent and gather any inputs you need.
2. Perform the task described by the skill's instructions.
3. Summarize what was done and surface any follow-ups.

## Supporting files (optional)

A skill can ship extra files alongside `SKILL.md` — scripts, templates,
reference docs — and reference them by relative path from the skill
directory. Keep them small and focused so the skill stays easy to read.
