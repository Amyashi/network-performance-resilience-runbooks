# Network Performance & Resilience Runbooks

Implementation-first Windows 11 Home, Windows 11 Pro, and macOS Apple Silicon
guides for validating and troubleshooting multi-gigabit networks without
cargo-cult tuning.

Version 1.0.2 is a build-tool compatibility and attribution maintenance
release. It updates ReportLab and pdfplumber, adds dependency-notice and
parser-extraction safeguards, and does not change the reader-facing
implementation guidance from v1.0.1. The runbooks separate authoritative
defaults, Amy's bounded field observations, conditional changes, controlled
experiments, and explicitly Amy-untested scaling methods. Every implementation
path emphasizes prerequisites, exact steps, when a restart is actually
required, validation, pass/fail criteria, rollback, and failure handling.

These materials are general educational information. They do not certify a
network, guarantee throughput or availability, replace current vendor
documentation, or substitute for qualified professional advice.

## Choose the guide that matches the endpoint

### Windows 11 Pro

- [Designed PDF guide](outputs/Windows_11_Pro_Wired_Network_Performance_Resilience_Runbook_v1.0.2.pdf)
- [Accessible Markdown companion](docs/WINDOWS_11_PRO_ACCESSIBLE_GUIDE.md)

This edition includes the supported Windows Connection Manager Local Group
Policy path for preferring Ethernet and preventing simultaneous Wi-Fi use
where the documented prerequisites are met.

### Windows 11 Home

- [Designed PDF guide](outputs/Windows_11_Home_Wired_Network_Performance_Resilience_Runbook_v1.0.2.pdf)
- [Accessible Markdown companion](docs/WINDOWS_11_HOME_ACCESSIBLE_GUIDE.md)

This edition preserves automatic fallback without pretending that unsupported
Group Policy workarounds reproduce Windows 11 Pro behavior.

### macOS on Apple silicon

- [Designed PDF guide](outputs/macOS_Apple_Silicon_Network_Performance_Resilience_Runbook_v1.0.2.pdf)
- [Accessible Markdown companion](docs/MACOS_APPLE_SILICON_ACCESSIBLE_GUIDE.md)

This edition covers service order, direct M1 Pro host failover, eero-wide
backup, Wi-Fi context, and documentation-backed throughput methods. macOS
service order ranks active services; it does not reproduce the Windows Pro
policy or preserve established sessions through a path change.

The PDFs are generated visual artifacts. The Markdown companions are the
preferred accessible formats when a PDF reader does not expose document
structure adequately.

## Evidence boundary

Amy's recorded environment includes:

- a Windows 2 Gbps upload / 2 Gbps download symmetric validation path;
- approximately 3.8-3.9 Gbps simultaneous aggregate application throughput in
  the documented run;
- Windows 11 Pro direct-host failover;
- M1 Pro direct-host failover;
- eero Plus Internet Backup switching the full network; and
- eero radio/noise observations that supported making no Wi-Fi change.

The tested direct-host and eero-wide recovery paths both used the same
T-Mobile Home Backup Internet service. They are separate controls sharing the
same carrier, gateway, power, radio, and service-plan failure domain; they are
not carrier-diverse redundancy.

The 5/5 and 10/10 Gbps appendices are documentation-backed methods that Amy did
not field-test. macOS throughput methods at 2/2, 5/5, and 10/10 are also
Amy-untested. Intel card and motherboard examples are compatibility reference
points, not endorsements.

See the [evidence and source policy](docs/EVIDENCE_AND_SOURCES.md) for the
editorial rules behind these labels.

## Safe-use principles

1. Establish recovery, authorization, and a known-good baseline before changing
   a driver, adapter property, service order, route preference, firmware, or
   physical adapter.
2. Record the exact prior value and make one change at a time.
3. Pass a controlled local-network gate before interpreting an Internet result.
4. Treat application throughput as payload evidence, not physical line rate.
5. Record endpoint CPU, temperatures, negotiated modes, counter deltas, route,
   server, direction, stream count, and duration with every stress result.
6. Stop after link instability, new errors or drops, thermal throttling,
   unexplained crashes, data-limit risk, or a measurable regression.
7. Do not run multi-gigabit stress traffic through a metered or limited backup
   connection.
8. Never publish raw diagnostics or evidence containing account, customer,
   device, network, or location identifiers.

Product behavior, subscriptions, service allowances, drivers, firmware, and
documentation change. Recheck current authoritative sources and exact-model
support before relying on a dated instruction.

## Repository layout

| Path | Purpose |
| --- | --- |
| `outputs/*.pdf` | Three reviewed, versioned visual runbooks |
| `outputs/SHA256SUMS.txt` | SHA-256 release-artifact checksums |
| `docs/*_ACCESSIBLE_GUIDE.md` | Generated, reflowable edition companions |
| `docs/EVIDENCE_AND_SOURCES.md` | Evidence labels, source hierarchy, and privacy boundary |
| `src/build_guide.py` | Canonical Windows content and PDF layout |
| `src/build_macos_guide.py` | Canonical macOS content and PDF layout |
| `src/build_accessible_guides.py` | Markdown companion generator |
| `tools/qa_pdfs.py` | PDF-specific structural, text, metadata, link, and bounds checks |
| `scripts/validate_public_release.py` | Repository-wide public-release validation |
| `scripts/update_checksums.py` | Deterministic release checksum generation |
| `tools/make_contact_sheets.py` | Local visual-review contact sheets |
| `requirements.txt` | Direct, version-pinned build and validation dependencies |

Raw chats, private screenshots, source-reconciliation notes, packet captures,
diagnostics, full-size page renders, and contact sheets are deliberately
excluded.

## Rebuild and validate

Use Python 3.12.13. Direct dependencies are version-pinned in
`requirements.txt`, but the installer, platform, and transitive dependency
graph are not fully locked. Treat a rebuild as release validation in the
documented environment, not as a promise of bit-for-bit reproduction across
arbitrary environments.

The PDF builder uses the standard PDF Base 14 Helvetica and Courier families.
No proprietary operating-system font file is copied, embedded, or required.

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

Run the same build and validation commands on every platform:

```sh
python -m pip install --disable-pip-version-check -r requirements.txt
python src/build_guide.py
python src/build_macos_guide.py
python src/build_accessible_guides.py
python scripts/update_checksums.py
python tools/qa_pdfs.py
python scripts/validate_public_release.py
```

Automated checks do not replace visual review. Before release, render every
page with Poppler and confirm that:

- no text, command, status marker, reference, or link is clipped or overlaps;
- page markers, headings, and section transitions remain clear;
- color is not the only way meaning is conveyed;
- reading order remains understandable;
- small text and code remain legible; and
- no sparse or accidental spill page was introduced.

With Poppler's `pdftoppm` on `PATH`, create the required 144-DPI review
renders:

```sh
mkdir -p work/final_render/pro work/final_render/home work/final_render/mac
pdftoppm -png -r 144 outputs/Windows_11_Pro_Wired_Network_Performance_Resilience_Runbook_v1.0.2.pdf work/final_render/pro/page
pdftoppm -png -r 144 outputs/Windows_11_Home_Wired_Network_Performance_Resilience_Runbook_v1.0.2.pdf work/final_render/home/page
pdftoppm -png -r 144 outputs/macOS_Apple_Silicon_Network_Performance_Resilience_Runbook_v1.0.2.pdf work/final_render/mac/page
python tools/make_contact_sheets.py
```

In Windows PowerShell, replace the `mkdir` line with:

```powershell
New-Item -ItemType Directory -Force -Path work/final_render/pro,work/final_render/home,work/final_render/mac
```

Then run the same `pdftoppm` and Python commands. Contact sheets accelerate
review but do not replace inspection of every full-size rendered page.

See [ACCESSIBILITY.md](ACCESSIBILITY.md) for the accessibility target and
[CONTRIBUTING.md](CONTRIBUTING.md) for review requirements.

## Verify a downloaded release

Compare each PDF with [outputs/SHA256SUMS.txt](outputs/SHA256SUMS.txt). The
checksum file covers exactly the three versioned release PDFs. Modified,
unversioned, or checksum-mismatched copies are not supported releases.

The canonical publication target is
[`Amyashi/network-performance-resilience-runbooks`](https://github.com/Amyashi/network-performance-resilience-runbooks).

## Reporting problems

- Use a GitHub issue for a factual error, broken reference, accessibility
  problem, build defect, or evidence-based proposal.
- Use
  [GitHub private vulnerability reporting](https://github.com/Amyashi/network-performance-resilience-runbooks/security/advisories/new)
  for a vulnerability in the repository, automation, or generated artifacts.
- Do not attach unredacted diagnostics or identifying network evidence to
  either channel.

## Release policy

A public release must:

1. rebuild all three PDFs and all three Markdown companions;
2. pass the PDF-specific and repository-wide validators;
3. keep the committed artifacts synchronized with their generators;
4. receive a complete rendered-page visual review and accessibility spot
   check;
5. contain no account, customer, device, network, recovery, or diagnostic
   evidence;
6. keep edition boundaries, citations, citation metadata, license disclosures,
   checksums, and changelog synchronized; and
7. be published from a protected semantic-version tag with
   `outputs/SHA256SUMS.txt`.

The GitHub Release for a version must attach exactly the three versioned PDFs
and `outputs/SHA256SUMS.txt`. Do not attach raw evidence, diagnostics, page
renders, contact sheets, or private source material. Push the reviewed commit
to protected `main`, wait for its validation workflow, create the protected
`vMAJOR.MINOR.PATCH` tag, wait for the tag workflow, and only then publish the
release assets.

## License

The generated PDFs, accessible companions, documentation prose, and
reader-facing guide content embedded in mixed-content source files are licensed
under the
[Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License](LICENSE.md#guide-materials).

The build, validation, workflow, configuration, and automation code is not open
source. It is all rights reserved, with limited permission to download and
execute unmodified copies for personal, noncommercial reproduction and
validation of the unmodified guide materials.

The license also provides a narrow permission to fork, modify, and share
repository material solely as needed to submit a contribution to the official
project. It does not authorize separate modified releases, general-purpose
modified forks, commercial use, or broader redistribution. See
[LICENSE.md](LICENSE.md) for the complete terms.

Third-party components and documentation remain subject to their own rights.
See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
