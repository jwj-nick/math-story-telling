#!/usr/bin/env bash
# sync-skills.sh — 10_system/30_skills/ + 10_system/35_agents/ → .claude/ 단방향 동기화
#
# SSOT: 10_system/30_skills/<skill>/, 10_system/35_agents/<agent>.md
# Mirror: .claude/skills/<skill>/, .claude/agents/<agent>.md
#
# 방향: 10_system → .claude (단방향)
# 역방향 금지: .claude/에서 직접 수정한 내용은 이 스크립트 실행 시 덮어쓰임.
#
# 사용 (어디서 실행해도 동일):
#   bash 70_tools/sync-skills.sh           # 실행
#   bash 70_tools/sync-skills.sh --dry     # dry run only
#
# 동작:
#   - 10_system/30_skills/<skill>/ → .claude/skills/<skill>/ (cp -r 덮어쓰기)
#   - 10_system/35_agents/<file>.md → .claude/agents/<file>.md
#   - 새 파일은 추가, 기존 파일은 갱신, 삭제된 파일은 동기화 안 함 (mirror 모드 아님)
#
# 안전:
#   - SOURCE가 비어있으면 중단 (실수로 mirror 다 지우는 사고 방지)
#   - DEST가 없으면 mkdir -p

set -euo pipefail

# repo root는 이 스크립트 위치의 상위 (70_tools/의 부모)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

SKILLS_SRC="$ROOT/10_system/30_skills"
SKILLS_DST="$ROOT/.claude/skills"
AGENTS_SRC="$ROOT/10_system/35_agents"
AGENTS_DST="$ROOT/.claude/agents"

DRY_RUN=0
if [[ "${1:-}" == "--dry" ]]; then
  DRY_RUN=1
fi

sync_skills() {
  if [[ ! -d "$SKILLS_SRC" ]]; then
    echo "[sync] SKILLS_SRC 없음: $SKILLS_SRC — skip"
    return 0
  fi

  shopt -s nullglob
  local skill_dirs=("$SKILLS_SRC"/*/)
  if [[ ${#skill_dirs[@]} -eq 0 ]]; then
    echo "[sync] 10_system/30_skills/ 에 skill이 없습니다. (0개)"
    return 0
  fi

  mkdir -p "$SKILLS_DST"

  for skill_dir in "${skill_dirs[@]}"; do
    local skill_name
    skill_name="$(basename "$skill_dir")"
    local target="$SKILLS_DST/$skill_name"

    if [[ $DRY_RUN -eq 1 ]]; then
      echo "[dry] skill: $skill_name → $target"
    else
      echo "[sync] skill: $skill_name"
      cp -r "$skill_dir." "$target/"
    fi
  done
  echo "[sync] skills 완료. ${#skill_dirs[@]}개."
}

sync_agents() {
  if [[ ! -d "$AGENTS_SRC" ]]; then
    echo "[sync] AGENTS_SRC 없음: $AGENTS_SRC — skip"
    return 0
  fi

  shopt -s nullglob
  local agent_files=("$AGENTS_SRC"/*.md)
  if [[ ${#agent_files[@]} -eq 0 ]]; then
    echo "[sync] 10_system/35_agents/ 에 agent .md가 없습니다. (0개)"
    return 0
  fi

  mkdir -p "$AGENTS_DST"

  for agent_file in "${agent_files[@]}"; do
    local agent_name
    agent_name="$(basename "$agent_file")"
    local target="$AGENTS_DST/$agent_name"

    if [[ $DRY_RUN -eq 1 ]]; then
      echo "[dry] agent: $agent_name → $target"
    else
      echo "[sync] agent: $agent_name"
      cp "$agent_file" "$target"
    fi
  done
  echo "[sync] agents 완료. ${#agent_files[@]}개."
}

sync_skills
sync_agents

if [[ $DRY_RUN -eq 1 ]]; then
  echo "[sync] dry run 완료. 실제 동기화: bash 70_tools/sync-skills.sh"
fi
