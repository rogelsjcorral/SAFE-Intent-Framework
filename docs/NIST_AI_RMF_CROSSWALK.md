# NIST AI RMF 1.0 Crosswalk: SAFE Intent Framework

**Document Version:** 1.0  
**Target Standard:** NIST AI Risk Management Framework (NIST AI RMF 1.0 / NIST SP 1270)  
**Applicable Layer:** Layer 2 (L2) Execution & Control Runtime  
**License:** [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

---

## Executive Summary

This crosswalk provides a formal mapping between the **SAFE (Structured Automation For Execution) Intent Framework** and the core subcategories of the **NIST AI Risk Management Framework (AI RMF 1.0)**. 

While Large Language Models (LLMs) operate as non-deterministic proposal engines, the SAFE Framework establishes an air-gapped, deterministic Layer 2 (L2) runtime boundary. By decoupling non-deterministic intent generation from privileged OS/API execution, SAFE operationalizes NIST AI RMF guidance across the **GOVERN**, **MAP**, **MEASURE**, and **MANAGE** functions.

---

## Technical Architecture Mapping

+------------------------------------------------------------------------+
|                        NIST AI RMF FUNCTIONS                           |
+-------------------+-------------------+--------------------------------+
|  MAP & GOVERN     |     MANAGE        |            MEASURE             |
|  (Intent Stage)   | (Runtime Gate)    |     (Forensics / Integrity)    |
+---------+---------+---------+---------+----------------+---------------+
          |                   |                          |
          v                   v                          v
+-------------------+ +---------------+ +--------------------------------+
|   UNTRUSTED LLM   | |  SAFE L2 GATE | |   MINIMAL EVIDENCE RECORD      |
| Proposes Action   | | AST & Bounds  | | MER / Cryptographic Verification|
+-------------------+ +---------------+ +--------------------------------+

---

## NIST AI RMF Core Function Crosswalk

### 1. GOVERN (GVN)
*Establishing and maintaining culture, processes, and structures for AI risk management.*

| NIST Subcategory | NIST Requirement | SAFE Framework Implementation | Compliance Artifact |
| :--- | :--- | :--- | :--- |
| **GOVERN 1.2** | Management mechanisms are in place to identify and mitigate AI risks in deployment contexts. | Implements a mandatory 5-phase deterministic pipeline (Enumerate -> Snapshot -> Confirm -> Execute -> Verify) before any system state alteration occurs. | Pipeline State Machine |
| **GOVERN 3.2** | Human-in-the-loop (HITL) and automation controls are aligned with risk tolerance thresholds. | High-blast-radius actions or replay detections automatically trigger mandatory human confirmation gates with single-use confirmation tokens (`I CONFIRM <TOKEN>`). | Confirmation Gate Logs |
| **GOVERN 6.1** | Policies and procedures for organizational responsibilities are established for AI system outputs. | Establishes explicit boundaries separating probabilistic text output (L1) from privileged system commands (L2), ensuring untrusted LLM outputs cannot directly execute without L2 compilation. | Architectural Isolation Spec |

---

### 2. MAP (MAP)
*Categorizing context, capabilities, risks, and impacts of AI systems.*

| NIST Subcategory | NIST Requirement | SAFE Framework Implementation | Compliance Artifact |
| :--- | :--- | :--- | :--- |
| **MAP 1.5** | Organizational risks from third-party AI components and non-deterministic tools are mapped. | Treats LLMs as untrusted, uncalibrated proposal engines. All natural language intent strings must resolve into explicit, typed Target Digests rather than raw shell variables. | Target Scope Binding |
| **MAP 3.5** | System boundaries, dependencies, and blast-radius potentials are documented and constrained. | Phase 1 (`Enumerate`) forces the explicit resolution of ambiguous target descriptors into bounded array IDs with SHA256 target digests prior to execution. | Target Array Manifest |

---

### 3. MEASURE (MEA)
*Analyzing, assessing, benchmarking, and monitoring AI risk and system safety.*

| NIST Subcategory | NIST Requirement | SAFE Framework Implementation | Compliance Artifact |
| :--- | :--- | :--- | :--- |
| **MEASURE 2.6** | System performance and safety metrics are monitored post-deployment under operational conditions. | Phase 2 (`Snapshot`) captures pre-change system state baselines to measure execution drift and establish rollback parameters. | Pre-Change Snapshot Digest |
| **MEASURE 2.7** | AI mechanisms are evaluated for safety, correctness, and failure recovery. | Phase 4 (`Verify`) executes post-change state assertions. Non-zero exit codes or invariant failures immediately fail the operational cycle before returning success. | Assertion Exit Codes |
| **MEASURE 2.11** | Auditability and traceability mechanisms are enabled for post-hoc forensic analysis. | Phase 5 generates an immutable **Minimal Evidence Record (MER)** (`mer.json`) containing raw output hashes, redacted parameters, and execution telemetry. | Minimal Evidence Record (MER) |

---

### 4. MANAGE (MNG)
*Allocating resources and implementing risk treatments to control AI risks.*

| NIST Subcategory | NIST Requirement | SAFE Framework Implementation | Compliance Artifact |
| :--- | :--- | :--- | :--- |
| **MANAGE 1.3** | System safety procedures are activated to prevent hazardous state transitions. | The L2 execution layer invokes commands using strict OS process controls (`subprocess` with `shell=False`), preventing command injection and shell-expansion vulnerabilities. | AST Invocation Engine |
| **MANAGE 2.2** | AI agency and execution autonomy are bounded according to system risk profiles. | Implements **Envelope Protection**. If proposed actions exceed the compiled target set or attempt out-of-bounds state mutations, the L2 wrapper executes an unscheduled `SystemExit` (fail-closed). | Fail-Closed Exception Logs |
| **MANAGE 4.1** | Post-incident response mechanisms, including state rollback and isolation, are deployed. | The combination of pre-change state snapshots (Phase 2) and cryptographic verification (Phase 4) enables immediate execution halt and forensic reconstruction following abnormal termination. | MER Forensic Bundle |

---

## OWASP & NIST CSF Cross-Reference

To assist enterprise compliance auditors, SAFE controls mapped to NIST AI RMF simultaneously satisfy adjacent cybersecurity controls:

* **OWASP LLM Top 10 (2025):** Direct mitigation for **LLM08: Excessive Agency** and **LLM06: Unsecure Output Handling**.
* **NIST CSF 2.0:** Aligns with **PR.DS-11** (Data & State Integrity) and **DE.AE-03** (Forensic Evidence & Log Analysis).
* **NIST SP 800-53 Rev. 5:** Maps to **AC-6** (Least Privilege Execution) and **AU-12** (Audit Generation).

---

## Summary Statement for Auditors

> *"The SAFE Intent Framework operationalizes NIST AI RMF recommendations by establishing a deterministic execution perimeter around non-deterministic AI models. By enforcing state snapshotting, scope-bound target enumeration, post-execution verification, and immutable log generation (MER), SAFE ensures that autonomous or semi-autonomous AI operations remain bounded within organizational risk tolerances."*
