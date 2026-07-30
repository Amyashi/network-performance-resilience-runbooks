# Contributing

Thank you for helping improve the Network Performance & Resilience Runbooks.
This is a controlled-author project: issues and well-supported proposals are
welcome, but changes are accepted at the author's discretion.

## Before contributing

Search existing issues before opening a new one. Use:

- **Guide, build, or accessibility problem** for a factual error, broken
  reference, unclear instruction, unsafe ambiguity, build defect, or
  accessibility problem;
- **Improvement proposal** for a substantive procedure, test method,
  structure, or usability change; and
- **GitHub private vulnerability reporting** for a vulnerability in the
  repository, automation, or generated artifacts.

This repository cannot provide individualized device, ISP, eero, T-Mobile,
Windows, macOS, or hardware support.

## Evidence and privacy

Use current primary sources whenever possible. A claim about Windows, macOS,
eero, T-Mobile, network drivers, adapters, motherboards, media, licensing,
product behavior, or performance should include:

- the authoritative source URL;
- the date it was checked;
- the affected edition, OS release, driver, firmware, adapter, hardware
  prerequisite, or service plan;
- the exact topology and measurement boundary needed to interpret the claim;
  and
- a clear distinction between documented behavior, Amy's bounded field
  observation, another contributor's observation, inference, and an untested
  method.

Never submit credentials, recovery material, tokens, certificates, full logs,
dumps, packet captures, registry exports, unredacted screenshots, serial
numbers, hostnames, SSIDs, BSSIDs, MAC addresses, public IP addresses, account
identifiers, precise locations, customer information, plan details, or other
sensitive evidence. Replace necessary examples with neutral placeholders.

## Limited permission to prepare a contribution

The
[contribution-only permission in LICENSE.md](LICENSE.md#contribution-only-permission)
allows you to fork, modify, and share repository material only as reasonably
necessary to prepare, discuss, review, and submit a contribution to the
official
[`Amyashi/network-performance-resilience-runbooks`](https://github.com/Amyashi/network-performance-resilience-runbooks)
repository through GitHub.

That permission does not authorize a separate release, a general-purpose
modified fork, commercial use, or redistribution outside the contribution
process. Preserve existing copyright and license notices, identify your
changes, and do not include third-party material unless you have the right to
submit it under the grant below.

## Useful contributions

- Corrections supported by current primary documentation
- Safer prerequisites, restart gates, validation, rollback, or failure routing
- Clearer separation of defaults, field evidence, conditional changes,
  controlled experiments, and Amy-untested methods
- Reproducible Windows Home, Windows Pro, or macOS build and validation fixes
- Accessibility and plain-language improvements
- Reports that an OS, driver, adapter, eero, T-Mobile, iPerf3, PsPing, or
  dependency change invalidated an instruction

Do not promote a single adapter setting, stream count, speed result, radio
observation, or failover outcome into a universal recommendation.

## Pull requests

Discuss a substantial pull request in an issue first. A pull request should:

1. address one coherent change;
2. identify every affected edition and evidence label;
3. explain prerequisites, restart behavior, validation, pass/fail criteria,
   rollback, and failure handling when a procedure changes;
4. update each affected PDF and matching Markdown companion;
5. keep shared Windows and cross-platform content synchronized while preserving
   edition-specific behavior;
6. update authoritative references and the date checked;
7. rebuild checksums and pass all automated checks;
8. include a complete rendered-page visual review for every changed PDF; and
9. contain no sensitive or identifying evidence.

Opening a pull request makes a proposal; it does not incorporate the change
into the project. The author may edit, combine, defer, decline, remove, or
decline to maintain a contribution.

## Contribution grant

By opening a pull request, posting proposed material in an issue, or otherwise
submitting material through the official repository, you represent that you
have the right to submit it and grant Amyashi a perpetual, worldwide,
non-exclusive, royalty-free, irrevocable license to use, reproduce, modify,
prepare derivative works from, distribute, publicly display, publicly perform,
sublicense, and relicense the contribution as part of this project or related
editions.

The grant covers the material you contribute and revisions you submit during
review; it does not transfer ownership of pre-existing repository material. If
accepted, the author may incorporate and distribute the contribution under the
project terms applicable to the resulting material.

You retain any copyright you hold in your original contribution. The grant
remains effective whether the submission is accepted, edited, declined, or
later removed. Submission does not grant contributors a license to other
repository content beyond the contribution-only permission and does not
otherwise change the terms in [LICENSE.md](LICENSE.md).

## Editorial rules

- Do not describe a guide as certified, exhaustive, guaranteed, or universally
  effective.
- Do not describe application throughput as physical line rate.
- Do not turn Amy's 2/2 Gbps or failover observation into evidence for 5/5,
  10/10, another ISP, another backup carrier, or another topology.
- Keep the T-Mobile direct-host and eero Internet Backup paths separate while
  naming their shared failure domain.
- Keep Windows Home, Windows Pro, and macOS capability boundaries explicit.
- Preserve warnings before consequential commands or hardware work.
- Keep public evidence sanitized and non-identifying.
- Do not add telemetry, analytics, network calls, or external services without
  prior discussion.

## Local validation

Use Python 3.12.13 and the documented dependency versions:

Create and activate a virtual environment on Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```sh
python3 -m venv .venv
. .venv/bin/activate
```

Run the common validation sequence:

```sh
python -m pip install --disable-pip-version-check -r requirements.txt
python src/build_guide.py
python src/build_macos_guide.py
python src/build_accessible_guides.py
python scripts/update_checksums.py
python tools/qa_pdfs.py
python scripts/validate_public_release.py
```

Automated validation is necessary but not sufficient. Render and inspect every
page of every changed PDF before marking a change ready for release.

With Poppler's `pdftoppm` on `PATH`, run:

```sh
mkdir -p work/final_render/pro work/final_render/home work/final_render/mac
pdftoppm -png -r 144 outputs/Windows_11_Pro_Wired_Network_Performance_Resilience_Runbook_v1.0.1.pdf work/final_render/pro/page
pdftoppm -png -r 144 outputs/Windows_11_Home_Wired_Network_Performance_Resilience_Runbook_v1.0.1.pdf work/final_render/home/page
pdftoppm -png -r 144 outputs/macOS_Apple_Silicon_Network_Performance_Resilience_Runbook_v1.0.1.pdf work/final_render/mac/page
python tools/make_contact_sheets.py
```

On Windows, replace the `mkdir` line with:

```powershell
New-Item -ItemType Directory -Force -Path work/final_render/pro,work/final_render/home,work/final_render/mac
```

Then run the same rendering commands. Inspect every full-size page; contact
sheets are navigation aids, not the acceptance record.

Raw chats, private screenshots, source-reconciliation notes, packet captures,
diagnostics, full-size page renders, and contact sheets are deliberately
excluded.

## Publisher-only release steps

1. Confirm the public branch has a clean-root history with no private
   pre-publication commits.
2. Confirm protected rules exist for `main` and semantic-version tags matching
   `v*.*.*`, and that private vulnerability reporting is enabled.
3. Update the version, release date, changelog, citation metadata, filenames,
   checksums, and validation expectations together.
4. Complete the build, automated checks, full-page visual review,
   accessibility spot check, and privacy review.
5. Push the reviewed commit to `main` and wait for its workflow to pass.
6. Create the protected annotated version tag and wait for the tag workflow to
   pass.
7. Publish a GitHub Release containing exactly the three versioned PDFs and
   `outputs/SHA256SUMS.txt`. Do not attach private evidence, page renders,
   contact sheets, or diagnostic material.
