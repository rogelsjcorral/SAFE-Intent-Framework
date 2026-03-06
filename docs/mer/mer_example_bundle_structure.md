SPDX-License-Identifier: CC-BY-SA-4.0

Copyright 2026 Rogel S.J. Corral

This document illustrates an example structure of a Minimal Evidence Record (MER)
bundle produced by a SAFE-compliant execution wrapper.

Full license text: ../../LICENSES/CC-BY-SA-4.0.txt

---

# Example MER Bundle Structure

A SAFE execution wrapper produces an evidence bundle containing logs,
artifacts, and a structured MER file describing the operation.

## Example directory layout

    evidence/
    └── run_2026_04_example/
        ├── mer.json
        ├── enumerate.raw.log
        ├── snapshot.raw.log
        ├── execute.raw.log
        ├── verify.raw.log
        └── secret_scan.log

## File descriptions

| File | Purpose |
|-----|--------|
| mer.json | Structured Minimal Evidence Record describing the run |
| enumerate.raw.log | Raw output from the enumeration phase |
| snapshot.raw.log | Captured pre-change system state |
| execute.raw.log | Execution log for the change action |
| verify.raw.log | Verification results confirming the final state |
| secret_scan.log | Credential or secret leak detection results |

## Design goals

The MER bundle is intended to provide:

- Deterministic execution traceability
- Minimal but sufficient forensic evidence
- Machine-readable audit artifacts
- Compatibility with external logging or SIEM systems
- Clear phase separation between enumeration, snapshot, execution, and verification

## Notes

The MER concept is designed as a lightweight evidence format for
SAFE-compliant automation workflows. It is not intended to replace
full enterprise audit pipelines, but to provide a minimal, structured
record that enables investigation, replay analysis, and operational
accountability.
