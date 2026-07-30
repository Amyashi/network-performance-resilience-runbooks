# Accessibility

The project provides the same core implementation guidance in designed PDF and
reflowable Markdown formats. Accessibility defects are treated as publication
defects.

## Available formats

- The
  [Windows 11 Pro Markdown companion](docs/WINDOWS_11_PRO_ACCESSIBLE_GUIDE.md)
  follows the Pro PDF's ordered path, including supported Local Group Policy
  procedures.
- The
  [Windows 11 Home Markdown companion](docs/WINDOWS_11_HOME_ACCESSIBLE_GUIDE.md)
  follows the Home PDF without unsupported Pro-only workarounds.
- The
  [macOS Apple Silicon Markdown companion](docs/MACOS_APPLE_SILICON_ACCESSIBLE_GUIDE.md)
  follows the macOS PDF's direct-host, eero-wide, Wi-Fi, and throughput paths.
- The [Windows 11 Pro PDF](outputs/Windows_11_Pro_Wired_Network_Performance_Resilience_Runbook_v1.0.2.pdf),
  [Windows 11 Home PDF](outputs/Windows_11_Home_Wired_Network_Performance_Resilience_Runbook_v1.0.2.pdf),
  and [macOS PDF](outputs/macOS_Apple_Silicon_Network_Performance_Resilience_Runbook_v1.0.2.pdf)
  are the designed visual editions.

Each Markdown companion contains the essential safety warnings, prerequisites,
commands or interface paths, evidence states, restart decisions, validation,
pass/fail gates, rollback, failure routing, and references for its edition. It
is the preferred accessible alternative when a PDF reader does not expose the
corresponding PDF correctly.

## PDF accessibility features and target

Each release PDF is intended to provide:

- a meaningful edition-specific title and `en-US` language metadata;
- bookmarks for major page sections;
- selectable and searchable text;
- status words in addition to color;
- sufficient small-text contrast;
- descriptive visible reference titles and HTTPS link annotations; and
- a deliberate visual reading order.

The project does not claim PDF/UA, WCAG, Section 508, or other formal
accessibility certification. Bookmarks, metadata, selectable text, automated
checks, and a visually correct render do not establish conformance.

## Release review

Before a public release:

- render and inspect every page of all three PDFs;
- confirm that no text, status, command, reference, or page marker is clipped
  or overlaps another element;
- confirm that color is not the only way meaning is conveyed;
- compare every PDF with its generated Markdown companion;
- test browser zoom and keyboard navigation in the Markdown companions; and
- perform a keyboard and screen-reader spot check of both formats.

## Known limitations

Generated PDFs may not expose every structural relationship, card, code sample,
or decision strip correctly to every assistive technology. Visual order and
assistive-technology reading order can differ. Use the matching Markdown
companion when a PDF feature does not work well with a reader's tools.

The acceptance-record pages are not secure evidence stores. Do not place
sensitive network, account, device, recovery, customer, or location data in a
copy that may be shared.

## Report an accessibility problem

Use the **Guide, build, or accessibility problem** issue form. Identify the
edition, release, page or section, viewer or assistive technology, expected
result, and barrier encountered. Do not include sensitive or identifying
evidence. Follow [SECURITY.md](SECURITY.md) for a security-sensitive defect.
