# Third-party notices

This project uses third-party software to build or validate the guides.
Amyashi claims no ownership of those components, names, marks, documentation,
or license text. This repository's copyright and permission notice does not
replace an upstream license.

| Component | Version | Purpose | License |
| --- | ---: | --- | --- |
| [ReportLab](https://pypi.org/project/reportlab/5.0.0/) | 5.0.0 | PDF generation | BSD-style license |
| [pypdf](https://pypi.org/project/pypdf/6.14.2/) | 6.14.2 | PDF structure, metadata, and link validation | BSD-3-Clause |
| [pdfplumber](https://pypi.org/project/pdfplumber/0.11.10/) | 0.11.10 | PDF text and geometry validation | MIT |
| [Pillow](https://pypi.org/project/pillow/12.3.0/) | 12.3.0 | Local contact-sheet generation | MIT-CMU |

The authoritative license text for each installed package is included in its
distribution and source repository. Transitive dependencies retain their own
license terms. A plain-text reproduction of the license shipped with the
pinned ReportLab distribution is included at
[`licenses/REPORTLAB.txt`](licenses/REPORTLAB.txt).

## Fonts in the PDFs

The builders use the standard PDF Base 14 Helvetica and Courier families
through local aliases. They do not copy, embed, or redistribute Segoe UI,
Consolas, or another proprietary operating-system font file.

PDF viewers may substitute metrically compatible local fonts for Base 14
families. Visual release review therefore remains required.

## External documentation, software, names, and marks

The guides link to documentation and software from Microsoft, Apple, Intel,
eero, T-Mobile, ESnet, Sysinternals, Flent, Cisco, motherboard vendors, and
other publishers. Links and short factual citations do not transfer ownership,
relicense those materials, or imply endorsement.

Microsoft, Windows, Apple, macOS, Intel, eero, T-Mobile, iPerf, PsPing, and all
other product names, company names, and marks belong to their respective
owners. This is an independent informational project and is not affiliated
with, sponsored by, or endorsed by any cited organization.

## Version-specific review

Dependency versions are recorded in `requirements.txt`. Before distributing a
rebuilt artifact or dependency bundle, inspect the license metadata and files
shipped with the exact versions used. This notice is an attribution aid, not a
substitute for those controlling terms.
