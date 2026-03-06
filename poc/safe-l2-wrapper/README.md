# SAFE-L2 Reference Wrapper (Proof of Concept)

SPDX-License-Identifier: Apache-2.0

Copyright 2026 Rogel S.J. Corral

This directory contains a minimal reference wrapper demonstrating
SAFE-L2 enforcement semantics for administrative automation.

The wrapper is intentionally small and designed only to show that
the SAFE Intent Framework can be implemented in a practical execution
pipeline.

This implementation is not production security software.

---

## Purpose

The SAFE-L2 wrapper demonstrates how a runtime control layer can enforce
basic safety properties when executing administrative actions.

The wrapper enforces:

- phase ordering
- scope binding
- confirmation gating
- evidence artifact generation (MER)

The design goal is to show that intent verification and execution
discipline can be enforced outside the model itself.

---

## SAFE-L2 Execution Phases

A SAFE-L2 execution run follows a strict sequence:

1. Enumeration  
   Resolve ambiguous targets into a concrete list.

2. Snapshot  
   Capture the pre-change state.

3. Execution  
   Apply the intended change.

4. Verification  
   Confirm the resulting system state.

5. Evidence generation  
   Produce a Minimal Evidence Record (MER) bundle.

---

## Example Usage

    python safe_l2_reference_wrapper.py \
      --env prod \
      --change-class iam \
      --risk-tier high \
      --intent "Disable legacy auth for tenants in OU=Sales" \
      --ticket "CHG-12345" \
      --enumerate 'python enumerate_targets.py' \
      --snapshot  'python snapshot_state.py --targets-file {targets_ref}' \
      --execute   'python apply_change.py --targets-file {targets_ref}' \
      --verify    'python verify_state.py --targets-file {targets_ref}' \
      --secret-scan-cmd 'python secret_scan.py --dir {evidence_dir}'

The wrapper runs each stage sequentially and produces a structured
evidence bundle describing the execution.

---

## Minimal Evidence Record (MER)

Each run produces a minimal evidence bundle that can be used for
auditing or post-incident investigation.

Typical bundle structure:

    evidence/
    └── run_<id>/
        ├── mer.json
        ├── enumerate.raw.log
        ├── snapshot.raw.log
        ├── execute.raw.log
        ├── verify.raw.log
        └── secret_scan.log

MER schema examples are available in:

    docs/mer/

---

## Scope of This Reference Implementation

This wrapper demonstrates control semantics only.

It does not attempt to provide:

- hardened security controls
- immutable evidence storage
- enterprise audit integrations
- high-availability execution pipelines

Production implementations will require additional safeguards.

---

## Relationship to the SAFE RFC

This wrapper demonstrates concepts described in the SAFE Intent
Framework RFC.

The RFC defines:

- control principles
- failure modes
- readiness scorecards
- operational guidance

The wrapper exists purely to show that the control model can be
implemented in a practical workflow.

---

## License

This reference implementation is licensed under the Apache License 2.0.

See the LICENSE file in this directory for the full license text.

---

## Disclaimer

This implementation is provided for educational and research purposes.

It is intended to demonstrate SAFE-L2 control semantics and should not
be deployed as production security software without significant
hardening and review.
