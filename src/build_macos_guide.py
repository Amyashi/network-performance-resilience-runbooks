"""Build the macOS Apple-silicon network runbook."""

from __future__ import annotations

import math
from pathlib import Path

from reportlab.lib.colors import HexColor, white

from build_guide import (
    AMBER_PALE,
    BLUE,
    BLUE_PALE,
    CODE_BG,
    GREEN,
    GREEN_PALE,
    INK,
    LINE,
    MUTED,
    NAVY,
    PAPER,
    PURPLE,
    PURPLE_PALE,
    RED,
    RED_PALE,
    RELEASE_DATE_LONG,
    ROOT,
    SLATE,
    TEAL,
    TEAL_DARK,
    TEAL_PALE,
    WHITE,
    VERSION,
    Guide,
    PAGE_H,
    PAGE_W,
    b,
    check,
    code,
    label,
    p,
    page_wifi_evidence,
    page_wifi_protocol,
    register_fonts,
    rr,
    s,
    wrap,
)


OUTPUT = ROOT / "outputs" / f"macOS_Apple_Silicon_Network_Performance_Resilience_Runbook_v{VERSION}.pdf"
TOTAL_PAGES = 26


def cover(g: Guide) -> None:
    g.page_no += 1
    c = g.c
    g.add_bookmark("Cover")
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.rect(0, 0, 13, PAGE_H, fill=1, stroke=0)
    rr(c, 40, 56, PAGE_W - 80, PAGE_H - 96, 22, NAVY, NAVY)
    c.setFillColor(HexColor("#174466"))
    c.circle(PAGE_W - 128, PAGE_H - 145, 76, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.circle(PAGE_W - 128, PAGE_H - 145, 49, fill=1, stroke=0)
    c.setFont("Segoe-Light", 32)
    c.setFillColor(WHITE)
    c.drawCentredString(PAGE_W - 128, PAGE_H - 155, "M1")
    c.setFont("Segoe-Bold", 7.5)
    c.drawCentredString(PAGE_W - 128, PAGE_H - 180, "PRO FIELD PATH")
    c.setFont("Segoe-Bold", 8)
    c.setFillColor(TEAL)
    c.drawString(74, PAGE_H - 105, "IMPLEMENTATION-FIRST macOS / APPLE SILICON GUIDE")
    c.setFont("Segoe-Bold", 29)
    c.setFillColor(WHITE)
    c.drawString(74, PAGE_H - 157, "macOS Network")
    c.drawString(74, PAGE_H - 194, "Performance & Resilience")
    c.drawString(74, PAGE_H - 231, "Runbook")
    c.setFont("Segoe", 11)
    c.setFillColor(HexColor("#D5E6F3"))
    c.drawString(76, PAGE_H - 264, "M1 Pro failover  •  eero + T-Mobile backup  •  local validation")
    c.drawString(76, PAGE_H - 282, "documentation-backed 2/2, 5/5, and 10/10 stress methods")
    rr(c, 74, 155, 456, 78, 12, HexColor("#163D5C"), HexColor("#2B5978"), 0.8)
    c.setFont("Segoe-Bold", 8.2)
    c.setFillColor(TEAL)
    c.drawString(91, 211, "EVIDENCE BOUNDARY")
    c.setFont("Segoe", 9.0)
    c.setFillColor(WHITE)
    c.drawString(91, 190, "Direct host failover and eero-wide backup: field verified")
    c.drawString(91, 173, "macOS throughput methods at 2/2, 5/5, and 10/10: Amy-untested")
    g.badge("FIELD VERIFIED", 74, 122)
    c.setFont("Segoe-Bold", 7.1)
    c.setFillColor(WHITE)
    c.drawString(188, 119, "M1 PRO FAILOVER")
    g.badge("AMY-UNTESTED", 346, 122)
    c.setFont("Segoe-Bold", 7.1)
    c.setFillColor(WHITE)
    c.drawString(452, 119, "THROUGHPUT METHODS")
    c.setFont("Segoe", 7.2)
    c.setFillColor(MUTED)
    c.drawString(40, 28, f"v{VERSION}  |  {RELEASE_DATE_LONG}  |  Safe defaults, measured changes, explicit rollback")
    c.drawRightString(PAGE_W - 40, 28, f"1 / {g.total_pages}")
    g.next()


def page_2(g: Guide) -> None:
    g.begin("Use the evidence path that matches the question", "Start here", "PROVEN BASELINE",
            "Failover is field evidence. Every macOS throughput target in this edition is a reproducible test method.")
    cards = [
        ("1  BASELINE", TEAL_PALE, [
            p("Capture the Mac, adapter, services, routes, eero state, and counters before changing anything.", size=7.4),
            b("Keep a local console/second path."),
            b("Use one declared objective."),
        ]),
        ("2  FAILOVER", GREEN_PALE, [
            p("Reproduce Amy's host-direct and network-wide T-Mobile recovery as two separate tests.", size=7.4),
            b("Expect sessions to reset."),
            b("Verify failback as well as failover."),
        ]),
        ("3  THROUGHPUT", PURPLE_PALE, [
            p("Treat 2/2, 5/5, and 10/10 as Amy-untested until the exact Mac path clears the local and WAN gates.", size=7.4),
            b("Local server first."),
            b("Three runs and clean counters."),
        ]),
        ("4  OPTIMIZE", AMBER_PALE, [
            p("Change a service, adapter, SQM, or Wi-Fi variable only for a repeatable symptom.", size=7.4),
            b("One change at a time."),
            b("Roll back neutral results."),
        ]),
    ]
    gap = 12
    width = (PAGE_W - 80 - gap * 3) / 4
    for index, (title, fill, blocks) in enumerate(cards):
        g.card(40 + index * (width + gap), 520, width, 216, title, blocks,
               fill=fill, page_tag=f"mac-p2-{index}")
    g.card(40, 288, 435, 151, "Evidence labels", [
        p("PROVEN BASELINE — authoritative behavior and safe defaults.", size=7.45),
        p("FIELD VERIFIED — Amy observed the stated outcome on the named topology.", size=7.45),
        p("CONDITIONAL CHANGE — justified only by a deployment need or symptom.", size=7.45),
        p("CONTROLLED EXPERIMENT / AMY-UNTESTED — measured protocol, not Amy's result.", size=7.45),
    ], fill=WHITE, page_tag="mac-p2-labels")
    g.card(487, 288, 265, 151, "Release integrity", [
        p("Use a PDF from the official tagged release and match it to the same-version Markdown companion.", size=7.55),
        p("Verify the file against outputs/SHA256SUMS.txt before relying on a downloaded copy.", size=7.55),
        p("Modified, unversioned, or checksum-mismatched copies are outside the supported release.", size=7.35),
    ], fill=BLUE_PALE, page_tag="mac-p2-repo")
    g.action_strip([
        ("Start", "Read pages 3–5 before any change.", "info"),
        ("Restart", "None.", "pass"),
        ("Pass", "Claim and evidence label match.", "pass"),
        ("Fail", "A test method is presented as Amy's result.", "fail"),
        ("Rollback", "Return to baseline and relabel.", "warn"),
    ])
    g.next()


def page_3(g: Guide) -> None:
    g.begin("Amy's tested resilience topology", "Field record", "FIELD VERIFIED",
            "Two recovery controls share one T-Mobile Home Backup Internet service and are not carrier-diverse.")
    g.card(40, 520, 352, 327, "Observed topology and outcomes", [
        label("Primary"),
        p("Metronet symmetric 2/2 Gbps → eero gateway/network → M1 Pro MacBook Pro and other clients.", size=7.5),
        label("Direct Mac recovery — successful"),
        p("The tested M1 Pro MacBook Pro was configured to recover directly to the T-Mobile Home Backup Internet Wi-Fi path when its primary Ethernet/eero path was unavailable.", size=7.5),
        label("Whole-network recovery — successful"),
        p("eero Plus Internet Backup was configured to use that same T-Mobile backup Wi-Fi source. A full eero-network switch to it completed successfully.", size=7.5),
        label("What this proves"),
        p("Both control layers worked in the tested conditions. It does not prove a particular recovery time on a future macOS/eero release or under a different cellular signal, allowance, power, or workload.", size=7.35, color=SLATE),
    ], fill=GREEN_PALE, page_tag="mac-p3-record")
    g.card(406, 520, 346, 327, "Boundaries to preserve", [
        b("Both backup modes depend on the same T-Mobile carrier, gateway, power, RF conditions, and usable plan allowance."),
        b("When Ethernet remains linked but the primary WAN fails, eero Internet Backup—not macOS service order—owns network-wide recovery."),
        b("macOS service order is best matched to loss/inactivation of the Ethernet service. It is not a stateful application failover system."),
        b("Existing TCP, VPN, voice, and remote-desktop sessions may reset even when new connections recover."),
        b("A managed work Mac may restrict network services, known Wi-Fi networks, drivers, extensions, VPN behavior, or diagnostics. Obtain the required device-owner authorization before changing them."),
        b("Amy did not field-test macOS iPerf3 at 2/2, 5/5, or 10/10 for this guide. Those sections are documentation-backed methods."),
        p("Do not run multi-gigabit stress traffic through a metered/time-limited cellular backup. Test the minimum workload the backup must carry.", size=7.25, color=RED),
    ], fill=WHITE, page_tag="mac-p3-boundary")
    g.action_strip([
        ("Restart", "None for understanding the topology.", "pass"),
        ("Pass", "Both layers and the shared failure domain are named.", "pass"),
        ("Expected", "Existing sessions may reset.", "warn"),
        ("Fail", "Two controls are called two independent carriers.", "fail"),
        ("Recovery", "Test each layer separately.", "info"),
    ])
    g.next()


def page_4(g: Guide) -> None:
    g.begin("Safety package before any macOS change", "Preparation", "PROVEN BASELINE",
            "Preserve work access, capture the current network location, and avoid weakening Apple silicon startup security.")
    g.card(40, 520, 350, 300, "Prerequisites", [
        check("Use a local account with the required administrator rights and keep a local console/second path."),
        check("If the Mac is managed, confirm the allowed test window and whether Wi-Fi, VPN, filters, system extensions, or network locations are managed."),
        check("Keep the adapter vendor's current Apple-silicon/macOS package and uninstall/rollback instructions offline."),
        check("Record the current network location, service order, Auto-Join states, VPN/content filters, DNS/proxy state, and adapter hardware mode."),
        check("Connect power; stop large sync, backup, and update workloads unless they are the declared workload."),
        check("Name the symptom, test, pass threshold, and rollback before a change."),
        check("Perform failover from a local session; unplugging the active adapter can terminate remote access."),
        p("Do not lower Startup Security or approve a legacy kernel extension merely to make an old NIC work. Select current Apple-silicon support or a DriverKit/class-compliant alternative.", size=7.1, color=RED),
    ], fill=WHITE, page_tag="mac-p4-prereq")
    g.card(404, 520, 348, 300, "Stop conditions", [
        b("The Ethernet service disappears or negotiates below the target."),
        b("Gateway/DNS/work resources do not return after the declared rollback."),
        b("VPN, endpoint security, content filters, certificates, or device management become unhealthy."),
        b("The adapter resets, link flaps, errors grow, a port/module overheats, or one CPU core stays saturated."),
        b("The T-Mobile plan allowance/signal/power is not ready for the backup test."),
        b("A vendor installer requests a restart you cannot safely schedule."),
        {"type": "rule"},
        p("Restore basic connectivity before collecting performance evidence. Never stack a service-order change, driver change, MTU change, and SQM change into one test.", size=7.5),
    ], fill=RED_PALE, stroke=HexColor("#F2B8B5"), page_tag="mac-p4-stop")
    g.action_strip([
        ("Prerequisite", "Authorization, local access, rollback package, power.", "info"),
        ("Restart", "Only when macOS/vendor installer explicitly requires it.", "pass"),
        ("Pass", "One change maps to one repeatable result.", "pass"),
        ("Fail", "Work access or rollback is uncertain.", "fail"),
        ("Rollback", "Undo the last change before more testing.", "warn"),
    ])
    g.next()


def page_5(g: Guide) -> None:
    g.begin("Capture a reusable macOS baseline", "Baseline", "PROVEN BASELINE",
            "Run in Terminal. The commands inspect and save state; they do not change the network.")
    g.card(40, 520, 456, 282, "Create a dated evidence folder", [
        code(
            'stamp=$(date +%Y%m%d-%H%M%S)\n'
            'dir="$HOME/Documents/Network-Baseline-$stamp"\n'
            'mkdir -p "$dir"\n'
            'sw_vers > "$dir/macos-version.txt"\n'
            'system_profiler SPHardwareDataType SPNetworkDataType SPThunderboltDataType \\\n'
            '  > "$dir/system-profile.txt"\n'
            'networksetup -listallhardwareports > "$dir/hardware-ports.txt"\n'
            'networksetup -listnetworkserviceorder > "$dir/service-order.txt"\n'
            'scutil --nwi > "$dir/network-information.txt"\n'
            'route -n get default > "$dir/default-route.txt"\n'
            'ifconfig -a > "$dir/interfaces.txt"\n'
            'netstat -ibdn > "$dir/interface-counters.txt"',
            size=6.1,
            leading=7.7,
        ),
        p("The Wi-Fi and Ethernet interface names can vary. Use hardware-ports.txt rather than assuming en0/en1.", size=7.2, color=SLATE),
    ], fill=WHITE, page_tag="mac-p5-commands")
    g.card(510, 520, 242, 282, "Record beside the files", [
        check("Mac model/chip and macOS build"),
        check("Managed or unmanaged device"),
        check("Adapter make/model/firmware/driver"),
        check("Ethernet service + hardware port"),
        check("Negotiated media and MTU"),
        check("Current network location"),
        check("Service order"),
        check("T-Mobile Auto-Join state"),
        check("eeroOS / SQM / backup state"),
        check("Gateway + public route"),
        check("Endpoint CPU/temperature"),
        check("Counter deltas after each run"),
    ], fill=TEAL_PALE, page_tag="mac-p5-record")
    g.card(40, 222, 712, 115, "Quick live checks before every test set", [
        code(
            'networksetup -listnetworkserviceorder\n'
            'scutil --nwi\n'
            'route -n get default\n'
            'networkQuality -v',
            size=6.6,
        ),
        p("networkQuality is corroboration for responsiveness and capacity to Apple's selected test service; it does not replace a controlled local iPerf3 server.", size=7.05, color=SLATE),
    ], fill=BLUE_PALE, page_tag="mac-p5-live")
    g.action_strip([
        ("Restart", "None.", "pass"),
        ("Pass", "Files identify services, ports, route, and before counters.", "pass"),
        ("Fail", "Interface names or active route remain unknown.", "fail"),
        ("Recovery", "Re-run hardware-port and service-order discovery.", "info"),
        ("Preserve", "Keep baseline with test results.", "warn"),
    ])
    g.next()


def page_6(g: Guide) -> None:
    g.begin("Adapter, update, and hardware defaults", "macOS baseline", "PROVEN BASELINE",
            "Use Automatic hardware configuration and standard MTU unless a supported design requires otherwise.")
    g.card(40, 520, 352, 321, "Safe starting state", [
        s(1, "Open System Settings > Network and select the Ethernet service."),
        s(2, "Open Details > Hardware. Record the MAC address and current values."),
        s(3, "Keep Configure set to Automatically. Keep the normal/standard MTU unless every hop in an isolated design is documented for another value."),
        s(4, "Record adapter/bridge/dock firmware and any vendor app or system extension."),
        s(5, "Install a macOS or adapter update only for security/support or a documented problem. Read the restart requirement before starting."),
        label("External 5/10 GbE"),
        p("Require explicit support for the exact adapter, Apple silicon, and current macOS release. Prefer a class-compliant or current DriverKit implementation. A connector or chipset name is not a support matrix.", size=7.3),
        p("If the vendor requires a legacy kernel extension or Reduced Security, stop and choose a supported alternative unless the device owner explicitly accepts that security tradeoff.", size=7.15, color=RED),
    ], fill=WHITE, page_tag="mac-p6-defaults")
    g.card(406, 520, 346, 321, "Avoid cargo-cult macOS tuning", [
        b("Forcing speed/duplex when both ends support autonegotiation."),
        b("Enabling jumbo MTU on only the Mac or for an Internet test."),
        b("Copying Linux/Windows sysctl or offload recipes into macOS."),
        b("Persisting undocumented TCP buffer/timer changes for a benchmark."),
        b("Disabling VPN, filters, firewall, or endpoint security to make a score look better."),
        b("Installing an old Intel-only package through Rosetta and assuming its driver supports Apple silicon."),
        b("Keeping an adapter/driver because four streams improved while a single flow, latency, thermals, or work access regressed."),
        {"type": "rule"},
        p("Apple delivers built-in network stack fixes with macOS. Third-party Ethernet hardware may add its own app/system extension; use the vendor's supported install and uninstall path.", size=7.35, color=SLATE),
    ], fill=AMBER_PALE, page_tag="mac-p6-avoid")
    g.action_strip([
        ("Restart", "Only if macOS/vendor package says so.", "warn"),
        ("Validate", "Adapter identity, media, MTU, route, gateway, work access.", "info"),
        ("Pass", "Automatic mode and supported driver hold target link.", "pass"),
        ("Fail", "Reduced Security/legacy driver or link regression.", "fail"),
        ("Rollback", "Vendor uninstall/known-good package; Automatic hardware.", "warn"),
    ])
    g.next()


def page_7(g: Guide) -> None:
    g.begin("Put Ethernet before Wi-Fi with service order", "Host path preference", "CONDITIONAL CHANGE",
            "Apple documents service order for active connections; it does not migrate an established session.")
    g.card(40, 520, 365, 314, "Exact supported path", [
        s(1, "Confirm Ethernet and Wi-Fi each work independently and save the current order from page 5."),
        s(2, "Open Apple menu > System Settings > Network."),
        s(3, "Open the Action (…) menu and choose Set Service Order."),
        s(4, "Drag the intended Ethernet service above Wi-Fi. Keep VPN services under their managed design; Apple notes VPN priority is handled separately."),
        s(5, "Select OK. No Mac restart is required."),
        label("Verify"),
        code('networksetup -listnetworkserviceorder\nroute -n get default\nscutil --nwi', size=6.4),
        p("The first active service is attempted before lower services. Confirm both IPv4 and IPv6 behavior, DNS, VPN, and the source interface used by a new connection.", size=7.3),
    ], fill=WHITE, page_tag="mac-p7-steps")
    g.card(419, 520, 333, 314, "Boundary and rollback", [
        label("This control covers"),
        b("Ethernet adapter/cable/port loss that makes the service inactive."),
        b("New connection selection after the lower service becomes active."),
        label("This control does not guarantee"),
        b("WAN health detection while Ethernet remains linked."),
        b("Preservation of existing TCP/VPN/voice sessions."),
        b("Selection among multiple available Wi-Fi SSIDs."),
        b("Carrier diversity when both backup modes use T-Mobile."),
        p("Service order ranks active services; it neither disables nor disconnects Wi-Fi. This guide does not claim a Windows WCM/Group Policy equivalent.", size=7.05, color=SLATE),
        label("Rollback"),
        p("Return to System Settings > Network > Action > Set Service Order and restore the captured order. If a separate Network Location was used, return to the captured location.", size=7.35),
        p("Do not delete services to change preference. An inactive/removed service can defeat automatic recovery.", size=7.25, color=RED),
    ], fill=BLUE_PALE, page_tag="mac-p7-boundary")
    g.action_strip([
        ("Restart", "None.", "pass"),
        ("Pass", "New traffic uses Ethernet while it is active.", "pass"),
        ("Fail", "Wrong route/family, DNS/VPN failure, or Wi-Fi disabled.", "fail"),
        ("Rollback", "Restore captured service order/location.", "warn"),
        ("Next", "Prepare and test the T-Mobile Wi-Fi profile.", "info"),
    ])
    g.next()


def page_8(g: Guide) -> None:
    g.begin("Prepare the direct T-Mobile Wi-Fi fallback", "Host resilience", "FIELD VERIFIED",
            "Keep the backup network known and test current macOS behavior; do not assume SSID selection.")
    g.card(40, 520, 356, 329, "Profile and path preparation", [
        s(1, "Power the T-Mobile Home Backup Internet gateway and confirm signal, plan allowance, Wi-Fi security, and a lightweight Internet test on another device."),
        s(2, "On the Mac, open System Settings > Wi-Fi and join the T-Mobile backup network once."),
        s(3, "Open Wi-Fi > Advanced > Known Networks. Next to the T-Mobile network, confirm Auto-Join is enabled unless device management controls it."),
        s(4, "Record its private-address, Low Data Mode, DNS, proxy, and managed-network state; do not change them merely for speed."),
        s(5, "Reconnect the normal primary path and confirm Ethernet remains first in service order."),
        s(6, "Test the exact failure trigger on page 10. If more than one known Wi-Fi network remains available, verify which SSID macOS actually selects rather than assuming."),
        p("A managed profile may prevent forgetting or changing Auto-Join. iCloud Keychain can synchronize forgotten Wi-Fi networks to other devices; do not use Forget as a casual test step.", size=7.15, color=SLATE),
    ], fill=WHITE, page_tag="mac-p8-prepare")
    g.card(410, 520, 342, 329, "When each layer should recover", [
        label("Primary WAN fails; eero and Ethernet stay linked"),
        p("eero Internet Backup should switch the eero network to T-Mobile. macOS service order may see no local link failure.", size=7.45),
        label("Ethernet/eero path becomes unavailable"),
        p("The Mac's Wi-Fi service can become the lower active service and the known T-Mobile network can provide direct host recovery.", size=7.45),
        label("T-Mobile gateway/carrier/power fails"),
        p("Both backup controls fail together. Restore the primary or use a genuinely independent, authorized path.", size=7.45, color=RED),
        label("Existing applications"),
        p("Treat reconnection as application-specific. VPN and long-lived sessions can reset even when a new browser/DNS connection succeeds.", size=7.45),
        p("Optional experiment: Low Data Mode may reduce background usage on a constrained backup. Capture its original state and A/B the required workload; it is not part of Amy's recorded outcome.", size=7.15, color=PURPLE),
    ], fill=AMBER_PALE, page_tag="mac-p8-roles")
    g.action_strip([
        ("Restart", "None.", "pass"),
        ("Pass", "Profile is known/Auto-Join; Ethernet still preferred.", "pass"),
        ("Fail", "Selection is assumed or management policy is bypassed.", "fail"),
        ("Rollback", "Restore captured Auto-Join/data/location state.", "warn"),
        ("Test", "Run direct and eero-wide triggers separately.", "info"),
    ])
    g.next()


def page_9(g: Guide) -> None:
    g.begin("Reproduce eero-wide Internet Backup", "Field resilience", "FIELD VERIFIED",
            "Use the same T-Mobile backup, but score it as a continuity path—not a multi-gigabit benchmark.")
    g.card(40, 520, 355, 328, "Prerequisites and exact path", [
        check("eero Plus active; eero not in bridge mode."),
        check("T-Mobile gateway powered, in range, and within usable allowance."),
        check("Primary eero WAN, wired LAN, and local gateway healthy."),
        s(1, "In the eero app, open Security & privacy > eero Plus > eero Internet Backup."),
        s(2, "Add or select the T-Mobile Home Backup Internet Wi-Fi source."),
        s(3, "Start lightweight gateway/Internet pings and new-connection checks on the Mac plus at least one other eero client."),
        s(4, "Disconnect only the primary WAN feed from the gateway eero. Keep eero and T-Mobile powered."),
        s(5, "Record detection/recovery, backup status, DNS, local LAN, public reachability, and the minimum work application."),
        s(6, "Restore the primary WAN and verify automatic failback after it is stable."),
        s(7, "Repeat the outage/failback cycle three times; one failed cycle fails validation."),
    ], fill=WHITE, page_tag="mac-p9-steps")
    g.card(409, 520, 343, 328, "Pass, fail, and rollback", [
        label("Pass"),
        b("Mac and second client create new Internet connections through T-Mobile."),
        b("Local LAN remains reachable as designed."),
        b("The required lightweight workload works within the predeclared recovery objective."),
        b("eero automatically returns to the primary WAN."),
        label("Expected"),
        p("Brief downtime and existing-session resets can occur. eero documents that Internet Backup automatically returns when the primary connection is restored.", size=7.2),
        label("Fail"),
        p("Bridge mode, no T-Mobile signal/allowance, shared power loss, DNS failure, or no automatic failback.", size=7.2, color=RED),
        label("Rollback"),
        p("Reconnect the primary WAN. If necessary, disable/remove the backup source in the eero app and restore its captured state.", size=7.2),
    ], fill=GREEN_PALE, page_tag="mac-p9-score")
    g.action_strip([
        ("Restart", "No Mac/eero reboot; keep both gateways powered.", "pass"),
        ("Pass", "New clients recover and fail back.", "pass"),
        ("Expected", "Existing sessions may reset.", "warn"),
        ("Fail", "No DNS/route or T-Mobile unavailable.", "fail"),
        ("Preserve", "Timestamp eero state and client results.", "info"),
    ])
    g.next()


def page_10(g: Guide) -> None:
    g.begin("Reproduce direct Mac failover and failback", "Host resilience", "FIELD VERIFIED",
            "Trigger Ethernet-path loss locally. WAN-only loss belongs to the eero test on page 9.")
    g.card(40, 520, 430, 330, "Controlled direct-host test", [
        s(1, "Confirm Ethernet and T-Mobile Wi-Fi each work alone. Restore Ethernet first and keep Wi-Fi enabled."),
        s(2, "Identify the actual Wi-Fi and Ethernet hardware devices from networksetup -listallhardwareports."),
        s(3, "Start two Terminal windows and a lightweight new-connection check."),
        code(
            'ping -c 600 -i 0.2 <LOCAL-GATEWAY-IP>\n'
            'ping -c 600 -i 0.2 1.1.1.1',
            size=6.55,
        ),
        s(4, "Disconnect the Ethernet cable/adapter. Do not power off the T-Mobile gateway. Record loss, selected Wi-Fi SSID, route, DNS, public IP/path, and recovery time."),
        code(
            'networksetup -getairportnetwork <WIFI-DEVICE>\n'
            'route -n get default\n'
            'scutil --nwi',
            size=6.25,
        ),
        s(5, "Open new DNS, HTTPS, VPN, and required work connections. Record which existing sessions reset."),
        s(6, "Reconnect Ethernet. After link stability, verify new traffic returns to Ethernet and the direct T-Mobile path is no longer selected for ordinary traffic."),
        s(7, "Repeat the outage/failback cycle three times; one failed cycle fails validation."),
    ], fill=WHITE, page_tag="mac-p10-test")
    g.card(484, 520, 268, 330, "Decision gate", [
        label("Pass"),
        p("The Mac selects the intended T-Mobile Wi-Fi path and restores new connections within the objective declared before testing.", size=7.45),
        p("After Ethernet returns, new traffic cleanly prefers it again; DNS/VPN/work resources remain correct.", size=7.45),
        label("Fail"),
        b("Wi-Fi was off or Auto-Join/profile policy blocked recovery."),
        b("A different SSID was selected."),
        b("No default route/DNS or no failback."),
        b("Management/VPN policy breaks the required workload."),
        label("Recovery"),
        p("Reconnect Ethernet first, restore the captured service order/location and Auto-Join states, then retest each interface alone.", size=7.25, color=RED),
    ], fill=BLUE_PALE, page_tag="mac-p10-gate")
    g.action_strip([
        ("Restart", "None; cable removal is the intended outage.", "pass"),
        ("Pass", "New traffic recovers and later returns to Ethernet.", "pass"),
        ("Expected", "Existing TCP/VPN sessions can reset.", "warn"),
        ("Fail", "Wrong SSID/route/DNS or no failback.", "fail"),
        ("Rollback", "Reconnect Ethernet; restore order/profile state.", "warn"),
    ])
    g.next()


def page_11(g: Guide) -> None:
    g.begin("Install and verify the macOS test toolkit", "Throughput testing", "AMY-UNTESTED",
            "Built-in ping/networkQuality plus a trusted iPerf3 build; never expose a listener broadly.")
    g.card(40, 520, 355, 316, "Built-in tools", [
        label("Latency and route"),
        code(
            'ping -c 100 <LOCAL-GATEWAY-IP>\n'
            'ping -c 100 1.1.1.1\n'
            'route -n get default\n'
            'scutil --nwi',
            size=6.45,
        ),
        label("Apple responsiveness/capacity corroboration"),
        code('networkQuality -v\nnetworkQuality -h', size=6.55),
        p("Record the macOS version because available options and the selected Apple test endpoint can change. Responsiveness uses round trips per minute; do not translate it into an invented universal pass threshold.", size=7.25),
        label("Counters"),
        code('netstat -ibdn\nifconfig <ETHERNET-DEVICE>', size=6.45),
        p("Capture before/after deltas on the tested interface rather than interpreting lifetime totals.", size=7.25, color=SLATE),
    ], fill=TEAL_PALE, page_tag="mac-p11-builtins")
    g.card(409, 520, 343, 316, "iPerf3", [
        s(1, "Use an approved package source. If Homebrew is already approved, install with brew install iperf3; otherwise use the ESnet project/source or an organization-managed package."),
        code('iperf3 --version', size=6.65),
        s(2, "Run the server only on a controlled wired endpoint with capacity above the target."),
        code('iperf3 -s -p 5201', size=6.65),
        s(3, "Scope the host firewall/test VLAN to the intended private client. Do not create an Internet port-forward."),
        s(4, "Record the exact iPerf3 version, server, hash/package source, route, and endpoint CPU."),
        p("A public server can be a secondary observation only when its owner permits the load. It is not the default for reproducible 2/2, 5/5, or 10/10 testing.", size=7.25, color=RED),
    ], fill=WHITE, page_tag="mac-p11-iperf")
    g.action_strip([
        ("Prerequisite", "Approved binaries; controlled endpoint; scoped firewall.", "info"),
        ("Restart", "None for tools.", "pass"),
        ("Pass", "Versions run; server is attributable and private.", "pass"),
        ("Fail", "Unknown binary/server or broad listener exposure.", "fail"),
        ("Rollback", "Stop listener and remove scoped rule.", "warn"),
    ])
    g.next()


def page_12(g: Guide) -> None:
    g.begin("Pass the wired local gate first", "Throughput testing", "AMY-UNTESTED",
            "The adapter, Thunderbolt/USB path, switch, server, media, and CPU must clear the target before the ISP is tested.")
    g.card(40, 520, 375, 319, "Local sequence", [
        check("Draw every hop; record adapter, dock/chassis, cable/module, switch port, and negotiated rate."),
        check("Use a wired server whose NIC, PCIe/USB/Thunderbolt path, CPU, and switch port exceed the target."),
        check("Pause VPN/cloud sync/backups unless they are the declared real workload."),
        code(
            'networksetup -getMedia "<ETHERNET-SERVICE>"\n'
            'netstat -ibdn\n'
            'iperf3 -c <LAN-SERVER-IP> -P 1 -t 30 -O 5\n'
            'iperf3 -c <LAN-SERVER-IP> -P 4 -t 30 -O 5\n'
            'iperf3 -c <LAN-SERVER-IP> -R -P 4 -t 30 -O 5',
            size=6.1,
        ),
        s(1, "Run one stream, then four; use eight only while throughput is still rising."),
        s(2, "Repeat the selected stream count three times in both directions."),
        s(3, "Capture counter deltas, interval stability, per-core CPU, and adapter/dock temperature."),
    ], fill=WHITE, page_tag="mac-p12-sequence")
    g.card(429, 520, 323, 319, "Local acceptance gate", [
        label("Pass"),
        b("Median application throughput ≥90% of the slower negotiated link, or a documented platform ceiling."),
        b("No unexplained run <85% of negotiated rate."),
        b("No local error/drop delta, link renegotiation, driver reset, saturated core, or thermal drift."),
        label("Fail — stay local"),
        b("Wrong media: inspect adapter, cable/module, port, autonegotiation, dock/chassis, and driver."),
        b("One direction slow: swap endpoints/ports and inspect receive CPU/driver."),
        b("More streams plateau early: inspect endpoint CPU, bus sharing, server, and switch."),
        p("Do not use a WAN result to excuse a failed local gate.", size=7.35, color=RED),
    ], fill=BLUE_PALE, page_tag="mac-p12-gate")
    g.action_strip([
        ("Restart", "Only if the adapter/driver package explicitly requires it.", "warn"),
        ("Pass", "Three-run local gate with clean counters/thermals.", "pass"),
        ("Fail", "Stay local; do not tune WAN/SQM.", "fail"),
        ("Rollback", "Return last adapter/media/MTU change.", "warn"),
        ("Next", "Proceed to the declared WAN tier.", "info"),
    ])
    g.next()


def page_13(g: Guide) -> None:
    g.begin("macOS 2/2 Gbps validation method", "2/2 Gbps method", "AMY-UNTESTED",
            "This is not Amy's Windows 3.8–3.9 Gbps result; reproduce it on the Mac before making any claim.")
    g.card(40, 520, 355, 318, "Idle and one direction at a time", [
        label("Baseline"),
        code(
            'ping -c 300 -i 0.2 <LOCAL-GATEWAY-IP>\n'
            'ping -c 300 -i 0.2 1.1.1.1\n'
            'networkQuality -v',
            size=6.35,
        ),
        label("Upload / reverse download"),
        code(
            'iperf3 -4 -c <CONTROLLED-SERVER> -P 8 -t 120 -O 10\n'
            'iperf3 -4 -c <CONTROLLED-SERVER> -R -P 8 -t 120 -O 10',
            size=6.2,
        ),
        s(1, "Characterize a new endpoint with 1, then 4, then at most 8 streams; keep the one-stream result."),
        s(2, "Run upload and download separately three times each."),
        s(3, "Use a second controlled endpoint/time if WAN results vary."),
        s(4, "Record route, VPN/Private Relay state, SQM, server, interval output, counters, CPU, and temperature."),
    ], fill=WHITE, page_tag="mac-p13-method")
    g.card(409, 520, 343, 318, "2 Gbps method gate", [
        label("Each direction"),
        p("Median ≥1.8 Gbps; no unexplained run <1.7 Gbps; stable plateau; clean local counter deltas; no saturated endpoint core.", size=7.55),
        label("Interpretation"),
        b("Local pass + one WAN server miss: endpoint/route first."),
        b("Repeatable miss across controlled servers: inspect service provisioning, router, adapter, CPU, and SQM state."),
        b("Gateway flat but Internet latency rises: WAN/upstream/remote queue."),
        b("Gateway and Internet both rise: client/router/local queue."),
        label("Do not claim"),
        p("networkQuality or one browser test alone validates symmetric 2/2. It uses a selected remote service and is corroboration, not path isolation.", size=7.25, color=RED),
    ], fill=PURPLE_PALE, page_tag="mac-p13-gate")
    g.action_strip([
        ("Restart", "None.", "pass"),
        ("Pass", "Both directions independently clear the gate.", "pass"),
        ("Conditional", "Public/remote miss; controlled paths pass.", "warn"),
        ("Fail", "Same bounded deficit across controlled paths.", "fail"),
        ("Next", "Run simultaneous load only after both pass.", "info"),
    ])
    g.next()


def page_14(g: Guide) -> None:
    g.begin("macOS simultaneous 2/2 method", "2/2 Gbps method", "AMY-UNTESTED",
            "Use two sessions and concurrent pings; the Windows field record is context, not a Mac result.")
    g.card(40, 520, 455, 326, "Four-terminal run order", [
        s(1, "Start local-gateway and Internet pings, then wait about 10 seconds."),
        code(
            'ping -c 800 -i 0.2 <LOCAL-GATEWAY-IP>\n'
            'ping -c 800 -i 0.2 1.1.1.1',
            size=6.2,
        ),
        s(2, "Start upload and reverse-download as close together as practical."),
        code(
            '# Terminal A — upload\n'
            'iperf3 -4 -c <UPLOAD-SERVER> -P 8 -t 150 -O 15\n'
            '# Terminal B — reverse download\n'
            'iperf3 -4 -c <DOWNLOAD-SERVER> -R -P 8 -t 150 -O 15',
            size=5.95,
        ),
        s(3, "Record sender/receiver totals, interval stability, retransmissions, ping distributions/loss, route, counter deltas, CPU, and thermals."),
        s(4, "Repeat three times. Add streams only to characterize a non-plateauing endpoint; never to hide a weak single-flow result."),
        p("Separate controlled servers or ports reduce the chance that one remote endpoint/process masks full-duplex capacity.", size=7.2, color=SLATE),
    ], fill=WHITE, page_tag="mac-p14-order")
    g.card(509, 520, 243, 326, "Acceptance", [
        label("Target"),
        p("Upload ≥1.8 Gbps and download ≥1.8 Gbps at the same time; aggregate ≥3.6 Gbps.", size=7.7),
        label("Also required"),
        b("Three repeatable runs."),
        b("Zero local error/drop delta."),
        b("Stable link and endpoint headroom."),
        b("Declared loaded-latency objective."),
        label("Evidence boundary"),
        p("Amy's approximately 3.8–3.9 Gbps aggregate was recorded on Windows/I225-V/eero/Metronet. Until this Mac procedure passes, cite no equivalent Mac result.", size=7.25, color=PURPLE),
    ], fill=GREEN_PALE, page_tag="mac-p14-gate")
    g.action_strip([
        ("Restart", "None.", "pass"),
        ("Pass", "Each ≥1.8; aggregate ≥3.6; counters clean.", "pass"),
        ("Fail", "Repeatable controlled deficit or local errors.", "fail"),
        ("Rollback", "Stop load; restore adapter/SQM baseline.", "warn"),
        ("Record", "Keep all terminals and counter snapshots.", "info"),
    ])
    g.next()


def page_15(g: Guide) -> None:
    g.begin("Loaded latency: networkQuality plus SQM A/B", "Latency under load", "CONTROLLED EXPERIMENT",
            "Use Apple responsiveness as corroboration and gateway/Internet pings to localize the queue.")
    g.card(40, 520, 370, 325, "A/B sequence", [
        s(1, "Record the current eero SQM state. In the eero app: Settings > Advanced networking > under Network services > SQM."),
        s(2, "Run networkQuality -v twice at idle and record upload/download capacity, idle latency, and responsiveness."),
        s(3, "Run idle, download-only, upload-only, and simultaneous iPerf3 loads while pinging the gateway and Internet."),
        s(4, "Toggle SQM. No eero/Mac reboot is normally required; allow the network to settle."),
        s(5, "Repeat the identical servers, commands, order, client power state, and time window three times."),
        s(6, "Compare throughput, gateway and Internet latency/loss, networkQuality responsiveness, counters, and the actual work application."),
        code('networkQuality -v\nping -c 300 -i 0.2 <LOCAL-GATEWAY-IP>', size=6.25),
        p("eero documents that SQM is unavailable in bridge mode and can reduce peak throughput while improving latency-sensitive traffic.", size=7.15, color=SLATE),
    ], fill=PURPLE_PALE, page_tag="mac-p15-sequence")
    g.card(424, 520, 328, 325, "Decision rule", [
        label("Keep SQM when"),
        b("Gateway/Internet loaded latency or Apple responsiveness improves repeatedly."),
        b("The required application improves."),
        b("Throughput stays above its predeclared floor."),
        label("Roll back when"),
        b("The gain is neutral/inconsistent."),
        b("Throughput cost or application regression is unacceptable."),
        label("Interpret"),
        p("Gateway stays low while Internet rises: likely WAN/upstream/remote queue. Both rise: investigate the Mac, adapter, eero, or local queue.", size=7.35),
        p("Do not convert Apple's round trips per minute into an invented universal grade. Compare the same Mac/path/state against itself.", size=7.25, color=RED),
    ], fill=WHITE, page_tag="mac-p15-rule")
    g.action_strip([
        ("Restart", "No reboot; allow eero state to settle.", "pass"),
        ("Pass", "Repeatable responsiveness gain above throughput floor.", "pass"),
        ("Fail", "Neutral, unstable, or harmful result.", "fail"),
        ("Rollback", "Restore the captured SQM state.", "warn"),
        ("Record", "Keep both states and all four workloads.", "info"),
    ])
    g.next()


def page_18(g: Guide) -> None:
    g.begin("Localize the first failing boundary", "Troubleshooting", "PROVEN BASELINE",
            "Service → local adapter/path → controlled WAN → simultaneous load → application.")
    g.card(40, 520, 350, 330, "Signal → next check", [
        p("Ethernet service absent/wrong media — adapter power, cable/module, dock/chassis, port, supported driver, Hardware = Automatic.", size=7.4),
        p("Wrong route after failback — service order, active Network Location, IPv4/IPv6, VPN/filter, and scutil --nwi.", size=7.4),
        p("Local iPerf3 slow — swap endpoint/port/media; inspect single core, bus sharing, server capacity, thermals, and counters.", size=7.4),
        p("Only one WAN server slow — retest a controlled second server/route/time; do not tune the Mac around a shared public endpoint.", size=7.4),
        p("Single direction slow — swap sender/receiver roles; inspect receive path, endpoint CPU, service shaping, and adapter driver.", size=7.4),
        p("Only simultaneous load slow — test eero/router full-duplex NAT/firewall/SQM capacity and endpoint contention.", size=7.4),
        p("Wi-Fi local test slow but wired control clean — use the two Wi-Fi pages; do not call the ISP first.", size=7.4),
    ], fill=WHITE, page_tag="mac-p18-signals")
    g.card(404, 520, 348, 330, "Failure routing", [
        label("Direct Mac failover"),
        p("Wrong/no SSID → Wi-Fi/Auto-Join/managed profile. Right SSID, no Internet → T-Mobile gateway/signal/allowance/DNS. No Ethernet failback → service order/location/link.", size=7.35),
        label("eero-wide failover"),
        p("Bridge mode or backup source absent → eero configuration. Backup selected but no clients online → T-Mobile/DNS. One client only → client/VPN/policy.", size=7.35),
        label("Throughput"),
        p("Local gate fails → stay local. Local passes but all controlled WAN endpoints fail → provisioning/router/ISP evidence package. One public server fails → conditional endpoint/path result.", size=7.35),
        label("Evidence package"),
        p("Timestamps, topology, service order, route, macOS/adapter/eero versions, exact commands, interval output, CPU, counter deltas, ping/networkQuality, failover status, and rollback result.", size=7.25, color=SLATE),
    ], fill=BLUE_PALE, page_tag="mac-p18-routing")
    g.action_strip([
        ("Restart", "Only after a supported package says so.", "warn"),
        ("Pass", "Earliest failed boundary is identified.", "pass"),
        ("Fail", "Multiple variables change before localization.", "fail"),
        ("Rollback", "Undo last change; repeat same boundary.", "warn"),
        ("Escalate", "Send evidence, not one speed screenshot.", "info"),
    ])
    g.next()


def page_19(g: Guide) -> None:
    g.begin("Rollback and acceptance record", "Closeout", "PROVEN BASELINE",
            "Restore basic connectivity first; keep a result only when the before state and recovery are reproducible.")
    g.card(40, 520, 350, 317, "Rollback matrix", [
        p("Service order/location — restore the captured order/location. No reboot. Verify route, DNS, IPv4/IPv6, VPN, and Ethernet preference.", size=7.25),
        p("T-Mobile Auto-Join/data settings — restore captured Wi-Fi values. No reboot. Test the primary and backup independently.", size=7.25),
        p("Ethernet Hardware/MTU — restore Configure = Automatically and standard/prior MTU. Link reset may occur; reboot rarely needed.", size=7.25),
        p("Adapter app/driver/extension — use the vendor's uninstall/known-good package. Restart only when prompted. Never improvise removal of system files.", size=7.25),
        p("SQM — restore captured toggle; allow settling; repeat idle plus one loaded run. No reboot.", size=7.25),
        p("eero Internet Backup — reconnect primary WAN first; restore/remove backup source only if required. Keep gateways powered.", size=7.25),
        p("Emergency order: stop load → reconnect Ethernet/primary WAN → restore order/location/profile → undo last change → restart only if required → verify gateway/DNS/work access.", size=7.2, color=RED),
    ], fill=WHITE, page_tag="mac-p19-rollback")
    g.card(404, 520, 348, 317, "Acceptance record", [
        check("Mac model/chip/build: ______________________________"),
        check("Adapter/driver/media/MTU: __________________________"),
        check("Service order/location: _____________________________"),
        check("Primary + T-Mobile path: ____________________________"),
        check("Direct failover / failback: _________________________"),
        check("eero-wide failover / failback: ______________________"),
        check("Local median / lowest: ______________________________"),
        check("WAN up / down / simultaneous: _______________________"),
        check("Latency/responsiveness/SQM: _________________________"),
        check("Counter/CPU/thermal result: _________________________"),
        check("Outcome: PASS / CONDITIONAL / FAIL / ROLLED BACK"),
        check("Rollback verified: YES / NO / N/A"),
    ], fill=TEAL_PALE, page_tag="mac-p19-record")
    g.action_strip([
        ("Accept", "All declared gates and recovery pass.", "pass"),
        ("Conditional", "Remote/path exception is bounded and recorded.", "warn"),
        ("Reject", "Missing baseline, repeatability, or rollback.", "fail"),
        ("Integrity", "Record the release version and verify its checksum.", "purple"),
        ("Privacy", "Keep raw diagnostics and identifying evidence private.", "info"),
    ])
    g.next()


def appendix_cover(g: Guide) -> None:
    g.page_no += 1
    c = g.c
    g.add_bookmark("Apple-silicon scaling appendix: 5/5 and 10/10 Gbps stress-test method")
    c.setFillColor(PURPLE_PALE)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(PURPLE)
    c.rect(0, 0, 13, PAGE_H, fill=1, stroke=0)
    rr(c, 40, 56, PAGE_W - 80, PAGE_H - 96, 22, NAVY, NAVY)
    c.setFont("Segoe-Bold", 8)
    c.setFillColor(HexColor("#BDA9DC"))
    c.drawString(74, PAGE_H - 107, "SEPARATE APPLE-SILICON SCALING APPENDIX")
    c.setFont("Segoe-Bold", 31)
    c.setFillColor(WHITE)
    c.drawString(74, PAGE_H - 168, "5/5 and 10/10 Gbps")
    c.drawString(74, PAGE_H - 207, "Stress-Test Method")
    c.setFont("Segoe", 11)
    c.setFillColor(HexColor("#D5E6F3"))
    c.drawString(76, PAGE_H - 246, "Documentation-backed and Amy-untested on the M1 Pro MacBook Pro")
    c.drawString(76, PAGE_H - 264, "External adapter, Thunderbolt/USB path, driver, media, and server all become gates")
    rr(c, 74, 164, 628, 98, 12, HexColor("#163D5C"), HexColor("#2B5978"), 0.8)
    c.setFont("Segoe-Bold", 8)
    c.setFillColor(HexColor("#BDA9DC"))
    c.drawString(92, 236, "DO NOT TREAT A 40 GB/S THUNDERBOLT LABEL AS 10 GB/S ETHERNET PROOF")
    c.setFont("Segoe", 9)
    c.setFillColor(WHITE)
    c.drawString(92, 214, "The adapter implementation, driver, shared dock/chassis traffic, switch, router, endpoint CPU,")
    c.drawString(92, 197, "media, thermals, and test server determine sustained full-duplex payload.")
    c.drawString(92, 180, "Intel PCIe cards require an enclosure and explicit current macOS/Apple-silicon support.")
    g.badge("AMY-UNTESTED", 74, 123)
    c.setFont("Segoe-Bold", 7.1)
    c.setFillColor(WHITE)
    c.drawString(178, 120, "DOCUMENTATION-BACKED / CONTROLLED EXPERIMENT")
    c.setFont("Segoe", 7.2)
    c.setFillColor(MUTED)
    c.drawString(40, 28, "Scaling boundary  |  Re-verify adapter, macOS, enclosure, media, and endpoint support")
    c.drawRightString(PAGE_W - 40, 28, f"{g.page_no} / {g.total_pages}")
    g.next()


def page_21(g: Guide) -> None:
    g.begin("Architecture prerequisites for 5 and 10 Gbps", "Scaling appendix", "AMY-UNTESTED",
            "The slowest hop and the busiest shared bus set the result.", appendix=True)
    g.card(40, 520, 352, 330, "Every boundary must clear the target", [
        check("M1 Pro Thunderbolt/USB port and cable expose the adapter's required mode."),
        check("Adapter has explicit Apple-silicon/current-macOS support and negotiates the required Ethernet rate."),
        check("Dock/chassis and other attached devices do not share the tested path into a lower ceiling."),
        check("Router/firewall/NAT/SQM sustains simultaneous aggregate, not only one-way marketing rate."),
        check("Switch ports/fabric and every cable/module support the mode without oversubscription."),
        check("Controlled server NIC, PCIe path, CPU, OS, and storage/workload exceed the target."),
        check("Endpoint per-core CPU and thermals remain below saturation/throttle."),
        check("VPN, content filters, Private Relay, backup, and security inspection state is recorded."),
        check("No errors/drops/link renegotiation before load."),
        check("WAN handoff/provisioning actually supports the declared tier."),
    ], fill=WHITE, page_tag="mac-p21-boundaries")
    g.card(406, 520, 346, 330, "Preflight and stop gates", [
        code(
            'system_profiler SPThunderboltDataType SPNetworkDataType\n'
            'networksetup -getMedia "<ETHERNET-SERVICE>"\n'
            'ifconfig <ETHERNET-DEVICE>\n'
            'netstat -ibdn',
            size=6.2,
        ),
        label("Inspect physically"),
        b("Exact adapter/enclosure/dock model, firmware, power supply, upstream port, and certified host cable."),
        b("Switch/router port combinations, fabric/NAT/SQM throughput, and module/media compatibility."),
        b("Thermal path around copper PHY, SFP+ module, adapter, and enclosure."),
        label("Stop"),
        p("Do not start WAN load if the local server has not cleared the target, any hop negotiates low, counters already grow, one core is saturated, or the adapter/enclosure overheats.", size=7.25, color=RED),
    ], fill=PURPLE_PALE, page_tag="mac-p21-preflight")
    g.action_strip([
        ("Restart", "Only after supported driver/firmware install requires it.", "warn"),
        ("Pass", "Every hop negotiates target with clean idle state.", "pass"),
        ("Fail", "Any endpoint/shared bus is below target.", "fail"),
        ("Rollback", "Known-good adapter/media; Automatic hardware/standard MTU.", "warn"),
        ("Next", "Clear phased local gates.", "purple"),
    ], appendix=True)
    g.next()


def page_22(g: Guide) -> None:
    g.begin("Phased 5/5 and 10/10 gates", "Scaling appendix", "AMY-UNTESTED",
            "Runbook gate: median ≥90%, no unexplained run <85%, three runs, clean counters.", appendix=True)
    g.card(40, 520, 350, 327, "Stream progression", [
        s(1, "Local: 30 seconds after 5-second omit. WAN: 120 seconds after the local gate passes."),
        code(
            'iperf3 -c <SERVER> -P 1 -t 30 -O 5\n'
            'iperf3 -c <SERVER> -P 4 -t 30 -O 5\n'
            'iperf3 -c <SERVER> -P 8 -t 30 -O 5\n'
            'iperf3 -c <SERVER> -R -P 4 -t 30 -O 5',
            size=6.25,
        ),
        s(2, "Stop adding streams when throughput plateaus; preserve every lower-stream result."),
        s(3, "Repeat selected count three times per direction, then two simultaneous sessions."),
        s(4, "Record iPerf3/macOS versions, adapter/media, route, interval stability, retransmissions, counter deltas, per-core CPU, and thermals."),
        p("iPerf3 3.16+ uses a separate thread per stream, but endpoints, drivers, and the path can still bottleneck.", size=7.15, color=SLATE),
    ], fill=WHITE, page_tag="mac-p22-order")
    g.card(404, 520, 348, 327, "Application-throughput method gates", [
        label("5 Gbps path"),
        p("Single direction median ≥4.5 Gbps. Simultaneous: each direction ≥4.5 Gbps; aggregate ≥9.0 Gbps.", size=7.65),
        label("10 Gbps path"),
        p("Single direction median ≥9.0 Gbps. Simultaneous: each direction ≥9.0 Gbps; aggregate ≥18.0 Gbps.", size=7.65),
        label("Also required"),
        b("No unexplained run below 85% of negotiated rate."),
        b("Zero local error/drop delta; stable link."),
        b("No saturated core, shared-bus ceiling, driver reset, or thermal throttle."),
        p("These are editorial runbook gates, not Apple, eero, Intel, or ISP guarantees. Payload is lower than nominal PHY rate because of protocol/implementation overhead.", size=7.2, color=PURPLE),
    ], fill=PURPLE_PALE, page_tag="mac-p22-gates")
    g.action_strip([
        ("Restart", "None for testing.", "pass"),
        ("Pass", "Median ≥90%; all ≥85%; clean counters/CPU/thermals.", "pass"),
        ("Fail", "Same deficit locally or across controlled endpoints.", "fail"),
        ("Rollback", "Stop; restore last adapter/media/MTU change.", "warn"),
        ("Escalate", "More streams characterize; never conceal.", "purple"),
    ], appendix=True)
    g.next()


def page_23(g: Guide) -> None:
    g.begin("M1 Pro adapter and Intel-card reality check", "Scaling appendix", "AMY-UNTESTED",
            "The MacBook Pro has Thunderbolt 4/USB4 ports, not an internal Ethernet PCIe slot.", appendix=True)
    g.card(40, 520, 352, 330, "External Apple-silicon path", [
        label("Documented host capability"),
        p("Apple lists three Thunderbolt 4 (USB-C) ports supporting Thunderbolt 4 and USB4 up to 40 Gb/s on both 2021 M1 Pro MacBook Pro sizes. Confirm the exact model identifier in the baseline.", size=7.45),
        label("What to require from an adapter"),
        b("Explicit exact-model support for Apple silicon and the installed macOS release."),
        b("Documented 2.5/5/10 GbE link modes and full-duplex sustained performance."),
        b("Current firmware/DriverKit or class-compliant support; supported uninstall/rollback."),
        b("Dedicated host cable/port and adequate adapter/enclosure power/cooling."),
        b("RJ45/SFP+ media compatibility with the switch and intended length."),
        p("Thunderbolt's headline signaling rate is not payload proof. Displays, storage, docks, and other devices can share resources or add thermal/power constraints.", size=7.25, color=SLATE),
    ], fill=WHITE, page_tag="mac-p23-external")
    g.card(406, 520, 346, 330, "Intel PCIe cards and motherboards", [
        label("Do not transplant the Windows recommendation"),
        p("Intel X710-T2L, X550-T2, and X710-DA2 are useful Windows/PCIe selection references in the companion guides. They are not automatic M1 Pro recommendations.", size=7.4),
        b("A PCIe card requires a Thunderbolt PCIe enclosure with enough lanes, power, cooling, cable bandwidth, and explicit card compatibility."),
        b("The exact NIC still needs a current Apple-silicon/macOS driver. Intel's Windows/Linux support matrix does not establish macOS support."),
        b("Do not rely on Boot Camp drivers, abandoned kernel extensions, or Reduced Security to make an unsupported card work."),
        b("A “10 Gb capable motherboard” checklist belongs to a Windows/desktop path; the M1 Pro MacBook Pro motherboard has no user PCIe slot or built-in Ethernet port."),
        label("Pass"),
        p("Adapter + enclosure/dock + host cable + macOS driver + media + switch are documented together and clear the local gate.", size=7.25, color=GREEN),
    ], fill=PURPLE_PALE, page_tag="mac-p23-intel")
    g.action_strip([
        ("Restart", "Only if supported adapter package requests it.", "warn"),
        ("Pass", "Exact end-to-end Apple-silicon combination is supported.", "pass"),
        ("Fail", "Support inferred from connector/chipset/headline rate.", "fail"),
        ("Rollback", "Remove per vendor; restore known-good adapter.", "warn"),
        ("Avoid", "Reduced Security for an obsolete NIC.", "fail"),
    ], appendix=True)
    g.next()


def page_24(g: Guide) -> None:
    g.begin("Media, thermals, and a sustained-load gate", "Scaling appendix", "AMY-UNTESTED",
            "Choose one supported media system end to end and prove it holds rate.", appendix=True)
    g.card(40, 520, 350, 329, "RJ45 / copper", [
        b("For a new 10GBASE-T run, Cat6A is the conservative 100 m choice; follow the exact adapter/switch cable matrix."),
        b("Use certified patch cords/terminations; avoid damaged, flat, sharply bent, or unknown-category cable."),
        b("Verify both ends advertise and negotiate the intended 2.5/5/10G mode."),
        b("10GBASE-T PHYs and small adapters run warm; provide airflow and monitor link changes under full-duplex load."),
        label("SFP+ / DAC / fiber"),
        b("Verify adapter/enclosure, switch, module/DAC, firmware, and vendor compatibility together."),
        b("Match passive/active DAC type and length, or fiber type/wavelength/connector/reach."),
        b("Treat SFP+ RJ45 modules as separate high-heat compatibility cases."),
        label("Baseline"),
        p("Automatic hardware configuration, standard MTU, supported driver defaults.", size=7.25),
    ], fill=WHITE, page_tag="mac-p24-media")
    g.card(404, 520, 348, 329, "Ten-minute full-duplex soak", [
        s(1, "Clear the three-run local gate first."),
        s(2, "Capture starting counters, media, adapter/enclosure temperature, CPU, and power state."),
        s(3, "Run two simultaneous local iPerf3 directions for 10 minutes after a 15-second omit."),
        code(
            'iperf3 -c <SERVER-A> -P 4 -t 600 -O 15\n'
            'iperf3 -c <SERVER-B> -R -P 4 -t 600 -O 15',
            size=6.2,
        ),
        s(4, "Compare the final complete 60 seconds with the first complete post-omit 60 seconds."),
        label("Pass"),
        p("Final mean is no more than 5% below the initial mean; link remains at target; errors/drops remain zero; no reset, throttle, saturated core, or unsafe temperature.", size=7.25),
        label("Fail / rollback"),
        p("Stop load; restore known-good media/adapter/MTU; cool hardware; retest one component at a time.", size=7.2, color=RED),
    ], fill=PURPLE_PALE, page_tag="mac-p24-soak")
    g.action_strip([
        ("Restart", "Link/module reset first; reboot only for package need.", "warn"),
        ("Pass", "Rate, link, counters, CPU, and thermals hold.", "pass"),
        ("Fail", "Drift >5%, renegotiation, errors, reset, or heat.", "fail"),
        ("Rollback", "Known-good media/adapter; standard MTU.", "warn"),
        ("Record", "Exact port/cable/module/firmware combination.", "purple"),
    ], appendix=True)
    g.next()


CORE_REFS = [
    ("Apple — Change network service order", "https://support.apple.com/guide/mac-help/change-order-network-services-mac-mchlp2711/mac"),
    ("Apple — Manage network locations", "https://support.apple.com/guide/mac-help/manage-network-locations-on-mac-mchlp1175/mac"),
    ("Apple — Wi-Fi Auto-Join / forget behavior", "https://support.apple.com/en-us/102480"),
    ("Apple — Ethernet settings", "https://support.apple.com/guide/mac-help/ethernet-settings-on-mac-mh11939/mac"),
    ("Apple — Change network hardware settings", "https://support.apple.com/guide/mac-help/change-hardware-settings-mac-mchlp2505/mac"),
    ("Apple — Wireless Diagnostics", "https://support.apple.com/guide/mac-help/use-wireless-diagnostics-mchlf4de377f/mac"),
    ("Apple Developer — networkQuality and responsiveness", "https://developer.apple.com/videos/play/wwdc2021/10239/"),
    ("Apple — System extension alert / legacy kext boundary", "https://support.apple.com/en-us/120363"),
    ("ESnet — Invoking iPerf3", "https://software.es.net/iperf/invoking.html"),
    ("Homebrew — iPerf3 formula", "https://formulae.brew.sh/formula/iperf3"),
    ("eero — Internet Backup", "https://support.eero.com/hc/en-us/articles/8947860842523-What-is-eero-Internet-Backup"),
    ("eero — Smart Queue Management", "https://eero.com/support/articles/360000709886-What-is-Smart-Queue-Management-SQM"),
    ("eero — Wifi Radio Analytics", "https://support.eero.com/hc/en-us/articles/15282384606107-Wifi-Radio-Analytics"),
    ("eero — Coverage scan", "https://support.eero.com/hc/en-us/articles/34604365204635-What-is-Coverage-scan"),
    ("eero — How network optimization works", "https://support.eero.com/hc/en-us/articles/360057257311-How-Does-eero-Optimize-My-Network"),
    ("eero — Client Steering and DFS", "https://support.eero.com/hc/en-us/articles/207613326-What-advanced-features-does-eero-support"),
    ("eero — Ethernet backhaul", "https://support.eero.com/hc/en-us/articles/207852743-Can-I-connect-my-eeros-with-Ethernet"),
    ("T-Mobile — Home Internet Backup", "https://www.t-mobile.com/home-internet/plans/5g-backup-internet-options"),
]

SCALE_REFS = [
    ("Apple — MacBook Pro 14-inch 2021 specifications", "https://support.apple.com/en-us/111902"),
    ("Apple — MacBook Pro 16-inch 2021 specifications", "https://support.apple.com/en-us/111901"),
    ("Apple Developer — NetworkingDriverKit", "https://developer.apple.com/documentation/networkingdriverkit"),
    ("Apple Developer — System Extensions and DriverKit", "https://developer.apple.com/system-extensions/"),
    ("ESnet — Network performance expectations", "https://fasterdata.es.net/performance-testing/troubleshooting/network-performance-expectations/"),
    ("ESnet — Test host tuning", "https://fasterdata.es.net/host-tuning/linux/test-measurement-host-tuning/"),
    ("Intel — X710-T2L specifications", "https://www.intel.com/content/www/us/en/products/sku/189463/intel-ethernet-network-adapter-x710t2l/specifications.html"),
    ("Intel — Retail Ethernet adapter OS matrix", "https://www.intel.com/content/www/us/en/support/articles/000025890/ethernet-products.html"),
    ("Intel — X550-T2 specifications", "https://www.intel.com/content/www/us/en/products/sku/88209/intel-ethernet-converged-network-adapter-x550t2/specifications.html"),
    ("Intel — X710-DA2 specifications", "https://www.intel.com/content/www/us/en/products/sku/83964/intel-ethernet-converged-network-adapter-x710da2/specifications.html"),
    ("Cisco — 10GBASE SFP+ modules", "https://www.cisco.com/c/en/us/products/collateral/interfaces-modules/transceiver-modules/data_sheet_c78-455693.html"),
]


def draw_columns(g: Guide, refs: list[tuple[str, str]], appendix: bool) -> None:
    c = g.c
    accent = PURPLE if appendix else TEAL_DARK
    midpoint = math.ceil(len(refs) / 2)
    for items, x, offset in ((refs[:midpoint], 40, 0), (refs[midpoint:], 404, midpoint)):
        y = 526
        for local_index, (title, url) in enumerate(items, 1):
            rr(c, x, y - 38, 348, 34, 6, WHITE, LINE, 0.55)
            c.setFont("Segoe-Bold", 6.3)
            c.setFillColor(accent)
            c.drawString(x + 9, y - 15, f"{offset + local_index:02d}")
            c.setFont("Segoe-Bold", 6.55)
            c.setFillColor(NAVY)
            for line_index, line in enumerate(wrap(title, 298, "Segoe-Bold", 6.55)[:2]):
                c.drawString(x + 32, y - 14 - line_index * 7.2, line)
            shown = url.replace("https://", "")
            if len(shown) > 79:
                shown = shown[:76] + "…"
            c.setFont("Segoe", 4.75)
            c.setFillColor(BLUE)
            c.drawString(x + 32, y - 31, shown)
            c.linkURL(url, (x + 30, y - 34, x + 339, y - 4), relative=0)
            y -= 42


def page_25(g: Guide) -> None:
    g.begin("Authoritative references — macOS and core method", "References", "PROVEN BASELINE",
            "Reviewed 30 July 2026. Re-check current macOS UI, managed-device policy, and vendor support.")
    draw_columns(g, CORE_REFS, appendix=False)
    rr(g.c, 40, 43, 712, 46, 7, NAVY, NAVY)
    g.c.setFont("Segoe-Bold", 7.0)
    g.c.setFillColor(TEAL)
    g.c.drawString(52, 71, "SOURCE-USE BOUNDARY")
    g.c.setFont("Segoe", 6.9)
    g.c.setFillColor(WHITE)
    g.c.drawString(52, 56, "Apple/eero define behavior; Amy's field record and explicitly labeled runbook gates retain their separate evidence status.")
    g.next()


def page_26(g: Guide) -> None:
    g.begin("Authoritative references — scaling and hardware", "References", "AMY-UNTESTED",
            "Hardware examples are compatibility checkpoints, not purchase endorsements.", appendix=True)
    draw_columns(g, SCALE_REFS, appendix=True)
    rr(g.c, 40, 43, 712, 46, 7, NAVY, NAVY)
    g.c.setFont("Segoe-Bold", 7.0)
    g.c.setFillColor(HexColor("#BDA9DC"))
    g.c.drawString(52, 71, "PUBLICATION CHECKPOINT")
    g.c.setFont("Segoe", 7.0)
    g.c.setFillColor(WHITE)
    g.c.drawString(52, 56, "Verify this PDF against outputs/SHA256SUMS.txt and use the same-version accessible Markdown companion.")
    g.next()


def build() -> Path:
    register_fonts()
    title = "macOS Network Performance & Resilience Runbook"
    g = Guide(
        OUTPUT,
        edition="macOS",
        title=title,
        footer_title=title,
        subject=(
            "Implementation-first Apple-silicon network baseline, T-Mobile/eero failover, "
            "Wi-Fi analysis, and documentation-backed multi-gigabit validation"
        ),
        keywords=(
            "macOS, Apple silicon, M1 Pro, Ethernet, iPerf3, networkQuality, "
            "2 Gbps, 5 Gbps, 10 Gbps, eero, T-Mobile, failover"
        ),
        total_pages=TOTAL_PAGES,
    )
    cover(g)
    page_2(g)
    page_3(g)
    page_4(g)
    page_5(g)
    page_6(g)
    page_7(g)
    page_8(g)
    page_9(g)
    page_10(g)
    page_11(g)
    page_12(g)
    page_13(g)
    page_14(g)
    page_15(g)
    page_wifi_evidence(g)
    page_wifi_protocol(g)
    page_18(g)
    page_19(g)
    appendix_cover(g)
    page_21(g)
    page_22(g)
    page_23(g)
    page_24(g)
    page_25(g)
    page_26(g)
    g.finish()
    return OUTPUT


if __name__ == "__main__":
    print(build())
