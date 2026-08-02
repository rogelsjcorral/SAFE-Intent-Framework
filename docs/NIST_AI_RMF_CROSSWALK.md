# NIST AI RMF 1.0 Crosswalk: S.A.F.E. Intent Framework

**Document Version:** 1.0  
**Target Framework:** NIST AI Risk Management Framework 1.0  
**NIST Publication:** NIST AI 100-1  
**Applicable Layer:** SAFE-L2 Execution and Control Runtime  
**License:** CC BY-SA 4.0  

---

## Executive Summary

This crosswalk maps the S.A.F.E. Intent Framework to selected
functions and subcategories of the NIST AI Risk Management Framework
(AI RMF 1.0).

S.A.F.E. addresses a specific operational risk in AI-assisted privileged
automation: an AI-generated or AI-assisted artifact may execute
successfully while applying the wrong intent, target set, or operational
scope.

The framework treats large language models and other AI systems as
proposal sources rather than trusted execution authorities. Privileged
writes are routed through a controlled execution boundary that requires
target enumeration, state snapshotting, explicit confirmation, bounded
execution, post-execution verification, and generation of a Minimal
Evidence Record (MER).

This document is an alignment crosswalk. It does not assert certification
or compliance with NIST AI RMF 1.0. It identifies how S.A.F.E. controls
can support selected NIST AI RMF outcomes across the GOVERN, MAP,
MEASURE, and MANAGE functions.

---

## Technical Architecture Mapping

    +-----------------------------------------------------------------------+
    |                       NIST AI RMF FUNCTIONS                           |
    +--------------------+-------------------+------------------------------+
    | GOVERN / MAP       | MANAGE            | MEASURE                      |
    | Intent, context,   | Execution gates   | Verification, evidence,      |
    | risk tolerance     | and risk response | monitoring, audit support    |
    +---------+----------+---------+---------+---------------+--------------+
              |                    |                         |
              v                    v                         v
    +-------------------+  +----------------+  +-----------------------------+
    | AI-ASSISTED       |  | SAFE-L2 GATE   |  | MINIMAL EVIDENCE RECORD     |
    | PROPOSAL SOURCE   |  | Controlled     |  | Intent, targets, snapshot,  |
    | Suggests action   |  | execution path |  | execution, verification     |
    +-------------------+  +----------------+  +-----------------------------+

---

## NIST AI RMF Core Function Crosswalk

### 1. GOVERN

The GOVERN function establishes organizational policies, processes,
roles, and accountability structures for managing AI risk.

| NIST AI RMF Subcategory | AI RMF Outcome | S.A.F.E. Alignment | Suggested Evidence |
|---|---|---|---|
| GOVERN 1.2 | Trustworthy AI characteristics are integrated into organizational policies, processes, procedures, and practices. | S.A.F.E. provides a repeatable operational control pattern for AI-assisted privileged changes, requiring explicit scope, verification, and evidence before privileged execution is treated as successful. | S.A.F.E. policy profile; SAFE-L2 workflow definition |
| GOVERN 1.3 | Risk management activities are determined according to organizational risk tolerance. | S.A.F.E. supports risk-tiered execution. Higher-risk or higher-blast-radius changes can require stronger confirmation, second approval, or escalation to stricter execution profiles. | Risk-tier policy; confirmation threshold table |
| GOVERN 3.2 | Roles and responsibilities for human-AI configurations and oversight are defined and differentiated. | S.A.F.E. separates AI-assisted proposal generation from privileged execution authority. The AI may propose an action, but the operator and execution gate remain responsible for confirmation and controlled execution. | Human-AI responsibility matrix; confirmation log |
| GOVERN 4.3 | Practices are in place to enable AI testing, incident identification, and information sharing. | MER artifacts preserve operational evidence that can support review, incident triage, lessons learned, and sharing of observed failure modes. | MER records; incident review packet |
| GOVERN 6.2 | Contingency processes are in place for failures or incidents involving high-risk third-party AI systems. | By treating AI-generated operational artifacts as untrusted proposals, S.A.F.E. reduces direct dependency on third-party model correctness during privileged execution. | Third-party AI handling procedure; rollback reference |

---

### 2. MAP

The MAP function establishes context, intended use, system boundaries,
capabilities, risks, and potential impacts.

| NIST AI RMF Subcategory | AI RMF Outcome | S.A.F.E. Alignment | Suggested Evidence |
|---|---|---|---|
| MAP 1.5 | Organizational risk tolerances are determined and documented. | S.A.F.E. allows organizations to define risk thresholds based on target count, environment, action type, reversibility, and blast radius. | Risk tolerance matrix; SAFE-L2 profile |
| MAP 2.2 | Knowledge limits and human oversight of AI system output are documented. | S.A.F.E. assumes AI output may be incomplete, ambiguous, or wrong in scope. It requires operational intent to be resolved into concrete targets before execution. | AI-output handling procedure; scope-resolution log |
| MAP 3.3 | Targeted application scope is specified and documented. | The Enumerate phase resolves vague intent into a bounded target set before any write action is allowed. | Target manifest; target digest |
| MAP 3.5 | Processes for human oversight are defined, assessed, and documented. | The Confirm phase requires the operator to review and accept the resolved scope before the Execute phase begins. | Confirmation record; operator acknowledgement |
| MAP 4.2 | Internal risk controls for AI system components, including third-party AI technologies, are identified and documented. | S.A.F.E. defines the AI proposal source, execution gate, target manifest, verification phase, and MER as separate control points. | Architecture diagram; control inventory |

---

### 3. MEASURE

The MEASURE function supports testing, evaluation, verification,
validation, monitoring, and documentation of AI risk.

| NIST AI RMF Subcategory | AI RMF Outcome | S.A.F.E. Alignment | Suggested Evidence |
|---|---|---|---|
| MEASURE 2.3 | AI system performance or assurance criteria are measured for conditions similar to deployment settings. | S.A.F.E. allows privileged automation to be evaluated against operational assurance criteria such as target accuracy, verification success, partial-failure handling, and rollback readiness. | Test run results; lab or staging MER |
| MEASURE 2.4 | Functionality and behavior are monitored in production. | S.A.F.E. records execution outcomes and verification results for each controlled run, supporting operational monitoring and review. | Execution results; verification results |
| MEASURE 2.6 | AI systems are evaluated regularly for safety risks and ability to fail safely. | S.A.F.E. supports fail-closed behavior when required phases are missing, scope exceeds policy, verification fails, or operator confirmation is absent. | Failed-run MER; policy violation log |
| MEASURE 2.7 | AI system security and resilience are evaluated and documented. | S.A.F.E. evaluates AI-assisted privileged changes against execution controls, bounded target sets, and post-change assertions. | Security test results; SAFE-L2 validation report |
| MEASURE 2.8 | Risks associated with transparency and accountability are examined and documented. | The MER records intent, target-set representation, confirmation, execution results, verification output, and rollback reference for later review. | Minimal Evidence Record |
| MEASURE 3.1 | Existing, unanticipated, and emergent AI risks are tracked over time. | Repeated MER records can be analyzed to identify recurring wrong-scope proposals, failed verifications, high-risk patterns, or confirmation overrides. | MER archive; trend analysis |

---

### 4. MANAGE

The MANAGE function prioritizes, responds to, and treats identified AI
risks, including incident response, recovery, and change management.

| NIST AI RMF Subcategory | AI RMF Outcome | S.A.F.E. Alignment | Suggested Evidence |
|---|---|---|---|
| MANAGE 1.2 | Documented AI risks are prioritized based on impact, likelihood, and available resources or methods. | S.A.F.E. supports prioritization through risk tiers, target count thresholds, environment classification, and action reversibility. | Risk-tier configuration; approval rules |
| MANAGE 1.3 | Responses to high-priority AI risks are developed, planned, and documented. | S.A.F.E. provides a concrete risk treatment for AI-assisted privileged writes: controlled execution gates, target binding, verification, and rollback grounding. | SAFE-L2 workflow; control mapping |
| MANAGE 2.1 | Resources required to manage AI risks are considered, including viable non-AI alternatives. | S.A.F.E. allows organizations to decide when AI assistance is appropriate, when manual execution is safer, and when additional approval is required. | AI-use decision record; escalation policy |
| MANAGE 2.4 | Mechanisms are in place to disengage or deactivate AI systems that produce outcomes inconsistent with intended use. | S.A.F.E. can halt execution when intent, scope, confirmation, execution output, or verification does not match policy. | Fail-closed log; halted execution record |
| MANAGE 4.1 | Post-deployment monitoring, incident response, recovery, and change management mechanisms are implemented. | S.A.F.E. links pre-change snapshots, execution logs, verification outputs, and rollback references into a single MER bundle for review and recovery. | MER forensic bundle; rollback reference |
| MANAGE 4.3 | Incidents and errors are communicated, tracked, responded to, recovered from, and documented. | Failed S.A.F.E. runs produce evidence that can be attached to incident tickets, change records, or post-incident reviews. | Incident ticket attachment; failed-run MER |

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
| NIST CSF 2.0 | DE.AE-03: Information is correlated from multiple sources. | MER artifacts can correlate intent, target manifests, snapshots, command outcomes, and verification results. |
| NIST CSF 2.0 | RS.AN-03: Analysis is performed to determine what occurred during an incident and identify root cause. | MER artifacts support reconstruction of what was intended, what was confirmed, what executed, and what verification observed. |
| NIST SP 800-53 Rev. 5 | AC-6: Least Privilege | S.A.F.E. supports least-privilege execution by separating proposal generation from write-capable execution and by bounding privileged actions to confirmed targets. |
| NIST SP 800-53 Rev. 5 | AU-12: Audit Record Generation | S.A.F.E. requires generation of structured evidence for controlled privileged execution runs. |

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
