#!/usr/bin/env bash

# Example SAFE-L2 PoC execution
# Demonstrates enumeration → snapshot → confirmation → execution → verification

python poc/safe-l2-wrapper/safe_l2_reference_wrapper.py \
  --env prod \
  --change-class iam \
  --risk-tier high \
  --intent "Disable legacy authentication for tenants in OU=Sales" \
  --ticket "CHG-12345" \
  --enumerate "python poc/sample-scripts/enumerate_targets.py" \
  --snapshot "python poc/sample-scripts/snapshot_state.py --targets-file {targets_ref}" \
  --execute "python poc/sample-scripts/apply_change.py --targets-file {targets_ref}" \
  --verify "python poc/sample-scripts/verify_state.py --targets-file {targets_ref}" \
  --secret-scan-cmd "python poc/sample-scripts/secret_scan.py --dir {evidence_dir}"

echo ""
echo "SAFE demo run complete."
echo "Evidence bundle created under .safe_evidence/"
