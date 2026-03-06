# Copyright 2026 Rogel S.J. Corral
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# This reference wrapper is a proof of concept for SAFE-L2 semantics.
# It is intended to demonstrate enforceable phase ordering, scope binding,
# confirmation gating, and MER generation. It is not an industrial-grade
# implementation and is not presented as production-ready security software.

#!/usr/bin/env python3
"""
SAFE-L2 minimal enforcement wrapper (PoC): enforces phase ordering and produces MER artifacts.

Scope note:
This reference wrapper is a proof of concept for SAFE-L2 semantics. It is intended
to demonstrate enforceable phase ordering, scope binding, confirmation gating,
and MER generation. It is not an industrial-grade implementation and is not
presented as production-ready security software.

Usage example:
  python safe_l2_reference_wrapper.py \
    --env prod \
    --change-class iam \
    --risk-tier high \
    --intent "Disable legacy auth for tenants in OU=Sales" \
    --ticket "CHG-12345" \
    \
    --enumerate 'python enumerate_targets.py' \
    --snapshot  'python snapshot_state.py --targets-file {targets_ref}' \
    --execute   'python apply_change.py --targets-file {targets_ref}' \
    --verify    'python verify_state.py --targets-file {targets_ref}' \
    \
    --secret-scan-cmd 'python secret_scan.py --dir {evidence_dir}'

Notes:
- Commands are executed without a shell (shlex.split).
- The wrapper supports templating variables in command strings:
    {targets_ref}, {evidence_dir}, {run_id}, {env}, {risk_tier}, {change_class}
- For strictest “bind to scope” behavior, make your execute/snapshot/verify scripts require --targets-file.

Non-goals:
- This wrapper does not prove correctness of downstream scripts.
- This wrapper does not provide immutable evidence storage.
- This wrapper is intended only to demonstrate SAFE-L2 control semantics.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import platform
import re
import shlex
import subprocess
import sys
import uuid
from pathlib import Path
from typing import Any, Dict, List, Tuple

DEFAULT_EVIDENCE_DIR = ".safe_evidence"
MAX_INLINE_TARGETS = 200  # beyond this, store digest + stable sample only
STABLE_SAMPLE_N = 10

SECRET_PATTERNS = [
    # crude-but-useful patterns; you can harden later
    r"AKIA[0-9A-Z]{16}",  # AWS access key id
    r"(?i)secret\s*=\s*['\"][^'\"]+['\"]",
    r"(?i)api[_-]?key\s*[:=]\s*['\"][^'\"]+['\"]",
    r"(?i)token\s*[:=]\s*['\"][^'\"]+['\"]",
    r"(?i)authorization:\s*bearer\s+[a-z0-9\-\._]+",
]

# Minimal PHI-ish patterns are intentionally NOT included here.
# For healthcare contexts, you should prefer a deliberate "PHI-safe logging mode"
# in your downstream scripts (do not log identifiers in the first place),
# plus encryption-at-rest for evidence bundles.


def utc_now() -> str:
    return dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def digest_list(items: List[str]) -> str:
    joined = "\n".join(items).encode("utf-8")
    return sha256_bytes(joined)


def stable_sample(items: List[str], n: int = STABLE_SAMPLE_N) -> List[str]:
    # stable deterministic ordering: sort then take first n
    return sorted(items)[:n]


def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def redact_secrets(text: str) -> str:
    redacted = text
    for pat in SECRET_PATTERNS:
        redacted = re.sub(pat, "[REDACTED]", redacted)
    return redacted


def write_redacted_copy(src: Path, dst: Path) -> Dict[str, Any]:
    raw = src.read_text(encoding="utf-8", errors="replace")
    red = redact_secrets(raw)
    dst.write_text(red, encoding="utf-8")
    return {
        "redaction_performed": True,
        "redaction_rules_count": len(SECRET_PATTERNS),
        "redacted_file": str(dst),
        "changed": (raw != red),
    }


def parse_targets_from_output(text: str) -> List[str]:
    """
    Minimal target parser.
    Expect enumeration command to print one target id per line.
    Empty lines and comment lines (#...) ignored.
    """
    targets: List[str] = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        targets.append(line)
    return targets


def format_cmd(template: str, ctx: Dict[str, str]) -> str:
    """
    Replace {var} placeholders in the command string.
    """
    try:
        return template.format(**ctx)
    except KeyError as e:
        raise SystemExit(f"Command template missing placeholder value: {e}")


def run_cmd(cmd: str, out_path: Path) -> Tuple[int, str]:
    """
    Run a command string without a shell (shlex.split).
    Captures stdout+stderr into out_path.
    """
    args = shlex.split(cmd)
    proc = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    output = proc.stdout or ""
    out_path.write_text(output, encoding="utf-8")
    return proc.returncode, output


def evidence_hashes_for_dir(evidence_dir: Path) -> Dict[str, str]:
    """
    Compute sha256 checksums for all files in the evidence directory tree.
    Paths are stored relative to evidence_dir for portability.
    """
    hashes: Dict[str, str] = {}
    for p in sorted(evidence_dir.rglob("*")):
        if p.is_file():
            rel = str(p.relative_to(evidence_dir))
            hashes[rel] = sha256_file(p)
    return hashes


def build_change_fingerprint(env: str, change_class: str, risk_tier: str, intent: str, action: str, targets_digest: str) -> str:
    """
    Idempotency-ish fingerprint.
    If you run the same change twice, we detect it and require extra confirmation.
    """
    payload = "\n".join([env, change_class, risk_tier, action, intent.strip(), targets_digest]).encode("utf-8")
    return sha256_bytes(payload)


def require_confirmation(summary: str, *, mode: str = "normal") -> None:
    """
    Confirmation gate.
    mode="normal" -> require "I CONFIRM"
    mode="high"   -> require "I CONFIRM <8-hex>" where <8-hex> is a provided token included in summary.
    """
    print("\n=== SAFE CONFIRMATION REQUIRED ===")
    print(summary)

    if mode == "high":
        print("\nType EXACTLY: I CONFIRM <TOKEN>\n")
    else:
        print("\nType EXACTLY: I CONFIRM\n")

    typed = input("> ").strip()
    if mode == "high":
        # We expect the token to be included in the summary in a line "Confirm token: XXXXXXXX"
        token = ""
        for ln in summary.splitlines():
            if ln.lower().startswith("confirm token:"):
                token = ln.split(":", 1)[1].strip()
                break
        expected = f"I CONFIRM {token}"
        if typed != expected:
            raise SystemExit("Confirmation not provided (high-risk token mismatch). Aborting before execution.")
    else:
        if typed != "I CONFIRM":
            raise SystemExit("Confirmation not provided. Aborting before execution.")


def build_mer(
    *,
    run_id: str,
    evidence_dir: Path,
    args: argparse.Namespace,
    enumeration: Dict[str, Any],
    snapshot: Dict[str, Any],
    confirmation: Dict[str, Any],
    execution: Dict[str, Any],
    verification: Dict[str, Any],
    rollback: Dict[str, Any],
    security: Dict[str, Any],
    evidence_hashes: Dict[str, str],
    fingerprint: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "mer_version": "0.6",
        "safe_compliance_level": "L2",
        "run_id": run_id,
        "timestamp_utc": utc_now(),
        "environment": {
            "name": args.env,
            "change_class": args.change_class,
            "risk_tier": args.risk_tier,
        },
        "intent": {
            "operator_intent_text": args.intent,
            "requested_action": args.action,
            "justification": args.justification or "",
            "approval_ticket_ref": args.ticket or "",
        },
        "operator": {
            "actor_id": args.actor or "",
            "approval_mechanism": "interactive_confirm",
            "approver_ids": [],
        },
        "toolchain": {
            "wrapper_name": "safe-l2-minimal-hardened",
            "wrapper_version": "0.2",
            "execution_tools": ["no-shell subprocess"],
            "python_version": sys.version.split()[0],
            "platform": platform.platform(),
        },
        "phases": {
            "generation": {
                "write_credentials_present": False,
                "retrieval_used": bool(args.retrieval_used),
                "retrieval_provenance": args.retrieval_provenance or "",
            },
            "enumeration": enumeration,
            "snapshot": snapshot,
            "confirmation": confirmation,
            "execution": execution,
            "verification": verification,
            "rollback": rollback,
        },
        "security": security,
        "evidence_storage": {
            "storage_type": "filesystem",
            "immutability": "none",
            "evidence_bundle_ref": str(evidence_dir),
        },
        "evidence_hashes_sha256": evidence_hashes,
        "replay_guard": fingerprint,
        "exceptions": [],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--env", required=True)
    ap.add_argument(
        "--change-class",
        required=True,
        choices=["iam", "tenant_policy", "endpoint_mass", "network_access", "other"],
    )
    ap.add_argument("--risk-tier", required=True, choices=["low", "medium", "high"])
    ap.add_argument("--intent", required=True)
    ap.add_argument("--action", default="update", help="create|update|delete|assign|revoke|enable|disable|other")
    ap.add_argument("--justification", default="")
    ap.add_argument("--ticket", default="")
    ap.add_argument("--actor", default="")

    ap.add_argument("--enumerate", required=True, help="command that prints one target id per line")
    ap.add_argument("--snapshot", required=True, help="command that captures before-state")
    ap.add_argument("--execute", required=True, help="command that performs the write")
    ap.add_argument("--verify", required=True, help="command that verifies after-state")

    ap.add_argument("--verify-on-failure", action="store_true", help="run verify even if execute fails")
    ap.add_argument("--evidence-dir", default=DEFAULT_EVIDENCE_DIR)

    ap.add_argument("--retrieval-used", action="store_true")
    ap.add_argument("--retrieval-provenance", default="")

    ap.add_argument("--rollback-plan-ref", default="")
    ap.add_argument("--restore-validation-query", default="")

    ap.add_argument(
        "--secret-scan-cmd",
        default="",
        help="optional command to scan evidence dir for secrets; supports {evidence_dir} templating",
    )

    args = ap.parse_args()

    # Risk-tier enforcement rules (minimal but real)
    if args.risk_tier == "high" and not args.ticket:
        raise SystemExit("High risk changes require --ticket (approval reference). Aborting.")

    run_id = str(uuid.uuid4())
    base = Path(args.evidence_dir) / run_id
    ensure_dir(base)

    ctx: Dict[str, str] = {
        "run_id": run_id,
        "evidence_dir": str(base),
        "env": args.env,
        "risk_tier": args.risk_tier,
        "change_class": args.change_class,
        "targets_ref": "",  # populated after enumeration
    }

    # 1) ENUMERATION
    enum_out = base / "enumeration.raw.log"
    enum_cmd = format_cmd(args.enumerate, ctx)
    enum_rc, enum_txt = run_cmd(enum_cmd, enum_out)

    enum_red = base / "enumeration.log"
    red_enum_info = write_redacted_copy(enum_out, enum_red)

    if enum_rc != 0:
        # Even on early failure, write a minimal MER stub for auditability
        (base / "mer.json").write_text(
            json.dumps(
                {
                    "mer_version": "0.6",
                    "safe_compliance_level": "L2",
                    "run_id": run_id,
                    "timestamp_utc": utc_now(),
                    "failed_phase": "enumeration",
                    "return_code": enum_rc,
                    "enumeration_output_ref": str(enum_red),
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        raise SystemExit(f"Enumeration failed (rc={enum_rc}). See {enum_red}")

    targets = parse_targets_from_output(enum_txt)
    t_count = len(targets)

    if t_count == 0:
        raise SystemExit("Enumeration returned 0 targets. Aborting (SAFE default).")

    target_repr: Dict[str, Any] = {"method": "", "stable_sample_ids": [], "hashed_list_digest": ""}

    if t_count <= MAX_INLINE_TARGETS:
        targets_file = base / "targets.txt"
        targets_file.write_text("\n".join(targets) + "\n", encoding="utf-8")
        target_repr["method"] = "full_list"
        target_repr["stable_sample_ids"] = stable_sample(targets)
        target_repr["hashed_list_digest"] = digest_list(targets)
        targets_ref = str(targets_file)
    else:
        # Avoid dumping huge lists; store digest + stable sample
        target_repr["method"] = "stable_sample"
        target_repr["stable_sample_ids"] = stable_sample(targets)
        target_repr["hashed_list_digest"] = digest_list(targets)
        sample_file = base / "targets.sample.txt"
        sample_file.write_text("\n".join(target_repr["stable_sample_ids"]) + "\n", encoding="utf-8")
        targets_ref = str(sample_file)

    ctx["targets_ref"] = targets_ref  # Bind subsequent phases to the enumerated scope

    enumeration = {
        "enumeration_time_utc": utc_now(),
        "scope_logic_executed": enum_cmd,
        "target_count": t_count,
        "target_representation": target_repr,
        "enumeration_output_ref": str(enum_red),
        "targets_ref": targets_ref,
    }

    # Replay guard fingerprint
    change_fp = build_change_fingerprint(
        args.env, args.change_class, args.risk_tier, args.intent, args.action, target_repr["hashed_list_digest"]
    )
    fp_file = Path(args.evidence_dir) / "change_fingerprints.jsonl"
    fp_seen = False
    try:
        if fp_file.exists():
            for line in fp_file.read_text(encoding="utf-8", errors="replace").splitlines():
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                if obj.get("fingerprint") == change_fp and obj.get("env") == args.env and obj.get("change_class") == args.change_class:
                    fp_seen = True
                    break
    except Exception:
        # If fingerprint registry read fails, do not block execution, but record later.
        fp_seen = False

    fingerprint_info = {
        "fingerprint_sha256": change_fp,
        "registry_ref": str(fp_file),
        "seen_before": fp_seen,
    }

    # 2) SNAPSHOT (bind to targets_ref if downstream supports it)
    snap_out = base / "snapshot.raw.log"
    snap_cmd = format_cmd(args.snapshot, ctx)
    snap_rc, _snap_txt = run_cmd(snap_cmd, snap_out)

    snap_red = base / "snapshot.log"
    red_snap_info = write_redacted_copy(snap_out, snap_red)

    if snap_rc != 0:
        raise SystemExit(f"Snapshot failed (rc={snap_rc}). See {snap_red}")

    snapshot = {
        "snapshot_time_utc": utc_now(),
        "snapshot_ids": [],
        "snapshot_definition": snap_cmd,
        "snapshot_output_ref": str(snap_red),
    }

    # 3) CONFIRMATION (stronger for high risk, and extra warning on replay)
    confirm_token = sha256_bytes(change_fp.encode("utf-8"))[:8].upper()
    confirmation_summary = (
        f"Environment: {args.env}\n"
        f"Change class: {args.change_class} | Risk: {args.risk_tier}\n"
        f"Intent: {args.intent}\n"
        f"Action: {args.action}\n"
        f"Enumeration cmd: {enum_cmd}\n"
        f"Snapshot cmd: {snap_cmd}\n"
        f"Target count: {t_count}\n"
        f"Targets ref: {targets_ref}\n"
        f"Targets digest: {target_repr.get('hashed_list_digest','')}\n"
        f"Change fingerprint: {change_fp}\n"
        f"Replay seen before: {fp_seen}\n"
    )

    # If replay detected, require extra confirmation even for non-high risk
    if args.risk_tier == "high" or fp_seen:
        confirmation_summary += f"Confirm token: {confirm_token}\n"
        require_confirmation(confirmation_summary, mode="high")
        confirmation_mode = "high_token"
    else:
        require_confirmation(confirmation_summary, mode="normal")
        confirmation_mode = "standard"

    confirmation = {
        "confirmed": True,
        "confirmation_mode": confirmation_mode,
        "confirmation_time_utc": utc_now(),
        "confirmation_summary_shown_ref": str(base / "confirmation.summary.txt"),
        "threshold_flags": (["replay_guard_triggered"] if fp_seen else []),
        "confirm_token": (confirm_token if (args.risk_tier == "high" or fp_seen) else ""),
    }
    (base / "confirmation.summary.txt").write_text(confirmation_summary, encoding="utf-8")

    # Update fingerprint registry (append-only best effort)
    try:
        ensure_dir(fp_file.parent)
        with fp_file.open("a", encoding="utf-8") as f:
            f.write(
                json.dumps(
                    {
                        "timestamp_utc": utc_now(),
                        "fingerprint": change_fp,
                        "env": args.env,
                        "change_class": args.change_class,
                        "risk_tier": args.risk_tier,
                        "run_id": run_id,
                        "targets_digest": target_repr.get("hashed_list_digest", ""),
                        "target_count": t_count,
                        "ticket": args.ticket or "",
                    }
                )
                + "\n"
            )
    except Exception:
        # Non-fatal; recorded later in MER via evidence_hashes anyway
        pass

    # 4) EXECUTION (must be templated to include {targets_ref} for true scope binding)
    exec_out = base / "execution.raw.log"
    exec_cmd = format_cmd(args.execute, ctx)
    exec_rc, exec_txt = run_cmd(exec_cmd, exec_out)

    exec_red = base / "execution.log"
    red_exec_info = write_redacted_copy(exec_out, exec_red)

    # Minimal status accounting: optional convention OK/FAIL
    ok_count = len([ln for ln in exec_txt.splitlines() if ln.strip().upper().startswith("OK")])
    fail_lines = len([ln for ln in exec_txt.splitlines() if ln.strip().upper().startswith("FAIL")])

    # Explicit semantics: return_code dominates
    failure_count = 0
    if exec_rc != 0:
        failure_count = max(1, fail_lines)
    else:
        failure_count = fail_lines

    execution = {
        "execution_time_utc": utc_now(),
        "write_action_performed": True,
        "success_semantics": "return_code",
        "status_semantics": "ok_fail_prefix_optional",
        "success_count_observed": ok_count,
        "failure_count_observed": failure_count,
        "per_target_status_ref": str(exec_red),
        "exit_policy": "fail_on_any_failure",
        "retries_policy": "bounded",
        "return_code": exec_rc,
        "execution_command": exec_cmd,
    }

    # 5) VERIFICATION
    verification: Dict[str, Any] = {
        "verification_time_utc": "",
        "verification_query": "",
        "verification_output_ref": "",
        "diff_summary": "",
        "return_code": None,
        "verification_mode": "",
        "skipped": False,
        "skip_reason": "",
    }

    do_verify = True
    if exec_rc != 0 and not args.verify_on_failure:
        do_verify = False
        verification.update(
            {
                "skipped": True,
                "skip_reason": "execution_failed_and_verify_on_failure_false",
                "verification_mode": "skipped_due_to_exec_failure",
            }
        )

    if do_verify:
        ver_out = base / "verification.raw.log"
        ver_cmd = format_cmd(args.verify, ctx)
        ver_rc, _ver_txt = run_cmd(ver_cmd, ver_out)

        ver_red = base / "verification.log"
        red_ver_info = write_redacted_copy(ver_out, ver_red)

        verification.update(
            {
                "verification_time_utc": utc_now(),
                "verification_query": ver_cmd,
                "verification_output_ref": str(ver_red),
                "return_code": ver_rc,
                "verification_mode": ("post_failure" if exec_rc != 0 else "post_success"),
            }
        )
    else:
        red_ver_info = {"redaction_performed": False, "redaction_rules_count": 0, "redacted_file": "", "changed": False}

    # 6) OPTIONAL SECRET SCAN (evidence-dir scoped)
    secret_scan: Dict[str, Any] = {
        "secret_scan_performed": False,
        "secret_scan_tool": "",
        "secret_scan_result": "not_run",
        "secret_scan_output_ref": "",
        "return_code": None,
    }

    if args.secret_scan_cmd.strip():
        scan_out = base / "secret_scan.raw.log"
        scan_cmd = format_cmd(args.secret_scan_cmd, ctx)
        scan_rc, _scan_txt = run_cmd(scan_cmd, scan_out)

        scan_red = base / "secret_scan.log"
        _ = write_redacted_copy(scan_out, scan_red)

        secret_scan.update(
            {
                "secret_scan_performed": True,
                "secret_scan_tool": scan_cmd.split()[0],
                "secret_scan_result": ("clean" if scan_rc == 0 else "findings_or_error"),
                "secret_scan_output_ref": str(scan_red),
                "return_code": scan_rc,
            }
        )

    # Rollback block (still metadata in this minimal wrapper)
    rollback = {
        "rollback_plan_ref": args.rollback_plan_ref or "",
        "rollback_without_llm": True,
        "restore_validation_query": args.restore_validation_query or "",
    }

    # Security notes
    security = {
        **secret_scan,
        "redaction_performed": True,
        "redaction_notes": json.dumps(
            {
                "enumeration": red_enum_info,
                "snapshot": red_snap_info,
                "execution": red_exec_info,
                "verification": red_ver_info,
            }
        ),
        "warnings": [],
    }

    if args.risk_tier == "high" and args.retrieval_used and not args.retrieval_provenance:
        security["warnings"].append("retrieval_used_true_but_no_retrieval_provenance_provided")

    # Evidence hashes (tamper-evidence)
    hashes = evidence_hashes_for_dir(base)

    # Build MER
    mer = build_mer(
        run_id=run_id,
        evidence_dir=base,
        args=args,
        enumeration=enumeration,
        snapshot=snapshot,
        confirmation=confirmation,
        execution=execution,
        verification=verification,
        rollback=rollback,
        security=security,
        evidence_hashes=hashes,
        fingerprint=fingerprint_info,
    )

    (base / "mer.json").write_text(json.dumps(mer, indent=2), encoding="utf-8")

    print(f"\nSAFE-L2 complete. Evidence bundle: {base}")
    print(f"MER: {base / 'mer.json'}")
    print(f"Targets ref: {targets_ref}")

    # overall exit policy
    # - If execute failed -> exit 2
    # - Else if verify ran and failed -> exit 2
    # - Else success -> 0
    if exec_rc != 0:
        return 2
    if not verification.get("skipped", False) and (verification.get("return_code") not in (None, 0)):
        return 2

    # If secret scan ran and found issues, you may want to treat it as non-zero exit in higher tiers.
    # For PoC, we keep it informational.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
