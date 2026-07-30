# Evidence and source policy

## Evidence labels

- **Proven baseline** - authoritative documentation and safe default behavior.
- **Field verified** - observed in Amy's recorded environment, within the
  topology and hardware stated in the guide.
- **Conditional change** - justified only by a named symptom or deployment
  requirement.
- **Controlled experiment** - one-variable A/B test retained only after a
  repeatable improvement without regression.
- **Avoid** - unsafe bulk changes, unsupported folklore, or advice that
  conflicts with the available evidence.
- **Amy-untested** - documentation-backed method that has not been validated in
  Amy's environment.

## Source hierarchy

The guides prefer primary, authoritative sources:

1. Microsoft documentation for Windows behavior and supported policy paths.
2. Apple documentation for macOS network behavior.
3. Intel and system-OEM documentation for adapters, drivers, and supported
   operating systems.
4. eero and T-Mobile documentation for backup and Wi-Fi behavior.
5. ESnet/iPerf3, Microsoft Sysinternals, and Flent documentation for
   measurement methodology.
6. Cisco documentation where media and transceiver engineering context is
   required.

The complete live-link inventory is rendered in the reference pages of each PDF
and is defined in the builders:

- `CORE_REFS` and `APPENDIX_REFS` in `src/build_guide.py`
- `CORE_REFS` and `SCALE_REFS` in `src/build_macos_guide.py`

Those code lists are canonical. A second manually copied URL inventory is
intentionally avoided so that published references cannot silently drift from
the PDFs.

## Field-evidence boundary

Field observations are not universal performance guarantees. They establish
only what happened on the named path at the recorded time. In particular:

- A 2/2 Gbps result does not prove a 5/5 or 10/10 architecture.
- A simultaneous full-duplex result does not prove every public test server.
- Host failover through T-Mobile and eero Internet Backup are two control
  layers sharing one backup service, not carrier-diverse redundancy.
- Interface metrics choose preferred routes for new traffic; they do not
  migrate established TCP or VPN sessions.
- Historical adapter settings are preserved as context, not promoted as a
  reusable tuning bundle.

## Private-source policy

Raw conversations, turn identifiers, screenshots, personal filesystem paths,
and internal reconciliation notes stay outside version control. Public claims
must be supportable from the guides' field-evidence statements or their
authoritative references without exposing those private materials.
