# Current project and team-agent instructions

Updated by the owner’s coordination workflow on 2026-10-27. Read this file, PROJECT_STATE.md and docs/handoffs/HANDOFF.md before work. These current instructions supersede earlier scaffold-only, sandbox-only, nested-AML and local-commit-only handoff instructions in Git history or ZIP snapshots.

## Repository, layout and branches

- Canonical team repository: https://github.com/KatalKavya96/DLML_Midsem_Project.git . Do not submit team PRs to DLML-sandbox.
- Use origin/main as the team base and PR target. There is NO prerequisite integration/phase1-handoff branch. Do not create or wait for one.
- The intended implementation layout is directly at this repository root: src/trafficml/, scripts/, tests/, configs/, report/ and slides/. Copy assigned payload CONTENTS to the root without an AML/, DLML-sandbox/ or payload/ wrapper. The coordination-only baseline may contain placeholders until member PRs import implementation files; this is expected, not a reason to reject the layout.
- Fetch the latest origin/main, then create a personal codex/<member>-<module> branch. If the clone points to a fork, retain origin as the personal fork and use upstream/main from the verified canonical repository as base; PR destination remains the canonical repository's main branch.
- The owner’s group instructions authorize each member's agent to push their personal branch and open a PR into canonical main (including from a fork if needed). No further confirmation of that member-branch/PR workflow is needed. No direct-main push, force push or PR merge is authorized for members. The coordinator does not publish this repair without owner direction.

## Scope, ownership and integrity

- Phase 1 traditional ML implementation, review, tests, EDA and documentation are authorized. Phase 2, GAT and calibrated LWR/control implementation remain deferred. Any signal-control work is simulated only.
- Use the package MANIFEST.json and COMMIT_PATHS.txt to verify original payload hashes and restrict staging. docs/handoffs/FILE_OWNERSHIP.json is the shared map. Each member commits only assigned work; do not use git add . or git add -A.
- Shared coordinator-maintained files AGENTS.md, PROJECT_STATE.md, .gitignore, README.md, CONTRIBUTING.md and docs/handoffs/* must preserve these newer directives. When a package contains an older copy of those paths, merge only necessary nonconflicting information; never replace current instructions with historical snapshots. Package manifests are immutable provenance, not authority to overwrite live owner instructions.
- Preserve unrelated edits, existing staged work and actual Git history. Ask only for concrete unresolved repository/identity/conflict information. Do not silently clean/reset/stash or overwrite another person's work.
- Make meaningful scoped commits describing actual integration, review, tests or improvements. Use the configured real identity and actual dates; do not manufacture empty commits, independent authorship or completed student activity.
- The integrated source was prepared by the owner with substantial AI assistance on top of the supplied teammate prototype. Preserve that disclosure. Agent review does not establish that a student understands the implementation; human learning/reproduction remains pending unless demonstrated.
- Keep datasets, node_modules, environments, caches, ZIPs, fitted models, predictions and private slide-build artifacts out of Git. Small documented evidence and academic deliverables may be committed.

## Verification and preservation

- Individual packages depend on other packages. Partial imports may not run; report missing dependencies, skipped checks and failures accurately. Never call prior 56-test results a fresh run. The coordinator verifies the assembled tree before final acceptance.
- Use chronological purged splits, training-only preprocessing, causal features, no target imputation, matching masks/targets and source/data/config fingerprints. Do not tune on the exposed test interval or fabricate scores/citations/approvals.
- Preserve the original Downloads/AML. The canonical local implementation is now at the repository root; delivery files, historical placeholders and private artifacts are in the separate sibling DLML_Project_Archive_2026-10-27 archive. Do not reintroduce nested AML/.
- Faculty scope versus speed-only forecasting, timezone/DST, raw-data rights, exposed test results and final PDF/package/individual viva review remain unresolved. No implementation or commit guarantees final-submission acceptance.

## Owner-authorized integration branch - 2026-10-27

The owner requested syncing merged team work and integrating all remaining required local work on the exact branch `kavya`, overriding the default codex/ prefix for this branch. This includes package 05, necessary shared documentation/evidence, deferred review-log corrections and combined verification. Keep all new commits on kavya; do not commit directly to main. Use the configured real Kavya identity and no co-author trailer; preserve the existing assistance/provenance disclosures. The owner will review the prepared result before raising/merging the final PR. No new model/score tuning, Phase 2 or claim of final faculty acceptance is authorized by this integration.
