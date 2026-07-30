# Security policy

## Supported material

Security corrections are provided for the latest published Windows 11 Home,
Windows 11 Pro, and macOS guides and the current `main` branch. Earlier
releases, forks, modified copies, and untagged artifacts are not independently
maintained.

This policy covers:

- unsafe or materially misleading security-sensitive instructions;
- a build, validation, workflow, or dependency flaw with security impact;
- unexpected active content, embedded files, scripts, unsafe actions, or
  sensitive metadata in a generated PDF; and
- a repository process that could expose credentials, personal information,
  network identifiers, diagnostic evidence, or release integrity.

It does not provide product support for Microsoft Windows, Apple macOS, eero,
T-Mobile, Internet service providers, network hardware, iPerf3, PsPing,
ReportLab, or other third-party products. Ordinary documentation errors belong
in the guide-problem issue form.

## Report privately

Use
[GitHub private vulnerability reporting](https://github.com/Amyashi/network-performance-resilience-runbooks/security/advisories/new).

Include, when safe and relevant:

- the affected release, edition, file, section, page, or commit;
- a concise impact description;
- safe reproduction steps using synthetic or sanitized data;
- a proposed mitigation, if known; and
- only the minimum redacted evidence needed to understand the report.

Do not disclose an unpatched vulnerability in a public issue, pull request,
discussion, commit, branch, release, or attachment.

## Never publish sensitive network evidence

Do not submit passwords, tokens, cookies, certificates, recovery material,
private keys, full logs, packet captures, registry exports, crash dumps,
diagnostic archives, screenshots, serial numbers, hostnames, SSIDs, BSSIDs,
MAC addresses, public IP addresses, account identifiers, plan information,
customer data, or precise location data.

If a credential or secret is exposed, rotate or revoke it immediately.
Deleting the visible file is not sufficient because copies may remain in Git
history, forks, caches, notifications, or workflow logs.

## Handling and disclosure

Reports are reviewed on a best-effort basis. Receipt does not promise a
particular response time, fix, reward, or coordinated-disclosure schedule.
Please allow a reasonable opportunity to investigate and prepare a corrected
release before public disclosure.

Submitting a report does not authorize testing against systems, accounts,
services, devices, or data you do not own or have explicit permission to test.
