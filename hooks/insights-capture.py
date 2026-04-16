#!/usr/bin/env python3
"""insights-capture.py — Stop hook for Insight card capture (Protocols 3.2).

Reads the session transcript (JSONL) via transcript_path in hook input,
extracts `★ Insight ─...` blocks from assistant messages, appends new
ones to .claude/insights-buffer.md with timestamp + session id + cwd.

Design invariants:
- Cwd-guarded to repo root (matches stop-gate.sh pattern)
- NEVER blocks — always outputs {"decision": "approve"} so session close
  is never gated by insight capture
- Dedupes by a first-80-chars fingerprint so re-firing the Stop hook
  (or running it twice on the same transcript) is idempotent
- Silent on all error paths — missing transcript, malformed JSON,
  empty body, whatever — emit approve and move on

P8 audit path: _config/agent-protocols.md Protocol 8 step 7 reads
.claude/insights-buffer.md to detect recurring insights across sessions.
"""

import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def _get_repo_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True
    )
    return Path(result.stdout.strip()) if result.returncode == 0 else Path.cwd()


REPO_ROOT = _get_repo_root()
BUFFER_PATH = REPO_ROOT / ".claude" / "insights-buffer.md"

INSIGHT_PATTERN = re.compile(
    r"★\s*Insight[^\n]*\n"
    r"(.*?)"
    r"\n[`\s]*[─\-]{5,}",
    re.DOTALL,
)


def approve(reason: str) -> None:
    print(json.dumps({"decision": "approve", "reason": reason}))
    sys.exit(0)


def extract_assistant_texts(transcript_path: Path) -> list[str]:
    texts: list[str] = []
    try:
        with open(transcript_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    msg = json.loads(line)
                except json.JSONDecodeError:
                    continue

                if msg.get("type") != "assistant":
                    continue
                message = msg.get("message") or {}
                content = message.get("content")
                if not content:
                    continue

                if isinstance(content, str):
                    texts.append(content)
                    continue

                if isinstance(content, list):
                    for block in content:
                        if isinstance(block, dict) and block.get("type") == "text":
                            t = block.get("text", "")
                            if t:
                                texts.append(t)
                        elif isinstance(block, str):
                            texts.append(block)
    except FileNotFoundError:
        return []
    except OSError:
        return []
    return texts


def extract_insight_bodies(texts: list[str]) -> list[str]:
    bodies: list[str] = []
    for text in texts:
        for match in INSIGHT_PATTERN.finditer(text):
            body = match.group(1).strip()
            body = body.strip("`").strip()
            if body:
                bodies.append(body)
    return bodies


def fingerprint(body: str) -> str:
    normalized = re.sub(r"^\s*([-*•]|\d+[.)])\s+", "", body)
    normalized = re.sub(r"^(\*+|_+)", "", normalized)
    normalized = " ".join(normalized.split())
    return normalized[:80]


def main() -> None:
    try:
        raw = sys.stdin.read()
        hook_input = json.loads(raw) if raw else {}
    except (json.JSONDecodeError, OSError):
        approve("insights-capture: no readable input")

    cwd = hook_input.get("cwd", "")
    transcript_path_str = hook_input.get("transcript_path", "")
    session_id = hook_input.get("session_id", "unknown")

    if not cwd.startswith(str(REPO_ROOT)):
        approve("insights-capture: outside repo")

    if not transcript_path_str:
        approve("insights-capture: no transcript_path in hook input")
    transcript_path = Path(transcript_path_str)
    if not transcript_path.exists():
        approve(f"insights-capture: transcript not found at {transcript_path_str}")

    texts = extract_assistant_texts(transcript_path)
    if not texts:
        approve("insights-capture: no assistant texts in transcript")

    bodies = extract_insight_bodies(texts)
    if not bodies:
        approve("insights-capture: no insight cards this session")

    existing_content = BUFFER_PATH.read_text(encoding="utf-8") if BUFFER_PATH.exists() else ""
    existing_fingerprints: set[str] = set()
    current_block: list[str] = []
    for line in existing_content.splitlines():
        if line.startswith("## ") or line.startswith("---"):
            if current_block:
                block_text = "\n".join(current_block).strip()
                if block_text:
                    existing_fingerprints.add(fingerprint(block_text))
                current_block = []
            continue
        current_block.append(line)
    if current_block:
        block_text = "\n".join(current_block).strip()
        if block_text:
            existing_fingerprints.add(fingerprint(block_text))

    new_bodies = [b for b in bodies if fingerprint(b) not in existing_fingerprints]

    if not new_bodies:
        approve(f"insights-capture: {len(bodies)} card(s) already buffered (no new)")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    short_session = session_id[:8] if session_id != "unknown" else "unknown"
    cwd_rel = cwd.replace(str(REPO_ROOT) + "/", "").rstrip("/") or "(root)"

    BUFFER_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(BUFFER_PATH, "a", encoding="utf-8") as f:
        for body in new_bodies:
            f.write(f"\n---\n\n## {timestamp} | session {short_session} | cwd {cwd_rel}\n\n")
            f.write(body + "\n")

    approve(f"insights-capture: {len(new_bodies)} new card(s) buffered")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        approve(f"insights-capture: unexpected error ({type(e).__name__})")
