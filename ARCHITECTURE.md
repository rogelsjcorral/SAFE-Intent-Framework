# SAFE Intent Framework – Architecture Overview

This repository contains the specification and a minimal reference
implementation demonstrating SAFE-L2 control semantics.

SAFE is designed to enforce structured execution phases around
administrative automation tasks such as IAM updates, tenant policy
changes, or bulk endpoint operations.

The repository is organized into four major components.

## 1. Specification

Location:
docs/

This directory contains the SAFE RFC document and supporting
documentation.

The RFC defines the SAFE execution model, including:

• Intent declaration
• Target enumeration
• Pre-change snapshot
• Human confirmation gate
• Controlled execution
• Post-change verification
• Machine Execution Record (MER)

The documentation is licensed under CC BY-SA 4.0 to encourage
adaptation and discussion in the research and engineering community.

## 2. Reference Implementation (PoC)

Location:
poc/safe-l2-wrapper/

This directory contains a minimal SAFE-L2 enforcement wrapper.

The wrapper demonstrates:

• Enforced phase ordering
• Scope binding between enumeration and execution
• Confirmation gating
• Evidence bundle generation
• MER artifact creation

The wrapper is intentionally minimal and is provided only as a proof
of concept.

It is not intended to be production-grade software.

## 3. Sample Scripts

Location:
poc/sample-scripts/

These small utilities simulate administrative operations that the
wrapper orchestrates.

Examples include:

• enumerate_targets.py
• snapshot_state.py
• apply_change.py
• verify_state.py
• secret_scan.py

These scripts demonstrate how SAFE binds execution to enumerated
targets and produces verifiable artifacts.

## 4. Execution Examples

Location:
examples/

This directory contains demonstration commands and sample outputs
illustrating how a SAFE run behaves.

These examples allow reviewers to quickly understand SAFE without
running the code.

Example artifacts include:

• command execution scripts
• simulated console output
• example MER artifacts

## 5. Evidence Bundles

During execution, SAFE generates an evidence bundle containing logs
and a Machine Execution Record (MER).

Example structure:

.safe_evidence/<run_id>/

  enumeration.log
  snapshot.log
  execution.log
  verification.log
  mer.json

The MER provides an auditable record of the change operation and
links to the evidence files produced during each phase.

## Design Goal

SAFE does not attempt to replace existing administrative tools.

Instead, it provides a structured execution layer that enforces
intent declaration, scope binding, and verification before and after
changes are applied.

The goal is to reduce ambiguity and operational risk in automated
administrative workflows.
