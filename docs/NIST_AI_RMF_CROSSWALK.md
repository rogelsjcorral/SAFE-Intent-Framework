# SPDX-License-Identifier: CC-BY-SA-4.0
#
# Copyright 2026 Rogel S.J. Corral
#
# This document is licensed under the Creative Commons
# Attribution-ShareAlike 4.0 International License.

# NIST AI RMF 1.0 Crosswalk: S.A.F.E. Intent Framework

**Document Version:** 1.0  
**Target Framework:** NIST AI Risk Management Framework 1.0  
**NIST Publication:** NIST AI 100-1  
**Applicable Layer:** SAFE-L2 Execution and Control Runtime  
**License:** CC BY-SA 4.0  

---

## Executive Summary

This crosswalk maps the S.A.F.E. Intent Framework to selected functions
and subcategories of the NIST AI Risk Management Framework 1.0
(AI RMF 1.0).

S.A.F.E. addresses a narrow operational risk in AI-assisted privileged
automation: an AI-generated or AI-assisted artifact may execute
successfully while applying the wrong intent, target set, or operational
scope.

S.A.F.E. denotes four control families:

- Separation of Context
- Ambiguity Resolution
- Forensic Idempotency
- Evidence-Based Rollback

The framework treats large language models and other AI systems as
proposal sources rather than trusted execution authorities. Privileged
writes are routed through a controlled execution boundary that requires
target enumeration, before-state snapshotting, explicit confirmation,
bounded execution, after-state verification, and generation of a Minimal
Evidence Record (MER).

This document is an alignment crosswalk. It does not assert
certification, formal compliance, or endorsement by NIST or any other
standards body. It identifies how S.A.F.E. controls can support selected
AI RMF outcomes across the GOVERN, MAP, MEASURE, and MANAGE functions.

---

## Scope of Alignment

This crosswalk applies to S.A.F.E. as an execution-control pattern for
AI-assisted privileged automation.

It is most applicable where AI-generated or AI-assisted artifacts are
used to propose, prepare, or modify administrative changes involving:

- identity and access management
- tenant or cloud policy
- endpoint fleets
- network access controls
- infrastructure-as-code workflows
- privileged administrative scripts
- security or compliance automation

This document does not claim that S.A.F.E. validates the correctness of
an AI model, guarantees the semantic adequacy of verification queries, or
provides production-grade immutable evidence storage. Those properties
remain implementation and deployment responsibilities.

---

## Technical Architecture Mapping

    +-----------------------------------------------------------------------+
    |                       NIST AI RMF FUNCTIONS                           |
    +--------------------+-------------------+------------------------------+
    | GOVERN / MAP       | MANAGE            | MEASURE                      |
    | Intent, context,   | Execution gates   | Verification, evidence,      |
    | risk tolerance     | and risk response | monitoring, review support   |
    +---------+----------+---------+---------+---------------+--------------+
              |                    |                         |
              v                    v                         v
    +-------------------+  +----------------+  +-----------------------------+
    | AI-ASSISTED       |  | SAFE-L2 GATE   |  | MINIMAL EVIDENCE RECORD     |
    | PROPOSAL SOURCE   |  | Controlled     |  | Intent, targets, snapshot,  |
    | Suggests action   |  | execution path |  | execution, verification     |
    +-------------------+  +----------------+  +-----------------------------+

---

## S.A.F.E. Control Flow

The SAFE-L2 execution model uses the following control sequence:

1. Enumerate targets
2. Capture before-state snapshot
3. Present resolved scope for explicit confirmation
4. Execute only against the confirmed target set
5. Verify after-state
6. Generate a Minimal Evidence Record

The minimal SAFE-L2 reference wrapper demonstrates this flow through
separate phase commands for enumeration, snapshot, execution, and
verification. The wrapper also records evidence hashes, confirmation
metadata, execution return codes, verification output references, and
rollback metadata.

---

## NIST AI RMF Core Function Crosswalk

### 1. GOVERN

The GOVERN function establishes organizational policies, processes,
roles, and accountability structures for managing AI risk.

| NIST AI RMF Subcategory | AI RMF Outcome | S.A.F.E. Alignment | Suggested Evidence |
|---|---|---|---|
| GOVERN 1.2 | Trustworthy AI characteristics are integrated into organizational policies, processes, procedures, and practices. | S.A.F.E. provides a repeatable operational control pattern for AI-assisted privileged changes. It requires explicit scope, confirmation, verification, and evidence before privileged execution is treated as complete. | S.A.F.E. policy profile; SAFE-L2 workflow definition; MER schema |
| GOVERN 1.3 | Risk management activities are determined according to organizational risk tolerance. | S.A.F.E. supports risk-tiered execution. Higher-risk or higher-blast-radius changes can require approval references, stronger confirmation, second approval, or stricter execution profiles. | Risk-tier policy; confirmation threshold table; approval-ticket requirement |
| GOVERN 3.2 | Roles and responsibilities for human-AI configurations and oversight are defined and differentiated. | S.A.F.E. separates AI-assisted proposal generation from privileged execution authority. The AI may propose an action, but the operator and execution gate remain responsible for scope confirmation and controlled execution. | Human-AI responsibility matrix; confirmation summary; operator acknowledgement |
| GOVERN 4.3 | Practices are in place to enable AI testing, incident identification, and information sharing. | MER artifacts preserve run evidence that can support review, incident triage, lessons learned, and sharing of observed failure modes. | MER records; failed-run bundles; incident review packet |
| GOVERN 5.1 | Organizational policies and practices are in place to collect, consider, prioritize, and integrate feedback from relevant AI actors. | S.A.F.E. evidence records and failure-mode mappings provide concrete feedback artifacts that can be reviewed by operations, security, governance, and audit stakeholders. | MER archive; failure-mode review notes; change-control feedback |
| GOVERN 6.2 | Contingency processes are in place for failures or incidents involving third-party AI systems. | S.A.F.E. does not directly manage vendor availability, model deprecation, contractual SLA failure, or third-party supply-chain risk. Its narrower contribution is to reduce direct reliance on third-party AI output by requiring AI-assisted proposals to pass through a deterministic execution gate before privileged writes occur. | Third-party AI handling note; LLM-output handling procedure; SAFE-L2 gate policy |

---

### 2. MAP

The MAP function establishes context, intended use, system boundaries,
capabilities, risks, and potential impacts.

| NIST AI RMF Subcategory | AI RMF Outcome | S.A.F.E. Alignment | Suggested Evidence |
|---|---|---|---|
| MAP 1.5 | Organizational risk tolerances are determined and documented. | S.A.F.E. allows organizations to define risk thresholds based on target count, environment, action type, reversibility, and blast radius. | Risk tolerance matrix; SAFE-L2 profile; change-class policy |
| MAP 2.2 | Knowledge limits and human oversight of AI system output are documented. | S.A.F.E. assumes AI output may be incomplete, ambiguous, or wrong in scope. It requires operational intent to be resolved into concrete targets before execution. | AI-output handling procedure; scope-resolution log; target manifest |
| MAP 3.3 | Targeted application scope is specified and documented. | The Enumerate phase resolves vague intent into a bounded target set before any write action is allowed. | Target manifest; targets reference; target digest |
| MAP 3.5 | Processes for human oversight are defined, assessed, and documented. | The Confirm phase requires the operator to review and accept the resolved scope before the Execute phase begins. | Confirmation summary; confirmation token record; operator acknowledgement |
| MAP 4.2 | Internal risk controls for AI system components, including third-party AI technologies, are identified and documented. | S.A.F.E. identifies control points around the AI proposal source, execution gate, target manifest, verification phase, and MER. This supports architectural risk decomposition, but does not by itself complete third-party vendor risk assessment. | Architecture diagram; control inventory; LLM-output handling procedure |
| MAP 5.1 | Likelihood and magnitude of each identified impact are assessed. | S.A.F.E. supports impact assessment by requiring target counts, environment classification, change class, risk tier, and scope representation before execution. | Target count; risk tier; change class; blast-radius notes |
| MAP 5.2 | Practices and personnel for supporting regular engagement with relevant AI actors and integrating feedback about positive, negative, and unanticipated impacts are in place. | S.A.F.E. evidence records can be reviewed with affected operations, security, service-owner, and audit stakeholders after high-risk or failed runs. | Post-change review notes; MER-linked incident or change ticket |

---

### 3. MEASURE

The MEASURE function supports testing, evaluation, verification,
validation, monitoring, and documentation of AI risk.

S.A.F.E. supports the MEASURE function by requiring evidence-producing
phases and post-execution verification. However, S.A.F.E. does not prove
that a particular verification query is semantically adequate. The
adequacy of verification logic remains an implementation responsibility.

| NIST AI RMF Subcategory | AI RMF Outcome | S.A.F.E. Alignment | Suggested Evidence |
|---|---|---|---|
| MEASURE 2.3 | AI system performance or assurance criteria are measured for conditions similar to deployment settings. | S.A.F.E. allows AI-assisted privileged automation to be evaluated against operational assurance criteria such as target accuracy, confirmation quality, verification success, partial-failure handling, and rollback readiness. | Staging MER; test-run MER; assurance criteria checklist |
| MEASURE 2.4 | Functionality and behavior are monitored in production. | S.A.F.E. records execution outcomes and verification results for each controlled run, supporting operational monitoring and review. | Execution log; verification log; MER archive |
| MEASURE 2.6 | AI systems are evaluated regularly for safety risks and ability to fail safely. | S.A.F.E. supports fail-closed behavior when required phases are missing, enumeration returns no targets, confirmation is absent, execution fails, or verification returns failure. | Failed-run MER; policy violation log; non-zero return code |
| MEASURE 2.7 | AI system security and resilience are evaluated and documented. | S.A.F.E. evaluates AI-assisted privileged changes against execution controls, bounded target sets, no-shell command invocation, redacted evidence, and post-change assertions. This supports security review but does not replace independent testing of downstream scripts. | SAFE-L2 validation report; wrapper test results; evidence hash list |
| MEASURE 2.8 | Risks associated with transparency and accountability are examined and documented. | The MER records intent, target representation, confirmation, execution results, verification output, rollback reference, evidence hashes, and toolchain metadata for later review. | Minimal Evidence Record; evidence bundle; hash manifest |
| MEASURE 3.1 | Existing, unanticipated, and emergent AI risks are tracked over time. | Repeated MER records can be analyzed to identify recurring wrong-scope proposals, failed verifications, repeated replay-guard triggers, or confirmation overrides. | MER archive; trend analysis; replay-guard registry |
| MEASURE 4.2 | Measurement results regarding AI system trustworthiness in deployment context and across the AI lifecycle are informed by input from relevant AI actors. | S.A.F.E. creates reviewable artifacts that can be inspected by operators, approvers, auditors, service owners, and security reviewers after execution. | Review comments; change-ticket attachments; audit notes |

---

### 4. MANAGE

The MANAGE function prioritizes, responds to, and treats identified AI
risks, including incident response, recovery, and change management.

| NIST AI RMF Subcategory | AI RMF Outcome | S.A.F.E. Alignment | Suggested Evidence |
|---|---|---|---|
| MANAGE 1.2 | Documented AI risks are prioritized based on impact, likelihood, and available resources or methods. | S.A.F.E. supports prioritization through risk tiers, target count thresholds, environment classification, action type, and reversibility. | Risk-tier configuration; approval rules; target-count threshold |
| MANAGE 1.3 | Responses to high-priority AI risks are developed, planned, and documented. | S.A.F.E. provides a concrete risk treatment for AI-assisted privileged writes: controlled execution gates, target binding, verification, and rollback grounding. | SAFE-L2 workflow; control mapping; MER schema |
| MANAGE 2.1 | Resources required to manage AI risks are considered, including viable non-AI alternatives. | S.A.F.E. allows organizations to decide when AI assistance is appropriate, when manual execution is safer, and when stronger review or approval is required. | AI-use decision record; escalation policy; manual-execution fallback |
| MANAGE 2.4 | Mechanisms are in place to disengage or deactivate AI systems that produce outcomes inconsistent with intended use. | S.A.F.E. can halt execution when intent, target enumeration, confirmation, execution output, or verification does not meet policy. | Fail-closed log; halted execution record; failed-run MER |
| MANAGE 3.1 | AI risks and benefits from third-party resources are regularly monitored and risk controls are applied. | S.A.F.E. does not perform full third-party vendor risk management. It can support monitoring of third-party AI-assisted outputs by requiring such outputs to pass through local execution controls before privileged writes occur. | Third-party AI output handling log; local gate policy; MER records |
| MANAGE 4.1 | Post-deployment monitoring, incident response, recovery, and change management mechanisms are implemented. | S.A.F.E. links pre-change snapshots, execution logs, verification outputs, rollback references, and evidence hashes into a single MER bundle for review and recovery. | MER forensic bundle; rollback reference; change-ticket attachment |
| MANAGE 4.3 | Incidents and errors are communicated, tracked, responded to, recovered from, and documented. | Failed S.A.F.E. runs produce evidence that can be attached to incident tickets, change records, post-incident reviews, or audit packages. | Incident ticket attachment; failed-run MER; post-incident review |

---

## Implementation Notes from SAFE-L2 Reference Wrapper

The SAFE-L2 reference wrapper is a proof of concept. It demonstrates
control semantics rather than production-grade security engineering.

The wrapper demonstrates:

- command execution without shell expansion
- explicit phase ordering
- target enumeration before execution
- binding of later phases to the enumerated target reference
- high-risk confirmation using a confirmation token
- replay detection through a change fingerprint
- redacted evidence copies
- evidence hash generation
- MER generation
- optional secret scanning
- non-zero exit behavior on execution or verification failure

The wrapper does not provide:

- proof of downstream script correctness
- proof that verification queries are semantically complete
- immutable or write-once evidence storage
- full policy-engine integration
- production-grade secret detection
- cryptographic signing of MER records
- complete third-party AI vendor risk management

These non-goals should be preserved in any implementation-specific
alignment claim.

---

## OWASP and NIST CSF Cross-Reference

This section provides a non-exhaustive cross-reference to adjacent
security guidance. These mappings are intended to support discussion and
implementation planning. They do not assert formal compliance.

| Framework | Relevant Control / Risk | S.A.F.E. Alignment |
|---|---|---|
| OWASP Top 10 for LLM Applications 2025 | LLM05: Improper Output Handling | S.A.F.E. does not treat AI output as directly executable. Output must be transformed into bounded operational intent and pass through controlled execution. |
| OWASP Top 10 for LLM Applications 2025 | LLM06: Excessive Agency | S.A.F.E. limits AI agency by separating proposal from execution, requiring human confirmation for privileged writes, and enforcing bounded target sets. |
| NIST CSF 2.0 | PR.PS-04: Log records are generated and made available for continuous monitoring. | MER generation provides structured run evidence that can be forwarded to logging, monitoring, or audit systems. |
| NIST CSF 2.0 | DE.AE-03: Information is correlated from multiple sources. | MER artifacts can correlate intent, target manifests, snapshots, command outcomes, verification results, and replay-guard metadata. |
| NIST CSF 2.0 | RS.AN-03: Analysis is performed to determine what occurred during an incident and identify root cause. | MER artifacts support reconstruction of what was intended, what was confirmed, what executed, and what verification observed. |
| NIST SP 800-53 Rev. 5 | AC-6: Least Privilege | S.A.F.E. supports least-privilege execution by separating proposal generation from write-capable execution and by bounding privileged actions to confirmed targets. |
| NIST SP 800-53 Rev. 5 | AU-12: Audit Record Generation | S.A.F.E. requires generation of structured evidence for controlled privileged execution runs. |

---

## Supplementary Traceability Table

This table connects selected S.A.F.E. failure modes to control families,
evidence artifacts, and NIST AI RMF outcomes. It is intended to provide
a practical audit trail from operational failure mode to risk-management
alignment.

| Failure Mode | Description | Primary S.A.F.E. Control | Evidence Artifact | Related NIST AI RMF Outcome |
|---|---|---|---|---|
| FM-01 | Overbroad target selection | Ambiguity Resolution | Target manifest; target count; target digest | MAP 3.3; MAP 5.1; MANAGE 1.2 |
| FM-02 | Empty or unresolved target set | Ambiguity Resolution | Enumeration log; SAFE stop record | MEASURE 2.6; MANAGE 2.4 |
| FM-03 | Target drift between planning and execution | Separation of Context; Ambiguity Resolution | Targets reference; evidence hash; execution command | MAP 3.3; MEASURE 2.8 |
| FM-04 | AI-generated command executed without review | Separation of Context | Confirmation summary; operator acknowledgement | GOVERN 3.2; MAP 3.5 |
| FM-05 | Successful execution with wrong operational intent | Ambiguity Resolution; Forensic Idempotency | Intent text; target manifest; verification output | MEASURE 2.8; MANAGE 4.1 |
| FM-06 | Silent partial failure | Forensic Idempotency | Execution log; return code; per-target status | MEASURE 2.4; MEASURE 2.6 |
| FM-07 | Verification skipped or incomplete | Forensic Idempotency | Verification log; verification return code; skipped flag | MEASURE 2.3; MEASURE 2.7 |
| FM-08 | Rollback improvised after failure | Evidence-Based Rollback | Snapshot reference; rollback plan reference | MANAGE 4.1; MANAGE 4.3 |
| FM-09 | Replay of a previously executed change | Forensic Idempotency | Change fingerprint; replay-guard registry | MEASURE 3.1; MANAGE 2.4 |
| FM-10 | Secret or sensitive value leaked into run evidence | Forensic Idempotency | Redaction notes; optional secret-scan output | MEASURE 2.7; MANAGE 4.3 |
| FM-11 | AI output treated as privileged authority | Separation of Context | LLM-output handling procedure; SAFE-L2 gate record | GOVERN 3.2; MANAGE 2.4 |
| FM-12 | Evidence unavailable during incident review | Forensic Idempotency; Evidence-Based Rollback | MER; evidence bundle; hash manifest | MEASURE 2.8; MANAGE 4.3 |

The full S.A.F.E. failure-mode catalog remains the authoritative source
for framework-specific failure-mode definitions. This supplementary table
is a crosswalk aid, not a replacement for the main failure-mode matrix.

---

## Limits of Alignment

S.A.F.E. supports selected NIST AI RMF outcomes, but it does not provide
complete coverage of the AI RMF.

In particular:

- S.A.F.E. does not provide model evaluation.
- S.A.F.E. does not validate model training data.
- S.A.F.E. does not manage third-party AI vendor availability or SLAs.
- S.A.F.E. does not guarantee correctness of downstream scripts.
- S.A.F.E. does not prove that verification queries are adequate.
- S.A.F.E. does not provide immutable evidence storage unless paired with
  appropriate storage controls.
- S.A.F.E. does not replace PAM, change management, SIEM, GRC, or incident
  response tooling.

Its contribution is narrower: it defines an execution-control pattern for
AI-assisted privileged changes so that intent, scope, confirmation,
execution, verification, and rollback evidence are captured before the
operation is treated as complete.

---

## Summary Statement

The S.A.F.E. Intent Framework supports selected NIST AI RMF outcomes by
placing a controlled execution boundary around AI-assisted privileged
automation.

Rather than treating AI-generated commands as directly executable,
S.A.F.E. requires privileged operations to pass through a documented
workflow: enumerate targets, snapshot before-state, confirm scope,
execute against the confirmed target set, verify after-state, and produce
a Minimal Evidence Record.

This makes AI-assisted privileged changes more reviewable, auditable,
and recoverable, while preserving human accountability at the point where
system state is changed.
