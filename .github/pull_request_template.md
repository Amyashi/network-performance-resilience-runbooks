## Summary

Read `CONTRIBUTING.md` and the contribution-only permission in `LICENSE.md`
before preparing or submitting a change.

Explain the smallest coherent change and why it benefits readers or improves
safety, evidence quality, accessibility, or reproducibility.

## Scope and evidence

- Affected editions, files, or guide sections:
- Evidence state: documented, Amy field-verified, other observation, inference,
  controlled experiment, or Amy-untested:
- Primary sources, dates checked, and the claims they support:

## Validation

List the prerequisites, commands, pass/fail gates, rollback checks, affected
PDF and Markdown rebuilds, automated checks, and full rendered-page inspection
performed.

## Checklist

- [ ] I discussed substantial scope in an issue and read `CONTRIBUTING.md`.
- [ ] This change does not overstate certification, completeness, throughput, availability, or universal effectiveness.
- [ ] Consequential steps retain prerequisites, restart guidance, validation, pass/fail criteria, rollback, and failure handling.
- [ ] I rebuilt and reviewed every affected PDF and its matching Markdown companion.
- [ ] Shared Windows content remains synchronized, and Home/Pro differences are explicit.
- [ ] macOS behavior is not described as equivalent to Windows Group Policy.
- [ ] Amy's field observations remain bounded to the named topology and are not used as evidence for Amy-untested 5/5 or 10/10 methods.
- [ ] I checked links, citations, selectable text, bookmarks, reading order, contrast, and small text as applicable.
- [ ] I regenerated and verified release checksums.
- [ ] I have the right to submit this material and agree to the contribution grant in `CONTRIBUTING.md`.
- [ ] I understand that the contribution-only permission does not authorize a separate release, general-purpose modified fork, commercial use, or redistribution outside this contribution process.
- [ ] No commit, branch, comment, attachment, test output, or workflow log contains secrets, personal information, network identifiers, raw diagnostics, or other sensitive evidence.

Security-sensitive changes must follow `SECURITY.md` and must not be disclosed
in a public pull request.
