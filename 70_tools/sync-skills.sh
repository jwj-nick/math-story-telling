#!/usr/bin/env bash
# sync-skills.sh — 10_system/30_skills/ + 10_system/35_agents/ → .claude/ 미러 동기화
#
# SSOT: 10_system/30_skills/<skill>/, 10_system/35_agents/<agent>.md
# Mirror: .claude/skills/<skill>/, .claude/agents/<agent>.md
#
# 방향: 10_system → .claude (단방향 미러)
# 역방향 금지: .claude/에서 직접 수정한 내용은 이 스크립트 실행 시 덮어쓰임.
#
# 사용 (어디서 실행해도 동일):
#   bash 70_tools/sync-skills.sh           # 실행
#   bash 70_tools/sync-skills.sh --dry     # dry run only
#
# 동작 (★ mirror 모드):
#   - 새 파일 추가 / 기존 파일 갱신 / SSOT에서 사라진 항목은 mirror에서도 삭제 (prune)
#   - skill: SSOT에 없는 .claude/skills/<dir> 제거
#   - agent: SSOT에 없는 .claude/agents/<file>.md 제거
#
# 안전:
#   - SOURCE 디렉터리가 아예 없거나 비어있으면 prune 중단 (실수로 mirror 전체 삭제 방지)
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
    echo "[sync] 10_system/30_skills/ 에 skill이 없습니다. (0개) — prune 중단(안전)"
    return 0
  fi

  mkdir -p "$SKILLS_DST"

  # SSOT skill 이름 집합
  local -A src_names=()
  for skill_dir in "${skill_dirs[@]}"; do
    src_names["$(basename "$skill_dir")"]=1
  done

  # copy/update
  for skill_dir in "${skill_dirs[@]}"; do
    local skill_name target
    skill_name="$(basename "$skill_dir")"
    target="$SKILLS_DST/$skill_name"
    if [[ $DRY_RUN -eq 1 ]]; then
      echo "[dry] skill: $skill_name → $target"
    else
      echo "[sync] skill: $skill_name"
      rm -rf "$target"            # 깨끗이 덮어쓰기 (mirror 내부 stale 파일 제거)
      cp -r "$skill_dir." "$target/"
    fi
  done

  # prune: mirror에만 있고 SSOT에 없는 skill 제거
  local dst_dirs=("$SKILLS_DST"/*/)
  for dst_dir in "${dst_dirs[@]}"; do
    local name
    name="$(basename "$dst_dir")"
    if [[ -z "${src_names[$name]:-}" ]]; then
      if [[ $DRY_RUN -eq 1 ]]; then
        echo "[dry] PRUNE skill (SSOT 없음): $name"
      else
        echo "[prune] skill 제거: $name"
        rm -rf "$dst_dir"
      fi
    fi
  done
  echo "[sync] skills 완료. SSOT ${#skill_dirs[@]}개."
}

sync_agents() {
  if [[ ! -d "$AGENTS_SRC" ]]; then
    echo "[sync] AGENTS_SRC 없음: $AGENTS_SRC — skip"
    return 0
  fi

  shopt -s nullglob
  local agent_files=("$AGENTS_SRC"/*.md)
  if [[ ${#agent_files[@]} -eq 0 ]]; then
    echo "[sync] 10_system/35_agents/ 에 agent .md가 없습니다. (0개) — prune 중단(안전)"
    return 0
  fi

  mkdir -p "$AGENTS_DST"

  local -A src_names=()
  for agent_file in "${agent_files[@]}"; do
    src_names["$(basename "$agent_file")"]=1
  done

  for agent_file in "${agent_files[@]}"; do
    local agent_name target
    agent_name="$(basename "$agent_file")"
    target="$AGENTS_DST/$agent_name"
    if [[ $DRY_RUN -eq 1 ]]; then
      echo "[dry] agent: $agent_name → $target"
    else
      echo "[sync] agent: $agent_name"
      cp "$agent_file" "$target"
    fi
  done

  # prune: mirror에만 있는 agent .md 제거
  local dst_files=("$AGENTS_DST"/*.md)
  for dst_file in "${dst_files[@]}"; do
    local name
    name="$(basename "$dst_file")"
    if [[ -z "${src_names[$name]:-}" ]]; then
      if [[ $DRY_RUN -eq 1 ]]; then
        echo "[dry] PRUNE agent (SSOT 없음): $name"
      else
        echo "[prune] agent 제거: $name"
        rm -f "$dst_file"
      fi
    fi
  done
  echo "[sync] agents 완료. SSOT ${#agent_files[@]}개."
}

sync_skills
sync_agents

if [[ $DRY_RUN -eq 1 ]]; then
  echo "[sync] dry run 완료. 실제 동기화: bash 70_tools/sync-skills.sh"
fi
