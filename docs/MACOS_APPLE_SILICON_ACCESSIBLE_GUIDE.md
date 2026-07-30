# macOS Apple Silicon Network Performance & Resilience Runbook

**Edition:** macOS on Apple silicon
**Version:** 1.0.1
**Release date:** 30 July 2026
**Author:** Amyashi

> This is the substantive, reflowable companion to the matching PDF. It preserves the implementation sequence, safety boundaries, commands, validation gates, rollback guidance, and references. The PDF remains the designed visual edition.

## Evidence boundary

- Amy field-validated direct M1 Pro host failover and eero Internet Backup through the same T-Mobile Home Backup Internet service.
- Those two recovery controls share a carrier, gateway, power, radio, and plan failure domain; they are not carrier-diverse redundancy.
- macOS throughput methods at 2/2, 5/5, and 10/10 Gbps are documentation-backed and Amy-untested.
- Service order ranks active network services; it does not reproduce the Windows Pro policy or preserve established sessions.

Evidence labels are part of the instructions. Do not present an Amy-untested method or controlled experiment as Amy's field result.

Guide materials are licensed as described in [LICENSE.md](../LICENSE.md). Modified or checksum-mismatched copies are outside the supported release.

## Page 1: Cover and scope

Implementation-first Apple-silicon network baseline, direct-host and eero-wide failover, Wi-Fi context, and multi-gigabit validation methods.

---

## Page 2: Use the evidence path that matches the question

**Section:** Start here
**Evidence state:** PROVEN BASELINE

Failover is field evidence. Every macOS throughput target in this edition is a reproducible test method.

### 1  BASELINE

Capture the Mac, adapter, services, routes, eero state, and counters before changing anything.

- Keep a local console/second path.

- Use one declared objective.

### 2  FAILOVER

Reproduce Amy's host-direct and network-wide T-Mobile recovery as two separate tests.

- Expect sessions to reset.

- Verify failback as well as failover.

### 3  THROUGHPUT

Treat 2/2, 5/5, and 10/10 as Amy-untested until the exact Mac path clears the local and WAN gates.

- Local server first.

- Three runs and clean counters.

### 4  OPTIMIZE

Change a service, adapter, SQM, or Wi-Fi variable only for a repeatable symptom.

- One change at a time.

- Roll back neutral results.

### Evidence labels

PROVEN BASELINE - authoritative behavior and safe defaults.

FIELD VERIFIED - Amy observed the stated outcome on the named topology.

CONDITIONAL CHANGE - justified only by a deployment need or symptom.

CONTROLLED EXPERIMENT / AMY-UNTESTED - measured protocol, not Amy's result.

### Release integrity

Use a PDF from the official tagged release and match it to the same-version Markdown companion.

Verify the file against outputs/SHA256SUMS.txt before relying on a downloaded copy.

Modified, unversioned, or checksum-mismatched copies are outside the supported release.

### Decision gate

- **Start [INFO]:** Read pages 3-5 before any change.

- **Restart [PASS]:** None.

- **Pass [PASS]:** Claim and evidence label match.

- **Fail [FAIL]:** A test method is presented as Amy's result.

- **Rollback [WARN]:** Return to baseline and relabel.

---

## Page 3: Amy's tested resilience topology

**Section:** Field record
**Evidence state:** FIELD VERIFIED

Two recovery controls share one T-Mobile Home Backup Internet service and are not carrier-diverse.

### Observed topology and outcomes

**PRIMARY**

Metronet symmetric 2/2 Gbps -> eero gateway/network -> M1 Pro MacBook Pro and other clients.

**DIRECT MAC RECOVERY - SUCCESSFUL**

The tested M1 Pro MacBook Pro was configured to recover directly to the T-Mobile Home Backup Internet Wi-Fi path when its primary Ethernet/eero path was unavailable.

**WHOLE-NETWORK RECOVERY - SUCCESSFUL**

eero Plus Internet Backup was configured to use that same T-Mobile backup Wi-Fi source. A full eero-network switch to it completed successfully.

**WHAT THIS PROVES**

Both control layers worked in the tested conditions. It does not prove a particular recovery time on a future macOS/eero release or under a different cellular signal, allowance, power, or workload.

### Boundaries to preserve

- Both backup modes depend on the same T-Mobile carrier, gateway, power, RF conditions, and usable plan allowance.

- When Ethernet remains linked but the primary WAN fails, eero Internet Backup - not macOS service order - owns network-wide recovery.

- macOS service order is best matched to loss/inactivation of the Ethernet service. It is not a stateful application failover system.

- Existing TCP, VPN, voice, and remote-desktop sessions may reset even when new connections recover.

- A managed work Mac may restrict network services, known Wi-Fi networks, drivers, extensions, VPN behavior, or diagnostics. Obtain the required device-owner authorization before changing them.

- Amy did not field-test macOS iPerf3 at 2/2, 5/5, or 10/10 for this guide. Those sections are documentation-backed methods.

Do not run multi-gigabit stress traffic through a metered/time-limited cellular backup. Test the minimum workload the backup must carry.

### Decision gate

- **Restart [PASS]:** None for understanding the topology.

- **Pass [PASS]:** Both layers and the shared failure domain are named.

- **Expected [WARN]:** Existing sessions may reset.

- **Fail [FAIL]:** Two controls are called two independent carriers.

- **Recovery [INFO]:** Test each layer separately.

---

## Page 4: Safety package before any macOS change

**Section:** Preparation
**Evidence state:** PROVEN BASELINE

Preserve work access, capture the current network location, and avoid weakening Apple silicon startup security.

### Prerequisites

- [ ] Use a local account with the required administrator rights and keep a local console/second path.

- [ ] If the Mac is managed, confirm the allowed test window and whether Wi-Fi, VPN, filters, system extensions, or network locations are managed.

- [ ] Keep the adapter vendor's current Apple-silicon/macOS package and uninstall/rollback instructions offline.

- [ ] Record the current network location, service order, Auto-Join states, VPN/content filters, DNS/proxy state, and adapter hardware mode.

- [ ] Connect power; stop large sync, backup, and update workloads unless they are the declared workload.

- [ ] Name the symptom, test, pass threshold, and rollback before a change.

- [ ] Perform failover from a local session; unplugging the active adapter can terminate remote access.

Do not lower Startup Security or approve a legacy kernel extension merely to make an old NIC work. Select current Apple-silicon support or a DriverKit/class-compliant alternative.

### Stop conditions

- The Ethernet service disappears or negotiates below the target.

- Gateway/DNS/work resources do not return after the declared rollback.

- VPN, endpoint security, content filters, certificates, or device management become unhealthy.

- The adapter resets, link flaps, errors grow, a port/module overheats, or one CPU core stays saturated.

- The T-Mobile plan allowance/signal/power is not ready for the backup test.

- A vendor installer requests a restart you cannot safely schedule.

---

Restore basic connectivity before collecting performance evidence. Never stack a service-order change, driver change, MTU change, and SQM change into one test.

### Decision gate

- **Prerequisite [INFO]:** Authorization, local access, rollback package, power.

- **Restart [PASS]:** Only when macOS/vendor installer explicitly requires it.

- **Pass [PASS]:** One change maps to one repeatable result.

- **Fail [FAIL]:** Work access or rollback is uncertain.

- **Rollback [WARN]:** Undo the last change before more testing.

---

## Page 5: Capture a reusable macOS baseline

**Section:** Baseline
**Evidence state:** PROVEN BASELINE

Run in Terminal. The commands inspect and save state; they do not change the network.

### Create a dated evidence folder

```bash
stamp=$(date +%Y%m%d-%H%M%S)
dir="$HOME/Documents/Network-Baseline-$stamp"
mkdir -p "$dir"
sw_vers > "$dir/macos-version.txt"
system_profiler SPHardwareDataType SPNetworkDataType SPThunderboltDataType \
  > "$dir/system-profile.txt"
networksetup -listallhardwareports > "$dir/hardware-ports.txt"
networksetup -listnetworkserviceorder > "$dir/service-order.txt"
scutil --nwi > "$dir/network-information.txt"
route -n get default > "$dir/default-route.txt"
ifconfig -a > "$dir/interfaces.txt"
netstat -ibdn > "$dir/interface-counters.txt"
```

The Wi-Fi and Ethernet interface names can vary. Use hardware-ports.txt rather than assuming en0/en1.

### Record beside the files

- [ ] Mac model/chip and macOS build

- [ ] Managed or unmanaged device

- [ ] Adapter make/model/firmware/driver

- [ ] Ethernet service + hardware port

- [ ] Negotiated media and MTU

- [ ] Current network location

- [ ] Service order

- [ ] T-Mobile Auto-Join state

- [ ] eeroOS / SQM / backup state

- [ ] Gateway + public route

- [ ] Endpoint CPU/temperature

- [ ] Counter deltas after each run

### Quick live checks before every test set

```bash
networksetup -listnetworkserviceorder
scutil --nwi
route -n get default
networkQuality -v
```

networkQuality is corroboration for responsiveness and capacity to Apple's selected test service; it does not replace a controlled local iPerf3 server.

### Decision gate

- **Restart [PASS]:** None.

- **Pass [PASS]:** Files identify services, ports, route, and before counters.

- **Fail [FAIL]:** Interface names or active route remain unknown.

- **Recovery [INFO]:** Re-run hardware-port and service-order discovery.

- **Preserve [WARN]:** Keep baseline with test results.

---

## Page 6: Adapter, update, and hardware defaults

**Section:** macOS baseline
**Evidence state:** PROVEN BASELINE

Use Automatic hardware configuration and standard MTU unless a supported design requires otherwise.

### Safe starting state

1. Open System Settings > Network and select the Ethernet service.

2. Open Details > Hardware. Record the MAC address and current values.

3. Keep Configure set to Automatically. Keep the normal/standard MTU unless every hop in an isolated design is documented for another value.

4. Record adapter/bridge/dock firmware and any vendor app or system extension.

5. Install a macOS or adapter update only for security/support or a documented problem. Read the restart requirement before starting.

**EXTERNAL 5/10 GBE**

Require explicit support for the exact adapter, Apple silicon, and current macOS release. Prefer a class-compliant or current DriverKit implementation. A connector or chipset name is not a support matrix.

If the vendor requires a legacy kernel extension or Reduced Security, stop and choose a supported alternative unless the device owner explicitly accepts that security tradeoff.

### Avoid cargo-cult macOS tuning

- Forcing speed/duplex when both ends support autonegotiation.

- Enabling jumbo MTU on only the Mac or for an Internet test.

- Copying Linux/Windows sysctl or offload recipes into macOS.

- Persisting undocumented TCP buffer/timer changes for a benchmark.

- Disabling VPN, filters, firewall, or endpoint security to make a score look better.

- Installing an old Intel-only package through Rosetta and assuming its driver supports Apple silicon.

- Keeping an adapter/driver because four streams improved while a single flow, latency, thermals, or work access regressed.

---

Apple delivers built-in network stack fixes with macOS. Third-party Ethernet hardware may add its own app/system extension; use the vendor's supported install and uninstall path.

### Decision gate

- **Restart [WARN]:** Only if macOS/vendor package says so.

- **Validate [INFO]:** Adapter identity, media, MTU, route, gateway, work access.

- **Pass [PASS]:** Automatic mode and supported driver hold target link.

- **Fail [FAIL]:** Reduced Security/legacy driver or link regression.

- **Rollback [WARN]:** Vendor uninstall/known-good package; Automatic hardware.

---

## Page 7: Put Ethernet before Wi-Fi with service order

**Section:** Host path preference
**Evidence state:** CONDITIONAL CHANGE

Apple documents service order for active connections; it does not migrate an established session.

### Exact supported path

1. Confirm Ethernet and Wi-Fi each work independently and save the current order from page 5.

2. Open Apple menu > System Settings > Network.

3. Open the Action (…) menu and choose Set Service Order.

4. Drag the intended Ethernet service above Wi-Fi. Keep VPN services under their managed design; Apple notes VPN priority is handled separately.

5. Select OK. No Mac restart is required.

**VERIFY**

```bash
networksetup -listnetworkserviceorder
route -n get default
scutil --nwi
```

The first active service is attempted before lower services. Confirm both IPv4 and IPv6 behavior, DNS, VPN, and the source interface used by a new connection.

### Boundary and rollback

**THIS CONTROL COVERS**

- Ethernet adapter/cable/port loss that makes the service inactive.

- New connection selection after the lower service becomes active.

**THIS CONTROL DOES NOT GUARANTEE**

- WAN health detection while Ethernet remains linked.

- Preservation of existing TCP/VPN/voice sessions.

- Selection among multiple available Wi-Fi SSIDs.

- Carrier diversity when both backup modes use T-Mobile.

Service order ranks active services; it neither disables nor disconnects Wi-Fi. This guide does not claim a Windows WCM/Group Policy equivalent.

**ROLLBACK**

Return to System Settings > Network > Action > Set Service Order and restore the captured order. If a separate Network Location was used, return to the captured location.

Do not delete services to change preference. An inactive/removed service can defeat automatic recovery.

### Decision gate

- **Restart [PASS]:** None.

- **Pass [PASS]:** New traffic uses Ethernet while it is active.

- **Fail [FAIL]:** Wrong route/family, DNS/VPN failure, or Wi-Fi disabled.

- **Rollback [WARN]:** Restore captured service order/location.

- **Next [INFO]:** Prepare and test the T-Mobile Wi-Fi profile.

---

## Page 8: Prepare the direct T-Mobile Wi-Fi fallback

**Section:** Host resilience
**Evidence state:** FIELD VERIFIED

Keep the backup network known and test current macOS behavior; do not assume SSID selection.

### Profile and path preparation

1. Power the T-Mobile Home Backup Internet gateway and confirm signal, plan allowance, Wi-Fi security, and a lightweight Internet test on another device.

2. On the Mac, open System Settings > Wi-Fi and join the T-Mobile backup network once.

3. Open Wi-Fi > Advanced > Known Networks. Next to the T-Mobile network, confirm Auto-Join is enabled unless device management controls it.

4. Record its private-address, Low Data Mode, DNS, proxy, and managed-network state; do not change them merely for speed.

5. Reconnect the normal primary path and confirm Ethernet remains first in service order.

6. Test the exact failure trigger on page 10. If more than one known Wi-Fi network remains available, verify which SSID macOS actually selects rather than assuming.

A managed profile may prevent forgetting or changing Auto-Join. iCloud Keychain can synchronize forgotten Wi-Fi networks to other devices; do not use Forget as a casual test step.

### When each layer should recover

**PRIMARY WAN FAILS; EERO AND ETHERNET STAY LINKED**

eero Internet Backup should switch the eero network to T-Mobile. macOS service order may see no local link failure.

**ETHERNET/EERO PATH BECOMES UNAVAILABLE**

The Mac's Wi-Fi service can become the lower active service and the known T-Mobile network can provide direct host recovery.

**T-MOBILE GATEWAY/CARRIER/POWER FAILS**

Both backup controls fail together. Restore the primary or use a genuinely independent, authorized path.

**EXISTING APPLICATIONS**

Treat reconnection as application-specific. VPN and long-lived sessions can reset even when a new browser/DNS connection succeeds.

Optional experiment: Low Data Mode may reduce background usage on a constrained backup. Capture its original state and A/B the required workload; it is not part of Amy's recorded outcome.

### Decision gate

- **Restart [PASS]:** None.

- **Pass [PASS]:** Profile is known/Auto-Join; Ethernet still preferred.

- **Fail [FAIL]:** Selection is assumed or management policy is bypassed.

- **Rollback [WARN]:** Restore captured Auto-Join/data/location state.

- **Test [INFO]:** Run direct and eero-wide triggers separately.

---

## Page 9: Reproduce eero-wide Internet Backup

**Section:** Field resilience
**Evidence state:** FIELD VERIFIED

Use the same T-Mobile backup, but score it as a continuity path - not a multi-gigabit benchmark.

### Prerequisites and exact path

- [ ] eero Plus active; eero not in bridge mode.

- [ ] T-Mobile gateway powered, in range, and within usable allowance.

- [ ] Primary eero WAN, wired LAN, and local gateway healthy.

1. In the eero app, open Security & privacy > eero Plus > eero Internet Backup.

2. Add or select the T-Mobile Home Backup Internet Wi-Fi source.

3. Start lightweight gateway/Internet pings and new-connection checks on the Mac plus at least one other eero client.

4. Disconnect only the primary WAN feed from the gateway eero. Keep eero and T-Mobile powered.

5. Record detection/recovery, backup status, DNS, local LAN, public reachability, and the minimum work application.

6. Restore the primary WAN and verify automatic failback after it is stable.

7. Repeat the outage/failback cycle three times; one failed cycle fails validation.

### Pass, fail, and rollback

**PASS**

- Mac and second client create new Internet connections through T-Mobile.

- Local LAN remains reachable as designed.

- The required lightweight workload works within the predeclared recovery objective.

- eero automatically returns to the primary WAN.

**EXPECTED**

Brief downtime and existing-session resets can occur. eero documents that Internet Backup automatically returns when the primary connection is restored.

**FAIL**

Bridge mode, no T-Mobile signal/allowance, shared power loss, DNS failure, or no automatic failback.

**ROLLBACK**

Reconnect the primary WAN. If necessary, disable/remove the backup source in the eero app and restore its captured state.

### Decision gate

- **Restart [PASS]:** No Mac/eero reboot; keep both gateways powered.

- **Pass [PASS]:** New clients recover and fail back.

- **Expected [WARN]:** Existing sessions may reset.

- **Fail [FAIL]:** No DNS/route or T-Mobile unavailable.

- **Preserve [INFO]:** Timestamp eero state and client results.

---

## Page 10: Reproduce direct Mac failover and failback

**Section:** Host resilience
**Evidence state:** FIELD VERIFIED

Trigger Ethernet-path loss locally. WAN-only loss belongs to the eero test on page 9.

### Controlled direct-host test

1. Confirm Ethernet and T-Mobile Wi-Fi each work alone. Restore Ethernet first and keep Wi-Fi enabled.

2. Identify the actual Wi-Fi and Ethernet hardware devices from networksetup -listallhardwareports.

3. Start two Terminal windows and a lightweight new-connection check.

```bash
ping -c 600 -i 0.2 <LOCAL-GATEWAY-IP>
ping -c 600 -i 0.2 1.1.1.1
```

4. Disconnect the Ethernet cable/adapter. Do not power off the T-Mobile gateway. Record loss, selected Wi-Fi SSID, route, DNS, public IP/path, and recovery time.

```bash
networksetup -getairportnetwork <WIFI-DEVICE>
route -n get default
scutil --nwi
```

5. Open new DNS, HTTPS, VPN, and required work connections. Record which existing sessions reset.

6. Reconnect Ethernet. After link stability, verify new traffic returns to Ethernet and the direct T-Mobile path is no longer selected for ordinary traffic.

7. Repeat the outage/failback cycle three times; one failed cycle fails validation.

### Decision gate

**PASS**

The Mac selects the intended T-Mobile Wi-Fi path and restores new connections within the objective declared before testing.

After Ethernet returns, new traffic cleanly prefers it again; DNS/VPN/work resources remain correct.

**FAIL**

- Wi-Fi was off or Auto-Join/profile policy blocked recovery.

- A different SSID was selected.

- No default route/DNS or no failback.

- Management/VPN policy breaks the required workload.

**RECOVERY**

Reconnect Ethernet first, restore the captured service order/location and Auto-Join states, then retest each interface alone.

### Decision gate

- **Restart [PASS]:** None; cable removal is the intended outage.

- **Pass [PASS]:** New traffic recovers and later returns to Ethernet.

- **Expected [WARN]:** Existing TCP/VPN sessions can reset.

- **Fail [FAIL]:** Wrong SSID/route/DNS or no failback.

- **Rollback [WARN]:** Reconnect Ethernet; restore order/profile state.

---

## Page 11: Install and verify the macOS test toolkit

**Section:** Throughput testing
**Evidence state:** AMY-UNTESTED

Built-in ping/networkQuality plus a trusted iPerf3 build; never expose a listener broadly.

### Built-in tools

**LATENCY AND ROUTE**

```bash
ping -c 100 <LOCAL-GATEWAY-IP>
ping -c 100 1.1.1.1
route -n get default
scutil --nwi
```

**APPLE RESPONSIVENESS/CAPACITY CORROBORATION**

```bash
networkQuality -v
networkQuality -h
```

Record the macOS version because available options and the selected Apple test endpoint can change. Responsiveness uses round trips per minute; do not translate it into an invented universal pass threshold.

**COUNTERS**

```bash
netstat -ibdn
ifconfig <ETHERNET-DEVICE>
```

Capture before/after deltas on the tested interface rather than interpreting lifetime totals.

### iPerf3

1. Use an approved package source. If Homebrew is already approved, install with brew install iperf3; otherwise use the ESnet project/source or an organization-managed package.

```bash
iperf3 --version
```

2. Run the server only on a controlled wired endpoint with capacity above the target.

```bash
iperf3 -s -p 5201
```

3. Scope the host firewall/test VLAN to the intended private client. Do not create an Internet port-forward.

4. Record the exact iPerf3 version, server, hash/package source, route, and endpoint CPU.

A public server can be a secondary observation only when its owner permits the load. It is not the default for reproducible 2/2, 5/5, or 10/10 testing.

### Decision gate

- **Prerequisite [INFO]:** Approved binaries; controlled endpoint; scoped firewall.

- **Restart [PASS]:** None for tools.

- **Pass [PASS]:** Versions run; server is attributable and private.

- **Fail [FAIL]:** Unknown binary/server or broad listener exposure.

- **Rollback [WARN]:** Stop listener and remove scoped rule.

---

## Page 12: Pass the wired local gate first

**Section:** Throughput testing
**Evidence state:** AMY-UNTESTED

The adapter, Thunderbolt/USB path, switch, server, media, and CPU must clear the target before the ISP is tested.

### Local sequence

- [ ] Draw every hop; record adapter, dock/chassis, cable/module, switch port, and negotiated rate.

- [ ] Use a wired server whose NIC, PCIe/USB/Thunderbolt path, CPU, and switch port exceed the target.

- [ ] Pause VPN/cloud sync/backups unless they are the declared real workload.

```bash
networksetup -getMedia "<ETHERNET-SERVICE>"
netstat -ibdn
iperf3 -c <LAN-SERVER-IP> -P 1 -t 30 -O 5
iperf3 -c <LAN-SERVER-IP> -P 4 -t 30 -O 5
iperf3 -c <LAN-SERVER-IP> -R -P 4 -t 30 -O 5
```

1. Run one stream, then four; use eight only while throughput is still rising.

2. Repeat the selected stream count three times in both directions.

3. Capture counter deltas, interval stability, per-core CPU, and adapter/dock temperature.

### Local acceptance gate

**PASS**

- Median application throughput >=90% of the slower negotiated link, or a documented platform ceiling.

- No unexplained run <85% of negotiated rate.

- No local error/drop delta, link renegotiation, driver reset, saturated core, or thermal drift.

**FAIL - STAY LOCAL**

- Wrong media: inspect adapter, cable/module, port, autonegotiation, dock/chassis, and driver.

- One direction slow: swap endpoints/ports and inspect receive CPU/driver.

- More streams plateau early: inspect endpoint CPU, bus sharing, server, and switch.

Do not use a WAN result to excuse a failed local gate.

### Decision gate

- **Restart [WARN]:** Only if the adapter/driver package explicitly requires it.

- **Pass [PASS]:** Three-run local gate with clean counters/thermals.

- **Fail [FAIL]:** Stay local; do not tune WAN/SQM.

- **Rollback [WARN]:** Return last adapter/media/MTU change.

- **Next [INFO]:** Proceed to the declared WAN tier.

---

## Page 13: macOS 2/2 Gbps validation method

**Section:** 2/2 Gbps method
**Evidence state:** AMY-UNTESTED

This is not Amy's Windows 3.8-3.9 Gbps result; reproduce it on the Mac before making any claim.

### Idle and one direction at a time

**BASELINE**

```bash
ping -c 300 -i 0.2 <LOCAL-GATEWAY-IP>
ping -c 300 -i 0.2 1.1.1.1
networkQuality -v
```

**UPLOAD / REVERSE DOWNLOAD**

```bash
iperf3 -4 -c <CONTROLLED-SERVER> -P 8 -t 120 -O 10
iperf3 -4 -c <CONTROLLED-SERVER> -R -P 8 -t 120 -O 10
```

1. Characterize a new endpoint with 1, then 4, then at most 8 streams; keep the one-stream result.

2. Run upload and download separately three times each.

3. Use a second controlled endpoint/time if WAN results vary.

4. Record route, VPN/Private Relay state, SQM, server, interval output, counters, CPU, and temperature.

### 2 Gbps method gate

**EACH DIRECTION**

Median >=1.8 Gbps; no unexplained run <1.7 Gbps; stable plateau; clean local counter deltas; no saturated endpoint core.

**INTERPRETATION**

- Local pass + one WAN server miss: endpoint/route first.

- Repeatable miss across controlled servers: inspect service provisioning, router, adapter, CPU, and SQM state.

- Gateway flat but Internet latency rises: WAN/upstream/remote queue.

- Gateway and Internet both rise: client/router/local queue.

**DO NOT CLAIM**

networkQuality or one browser test alone validates symmetric 2/2. It uses a selected remote service and is corroboration, not path isolation.

### Decision gate

- **Restart [PASS]:** None.

- **Pass [PASS]:** Both directions independently clear the gate.

- **Conditional [WARN]:** Public/remote miss; controlled paths pass.

- **Fail [FAIL]:** Same bounded deficit across controlled paths.

- **Next [INFO]:** Run simultaneous load only after both pass.

---

## Page 14: macOS simultaneous 2/2 method

**Section:** 2/2 Gbps method
**Evidence state:** AMY-UNTESTED

Use two sessions and concurrent pings; the Windows field record is context, not a Mac result.

### Four-terminal run order

1. Start local-gateway and Internet pings, then wait about 10 seconds.

```bash
ping -c 800 -i 0.2 <LOCAL-GATEWAY-IP>
ping -c 800 -i 0.2 1.1.1.1
```

2. Start upload and reverse-download as close together as practical.

```bash
# Terminal A - upload
iperf3 -4 -c <UPLOAD-SERVER> -P 8 -t 150 -O 15
# Terminal B - reverse download
iperf3 -4 -c <DOWNLOAD-SERVER> -R -P 8 -t 150 -O 15
```

3. Record sender/receiver totals, interval stability, retransmissions, ping distributions/loss, route, counter deltas, CPU, and thermals.

4. Repeat three times. Add streams only to characterize a non-plateauing endpoint; never to hide a weak single-flow result.

Separate controlled servers or ports reduce the chance that one remote endpoint/process masks full-duplex capacity.

### Acceptance

**TARGET**

Upload >=1.8 Gbps and download >=1.8 Gbps at the same time; aggregate >=3.6 Gbps.

**ALSO REQUIRED**

- Three repeatable runs.

- Zero local error/drop delta.

- Stable link and endpoint headroom.

- Declared loaded-latency objective.

**EVIDENCE BOUNDARY**

Amy's approximately 3.8-3.9 Gbps aggregate was recorded on Windows/I225-V/eero/Metronet. Until this Mac procedure passes, cite no equivalent Mac result.

### Decision gate

- **Restart [PASS]:** None.

- **Pass [PASS]:** Each >=1.8; aggregate >=3.6; counters clean.

- **Fail [FAIL]:** Repeatable controlled deficit or local errors.

- **Rollback [WARN]:** Stop load; restore adapter/SQM baseline.

- **Record [INFO]:** Keep all terminals and counter snapshots.

---

## Page 15: Loaded latency: networkQuality plus SQM A/B

**Section:** Latency under load
**Evidence state:** CONTROLLED EXPERIMENT

Use Apple responsiveness as corroboration and gateway/Internet pings to localize the queue.

### A/B sequence

1. Record the current eero SQM state. In the eero app: Settings > Advanced networking > under Network services > SQM.

2. Run networkQuality -v twice at idle and record upload/download capacity, idle latency, and responsiveness.

3. Run idle, download-only, upload-only, and simultaneous iPerf3 loads while pinging the gateway and Internet.

4. Toggle SQM. No eero/Mac reboot is normally required; allow the network to settle.

5. Repeat the identical servers, commands, order, client power state, and time window three times.

6. Compare throughput, gateway and Internet latency/loss, networkQuality responsiveness, counters, and the actual work application.

```bash
networkQuality -v
ping -c 300 -i 0.2 <LOCAL-GATEWAY-IP>
```

eero documents that SQM is unavailable in bridge mode and can reduce peak throughput while improving latency-sensitive traffic.

### Decision rule

**KEEP SQM WHEN**

- Gateway/Internet loaded latency or Apple responsiveness improves repeatedly.

- The required application improves.

- Throughput stays above its predeclared floor.

**ROLL BACK WHEN**

- The gain is neutral/inconsistent.

- Throughput cost or application regression is unacceptable.

**INTERPRET**

Gateway stays low while Internet rises: likely WAN/upstream/remote queue. Both rise: investigate the Mac, adapter, eero, or local queue.

Do not convert Apple's round trips per minute into an invented universal grade. Compare the same Mac/path/state against itself.

### Decision gate

- **Restart [PASS]:** No reboot; allow eero state to settle.

- **Pass [PASS]:** Repeatable responsiveness gain above throughput floor.

- **Fail [FAIL]:** Neutral, unstable, or harmful result.

- **Rollback [WARN]:** Restore the captured SQM state.

- **Record [INFO]:** Keep both states and all four workloads.

---

## Page 16: Amy's eero radio record: healthy, no change

**Section:** Wi-Fi optimization
**Evidence state:** FIELD VERIFIED

Two wired eero Pro 7 nodes already had excellent 5/6 GHz conditions and no symptom that justified tuning.

### 2.4 GHz - busy air, quiet network

**REPRESENTATIVE NODE A SNAPSHOT**

Total busyness 48% = 4% activity on this radio + 44% other-device interference. 24-hour average 36%; P99 47%; maximum 59%; noise floor -111 dBm; channel 6 at 20 MHz.

**LATER OBSERVATIONS ACROSS BOTH NODES**

Averages were roughly 28-30%, current readings roughly 26-36%, and noise floor roughly -95 to -107 dBm. Node B sometimes heard more RF energy than Node A.

**DECISION**

The eero network itself occupied little airtime; neighboring/other transmitters explained most of the busy time. With stable latency, no loss/disconnect symptom, and clean higher bands, no change was warranted.

Official eero definitions: total busyness is own-radio activity plus other-device interference; P99 describes the worst 1% more usefully than one maximum spike.

### 5 and 6 GHz - exceptionally clean

**5 GHZ**

Current busyness 4% = 1% own + 3% other; 24-hour average 5%; P99 9%; one transient maximum 69%; noise floor -105 dBm; channel 130 at 240 MHz.

**6 GHZ**

Across the wired Pro 7 nodes, average busyness was about 2%, P99 3%, maximum 4-5%, and noise floor about -107 dBm.

**CONTEXT**

eero documents 240 MHz channel support on Wi-Fi 7 5/6 GHz radios. DFS operation and an isolated maximum are not failures by themselves; correlate a channel event with a real client symptom.

**EVIDENCE BOUNDARY**

These values describe Amy's two-node, Ethernet-backhauled home at the observed times. They do not define universal pass thresholds, predict every client, or prove Wi-Fi can carry the wired 2/2 service rate.

### Decision gate

- **Prerequisite [INFO]:** Compare 24-hour data and actual client symptoms.

- **Restart [PASS]:** None; no setting changed.

- **Pass [PASS]:** Healthy clients + low sustained own activity + stable tests.

- **Fail [FAIL]:** A single maximum or neighbor traffic is treated as a fault.

- **Decision [WARN]:** Preserve the working topology and automatic control.

---

## Page 17: Optimize Wi-Fi only after a client fails a test

**Section:** Wi-Fi optimization
**Evidence state:** CONDITIONAL CHANGE

Observe -> localize -> change one physical or feature variable -> retest -> roll back if it does not help.

### Measurement sequence

1. Name the affected device, room, application, time window, and symptom. Keep a wired client as the control.

2. In the eero app: Home > select an eero > Wifi radio analytics. Choose 24 hours and record each node/band: average, P99, maximum, total, own activity, other interference, noise floor, channel, width, and channel-change times.

3. Run Settings > Troubleshooting > Device coverage scan. Treat an eero result of zero poor connections as healthy; follow placement guidance for a poor device.

4. From the same client position, ping the gateway and test both directions to a wired local server before testing the Internet.

```bash
iperf3 -c <WIRED-LAN-SERVER> -t 60 -O 5
iperf3 -c <WIRED-LAN-SERVER> -R -t 60 -O 5
```

5. Repeat three times on the same client, position, power state, band, and server. If aggregate capacity is the question, repeat separately with -P 4; do not hide the one-stream result.

Runbook consistency gate: no loss/abort, and each direction's slowest run is at least 85% of its three-run median. Choose a client-specific throughput target before testing.

Wi-Fi is shared, half-duplex airtime. Do not apply the wired 2/2, 5/5, or 10/10 gates to a wireless client; its radio, channel width, signal, contention, and power state may be the ceiling.

### Symptom-driven changes and stop rules

**IF OWN-RADIO ACTIVITY IS SUSTAINED AND THE CLIENT IS SLOW**

Identify local talkers, backups, cameras, or downloads; pause/reschedule one source and repeat the identical test.

**IF COVERAGE SCAN REPORTS A POOR CONNECTION**

Move the affected eero/client away from obstructions and retest. Add a node only when measured coverage remains poor and the app's guidance supports it; validate that contention and roaming do not worsen.

**IF OTHER INTERFERENCE IS HIGH BUT CLIENTS ARE HEALTHY**

Observe. eero chooses channels automatically and does not expose ordinary manual channel/width selection. Keep Ethernet backhaul and Client Steering defaults unless a documented compatibility symptom requires an A/B test.

**OPERATOR HEURISTICS - NOT EERO SPECIFICATIONS**

A high-performance client around -65 dBm or better, sustained busyness around 70-80%+, or noise approaching -90 dBm can justify closer investigation only when a repeatable symptom agrees. They are not automatic change thresholds.

Avoid repeated reboots to chase a channel: eero says long-term channel optimization takes roughly 2 days to 1 week, and resets restart that learning.

### Decision gate

- **Restart [PASS]:** Normally none; allow automatic optimization to settle.

- **Pass [PASS]:** No loss; >=85% consistency; declared client target met.

- **Fail [FAIL]:** No repeatable gain, new poor devices, or worse latency.

- **Rollback [WARN]:** Restore prior placement/toggle; leave ACS automatic.

- **Escalate [INFO]:** Capture graphs, scan, client details, and exact times.

---

## Page 18: Localize the first failing boundary

**Section:** Troubleshooting
**Evidence state:** PROVEN BASELINE

Service -> local adapter/path -> controlled WAN -> simultaneous load -> application.

### Signal -> next check

Ethernet service absent/wrong media - adapter power, cable/module, dock/chassis, port, supported driver, Hardware = Automatic.

Wrong route after failback - service order, active Network Location, IPv4/IPv6, VPN/filter, and scutil --nwi.

Local iPerf3 slow - swap endpoint/port/media; inspect single core, bus sharing, server capacity, thermals, and counters.

Only one WAN server slow - retest a controlled second server/route/time; do not tune the Mac around a shared public endpoint.

Single direction slow - swap sender/receiver roles; inspect receive path, endpoint CPU, service shaping, and adapter driver.

Only simultaneous load slow - test eero/router full-duplex NAT/firewall/SQM capacity and endpoint contention.

Wi-Fi local test slow but wired control clean - use the two Wi-Fi pages; do not call the ISP first.

### Failure routing

**DIRECT MAC FAILOVER**

Wrong/no SSID -> Wi-Fi/Auto-Join/managed profile. Right SSID, no Internet -> T-Mobile gateway/signal/allowance/DNS. No Ethernet failback -> service order/location/link.

**EERO-WIDE FAILOVER**

Bridge mode or backup source absent -> eero configuration. Backup selected but no clients online -> T-Mobile/DNS. One client only -> client/VPN/policy.

**THROUGHPUT**

Local gate fails -> stay local. Local passes but all controlled WAN endpoints fail -> provisioning/router/ISP evidence package. One public server fails -> conditional endpoint/path result.

**EVIDENCE PACKAGE**

Timestamps, topology, service order, route, macOS/adapter/eero versions, exact commands, interval output, CPU, counter deltas, ping/networkQuality, failover status, and rollback result.

### Decision gate

- **Restart [WARN]:** Only after a supported package says so.

- **Pass [PASS]:** Earliest failed boundary is identified.

- **Fail [FAIL]:** Multiple variables change before localization.

- **Rollback [WARN]:** Undo last change; repeat same boundary.

- **Escalate [INFO]:** Send evidence, not one speed screenshot.

---

## Page 19: Rollback and acceptance record

**Section:** Closeout
**Evidence state:** PROVEN BASELINE

Restore basic connectivity first; keep a result only when the before state and recovery are reproducible.

### Rollback matrix

Service order/location - restore the captured order/location. No reboot. Verify route, DNS, IPv4/IPv6, VPN, and Ethernet preference.

T-Mobile Auto-Join/data settings - restore captured Wi-Fi values. No reboot. Test the primary and backup independently.

Ethernet Hardware/MTU - restore Configure = Automatically and standard/prior MTU. Link reset may occur; reboot rarely needed.

Adapter app/driver/extension - use the vendor's uninstall/known-good package. Restart only when prompted. Never improvise removal of system files.

SQM - restore captured toggle; allow settling; repeat idle plus one loaded run. No reboot.

eero Internet Backup - reconnect primary WAN first; restore/remove backup source only if required. Keep gateways powered.

Emergency order: stop load -> reconnect Ethernet/primary WAN -> restore order/location/profile -> undo last change -> restart only if required -> verify gateway/DNS/work access.

### Acceptance record

- [ ] Mac model/chip/build: ______________________________

- [ ] Adapter/driver/media/MTU: __________________________

- [ ] Service order/location: _____________________________

- [ ] Primary + T-Mobile path: ____________________________

- [ ] Direct failover / failback: _________________________

- [ ] eero-wide failover / failback: ______________________

- [ ] Local median / lowest: ______________________________

- [ ] WAN up / down / simultaneous: _______________________

- [ ] Latency/responsiveness/SQM: _________________________

- [ ] Counter/CPU/thermal result: _________________________

- [ ] Outcome: PASS / CONDITIONAL / FAIL / ROLLED BACK

- [ ] Rollback verified: YES / NO / N/A

### Decision gate

- **Accept [PASS]:** All declared gates and recovery pass.

- **Conditional [WARN]:** Remote/path exception is bounded and recorded.

- **Reject [FAIL]:** Missing baseline, repeatability, or rollback.

- **Integrity [PURPLE]:** Record the release version and verify its checksum.

- **Privacy [INFO]:** Keep raw diagnostics and identifying evidence private.

---

## Page 20: 5/5 and 10/10 Gbps Apple-silicon stress-test method

**Evidence state:** AMY-UNTESTED

This separate appendix is documentation-backed and was not field-tested by Amy on the M1 Pro MacBook Pro.

A Thunderbolt label is not Ethernet throughput proof. The adapter, enclosure, driver, shared bus, switch, router, media, endpoint CPU, thermals, and test server all remain gates.

---

## Page 21: Architecture prerequisites for 5 and 10 Gbps

**Section:** Scaling appendix
**Evidence state:** AMY-UNTESTED
**Appendix boundary:** Documentation-backed and not field-tested by Amy.

The slowest hop and the busiest shared bus set the result.

### Every boundary must clear the target

- [ ] M1 Pro Thunderbolt/USB port and cable expose the adapter's required mode.

- [ ] Adapter has explicit Apple-silicon/current-macOS support and negotiates the required Ethernet rate.

- [ ] Dock/chassis and other attached devices do not share the tested path into a lower ceiling.

- [ ] Router/firewall/NAT/SQM sustains simultaneous aggregate, not only one-way marketing rate.

- [ ] Switch ports/fabric and every cable/module support the mode without oversubscription.

- [ ] Controlled server NIC, PCIe path, CPU, OS, and storage/workload exceed the target.

- [ ] Endpoint per-core CPU and thermals remain below saturation/throttle.

- [ ] VPN, content filters, Private Relay, backup, and security inspection state is recorded.

- [ ] No errors/drops/link renegotiation before load.

- [ ] WAN handoff/provisioning actually supports the declared tier.

### Preflight and stop gates

```bash
system_profiler SPThunderboltDataType SPNetworkDataType
networksetup -getMedia "<ETHERNET-SERVICE>"
ifconfig <ETHERNET-DEVICE>
netstat -ibdn
```

**INSPECT PHYSICALLY**

- Exact adapter/enclosure/dock model, firmware, power supply, upstream port, and certified host cable.

- Switch/router port combinations, fabric/NAT/SQM throughput, and module/media compatibility.

- Thermal path around copper PHY, SFP+ module, adapter, and enclosure.

**STOP**

Do not start WAN load if the local server has not cleared the target, any hop negotiates low, counters already grow, one core is saturated, or the adapter/enclosure overheats.

### Decision gate

- **Restart [WARN]:** Only after supported driver/firmware install requires it.

- **Pass [PASS]:** Every hop negotiates target with clean idle state.

- **Fail [FAIL]:** Any endpoint/shared bus is below target.

- **Rollback [WARN]:** Known-good adapter/media; Automatic hardware/standard MTU.

- **Next [PURPLE]:** Clear phased local gates.

---

## Page 22: Phased 5/5 and 10/10 gates

**Section:** Scaling appendix
**Evidence state:** AMY-UNTESTED
**Appendix boundary:** Documentation-backed and not field-tested by Amy.

Runbook gate: median >=90%, no unexplained run <85%, three runs, clean counters.

### Stream progression

1. Local: 30 seconds after 5-second omit. WAN: 120 seconds after the local gate passes.

```bash
iperf3 -c <SERVER> -P 1 -t 30 -O 5
iperf3 -c <SERVER> -P 4 -t 30 -O 5
iperf3 -c <SERVER> -P 8 -t 30 -O 5
iperf3 -c <SERVER> -R -P 4 -t 30 -O 5
```

2. Stop adding streams when throughput plateaus; preserve every lower-stream result.

3. Repeat selected count three times per direction, then two simultaneous sessions.

4. Record iPerf3/macOS versions, adapter/media, route, interval stability, retransmissions, counter deltas, per-core CPU, and thermals.

iPerf3 3.16+ uses a separate thread per stream, but endpoints, drivers, and the path can still bottleneck.

### Application-throughput method gates

**5 GBPS PATH**

Single direction median >=4.5 Gbps. Simultaneous: each direction >=4.5 Gbps; aggregate >=9.0 Gbps.

**10 GBPS PATH**

Single direction median >=9.0 Gbps. Simultaneous: each direction >=9.0 Gbps; aggregate >=18.0 Gbps.

**ALSO REQUIRED**

- No unexplained run below 85% of negotiated rate.

- Zero local error/drop delta; stable link.

- No saturated core, shared-bus ceiling, driver reset, or thermal throttle.

These are editorial runbook gates, not Apple, eero, Intel, or ISP guarantees. Payload is lower than nominal PHY rate because of protocol/implementation overhead.

### Decision gate

- **Restart [PASS]:** None for testing.

- **Pass [PASS]:** Median >=90%; all >=85%; clean counters/CPU/thermals.

- **Fail [FAIL]:** Same deficit locally or across controlled endpoints.

- **Rollback [WARN]:** Stop; restore last adapter/media/MTU change.

- **Escalate [PURPLE]:** More streams characterize; never conceal.

---

## Page 23: M1 Pro adapter and Intel-card reality check

**Section:** Scaling appendix
**Evidence state:** AMY-UNTESTED
**Appendix boundary:** Documentation-backed and not field-tested by Amy.

The MacBook Pro has Thunderbolt 4/USB4 ports, not an internal Ethernet PCIe slot.

### External Apple-silicon path

**DOCUMENTED HOST CAPABILITY**

Apple lists three Thunderbolt 4 (USB-C) ports supporting Thunderbolt 4 and USB4 up to 40 Gb/s on both 2021 M1 Pro MacBook Pro sizes. Confirm the exact model identifier in the baseline.

**WHAT TO REQUIRE FROM AN ADAPTER**

- Explicit exact-model support for Apple silicon and the installed macOS release.

- Documented 2.5/5/10 GbE link modes and full-duplex sustained performance.

- Current firmware/DriverKit or class-compliant support; supported uninstall/rollback.

- Dedicated host cable/port and adequate adapter/enclosure power/cooling.

- RJ45/SFP+ media compatibility with the switch and intended length.

Thunderbolt's headline signaling rate is not payload proof. Displays, storage, docks, and other devices can share resources or add thermal/power constraints.

### Intel PCIe cards and motherboards

**DO NOT TRANSPLANT THE WINDOWS RECOMMENDATION**

Intel X710-T2L, X550-T2, and X710-DA2 are useful Windows/PCIe selection references in the companion guides. They are not automatic M1 Pro recommendations.

- A PCIe card requires a Thunderbolt PCIe enclosure with enough lanes, power, cooling, cable bandwidth, and explicit card compatibility.

- The exact NIC still needs a current Apple-silicon/macOS driver. Intel's Windows/Linux support matrix does not establish macOS support.

- Do not rely on Boot Camp drivers, abandoned kernel extensions, or Reduced Security to make an unsupported card work.

- A “10 Gb capable motherboard” checklist belongs to a Windows/desktop path; the M1 Pro MacBook Pro motherboard has no user PCIe slot or built-in Ethernet port.

**PASS**

Adapter + enclosure/dock + host cable + macOS driver + media + switch are documented together and clear the local gate.

### Decision gate

- **Restart [WARN]:** Only if supported adapter package requests it.

- **Pass [PASS]:** Exact end-to-end Apple-silicon combination is supported.

- **Fail [FAIL]:** Support inferred from connector/chipset/headline rate.

- **Rollback [WARN]:** Remove per vendor; restore known-good adapter.

- **Avoid [FAIL]:** Reduced Security for an obsolete NIC.

---

## Page 24: Media, thermals, and a sustained-load gate

**Section:** Scaling appendix
**Evidence state:** AMY-UNTESTED
**Appendix boundary:** Documentation-backed and not field-tested by Amy.

Choose one supported media system end to end and prove it holds rate.

### RJ45 / copper

- For a new 10GBASE-T run, Cat6A is the conservative 100 m choice; follow the exact adapter/switch cable matrix.

- Use certified patch cords/terminations; avoid damaged, flat, sharply bent, or unknown-category cable.

- Verify both ends advertise and negotiate the intended 2.5/5/10G mode.

- 10GBASE-T PHYs and small adapters run warm; provide airflow and monitor link changes under full-duplex load.

**SFP+ / DAC / FIBER**

- Verify adapter/enclosure, switch, module/DAC, firmware, and vendor compatibility together.

- Match passive/active DAC type and length, or fiber type/wavelength/connector/reach.

- Treat SFP+ RJ45 modules as separate high-heat compatibility cases.

**BASELINE**

Automatic hardware configuration, standard MTU, supported driver defaults.

### Ten-minute full-duplex soak

1. Clear the three-run local gate first.

2. Capture starting counters, media, adapter/enclosure temperature, CPU, and power state.

3. Run two simultaneous local iPerf3 directions for 10 minutes after a 15-second omit.

```bash
iperf3 -c <SERVER-A> -P 4 -t 600 -O 15
iperf3 -c <SERVER-B> -R -P 4 -t 600 -O 15
```

4. Compare the final complete 60 seconds with the first complete post-omit 60 seconds.

**PASS**

Final mean is no more than 5% below the initial mean; link remains at target; errors/drops remain zero; no reset, throttle, saturated core, or unsafe temperature.

**FAIL / ROLLBACK**

Stop load; restore known-good media/adapter/MTU; cool hardware; retest one component at a time.

### Decision gate

- **Restart [WARN]:** Link/module reset first; reboot only for package need.

- **Pass [PASS]:** Rate, link, counters, CPU, and thermals hold.

- **Fail [FAIL]:** Drift >5%, renegotiation, errors, reset, or heat.

- **Rollback [WARN]:** Known-good media/adapter; standard MTU.

- **Record [PURPLE]:** Exact port/cable/module/firmware combination.

---

## Page 25: Authoritative references - macOS and core method

**Section:** References
**Evidence state:** PROVEN BASELINE

Reviewed 30 July 2026. Re-check macOS UI, managed-device policy, and vendor support.

- [Apple - Change network service order](https://support.apple.com/guide/mac-help/change-order-network-services-mac-mchlp2711/mac)
- [Apple - Manage network locations](https://support.apple.com/guide/mac-help/manage-network-locations-on-mac-mchlp1175/mac)
- [Apple - Wi-Fi Auto-Join / forget behavior](https://support.apple.com/en-us/102480)
- [Apple - Ethernet settings](https://support.apple.com/guide/mac-help/ethernet-settings-on-mac-mh11939/mac)
- [Apple - Change network hardware settings](https://support.apple.com/guide/mac-help/change-hardware-settings-mac-mchlp2505/mac)
- [Apple - Wireless Diagnostics](https://support.apple.com/guide/mac-help/use-wireless-diagnostics-mchlf4de377f/mac)
- [Apple Developer - networkQuality and responsiveness](https://developer.apple.com/videos/play/wwdc2021/10239/)
- [Apple - System extension alert / legacy kext boundary](https://support.apple.com/en-us/120363)
- [ESnet - Invoking iPerf3](https://software.es.net/iperf/invoking.html)
- [Homebrew - iPerf3 formula](https://formulae.brew.sh/formula/iperf3)
- [eero - Internet Backup](https://support.eero.com/hc/en-us/articles/8947860842523-What-is-eero-Internet-Backup)
- [eero - Smart Queue Management](https://eero.com/support/articles/360000709886-What-is-Smart-Queue-Management-SQM)
- [eero - Wifi Radio Analytics](https://support.eero.com/hc/en-us/articles/15282384606107-Wifi-Radio-Analytics)
- [eero - Coverage scan](https://support.eero.com/hc/en-us/articles/34604365204635-What-is-Coverage-scan)
- [eero - How network optimization works](https://support.eero.com/hc/en-us/articles/360057257311-How-Does-eero-Optimize-My-Network)
- [eero - Client Steering and DFS](https://support.eero.com/hc/en-us/articles/207613326-What-advanced-features-does-eero-support)
- [eero - Ethernet backhaul](https://support.eero.com/hc/en-us/articles/207852743-Can-I-connect-my-eeros-with-Ethernet)
- [T-Mobile - Home Internet Backup](https://www.t-mobile.com/home-internet/plans/5g-backup-internet-options)

**Source-use boundary:** Apple and eero define documented behavior; Amy's field record retains its separate evidence status.

---

## Page 26: Authoritative references - scaling and hardware

**Section:** References
**Evidence state:** AMY-UNTESTED
**Appendix boundary:** Documentation-backed and not field-tested by Amy.

Hardware examples are compatibility checkpoints, not purchase endorsements.

- [Apple - MacBook Pro 14-inch 2021 specifications](https://support.apple.com/en-us/111902)
- [Apple - MacBook Pro 16-inch 2021 specifications](https://support.apple.com/en-us/111901)
- [Apple Developer - NetworkingDriverKit](https://developer.apple.com/documentation/networkingdriverkit)
- [Apple Developer - System Extensions and DriverKit](https://developer.apple.com/system-extensions/)
- [ESnet - Network performance expectations](https://fasterdata.es.net/performance-testing/troubleshooting/network-performance-expectations/)
- [ESnet - Test host tuning](https://fasterdata.es.net/host-tuning/linux/test-measurement-host-tuning/)
- [Intel - X710-T2L specifications](https://www.intel.com/content/www/us/en/products/sku/189463/intel-ethernet-network-adapter-x710t2l/specifications.html)
- [Intel - Retail Ethernet adapter OS matrix](https://www.intel.com/content/www/us/en/support/articles/000025890/ethernet-products.html)
- [Intel - X550-T2 specifications](https://www.intel.com/content/www/us/en/products/sku/88209/intel-ethernet-converged-network-adapter-x550t2/specifications.html)
- [Intel - X710-DA2 specifications](https://www.intel.com/content/www/us/en/products/sku/83964/intel-ethernet-converged-network-adapter-x710da2/specifications.html)
- [Cisco - 10GBASE SFP+ modules](https://www.cisco.com/c/en/us/products/collateral/interfaces-modules/transceiver-modules/data_sheet_c78-455693.html)

**Source-use boundary:** Verify the same-version PDF against outputs/SHA256SUMS.txt before use.

---

End of accessible companion.
