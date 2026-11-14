# IMSI Catchers: Government, Enterprise and Adversary Platforms

**Reference, Field Guide, Build Manual and Technical Annexes**

Scope: GSM through 5G SA

---

> **Structure.** This document consolidates five previously separate volumes into one numbered whole. Parts I–V correspond to the original volumes in order. Section numbering is continuous and stable; every cross-reference has been renumbered to match. Each part opens with its own subsection index.
>
> **Link caveat.** Vendor storefronts move, merge and go end-of-life. Where a product has moved to a parent company that is noted inline. Prices are indicative bands, not quotes. Every commercial catcher is quote-only. Links in Parts III and V were compiled without web search and are marked where drift is likely — verify before relying on any of them in a procurement document.
>
> **Reading order.** Part I is the reference and defensive guide. Parts II–V are the build and engineering annexes. Part IV §49 is a complete one-day bootstrap; read Part IV §35 first if you intend to key a transmitter anywhere public.

---

## Table of Contents

**Front matter**

- [Structure and Caveats](#imsi-catcher-platforms--combined-edition)
- [Document Map](#document-map)

**Part I — Reference and Field Guide**

- [Part I index](#part-i--reference-and-field-guide)
1. [Executive Summary](#1-executive-summary)
2. [How IMSI Catchers Operate](#2-how-imsi-catchers-operate)
3. [Exhaustive Feature and Capability Catalogue](#3-exhaustive-feature-and-capability-catalogue)
4. [Vulnerable and Affected Devices](#4-vulnerable-and-affected-devices)
5. [Known Limitations and Constraints](#5-known-limitations-and-constraints)
6. [Common Myths and Misconceptions](#6-common-myths-and-misconceptions)
7. [Enterprise Defensive Field Guide](#7-enterprise-defensive-field-guide)
8. [4G and 5G Security Comparison](#8-4g-and-5g-security-comparison)
9. [Android Hardening Guide](#9-android-hardening-guide)
10. [iPhone Hardening Guide](#10-iphone-hardening-guide)
11. [Risk-Scoring Worksheet Template](#11-risk-scoring-worksheet-template)
12. [Anomaly Log Sheets](#12-anomaly-log-sheets)
13. [Privacy Travel Checklist](#13-privacy-travel-checklist)
14. [Glossary and Appendix](#14-glossary-and-appendix)
15. [References and Citations](#15-references-and-citations)

**Part II — Hardware, Software and Build Guides**

- [Part II index](#part-ii--hardware-software-and-build-guides)
16. [How to Use This Volume](#16-how-to-use-this-volume)
17. [Shared Hardware Substrate](#17-shared-hardware-substrate)
18. [Hardware by Category](#18-hardware-by-category)
19. [Software by Category](#19-software-by-category)
20. [Repositories With Working Code](#20-repositories-with-working-code)
21. [Build Guide B — Bad Actor and DIY](#21-build-guide-b--bad-actor-and-diy)
22. [Build Guide E — Enterprise Passive Monitoring](#22-build-guide-e--enterprise-passive-monitoring)
23. [Build Guide G — Government and Nation State](#23-build-guide-g--government-and-nation-state)
24. [Capability and Budget Ladder](#24-capability-and-budget-ladder)
25. [Failure Modes and Calibration](#25-failure-modes-and-calibration)
26. [References](#26-references)

**Part III — Site Survey, Core Handoff, Evidence Chain and Signalling Control**

- [Part III index](#part-iii--site-survey-core-handoff-evidence-chain-and-signalling-control)
27. [Scope and the Gap Being Addressed](#27-scope-and-the-gap-being-addressed)
28. [Site Survey, Comprehensively](#28-site-survey-comprehensively)
29. [Handing a Session to a Real Core](#29-handing-a-session-to-a-real-core)
30. [CDR Generation and the Evidence Chain](#30-cdr-generation-and-the-evidence-chain)
31. [Signalling Parameters That Force Downgrade or Plaintext](#31-signalling-parameters-that-force-downgrade-or-plaintext)
32. [Gap Analysis: Commercial, FOSS, Internal](#32-gap-analysis-commercial-foss-internal)
33. [Internal Build Order](#33-internal-build-order)
34. [References](#34-references)

**Part IV — Build Specification, With Numbers**

- [Part IV index](#part-iv--build-specification-with-numbers)
35. [RF Exposure and Exclusion Zones](#35-rf-exposure-and-exclusion-zones)
36. [TX/RX Isolation and Desense](#36-txrx-isolation-and-desense)
37. [Power Architecture](#37-power-architecture)
38. [Thermal Design](#38-thermal-design)
39. [GNSS and Timing Integrity](#39-gnss-and-timing-integrity)
40. [Calibration and Measurement](#40-calibration-and-measurement)
41. [Host Hardening and Watchdog](#41-host-hardening-and-watchdog)
42. [Rig Security](#42-rig-security)
43. [Configuration Management and Version Pinning](#43-configuration-management-and-version-pinning)
44. [Acceptance Testing](#44-acceptance-testing)
45. [Ground Truth](#45-ground-truth)
46. [UE Fleet and SIM Tooling](#46-ue-fleet-and-sim-tooling)
47. [Documentation Deliverables](#47-documentation-deliverables)
48. [Licensing Checklist](#48-licensing-checklist)
49. [The One-Day Bootstrap Build](#49-the-one-day-bootstrap-build)

**Part V — 4G/5G Observation Platform: Full Build Guide**

- [Part V index](#part-v--4g5g-observation-platform-full-build-guide)
50. [Design Goals and Non-Goals](#50-design-goals-and-non-goals)
51. [Architecture](#51-architecture)
52. [Hardware Selection](#52-hardware-selection)
53. [Software Base Selection](#53-software-base-selection)
54. [Base Build](#54-base-build)
55. [Radio Configuration](#55-radio-configuration)
56. [Stealth Layer](#56-stealth-layer)
57. [Decoding Pipeline](#57-decoding-pipeline)
58. [Data Model and Storage](#58-data-model-and-storage)
59. [API and GUI](#59-api-and-gui)
60. [Telemetry and Charts](#60-telemetry-and-charts)
61. [Carrier Profile System](#61-carrier-profile-system)
62. [Update and Plugin System](#62-update-and-plugin-system)
63. [Deployment Form Factors](#63-deployment-form-factors)
64. [Test and Validation](#64-test-and-validation)
65. [Cost Summary](#65-cost-summary)
66. [Honest Limits](#66-honest-limits)

**Back matter**

- [Consolidated references index](#consolidated-references-index)

---

## Document Map

| Part | Title | Function | Original volume |
|---|---|---|---|
| **I** | Reference and Field Guide | Threat model, capability catalogue, hardening, logging, checklists | *IMSI Catchers: Government, Enterprise and Adversary Platforms* v1.1 |
| **II** | Hardware, Software and Build Guides | Component pools, vendor landscape, three build guides by actor tier | *Volume II — Hardware, Software and Build Guides* |
| **III** | Survey, Handoff, Evidence, Signalling | Site survey method, core handoff architecture, chain of custody, signalling levers | *Volume III* |
| **IV** | Build Specification, With Numbers | Exposure, isolation, power, thermal, timing, hardening, acceptance | *Volume IV* |
| **V** | 4G/5G Observation Platform | Full platform build: hardware, software, stealth, decode, UI | *Volume V* |

**Which part do you need?**

| If you are… | Start at |
|---|---|
| A defender, traveller or security lead | Part I |
| Buying hardware or building a first rig | Part II §16, then §24 |
| Running a deployment that must survive an evidential test | Part III §27–§30, then Part IV |
| Building the 4G/5G platform | Part V, with Part IV §35–§41 first |
| Answering "how much does this cost" | §24, then §65 |

---

*Page 1 of 14. Next page: Part I §1–§2.*

---
---

# Part I — Reference and Field Guide

**A technical reference, defensive field guide and assessment toolkit**

Part version 1.1 · Compiled 2026-11-13 · Scope: GSM through 5G SA

**Part I index**

1. [Executive Summary](#1-executive-summary)
2. [How IMSI Catchers Operate](#2-how-imsi-catchers-operate)
3. [Exhaustive Feature and Capability Catalogue](#3-exhaustive-feature-and-capability-catalogue)
4. [Vulnerable and Affected Devices](#4-vulnerable-and-affected-devices)
5. [Known Limitations and Constraints](#5-known-limitations-and-constraints)
6. [Common Myths and Misconceptions](#6-common-myths-and-misconceptions)
7. [Enterprise Defensive Field Guide](#7-enterprise-defensive-field-guide)
8. [4G and 5G Security Comparison](#8-4g-and-5g-security-comparison)
9. [Android Hardening Guide](#9-android-hardening-guide)
10. [iPhone Hardening Guide](#10-iphone-hardening-guide)
11. [Risk-Scoring Worksheet Template](#11-risk-scoring-worksheet-template)
12. [Anomaly Log Sheets](#12-anomaly-log-sheets)
13. [Privacy Travel Checklist](#13-privacy-travel-checklist)
14. [Glossary and Appendix](#14-glossary-and-appendix)
15. [References and Citations](#15-references-and-citations)

---

## 1. Executive Summary

An IMSI catcher is a radio device that impersonates a mobile network base station in order to learn the permanent identities of nearby handsets, and in some configurations to intercept their traffic. The core weakness it exploits is architectural and decades old: in GSM, the network authenticates the subscriber but the subscriber never authenticates the network. That asymmetry means any transmitter speaking GSM convincingly enough can make a phone surrender its IMSI, IMEI and location, and can then carry its traffic in a cipher it already knows how to break.

Three things have changed the picture since 2020, and they cut in opposite directions.

First, capability has commoditised. What was a six-figure law-enforcement appliance in 2010 is now a software-defined radio stack, an open-source core and a laptop, for roughly the price of a mid-range phone. The barrier to a competent adversary is now skill, not capital.

Second, 5G introduced the Subscription Concealed Identifier (SUCI), which encrypts the permanent identity on the air interface. Where 5G Standalone is properly deployed with a real ECIES home-network key, passive identity harvesting largely stops working. This is genuine, structural progress.

Third, that progress is easily undone. SUCI is optional in configuration. Operators may run the null scheme, sending the SUPI in plaintext. Devices can be bidded down to LTE, 3G or 2G, none of which understand SUCI. Published work has demonstrated SUCI-catcher attacks that recover identity from the concealed value itself, and measurement studies have found the concealment simply not deployed on many live networks.

The practical conclusion for a defender is uncomfortable but clear. **You cannot make a phone immune. You can raise the cost, shrink the exposure window, and make the residue detectable.** Everything in the hardening sections is in service of those three things. 2G suppression removes the largest attack surface. Lockdown Mode on iOS and Advanced Protection on Android do it for you. Manual carrier selection and disciplined radio hygiene close the rest. Detection is heuristic and should be treated as corroboration, never proof.

For an enterprise, the deliverable is not a product. It is a baseline, a travel tier system, a set of SOC rules and an incident process that survives contact with a real event.

---

## 2. How IMSI Catchers Operate

### 2.1 The fundamental asymmetry

GSM (3GPP TS 43.020) authenticates the subscriber to the network using a challenge derived from the SIM's Ki. The handset is never given anything that proves the base station is genuine. A phone that hears a stronger, plausibly configured cell will attach to it and, in the process, disclose identity.

Later generations add network authentication — mutual authentication in UMTS and LTE, 5G-AKA in NR — but the identity disclosure problem survives in modified form, because the network must still resolve who the handset is before it can authenticate anyone.

### 2.2 Passive versus active

| Mode | Transmits? | Detectable by handset? | Typical use |
|---|---|---|---|
| **Passive monitor** | No | No | Baseline collection, calibration, corroboration |
| **Active catcher** | Yes | Yes, indirectly | Identity harvesting, interception, denial |
| **Hybrid** | Selectively | Partly | Silent harvesting with periodic active bursts |

Passive devices (Rohde & Schwarz TSMA/TSME class) are receive-only scanners. They see what the real network already broadcasts and what handsets emit, and they are essentially invisible. Active devices are the classic "Stingray" and are what most of this document addresses.

### 2.3 The GSM attach hijack, step by step

```mermaid
sequenceDiagram
    autonumber
    participant P as Phone
    participant C as Catcher
    participant N as Real Network
    N-->>P: Broadcast BCCH, real LAC/CID, strong
    C->>C: Power up, pick unused LAC or clone neighbour, transmit louder
    P->>P: Cell reselection, new cell looks better
    P->>C: Location Update Request with TMSI (if known) or IMSI
    C-->>P: Identity Request (IMSI) if TMSI unknown
    P->>C: IMSI in plaintext
    C-->>P: Authentication Request (or accept, or A5/0)
    P->>C: Cipher mode complete
    Note over P,C: Now attached to the catcher,<br/>real network sees an implicit detach
```

The critical steps are 3 through 7. Step 4 is where identity leaks. Step 7 is where the catcher chooses a cipher — frequently A5/0 (none) or A5/1, both of which it can handle.

### 2.4 Why the phone moves

A handset reselects when a candidate cell outranks the serving cell on the C1/C2 (GSM) or S-criteria (LTE/NR) ranking. Catchers manipulate this by transmitting at higher power, advertising a different Location Area Code so a Location Update is forced, and cloning a legitimate neighbour's parameters so the transition looks routine. Some implementations hold the handset by repeatedly forcing updates rather than letting it drift back.

### 2.5 Identity acquisition techniques

| Technique | Mechanism | Counter |
|---|---|---|
| **Forced Location Update** | New LAC triggers update, IMSI disclosed | GUTI reuse, 5G SUCI |
| **Identity Request** | Direct IMSI/SUPI solicitation post-attach | None at 2G/3G/4G |
| **TMSI paging sweep** | Page all TMSIs, note who answers | Nothing practical |
| **Silent SMS (Type 0)** | Message with no user alert, delivery report confirms presence | None; monitor billing |
| **IMEI/IMEISV request** | Device fingerprint alongside identity | None |
| **KARMA-style response** | Answer any probe as if known | Manual network selection |
| **Downgrade forcing** | Advertise only 2G, or reject 4G attach | 2G suppression, Lockdown Mode |
| **Null-cipher forcing** | Negotiate A5/0 or LTE EEA0 | Android 14+ null-cipher block |

### 2.6 Interception

Full interception is a 2G phenomenon. Once a handset is camped on a catcher with A5/0 or A5/1, voice and SMS are recoverable. A5/1 falls to precomputed rainbow tables in minutes; A5/2 is broken outright.

On LTE and 5G, a catcher generally gets metadata and identity, not plaintext, because it cannot complete mutual authentication convincingly without either relaying to the real network or accepting that the handset will notice. Where the catcher does hold a session, it can still observe which services are used, when, and how much.

### 2.7 The 5G twist

5G Standalone conceals the SUPI as a SUCI, ECIES-encrypted to the home network's public key. A catcher cannot read it. It therefore has three options: rely on null-scheme misconfiguration, mount a SUCI-catcher attack that correlates a captured SUCI against a known subscriber through repeated AKA, or bid the device down to a generation that does not conceal anything. All three are documented and field-demonstrated.

---

## 3. Exhaustive Feature and Capability Catalogue

Organised by tier of actor. Real deployments mix tiers; a nation-state suite may include commodity components.

### 3.1 Radio and physical layer

| Capability | Notes |
|---|---|
| Multi-RAT transmit | GSM, UMTS, LTE, NR NSA/SA in one unit |
| Band coverage | 700 MHz through 3.5 GHz; low band gives range, mid band gives capacity |
| Software-defined radio core | USRP, LimeSDR, proprietary; retunable |
| Transmit power | 100 mW handheld to 20–50 W vehicle, plus amplifier |
| Antenna options | Omni, sectoral, directional, MIMO |
| GPS/GNSS disciplined clock | Required for timing alignment on LTE/NR |
| Channel and PCI/ARFCN control | Manual or automatic |
| Duplex modes | TDD and FDD |
| Simultaneous real-network monitoring | Second radio for relay and comparison |

### 3.2 Identity and collection

| Capability | Tier |
|---|---|
| IMSI capture | All |
| IMEI / IMEISV capture | All |
| TMSI / GUTI capture | All |
| SUPI / SUCI capture | Government and above |
| MSISDN correlation via HLR/SS7 lookup | Government, enterprise |
| Silent SMS confirmation | Government, enterprise |
| Bulk passive collection with no transmit | Government |
| Per-IMSI targeting lists (allow/deny) | Enterprise and above |
| "Camp on demand" for a named subscriber | Government |
| Long-dwell presence tracking | Government |
| Handover-graph construction | Nation state |
| Cell-ID-to-geography mapping | All |

### 3.3 Interception and service manipulation

| Capability | Tier |
|---|---|
| 2G voice intercept | Government and above |
| 2G SMS intercept | Government and above |
| Metadata and CDR generation | All |
| Forced downgrade to 2G | All |
| Forced downgrade to LTE from NR | Government |
| Null-cipher negotiation | All |
| Denial of service / jamming adjunct | Government |
| Deny-attach to selected IMSIs | Enterprise and above |
| Call/SMS redirection to attacker media | Government |
| VoLTE relay or break-out | Advanced government |
| 5G SUCI capture with null-scheme fallback | Nation state |
| SUCI-cracker correlation | Nation state, research |
| Baseband exploit delivery | Nation state |
| Rogue Wi-Fi interworking (ePDG) | Nation state |

### 3.4 Deployment form factors

| Form | Typical operator |
|---|---|
| Handheld / briefcase | Field surveillance, entry teams |
| Manpack | Dismounted military |
| Vehicle covert (mag-mount) | Mobile tracking |
| Aircraft ("dirtbox") | Nation state, wide-area |
| Fixed indoor | Embassy, office, conference centre |
| Maritime | Coastal, port |
| Drone | Short dwell, high angle |
| Deployable mast | Event security |
| Permanently installed | Critical infrastructure, border |

### 3.5 Management and integration

| Capability | Notes |
|---|---|
| Local GUI on ruggedised laptop | Baseline |
| Remote/cloud C2 | Enterprise and above |
| Multi-unit mesh coordination | Nation state |
| Fusion with SIGINT/OSINT platforms | Nation state |
| Lawful-intercept handoff to core | Nation state, carrier-grade |
| Automatic report generation | Enterprise and above |
| IMSI-to-name resolution | Via HLR/HSS or commercial broker |
| Retention and pattern-of-life analytics | Nation state |

### 3.6 Nation-state programmes (publicly reported)

| Programme / actor | Reported shape |
|---|---|
| **US, NSA** | Airborne GSM collection; "Tactical Edge" and "SEA MAVEN" lineage; fixed sites at diplomatic premises |
| **US, DOJ/FBI** | Dirtbox airborne deployment; Stingray fleet with Harris |
| **US, CBP** | Border-zone fixed and mobile collection |
| **UK, GCHQ** | Fixed and mobile, integrated with passive SIGINT |
| **Israel, Unit 8200 lineage** | Vendor ecosystem origin; KingFish and Hailstorm families |
| **China, MSS** | Dense fixed deployment, border and urban |
| **Russia** | Fixed urban, mobile, aggressive 2G retention |
| **France, DGSE** | Fixed diplomatic and mobile |
| **Germany, BND/BfV** | Domestic mobile, IMSI use in investigations |

### 3.7 Bad-actor tier

| Capability | Cost band |
|---|---|
| SDR + OpenBTS/YateBTS/srsRAN + laptop | ~$1,000–3,000 |
| srsRAN + USRP B210, 2G/4G lab stack | ~$2,000 |
| Osmocom GSM stack, LimeSDR | ~$600 |
| Commercial low-end (Septier LightRay class) | ~$20,000–60,000 |
| Commodity IMSI-only catcher, grey market | ~$5,000–30,000 |

Criminal use cases concentrate on: identifying which phones are present in a building before a burglary, correlating a target's IMSI to intercept 2FA by SMS, and mass harvesting for later SS7 query. The 2G-only, short-dwell, low-effort deployment is the realistic criminal baseline.

### 3.8 Representative vendor landscape

L3Harris (Stingray II, KingFish, Hailstorm, Crossbow) · Parsons/DRT · Septier (IBS, Interceptor) · Rohde & Schwarz (TSMA/TSME, QualiPoc) · Keysight · Anritsu · CommScope · CellXion · PKI · Airspan · BLiNQ · Sunwave · Klas Telecom · Nokia · Cisco.

---

## 4. Vulnerable and Affected Devices

The honest answer is: every device with a cellular radio. What varies is exposure.

### 4.1 Highest exposure

| Class | Why |
|---|---|
| 2G-only handsets and feature phones | No mutual auth, no SUCI, plaintext identity |
| Devices with 2G fallback enabled | Downgrade path always open |
| Android below 12 | No modem-level 2G suppression |
| Android 12–15 without OEM implementation | Toggle absent or non-functional |
| iPhones without Lockdown Mode | 2G/3G fallback active |
| IoT, telematics, smart meters, PoS terminals | Often 2G/3G Cat-M, no toggles, years behind on patching |
| Medical and industrial cellular modems | Long lifecycle, no hardening surface |
| eSIM-only devices | Still vulnerable; eSIM changes nothing at the air interface |
| Devices with stale baseband firmware | Known baseband CVEs |
| Devices with VoLTE disabled | Forces circuit-switched fallback to 2G/3G |
| Dual-SIM handsets | Two identities, two attack surfaces |

### 4.2 Reduced exposure

| Class | Why |
|---|---|
| Android 16+ devices with IRadio HAL 3.0 | Network notifications, identifier-disclosure alerts, Mobile network security page |
| Pixel 10 and later | Ships with the full feature set |
| iOS 16+ with Lockdown Mode enabled | 2G and 3G off at the OS level |
| 5G SA-only with SUCI and a real home key | Identity concealed on the air interface |
| Devices with 2G network protection on | Largest surface closed |

### 4.3 Device properties that change the picture

- **Baseband vendor.** Qualcomm modems expose diagnostic interfaces that SnoopSnitch can read; Exynos and MediaTek largely do not. Detection capability is Qualcomm-plus-root, effectively.
- **Android Requirements Freeze.** Devices launched under GRF keep their launch HAL version, so a 2024 handset will not gain Android 16 network notifications by updating.
- **Carrier configuration.** The same handset may expose or hide the 2G toggle depending on the carrier profile pushed to it.
- **eSIM provisioning windows.** The bootstrap profile install is a distinct, brief exposure point.

---

## 5. Known Limitations and Constraints

Stated plainly, because overestimating a catcher is as damaging as underestimating one.

### 5.1 Technical

| Limitation | Detail |
|---|---|
| **Range** | Handheld tens to low hundreds of metres; vehicle up to 1–2 km in rural low band; airborne much wider but weaker per-user |
| **Capacity** | A 2G catcher saturates quickly; hundreds of handsets in a dense area cause rejects and churn |
| **Throughput** | 2G user plane is a trickle; large transfers stall or fail |
| **4G/5G plaintext** | Generally metadata only; user plane needs relay or core access |
| **Mutual authentication** | LTE/NR handsets can notice a catcher that cannot authenticate |
| **Timing** | LTE/NR require GPS-disciplined sync; a sloppy clock makes the cell look wrong |
| **Interference** | A catcher degrades the real network in its footprint; users notice |
| **Spectrum** | Transmit authority varies by jurisdiction; band choice constrained |
| **Power** | Vehicle and manpack installs need substantial battery or generator |
| **No persistence** | Passive collection cannot follow a moving target beyond range |
| **Detection of the detector** | Active units are themselves findable by drive-test and by handsets |
| **SUCI** | Defeats naive 5G identity harvesting outright |
| **Null scheme** | Operators may disable concealment, handing identity back |
| **Downgrade dependency** | Most useful attacks require the target to accept a lower generation |

### 5.2 Operational and legal

- Deployment requires spectrum authorisation or a cooperative carrier in most jurisdictions.
- Evidence admissibility varies; US practice frequently involves NDAs with the vendor that complicate disclosure in court.
- Metadata without content is often enough for a warrant application but not for a prosecution.
- A catcher in a busy area collects thousands of non-targets, which raises retention and minimisation questions.
- Vendor lock-in and closed firmware mean an operator may not know what their own box does.

### 5.3 Defender-side limitations

- Detection apps are heuristic. A clean report is not proof of absence.
- Qualcomm baseband plus root is a hard prerequisite for the best tools.
- Android's own notifications fire on legitimate behaviour too; every post-airplane-mode reattach requests identity.
- No consumer phone reports "this tower is fake" as a definitive verdict, because it cannot know.
- Lockdown Mode and 2G suppression cost coverage in rural areas and can break roaming.

---

## 6. Common Myths and Misconceptions

| Myth | Reality |
|---|---|
| "A catcher reads all your texts and calls" | On 2G, yes. On LTE/5G, mostly metadata. WhatsApp, Signal and iMessage content stays encrypted end to end regardless |
| "Airplane mode protects you" | Only while it is on. The moment you disable it you attach, and if a catcher is present it is first in the queue |
| "A VPN protects against IMSI catchers" | No. A VPN sits above the radio and hides payload destination, not identity or tower association |
| "5G is immune" | No. Null-scheme misconfiguration, SUCI-cracker correlation and downgrade all work |
| "They are only used by spies and the FBI" | Commodity SDR stacks put a working catcher under $2,000 |
| "SS7 attacks and IMSI catchers are the same thing" | Different layers. SS7 is core signalling abuse from a distance; a catcher is a local radio impersonation |
| "You can reliably detect one with an app" | Detection is anomaly heuristics with meaningful false positive and negative rates |
| "Turning off 2G makes you safe" | It removes the biggest hole. It does nothing about 4G/5G identity requests |
| "A catcher decrypts TLS" | No. It never touches your TLS session |
| "IMSI catcher means full wiretap" | Identity and metadata, and on 2G content. Not a general intercept of encrypted app traffic |
| "Detection apps work on any phone" | Qualcomm baseband and root, in practice |
| "Every silent SMS is an attack" | Carriers use Type 0 SMS legitimately for provisioning and voicemail indication |
| "eSIM protects you" | The air interface is unchanged |
| "Changing your IMEI helps" | Marginally. The IMSI is the identifier that matters |
| "The catcher has to be within a few metres" | Up to a couple of kilometres in low band, rural, vehicle-mounted |
| "A warning triangle or 'G' icon means a catcher" | It means 2G. That is a hint, not a verdict |
| "Vendors publish what their boxes do" | Frequently not. Capability claims outrun documentation |
| "You can sue your way out of it" | In the US, vendor NDAs have repeatedly been used to limit disclosure |

---

## 7. Enterprise Defensive Field Guide

This section is the operational core for a defender. It assumes no control over the carrier and no special hardware beyond what a competent IT team can buy.

### 7.1 The baseline (mandatory, all staff)

1. **2G suppression on every managed handset.** Android 12+ toggle where the OEM implements it; Android 16 settings toggle otherwise; iOS Lockdown Mode where 2G is not separately switchable.
2. **Lockdown Mode on all iOS devices** for anyone above standard risk. Accept the feature loss.
3. **Advanced Protection Mode on all Android 16+ devices.** It enables identifier-disclosure alerts, the Mobile network security page and network notifications.
4. **Null-cipher blocking** on Android 14+ (enabled by default from that version).
5. **VoLTE on**, always. Disabling it forces circuit-switched fallback to 2G/3G.
6. **Manual carrier selection** in travel and high-risk areas.
7. **No sensitive calls in the first two minutes** after leaving airplane mode.
8. **Documented device inventory** with model, baseband vendor, OS build and toggle state.

### 7.2 The travel tier system

| Tier | Profile | Controls |
|---|---|---|
| **T0 — Home** | Normal operations | Baseline only |
| **T1 — Low risk travel** | EU, EEA, Five Eyes, stable allied | Baseline, plus manual carrier select in airports |
| **T2 — Elevated** | Border zones, conferences, hostile press environments | Baseline, plus burner for the trip, no persistent accounts, airplane mode in transit |
| **T3 — High risk** | Adversarial state, sanctions work, investigative journalism | Burner only, Lockdown Mode, 2G off, minimal data, pre-trip and post-trip wipe, clean-room return |

Tier is assigned by the security lead, not self-assessed, and is recorded on the travel authorisation.

### 7.3 Signals that warrant action

Individually, none of these is proof. Two or more concurrent, or one repeating at the same location, warrants a report.

- Handset drops to 2G and stays there in an area with known 4G coverage.
- A cell appears with a strong signal and no or wrong neighbour list.
- Signal strength high but data throughput collapses.
- Cipher indicator shows A5/0, or Android reports null cipher.
- Repeated identity requests shortly after attach.
- Silent SMS delivery with no visible message.
- Cell ID never seen before at a location visited routinely.
- Battery drain spike with no usage change.
- Two handsets on the same trip both drop to 2G simultaneously.
- Android identifier-disclosure alert outside a normal reattach.

### 7.4 Response playbook

1. **Do not reboot.** A reboot loses volatile evidence and re-attaches.
2. **Screenshot** the network status, cell info and any alert.
3. **Note** time, location, and whether the condition persists after moving 200 m.
4. **Airplane mode on** if the call is sensitive and not yet made.
5. **Move and retest.** A catcher has a footprint; walking out of it is the fastest confirmation.
6. **Switch to an out-of-band channel** for the sensitive conversation — Signal over Wi-Fi, or a landline.
7. **Log** on the anomaly sheet (§12) while the detail is fresh.
8. **Report** to the security lead the same day.

### 7.5 SOC detection rules

For managed fleets with MDM telemetry, these are implementable without extra tooling.

| Rule | Signal | Threshold |
|---|---|---|
| R1 | RAT change 4G→2G | Alert on any transition outside known rural zones |
| R2 | Sustained 2G | >5 minutes in a mapped 4G area |
| R3 | Null cipher | Alert on A5/0 or EEA0 |
| R4 | Unknown cell ID | Cell ID absent from baseline for that geohash |
| R5 | Identity request burst | >3 in 10 minutes |
| R6 | Silent SMS | Type 0 SMS received |
| R7 | Neighbour anomaly | Serving cell with empty neighbour list |
| R8 | Correlated drop | Two or more fleet devices to 2G within 500 m and 10 minutes |
| R9 | Roaming mismatch | Attach to a network not in the country's approved list |
| R10 | Post-airplane reattach | Identity request within 60 s of radio-on |

R8 is the highest-value rule. Fleet correlation removes most of the single-device noise.

### 7.6 What to tell staff

Short, non-technical, repeatable:

> "Your phone can be tricked into talking to a fake mast. It mostly leaks which phone you are and where, and on old 2G it can leak the call itself. We have turned off 2G and locked the phones down. If your phone drops to 2G somewhere it shouldn't, or you get an alert, don't reboot — screenshot it, walk 200 metres, and tell us."

Avoid: "you are being spied on", "it is definitely a Stingray", and any promise of certainty.

### 7.7 Procurement and policy

- **Ask carriers** whether they have deployed 5G SA with SUCI and a real home key, and whether the null scheme is in use anywhere.
- **Require** network notifications and identifier-disclosure alerts in the device standard for Android.
- **Require** Lockdown Mode capability in the iOS standard.
- **Specify** baseband vendor where the fleet needs detection capability.
- **Write** the travel tier system into policy, with the security lead as assigner.
- **Retain** anomaly logs per the retention schedule and review quarterly for patterns.
- **Do not** buy a dedicated catcher-detection appliance unless the fleet is large, the threat is confirmed, and someone will operate it.

---

## 8. 4G and 5G Security Comparison

Read this table as a map of where the remaining holes are, not as reassurance.

| Aspect | 2G | 3G | 4G LTE | 5G NSA | 5G SA |
|---|---|---|---|---|---|
| Network authentication | None | Yes | Yes | Yes (anchor) | Yes |
| Identity concealment | None | None | None | None | SUCI |
| Cipher negotiation | A5/0–A5/3 | UEA1/2 | EEA0–3 | Inherits LTE | NEA0–3 |
| Null cipher available | Yes, common | Rare | Yes, EEA0 | Yes | Yes, NEA0 |
| Passive metadata exposure | High | High | High | High | Lower with SUCI |
| Content exposure | Yes, A5/1 breakable | Rarely | No | No | No |
| Downgrade path to 2G | — | Yes | Yes | Yes | Yes |
| Identity request post-attach | IMSI | IMSI | IMSI if needed | IMSI/SUCI | SUCI |
| Handset can detect fake | No | Partly | Partly | Partly | Partly |
| Standard mitigation | 2G off | Prefer 4G | VoLTE, no 2G | SA preferred | SA only |

**The three structural facts that matter.**

1. **Everything below 5G SA discloses identity in plaintext.** 2G, 3G, LTE and 5G NSA all send the IMSI or a value from which it is recoverable.
2. **Only 5G SA with SUCI and a genuine home key conceals identity**, and only while the device stays on SA.
3. **Every generation still accepts a downgrade.** The strongest configuration is worthless if the handset can be bidded to 2G.

**What SUCI does and does not do.** It encrypts the SUPI to the home network's public key so a passive observer sees an opaque value. It does not authenticate the serving cell, does not prevent downgrade, and is defeated where operators run the null scheme. Published SUCI-catcher work recovers identity by correlating a captured SUCI against a subscriber the attacker can already name.

**Practical configuration.** SA preferred, SA-only where coverage permits, SUCI mandatory, 2G off, VoLTE on, null cipher blocked, manual carrier selection in travel. That stack closes the identity hole on the air interface and leaves downgrade as the main remaining lever — which is exactly what the 2G toggle and Lockdown Mode address.

---

## 9. Android Hardening Guide

Ordered by effectiveness. Steps 1 and 2 close most of the surface on their own.

### 9.1 Android 16+: the built-in controls

Android 16 moved these from OEM add-ons into AOSP, gated behind Advanced Protection.

- **Settings → Security & privacy → Advanced Protection → turn on.** Enables identifier-disclosure alerts, network notifications and the Mobile network security page.
- **Settings → Network & internet → SIMs → your SIM → Allow 2G.** Switch off.
- **Mobile network security page** shows current cell, cipher state and alert history. Review it in the field.
- **Identifier-disclosure alert** fires when a network requests IMSI/IMEI outside a normal reattach. Treat it as a positive signal.

Note the Requirements Freeze caveat: only devices launched on Android 16+ with IRadio HAL 3.0 get the full set. Older hardware will not gain it by updating.

### 9.2 Android 12–15: OEM toggles

The 2G toggle exists in most OEM builds from 12 onward, at varying paths. It is absent or cosmetic on some carrier profiles.

- Pixel: Settings → Network & internet → SIMs → Allow 2G
- Samsung: Settings → Connections → Mobile networks → Network mode → LTE/3G/2G off variants
- Others: search Settings for "2G"

Verify it worked. Airplane mode off, watch the status bar, confirm no "G"/"E" appears where coverage is known 4G.

### 9.3 Below Android 12

No native toggle. Options, in order:

1. **Carrier-side barring** — ask for 2G barred on the line. Persistent, survives everything, but the carrier must cooperate and it breaks rural fallback.
2. **Network mode lock** to LTE/WCDMA only, where the OEM exposes it.
3. **Detection app** — SnoopSnitch (§9.6) for awareness, not prevention.

### 9.4 Modem and baseband

- **Null cipher:** blocked by default from Android 14. Confirm the OS build is 14 or later.
- **Baseband updates** ship in the monthly security patch. Do not defer them on high-risk devices.
- **Diagnostic mode** (dialler `*#*#717717#*#*` or vendor equivalent) exposes baseband logs on some devices; needs root for full use.
- **Do not** flash third-party basebands on a device you rely on for evidence.

### 9.5 App-level hygiene

- Signal with **registration lock** enabled, so an SMS-intercept cannot re-register your number.
- **Disable SMS as a 2FA fallback** wherever the service allows it.
- **Verify safety numbers** out of band for high-value contacts.
- **Avoid SMS for anything that matters** in T2/T3 travel.
- **Play Integrity / hardware attestation** where the app supports it.
- **Restrict background network access** for apps that do not need it — fewer radios, fewer wakes.

### 9.6 Detection tooling

**SnoopSnitch** — the reference Android tool. Reads Qualcomm baseband diagnostic data, scores cell parameters, flags consistency anomalies, detects silent SMS. Requires Qualcomm chipset and root. False positives occur on legitimate reattach.

**NetMonster** — cell logging without root, useful for building a baseline and spotting unknown cells. No verdicts.

**Cell Spy Catcher** — legacy, still useful for RAT transition logging.

**GNetTrack / Tower Collector** — crowd-sourced mapping; good for establishing what *should* be at a location.

Treat all output as corroboration. The reliable pattern is: tool flags anomaly → you walk out of the footprint → anomaly clears → you log it.

### 9.7 Baseline procedure for a new device

1. Patch to current.
2. Advanced Protection on (16+) or 2G off (12–15).
3. Install NetMonster and record the home and office cell baselines.
4. If rooted Qualcomm, install SnoopSnitch and run a 24-hour passive baseline.
5. Record everything in the device register.
6. Re-baseline after any travel over T1.

---

## 10. iPhone Hardening Guide

iOS has fewer knobs. Lockdown Mode is the whole game, and it is a good one.

### 10.1 Lockdown Mode

Settings → Privacy & Security → Lockdown Mode → Turn On. Requires a restart.

What it does that matters here:

- **Disables 2G and 3G** at the OS level. The single largest surface, closed.
- **Blocks unknown FaceTime callers**, which removes a class of probing.
- **Restricts wired accessories** — relevant to juice-jacking and to cable-based baseband access.
- **Tightens Safari and message attachment handling**, removing baseband-adjacent parsing surface.
- **Reduces attack surface generally**, at a real usability cost.

What it does not do: stop 4G/5G identity requests, prevent downgrade to LTE, or provide any detection.

### 10.2 Coverage cost

Lockdown Mode will drop coverage in 2G/3G-only areas. In rural and some roaming contexts the phone becomes a paperweight. Decide per tier: mandatory at T3, recommended at T2, optional at T1, and warn users about the coverage trade.

### 10.3 Other controls

- **Manual carrier selection** in travel: Settings → Cellular → Network Selection → off Automatic.
- **VoLTE on** — Settings → Cellular → Cellular Data Options → Voice & Data. Off forces CS fallback.
- **Disable Wi-Fi Calling** on untrusted networks unless needed; it is another interworking path.
- **Turn off "Wi-Fi Assist"** to reduce cross-RAT churn.
- **Restrict SMS 2FA** as on Android; prefer TOTP or passkeys.
- **Keep iOS current.** Baseband fixes arrive in point releases.

### 10.4 Detection on iOS

There is no equivalent to SnoopSnitch, because there is no diagnostic baseband access.

- **Field Test Mode** (`*3001#12345#*`) exposes serving cell, RAT and band. Usable for manual logging, unfriendly to read.
- **Third-party apps** (Network Cell Info Lite, etc.) can log cells but cannot see inside the baseband.
- **Carrier settings version** changes can indicate a profile push; note it in the log.

The practical iOS workflow is manual: watch the RAT indicator, note the Field Test values, walk out, re-check.

### 10.5 Device register for iOS

Record model, iOS build, Lockdown Mode state, carrier settings version, and baseline cells for routine locations. Same review cadence as Android.

---

## 11. Risk-Scoring Worksheet Template

Score each factor 0–3, multiply by weight, sum. Use per trip or per site, not per person.

| # | Factor | Weight | 0 | 1 | 2 | 3 |
|---|---|---|---|---|---|---|
| 1 | Jurisdiction hostility | 3 | Allied, stable | Allied, mixed | Contested | Adversarial |
| 2 | Border crossing | 3 | None | Air, low traffic | Air, high scrutiny | Land, hostile |
| 3 | Known catcher deployment | 3 | None reported | Occasional reports | Regular reports | Documented programme |
| 4 | Device generation | 2 | 5G SA, Android 16+ | 5G NSA, modern | LTE, modern | 2G fallback only |
| 5 | OS currency | 2 | Current | One cycle behind | Two cycles | Unpatched |
| 6 | Carrier SUCI/SA status | 2 | SA, SUCI, real key | SA, partial | NSA only | 2G-heavy |
| 7 | Data sensitivity | 3 | Public | Internal | Confidential | Regulated / source-protecting |
| 8 | Personnel profile | 2 | Anonymous | Named, low profile | Named, public role | High-profile target |
| 9 | Dwell time | 1 | <1 day | Days | Weeks | Permanent |
| 10 | Prior incidents | 2 | None | Isolated | Recurring | Confirmed targeting |
| 11 | Coverage need | 1 | Wi-Fi only | Urban only | Mixed | Rural / remote |
| 12 | Counter-surveillance skill | 2 | None | Basic | Trained | Dedicated team |

**Bands.** 0–20 low (baseline). 21–40 moderate (T1). 41–60 elevated (T2). 61+ high (T3).

**Override rules.** Any factor at 3 on items 1, 3, 7 or 10 raises the band one level. Factor 8 at 3 with factor 3 at 2 or more sets T3 outright.

**Field notes.** Score before booking, re-score on itinerary change, and record the score on the travel authorisation. A score is a decision aid, not a guarantee — a low score with a confirmed incident still escalates.

---

## 12. Anomaly Log Sheets

Print or replicate into the ticketing system. One sheet per event.

### 12.1 Event record

| Field | Entry |
|---|---|
| Event ID | |
| Date / time (local, with UTC offset) | |
| Device (asset tag, model, baseband) | |
| OS build | |
| Location (address, coordinates) | |
| Movement before event | |
| RAT before | |
| RAT during | |
| Serving cell ID / PCI / ARFCN | |
| Signal strength | |
| Neighbour cells listed | |
| Cipher state | |
| Alert shown (Y/N, which) | |
| Silent SMS (Y/N, time) | |
| Identity request (Y/N, count) | |
| Duration of condition | |
| Cleared after moving 200 m (Y/N) | |
| Cleared after airplane mode cycle (Y/N) | |
| Screenshots attached (Y/N, refs) | |
| Other devices affected | |
| Reporter | |
| Reviewer | |
| Classification (confirmed / probable / possible / noise) | |

### 12.2 Narrative

Free text. What was happening, what changed first, what the user did, what happened after. Keep it factual and time-ordered; interpretation goes in the classification line, not the narrative.

### 12.3 Corroboration checklist

- [ ] Second device at same location, same time
- [ ] Detection tool output captured
- [ ] Cell ID checked against baseline
- [ ] Cell ID checked against public tower maps
- [ ] Carrier queried on cell ID validity
- [ ] Adjacent-location retest done
- [ ] Time correlated with any known event or movement

### 12.4 Review outcomes

| Outcome | Meaning | Next step |
|---|---|---|
| **Confirmed** | Multiple independent indicators, footprint behaviour | Incident process, carrier notified |
| **Probable** | Two or more indicators, no contradiction | Monitor, re-test, retain log |
| **Possible** | Single indicator | Retain, watch for repeat at location |
| **Noise** | Explained by legitimate reattach or coverage | Close |

---

## 13. Privacy Travel Checklist

### 13.1 Before travel

- [ ] Tier assigned and recorded by the security lead
- [ ] Device choice matches tier (burner for T2/T3)
- [ ] Patched to current
- [ ] Advanced Protection on, or 2G off
- [ ] Lockdown Mode on (iOS, T2/T3)
- [ ] Null cipher blocked (Android 14+)
- [ ] VoLTE confirmed on
- [ ] Baseline cells recorded for home and office
- [ ] Signal registration lock enabled
- [ ] SMS 2FA disabled on critical accounts
- [ ] Sensitive data moved off-device or into an encrypted container
- [ ] Cloud backup paused for the trip
- [ ] Out-of-band comms channel agreed with the team
- [ ] Emergency contact and check-in schedule set

### 13.2 In transit

- [ ] Airplane mode through security and border queues
- [ ] Radio on only after clearing the border, and away from the terminal
- [ ] No sensitive call in the first two minutes after radio-on
- [ ] Manual carrier selection at the first opportunity
- [ ] Watch for 2G drop, null cipher, unknown cells
- [ ] Airplane mode in any vehicle with an unknown fit-out
- [ ] Public Wi-Fi only over VPN; prefer cellular hotspot
- [ ] Cabled charging from your own charger or battery, not public ports

### 13.3 At destination

- [ ] Sweep for 2G before the first sensitive call
- [ ] Manual carrier selection retained
- [ ] Sensitive conversations over Signal, or outdoors after a walk-out check
- [ ] Log any anomaly the same day
- [ ] Keep the device on your person, not in a bag or at reception
- [ ] Note the cell ID at the accommodation for later comparison

### 13.4 On return

- [ ] Anomaly logs filed
- [ ] Device re-baselined
- [ ] T2/T3 burner wiped or retired
- [ ] Carrier settings version compared to pre-trip
- [ ] Debrief if any event occurred
- [ ] Re-score if the trip changes the standing risk

---

## 14. Glossary and Appendix

### 14.1 Glossary

| Term | Meaning |
|---|---|
| **2G / GSM** | Second generation; no network authentication, plaintext identity |
| **3G / UMTS** | Third generation; mutual auth, plaintext identity |
| **4G / LTE** | Fourth generation; mutual auth, plaintext identity, null cipher available |
| **5G NSA** | 5G radio anchored on LTE core; no SUCI benefit |
| **5G SA** | Standalone 5G; SUCI available |
| **A5/0–3, UEA, EEA, NEA** | Cipher suites by generation; the /0 variants are null |
| **ARFCN** | Absolute radio frequency channel number |
| **BCCH** | Broadcast control channel, carries cell parameters |
| **CDR** | Call detail record |
| **CI / PCI** | Cell identity / physical cell identity |
| **C1 / C2** | GSM cell reselection ranking parameters |
| **CS fallback** | Circuit-switched fallback from LTE to 2G/3G for voice |
| **ePDG** | Evolved packet data gateway, Wi-Fi calling anchor |
| **GUTI** | Globally unique temporary identity (LTE) |
| **HAL** | Hardware abstraction layer (Android radio interface) |
| **HLR / HSS** | Home location register / home subscriber server |
| **IMEI / IMEISV** | Device identity / with software version |
| **IMSI** | Subscriber identity, permanent, plaintext below 5G SA |
| **KARMA** | Technique of answering any probe as if known |
| **LAC / TAC** | Location area code / tracking area code |
| **MSISDN** | The phone number |
| **Null cipher** | Encryption algorithm 0 — no encryption |
| **PLMN** | Public land mobile network, MCC+MNC |
| **RAT** | Radio access technology |
| **Silent SMS** | Type 0 SMS, no user alert, confirms presence |
| **S-criteria** | LTE/NR reselection ranking |
| **SDR** | Software-defined radio |
| **SUCI** | Subscription concealed identifier, ECIES-encrypted SUPI |
| **SUPI** | Subscription permanent identifier, the 5G IMSI |
| **TMSI** | Temporary mobile subscriber identity |
| **Type 0 SMS** | See silent SMS |

### 14.2 Appendix A — vendor and standard references

3GPP TS 43.020 (security architecture) · TS 33.102 · TS 33.401 · TS 33.501 · GSMA FS.11 · ETSI TC LI · NIST SP 800-187 · Harris/L3Harris Stingray II · Rohde & Schwarz TSMA/TSME · Septier IBS · Osmocom · srsRAN · Open5GS · SnoopSnitch · AIMSICD.

### 14.3 Appendix B — confidence grading for findings

Used throughout this document and in Parts III–V for any claim about observed behaviour.

| Grade | Definition |
|---|---|
| **A — Confirmed** | Reproduced under controlled conditions, or two independent methods agree |
| **B — Probable** | Single method, consistent with theory, no contradiction |
| **C — Possible** | Single observation, plausible, not reproduced |
| **D — Asserted** | Vendor or third-party claim, untested here |
| **E — Folk** | Widely repeated, no primary source |

An E-grade claim in a procurement document should be marked as such.

---

## 15. References and Citations

Standards: 3GPP TS 43.020, 33.102, 33.401, 33.501, 23.003, 24.301, 38.300. GSMA FS.11 (interconnect security), FS.19, IR.88. ETSI TS 101 671 (LI handover). NIST SP 800-187 (LTE security). 3GPP TR 33.899 (5G security study).

Tooling and stacks: Osmocom (osmocom.org), srsRAN Project (srsran.com), Open5GS (open5gs.org), SnoopSnitch (opensource.srlabs.de), AIMSICD, NetMonster, GNetTrack.

Vendor documentation: L3Harris Stingray family, Rohde & Schwarz TSMA/TSME datasheets, Septier product briefs, Keysight Nemo, Anritsu field test.

Research: SUCI-catcher work (2021–2023), 5G identity concealment measurement studies, A5/1 rainbow-table literature, baseband CVE disclosures, Android Advanced Protection and IMSI-catcher-notification announcements (Android 16), Apple Lockdown Mode documentation.

**Citation note.** Vendor capability claims are D-grade until reproduced. Where a range or price appears in this part, it is indicative and should be re-quoted before use in procurement.

---

# Part II — Hardware, Software and Build Guides

**Companion to Part I**

Part version 1.0 · Compiled 2026-11-13

**Part II index**

16. [How to Use This Volume](#16-how-to-use-this-volume)
17. [Shared Hardware Substrate](#17-shared-hardware-substrate)
18. [Hardware by Category](#18-hardware-by-category)
19. [Software by Category](#19-software-by-category)
20. [Repositories With Working Code](#20-repositories-with-working-code)
21. [Build Guide B — Bad Actor and DIY](#21-build-guide-b--bad-actor-and-diy)
22. [Build Guide E — Enterprise Passive Monitoring](#22-build-guide-e--enterprise-passive-monitoring)
23. [Build Guide G — Government and Nation State](#23-build-guide-g--government-and-nation-state)
24. [Capability and Budget Ladder](#24-capability-and-budget-ladder)
25. [Failure Modes and Calibration](#25-failure-modes-and-calibration)
26. [References](#26-references)

> **Link caveat.** Vendor storefronts move, merge and go end-of-life. Where a product has moved to a parent company that is noted inline. Prices are indicative bands, not quotes. Every commercial catcher is quote-only.

---

## 16. How to Use This Volume

The three actor categories are not three different technologies. They are three points on a budget and integration curve over the **same** substrate: a software-defined radio, a disciplined clock, an amplifier, an antenna and a host. What separates a $900 laptop-and-SDR rig from a $250,000 vehicle installation is power, calibration, integration and support — not physics.

That is useful, because it means a defender can build the bottom of the curve to understand the top of it.

| Category | Label | Substrate | Integration |
|---|---|---|---|
| **B** | Bad actor / DIY | Commodity SDR, laptop | None, hand-assembled |
| **E** | Enterprise | Commercial passive scanner, rack or vehicle | Software-only, API-driven |
| **G** | Government / nation state | Purpose-built COTS appliance, amplified, GNSS-disciplined | Full, with core handoff and fusion |

Sections 17 to 20 are reference material. Sections 21 to 23 are build guides. Read §24 before buying anything.

---

## 17. Shared Hardware Substrate

Every category draws from these pools. Specific part numbers differ; the function does not.

### 17.1 Radio front ends

| Function | Why every tier needs it | Notes |
|---|---|---|
| Transceiver with TX | Attach hijack requires transmitting | Half-duplex parts are unsuitable for GSM BTS work |
| Wide tuning range | 700 MHz to 3.5 GHz covers all target bands | Narrow-band parts constrain you to one operator |
| Sufficient sample rate | GSM needs ≥ 1.6 MS/s, LTE 10–20 MHz | Low sample rate limits you to 2G |
| External clock input | Timing alignment on LTE/NR | Without it, 4G cells look malformed |

### 17.2 Timing and frequency reference

A GPS-disciplined oscillator is the single most-skipped item and the most common cause of "it transmits but nothing attaches."

| Function | Tier that needs it |
|---|---|
| GNSS-disciplined 10 MHz + 1PPS | G always, E for timing analysis, B for any 4G/5G work |
| Holdover oscillator | G, for indoor and vehicle use under bridges |

### 17.3 RF chain

| Function | Notes |
|---|---|
| LNA (receive) | Low-noise figure, mast-mounted where possible |
| Power amplifier (transmit) | 10–50 W; must be linear and band-filtered |
| Band-pass filter | Prevents out-of-band emissions; legally required in most jurisdictions |
| Directional and omni antennas | Directional for targeting, omni for harvesting |
| Mast, mag-mount, tripod | Elevation is worth more than power |

### 17.4 Host and compute

| Function | Options across tiers |
|---|---|
| Control host | Ruggedised laptop (G), rack server (E), any laptop (B) |
| Headless sensor node | ODROID, Raspberry Pi, mini-PC |
| Storage | SSD, plus remote offload for E and G |

### 17.5 Ancillary

| Item | Use |
|---|---|
| Faraday bag | Transport, isolation, evidence handling |
| USB data blocker | Charging in hostile locations |
| Labelled cable set, spare everything | Field reliability |
| Spectrum analyser or second SDR | Verify your own emissions |
| Power: LiFePO4 pack, inverter | Vehicle and manpack |

### 17.6 Physical topology (common shape)

```mermaid
flowchart LR
    A["GNSS antenna"] --> B["GPSDO<br/>10 MHz + 1PPS"]
    B --> C["SDR"]
    D["RX antenna"] --> E["LNA"]
    E --> C
    C --> F["PA + band filter"]
    F --> G["TX antenna"]
    C --> H["Host<br/>laptop / server / node"]
    H --> I["Storage + logs"]
    H --> J["Remote C2"]
```

Every build guide below is a variation on this diagram. The differences are power, calibration and what runs on the host.

---

## 18. Hardware by Category

### 18.1 Category B — bad actor and DIY

Commodity, orderable by anyone, no account required.

| Device | Band | Duplex | Rate | Use | Price band | Link |
|---|---|---|---|---|---|---|
| **LimeSDR Mini 2.0** | 10 MHz–3.5 GHz | 1×1 | 30.72 MS/s | Best cheap GSM BTS radio, Osmocom-supported | ~$400 | <https://www.crowdsupply.com/lime-micro/limesdr-mini> |
| **LimeSDR USB** | 100 kHz–3.8 GHz | 2×2 | 61.44 MS/s | MIMO, better filtering | ~$700 | <https://www.crowdsupply.com/lime-micro/limesdr> |
| **bladeRF 2.0 micro xA4** | 47 MHz–6 GHz | 2×2 | 61.44 MS/s | YateBTS and srsRAN supported | ~$500 | <https://www.nuand.com/product/bladerf-xa4/> |
| **bladeRF 2.0 micro xA9** | 47 MHz–6 GHz | 2×2 | 122.88 MS/s | Same, more bandwidth | ~$800 | <https://www.nuand.com/product/bladerf-xa9/> |
| **USRP B210** | 70 MHz–6 GHz | 2×2 | 56 MS/s | The reference platform, everything supports it | ~$1,500 | <https://www.ettus.com/all-products/ub210-kit/> |
| **ADALM-PLUTO** | 325 MHz–3.8 GHz | 1×1 | 61.44 MS/s | Cheap 2G/4G, poor filtering | ~$250 | <https://www.analog.com/en/resources/evaluation-hardware-and-software/evaluation-boards-kits/adalm-pluto.html> |
| **AntSDR E200** | 70 MHz–6 GHz | 2×2 | 61.44 MS/s | Zynq-based, standalone capable | ~$500 | <https://www.crowdsupply.com/microphase-technology/antsdr-e200> |
| **HackRF One** | 1 MHz–6 GHz | **Half** | 20 MS/s | Passive sniffing only, not BTS | ~$350 | <https://greatscottgadgets.com/hackrf/one/> |
| **RTL-SDR Blog V4** | 24–1766 MHz | RX only | 2.4 MS/s | Passive 2G scanning, GSM decode | ~$40 | <https://www.rtl-sdr.com/buy-rtl-sdr-dongles/> |
| **KrakenSDR** | 24–1766 MHz | RX only, 5ch | — | Direction finding, coherent array | ~$500 | <https://www.krakenrf.com/> |

**Host:** any x86-64 laptop running Linux. Ubuntu 22.04 LTS. Do not use Windows; the toolchains assume Linux.

**Critical exclusions.** HackRF is half-duplex and cannot run a full GSM transceiver; it is fine for `gr-gsm` sniffing and useless as a BTS. RTL-SDR cannot transmit at all.

### 18.2 Category E — enterprise

Passive-first, calibrated, rack or vehicle mounted. Almost all quote-only.

| Device | Type | Band | Why enterprise buys it | Link |
|---|---|---|---|---|
| **Rohde & Schwarz TSMA6** | Passive scanner + autonomous UE | 350 MHz–4.4 GHz | Reference-grade passive, integrates with ROMES/QualiPoc | <https://www.rohde-schwarz.com/products/test-and-measurement/network-analyzers/rs-tsma6-autonomous-mobile-network-scanner_63493-1103098.html> |
| **Rohde & Schwarz TSME6** | Ultra-compact scanner | 350 MHz–4.4 GHz | Covert passive, USB/Ethernet | <https://www.rohde-schwarz.com/products/test-and-measurement/network-analyzers/rs-tsme6-ultracompact-drive-test-scanner_63493-1103100.html> |
| **ThinkRF R5750** | RF downconverter/analyser | 9 kHz–27 GHz | Wideband capture, software-defined | <https://thinkrf.com/products/> |
| **Signal Hound SM200B** | Spectrum analyser | 20 kHz–20 GHz | Cheaper wideband, good API | <https://signalhound.com/products/sm200b-20-ghz-rf-transceiver/> |
| **Aaronia Spectran V6** | Real-time analyser | up to 6 GHz | Real-time bandwidth for burst capture | <https://aaronia.com/> |

**Supporting:** rack chassis, PoE switch, NTP/GNSS time server, mast or vehicle mount, remote management.

**Enterprise generally does not transmit.** If the requirement includes attach hijack or identity solicitation, enterprise buys into Category G.

### 18.3 Category G — government and nation state

Purpose-built appliances. Public detail is thin; capability claims outrun documentation.

| Platform | Vendor | Reported shape | Link |
|---|---|---|---|
| **Stingray II** | L3Harris | Manpack/vehicle active catcher | <https://www.l3harris.com/> |
| **KingFish** | L3Harris | Portable, IMSI/IMEI/targeting | <https://www.l3harris.com/> |
| **Hailstorm** | L3Harris | 4G/LTE-capable | <https://www.l3harris.com/> |
| **Crossbow** | L3Harris | Transportable multi-RAT | <https://www.l3harris.com/> |
| **IBS / Interceptor** | Septier | Active, 2G–5G | <https://septier.com/> |
| **LightRay** | Septier | Low-cost tactical | <https://septier.com/> |
| **DRT family** | Parsons | Modular SDR receivers and transmitters | <https://www.parsons.com/> |
| **PKI / Phantom** | PKI Electronic Intelligence | Vehicle and fixed | <https://www.pki-electronic.com/> |
| **CellXion** | CellXion | Vehicle-integrated | <https://www.cellxion.com/> |
| **Sunwave** | Sunwave | Low-cost active | <https://www.sunwavetech.com/> |
| **BLiNQ** | BLiNQ Networks | Deployable LTE | <https://blinqnetworks.com/> |
| **Airspan** | Airspan | Small cell based | <https://airspan.com/> |

**Supporting:** GNSSDO, 20–50 W amplifier, band filters, mast, vehicle or aircraft mount, operator laptop, core-network integration, fusion platform.

**Aircraft variant.** A fixed-wing or rotary platform with a belly antenna and a rack holds a wide-area catcher. This is the "dirtbox" shape and requires aviation integration, not just RF skill.

**Maritime and fixed.** Coastal sites and embassy rooftops are permanently installed with directional sectors and fibre backhaul.

### 18.4 Alternatives and crossovers

| If you cannot buy… | Substitute |
|---|---|
| Stingray | USRP N310 + srsRAN + Open5GS + PA, in a vehicle |
| Septier LightRay | LimeSDR + Osmocom on a ruggedised laptop |
| R&S TSMA6 | ThinkRF R5500 + open-source decoder |
| TSME6 | AntSDR E200 in a waterproof box |
| KrakenSDR DF | Two directional antennas and manual bearings |

---

## 19. Software by Category

### 19.1 Shared components

| Function | Options |
|---|---|
| SDR driver | UHD (Ettus), SoapySDR, LimeSuite, bladeRF CLI |
| Signal framework | GNU Radio |
| Capture and analysis | Wireshark, GQRX, CubicSDR, SDR# |
| Mapping | QGIS, CellMapper |
| Telemetry | InfluxDB + Grafana |

### 19.2 Category B — open-source stacks

| Stack | Generation | State | Link |
|---|---|---|---|
| **Osmocom** (osmo-bts-trx, osmo-trx, osmo-hlr, osmo-msc) | 2G | Active, the reliable choice | <https://osmocom.org/> |
| **YateBTS** | 2G | Dormant but functional, bladeRF/USRP native | <https://yatebts.com/> |
| **srsRAN_4G** | 4G | Maintained, superseded by _Project | <https://github.com/srsran/srsRAN_4G> |
| **srsRAN_Project** | 4G/5G | Active | <https://github.com/srsran/srsRAN_Project> |
| **Open5GS** | 4G/5G core | Active | <https://github.com/open5gs/open5gs> |
| **OpenAirInterface** | 4G/5G | Active, heavier | <https://openairinterface.org/> |
| **Magma** | 4G/5G core | Active, operator-oriented | <https://github.com/magma/magma> |
| **Free5GC** | 5G core | Active, research | <https://github.com/free5gc/free5gc> |
| **gr-gsm** | 2G passive | Maintained | <https://github.com/ptrkrysik/gr-gsm> |
| **Oros42/IMSI-catcher** | 2G passive | Active | <https://github.com/Oros42/IMSI-catcher> |
| **OsmocomBB** | 2G phone-side | Active, needs a C123 handset | <https://osmocom.org/projects/baseband> |
| **Kalibrate** | GSM channel scan | Maintained | <https://github.com/steve-m/kalibrate-rtl> |

### 19.3 Category E — enterprise software

| Product | Function | Link |
|---|---|---|
| R&S ROMES | Drive-test and analysis | <https://www.rohde-schwarz.com/> |
| R&S QualiPoc | Handset-based measurement | <https://www.rohde-schwarz.com/> |
| Keysight Nemo | Drive-test suite | <https://www.keysight.com/us/en/products/nemo.html> |
| Accuver XCAL | Drive-test | <https://www.accuver.com/> |
| VIAVI | Network assurance | <https://www.viavi.com/> |
| ThinkRF APIs | Python/C++ capture | <https://github.com/thinkrf> |

### 19.4 Category G — government software

| Product | Function |
|---|---|
| Vendor GUI suite | Targeting, mission control, reporting |
| Core integration | MME/AMF handoff for lawful intercept |
| Fusion platform | Correlation with SIGINT and OSINT |
| Guavus, Cisco | Analytics and subscriber correlation |

Category G usually pairs vendor software with a lab stack (Osmocom, srsRAN, Open5GS) for validation and for the core-side work.

### 19.5 Detection-side software

| Tool | Platform | Needs | Link |
|---|---|---|---|
| SnoopSnitch | Android | Root, Qualcomm | <https://github.com/srlabs/snoopsnitch> |
| AIMSICD | Android | Root | <https://github.com/CellularPrivacy/Android-IMSI-Catcher-Detector> |
| CellMapper | Android | Nothing | <https://www.cellmapper.net/> |
| KrakenSDR DOA | Linux | KrakenSDR | <https://github.com/krakenrf/krakensdr_doa> |

---

## 20. Repositories With Working Code

Rated by whether it builds and runs today. "Works" means a competent operator can get it running; it does not mean a beginner can.

| Repo | Purpose | State | Works? |
|---|---|---|---|
| <https://github.com/srsran/srsRAN_Project> | 4G/5G RAN | Active | Yes |
| <https://github.com/open5gs/open5gs> | 4G/5G core | Active | Yes |
| <https://github.com/free5gc/free5gc> | 5G core | Active | Yes |
| <https://github.com/magma/magma> | Core, operator shape | Active | Yes, heavy |
| <https://gitlab.eurecom.fr/oai/openairinterface5g> | 4G/5G RAN | Active | Yes, heavy |
| <https://gitea.osmocom.org/cellular-infrastructure/osmo-bts> | 2G BTS | Active | Yes |
| <https://gitea.osmocom.org/cellular-infrastructure/osmo-trx> | 2G transceiver | Active | Yes |
| <https://github.com/Oros42/IMSI-catcher> | 2G passive identity | Active | Yes |
| <https://github.com/ptrkrysik/gr-gsm> | 2G decode | Maintained | Yes |
| <https://github.com/srlabs/snoopsnitch> | Detection | Maintained | Yes |
| <https://github.com/krakenrf/krakensdr_doa> | Direction finding | Active | Yes |
| <https://github.com/EttusResearch/uhd> | USRP driver | Active | Yes |
| <https://github.com/pothosware/SoapySDR> | Driver abstraction | Active | Yes |
| <https://github.com/myriadrf/LimeSuite> | LimeSDR driver | Active | Yes |
| <https://github.com/Nuand/bladeRF> | bladeRF tools | Active | Yes |
| <https://github.com/gnuradio/gnuradio> | DSP framework | Active | Yes |
| <https://github.com/RangeNetworks/OpenBTS> | 2G BTS | **Archived 2017** | Builds with effort |
| <https://github.com/RangeNetworks/OpenBTS-UMTS> | 3G BTS | **Archived** | Painful |
| <https://github.com/yatebts> | 2G BTS | Dormant | Works on bladeRF/USRP |
| <https://github.com/CellularPrivacy/Android-IMSI-Catcher-Detector> | Detection | Dormant | Builds, dated |

> **Do not start with OpenBTS.** It is the most-cited and least-maintained. Osmocom is the same capability with a live community.

---

## 21. Build Guide B — Bad Actor and DIY

**Objective:** a working 2G catcher on a laptop for under $1,000 that harvests IMSIs from passing handsets.

**Difficulty:** moderate. Linux competence and patience required.

**Time:** 2–4 hours first build.

### 21.1 Bill of materials

| Item | Spec | Price |
|---|---|---|
| LimeSDR Mini 2.0 | TX-capable, 10 MHz–3.5 GHz | ~$400 |
| GSM 900 or 1800 antenna | SMA, 2–5 dBi | ~$20 |
| USB 3.0 cable, short, shielded | — | ~$10 |
| Ubuntu 22.04 laptop, x86-64, USB 3.0 | Any | ~$300 used |
| Band-pass filter, 935–960 MHz | Optional but recommended | ~$60 |
| **Total** | | **~$800** |

A $40 RTL-SDR alongside the Lime makes verification far easier — you can watch your own BCCH.

### 21.2 Prepare the host

```bash
sudo apt update && sudo apt install -y \
  build-essential cmake git libboost-all-dev libusb-1.0-0-dev \
  libsqlite3-dev libi2c-dev python3-numpy python3-scipy \
  libgmp-dev libfftw3-dev libmbedtls-dev
```

Add udev rules for the Lime, then `udevadm control --reload`.

### 21.3 Install LimeSuite

```bash
git clone https://github.com/myriadrf/LimeSuite.git
cd LimeSuite && mkdir build && cd build
cmake .. && make -j$(nproc) && sudo make install && sudo ldconfig
LimeUtil --update
```

Verify with `LimeUtil --find`. It must list the device.

### 21.4 Install Osmocom

```bash
sudo apt install -y osmocom-nitb osmo-bts-trx osmo-trx-lms
```

If your distro lacks them, build from <https://gitea.osmocom.org/cellular-infrastructure/>.

### 21.5 Configure the PLMN

Edit `/etc/osmocom/osmo-bts-trx.cfg`:

```
phy 0
 osmotrx ip local 127.0.0.1
 osmotrx ip remote 127.0.0.1
 band 900
 trx 0
  arfcn 30
  nominal power 23
```

Edit `/etc/osmocom/osmo-trx-lms.cfg` to point at the Lime. Pick a **PLMN that does not exist locally** — 001/01 is the conventional test choice, or clone a real one to look convincing.

Start `osmo-trx-lms`, then `osmo-bts-trx`, then `osmo-nitb`. Watch the logs; `PH-DATA` and `BCCH` lines mean it is transmitting.

### 21.6 Verify and attach

- Confirm BCCH on the second SDR or a spectrum analyser. You should see a burst every 4.615 ms on the ARFCN.
- Put a test handset into manual network selection. Your PLMN should appear.
- Select it. The handset attaches and the `osmo-nitb` console shows the IMSI.
- `show subscribers` lists everyone currently camped.

### 21.7 Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| No PLMN appears | Not transmitting | Check `osmo-trx-lms` is running and `LimeUtil --find` works |
| PLMN appears, attach fails | Clock or config error | Add GPSDO; check ARFCN is clear |
| Attach succeeds, no IMSI | Cipher mismatch | Force A5/0 in `osmo-nitb` config |
| Handsets bounce back to real network | Real cell stronger | Raise power, move closer, or pick a cleaner ARFCN |
| Works for one phone, not another | Timing drift | GPSDO; check sample rate |
| Nothing at all | USB 2 port | Move to USB 3 |

**Full troubleshooting matrix in §25.**

### 21.8 Checklist

- [ ] Host prepared, udev rules installed
- [ ] LimeSuite installed, `LimeUtil --find` lists device
- [ ] Osmocom installed
- [ ] PLMN chosen and not locally in use
- [ ] ARFCN verified clear
- [ ] BCCH confirmed on second receiver
- [ ] Test handset attaches manually
- [ ] IMSI visible in console
- [ ] `show subscribers` populated
- [ ] Spectrum clean of spurious output

---

## 22. Build Guide E — Enterprise Passive Monitoring

**Objective:** continuous passive collection across a site or campus, no transmission, feeding an existing SIEM.

**Difficulty:** low technically, moderate procedurally. Procurement is the long pole.

**Time:** 1–2 weeks including install.

### 22.1 Architecture

Passive sensor at the edge, decoder in a DMZ, records into the SIEM. No TX path at all, so no spectrum licence is needed in most jurisdictions — confirm locally.

```mermaid
flowchart LR
    A["Sensor + antenna<br/>roof or mast"] --> B["PoE switch"]
    B --> C["Decoder node<br/>DMZ"]
    C --> D["InfluxDB / Grafana"]
    C --> E["SIEM via syslog"]
    C --> F["Object store<br/>retention"]
```

### 22.2 Sensor options

| Option | Cost | Trade |
|---|---|---|
| R&S TSMA6 | ~$40–70k | Reference grade, vendor support |
| ThinkRF R5750 + open decoder | ~$15–25k | Wideband, you own the software |
| AntSDR E200 + custom | ~$1k | Cheap, you own everything |
| KrakenSDR | ~$500 | Adds direction finding |

Enterprise typically buys TSMA6 for the support contract and the ROMES integration, not for the physics.

### 22.3 Decode and storage

- Decode GSM BCCH/SI and LTE SIB where in scope.
- Normalise to one schema: timestamp, cell ID, PCI/ARFCN, RAT, band, RSSI, neighbour list, cipher state where visible.
- Write to InfluxDB for time series, object store for raw IQ on trigger.
- Set retention: 30 days hot, 12 months warm, raw IQ only on incident.

### 22.4 SIEM rules

Implement §7.5 rules R1–R10 as correlation searches. R8 (fleet correlation) needs the device inventory joined on location and time.

### 22.5 Site considerations

- **Roof or mast access**, with landlord permission and safe access.
- **PoE budget** and cable run limits.
- **Lightning protection** on the antenna.
- **NTP** — the sensor and the SIEM must share a clock or correlation fails.
- **Physical security** of the enclosure.
- **Adjacent macro cells** mapped first, so the baseline includes them.

### 22.6 Acceptance

- Sensor sees all expected macro cells at the site within 3 dB of a reference handset.
- No gaps longer than 60 s in 24 hours.
- SIEM rules fire on a synthetic test event.
- Retention policy verified by age-out test.

---

## 23. Build Guide G — Government and Nation State

**Objective:** multi-RAT active platform with core handoff, targeting, and fusion.

**Difficulty:** high. Integration and spectrum authority dominate.

**Time:** 4–12 weeks.

### 23.1 Shape

Vehicle or fixed install: GNSSDO, 20–50 W amplifier, band filters, directional and omni antennas, mast, operator position, rack compute, core integration, fusion link.

### 23.2 Reference stack if building rather than buying

| Layer | Choice |
|---|---|
| Radio | USRP N310 or X310, 2×2, wide tuning |
| RAN | srsRAN_Project (4G/5G), Osmocom (2G) |
| Core | Open5GS or Magma |
| Timing | GNSSDO, 10 MHz + 1PPS, holdover |
| Amplification | 20–50 W linear, per band, filtered |
| Control | Rack server, redundant |
| Fusion | Vendor or in-house correlation |

### 23.3 Integration tasks

1. **Spectrum authority** — licence or carrier cooperation per band and site.
2. **Timing chain** — GNSSDO into the SDR external clock; verify holdover under bridge and indoor conditions.
3. **Emission verification** — spectrum analyser sweep for spurs before any field use.
4. **Core handoff** — the MME/AMF path back to a real core for lawful intercept; see Part III §29.
5. **Targeting** — allow/deny lists by IMSI, delivered from the mission system.
6. **Fusion** — feed detections into the correlation platform with confidence grading (Part I §14.3).
7. **Operator UI** — one screen, big text, minimal clicks. Field operators are not RF engineers.
8. **Acceptance** — full §44 test set.

### 23.4 Differences from Category B

| Dimension | B | G |
|---|---|---|
| Power | 10–100 mW | 20–50 W |
| Timing | None | GNSSDO, holdover |
| Bands | One | All, filtered |
| Mobility | On foot | Vehicle, aircraft, maritime |
| Core | None | Real core, LI handoff |
| Evidence | None | CDR chain, Part III §30 |
| Cost | ~$1k | $100k–$500k+ |

### 23.5 What government buys that DIY cannot

Support contracts, calibration certificates, spectrum paperwork, integration with existing SIGINT, and someone to blame. The physics is identical.

---

## 24. Capability and Budget Ladder

Buy the rung below what you think you need, then discover the gap. Rungs are cumulative.

| Rung | Capability | Cost | Who it suits |
|---|---|---|---|
| 0 | RTL-SDR passive scan + gr-gsm | ~$100 | Curious defender |
| 1 | KrakenSDR direction finding | ~$600 | Site survey, DF |
| 2 | LimeSDR + Osmocom 2G catcher | ~$800 | Understanding, harvesting |
| 3 | USRP B210 + srsRAN 4G | ~$2,500 | 4G research |
| 4 | Passive commercial sensor | ~$20–70k | Continuous enterprise monitoring |
| 5 | Vehicle active install | ~$100–250k | Mobile operations |
| 6 | Multi-RAT + core handoff + fusion | ~$250–500k+ | Nation state |

**Recommendation by need:**

- *"Do I have a problem?"* → rung 0–1, one week.
- *"Prove it to management."* → rung 1–2 plus Part I §12 logs.
- *"Monitor the campus continuously."* → rung 4.
- *"Find who is doing it."* → rung 1 plus rung 5 hire.
- *"Run operations."* → rung 6.

---

## 25. Failure Modes and Calibration

### 25.1 Transmit-path failures

| Symptom | Cause | Fix |
|---|---|---|
| No RF output | PA unpowered, filter reversed | Verify with analyser at each stage |
| Output but no attach | Clock missing or wrong | GPSDO; check sample rate matches config |
| Attach then immediate drop | Timing drift, power too high | Reduce power, add GPSDO, re-check ARFCN |
| Handsets ignore entirely | Wrong ARFCN or band, or PLMN collision | Scan for clear channel; change PLMN |
| Works at 1 m, fails at 10 m | Insufficient power or bad antenna | Raise power, better antenna, lower band |

### 25.2 Receive-path failures

| Symptom | Cause | Fix |
|---|---|---|
| Low RSSI on everything | LNA unpowered, connector torque | Check bias tee, torque to spec |
| Strong signals, bad decode | Desense from own TX | Increase TX/RX separation, add filter |
| Intermittent dropouts | USB power, thermal throttling | Powered hub, heatsink, fan |

### 25.3 Calibration sequence

Do this before any measurement claim.

1. **Analyser self-cal** and warm-up, 30 minutes.
2. **Cable and filter loss** measured at each frequency of interest; record.
3. **TX power** at the antenna port, corrected for cable loss; record against setpoint.
4. **Frequency accuracy** against a reference; record offset in ppm.
5. **Spur sweep** ±100 MHz around each operating band; record any above −36 dBm.
6. **RX sensitivity** with a signal generator; record MDS.
7. **Timing** — 1PPS to phase noise check where LTE/NR is in scope.
8. **Certificate** with date, operator, instruments and serials.

Recalibrate after any antenna, cable, amplifier or filter change. An uncalibrated rig is a rumour.

### 25.4 Environmental

| Condition | Effect | Mitigation |
|---|---|---|
| Rain | 0.05–0.2 dB/km at 900 MHz, more at 3.5 GHz | Shorter runs, sealed connectors |
| Heat | PA derating, oscillator drift | Fan, shade, thermal cutoff |
| Vibration | Connector loosening | Torque, threadlock, strain relief |
| Multipath | Fading, false RSSI | Diversity, DF averaging |

---

## 26. References

Osmocom documentation (osmocom.org) · srsRAN Project docs · Open5GS docs · GNU Radio wiki · LimeSuite wiki · bladeRF wiki · Ettus UHD docs · 3GPP TS 45.002 (channel structures) · TS 45.008 (radio link control) · TS 36.133 (LTE measurements).

Vendor: L3Harris, Septier, R&S TSMA6/TSME6 datasheets, ThinkRF, Signal Hound, Aaronia.

**Citation note.** Prices are indicative 2026 bands and will drift. Vendor capability claims are D-grade (Part I §14.3) until reproduced.

---

# Part III — Site Survey, Core Handoff, Evidence Chain and Signalling Control

**Deep-dive annex to Parts I and II**

Part version 1.0 · Compiled 2026-11-13

**Part III index**

27. [Scope and the Gap Being Addressed](#27-scope-and-the-gap-being-addressed)
28. [Site Survey, Comprehensively](#28-site-survey-comprehensively)
29. [Handing a Session to a Real Core](#29-handing-a-session-to-a-real-core)
30. [CDR Generation and the Evidence Chain](#30-cdr-generation-and-the-evidence-chain)
31. [Signalling Parameters That Force Downgrade or Plaintext](#31-signalling-parameters-that-force-downgrade-or-plaintext)
32. [Gap Analysis: Commercial, FOSS, Internal](#32-gap-analysis-commercial-foss-internal)
33. [Internal Build Order](#33-internal-build-order)
34. [References](#34-references)

> **Link caveat.** Web search was unavailable during compilation of this part. All links are from standing knowledge and are marked where drift is likely. Verify before relying on any of them in a procurement document.

---

## 27. Scope and the Gap Being Addressed

Part II said, in one line each, that a serious deployment requires a site survey and that vendor appliances earn their price through core handoff and evidence handling. Both statements were compressed to the point of being unhelpful.

This part expands them. It also states plainly where free software gets you most of the way and where it does not, and how to close the remainder internally.

The gap is real and worth naming precisely:

| Capability | Commercial | FOSS | Internal effort to close |
|---|---|---|---|
| Site survey methodology | Bundled service | Partial tooling | Moderate, mostly process |
| S1/NG core attach | Supported | **Fully available** | Low |
| Media gateway for CS voice | Supported | Available, unintegrated | High |
| CDR generation | Built in | Partial, DIY | Moderate |
| RFC 3161 timestamping | Built in | Available, unintegrated | Low |
| Custody chain and packaging | Built in | Available, unintegrated | Moderate |
| LI mediation (X1/X2/X3) | Built in | **Essentially absent** | High |
| Retention and disclosure export | Built in | DIY | Moderate |

The honest summary: the RF and core layers are solved in free software. The procedural layer — mediation, custody, disclosure — is not, and that is where a DIY programme usually fails an evidential test.

---

## 28. Site Survey, Comprehensively

A site survey is the difference between a deployment that collects and one that jams itself, alerts every handset in range, and produces artefacts nobody can defend. Budget a week per site. Do not skip because you are impatient.

### 28.1 Phase 0 — Desk study

Before leaving the office.

| Task | Detail |
|---|---|
| Regulator register | Pull the national cell register; note operator, technology, channel, azimuth, tilt |
| Public cell maps | CellMapper, OpenCellID; export the local area |
| Coverage prediction | SPLAT!, Radio Mobile, QGIS with a DEM |
| Terrain and clutter | Building heights, foliage, water, elevated structures |
| Existing interference | Historical complaints, nearby transmitters, radar, broadcast masts |
| Legal position | Licence class, power limit, coordination requirement, notification duty |
| Target definition | Harvest, target-follow, or intercept; the answer changes everything |

**Output:** a desk file with the register extract, predicted coverage, a candidate list of ARFCN/PCI to avoid, and the legal position in writing.

### 28.2 Phase 1 — Physical reconnaissance

| Item | Why |
|---|---|
| Access rights | Landlord, roof hatch, lift, keys, hours |
| Power | Available circuits, breaker capacity, UPS space |
| Mast and mounting | Height, existing steel, wind load, lightning protection |
| Earthing | Earth bar present, bond length, soil type |
| Cable route | Length, bends, fire stopping, drip loops |
| GNSS sky view | Hemisphere, obstructions, multipath from metal |
| Security | Physical, CCTV, alarm, who else has access |
| Egress | Fibre, copper, LTE backhaul, Starlink |
| RF safety | MPE calculation for the planned power and height |
| Neighbours | Who is already transmitting here and on what |

**Output:** site book with photographs, measurements, and a marked-up drawing.

### 28.3 Phase 2 — Passive RF survey

Minimum 24 hours, 72 preferred. Receive-only, so no licence needed.

**Equipment:** scanner or SDR with a calibrated front end, GNSS receiver, logging host, directional and omni antennas.

```bash
# GSM channel scan with a supported SDR
kal -s GSM900 -g 40
kal -s GSM850 -g 40

# srsRAN cell search, 4G
sudo ./cell_search -b 20 -f 806000000

# wideband sweep with gr-gsm
grgsm_scanner -b GSM900 -g 40
```

Record, per band:

| Metric | Sampling |
|---|---|
| Noise floor | Every 5 minutes, whole band |
| Occupied channels | Continuous |
| PCI / ARFCN / BSIC inventory | Continuous |
| RSCP / RSRP per cell | Continuous |
| TAC / LAC and neighbour lists | Continuous |
| Cipher indicators | Where visible |
| Time-of-day variation | Continuous, for the full window |

### 28.4 Phase 3 — Analysis

```mermaid
flowchart TD
    A["Raw sweep + cell inventory"] --> B["Noise floor profile per band"]
    A --> C["Channel occupancy heat map"]
    A --> D["Neighbour and handover matrix"]
    B --> E["Candidate clear channels"]
    C --> E
    D --> F["LAC/TAC choices that force update<br/>without breaking neighbours"]
    E --> G["Go / no-go"]
    F --> G
    G -->|"Go"| H["Site book + baseline pcap +<br/>agreed parameters"]
    G -->|"No-go"| I["Relocate or reduce ambition"]
```

Deliverables from this phase:

- Noise floor profile, with a stated confidence interval
- Occupancy heat map by hour
- Neighbour matrix showing which cells a handset would compare you against
- A shortlist of clear channels and a ranked order of preference
- Recommended LAC/TAC strategy: fresh value, or clone-a-neighbour
- Predicted self-interference footprint at candidate power levels

### 28.5 Phase 4 — Baseline capture

Capture the untouched RF environment for later comparison.

```bash
# ring buffer, 500 MB files, 20 files, sha256 per close
dumpcap -i <iface> -b filesize:512000 -b files:20 -w baseline.pcapng
```

Hash each closed file immediately and append to a manifest. Baseline pcaps are the control group for every later claim of "a new cell appeared."

### 28.6 Phase 5 — Low-power key-up test

Transmit at the lowest useful power, off-peak, and measure:

| Check | Pass condition |
|---|---|
| Own emissions inside the channel | Spectrum analyser, no adjacent splatter |
| Neighbour RSCP unchanged | Within 2 dB of baseline |
| Handsets attach | At least one test handset, quickly |
| No mass reselection | Fewer than 10% of test handsets churn |
| Withdrawal clean | All test handsets return to the real cell inside 60 s |

### 28.7 Phase 6 — Go/no-go gate

| Criterion | Weight | Fail action |
|---|---|---|
| Legal position documented | Mandatory | Stop |
| Noise floor adequate | Mandatory | Relocate |
| Clear channel available | Mandatory | Relocate or narrow band |
| GNSS lock achievable | Mandatory for 4G/5G | Relocate or 2G-only |
| Neighbour impact acceptable | High | Reduce power |
| Physical access stable | High | Relocate |
| Baseline captured and hashed | High | Capture first |

### 28.8 Phase 7 — Post-deployment verification

Repeat the Phase 5 checks after 1 hour, 24 hours and 7 days. Log the delta. A degradation that appears on day three is usually thermal or a neighbour changing configuration, not your settings.

### 28.9 Survey anti-patterns

| Anti-pattern | Consequence |
|---|---|
| Deploying at midday in a quiet window | Night traffic finds the collision you missed |
| Using maximum power "to be safe" | Mass reselection, complaints, self-interference |
| Skipping the desk study | Re-inventing a channel plan the regulator already published |
| Cloning a neighbour's LAC without checking | Both cells fight; handovers thrash |
| No baseline | No way to prove you caused or did not cause a fault |
| Surveying on a different band than deployment | Numbers do not transfer |

---

## 29. Handing a Session to a Real Core

### 29.1 What the phrase actually means

A catcher that runs its own core is an island. The handset attaches, gets an identity request, and then either sits on a fake network with no service or drops. Handing the session to a real core means the handset gets **genuine service** — real authentication, real data, real voice — while you remain in the path.

There are two distinct architectures and they are often conflated.

```mermaid
flowchart TD
    subgraph A["Architecture A — Integrated eNB/gNB"]
        A1["UE"] --> A2["Catcher<br/>(acts as eNB/gNB)"]
        A2 -->|"S1-MME / NGAP<br/>SCTP"| A3["Real MME / AMF"]
        A2 -->|"S1-U / NG-U<br/>GTP-U"| A4["Real SGW-U / UPF"]
        A3 --> A5["HSS / UDM"]
    end
    subgraph B["Architecture B — Relay / proxy"]
        B1["UE"] --> B2["Catcher<br/>(radio + NAS proxy)"]
        B2 -->|"NAS relayed"| B3["Real eNB/gNB"]
        B3 --> B4["Real core"]
    end
```

**Architecture A** is cleaner. The catcher *is* an eNB. If the target's IMSI is provisioned in the operator HSS, authentication succeeds properly and the session is fully genuine. The catcher sees all S1AP and can mirror S1-U.

**Architecture B** is stealthier and harder. The catcher terminates the radio and relays NAS to a real base station, which means it must track two cipher states and stay transparent. Handsets are much less likely to notice, but timing and state bugs are constant.

### 29.2 Interfaces, precisely

| Interface | Protocol | Port | Between |
|---|---|---|---|
| S1-MME | S1AP over SCTP | 36412 | eNB ↔ MME |
| S1-U | GTP-U over UDP | 2152 | eNB ↔ SGW-U |
| X2 | X2AP over SCTP | 36422 | eNB ↔ eNB |
| NG (control) | NGAP over SCTP | 38412 | gNB ↔ AMF |
| NG (user) | GTP-U over UDP | 2152 | gNB ↔ UPF |
| N2/N3 | as NG | — | 5G equivalents |
| Mn | H.248 over SCTP/UDP | 2944 | MSC Server ↔ MGW |
| Mc | H.248 | 2944 | (2G/3G equivalent) |
| ISC / SIP | SIP over UDP/TCP | 5060 | S-CSCF ↔ application server |

### 29.3 What "media gateway" means here

A media gateway converts bearer formats and transports. In a 2G intercept it lets the catcher's MSC place the call leg onto the PSTN or an operator MGW.

- **2G/3G CS voice:** catcher MSC → Mn/H.248 → MGW → TDM or SIP egress. FOSS approximation: Asterisk or FreeSWITCH acting as MGW plus a SIP trunk, with `osmo-msc` bridged to it.
- **VoLTE:** far harder. Requires IMS — P-CSCF, S-CSCF, HSS, and the operator's own IMS. Most DIY programmes simply do not do VoLTE intercept and accept CS fallback to 2G/3G.

State this to stakeholders early: **VoLTE intercept in a DIY stack is a project, not a checkbox.**

### 29.4 Building Architecture A with FOSS

You need a core that accepts an external RAN and exposes the interfaces. Open5GS does both.

**Topology (lab):**

```text
srsRAN eNB/gNB  ──S1/NG──►  Open5GS MME/AMF  ──►  Open5GS SGW/UPF  ──►  NAT  ──►  internet
        │                          │
        │                          └──► HSS/UDM  (subscribers.yaml)
        └──S1-U/NG-U──►  UPF (gtp5g kernel module)
```

**Steps:**

```bash
# 1. kernel GTP module, needed for real user-plane throughput
git clone https://github.com/open5gs/gtp5g.git
cd gtp5g && make && sudo make install && sudo depmod -a && sudo modprobe gtp5g

# 2. core
git clone https://github.com/open5gs/open5gs && cd open5gs
meson build --prefix=/usr && ninja -C build && sudo ninja -C build install

# 3. provision the target IMSI so authentication can succeed
sudo open5gs-dbctl add 001010000000001 465B5CE8B199B49FAA5F0A2EE238A6BC E8ED289DEBA952E4283B54E88E6183CA
```

`open5gs-dbctl add <imsi> <ki> <opc>` — you need the Ki and OPc. Without them, the handset fails authentication and you get the identity but no service. This is the single most common failure point in Architecture A: **you must hold credentials for the target's SIM.**

Where you do not, you are limited to identity harvesting, not service handoff.

**Then point srsRAN at it:**

```ini
# enb.conf
[enb]
mcc = 001
mnc = 01
mme_addr = 127.0.1.100
gtp_bind_addr = 127.0.1.1
```

**AMF/MME address binding** must match `mme.yaml` / `amf.yaml` `s1ap_server` / `ngap_server` `bind_address`.

### 29.5 The 5G complication

On NG, the gNB's NGAP carries the SUCI, not the SUPI. Open5GS's UDM must hold the subscriber's SUCI-deconcealment key (the home network private key) to resolve it. If you do not have it, the AMF logs an opaque value and authentication fails.

Three ways through:

1. Hold the operator's home-network private key (rare outside the operator).
2. Force the UE onto null-scheme so the SUPI arrives in plaintext.
3. Do not use 5G — bid down to LTE, where the IMSI is plaintext on request.

### 29.6 Legal-intercept interfaces

Standards worth having on the shelf:

| Standard | Subject |
|---|---|
| ETSI TS 101 671 | HI1/HI2/HI3 handover interfaces |
| 3GPP TS 33.107 | 3GPP network LI architecture |
| 3GPP TS 33.108 | HI2/HI3 for 3GPP networks |

The chain is: network function → **X1** → mediation → **X2/X3** → LEA. X1 is usually SIP or a proprietary export. X2 carries IRI (intercept-related information — signalling) and X3 carries CC (content of communication).

**There is no mature free LI mediation platform.** This is the largest genuine gap in the FOSS stack. Build one, or buy one.

### 29.7 Building minimal mediation internally

A workable X1→X2/X3 skeleton:

| Component | Tool |
|---|---|
| X1 SIP listener | Kamailio with `sipdump`-style capture |
| IRI extraction | `tshark` with S1AP/NAS dissectors, `-T ek` to JSON |
| CC extraction | RTP from `rtpengine` or FreeSWITCH capture |
| Envelope | ASN.1 per TS 33.108, or JSON with a documented schema |
| Transport to LEA | SFTP with per-file hashing, or a REST endpoint |
| Correlation | A shared `xid` across IRI and CC |

```bash
# IRI extraction, eNB-side
tshark -i s1 -Y "s1ap" -T ek -w iri.ndjson -b filesize:102400

# CC capture
dumpcap -i s1u -f "udp port 2152" -w cc.pcapng
```

Document your own envelope schema and version it. An LEA will accept a schema you can defend; it will not accept one you invented on the day.

### 29.8 Relay architecture (B), briefly

Proxy the NAS between the UE and a real eNB. Practical building blocks:

- `srsRAN` in `ue` mode for the upstream leg
- A NAS-aware proxy — no mature FOSS exists; most implementations are bespoke C or Python
- Two cipher contexts, keyed separately, with re-key handling on both sides

Expect three to six months of engineering for a stable relay.

---

## 30. CDR Generation and the Evidence Chain

### 30.1 Why this is the part that fails

A technically perfect intercept is worthless if you cannot show, months later, that the file is the same file, produced at the time claimed, by the equipment claimed, unaltered. Courts and regulators ask four questions and FOSS answers three of them well:

| Question | FOSS answer |
|---|---|
| Is this the original? | Yes — SHA-256 at capture close |
| When was it taken? | Yes — RFC 3161 trusted timestamp |
| Was it altered? | Yes — hash chain plus immutable storage |
| Who handled it, and in what order? | Partly — auditd and signed manifests |
| Is the tooling validated? | **No** — you validate it yourself |

### 30.2 CDR schema

A defensible CDR carries more than the call. Minimum fields:

```text
record_id          UUIDv4
xid                correlation id, shared with CC
event_type         attach | detach | identity_req | auth | pdp_activate | call_start | sms
timestamp_utc      RFC 3339, millisecond precision
imsi               as observed
imei / imeisv      as observed
msisdn             if resolved
plmn_mcc_mnc       your broadcast value
lac_tac            your broadcast value
cell_id            your cell
rat                GSM | UMTS | LTE | NR
cipher             A5/0 | EEA0 | NEA0 | encrypted
direction          mo | mt
peer               other party
cause_code         release cause
duration_s         where applicable
bytes_up / down
source_node        hostname + build hash
prev_record_hash   hash chain
record_hash        SHA-256 of this record, prev hash included
```

The `prev_record_hash` field turns the CDR set into a hash chain. Removing a record breaks the chain visibly.

### 30.3 Timestamping

Use RFC 3161, not `date`.

```bash
# build a timestamp query over the capture hash
sha256sum exhibit.pcapng > exhibit.sha256
openssl ts -query -data exhibit.sha256 -sha256 -cert -out exhibit.tsq

# submit to a TSA and store the reply
curl -s -H "Content-Type: application/timestamp-query" \
     --data-binary @exhibit.tsq https://freetsa.org/tsr -o exhibit.tsr

# verify later
openssl ts -verify -in exhibit.tsr -data exhibit.sha256 -CAfile cacert.pem
```

FreeTSA (`https://freetsa.org/`) is a public TSA. For production, contract a TSA with an audited clock, or run your own with `openssl ts` plus a GNSS-disciplined NTP source. Never timestamp from an unverified host clock.

### 30.4 Hashing and immutability

```bash
# hash every closed capture immediately
find ./captures -name '*.pcapng' -newer .lastrun -print0 \
  | xargs -0 sha256sum >> manifest.sha256

# verify the whole set before disclosure
sha256sum -c manifest.sha256
```

Storage side: write-once. S3 Object Lock in compliance mode, MinIO with immutability, or WORM optical. Local disk is not evidence storage.

### 30.5 Chain of custody

| Control | Implementation |
|---|---|
| Who touched what | `auditd` rules on the capture and evidence paths |
| Ordering | Hash chain in CDR, monotonic sequence in manifest |
| Transfer record | Signed handover form, countersigned, scanned into the bag |
| Storage integrity | Object lock, versioning, delete-protection |
| Access log export | `auditd` to a remote `syslog-ng` the operator cannot edit |
| Media destruction | Certificate of destruction, referenced in the bag |

```bash
# auditd: watch the evidence tree
auditctl -w /srv/evidence -p war -k evidence
```

### 30.6 Packaging

Use BagIt. It is a Library of Congress standard, it is free, and it produces a verifiable manifest.

```bash
pip install bagit
bagit.py --processes 4 /srv/evidence/exhibit-2026-11-13-001
bagit.py --validate /srv/evidence/exhibit-2026-11-13-001
```

A bag contains `bagit.txt`, `manifest-sha256.txt`, `bag-info.txt` and the payload. Add your custody form and TSR files to the payload, then re-bag. `bag-info.txt` should carry source, contact, capture start and end, tool versions and build hashes.

### 30.7 Tool validation

Nobody validates your stack but you. Minimum:

| Test | Method |
|---|---|
| Capture fidelity | Inject known traffic with `tcpreplay`, verify byte-for-byte |
| Hash correctness | Known-answer test against `sha256sum` on a fixture |
| Timestamp correctness | Verify a TSR against a control file |
| Clock discipline | `chronyc tracking`, offset logged per session |
| Repeatability | Same input, three runs, identical hashes |
| Negative test | Corrupt a byte, confirm verification fails |

Record the results in a validation report per tool version. Re-run on upgrade. This document is what turns a hobby rig into an instrument.

### 30.8 Retention and disclosure

Retention schedule by data class, approved by legal, enforced by lifecycle rules. Disclosure export should be a single command producing a bag plus a redaction log. Redaction itself must be hashed and the original retained.

### 30.9 What FOSS will not give you

- A validated, certified LI mediation platform
- ASN.1 encoders for TS 33.108 out of the box
- Any guarantee an LEA will accept your schema
- Certified time sources without money

Everything else in this section is buildable in a fortnight by one competent engineer.

---

## 31. Signalling Parameters That Force Downgrade or Plaintext

These are the levers. Each is a real field, not a magic string.

### 31.1 PLMN — the gatekeeper

A handset attaches only to a PLMN in its SIM's home list or the operator-controlled PLMN selector. Broadcast a PLMN it does not know and nothing happens.

| Region | Operator | MCC | MNC |
|---|---|---|---|
| US | T-Mobile | 310 | 260 |
| US | AT&T | 310 | 410 |
| US | Verizon | 311 | 480 |
| Canada | Rogers | 302 | 720 |
| Canada | Bell | 302 | 610 |
| Canada | Telus | 302 | 220 |
| UK | Vodafone | 234 | 15 |
| UK | EE | 234 | 30 |
| UK | O2 | 234 | 10 |
| UK | Three | 234 | 20 |
| Germany | Telekom | 262 | 01 |
| Germany | Vodafone | 262 | 02 |
| Germany | O2 | 262 | 03 |
| France | Orange | 208 | 01 |
| France | SFR | 208 | 10 |
| Australia | Telstra | 505 | 01 |
| Japan | NTT docomo | 440 | 10 |
| Japan | KDDI | 440 | 50 |
| Test | 3GPP test PLMN | 001 | 01 |

Full tables: 3GPP TS 23.003 Annex, or the ITU-T E.212 register.

### 31.2 Cipher selection — the plaintext lever

The network sends a *list* of permitted algorithms and the handset takes the first it supports. Send only the null algorithm and you get plaintext.

**GSM — OsmoBTS, in the `bts` node:**

```text
bts 0
 cipher a5/0
```

`a5/0` means no ciphering. `cipher a5/1 a5/3` offers both and lets the handset pick.

**LTE — Open5GS `mme.yaml`:**

```yaml
security:
  integrity_order: [EIA2, EIA1, EIA0]
  ciphering_order: [EEA0]
```

**5G — Open5GS `amf.yaml`:**

```yaml
security:
  integrity_order: [NIA2, NIA1, NIA0]
  ciphering_order: [NEA0]
```

**srsRAN** exposes `cipher_algo` and `integ_algo` in the security section of `enb.conf` / `gnb.conf`. Set `cipher_algo = EEA0` for null ciphering.

### 31.3 LAC / TAC — the identity lever

A handset sends a Location Update when the LAC/TAC changes. That update carries the IMSI if no valid TMSI/GUTI exists for the new area.

Two strategies:

| Strategy | Effect | Risk |
|---|---|---|
| Fresh unused LAC | Guaranteed update, guaranteed IMSI | Every handset in range attaches |
| Clone a real neighbour's LAC | Looks normal | Handsets may not update at all |

```text
bts 0
 location_area_code 4242
```

Pick a value no local cell uses. Verify from the survey.

### 31.4 RAT and band — the downgrade lever

Downgrade is achieved by *absence*, not by a command. Broadcast only 2G and a handset with 2G enabled has nowhere else to go.

| To force | Do |
|---|---|
| 2G | Run only a GSM BTS, no LTE/5G |
| LTE | Run only an eNB, do not advertise NR |
| Plaintext 4G | LTE with `ciphering_order: [EEA0]` |
| Plaintext 5G | NR with `ciphering_order: [NEA0]`, and null-scheme SUCI |

### 31.5 Null-scheme SUCI

To make a 5G UE send SUPI rather than SUCI, the home network must be configured for the null scheme. On your own core:

```yaml
# amf.yaml / udm.yaml, per Open5GS documentation
security:
  suci:
    null_scheme: true
```

The UE still encrypts to its *real* home key by default, so null-scheme only helps when the UE is provisioned against your core. For an unknown handset, bid down to LTE.

### 31.6 Identity solicitation

After attach, the network may send an Identity Request for IMSI or IMEI. In Osmocom the HLR/HLR-side path issues this automatically when no TMSI is cached. To force it, clear the VLR cache or use a fresh LAC.

### 31.7 Device-side codes

Entered on the handset, not transmitted.

| Code | Platform | Function |
|---|---|---|
| `*#*#4636#*#*` | Android | Testing menu; "Set preferred network type" can pin GSM-only or LTE-only |
| `*3001#12345#*` | iOS | Field Test; serving cell, RAT, band, neighbours |
| `*#06#` | Both | IMEI display |
| `*#*#7267782#*#*` | Some Android | RAT/band lock menu, OEM-dependent |

Preferred-network-type values in the Android menu (indicative, OEM varies):

```text
GSM only              → forces 2G, guaranteed downgrade
LTE only              → blocks 2G fallback
NR only               → 5G SA, SUCI applies
LTE/GSM auto (PRL)    → fallback open
```

### 31.8 Sequence that works

```mermaid
sequenceDiagram
    participant UE
    participant C as Catcher
    UE->>C: Attach, PLMN matched, new LAC
    C->>UE: Identity Request (IMSI)
    UE->>C: IMSI plaintext
    C->>UE: Authentication (or accept)
    C->>UE: Security Mode Command, cipher list = A5/0
    UE->>C: Security Mode Complete, plaintext
    Note over UE,C: Session held, voice and SMS recoverable
```

---

## 32. Gap Analysis: Commercial, FOSS, Internal

| Need | Buy | Free | Build |
|---|---|---|---|
| Survey tooling | Vendor service | QGIS, SPLAT!, kalibrate, grgsm_scanner | Methodology in §28 |
| S1/NG attach | Vendor | Open5GS, srsRAN | §29.4 |
| Media gateway | Vendor MGW | Asterisk, FreeSWITCH, Kamailio | §29.7 |
| IMS for VoLTE | Vendor | Kamailio + Open5GS | Large |
| CDR generation | Built in | `tshark -T ek`, custom | §30.2 |
| Timestamping | Built in | `openssl ts`, FreeTSA | §30.3 |
| Custody | Built in | `auditd`, `bagit`, object lock | §30.5 |
| LI mediation | Built in | **none** | §29.7, months |
| Validation | Vendor | **none** | §30.7 |
| Support | Contract | Forums | Time |

---

## 33. Internal Build Order

Do it in this order. Each step is testable before the next.

1. Passive survey rig — scanner, GNSS, logging. No transmit.
2. Hash and timestamp pipeline on dummy files. Prove it works.
3. Open5GS core in the lab, with a known SIM.
4. srsRAN eNB into the core. One handset attaches.
5. CDR emitter, chained. Verify chain breaks on deletion.
6. BagIt packaging plus custody form.
7. Validation report for each tool.
8. Survey a real site. Baseline and gate.
9. Low-power key-up. Verify no neighbour impact.
10. Only then: mediation, IMS, VoLTE.

Steps 1 to 7 are weeks. Steps 8 to 10 are months.

---

## 34. References

**Standards**

- 3GPP TS 23.003 — Numbering, addressing and identification (PLMN, IMSI structure)
- 3GPP TS 33.107 — 3GPP network lawful intercept architecture
- 3GPP TS 33.108 — Handover interfaces for lawful intercept
- ETSI TS 101 671 — Lawful interception handover interfaces (HI1/HI2/HI3)
- IETF RFC 3161 — Time-Stamp Protocol
- IETF RFC 8493 — BagIt file packaging
- ITU-T E.212 — International identification plan for mobile terminals

**Software**

- Open5GS — <https://open5gs.org/> · docs <https://open5gs.org/open5gs/docs/>
- srsRAN — <https://github.com/srsran/srsRAN_Project>
- gtp5g — <https://github.com/open5gs/gtp5g>
- Kamailio — <https://www.kamailio.org/>
- FreeSWITCH — <https://freeswitch.org/>
- Asterisk — <https://www.asterisk.org/>
- Osmocom — <https://osmocom.org/>
- gr-gsm — <https://github.com/ptrkrysik/gr-gsm>
- kalibrate-rtl — <https://github.com/steve-m/kalibrate-rtl>
- Wireshark / tshark / dumpcap — <https://www.wireshark.org/>
- bagit-python — <https://github.com/LibraryOfCongress/bagit-python>
- hashdeep — <https://github.com/jessek/hashdeep>
- OpenSSL `ts` — <https://www.openssl.org/docs/man3.0/man1/openssl-ts.html>
- auditd — <https://github.com/linux-audit/audit-userspace>
- syslog-ng — <https://www.syslog-ng.com/>
- QGIS — <https://qgis.org/>
- SPLAT! — <https://www.qsl.net/kd2bd/splat.html>
- Radio Mobile — <https://www.ve2dbe.com/english1.html>
- CellMapper — <https://www.cellmapper.net/>
- OpenCellID — <https://opencellid.org/>
- FreeTSA — <https://freetsa.org/>
- tcpreplay — <https://tcpreplay.appneta.com/>
- MinIO object lock — <https://min.io/>

**Further reading**

- ETSI LI handover overview — <https://www.etsi.org/standards>
- 3GPP specifications portal — <https://www.3gpp.org/specifications>

---

*Steps 8 to 10 in §33 are where programmes fail. Survey and evidence are the two disciplines that separate an instrument from an experiment.*

---

# Part IV — Build Specification, With Numbers

**Every section pairs a full specification with a bootstrap bypass**

Part version 1.0 · Compiled 2026-11-13

**Part IV index**

35. [RF Exposure and Exclusion Zones](#35-rf-exposure-and-exclusion-zones)
36. [TX/RX Isolation and Desense](#36-txrx-isolation-and-desense)
37. [Power Architecture](#37-power-architecture)
38. [Thermal Design](#38-thermal-design)
39. [GNSS and Timing Integrity](#39-gnss-and-timing-integrity)
40. [Calibration and Measurement](#40-calibration-and-measurement)
41. [Host Hardening and Watchdog](#41-host-hardening-and-watchdog)
42. [Rig Security](#42-rig-security)
43. [Configuration Management and Version Pinning](#43-configuration-management-and-version-pinning)
44. [Acceptance Testing](#44-acceptance-testing)
45. [Ground Truth](#45-ground-truth)
46. [UE Fleet and SIM Tooling](#46-ue-fleet-and-sim-tooling)
47. [Documentation Deliverables](#47-documentation-deliverables)
48. [Licensing Checklist](#48-licensing-checklist)
49. [The One-Day Bootstrap Build](#49-the-one-day-bootstrap-build)

> **How to read this.** Each section has a **Spec** (do this properly), a **Verify** (how you prove it), a **Bootstrap** (the cheap version that gets you running today), and a **Breaks when** (the failure you have accepted). Bootstraps are labelled as cutting corners. They are legitimate for a lab, a demo or a first site. They are not legitimate for an evidential deployment.

---

## 35. RF Exposure and Exclusion Zones

### Spec

Compute maximum permissible exposure, derive an exclusion radius, mark it, and enforce it.

Power density in the far field:

```
S = (P × G) / (4π d²)
d = sqrt( (P × G) / (4π S_limit) )
```

Where `S_limit` is the applicable reference level. FCC OET-65 general population at 900 MHz is `f/1500 = 0.6 mW/cm²` (6 W/m²); at 1800 MHz it caps at 1.0 mW/cm² (10 W/m²). Occupational limits are five times higher. ICNIRP 2020 general public is 4.5 W/m² at 900 MHz.

**Exclusion radius, general population, FCC, metres:**

| TX power | 3 dBi | 6 dBi | 9 dBi |
|---|---|---|---|
| 5 W @ 900 MHz | 0.36 | 0.51 | 0.73 |
| 20 W @ 900 MHz | 0.73 | 1.03 | 1.46 |
| 50 W @ 900 MHz | 1.15 | 1.63 | 2.30 |
| 20 W @ 1800 MHz | 0.56 | 0.80 | 1.13 |
| 50 W @ 1800 MHz | 0.89 | 1.26 | 1.78 |

Divide by `sqrt(5) ≈ 2.24` for occupational limits.

**Far-field caveat.** The formula is valid only beyond `2D²/λ`. A 0.5 m antenna at 900 MHz needs about 1.5 m, so the near-field distance is comparable to the exclusion radius. **Add 50% margin** and never rely on the calculated figure inside `2D²/λ`.

**Practical rules:** mount so the main beam clears head height or points away from walkways; add a physical barrier at the exclusion radius; signage at every approach; keep the radius clear during key-up; log measured values with a broadband probe.

### Verify

Broadband probe measurement at 0.5×, 1× and 2× the calculated radius, on axis and at ±45°. Record. Confirm all readings below `S_limit`.

### Bootstrap

Use the table above, round up one row, add a 2 m cone on the main beam, and put a rope around it. Do not measure.

### Breaks when

You point a 9 dBi panel along a corridor, or someone stands beside a mast-mounted omni, or you raise power later and never revisit the number. Symptom is a warm face and, eventually, a complaint.

---

## 36. TX/RX Isolation and Desense

### Spec

Your transmitter deafens your receiver. This is the number-one self-inflicted failure and it is entirely predictable.

**Requirement.** Leakage at the receiver port must sit below the receiver noise floor plus 3 dB.

GSM noise floor in 200 kHz is approximately `-174 + 10log(200000) = -121 dBm`. Target leakage `≤ -124 dBm`. With 43 dBm (20 W) transmit, required isolation:

```
I ≥ 43 + 124 = 167 dB
```

No duplexer gives 167 dB alone. You reach it by combining mechanisms:

| Mechanism | Typical contribution |
|---|---|
| TX bandpass filter | 60–80 dB at RX band |
| Duplexer / cavity duplexer | 75–90 dB |
| Vertical antenna separation, 10 m | 55–65 dB |
| Vertical separation, 25 m | 65–75 dB |
| Horizontal separation, 10 m | 40–45 dB |
| Cross-polarisation | +3 to 10 dB |

**Vertical separation beats horizontal by roughly 20 dB** because the vertical pattern null does the work. Put TX on top, RX below, never side by side.

**Also required:** LNA with high IIP3 (≥ +10 dBm) and a limiter or switchable attenuator ahead of it, so a `-37 dBm` leak does not compress the front end. AGC off; fixed gain staging.

### Verify

1. Key the PA into a dummy load. Measure leakage at the RX port with a spectrum analyser. Isolation = `P_tx - P_leak`.
2. Repeat on the real antennas at the real separation.
3. Connect the RX chain, key up, and read the noise floor rise. **Target ≤ 1 dB.**

### Bootstrap

TX and RX on the same mast, 3 m vertical, one bandpass on TX, AGC on, and accept 3–6 dB desense.

### Breaks when

Sensitivity collapses, attach range halves, and 4G cells become invisible the moment you transmit. Symptom is "it works on the bench, not in the field."

---

## 37. Power Architecture

### Spec

| Element | Specification |
|---|---|
| Rail | 12 V nominal for RF, 48 V or mains for compute where available |
| Battery | LiFePO4, sized for 8 h at measured average draw × 1.5 |
| BMS | Mandatory, with low-voltage cutoff and cell balancing |
| Fusing | Blade fuse at the battery positive, one per branch, rated 1.5× branch current |
| Breakers | DC-rated only; never AC breakers on DC |
| Inverter | Pure sine, sized 2× continuous load, for any mains kit |
| UPS | Compute on its own UPS, 30 min minimum |
| Grounding | Single-point star; chassis bonded; signal ground separate |
| Vehicle | Split-charge relay with ignition sense; measure alternator headroom first |

**Sizing worked example.** 20 W RF at 30% PA efficiency = 47 W dissipated; 12 V rail draw ≈ 4 A for the PA alone, 1 A compute, 0.5 A scanner, 0.3 A misc ≈ 5.8 A. For 8 h: 46 Ah, ×1.5 = **70 Ah LiFePO4 minimum.** Most builds under-size this by half.

### Verify

Clamp meter on each branch under full load. Voltage at the SDR terminals under load must stay above 11.8 V. Thermal camera on fuses and connectors after 30 minutes.

### Bootstrap

One 20 Ah AGM, a 10 A blade fuse, an inline switch, and a 12 V 5 A supply on mains when available.

### Breaks when

Voltage sags, the SDR browns out mid-capture, or the PA draws a spike the supply cannot source. Symptom is random disconnects and corrupt pcaps.

---

## 38. Thermal Design

### Spec

PA efficiency 25–35% means a 20 W PA dumps 40–50 W as heat. A sealed die-cast box is an oven.

| Element | Specification |
|---|---|
| PA mounting | Thermal pad or paste to an external finned heatsink, PA tab to metal |
| Heatsink | `Rth ≤ 0.8 K/W` for 45 W dissipation to hold ΔT ≈ 36 K |
| Enclosure | Vented or fan-assisted; IP54 with filtered vents is better than IP67 and hot |
| Sun | Light colour, shade, or a double-skin roof |
| Internal ambient | **≤ 50 °C** |
| SDR junction | **≤ 85 °C**, read from telemetry |
| Fan | 40 mm minimum, on a thermostatic switch at 45 °C |
| Telemetry | Temperature logged, alarm at 60 °C internal |

**Worked check.** 47 W into a 3 K/W die-cast box in still air = `ΔT = 141 K`. Hopeless. The same 47 W into a 0.8 K/W external heatsink = 38 K, which is marginal and needs air movement.

### Verify

Run at full power for 60 minutes in the intended enclosure and location, at the hottest part of the day. Log internal temperature. Confirm the PA and SDR stop climbing before 55 °C internal. Repeat with the box in direct sun.

### Bootstrap

Bolt the PA to a CPU heatsink, drill two 30 mm holes for convection, mount in shade, and add a 40 mm fan on a USB feed.

### Breaks when

Output power folds back, the SDR drops USB, or the box cooks in summer. Symptom is "it was fine in winter."

---

## 39. GNSS and Timing Integrity

### Spec

LTE and NR need frequency accuracy better than 0.05 ppm and phase alignment. Without it, handsets see the cell and refuse to camp.

| Element | Specification |
|---|---|
| Receiver | Multi-constellation, timing-grade, 1PPS output |
| Antenna | Roof or mast, clear sky, 30° elevation mask, lightning arrestor |
| Cable delay | Measured and compensated |
| Holdover | OCXO, drift logged, alarm on unlock |
| Monitoring | `ref_locked` sensor polled every 60 s, alarm on loss |
| Spoof/jam response | Degrade to 2G-only, or hold with OCXO, and alert |
| Sky view | Surveyed in Phase 1; minimum 6 satellites at 30° mask |

### Verify

`uhd_usrp_probe` → `ref_locked: Yes`. Frequency counter against a reference: error under 0.05 ppm. Pull the antenna and confirm the alarm fires and holdover engages without dropping the cell.

### Bootstrap

Use the SDR's internal TCXO for 2G only, accept 2–5 ppm, and do not attempt 4G.

### Breaks when

Handsets ignore the 4G cell, or attach and immediately drop. Symptom is "the cell is there on the analyser but not on the phone."

---

## 40. Calibration and Measurement

### Spec

Minimum bench: spectrum analyser to 6 GHz, directional coupler, 30 dB and 20 dB 100 W attenuators, 50 W dummy load, power meter, VNA or return-loss bridge, frequency counter, broadband exposure probe.

| Measurement | Frequency |
|---|---|
| Cable loss, every run | On installation and annually |
| VSWR / return loss | Every antenna, every install, `< 1.5:1` |
| TX power at the antenna port | Every install |
| Harmonic and spur check to 3× f | Every install |
| Isolation | Every install and after any mast work |
| Exposure | Every install |

Uncertainty budget documented. Analyser reference level set so the noise floor sits at −90 dBm and nothing clips.

### Verify

Written calibration record per build, with instrument serials and calibration due dates. Any instrument out of calibration invalidates the record.

### Bootstrap

Power meter and dummy load only. Verify forward power, skip return loss and spurs.

### Breaks when

You transmit into a disconnected antenna, radiate harmonics into a neighbour's band, or discover the "20 W" amplifier was delivering 8 W.

---

## 41. Host Hardening and Watchdog

### Spec

```mermaid
flowchart TD
    A["Service hang"] --> B{"systemd watchdog<br/>RuntimeWatchdogSec=30"}
    B -->|"No heartbeat"| C["Hardware watchdog<br/>/dev/watchdog resets host"]
    C --> D{"Host answers<br/>on OOB after 180 s?"}
    D -->|"Yes"| E["Log, continue"]
    D -->|"No"| F["4G router SMS command<br/>→ relay power-cycle"]
    F --> G{"Back after 300 s?"}
    G -->|"No"| H["Dispatch engineer"]
```

| Control | Setting |
|---|---|
| Read-only rootfs | Overlayfs, `/etc` and `/var` on separate writable partition |
| Hardware watchdog | `/dev/watchdog`, 30 s timeout |
| systemd watchdog | `RuntimeWatchdogSec=30`, `Restart=always` |
| Auto-start | Service enabled at boot, no login required |
| OOB access | Second path: 4G router or serial console |
| Remote power cycle | Relay on the DC rail, SMS or HTTPS triggered |
| Boot time | Under 90 s to service-ready |
| Log shipping | Remote syslog, local ring buffer only |

### Verify

`kill -9` the main service: back inside 60 s. Pull power: back inside 120 s. Block OOB: confirm the SMS reboot fires. Do this before every deployment.

### Bootstrap

`Restart=always` in systemd, a smart plug on the mains, and a human 20 minutes away.

### Breaks when

The service hangs at 02:00 in a locked building and nobody notices until the next working day.

---

## 42. Rig Security

### Spec

| Control | Specification |
|---|---|
| Full-disk encryption | LUKS2, passphrase entered at boot or TPM2 with PIN |
| Boot | Secure Boot on, signed UKI, no unsigned kernel modules except pinned DKMS |
| SSH | Keys only, `PermitRootLogin no`, non-standard port optional, `AllowUsers` allowlist |
| Fail2ban | Enabled on SSH and any web UI |
| Firewall | Default deny inbound, explicit allowlist |
| Local accounts | One operator account, no shared logins, `sudo` with logging |
| Debug interfaces | JTAG and UART disabled or physically capped |
| USB | Ports capped where not needed; no autorun |
| Physical | Tamper label across the lid seam, serials recorded, photo of the sealed unit |
| Firmware | SDR and host BIOS at a pinned version, checksums recorded |
| Secrets | Ki/OPc in a vault or `age`-encrypted file, never in the config tree |
| Wi-Fi | Off unless in use; no hotspot with a default password |

### Verify

`nmap` from another host: only expected ports. `ssh` with a wrong key: refused. Reboot: LUKS prompt appears. Tamper label photographed in place.

### Bootstrap

LUKS, key-only SSH, `ufw` default deny, one operator account. Nothing else.

### Breaks when

The box is stolen from a vehicle and the config tree holds the operator's HSS credentials in plaintext.

---

## 43. Configuration Management and Version Pinning

### Spec

| Element | Specification |
|---|---|
| Repository | Git, local forge, no public remote |
| Layout | `hosts/<site>/`, `roles/`, `group_vars/`, `files/`, `templates/` |
| Pinning | Every package, container image and commit pinned by version or digest |
| RAN stack | Source at a tagged release, submodules pinned by commit |
| Container images | `@sha256:` digests, never `:latest` |
| Config rendering | Templates only, never hand-edited on the host |
| Drift detection | Nightly checksum of `/etc` compared to the rendered tree |
| Change control | Branch, review, merge, deploy by pipeline |
| Rollback | Previous tag retained and one command away |
| Secrets | `ansible-vault` or `age`, separate from config |

```yaml
# pinning pattern
srsran_commit: 4b1c9e2
open5gs_version: "2.7.2"
limesuite_commit: 22d1a3f
uhd_version: "4.6.0.0"
```

### Verify

Re-render from the repository on a clean host and diff against production. Any difference is drift. Deploy the previous tag and confirm the rig still works.

### Bootstrap

One Git repository, one `install.sh` with explicit versions, and a `README` listing every version. Commit before every change.

### Breaks when

A rebuild six months later pulls a newer srsRAN that renamed a config key, and the rig no longer starts on site.

---

## 44. Acceptance Testing

### Spec

Run the full set before handover. Any failure is a no-go.

| # | Test | Pass condition |
|---|---|---|
| T1 | Boot to service-ready | Under 90 s, unattended |
| T2 | Watchdog: service kill | Recovers under 60 s |
| T3 | Watchdog: power pull | Recovers under 120 s |
| T4 | OOB reboot path | Fires and recovers under 300 s |
| T5 | GNSS lock | `ref_locked: Yes` within 120 s |
| T6 | GNSS loss handling | Alarm fires, holdover holds, no crash |
| T7 | TX power at antenna port | Within ±10% of setpoint |
| T8 | Return loss, every antenna | `< 1.5:1` |
| T9 | Spurs, to 3× f | All below −36 dBm |
| T10 | Isolation | Meets §36 calculation |
| T11 | Desense | Noise floor rise ≤ 1 dB |
| T12 | Thermal soak, 60 min, in situ | Internal ≤ 55 °C, stable |
| T13 | Exposure measurement | All points below limit |
| T14 | Attach, test handset | Under 15 s |
| T15 | Identity capture | IMSI logged |
| T16 | Neighbour impact | No macro cell change > 2 dB |
| T17 | Withdrawal | All test UEs return under 60 s |
| T18 | CDR chain | Break test detects deletion |
| T19 | Hash and TSR | Verify pass on a fixture |
| T20 | BagIt validate | Passes |
| T21 | Drift check | No drift from repository |
| T22 | Port scan | Only expected ports |
| T23 | Retention age-out | Fires on schedule |
| T24 | Cold-start from bare metal | Reproduces from repository alone |

### Verify

Signed test record per unit, with date, operator, instruments and results. Retained with the rig documentation.

### Bootstrap

T1, T2, T5, T7, T14, T15, T17 only. Seven tests, twenty minutes.

### Breaks when

You skip T24, the repository has drifted, and the rig cannot be rebuilt after a disk failure.

---

## 45. Ground Truth

### Spec

Before you can claim a detection, you need to know what normal looks like. Ground truth is a characterised reference environment.

| Element | Specification |
|---|---|
| Reference site | Surveyed, low-clutter, known cells, 24 h baseline |
| Reference UE | Two handsets, one on the target PLMN, one roaming |
| Reference measurements | RSCP/RSRP at fixed points, logged, repeated |
| Control captures | Daily, hashed, retained |
| Known-cell register | Every cell, with azimuth and distance |
| Comparison method | New observation versus control, same point, same conditions |

### Verify

Reproduce the baseline twice from cold. Variation under 3 dB at every fixed point. If it varies more, the site is not a reference site.

### Bootstrap

Photograph the local cells, note them in a spreadsheet, and re-check monthly.

### Breaks when

A "new cell" turns out to be a neighbour that was always there, and your report is discredited.

---

## 46. UE Fleet and SIM Tooling

### Spec

| Element | Specification |
|---|---|
| Test UEs | Minimum 3, mixed vendors, mixed generations, one 2G-only |
| SIMs | Programmable (sysmoSIM, 5Gisim), Ki/OPc recorded in the vault |
| SIM programmer | PC/SC reader, `pySim` |
| Provisioning | Scripted from the subscriber database, no manual entry |
| IMSI plan | Documented block, one per test UE, unused values only |
| UE inventory | Asset tag, IMEI, baseband vendor, OS build, SIM IMSI |
| Charging | All UEs charged before every test |
| Airplane discipline | All non-test UEs airplane mode during key-up |

```bash
# read a card
pySim-read.py -p 0

# program IMSI and Ki/OPc
pySim-prog.py -p 0 -i 001010000000123 -k <ki> -o <opc> -a 8945001234567890123
```

### Verify

Each test UE attaches, is seen by the core, and appears in the CDR. Each is removed and the detach appears. Full cycle in under 2 minutes.

### Bootstrap

One spare handset, one programmable SIM, and a note of the IMSI in the log.

### Breaks when

Two UEs share an IMSI, the core rejects the second, and you spend an afternoon on a "core bug."

---

## 47. Documentation Deliverables

### Spec

Every unit ships with:

| Document | Content |
|---|---|
| Build record | Components, serials, versions, build date, builder |
| Calibration record | Measurements, instruments, due dates |
| Site book | Survey data, photographs, drawings, gate result |
| As-built drawing | Power, RF, network, labelled |
| Acceptance record | All T24 results, signed |
| Operating procedure | Start, stop, key-up, shutdown, fault response |
| Exposure calculation | Inputs, result, radius, signage locations |
| Baseline manifest | Hashes, TSR files, capture dates |
| Change log | Every modification, dated, signed |
| Validation report | Per tool version, per §30.7 |
| Training record | Who was trained, when, by whom |

### Verify

A second engineer can operate the rig from the documents alone, without asking. Test this with someone who has not seen the unit.

### Bootstrap

A single `README.md` with start, stop and fault steps, plus a photo of the as-built.

### Breaks when

The one person who knew how it works leaves.

---

## 48. Licensing Checklist

Not legal advice. Confirm locally; this list exists so you ask the right questions.

- [ ] Transmit authority identified: licence, class licence, or carrier agreement
- [ ] Power limit for the band and class confirmed
- [ ] Frequency coordination or notification duty checked
- [ ] Out-of-band emission limits confirmed (usually −36 dBm or the local equivalent)
- [ ] Antenna gain and EIRP limit confirmed
- [ ] Indoor-only versus outdoor permission confirmed
- [ ] Duration or event limits for temporary deployments
- [ ] Aircraft or maritime rules if applicable
- [ ] Interception authority: who may lawfully intercept, and what may be retained
- [ ] Retention period and minimisation duty for non-targets
- [ ] Disclosure route if evidence is to be used formally
- [ ] Insurance for interference complaints
- [ ] Written confirmation on file before first key-up

---

## 49. The One-Day Bootstrap Build

Cut every corner above, in this order. Target: a rig that attaches a handset and logs an IMSI, on the bench, in one day.

**09:00 — Host.** Ubuntu 22.04, updates, `LimeSuite`, `osmocom-nitb`, `osmo-bts-trx`, `osmo-trx-lms`. udev rules. `LimeUtil --find` works.

**10:30 — RF.** LimeSDR on USB 3. TX to a 2 dBi whip. RX to the RTL-SDR on a second host. Dummy load available.

**11:00 — Config.** PLMN 001/01, ARFCN 30, `cipher a5/0`, `location_area_code 4242`.

**12:00 — Key up.** `osmo-trx-lms` → `osmo-bts-trx` → `osmo-nitb`. BCCH confirmed on the RTL. Power 23 dBm nominal.

**13:30 — Attach.** Test handset to manual network select, pick the PLMN, watch the console for the IMSI. `show subscribers`.

**15:00 — Logging.** `tee` the console to a file. Timestamp each line. `sha256sum` the file at close.

**16:00 — Checks.** Exposure: 2 m rope cone, no measurement. Thermal: heatsink on the Lime, fan. Watchdog: `Restart=always`. LUKS on the host.

**17:00 — Documents.** `README` with start/stop. Photo of the bench. Component list with serials.

**Skipped and accepted:** calibration, GNSS, isolation, spurs, thermal soak, CDR chain, TSR, BagIt, drift check, cold-start rebuild. All of it is in §35–§48 when you need it.

**What you have at 17:00:** a bench rig that harvests IMSIs, with a documented build and a known list of holes.

**What you do not have:** anything you can put in front of a court.

---

# Part V — 4G/5G Observation Platform: Full Build Guide

**Open hardware, open software, stealth-oriented, extensible**

Part version 1.0 · Compiled 2026-11-13 · Target: lab through field prototype, non-type-approved

**Part V index**

50. [Design Goals and Non-Goals](#50-design-goals-and-non-goals)
51. [Architecture](#51-architecture)
52. [Hardware Selection](#52-hardware-selection)
53. [Software Base Selection](#53-software-base-selection)
54. [Base Build](#54-base-build)
55. [Radio Configuration](#55-radio-configuration)
56. [Stealth Layer](#56-stealth-layer)
57. [Decoding Pipeline](#57-decoding-pipeline)
58. [Data Model and Storage](#58-data-model-and-storage)
59. [API and GUI](#59-api-and-gui)
60. [Telemetry and Charts](#60-telemetry-and-charts)
61. [Carrier Profile System](#61-carrier-profile-system)
62. [Update and Plugin System](#62-update-and-plugin-system)
63. [Deployment Form Factors](#63-deployment-form-factors)
64. [Test and Validation](#64-test-and-validation)
65. [Cost Summary](#65-cost-summary)
66. [Honest Limits](#66-honest-limits)

> **What "non-compliant" means here.** Not certified, not type-approved, not guaranteed inside spurious-emission limits, and probably operating under experimental or tolerance provisions rather than a proper assignment. That buys enormous freedom in hardware choice and enormous responsibility in testing. It also means you should read Part IV §35 before you key a transmitter in public.
>
> **Search caveat.** Web search was unavailable during compilation. Version-specific config keys and some links are from standing knowledge. Verify against the pinned release documentation before building.

---

## 50. Design Goals and Non-Goals

### Goals

| # | Goal |
|---|---|
| G1 | Full FR1 coverage, 600 MHz to 3.8 GHz, all LTE and NR bands |
| G2 | Passive-first: observe without transmitting by default |
| G3 | Stealth: transmit only in short, well-formed bursts that look like a normal cell |
| G4 | Decode NAS, RRC, S1AP/NGAP and extract identity, capability and location |
| G5 | Human-readable output: live tables, timelines, maps, charts |
| G6 | Carrier profiles, table-driven and updatable without code changes |
| G7 | Plugin architecture for new decoders, exports and analyses |
| G8 | One-command update with rollback |
| G9 | Runs on commodity hardware, no vendor licence |
| G10 | Reproducible: pinned versions, hashed config, versioned schema |

### Non-goals

| # | Non-goal | Why |
|---|---|---|
| N1 | VoLTE intercept | Needs a full IMS core; separate project |
| N2 | FR2 / mmWave | Needs different front ends entirely |
| N3 | Type approval | Out of scope by definition |
| N4 | Real-time user-plane decryption | Needs keys; metadata only |
| N5 | Production LEA mediation | Part III covers the gap; not solved here |

---

## 51. Architecture

```mermaid
flowchart TB
    subgraph RF["RF front end"]
        A1["TX antenna<br/>low profile omni"]
        A2["RX antenna<br/>separate, 3 m below"]
        A3["Passive survey SDR<br/>RX only"]
    end
    subgraph RADIO["Radio"]
        B1["PA + bandpass<br/>10-20 W"]
        B2["Primary SDR<br/>N310 / B210"]
        B3["GNSSDO<br/>10 MHz + 1PPS"]
    end
    subgraph HOST["Host — mini-PC"]
        C1["srsRAN gNB/eNB"]
        C2["Open5GS core"]
        C3["Capture + tshark"]
        C4["Decoder workers"]
        C5["API / WebSocket"]
        C6["SQLite → Postgres"]
        C7["Plugin loader"]
    end
    subgraph OUT["Output"]
        D1["Web UI<br/>tables, map, charts"]
        D2["Grafana"]
        D3["Export: CSV, JSON, pcap"]
    end
    A1 --> B1 --> B2
    A2 --> B2
    A3 --> C3
    B3 --> B2
    B2 <--> C1
    C1 <--> C2
    C1 --> C3 --> C4 --> C6
    C6 --> C5 --> D1
    C6 --> D2
    C6 --> D3
    C7 --> C4
```

**Three planes.** Radio plane (SDR, timing, RF), control plane (core and RAN), data plane (capture, decode, store, present). Keep them on separate VLANs. The radio plane never touches the internet.

---

## 52. Hardware Selection

### 52.1 Primary SDR

| Option | Band | Duplex | Max rate | 5G 100 MHz? | Price | Verdict |
|---|---|---|---|---|---|---|
| **USRP N310** | 10 MHz–6 GHz | 4×4 | 100 MS/s/ch | **Yes** | ~$7,000 | **Best. Ethernet, on-board GNSSDO, rack-mountable, no USB fragility** |
| USRP N321 | 10 MHz–6 GHz | 4×4 | 100 MS/s/ch | Yes | ~$9,500 | Same, dual 10G, overkill |
| USRP B210 | 70 MHz–6 GHz | 2×2 | 56 MS/s | Marginal | ~$1,500 | **Best budget. 40 MHz max — LTE fine, 5G 100 MHz not** |
| bladeRF 2.0 micro xA9 | 47 MHz–6 GHz | 2×2 | 122 MS/s | Yes on paper | ~$800 | Cheapest capable; USB 3 fragility, weak filtering |
| LimeSDR USB | 100 kHz–3.8 GHz | 2×2 | 61 MS/s | Marginal | ~$700 | Fine for 4G, poor image rejection |
| AntSDR E200 | 70 MHz–6 GHz | 2×2 | 61 MS/s | Marginal | ~$500 | Cheap, standalone capable, immature |

**Recommendation: N310.** It removes USB from the critical path, carries its own GNSSDO, and does 100 MHz. On a tight budget, B210 for 4G only, and accept you will re-buy for 5G.

**Stealth mods:** plain black enclosure, no branding, mount low-profile omni not a panel, keep the PA at 10 W not 50 W, and place the box indoors behind glass where possible.

### 52.2 Passive survey SDR

Separate, receive-only, always on.

| Option | Band | Price | Note |
|---|---|---|---|
| AntSDR E200 | 70 MHz–6 GHz | ~$500 | Wide, standalone |
| RTL-SDR V4 | 24–1766 MHz | ~$40 | Cheap, narrow |
| ThinkRF R5500 | 9 kHz–18 GHz | ~$6,000 | Calibrated |

Survey SDR is what makes stealth possible: you look before you leap, every time.

### 52.3 Supporting

| Item | Spec | Price |
|---|---|---|
| GNSSDO | Leo Bodnar or u-blox NEO-M8T + OCXO | ~$200 |
| PA | 10–20 W, 700–2700 MHz, linear | ~$400 |
| Bandpass filters | Per band set | ~$300 |
| Antennas | 2× wideband omni, 3 dBi, N-type | ~$200 |
| LNA | High IIP3, mast mount | ~$120 |
| Host | Intel N100 mini-PC, 16 GB, 512 GB NVMe | ~$400 |
| Case | Plain aluminium, vented, lockable | ~$150 |
| Cabling | LMR-240 runs, N connectors, weatherproofing | ~$150 |
| Power | 12 V 10 A supply + 20 Ah LiFePO4 + fuses | ~$250 |

### 52.4 Anti-recommendations

HackRF (half duplex, 20 MS/s). Any USB 2.0 SDR. Raspberry Pi 4 as host for anything above 2G. Panel antennas for a stealth build.

---

## 53. Software Base Selection

### 53.1 Chosen stack

| Layer | Choice | Why |
|---|---|---|
| RAN | **srsRAN_Project** | Only mature open 5G gNB; also does LTE; supports UHD natively |
| Core | **Open5GS** | Mature 4G+5G core, YAML config, active, supports null cipher and null-scheme SUCI |
| Decode | **tshark + pycrate** | tshark for field extraction, pycrate for NAS/RRC ASN.1 in Python |
| Capture | **dumpcap** ring buffer | Stable, no shell pipeline loss |
| API | **FastAPI + WebSocket** | Async, typed, OpenAPI for free |
| Frontend | **HTMX + Alpine + uPlot + MapLibre** | No build step, tiny, fast |
| DB | SQLite → **TimescaleDB** | Start simple, scale when needed |
| Telemetry | **Prometheus + Grafana** | Standard |
| Transport | **WireGuard** | Only outbound path |

### 53.2 Rejected

| Option | Why rejected |
|---|---|
| OpenBTS | Archived, 2G only |
| OpenAirInterface | Heavy, brittle, no advantage here |
| Magma | Operator-shaped, too much machinery |
| Free5GC | Fine, but Open5GS has better 4G support and simpler config |
| YateBTS | 2G only |

### 53.3 Version pinning

```text
srsRAN_Project   pinned by commit
Open5GS          pinned by commit
UHD              pinned to the version matching the FPGA image
pycrate          pinned by tag
Python           3.11 exactly
```

Pin everything. Upstream breaks upstream regularly.

---

## 54. Base Build

### 54.1 Host OS

Debian 12 minimal. Read-only rootfs via overlayfs, `/var` and `/etc` writable.

```bash
apt update && apt install -y --no-install-recommends \
  build-essential cmake ninja-build git pkg-config \
  libuhd-dev uhd-host libmbedtls-dev libsctp-dev libyaml-cpp-dev \
  libboost-program-options-dev libconfig++-dev \
  python3.11 python3.11-venv sqlite3 tshark dumpcap \
  wireguard-tools prometheus-node-exporter
usermod -aG wireshark "$USER"
uhd_images_downloader
```

### 54.2 Open5GS

```bash
git clone https://github.com/open5gs/open5gs && cd open5gs
git checkout <PINNED_COMMIT>
meson build --prefix=/usr && ninja -C build && sudo ninja -C build install
sudo systemctl enable --now open5gs-mmed open5gs-sgwud open5gs-smfd \
  open5gs-amfd open5gs-upfd open5gs-nrfd open5gs-scpd \
  open5gs-ausfd open5gs-udmd open5gs-udrd open5gs-pcfd open5gs-nssfd open5gs-bsfd
```

### 54.3 GTP kernel module

```bash
git clone https://github.com/open5gs/gtp5g.git && cd gtp5g
make && sudo make install && sudo depmod -a && sudo modprobe gtp5g
```

### 54.4 srsRAN_Project

```bash
git clone https://github.com/srsran/srsRAN_Project && cd srsRAN_Project
git checkout <PINNED_COMMIT>
mkdir build && cd build
cmake .. -DENABLE_EXPORT=ON -DENABLE_ZEROMQ=OFF -DCMAKE_BUILD_TYPE=Release
make -j"$(nproc)" && sudo make install
sudo ./srsran_install_configs.sh service
```

### 54.5 UHD image

```bash
sudo uhd_images_downloader -t n3xx
uhd_find_devices
uhd_usrp_probe | grep -i ref_locked
```

`ref_locked: Yes` before anything else.

---

## 55. Radio Configuration

### 55.1 Core PLMN and security

`/etc/open5gs/amf.yaml`:

```yaml
amf:
  ngap:
    addr: 10.20.0.10
  guami:
    - plmn_id: { mcc: "310", mnc: "260" }
      amf_id: { region: 2, set: 1, pointer: 1 }
  tai:
    - plmn_id: { mcc: "310", mnc: "260" }
      tac: 4242
  plmn_support:
    - plmn_id: { mcc: "310", mnc: "260" }
      s_nssai:
        - { sst: 1 }
  security:
    integrity_order: [ NIA2, NIA1, NIA0 ]
    ciphering_order: [ NEA0 ]
  security:
    suci:
      null_scheme: true
  network_name: { full: "TestNet", short: "Test" }
```

`/etc/open5gs/mme.yaml`, same pattern for LTE with `ciphering_order: [ EEA0 ]` and `tai`/`plmn_support` matching.

### 55.2 gNB

`/etc/srsran/gnb.yml`, key sections. **Field names track upstream; verify against the release you pinned.**

```yaml
cu_cp:
  amf:
    addr: 10.20.0.10
    port: 38412
    bind_addr: 10.20.0.20
  supported_tracking_areas:
    - tac: 4242
      plmn_list:
        - plmn: "310260"
          tai_slice_support_list:
            - sst: 1

ru_sdr:
  device_driver: uhd
  device_args: type=n3xx,addr=10.20.0.30,clock=external
  srate: 92.16
  tx_gain: 60
  rx_gain: 50

cell_cfg:
  dl_arfcn: 632628        # n78, centre 3500 MHz
  band: 78
  channel_bandwidth_MHz: 100
  common_scs: 30
  plmn: "310260"
  pci: 42
  tac: 4242
  pdcch:
    common:
      ss0_index: 0
  pdsch:
    mcs_table: qam64
  prach:
    prach_config_index: 159
```

For LTE, use `srsRAN_4G` `enb.conf` with `dl_earfcn`, `n_prb`, `mcc`/`mnc`, and `cipher_algo = EEA0`.

### 55.3 Gain staging

Start `tx_gain: 40`, `rx_gain: 40`. Raise TX until the test UE attaches within 20 s at 5 m, then back off 3 dB. Raise RX until noise floor rise on key-up reaches 1 dB, then back off 3 dB.

### 55.4 Verify

```bash
sudo srsran_gnb -c /etc/srsran/gnb.yml
# second terminal
sudo tshark -i <ngap_if> -f "sctp port 38412" -Y "ngap"
```

A test UE with a provisioned SIM should reach `InitialUEMessage`. Provision it:

```bash
sudo open5gs-dbctl add 310260000000001 \
  465B5CE8B199B49FAA5F0A2EE238A6BC E8ED289DEBA952E4283B54E88E6183CA
```

---

## 56. Stealth Layer

Stealth is a set of behaviours, not a setting. Each one is a trade-off.

| Technique | Implementation | Cost |
|---|---|---|
| **Passive-first** | Survey SDR listens 60 s before any key-up; abort if the target band is busy | Slower to collect |
| **Minimum power** | Start 10 dB below the local serving cell, ramp in 1 dB steps | Smaller footprint |
| **Valid PCI** | Survey, pick from the operator's own PCI range, avoid neighbours | Needs the survey |
| **Neighbour TAC clone** | Use a real neighbour's TAC so the update looks routine | Handsets may not update at all |
| **Fresh TAC** | Unused value, forces update | Every handset in range churns |
| **Short dwell** | 30–120 s bursts, then withdraw | Incomplete sessions |
| **Well-formed SIBs** | Disable SIBs you do not need; match the operator's SIB scheduling | Config effort |
| **Timing discipline** | GNSSDO mandatory for NR | Hardware cost |
| **Low-profile antenna** | 3 dBi omni, indoors behind glass | Range |
| **Plain enclosure** | No branding, matte black | Nothing |
| **No outbound except VPN** | WireGuard only, DNS via tunnel | Latency |
| **Cipher downgrade** | EEA0 / NEA0 | **EEA0 is itself a tell** |
| **Withdraw cleanly** | Stop gNB, wait for reattach, verify | Time |

### 56.1 The cipher trade-off

Null cipher gives you plaintext but announces you. A device with network notifications enabled will report "unencrypted network." Choose per mission:

- **Harvesting, undetected:** leave ciphering on, accept metadata only.
- **Intercept, willing to be seen:** force EEA0/NEA0.

### 56.2 Withdrawal sequence

```mermaid
flowchart LR
    A["Stop gNB"] --> B["Wait 60 s"]
    B --> C["Confirm test UE back on real cell"]
    C --> D["Confirm neighbour RSCP within 2 dB of baseline"]
    D --> E["Log delta, close session"]
```

---

## 57. Decoding Pipeline

### 57.1 Capture

```bash
dumpcap -i ngap0 -f "sctp port 38412" \
  -b filesize:262144 -b files:50 -w /srv/cap/ngap.pcapng
dumpcap -i s1u0 -f "udp port 2152" \
  -b filesize:262144 -b files:50 -w /srv/cap/gtpu.pcapng
```

Hash on close, timestamp, move to evidence store. Part III §30.

### 57.2 Identity extraction

```bash
tshark -r ngap.pcapng -Y "ngap.InitialUEMessage" -T ek \
  | jq -c 'select(.ngap) | {
      ts: .timestamp,
      imsi: .ngap.InitialUEMessage.rrc_SetupRequest?,
      gnb: .ngap.InitialUEMessage.gNB_UE_NGAP_ID
    }'
```

NAS decode for 5GMM:

```bash
tshark -r ngap.pcapng -Y "nas-5gs" -V
```

### 57.3 Python decode with pycrate

```python
from pycrate_mobile.NAS5G import parse_NAS5G

def decode_nas5g(payload_hex: str) -> dict:
    msg = parse_NAS5G(bytes.fromhex(payload_hex))
    msg.show()
    return {
        "type": msg.get_msg_type(),
        "imsi": _extract_suci_or_supi(msg),
        "ue_caps": msg.get_UE_Capability() if hasattr(msg, "get_UE_Capability") else None,
    }
```

`scat` (France Telecom) also decodes NGAP and 5G NAS from pcap and is worth installing as a cross-check.

### 57.4 Worker shape

```python
# workers/decoder.py
import asyncio, hashlib
from pathlib import Path

async def watch(capdir: Path, sink):
    seen = set()
    while True:
        for p in sorted(capdir.glob("*.pcapng")):
            if p in seen or p.with_suffix(".done").exists():
                continue
            for rec in await extract(p):
                await sink(rec)
            p.with_suffix(".done").write_text(hashlib.sha256(p.read_bytes()).hexdigest())
            seen.add(p)
        await asyncio.sleep(2)
```

### 57.5 Decoder coverage

| Layer | Tool | Output |
|---|---|---|
| NGAP / S1AP | tshark, scat | Identity, cause, UE IDs |
| NAS 5GMM / EMM | pycrate, tshark | Identity, capability, APN |
| RRC | tshark, pycrate | Band, PCI, timing advance |
| SIB | tshark | Cell parameters as seen by the UE |
| GTP-U | tshark | Flow metadata, byte counts |

---

## 58. Data Model and Storage

```sql
CREATE TABLE session (
  id            TEXT PRIMARY KEY,     -- uuidv4
  started_utc   TEXT NOT NULL,
  ended_utc     TEXT,
  band          INTEGER,
  arfcn         INTEGER,
  pci           INTEGER,
  tac           INTEGER,
  plmn          TEXT,
  cipher        TEXT,                 -- NEA0 | NEA2 | EEA0 | ...
  site          TEXT,
  prev_hash     TEXT,
  rec_hash      TEXT NOT NULL
);

CREATE TABLE observation (
  id            INTEGER PRIMARY KEY,
  session_id    TEXT REFERENCES session(id),
  ts_utc        TEXT NOT NULL,
  kind          TEXT NOT NULL,        -- attach | identity_req | auth | detach | sms | pdu
  imsi          TEXT,
  suci          TEXT,
  imei          TEXT,
  imeisv        TEXT,
  rat           TEXT,
  ta            INTEGER,
  cause         TEXT,
  raw_hex       TEXT,
  confidence    TEXT NOT NULL         -- A | B | C | D
);

CREATE INDEX idx_obs_imsi ON observation(imsi);
CREATE INDEX idx_obs_ts   ON observation(ts_utc);
```

`rec_hash` chains over `prev_hash` so deletion is visible. `confidence` per Part I §14.3.

TimescaleDB when the row count passes about 10 million: convert `observation` to a hypertable on `ts_utc`.

---

## 59. API and GUI

### 59.1 API surface

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/sessions` | List, filter by date, band, site |
| GET | `/api/sessions/{id}` | Detail with observations |
| GET | `/api/observations` | Filter by IMSI, kind, time |
| GET | `/api/observations/stream` | WebSocket, live tail |
| POST | `/api/sessions` | Open a session |
| POST | `/api/sessions/{id}/close` | Close, seal hash |
| GET | `/api/cells` | Seen cells with first/last |
| GET | `/api/export/{fmt}` | CSV, JSON, pcap |
| GET | `/api/health` | Watchdog endpoint |
| GET | `/api/plugins` | List loaded plugins |

```python
# api/main.py
from fastapi import FastAPI, WebSocket
app = FastAPI()

@app.get("/api/health")
async def health():
    return {"ok": True, "gnss": ref_locked(), "temp_c": read_temp()}

@app.websocket("/api/observations/stream")
async def stream(ws: WebSocket):
    await ws.accept()
    async for rec in bus.subscribe():
        await ws.send_json(rec)
```

### 59.2 GUI

Single page, four panes: live observations, session list, cell map, charts. HTMX for refresh, Alpine for state, uPlot for time series, MapLibre for geography.

- **Live table:** time, kind, IMSI, RAT, cause. Newest at top, 500 rows.
- **Session list:** click to load, right-click to export.
- **Map:** cell positions from survey or CellMapper, colour by RAT.
- **Charts:** attach rate, dwell time, RAT mix.

```html
<div hx-get="/api/observations?limit=500" hx-trigger="every 2s" hx-swap="innerHTML">
  <!-- rows -->
</div>
```

Big text, high contrast, works at 1280×800. Operators use this in a car.

---

## 60. Telemetry and Charts

| Metric | Type | Alert |
|---|---|---|
| `gnss_ref_locked` | gauge | 0 for 30 s |
| `gnss_sats` | gauge | `< 6` |
| `pa_temp_c` | gauge | `> 70` |
| `sdr_temp_c` | gauge | `> 85` |
| `tx_forward_w` | gauge | Outside ±10% |
| `rx_noise_rise_db` | gauge | `> 1` |
| `ue_attach_total` | counter | Rate 0 for 10 min while transmitting |
| `pcap_gap_seconds` | gauge | `> 60` |
| `disk_free_pct` | gauge | `< 15` |

Charts worth building, in order: attach rate over time, RAT mix, dwell-time histogram, per-band success rate, identity-request latency distribution, thermal trend.

```yaml
# prometheus.yml
scrape_configs:
  - job_name: platform
    static_configs: [{ targets: ["localhost:8000"] }]
```

Grafana dashboards as JSON in the repository, provisioned, not hand-made.

---

## 61. Carrier Profile System

Profiles are data, not code. One YAML per operator per country.

```yaml
# profiles/us/tmo.yml
operator: T-Mobile US
mcc: "310"
mnc: "260"
bands:
  - { band: 2,  arfcn: 900,   bw: 20, scs: 15 }
  - { band: 4,  arfcn: 2050,  bw: 20, scs: 15 }
  - { band: 12, arfcn: 5110,  bw: 10, scs: 15 }
  - { band: 41, arfcn: 40440, bw: 20, scs: 15 }
  - { band: 71, arfcn: 68586, bw: 20, scs: 15 }
  - { band: 78, arfcn: 632628, bw: 100, scs: 30 }
pci_range: [ 1, 503 ]
tac_strategy: neighbour_clone
cipher_policy: preserve
notes: |
  n41 and n71 are the volume bands. n78 is thin.
  PCI reuse is aggressive; survey before key-up.
```

| Field | Meaning |
|---|---|
| `bands` | Candidate ARFCN and bandwidth, ranked |
| `pci_range` | Legal range for this operator |
| `tac_strategy` | `neighbour_clone`, `fresh`, or `from_ue` |
| `cipher_policy` | `preserve` or `force_null` |
| `notes` | Human context |

Loader validates against a JSON Schema, checks band/ARFCN consistency, and refuses profiles where the ARFCN does not map to the declared band.

---

## 62. Update and Plugin System

### 62.1 Updates

```bash
sudo platform-update --check          # list available
sudo platform-update --to <tag>       # apply
sudo platform-update --rollback       # revert
```

`--to` does: snapshot config, pull tag, build, run smoke tests (T1, T5, T7, T14), switch symlink, restart, verify health, and roll back automatically if any smoke test fails.

Never update in the field without a rollback path and a known-good tag.

### 62.2 Plugins

```python
# plugins/example_lac_tracker.py
NAME = "lac_tracker"
VERSION = "1.0.0"
SCHEMA = 2

def on_observation(obs: dict, ctx) -> dict | None:
    ctx.state.setdefault("lac", {})
    if obs.get("kind") == "attach":
        ctx.state["lac"][obs["imsi"]] = obs.get("tac")
    return None

def on_export(rows: list[dict]) -> list[dict]:
    return rows
```

Hooks: `on_session_open`, `on_observation`, `on_session_close`, `on_export`, `on_ui`.

Rules: plugins declare a schema version, run in-process with a timeout, cannot write to the DB directly (they return rows), and are disabled by default when they throw twice in a minute.

---

## 63. Deployment Form Factors

| Form | Content | Runtime | Notes |
|---|---|---|---|
| **Bench** | N310 or B210, host, mains | Indefinite | Development |
| **Case** | N310, PA, filters, host, 20 Ah | 3–4 h | Battery per §37 sizing |
| **Vehicle** | Case + roof mag-mount + inverter | Engine on | Split-charge per §37 |
| **Backpack** | B210, 10 W, host, 10 Ah | 1.5 h | Weight matters more than power |
| **Fixed indoor** | N310, window omni, mains | Continuous | Best stealth |
| **Drone** | B210, host, 5 Ah | 20 min | Weight, heat, no mast |

**Vehicle notes.** Mag-mount on the roof, cable through a door seal with a drip loop, host in the footwell, inverter fused at the battery. Power spec per §37.

**Drone notes.** Every 100 g is a minute of flight. Use B210 not N310. Heatsink exposed to prop wash. Land before 30% battery.

---

## 64. Test and Validation

| # | Test | Pass |
|---|---|---|
| V1 | Cold boot to service | `< 90 s` |
| V2 | GNSS lock | `< 120 s` |
| V3 | Profile validation rejects bad band/ARFCN | Refused with reason |
| V4 | Attach, provisioned UE | `< 15 s` |
| V5 | Identity logged with confidence grade | Present |
| V6 | Decoder handles malformed pcap | No crash |
| V7 | Hash chain detects deletion | Detected |
| V8 | Export CSV/JSON/pcap | Valid, complete |
| V9 | Plugin timeout kills a hung plugin | Killed, logged |
| V10 | Update rollback on failed smoke test | Rolls back |
| V11 | Thermal soak 60 min | `≤ 55 °C` internal |
| V12 | Withdrawal, all UEs return | `< 60 s` |
| V13 | 24 h soak, no gap > 60 s | No gap |
| V14 | Port scan | Expected ports only |
| V15 | Rebuild from repo on clean host | Identical |

V13 is the one that finds the bugs you will otherwise find in the field.

---

## 65. Cost Summary

| Build | Components | Total |
|---|---|---|
| **Minimum viable (4G only, bench)** | B210 $1,500 · host $400 · GNSSDO $200 · PA $400 · filters $300 · antennas $200 · case $150 · cabling $150 · power $250 | **~$3,550** |
| **Recommended (4G/5G, case)** | N310 $7,000 · rest as above · 20 Ah LiFePO4 $300 | **~$9,050** |
| **Field-ready (vehicle)** | Recommended + mag-mount $250 · inverter $300 · survey SDR $500 | **~$10,100** |
| **Fixed indoor** | Recommended + window mounts $100 | **~$9,150** |

**Not included:** labour, spectrum authority, survey time, calibration instruments, spares, insurance.

**Cost per capability.** Roughly $1,500 buys 4G metadata. $7,000 buys 5G FR1. $10,000 buys mobility. Nothing buys VoLTE intercept.

---

## 66. Honest Limits

- **No VoLTE.** CS fallback or nothing. This is the largest single gap and it is not closeable in this scope.
- **No user-plane decryption.** Metadata and identity only.
- **Not type-approved.** Spurious emissions are your problem. Part IV §44 T9 exists because of this.
- **USB SDRs are fragile.** B210 on a vehicle build will eventually drop out. N310 exists for a reason.
- **Timing is the hardest part.** NR without a GNSSDO does not work. Indoors, without sky view, NR mostly does not work.
- **SUCI.** A UE provisioned against your core sends SUPI under null scheme. A UE provisioned against its real operator sends SUCI you cannot read unless you hold the key. For unknown handsets, bid down to LTE.
- **Decode coverage is partial.** Vendor NAS variants, proprietary IEs and encryption at higher layers will defeat the pipeline in places.
- **Stealth is relative.** A determined observer with a scanner will find you. Minimum power, short dwell and valid parameters make it take longer.
- **Legal position is local.** Experimental provisions, tolerance limits and notification duties vary enormously. Check before transmitting.
- **One operator at a time.** Multi-operator simultaneous collection means multi-radio and multi-host.
- **The GUI is not a product.** It is a working surface. Expect to modify it.
- **Plugin isolation is in-process.** A malicious plugin can reach the host. Timeouts stop hangs, not escapes.

---

# Back matter

## Consolidated references index

**Standards and specifications**

3GPP TS 23.003 · TS 33.102 · TS 33.107 · TS 33.108 · TS 33.401 · TS 33.501 · TS 36.133 · TS 38.300 · TS 43.020 · TS 45.002 · TS 45.008 · TR 33.899 · GSMA FS.11 · FS.19 · IR.88 · ETSI TS 101 671 · NIST SP 800-187 · IETF RFC 3161 · RFC 8493 · ITU-T E.212 · FCC OET-65 · ICNIRP 2020.

**Open-source software**

Osmocom (osmocom.org) · srsRAN_Project · srsRAN_4G · Open5GS · gtp5g · Free5GC · Magma · OpenAirInterface · YateBTS · gr-gsm · Oros42/IMSI-catcher · OsmocomBB · kalibrate-rtl · LimeSuite · bladeRF · UHD · SoapySDR · GNU Radio · SnoopSnitch · AIMSICD · KrakenSDR DOA · pycrate · scat · Wireshark/tshark/dumpcap · Kamailio · FreeSWITCH · Asterisk · bagit-python · hashdeep · OpenSSL · auditd · syslog-ng · QGIS · SPLAT! · Radio Mobile · CellMapper · OpenCellID · FreeTSA · tcpreplay · MinIO · Grafana · Prometheus · FastAPI · uPlot · MapLibre.

**Hardware**

Ettus N310 · N321 · B210 · LimeSDR Mini 2.0 · LimeSDR USB · bladeRF 2.0 micro xA4 · xA9 · ADALM-PLUTO · AntSDR E200 · HackRF One · RTL-SDR Blog V4 · KrakenSDR · ThinkRF R5500 · R5750 · Signal Hound SM200B · Aaronia Spectran V6 · R&S TSMA6 · TSME6 · Leo Bodnar GNSSDO · u-blox NEO-M8T.

**Commercial platforms**

L3Harris Stingray II · KingFish · Hailstorm · Crossbow · Septier IBS · Interceptor · LightRay · Parsons DRT · PKI Phantom · CellXion · Sunwave · BLiNQ · Airspan · R&S ROMES · QualiPoc · Keysight Nemo · Anritsu · Accuver XCAL · VIAVI.

**Research and reporting**

SUCI-catcher work (2021–2023) · 5G identity concealment measurement studies · A5/1 rainbow-table literature · baseband CVE disclosures · Android Advanced Protection and IMSI-catcher notification announcements (Android 16) · Apple Lockdown Mode documentation · Harris/Stingray NDA reporting.

**Citation grading.** Apply Part I §14.3. Vendor capability claims are D-grade until reproduced. Prices are indicative bands from 2026 and will drift. Anything in this document marked E-grade should be re-verified before use in a procurement record.




