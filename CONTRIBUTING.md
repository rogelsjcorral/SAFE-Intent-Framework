# Contributing

Thank you for helping improve the S.A.F.E. Intent Framework.

This repository contains research material, documentation, and a minimal
reference implementation. Contributions that improve clarity, identify
failure modes, or refine operational semantics are welcome.

---

## How to Contribute

1. Open an **Issue** for questions, missing failure modes, or suggested
   clarifications.
2. For changes, **fork the repository** and submit a **Pull Request**.
3. Describe the motivation for the change and reference any relevant
   operational scenario, paper, or standard.

---

## Contribution Guidelines

• Keep pull requests focused on a single topic.

• If referencing external concepts, papers, standards, or incidents,
  include a citation.

• Do not include secrets, tokens, credentials, or production identifiers
  in examples or logs.

• Prefer clear, testable requirement language when proposing framework
  semantics (MUST, SHOULD, MAY).

• For code contributions, ensure examples remain minimal and suitable for
  a proof-of-concept reference implementation.

---

## Suggested Contribution Areas

• Failure modes and edge cases for privileged automation

• Confirmation thresholds for large target sets

• Integration profiles or SAFE wrapper examples

• MER schema refinements and evidence artifact structure

• Operational scenarios demonstrating SAFE phase enforcement

---

## Scope

The reference wrapper in this repository is intentionally minimal and
serves only to demonstrate SAFE control semantics. Contributions that
attempt to transform the wrapper into a production-grade security system
may be out of scope for this repository.
