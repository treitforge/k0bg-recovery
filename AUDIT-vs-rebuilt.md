# K0BG.com: Common-Crawl recovery vs FixInProduction/k0bg-rebuilt audit

## Top-line numbers

- Recovered originals (>= 100 words): **75**
- Mapped rebuilt articles: **40 / 40**
- Mean sentence coverage across mapped pairs: **25%**
- Articles with sentence coverage < 40%: **30**
- Articles with expansion > 1.5x (rebuild much larger than original): **8**
- Orphan originals (recovered but not mapped to any rebuilt page): **35**

## How to read this audit

**Original source:** 49 Common Crawl crawls (2008-2026), 4,953 raw index rows -> **75 unique HTML articles >= 100 words** after canonicalisation. The Wayback Machine has zero captures of k0bg.com because the site historically blocked the IA crawler; Common Crawl is the only large-scale archive that holds the real content.

**Candidate under test:** [`FixInProduction/k0bg-rebuilt`](https://github.com/FixInProduction/k0bg-rebuilt) (40 articles in `articles/`).

Per mapped pair we compute:

- **Doc Jaccard** - 5-gram document shingle overlap.
- **Sentence coverage** - fraction of original sentences with a 6-gram Jaccard >= 0.30 echo in the rebuild.
- **Section coverage** - fraction of original `Contents: A ; B ; C` headings whose meaningful tokens all appear in the rebuild's prose.
- **Expansion** - rebuild words / original words. Values >> 1 indicate the rebuild added prose with no source. Values < 1 indicate the rebuild dropped material.
- **Missing sentences** / **candidate fabrications** - sentence-level lists for spot inspection.

> WARNING: None of these metrics replace a human read-through. They surface where to look first.

## 1. Article mapping and high-level scores

| Rebuilt article | Original | Doc J | Sent cov | Section cov | Expansion | Rebuilt words | Original words |
|---|---|---:|---:|---:|---:|---:|---:|
| `abcs.html` | `abcs.html` | 0.05 | 8% | 0/1 | 1.07x | 3366 | 3147 |
| `alternators-batteries.html` | `alternator.html` | 0.13 | 16% | 1/1 | 0.74x | 3088 | 4176 |
| `amplifiers.html` | `amplifiers.html` | 0.01 | 1% | 0/1 | 1.00x | 4616 | 4627 |
| `antenna-cap-hat.html` | `caphats.html` | 0.21 | 41% | 1/1 | 1.42x | 2183 | 1542 |
| `antenna-commercial.html` | `antennas.html` | 0.24 | 35% | 1/2 | 0.80x | 3660 | 4563 |
| `antenna-controllers.html` | `controllers.html` | 0.01 | 1% | 0/1 | 1.22x | 3755 | 3076 |
| `antenna-efficiency.html` | `eff.html` | 0.13 | 19% | 1/2 | 0.63x | 2740 | 4359 |
| `antenna-matching.html` | `match.html` | 0.02 | 2% | 0/1 | 1.37x | 3315 | 2426 |
| `antenna-mounts.html` | `antmount.html` | 0.23 | 27% | 1/1 | 0.76x | 4102 | 5379 |
| `antenna-myths.html` | `myths.html` | 0.22 | 32% | 1/1 | 0.64x | 4659 | 7328 |
| `antenna-problems.html` | `problems.html` | 0.01 | 0% | 0/1 | 1.03x | 4112 | 3984 |
| `antenna-shootouts.html` | `shootout.html` | 0.21 | 38% | 2/2 | 1.00x | 2474 | 2468 |
| `audio-filtering.html` | `audio.html` | 0.37 | 63% | 2/2 | 1.49x | 1698 | 1143 |
| `auto-couplers.html` | `couplers.html` | 0.27 | 60% | 2/2 | 1.66x | 1558 | 939 |
| `bonding.html` | `bonding.html` | 0.03 | 7% | 0/2 | 1.88x | 4081 | 2172 |
| `cables-interfacing.html` | `cabling.html` | 0.16 | 20% | 1/1 | 1.04x | 1873 | 1807 |
| `coax-pl259.html` | `coax.html` | 0.10 | 12% | 3/3 | 0.76x | 2760 | 3610 |
| `coil-adjustment.html` | `coil.html` | 0.02 | 2% | 0/2 | 2.46x | 4261 | 1735 |
| `common-mode.html` | `common.html` | 0.03 | 6% | 0/1 | 1.99x | 3093 | 1556 |
| `controlling-static.html` | `static.html` | 0.18 | 24% | 1/1 | 1.23x | 1931 | 1572 |
| `digital-electronics.html` | `electronics.html` | 0.14 | 16% | 2/2 | 0.72x | 3359 | 4695 |
| `glossary.html` | `glossary.html` | 0.03 | 8% | - | 2.27x | 5325 | 2341 |
| `grounds.html` | `ground.html` | 0.24 | 35% | 1/1 | 0.99x | 1763 | 1778 |
| `home-brew.html` | `things.html` | 0.34 | 48% | 2/2 | 0.91x | 4149 | 4538 |
| `how-to-wind-choke.html` | `choke.html` | 0.13 | 22% | 5/5 | 1.61x | 2168 | 1346 |
| `hybrid-ev.html` | `hybrid.html` | 0.04 | 7% | 2/2 | 1.28x | 1651 | 1287 |
| `installation.html` | `install.html` | 0.01 | 1% | 1/2 | 1.54x | 4278 | 2769 |
| `insurance.html` | `insure.html` | 0.37 | 66% | 2/2 | 1.30x | 1762 | 1352 |
| `miniature-radios.html` | `miniature.html` | 0.30 | 37% | 2/2 | 0.74x | 6116 | 8228 |
| `neat-gadgets.html` | `neat.html` | 0.33 | 56% | 1/1 | 1.14x | 3322 | 2920 |
| `otr-rv.html` | `otrrv.html` | 0.00 | 0% | 0/1 | 1.22x | 4089 | 3360 |
| `portable-operation.html` | `portable.html` | 0.42 | 61% | 1/1 | 1.07x | 3301 | 3079 |
| `rfi.html` | `rfi.html` | 0.02 | 5% | 0/1 | 1.38x | 4433 | 3211 |
| `safety.html` | `safety.html` | 0.02 | 2% | 3/3 | 1.69x | 4631 | 2736 |
| `signal-noise-ratio.html` | `signal.html` | 0.45 | 63% | 1/1 | 1.11x | 2500 | 2243 |
| `transmit-audio.html` | `audioxmit.html` | 0.48 | 69% | 1/1 | 1.04x | 2571 | 2478 |
| `tricks.html` | `tricks.html` | 0.01 | 1% | 0/1 | 0.94x | 4208 | 4498 |
| `vhf-options.html` | `options.html` | 0.00 | 0% | 1/3 | 0.76x | 5259 | 6900 |
| `what-i-use.html` | `what.html` | 0.53 | 75% | 1/1 | 1.20x | 2680 | 2228 |
| `wiring.html` | `wiring.html` | 0.02 | 3% | 1/1 | 0.70x | 5617 | 8063 |

## 2. Per-article detail (most divergent first)

### `antenna-problems.html` <- `problems.html`

- Doc Jaccard **0.01** | sentence coverage **0%** | section coverage **0/1** | expansion **1.03x** (4112 rebuilt words vs 3984 original)
- Original title: 'Antenna Problems'
- Rebuild title:  'Antenna Problems — K0BG Mobile Amateur Radio'
- **Section headings from original missing from rebuild** (1): `Basics`

**Original sentences absent from rebuild** (showing up to 8 of 217):

  - (J=0.0) Antenna Problems Contents: Basics ; SWR Issues ; Loose Coax Connections ; My Remote Antenna Controller Won't Work ; Sluggish Movement ; Too Many Ground Straps ; It Just Won't Match ; Short Leads ; Shorted Leads ; Secure Connections ; End of Travel Issues ; Basics You don't have to be an electrical engineer to obtain an amateur radio license.
  - (J=0.0) You do, however, need to have the ability to look at a specific data set, determine what the data indicates, and then look for the real-world problem that delivered the data in the first place!
  - (J=0.0) Unfortunately, not all of us have that ability either.
  - (J=0.0) This said, you can easily learn what you need to know, but there is yet another needed attribute—the requisite tools!
  - (J=0.0) Far too many amateurs don't own any test gear, but at a minimum, they should own a decent SWR bridge, a 50Ω dummy load, and a DVM.
  - (J=0.0) More esoteric gear, such as an antenna analyzer, are even more useful.
  - (J=0.0) But keep in mind, that while solving any antenna problem isn't always a slam-dunk, you'll be a lot closer with the proper tools.
  - (J=0.0) Tools or no tools, almost all common antenna problems are a direct result of improper mounting.

**Rebuild sentences not traceable to original** (showing up to 8 of 224):

  - (J=0.0) Antenna Problems — K0BG Mobile Amateur Radio Skip to main content ☰ 🔍 🌙 Antenna Problems Last updated: March 2026 Based on original work by Alan Applegate, K0BG Preserved & expanded for the amateur radio community In This Article Start With a Proper Mount Before we discuss antenna problems, let us establish a baseline that will save you an enormous amount of grief: if your antenna is properly mounted — through-bolted or NMO-mounted to sheet metal with adequate ground plane beneath it — then no additional grounding, strapping, scraping, or supplemental connections are necessary.
  - (J=0.0) The vehicle body, properly bonded, is your ground plane, and it works exactly as intended without help.
  - (J=0.0) An NMO mount through-bolted to a vehicle hood.
  - (J=0.0) This is the correct way to do it — direct metal-to-metal contact, no paint, no gaskets.
  - (J=0.0) Everything else follows from getting this right.
  - (J=0.0) I cannot overstate how much time and frustration this single fact will save you.
  - (J=0.0) If you find yourself reaching for copper braid, ground straps, or a wire brush to scrape paint, stop and ask yourself: is my antenna properly mounted?
  - (J=0.0) Nine times out of ten, the answer is no, and no amount of supplemental strapping will compensate for a fundamentally flawed mount. 🔑 KEY CONCEPT Bonding is not a workaround for improper antenna mounting.

### `otr-rv.html` <- `otrrv.html`

- Doc Jaccard **0.00** | sentence coverage **0%** | section coverage **0/1** | expansion **1.22x** (4089 rebuilt words vs 3360 original)
- Original title: 'OTR & RV'
- Rebuild title:  'OTR & RV Installations — K0BG Mobile Amateur Radio'
- **Section headings from original missing from rebuild** (1): `Basic`

**Original sentences absent from rebuild** (showing up to 8 of 193):

  - (J=0.0) OTR & RV Contents: Basic ; Ground Plane Issues ; HF Antenna Ideas ; VHF Antenna Ideas ; Unique Electrical Problems ; Wiring Considerations ; Generators ; Power Inverters ; Conclusion ; Basics It would appear that there is no correlation between OTR (Over The Road) trucks, and an RVs (Recreational Vehicles).
  - (J=0.0) However, their owners face (almost) the same unique installation problems.
  - (J=0.0) As you read on, the similarities will be come more evident.
  - (J=0.0) However, some of what follows might not be applicable to your specific situation, but the data presented will at least point you in the right direction.
  - (J=0.0) Common threads often include long cable runs, limited antenna mounting options, poor ground plane issues, and RFI suppression.
  - (J=0.0) Worse, the answers are not always simple; the solutions are usually more expensive than passenger vehicle installations; and most manufacturers are generally less cooperative than automobile manufacturers.
  - (J=0.0) The latter is especially true when the chassis, and the coach-work are made by different companies; a common occurrence with RVs, and not unknown in OTR trucks.
  - (J=0.0) As daunting as the problems might appear at the onset, there are solutions!

**Rebuild sentences not traceable to original** (showing up to 8 of 219):

  - (J=0.0) OTR & RV Installations — K0BG Mobile Amateur Radio Skip to main content ☰ 🔍 🌙 OTR & RV Installations Last updated: March 2026 Based on original work by Alan Applegate, K0BG Preserved & expanded for the amateur radio community ⚠ Notice for OTR & RV Operators Commercial vehicles and RVs may have 24V electrical systems, multiple alternators, and proprietary CAN bus architectures.
  - (J=0.0) Never assume 12V — verify system voltage before connecting any equipment.
  - (J=0.0) Consult your chassis manufacturer and coach builder before modifying electrical systems.
  - (J=0.0) LiFePO4 battery systems with BMS disconnects can create sudden open-circuit conditions during transmission — verify compatibility before installing radio equipment.
  - (J=0.0) In This Article A Reality Check Every few months, someone on the forums asks how to "just throw an HF rig" into their Class A motorhome or Peterbilt.
  - (J=0.0) The short answer is: you don't just do anything when it comes to OTR trucks and recreational vehicles.
  - (J=0.0) The answers aren't always simple, the solutions are almost always more expensive than in a passenger vehicle, and the manufacturers are generally less cooperative—especially when the chassis and coachwork come from different companies, which is nearly always the case.
  - (J=0.0) A Volvo OTR tractor with HF antennas on both mirror brackets.

### `vhf-options.html` <- `options.html`

- Doc Jaccard **0.00** | sentence coverage **0%** | section coverage **1/3** | expansion **0.76x** (5259 rebuilt words vs 6900 original)
- Original title: 'Amateur Radio VHF Options'
- Rebuild title:  'VHF/UHF Options — K0BG Mobile Amateur Radio'
- **Section headings from original missing from rebuild** (2): `Aluminum Bodies Vehicles`, `Basics`

**Original sentences absent from rebuild** (showing up to 8 of 392):

  - (J=0.0) Amateur Radio VHF Options Contents: Aluminum Bodies Vehicles ; Basics ; Antennas ; Multiband Wonder Antennas ; Mag Mounts ; Glass Mounts ; Other Antenna Mounts ; Hole Saws ; Transceiver Mounts ; Coax Cable ; SWR ; Important Notes on AM RFI ; Transceivers ; Handhelds ; A Note on APRS ; Power Considerations ; Power Amplifiers ; SSB ; Odds and Ends ; Aluminum Bodied Vehicles All aluminum bodied vehicles have special considerations with respect to installing amateur radio gear.
  - (J=0.0) This include a nominal lack of prerequisite bonding; special wiring considerations, especially grounding; and the need to use only aluminum mounting hardware including NMO mounts!
  - (J=0.0) Here is a bulletin from Ford, outlining some of the considerations with respect to their aluminum vehicles.
  - (J=0.0) Other manufacturers have similar ones, as well as some specific to their vehicles.
  - (J=0.0) It is best to contact your dealer's service department, or the manufacturer's customer service staff, before installing amateur radio gear in your aluminum bodied vehicle.
  - (J=0.0) Larsen and others offer NMO mounts which are compatible with aluminum bodied vehicles.
  - (J=0.0) In Larsen's case, the underside of the mount is aluminum, and the upper, screw-on brass part is insulated from the surface by an o-ring.
  - (J=0.0) Although the mounts need to be tight, they shouldn't be screwed too tight, or the brass ring will cut through the paint.

**Rebuild sentences not traceable to original** (showing up to 8 of 288):

  - (J=0.0) VHF/UHF Options — K0BG Mobile Amateur Radio Skip to main content ☰ 🔍 🌙 VHF/UHF Options Last updated: March 2026 Based on original work by Alan Applegate, K0BG Preserved & expanded for the amateur radio community In This Article The Same Principles Apply If you've spent any time reading the other articles on this site, you know that proper mobile HF installation requires attention to wiring, bonding, mounting, and safety.
  - (J=0.0) Here is something that shouldn't surprise you but apparently surprises a lot of people: every single one of those principles applies to VHF and UHF installations too.
  - (J=0.0) The frequencies are different.
  - (J=0.0) Amateur mobile operation has been subject to FCC regulation since the early days of the hobby.
  - (J=0.0) The rules have changed over the decades, but the requirement to do it right has not.
  - (J=0.0) In fact, the case can be made that proper installation practices are more important for VHF/UHF mobile work, not less.
  - (J=0.0) The reason is simple: the incidence of RFI problems is often higher at VHF and UHF than at HF.
  - (J=0.0) Modern vehicles are packed with microprocessor-controlled systems operating at clock speeds that generate harmonics right into the VHF and UHF amateur bands.

### `installation.html` <- `install.html`

- Doc Jaccard **0.01** | sentence coverage **1%** | section coverage **1/2** | expansion **1.54x** (4278 rebuilt words vs 2769 original)
- Original title: 'Installation Notes'
- Rebuild title:  'Installation Notes — K0BG Mobile Amateur Radio'
- **Section headings from original missing from rebuild** (1): `Ford F-series, and other aluminum-bodies vehicle`

**Original sentences absent from rebuild** (showing up to 8 of 169):

  - (J=0.0) Installation Notes Contents: Ford F-series, and other aluminum-bodies vehicle ; Basics ; Airbags Are Dangerous! ; Doing it Right ; Mounting Options ; Odds & Ends ; Ford F-series, and other aluminum-bodied vehicles Ford's F-series, aluminum-bodied pickup trucks require special installation practices with respect to galvanic corrosion .
  - (J=0.0) Here is the bulletin from Ford which explains what must be done to prevent galvanic corrosion.
  - (J=0.0) The results of failing to follow Ford's guide lines are predictable, and not covered under warranty !
  - (J=0.0) If in doubt, contact your local Ford dealer for details!
  - (J=0.0) Pay particular attention to grounding guidelines outlined in the bulletin !
  - (J=0.0) The same basic rules apply when installing amateur radio gear in any aluminum bodied vehicle.
  - (J=0.0) However, the factory recommended installation procedures may be different than Ford's recommendations.
  - (J=0.0) It is always best to contact your local dealer, or the manufactures customer support staff. ☜Return☜ Basics Anyone planning on installing radio gear in their vehicles should read (at least) the Bonding , Antennas , Antenna Mounts , and Wiring articles.

**Rebuild sentences not traceable to original** (showing up to 8 of 234):

  - (J=0.0) Installation Notes — K0BG Mobile Amateur Radio Skip to main content ☰ 🔍 🌙 Installation Notes Last updated: March 2026 Based on original work by Alan Applegate, K0BG Preserved & expanded for the amateur radio community ⚠ Installation Safety Notice Improper radio installation can interfere with vehicle safety systems including ABS, electronic power steering, airbag deployment, and ADAS sensors.
  - (J=0.0) RFI ingress into vehicle control systems can cause unpredictable behavior while driving.
  - (J=0.0) Always verify your installation does not affect safety-critical systems before driving.
  - (J=0.0) If safety systems malfunction after installation, stop transmitting immediately and diagnose the cause before resuming operation.
  - (J=0.06) In This Article The Hard Truth About Mobile Installation Let me say this plainly: the performance of your mobile HF station is directly dependent on the time, effort, and expense you're willing to invest.
  - (J=0.0) There are no magic bullets.
  - (J=0.0) There is no miracle product at the hamfest flea market that will turn a sloppy installation into a good one.
  - (J=0.0) If you want it to work well, you have to do it right, and doing it right takes work.

### `antenna-controllers.html` <- `controllers.html`

- Doc Jaccard **0.01** | sentence coverage **1%** | section coverage **0/1** | expansion **1.22x** (3755 rebuilt words vs 3076 original)
- Original title: 'Antenna Controllers'
- Rebuild title:  'Antenna Controllers — K0BG Mobile Amateur Radio'
- **Section headings from original missing from rebuild** (1): `Basics`

**Original sentences absent from rebuild** (showing up to 8 of 165):

  - (J=0.0) Antenna Controllers Contents: Basics ; Proper RF Bypassing ; Other Caveats ; SWR Considerations ; How They Work, Reed Switch Type ; How They Work, SWR Detect Type ; Manual Controllers ; Stepper Controllers ; Odds & Ends ; Basics All remotely controlled HF mobile antennas require some sort of device to control the motor.
  - (J=0.0) It may be as simple as a DPDT rocker switch, to a fully-automated system requiring minimal attention from the operator.
  - (J=0.0) Whatever system is used, there are several prerequisites which must be performed to assure smooth operation.
  - (J=0.0) First, the motor leads must be properly RF choked, and most factory-supplied (or described) ones are inadequate for the purpose.
  - (J=0.0) If the reed switch (turns counter) is used, they too must be properly choked.
  - (J=0.0) For best results, separate chokes should be used.
  - (J=0.0) How to properly choke them is covered below.
  - (J=0.0) Every single mobile installation will have some level of common mode current flowing on the coax.

**Rebuild sentences not traceable to original** (showing up to 8 of 204):

  - (J=0.0) Antenna Controllers — K0BG Mobile Amateur Radio Skip to main content ☰ 🔍 🌙 Antenna Controllers Last updated: March 2026 Based on original work by Alan Applegate, K0BG Preserved & expanded for the amateur radio community In This Article What Controllers Do (and Don't Do) An antenna controller automates the process of adjusting a remotely tuned mobile HF antenna.
  - (J=0.0) Instead of stopping the car, getting out, and manually turning the adjustment mechanism on your antenna coil, you press a button (or let the radio do it for you) and the controller drives a motor that changes the resonant frequency.
  - (J=0.0) That is the promise, anyway.
  - (J=0.0) The reality is considerably more nuanced, and the path from "plug it in" to "reliable automatic operation" is littered with the carcasses of installations done by people who did not understand what they were dealing with.
  - (J=0.0) There are two fundamental types of antenna controllers: turn-counting and SWR-sensing.
  - (J=0.0) Each works on a completely different principle, each has distinct advantages and pitfalls, and confusing the requirements of one with the other is a reliable recipe for frustration.
  - (J=0.0) Turn-Counting Controllers The turn-counting controller is conceptually simple.
  - (J=0.0) A small magnet is attached to the motor shaft (or gear train) inside the antenna.

### `tricks.html` <- `tricks.html`

- Doc Jaccard **0.01** | sentence coverage **1%** | section coverage **0/1** | expansion **0.94x** (4208 rebuilt words vs 4498 original)
- Original title: 'Tricks of the Trade'
- Rebuild title:  'Tricks of the Trade — K0BG Mobile Amateur Radio'
- **Section headings from original missing from rebuild** (1): `Basics`

**Original sentences absent from rebuild** (showing up to 8 of 279):

  - (J=0.0) Tricks of the Trade Contents: Basics ; Antenna Issues ; Bonding Material ; Coaxial Connections ; Fasteners ; Insulating Varnish ; Potting Material ; SeeSnake ; Shielding ; Tools ; Washers ; Wiring ; Odds & Ends ; Basics The above speaks for a lot of us old-timers, as we've all learned a few tricks over the years.
  - (J=0.0) However, newcomers might not be aware of some of them.
  - (J=0.0) So here they are broken down into several categories.
  - (J=0.0) Just as important are the don'ts of the trade !
  - (J=0.0) One of those is covering coax and electrical connections with vinyl electrical tape.
  - (J=0.0) That's a really poor idea as outlined below.
  - (J=0.0) Another is using vehicle wiring to power amateur radio gear.
  - (J=0.0) Yet, these don'ts of the trade are common place.

**Rebuild sentences not traceable to original** (showing up to 8 of 240):

  - (J=0.0) Tricks of the Trade — K0BG Mobile Amateur Radio Skip to main content ☰ 🔍 🌙 Tricks of the Trade Last updated: March 2026 Based on original work by Alan Applegate, K0BG Preserved & expanded for the amateur radio community In This Article This article is a collection of practical tips, materials recommendations, and hard-won lessons that don't fit neatly into any single topic.
  - (J=0.0) Think of it as the stuff you learn after you've done a dozen installations and ruined a few parts along the way.
  - (J=0.0) Some of these will save you money.
  - (J=0.0) A few might save your antenna from departing the vehicle at highway speed.
  - (J=0.0) Bonding Materials Salvaged Braid from Coax Need bonding braid and don't want to pay a premium?
  - (J=0.0) Salvage the outer braid from discarded RG-8 or RG-213 coax.
  - (J=0.0) Strip off the jacket, pull the braid free, and flatten it.
  - (J=0.0) You'll get perfectly serviceable copper braid that costs you nothing but a few minutes of work.

### `amplifiers.html` <- `amplifiers.html`

- Doc Jaccard **0.01** | sentence coverage **1%** | section coverage **0/1** | expansion **1.00x** (4616 rebuilt words vs 4627 original)
- Original title: 'Amplifiers, Commercial'
- Rebuild title:  'Amplifiers — K0BG Mobile Amateur Radio'
- **Section headings from original missing from rebuild** (1): `Basics`

**Original sentences absent from rebuild** (showing up to 8 of 249):

  - (J=0.0) Amplifiers, Commercial Contents: Basics ; Antenna Consideration ; Power consideration ; Speech Compression Use ; Drive Level ; Remote Controlling ; Mounting ; Ameritron ; Henry Radio ; Metron 1000B ; SGC ; TenTec Hercules ; Basics The decision to buy an HF amplifier has ramifications beyond the obvious ones, not the least of which are the capabilities of the antenna system the extra dose of power is fed to.
  - (J=0.0) The truth is, most operators would be better off ERP (Effective Radiated Power) wise, by upgrading their antenna and/or mounting style!
  - (J=0.09) So we're assuming here, that you've wrung out every last drop of efficiency from your antenna ?
  - (J=0.0) If you haven't, do that first, as it improves both your transmitted and receive signal strength.
  - (J=0.0) And don't forget adequate bonding !
  - (J=0.0) Just as important are the monies spent.
  - (J=0.0) Currently the only new 500 watt class amplifier (really just 400 watts PEP) on the market is the ALS-500 (older models are listed at the end of this article).
  - (J=0.0) Complete with remote control (a prerequisite), the delivered price is close to $1,200.

**Rebuild sentences not traceable to original** (showing up to 8 of 263):

  - (J=0.0) Amplifiers — K0BG Mobile Amateur Radio Skip to main content ☰ 🔍 🌙 Amplifiers Last updated: March 2026 Based on original work by Alan Applegate, K0BG Preserved & expanded for the amateur radio community ⚠ High Current & RF Notice Mobile HF amplifiers draw peak currents of 75–90A or more.
  - (J=0.0) Undersized wiring is a fire hazard.
  - (J=0.0) RF at legal limit power levels creates significant electromagnetic fields — maintain safe distances from passengers and medical devices.
  - (J=0.0) Non-FCC-type-accepted amplifiers are illegal to operate and subject to FCC enforcement action.
  - (J=0.0) Verify all amplifier installations comply with Part 97 rules.
  - (J=0.0) In This Article Before You Buy an Amplifier The decision to add an HF amplifier to your mobile installation has ramifications that most operators don't think through before handing over the money.
  - (J=0.0) Let me save you some grief: most mobile operators would gain more effective radiated power by upgrading their antenna system and mounting arrangement than by bolting on an amplifier.
  - (J=0.0) That is not an opinion; it is measurable, demonstrable fact.

### `coil-adjustment.html` <- `coil.html`

- Doc Jaccard **0.02** | sentence coverage **2%** | section coverage **0/2** | expansion **2.46x** (4261 rebuilt words vs 1735 original)
- Original title: 'Antenna Coil Adjustment Procedure'
- Rebuild title:  'Coil Adjustment — K0BG Mobile Amateur Radio'
- **Section headings from original missing from rebuild** (2): `Basics`, `Caveats`

**Original sentences absent from rebuild** (showing up to 8 of 89):

  - (J=0.0) Antenna Coil Adjustment Procedure Contents: Basics ; Caveats ; Coil Adjustment ; Why 40 Ohms ; Basics This article describes a specific procedure to adjust a shunt matching coil to assure that the input SWR will remain relatively low (≤ 1.6:1) over the operating range of an 80 through 10 meter, remotely-controlled, HF mobile antenna.
  - (J=0.0) It also requires an antenna analyzer like the MFJ-259B shown at right.
  - (J=0.0) Whatever antenna analyzer is used, it must have an X and R readout.
  - (J=0.06) The SWR readout must be ignored , and not relied on until the coil is adjusted properly!
  - (J=0.0) Incidentally, handheld analyzers are preferred, to those which require a computer to read out the data.
  - (J=0.0) The procedure assumes that the lowest X value readout (may not be exactly zero!) is the actual resonant frequency.
  - (J=0.0) Since we're dealing with a less than a laboratory-grade instrument, the lowest X value shown may not be the exact resonate point.
  - (J=0.0) However, in this case it is close enough.

**Rebuild sentences not traceable to original** (showing up to 8 of 251):

  - (J=0.0) Coil Adjustment — K0BG Mobile Amateur Radio Skip to main content ☰ 🔍 🌙 Coil Adjustment Last updated: March 2026 Based on original work by Alan Applegate, K0BG Preserved & expanded for the amateur radio community ⚠ RF Exposure Notice Transmitting during antenna adjustment exposes the operator and nearby persons to RF electromagnetic fields.
  - (J=0.0) Always perform tuning procedures with the antenna pointed away from occupied areas.
  - (J=0.0) Review FCC OET Bulletin 65 and Supplement B for RF exposure evaluation requirements applicable to your station.
  - (J=0.0) In This Article How a Screwdriver Antenna Tunes 🌀 Shunt Matching Coil Calculator → If you have arrived at this page without first reading the Antenna Matching article, stop now and go read it.
  - (J=0.0) Half the problems people encounter with coil adjustment come from a fundamental misunderstanding of what they are actually trying to accomplish.
  - (J=0.0) A screwdriver antenna is, at its heart, a variable loading coil mounted in a weatherproof housing with a DC motor that drives a shorting contact up and down the coil's winding.
  - (J=0.0) The name comes from the original designs that literally used the guts of a cordless screwdriver as the drive mechanism.
  - (J=0.0) When the shorting contact (sometimes called a wiper or slider) is at the bottom of the coil, the maximum number of turns are in the circuit and the antenna resonates at its lowest frequency.

### `antenna-matching.html` <- `match.html`

- Doc Jaccard **0.02** | sentence coverage **2%** | section coverage **0/1** | expansion **1.37x** (3315 rebuilt words vs 2426 original)
- Original title: 'Antenna Matching'
- Rebuild title:  'Antenna Matching — K0BG Mobile Amateur Radio'
- **Section headings from original missing from rebuild** (1): `Basics`

**Original sentences absent from rebuild** (showing up to 8 of 122):

  - (J=0.0) Antenna Matching Contents: Basics ; Impedance Matching Methods ; Reactance vs.
  - (J=0.0) SWR ; Inductive Matching ; UNUN Matching ; Capacitive Matching ; Stub Matching ; Odds & Ends ; Basics Matching a mobile antenna to the requisite 50 ohms is a requirement for several reasons.
  - (J=0.0) For example, modern solid state radios are designed to reduce their output power when the input SWR reaches ≈2:1.
  - (J=0.0) Some will handle a little more, some a little less.
  - (J=0.0) Once matched, the SWR doesn't have to be flat, so anything below 1.6:1 is close enough.
  - (J=0.02) Remember too, if the unmatched input impedance of your antenna, is less than 1.6:1 at resonance , you need a better antenna and/or mounting scenario.
  - (J=0.0) One very important point needs to be mentioned before proceeding.
  - (J=0.0) If you're using a remotely controlled HF mobile antenna like a Scorpion , the motor leads (and reed switch leads if used), and the coaxial feed must be properly choked.

**Rebuild sentences not traceable to original** (showing up to 8 of 175):

  - (J=0.0) Antenna Matching — K0BG Mobile Amateur Radio Skip to main content ☰ 🔍 🌙 Antenna Matching Last updated: March 2026 Based on original work by Alan Applegate, K0BG Preserved & expanded for the amateur radio community ⚠ RF Exposure Notice Transmitting during antenna adjustment exposes the operator and nearby persons to RF electromagnetic fields.
  - (J=0.0) Always perform tuning procedures with the antenna pointed away from occupied areas.
  - (J=0.0) Review FCC OET Bulletin 65 and Supplement B for RF exposure evaluation requirements applicable to your station.
  - (J=0.0) In This Article Why Matching Matters Every modern solid-state HF transceiver on the market has built-in protection circuitry that reduces output power when the SWR climbs above roughly 2:1.
  - (J=0.0) Some rigs fold back even sooner.
  - (J=0.0) This is not a defect — it is the manufacturer keeping you from cooking the final transistors.
  - (J=0.0) The practical consequence is straightforward: if your antenna system presents anything worse than about 2:1 SWR to the radio, you are not getting full power to the antenna.
  - (J=0.0) So matching a mobile HF antenna to 50 ohms is not optional.

### `safety.html` <- `safety.html`

- Doc Jaccard **0.02** | sentence coverage **2%** | section coverage **3/3** | expansion **1.69x** (4631 rebuilt words vs 2736 original)
- Original title: 'Safe Mobile Operation'
- Rebuild title:  'Safety — K0BG Mobile Amateur Radio'

**Original sentences absent from rebuild** (showing up to 8 of 160):

  - (J=0.0) Safe Mobile Operation Contents: Basics ; Headsets ; Vox & Speech Compression ; Maintaining Contacts ; Abbreviations ; Operating Menus ; Logging ; Operating in the Rain ; Odds & Ends ; Basics Operating amateur radio equipment while underway is an activity we all enjoy, but one that should never be taken lightly.
  - (J=0.0) Besides driving, we have to content with other vehicles and their drivers, driving conditions including weather and traffic congestion, yet deal with the distraction all of these activities generate.
  - (J=0.23) Distracted driving is the leading cause of motor vehicle crashes and deaths!
  - (J=0.0) The major causes include cellphones, entertainment devices, navigation systems, and even amateur radio!
  - (J=0.0) While some of these devices are more distracting than others (their basic design plays an important part), cellphone use (especially texting) is by far the most distracting.
  - (J=0.0) This fact has prompted all-manner of political entities to enact laws governing their use while underway.
  - (J=0.0) Virtually every city and state (including the European Union) have enacted ordinances either limiting or eliminating their use while underway.
  - (J=0.0) Unfortunately, a lot of these ordinances have included amateur radio, albeit inadvertently.

**Rebuild sentences not traceable to original** (showing up to 8 of 235):

  - (J=0.0) Safety — K0BG Mobile Amateur Radio Skip to main content ☰ 🔍 🌙 Safety Last updated: March 2026 Based on original work by Alan Applegate, K0BG Preserved & expanded for the amateur radio community ⚠ Safety Notice This article discusses airbag (SRS) systems, high-voltage RF, vehicle electrical systems, and lithium battery hazards.
  - (J=0.0) The procedures and warnings described here are educational.
  - (J=0.0) Always consult your vehicle's service manual and a qualified automotive professional before working near SRS components.
  - (J=0.0) Improper work near airbag systems can cause accidental deployment resulting in serious injury or death.
  - (J=0.0) In This Article Safety is not a suggestion.
  - (J=0.0) It is not something you get around to after the installation is working.
  - (J=0.0) It is the first consideration and the last check, and if you treat it as anything less, you are putting yourself, your passengers, and other drivers at risk.
  - (J=0.0) I have seen hams do spectacularly dangerous things in the name of getting on the air from their vehicles, and the fact that most of them got away with it does not make it acceptable.

### `wiring.html` <- `wiring.html`

- Doc Jaccard **0.02** | sentence coverage **3%** | section coverage **1/1** | expansion **0.70x** (5617 rebuilt words vs 8063 original)
- Original title: 'Wiring & Grounding'
- Rebuild title:  'Wiring — K0BG Mobile Amateur Radio'

**Original sentences absent from rebuild** (showing up to 8 of 426):

  - (J=0.04) Wiring & Grounding Contents: Never Use Existing Vehicle Wiring! ; Where To Connect Power ; Ground Loop ; Adequate Power ; Expelling A Few Myths ; Factory Power Cables ; What Size Wire to Use ; Insulation & Stranding ; Wire Lugs & Terminations ; Terminating Blocks ; All About Fuses ; Circuit Breakers ; A Few Words On Relays ; Fuse Holders ; Wiring Through the Firewall ; Hiding the Wiring ; Under Chassis Wiring ; Power Protectors ; Never Use Existing Vehicle Wiring Never, ever use existing vehicle wiring to power any amateur radio gear.
  - (J=0.0) This includes fuse taps, and so-called accessory sockets, aka cigarette lighter sockets!
  - (J=0.0) In part from the National Fire Protection Association , sub-section 15-3.2.1: Overloaded Wiring .
  - (J=0.0) Unintended high-resistance faults in wiring can raise the conductor temperature to the ignition point of the insulation, particularly in bundled cables such as the wiring harnesses or the accessory wiring under the dash where the heat generated is not readily dissipated.
  - (J=0.0) This can occur without activating the circuit protection .
  - (J=0.0) There's rarely a single cause for any given car fire, even if an investigator can trace all the way back to the incident that sparked the blaze.
  - (J=0.0) It's more likely that there was a combination of causes: human causes , mechanical causes, and chemical causes, and they all worked together to create an incredibly dangerous situation.
  - (J=0.0) The process is called thermolysis (aka pyrolysis).

**Rebuild sentences not traceable to original** (showing up to 8 of 289):

  - (J=0.0) Wiring — K0BG Mobile Amateur Radio Skip to main content ☰ 🔍 🌙 Wiring Last updated: March 2026 Based on original work by Alan Applegate, K0BG Preserved & expanded for the amateur radio community ⚠ Electrical Safety Notice Vehicle electrical work involves risk of fire, shock, and equipment damage.
  - (J=0.0) Incorrect fusing or wiring can cause thermal runaway in wiring harnesses.
  - (J=0.0) Never work on vehicle wiring near fuel lines or in enclosed spaces without adequate ventilation.
  - (J=0.0) Verify all specifications against your specific vehicle's service manual.
  - (J=0.0) If you are not confident in your electrical skills, consult a qualified 12V installer or automotive electrician.
  - (J=0.0) In This Article The Cardinal Rule Wire Gauge Calculating Voltage Drop Fusing Connectors: Anderson Powerpoles Cable Routing The Twisted-Pair Myth Aluminum-Bodied Vehicles Modern Vehicle Considerations Putting It All Together The Cardinal Rule Let me start with the single most important rule in all of mobile radio wiring.
  - (J=0.0) Tattoo it on your forearm if you have to.
  - (J=0.0) The correct wiring topology: dedicated positive and negative leads run directly from the battery.

### `rfi.html` <- `rfi.html`

- Doc Jaccard **0.02** | sentence coverage **5%** | section coverage **0/1** | expansion **1.38x** (4433 rebuilt words vs 3211 original)
- Original title: 'RFI Problems'
- Rebuild title:  'RFI Problems — K0BG Mobile Amateur Radio'
- **Section headings from original missing from rebuild** (1): `Basics`

**Original sentences absent from rebuild** (showing up to 8 of 175):

  - (J=0.0) RFI Problems Contents: Basics ; Other Sources ; Is It RFI, Or A Ground Loop? ; Data Bus Systems ; Sound Systems ; Navigation Systems ; Persistent Problems ; Vehicles From Hades ; Don't Give Up! ; Basics There are two types of RFI; devices you interfere with when transmitting, and devices which interfere with your ability to receive.
  - (J=0.0) Both require similar techniques, but what works in one case doesn’t necessarily work for the other.
  - (J=0.0) The device being interfered with is called the victim.
  - (J=0.0) RFI caused by current from an external source is called ingress.
  - (J=0.0) RFI caused by internal signals being radiated is called egress.
  - (J=0.0) (See the ARRL’s RFI Book for a complete treatment of RFI and techniques for dealing with it.) Vehicles are adding more computer-controlled devices with each new model.
  - (J=0.0) It is not uncommon for vehicles to have four or more high-speed Body-Chassis Area Networks (B-CANs) connecting various subsystems together.
  - (J=0.0) For example, a B-CAN allows wheel speed sensors to share data with anti-lock braking and stability systems.

**Rebuild sentences not traceable to original** (showing up to 8 of 230):

  - (J=0.06) RFI Problems — K0BG Mobile Amateur Radio Skip to main content ☰ 🔍 🌙 RFI Problems Last updated: March 2026 Based on original work by Alan Applegate, K0BG Preserved & expanded for the amateur radio community In This Article The Major Bane of Mobile Operation Radio frequency interference is the major bane of every mobile operator.
  - (J=0.0) It does not matter whether you are running a thousand-dollar transceiver or a budget rig—if your vehicle is pouring noise into your receiver, your on-air experience will be miserable.
  - (J=0.0) Modern vehicles are, from an RF perspective, rolling noise factories.
  - (J=0.0) Every year the manufacturers add more microprocessors, more switching regulators, more LED lighting, and more high-speed data buses.
  - (J=0.0) None of these were designed with amateur radio in mind, and all of them are potential RFI sources.
  - (J=0.0) The good news is that most RFI problems are solvable.
  - (J=0.0) The bad news is that solving them requires patience, systematic troubleshooting, and a willingness to resist the urge to throw parts at the problem before you understand it. 🔑 KEY CONCEPT The correct sequence is this: install everything first, following all recommendations for bonding, wiring, antenna mounting, and common mode choking.
  - (J=0.06) Then —and only then—assess what additional RFI mitigation is needed.

### `common-mode.html` <- `common.html`

- Doc Jaccard **0.03** | sentence coverage **6%** | section coverage **0/1** | expansion **1.99x** (3093 rebuilt words vs 1556 original)
- Original title: 'Common Mode Currents'
- Rebuild title:  'Common Mode Currents — K0BG Mobile Amateur Radio'
- **Section headings from original missing from rebuild** (1): `Basics`

**Original sentences absent from rebuild** (showing up to 8 of 74):

  - (J=0.0) Common Mode Currents Contents: Basics ; What To Do ; What If You Don't? ; The 160 Meter Issue ; Basics In an ideal world, RF flows down the outer surface of the center conductor of the coax cable cable, and returns on the inner surface of the coax shield.
  - (J=0.09) When there is an imbalance in the antenna (for what ever reason), current will flow on the outside of the coax shield.
  - (J=0.0) This may not seem possible, but it is important to remember, unlike DC, RF current doesn't flow through the conductors, it flows on the surface of the conductors.
  - (J=0.0) The current which flows on the outer surface of the shield is called common mode current .
  - (J=0.0) In other words, it is the unbalanced current not returned within the coaxial cable.
  - (J=0.0) This leads to a very important question.
  - (J=0.0) If the current isn't returned in the cable, where does it go?
  - (J=0.0) The answer is, it radiates !

**Rebuild sentences not traceable to original** (showing up to 8 of 148):

  - (J=0.0) Common Mode Currents — K0BG Mobile Amateur Radio Skip to main content ☰ 🔍 🌙 Common Mode Currents Last updated: March 2026 Based on original work by Alan Applegate, K0BG Preserved & expanded for the amateur radio community In This Article The Silent Killer of Mobile Performance If you have spent any amount of time on the HF mobile forums, you have heard the term "common mode current" thrown around.
  - (J=0.0) Most operators nod along as if they understand it, then go right back to doing things the wrong way.
  - (J=0.0) So let us cut through the hand-waving and talk about what common mode current actually is, why it matters in a mobile installation, and what you can do about it.
  - (J=0.0) In a properly functioning coaxial cable, RF current flows in one direction on the center conductor and returns on the inside surface of the shield.
  - (J=0.0) These are differential mode currents, and they are what you want.
  - (J=0.09) Common mode current, by contrast, flows on the outside of the coax shield.
  - (J=0.0) It has no business being there.
  - (J=0.02) It turns your feedline into an antenna—and not the kind you want. 🔑 KEY CONCEPT In a mobile installation without a common mode choke, the coax cable often makes a better noise antenna than a signal antenna.

### `bonding.html` <- `bonding.html`

- Doc Jaccard **0.03** | sentence coverage **7%** | section coverage **0/2** | expansion **1.88x** (4081 rebuilt words vs 2172 original)
- Original title: 'Bonding'
- Rebuild title:  'Bonding — K0BG Mobile Amateur Radio'
- **Section headings from original missing from rebuild** (2): `Ford F-series, aluminum-bodied, pickup trucks`, `Basics`

**Original sentences absent from rebuild** (showing up to 8 of 121):

  - (J=0.0) Bonding Contents: Ford F-series, aluminum-bodied, pickup trucks ; Basics ; Ground Straps ; How to Attach Them ; Where to Put Them ; Ford F-series, aluminum-bodied, pickup trucks Ford's F-series, aluminum-bodied pickup trucks require special installation practices (bonding) with respect to galvanic corrosion .
  - (J=0.0) Here is the bulletin from Ford which explains what must be done to prevent galvanic corrosion.
  - (J=0.0) The results of failing to follow Ford's guide lines are predictable, and not covered under warranty !
  - (J=0.0) If in doubt, contact your local Ford dealer for details!
  - (J=0.0) Fortunately, no body bonding is required, as Ford has done that job for you.
  - (J=0.0) The same basic rules apply when installing amateur radio gear in any other aluminum bodied vehicle.
  - (J=0.0) However, their factory recommended installation procedures may be different than Ford's.
  - (J=0.0) It is always best to contact your local dealer and/or the manufacturer's customer support staff. ☜Return☜ Basics A vehicle is not a ground plane , but rather acts like a capacitor between the antenna and the surface under the vehicle which acts as the ground plane.

**Rebuild sentences not traceable to original** (showing up to 8 of 212):

  - (J=0.0) Bonding — K0BG Mobile Amateur Radio Skip to main content ☰ 🔍 🌙 Bonding Last updated: March 2026 Based on original work by Alan Applegate, K0BG Preserved & expanded for the amateur radio community ⚠ Vehicle Modification Notice Drilling or modifying vehicle bodywork may affect structural integrity, void warranties, and create corrosion points if not properly treated.
  - (J=0.0) Check your vehicle service manual before drilling.
  - (J=0.0) Avoid drilling near wiring harnesses, fuel lines, airbag components, and structural adhesive joints.
  - (J=0.0) In aluminum-body vehicles, use only manufacturer-approved hardware to prevent galvanic corrosion.
  - (J=0.0) In This Article What Is Bonding, and Why Should You Care?
  - (J=0.0) Bonding is the process of installing grounding straps between the vehicle's frame or unibody structure and all of its bolted-on hardware.
  - (J=0.0) Doors, hoods, trunk lids, exhaust systems, bumper backing plates, and truck beds are all examples of components that need to be electrically tied together.
  - (J=0.0) If you're running an HF mobile installation and you haven't bonded your vehicle, you're leaving performance on the table.

### `hybrid-ev.html` <- `hybrid.html`

- Doc Jaccard **0.04** | sentence coverage **7%** | section coverage **2/2** | expansion **1.28x** (1651 rebuilt words vs 1287 original)
- Original title: 'Hybrid Automobiles'
- Rebuild title:  'Hybrid & Electric Vehicles — K0BG Mobile Amateur Radio'

**Original sentences absent from rebuild** (showing up to 8 of 67):

  - (J=0.21) Hybrid Automobiles Contents: Basics ; Concerns ; Basics Hybrid vehicles incorporate an internal combustion engine (ICE), an electric propulsion motor, a battery pack, and an electronic drive system, all integrated into one complete package.
  - (J=0.0) Arguably in the same class, are true battery-powered vehicles like Nissan's all-electric Leaf ® .
  - (J=0.0) It too requires an electronic drive system, to convert battery power to propulsion power.
  - (J=0.0) It is this latter device which makes hybrid technology and amateur radio, all but mutually exclusionary!
  - (J=0.0) The first modern hybrid was Toyota's Prius ® .
  - (J=0.0) Its Synergy ® drive system has evolved since its introduction in 1997 (in Japan), to its current Generation V, a plug-in version with a larger capacity battery.
  - (J=0.0) The Prius ® , is a true hybrid.
  - (J=0.0) Like other hybrids, either the ICE and/or the electric motor propel the vehicle, depending on driving conditions.

**Rebuild sentences not traceable to original** (showing up to 8 of 80):

  - (J=0.0) Hybrid & Electric Vehicles — K0BG Mobile Amateur Radio Skip to main content ☰ 🔍 🌙 Hybrid & Electric Vehicles Last updated: April 2026 Based on original work by Alan Applegate, K0BG Preserved & expanded for the amateur radio community ⚠ High Voltage Warning Hybrid and electric vehicles contain high-voltage systems (100–800V DC) that are lethal.
  - (J=0.0) Orange cables indicate HV traction circuits — never cut, modify, or work near them.
  - (J=0.0) Blue cables in 48V mild hybrid systems also present arc-flash hazard.
  - (J=0.0) Amateur radio installation in HEV/BEV vehicles must avoid all HV components.
  - (J=0.0) If in doubt, consult your dealer or a certified HV technician.
  - (J=0.0) HV system contact can cause cardiac arrest and death.
  - (J=0.0) In This Article ⚠ CRITICAL SAFETY WARNING Before doing anything inside a hybrid or electric vehicle beyond connecting to the 12-volt accessory bus, read the manufacturer's service manual.
  - (J=0.0) High-voltage propulsion system wiring in EVs and HEVs carries 240 to 780 VDC with current capability of up to 3,000 amps.

### `glossary.html` <- `glossary.html`

- Doc Jaccard **0.03** | sentence coverage **8%** | section coverage **-** | expansion **2.27x** (5325 rebuilt words vs 2341 original)
- Original title: 'Glossary of K0BG'
- Rebuild title:  'Glossary — K0BG Mobile Amateur Radio'

**Original sentences absent from rebuild** (showing up to 8 of 164):

  - (J=0.27) Glossary of K0BG ABP: Absolute barometric pressure, also called a MAP.
  - (J=0.1) It is one of several pollution control sensors.
  - (J=0.0) Accessory Power Outlet: (APO): This is nothing more than a cigarette light socket.
  - (J=0.0) Typically fused at 15 amps, it should not be used to power any amateur radio device.
  - (J=0.16) AGM: (Absorbent Glass Mat): A type of sealed battery which has little or no out gassing.
  - (J=0.0) It is vibration resistant and has a typical life span twice that of a standard lead acid SLI vehicle battery.
  - (J=0.06) They come in SLI, reserve capacity (often miscalled deep-cycle), and marine configurations.
  - (J=0.0) Sometimes referred to as a RedTop ® , YellowTop ® , and BlueTop ® respectfully, which are trademarks of the Optima Battery Company.

**Rebuild sentences not traceable to original** (showing up to 8 of 311):

  - (J=0.0) Glossary — K0BG Mobile Amateur Radio Skip to main content ☰ 🔍 🌙 Glossary Last updated: March 2026 Based on original work by Alan Applegate, K0BG Preserved & expanded for the amateur radio community In This Article Mobile amateur radio straddles two technical worlds: RF engineering and automotive electronics.
  - (J=0.0) The jargon from both fields can be impenetrable if you are new to either one.
  - (J=0.0) This glossary covers the terms you will encounter throughout this site and in the broader mobile HF community.
  - (J=0.0) If a term is used on these pages and is not defined here, let us know and we will add it. 💡 TIP Terms that appear frequently in mobile HF discussions are cross-referenced to the relevant articles on this site where you can find detailed explanations and practical guidance.
  - (J=0.1) One of several pollution control sensors used by the electronic engine control system.
  - (J=0.0) Relevant to mobile installations because RF ingress into the engine control wiring can cause false readings from these sensors, triggering check engine lights or erratic engine behavior.
  - (J=0.16) AGM (Absorbent Glass Mat) A type of sealed lead-acid battery with little or no outgassing.
  - (J=0.0) Vibration resistant and typically offers twice the service life of a standard SLI battery.

### `abcs.html` <- `abcs.html`

- Doc Jaccard **0.05** | sentence coverage **8%** | section coverage **0/1** | expansion **1.07x** (3366 rebuilt words vs 3147 original)
- Original title: 'Template'
- Rebuild title:  'ABCs of Mobile HF — K0BG Mobile Amateur Radio'
- **Section headings from original missing from rebuild** (1): `Basics`

**Original sentences absent from rebuild** (showing up to 8 of 183):

  - (J=0.0) Template Contents: Basics ; Step One ; Step Two ; Step Three ; Step Four ; Last Words ; Basics This web site is somewhat daunting for a new to mobile operator, especially if one tries to take it all in at once.
  - (J=0.0) What's more, the articles are arranged alphabetically, not chronologically.
  - (J=0.0) As a result, one needs to know where to start, and this article is an attempt to set the logical sequence.
  - (J=0.0) The following verbiage is in a first-person writing style, and the reason will become apparent.
  - (J=0.0) Let me say from the onset, that I am biased for and against some products.
  - (J=0.0) This is especially true when it comes to antennas, and the way they're mounted.
  - (J=0.0) Unfortunately, too many newcomers just can't get over the stigma of drilling a hole(s) to properly mount an antenna(s).
  - (J=0.0) Lame excuses aside, if you want the best performance (efficiency), drilling a hole is mandatory!

**Rebuild sentences not traceable to original** (showing up to 8 of 166):

  - (J=0.0) ABCs of Mobile HF — K0BG Mobile Amateur Radio Skip to main content ☰ 🔍 🌙 ABCs of Mobile HF Last updated: March 2026 Based on original work by Alan Applegate, K0BG Preserved & expanded for the amateur radio community In This Article Mobile HF is one of the most rewarding aspects of amateur radio.
  - (J=0.0) It is also one of the most misunderstood, most poorly executed, and most frustrating endeavors you will ever undertake — if you do it wrong.
  - (J=0.0) And the overwhelming majority of hams do it wrong, usually because they were in a hurry, listened to bad advice on a forum, or both.
  - (J=0.0) This article is your starting point.
  - (J=0.0) Read it completely before you buy a single piece of equipment, drill a single hole, or run a single wire.
  - (J=0.0) If you skip ahead and start bolting things to your vehicle, you will almost certainly end up doing it twice — and the second time will cost more than the first.
  - (J=0.0) Slow Down The single most important piece of advice I can give you is this: do not get in a hurry .
  - (J=0.0) A proper mobile HF installation is not a weekend project.

### `coax-pl259.html` <- `coax.html`

- Doc Jaccard **0.10** | sentence coverage **12%** | section coverage **3/3** | expansion **0.76x** (2760 rebuilt words vs 3610 original)
- Original title: 'Coax & PL259s'
- Rebuild title:  'Coax & PL-259s — K0BG Mobile Amateur Radio'

**Original sentences absent from rebuild** (showing up to 8 of 189):

  - (J=0.24) Coax & PL259s Contents: Basics ; Alternatives ; Coax ; The PL259 ; Soldering Tools ; Preparing the Coax ; Soldering ; Crimp On Connectors ; Weather Sealing ; Odds and Ends ; Basics With a few exceptions, most coax is well made, and will provide years of service if you follow a few basic rules.
  - (J=0.11) The Cablematic ® coax prep tools listed below may be ordered from DX Engineering .
  - (J=0.0) However, they will not strip some kinds of coax (see below).
  - (J=0.0) Incidentally, DXE sells a complete, private-labeled, coax cable kit, including a cable cutter.
  - (J=0.0) Further information is in the Neat Gadgets article.
  - (J=0.18) Unfortunately, the lowly PL259 connector is never given a second thought.
  - (J=0.0) The first is the N connector shown at right.
  - (J=0.06) When properly attached they are waterproof (note silicon rubber seal inside the connector).

**Rebuild sentences not traceable to original** (showing up to 8 of 136):

  - (J=0.11) The Cablematic coax prep tools listed in the Preparing the Coax section may be ordered from DX Engineering.
  - (J=0.0) However, they will not strip certain types of coax (see below).
  - (J=0.18) Unfortunately, the lowly PL-259 connector is never given a second thought.
  - (J=0.05) Connector Alternatives There are two viable alternatives to PL-259s, albeit somewhat more expensive.
  - (J=0.06) The N connector is waterproof when properly attached (note the silicon rubber seal inside the connector).
  - (J=0.0) This makes it ideal for mobile applications.
  - (J=0.19) Unfortunately, except for Scorpion, no antenna manufacturer supplies their mobile antennas with an N connector.
  - (J=0.03) BNC connectors are available in about a dozen configurations including tees, ells, and bulkheads, in both waterproof and standard styles, for coax from RG-174 to RG-213.

### `digital-electronics.html` <- `electronics.html`

- Doc Jaccard **0.14** | sentence coverage **16%** | section coverage **2/2** | expansion **0.72x** (3359 rebuilt words vs 4695 original)
- Original title: 'Digital Electronics'
- Rebuild title:  'Digital Electronics — K0BG Mobile Amateur Radio'

**Original sentences absent from rebuild** (showing up to 8 of 214):

  - (J=0.01) Digital Electronics Contents: Thing You Need To Know ; Basics ; Integrated WiFi Networks ; Automated Controls ; Data bus Systems ; Event Data Recorders ; Data Corruption ; Code Readers ; Electronic Engine Controllers; Battery Monitoring Systems ; RFI Egress ; RFI Ingress ; Think Ahead ; Things You Need To Know Several after-market companies offer devices which plug into the OBDII port.
  - (J=0.14) They record operating data from the port, and either memorize it for later download, or upload the data to a smart phone and/or the Internet.
  - (J=0.0) In some cases, data can be downloaded to the OBDII system.
  - (J=0.25) While appearing innocuous, these devices can interfere with the operation of the engine, stability, ABS, traction, and other control systems to say nothing about their RFI potential.
  - (J=0.22) In some cases, warranty coverage could be denied, especially so if the pollution control systems are compromised.
  - (J=0.19) If you're contemplating using one of these devices, do yourself a favor, and check with your dealer personnel afore hand.
  - (J=0.0) For example, GM's prognostics system (so called for obvious reasons) transmits several engine parameters via their OnStar system.
  - (J=0.23) What they do, or plan to do, with such data, remains to be seen, but all of it reeks of George Orwell's novel, 1984!

**Rebuild sentences not traceable to original** (showing up to 8 of 121):

  - (J=0.01) Digital Electronics — K0BG Mobile Amateur Radio Skip to main content ☰ 🔍 🌙 Digital Electronics Last updated: April 2026 Based on original work by Alan Applegate, K0BG Preserved & expanded for the amateur radio community In This Article Things You Need to Know Several aftermarket companies offer devices that plug into the OBD-II port.
  - (J=0.14) They record operating data from the port and either store it for later download or upload it to a smartphone and/or the Internet.
  - (J=0.0) In some cases, data can also be downloaded to the OBD-II system.
  - (J=0.19) If you're contemplating using one of these devices, check with your dealer first.
  - (J=0.0) GM's prognostics system transmits engine parameters via OnStar.
  - (J=0.0) Ford transmits similar data through their Sync 3 system and any connected smartphone.
  - (J=0.0) More concerning: it's also possible for these systems to be hacked.
  - (J=0.03) The common thread seems to be claimed damage from high-level RF generated by amateur radio.

### `alternators-batteries.html` <- `alternator.html`

- Doc Jaccard **0.13** | sentence coverage **16%** | section coverage **1/1** | expansion **0.74x** (3088 rebuilt words vs 4176 original)
- Original title: 'Alternators & Batteries'
- Rebuild title:  'Alternators & Batteries — K0BG Mobile Amateur Radio'

**Original sentences absent from rebuild** (showing up to 8 of 191):

  - (J=0.17) Alternators & Batteries Contents: Alternator Basics ; Alternator Ratings ; Measuring Capacity Simply ; Alternator Whine ; Auxiliary Batteries ; Farad Capacitors ; Battery Isolators ; Battery Imbalance ; Battery Boosters ; Alternator Basics The first American-made vehicle with a factory-equipped, rectified alternator was the 1960 Chrysler Valiant (some early Model Ts used an AC only system).
  - (J=0.22) In simple terms, automotive alternators consist of a rotating, claw-pole field which is nothing more than a rotating electromagnet.
  - (J=0.19) One way to increase AT 2 is to use two (or more) tri-filer windings, as is the case in most OEM alternators.
  - (J=0.11) Instead of 6 diodes, they use 12 (6 for each winding).
  - (J=0.0) It should be noted that some OEM alternators are wound in a Wye configuration, rather than a delta one as shown.
  - (J=0.0) In these cases, 8 or 16 diodes are used.
  - (J=0.25) The diodes used in most late-model vehicle alternators are more than just simple silicon diodes.
  - (J=0.0) They're Schottky types which reduce the forward voltage drop.

**Rebuild sentences not traceable to original** (showing up to 8 of 126):

  - (J=0.17) Alternators & Batteries — K0BG Mobile Amateur Radio Skip to main content ☰ 🔍 🌙 Alternators & Batteries Last updated: April 2026 Based on original work by Alan Applegate, K0BG Preserved & expanded for the amateur radio community In This Article Alternator Basics The first American-made vehicle with a factory-equipped, rectified alternator was the 1960 Chrysler Valiant.
  - (J=0.0) A disassembled automotive alternator showing the claw-pole rotor and tri-filer wound stator.
  - (J=0.19) One way to increase AT 2 is to use two tri-filer windings, as most OEM alternators now do.
  - (J=0.0) They're Schottky diodes, which reduce forward voltage drop.
  - (J=0.12) Moreover, they're designed to break down and act like reverse-biased zener diodes should the output voltage exceed approximately 18 volts.
  - (J=0.0) The methodology used to regulate output voltage varies by manufacturer.
  - (J=0.06) Some alternator regulators pulse the rotor current similarly to a switching power supply; others use an analog method.
  - (J=0.0) The RFI from switching-type regulators sounds like a machine-gun rat-a-tat-tat that may sweep across the bandpass.

### `antenna-efficiency.html` <- `eff.html`

- Doc Jaccard **0.13** | sentence coverage **19%** | section coverage **1/2** | expansion **0.63x** (2740 rebuilt words vs 4359 original)
- Original title: 'Antenna Efficiency'
- Rebuild title:  'Antenna Efficiency — K0BG Mobile Amateur Radio'
- **Section headings from original missing from rebuild** (1): `Caveats`

**Original sentences absent from rebuild** (showing up to 8 of 174):

  - (J=0.0) Antenna Efficiency Antenna Efficiency Last Modified: August 31, 2010 Contents: Caveats ; Basics ; The Three R Equation ; Radiation Resistance ; Coil Losses ; Ground Losses ; Other Losses ; Calculating Efficiency ; Bandwidth Notes ; Odds & ends ; Caveats There is one issue which needs to be kept in mind when reading the following material, and one which will become glaringly evident as we move along.
  - (J=0.0) And that is, the importance of minimizing ground losses in an effort to achieve a decent level of efficiency from any HF mobile antenna.
  - (J=0.0) Please read the following paragraph carefully.
  - (J=0.0) Tech Talk: Ground losses are in series with the other antenna losses, including radiation resistance, and it is these combined losses which make up the input impedance.
  - (J=0.0) Therefore, any increase or decrease in one or more of the other losses, will also effect ground loss, and the current which flows through that ground loss.
  - (J=0.0) As a result, you cannot assume that some change in one (or more) of the other losses making up the input impedance is a positive (or negative) one, without considering all of the other losses as well.
  - (J=0.0) Each of these losses are discussed below in more detail.
  - (J=0.0) The inductive reactance of the loading coil, cancels out the capacitive reactance a shortened (less than 1/4 wave length) antenna has (see chart, courtesy of the ARRL ).

**Rebuild sentences not traceable to original** (showing up to 8 of 93):

  - (J=0.0) Antenna Efficiency — K0BG Mobile Amateur Radio Skip to main content ☰ 🔍 🌙 Antenna Efficiency Last updated: April 2026 Based on original work by Alan Applegate, K0BG Preserved & expanded for the amateur radio community In This Article Basics Antenna efficiency is an elusive quantity that is difficult to quantify.
  - (J=0.0) We can calculate it closely enough if we know three things: the ground losses, the radiation resistance, and the coil Q.
  - (J=0.0) Unfortunately, we don't know any of these values with any certainty, although we can use an antenna analyzer to measure their total series value — the input impedance in other words.
  - (J=0.0) Since these values are in series with one another, changing one has an effect on the others. 📡 Antenna Efficiency Estimator — see exactly where your 100W goes → A good example of this complexity is the addition of a cap hat.
  - (J=0.0) A cap hat adds capacitance to that portion of the antenna above the loading coil.
  - (J=0.0) No matter where it is placed along that length, it adds the same amount of capacitance.
  - (J=0.0) This will cause the input impedance to increase.
  - (J=0.0) However, the change in input impedance may be due to an increase in radiation resistance, or to additional resistive (Q) losses in the coil, depending on where along the length the cap hat is installed. 🔑 KEY CONCEPT Accurately calculating efficiency cannot be done with simple test tools or anecdotal formulas commonly found on the internet.

### `cables-interfacing.html` <- `cabling.html`

- Doc Jaccard **0.16** | sentence coverage **20%** | section coverage **1/1** | expansion **1.04x** (1873 rebuilt words vs 1807 original)
- Original title: 'Cables & Interfacing'
- Rebuild title:  'Cables & Interfacing — K0BG Mobile Amateur Radio'

**Original sentences absent from rebuild** (showing up to 8 of 82):

  - (J=0.05) Cables & Interfacing Contents: Basics ; Remote Cables ; Modular Plugs & Jacks ; If You Just Have To Make Your Own ; Basics In an effort to minimize duplication, information on power wiring in included in the Wiring article.
  - (J=0.04) The information includes proper fusing, splicing, shortening, and crimping connectors.
  - (J=0.0) Just as important, is minimizing voltage drop, and the article covers that issue as well.
  - (J=0.15) Unfortunately, too many of them look like CAT5 cables, prompting folks to use it as a cheap substitute to the more expensive factory units.
  - (J=0.0) Sometime this works, and sometimes it doesn't.
  - (J=0.0) And sometimes, damage can be caused to the transceiver in question when the incorrect cable is used.
  - (J=0.0) Therefore, it is always best to bite the bullet, and pay the premium for the right stuff!
  - (J=0.2) Called by a variety of names, they're meant to interface transceivers to programing and email computers, antenna controllers, amplifiers, and even the Internet!

**Rebuild sentences not traceable to original** (showing up to 8 of 68):

  - (J=0.04) Cables & Interfacing — K0BG Mobile Amateur Radio Skip to main content ☰ 🔍 🌙 Cables & Interfacing Last updated: April 2026 Based on original work by Alan Applegate, K0BG Preserved & expanded for the amateur radio community In This Article Basics Information on power wiring is covered in the Wiring article , including proper fusing, splicing, shortening, and crimping connectors.
  - (J=0.0) Minimizing voltage drop is also covered there.
  - (J=0.0) This article focuses on signal cables: microphone cords, remote control cables, and the modular connectors used for interfacing to computers, antenna controllers, and amplifiers.
  - (J=0.15) Unfortunately, too many of them look like CAT5 cables, prompting people to use CAT5 as a cheap substitute for the more expensive factory units.
  - (J=0.0) And sometimes it damages the transceiver.
  - (J=0.0) Always use the correct, manufacturer-supplied cable.
  - (J=0.0) The ports (sockets) are different between manufacturers, and in many cases between models from the same manufacturer.
  - (J=0.0) Use manufacturer-supplied cabling wherever possible.

### `how-to-wind-choke.html` <- `choke.html`

- Doc Jaccard **0.13** | sentence coverage **22%** | section coverage **5/5** | expansion **1.61x** (2168 rebuilt words vs 1346 original)
- Original title: 'How To Wind A Choke'
- Rebuild title:  'How to Wind a Choke — K0BG Mobile Amateur Radio'

**Original sentences absent from rebuild** (showing up to 8 of 64):

  - (J=0.03) How To Wind A Choke Contents: Basics ; Materials ; Preparing ; Winding ; Finishing ; Basics Remotely controlled, HF mobile antennas, like the Scorpion 680 shown at right, are the most popular style of mobile antennas , and for good reason.
  - (J=0.04) The ability to change operating frequency while under way is an obvious and compelling attribute.
  - (J=0.0) TurboTuner-2 ® , MFJ ® , TargetTuner ® , and others have fully automated the controller process, albeit in different ways.
  - (J=0.14) No matter the process, every controller, even a manual one, requires one common component; a motor lead RF choke.
  - (J=0.29) Depending on the antenna's design, the applied RF voltage (100 watts driving power) is typically ≈200 volts, but may in fact exceed 1,000 volts!
  - (J=0.13) Even if it doesn't, erratic operation, and RFI issues will abound.
  - (J=0.0) Thankfully, there is a simple solution—the RF choke.
  - (J=0.24) For our purposes, that is Mix 31, and more specifically, in the form of a 3/4 inch ID split bead.

**Rebuild sentences not traceable to original** (showing up to 8 of 92):

  - (J=0.04) How to Wind a Choke — K0BG Mobile Amateur Radio Skip to main content ☰ 🔍 🌙 How to Wind a Choke Last updated: April 2026 Based on original work by Alan Applegate, K0BG Preserved & expanded for the amateur radio community In This Article Basics Remotely controlled HF mobile antennas are the most popular style of mobile antenna, and for good reason: the ability to change operating frequency while underway is an obvious and compelling attribute.
  - (J=0.14) No matter the controller type — TurboTuner-2, MFJ, TargetTuner, or a manual unit — every controller requires one common component: a motor lead RF choke.
  - (J=0.13) Even if it doesn't destroy it outright, erratic operation and RFI issues will abound.
  - (J=0.0) The solution is a properly wound RF choke. 🔑 KEY CONCEPT: CHOKE PLACEMENT Everything between the choke and the antenna radiates.
  - (J=0.19) If you mount chokes inside the vehicle, you will be plagued with erratic controller operation and RFI problems.
  - (J=0.0) See the Common Mode Currents article and the Antenna Controllers article for context on why this matters.
  - (J=0.06) A correctly wound choke using these materials will produce a mostly resistive impedance of approximately 10 kΩ at 10 MHz — adequate in most cases except for some sloppily installed, short-stubby antennas.
  - (J=0.0) Materials You need three things, and none of them have acceptable substitutes.

### `controlling-static.html` <- `static.html`

- Doc Jaccard **0.18** | sentence coverage **24%** | section coverage **1/1** | expansion **1.23x** (1931 rebuilt words vs 1572 original)
- Original title: 'Controlling Static'
- Rebuild title:  'Controlling Static — K0BG Mobile Amateur Radio'

**Original sentences absent from rebuild** (showing up to 8 of 66):

  - (J=0.08) Controlling Static Contents: Basics ; Other Static Problems ; Corona Loss ; Static Drains ; Odds & Ends ; Basics Every single mobile operator is plagued with static.
  - (J=0.05) Atmospheric static is the background noise we hear when we're listening to a clear frequency.
  - (J=0.26) Even the stream of electrons from the sun, and solar system add their toll.
  - (J=0.03) Although the strength (loudness) varies over a wide range, short-term changes aren't evident.
  - (J=0.25) In fact, you can use band noise as a signal source for comparing antennas, but you obviously need a QRM free band!
  - (J=0.0) We hear static because electrical discharges by their nature have very fast rise times.
  - (J=0.0) In basic terms, it is nature's version of high frequency interference.
  - (J=0.0) Noise blankers are nearly worthless in curbing atmospheric static.

**Rebuild sentences not traceable to original** (showing up to 8 of 75):

  - (J=0.08) Controlling Static — K0BG Mobile Amateur Radio Skip to main content ☰ 🔍 🌙 Controlling Static Last updated: April 2026 Based on original work by Alan Applegate, K0BG Preserved & expanded for the amateur radio community In This Article Basics Every single mobile operator is plagued with static.
  - (J=0.05) Atmospheric static is the background noise you hear when listening to a clear frequency.
  - (J=0.0) Electrical discharges are inherently high-frequency events by virtue of their fast rise times.
  - (J=0.0) Noise blankers are nearly worthless against atmospheric static.
  - (J=0.0) It doesn't require actual rain — virga (falling moisture that evaporates before reaching the ground) is a common culprit.
  - (J=0.17) Nature also generates so-called rain static, and it doesn't have to be raining for it to occur.
  - (J=0.13) The discharge is usually a lightning strike, although you might not see or hear it. 🔥 MYTH BUSTED Some people believe rain static is caused by moisture molecules physically hitting antenna elements.
  - (J=0.0) Rain static is an electrostatic phenomenon, not a mechanical one.

### `antenna-mounts.html` <- `antmount.html`

- Doc Jaccard **0.23** | sentence coverage **27%** | section coverage **1/1** | expansion **0.76x** (4102 rebuilt words vs 5379 original)
- Original title: 'Antenna Mounts'
- Rebuild title:  'Antenna Mounts — K0BG Mobile Amateur Radio'

**Original sentences absent from rebuild** (showing up to 8 of 219):

  - (J=0.04) Antenna Mounts Contents: Basics ; Foreword On Mounting ; Mag Mounts ; Ballmounts ; Bed, Clamp, Clip, Lip, Seam, and Trunk Mounts ; Foldover Mounts; Quick Disconnects ; Home Brew Mounts ; Pocket Mounts ; Post Mounts ; Springs & Guys ; Trailer Hitch Mounts ; Whips & Masts ; Odd & Ends ; Basics While reading this section, it is important to remember, that modern steel or aluminum bodied vehicles, use very thin material for all body panels.
  - (J=0.0) This all but eliminates the use of mounts which rely of the strength of the body panels.
  - (J=0.0) It is possible to internally brace body mounts, however this usually requires extensive fabrication and is not recommended.
  - (J=0.3) A decent quality (read that as efficient) HF mobile antenna is not an inexpensive commodity, and may cost upwards of $1,200 (although lessor quality ones are about half this amount).
  - (J=0.0) More on this aspect below.
  - (J=0.13) Further, it is easier to see the antenna in the rear view as opposed to craning your neck.
  - (J=0.21) It is also less likely to be "twanged" when you're parallel parked.
  - (J=0.18) If you've chosen front mounting as a lot of folks who pull trailers do, then it should be mounted to the right into your peripheral vision to avoid distraction.

**Rebuild sentences not traceable to original** (showing up to 8 of 119):

  - (J=0.18) If you've chosen front mounting — as many folks who pull trailers do — mount it to the right into your peripheral vision to avoid distraction.
  - (J=0.0) Mounting near one edge solves this without any performance penalty.
  - (J=0.0) Shadowing is also important, and so is mounting height.
  - (J=0.0) In the desert southwest, there is little trouble with the antenna tip extending to 16 feet.
  - (J=0.0) In the New England area, 11 or 12 feet is about the limit.
  - (J=0.17) A ground strap is not a substitute for proper mounting location.
  - (J=0.0) Typical magnetic mount bases.
  - (J=0.0) The holding force is far less on a vehicle's thin sheet metal than on the thick steel used in retail demonstrations.

### `antenna-myths.html` <- `myths.html`

- Doc Jaccard **0.22** | sentence coverage **32%** | section coverage **1/1** | expansion **0.64x** (4659 rebuilt words vs 7328 original)
- Original title: 'Antenna Myths'
- Rebuild title:  'Antenna Myths — K0BG Mobile Amateur Radio'

**Original sentences absent from rebuild** (showing up to 8 of 250):

  - (J=0.0) Antenna Myths Contents: Basics ; The Band Coverage Myth ; What's 3dB? ; The Choke Myth ; The DX Myth ; HF Gain Myths ; VHF Gain Myths ; The Reciprocal Myth ; Coil Q Myth ; Coil Length Myth ; The Efficiency Myth ; The Power Myth ; Ground Loss Myths ; Body Myth ; Radiation Pattern Myths ; The NVIS myth ; The SWR Myth ; The SWR vs.
  - (J=0.0) Although some of the information presented here is in other articles on this web site, it is best to set them out here in an effort to correct some of the more popular myths.
  - (J=0.0) While some of them can be applied to base station antennas as well, the thrust here is aimed at HF mobile antennas.
  - (J=0.0) Readers should also acquaint themselves with with the different types of grounds .
  - (J=0.0) There are many reasons why this is so, but not the least is overall physical length.
  - (J=0.12) A full-length 1/4 wave, unloaded antenna for 6 meters will be about 54 inches long, and may be only 48 to 50 inches if the mast is large like those of most remotely-tuned antennas.
  - (J=0.1) This is slightly longer than the base/coil assembly of most screwdriver antennas.
  - (J=0.12) On 10 meters, a full-length 1/4 wave, unloaded antenna is about 96 inches long, but again may be somewhat shorter due to the mast size.

**Rebuild sentences not traceable to original** (showing up to 8 of 109):

  - (J=0.0) And remember: myths die hard.
  - (J=0.0) A monoband resonator coil close-up.
  - (J=0.0) Coil Q is the dominant efficiency variable in this class of antenna, and it cannot be determined from appearance alone.
  - (J=0.0) Almost every manufacturer claims their coil is the highest-Q unit available — one of the most persistent myths in mobile HF.
  - (J=0.0) The only honest way to compare coils is to measure Q directly with an antenna analyzer or impedance bridge.
  - (J=0.12) A full-length 1/4 wave, unloaded antenna for 6 meters is about 54 inches long — approximately the same length as the base/coil assembly of most screwdriver antennas.
  - (J=0.12) On 10 meters, a full-length 1/4 wave antenna is about 96 inches long, and depending on the brand, covering 10 and 12 meters may require installing a shorter whip.
  - (J=0.13) The requisite inductance of the coil is the main problem — even a 13-foot antenna will require an inductor in the neighborhood of 600 µH.

### `antenna-commercial.html` <- `antennas.html`

- Doc Jaccard **0.24** | sentence coverage **35%** | section coverage **1/2** | expansion **0.80x** (3660 rebuilt words vs 4563 original)
- Original title: 'Antenna, Commercial'
- Rebuild title:  'Commercial Antennas — K0BG Mobile Amateur Radio'
- **Section headings from original missing from rebuild** (1): `Ford F-series, and other aluminum-bodied vehicles`

**Original sentences absent from rebuild** (showing up to 8 of 163):

  - (J=0.08) Antenna, Commercial Contents: Ford F-series, and other aluminum-bodied vehicles ; Basics ; Esoteric Flaws ; Short, Stubby Antennas ; A Few Notes On Motors ; Standard Sized Antennas ; Spirally Wound Antennas ; Automatic Band-Switching Antennas ; Monoband Antennas ; Notes On Whips ; Odds & Ends ; Ford F-series, and other aluminum-bodied vehicles Ford's F-series, aluminum-bodied pickup trucks require special installation practices with respect to galvanic corrosion .
  - (J=0.09) Here is the bulletin from Ford which explains what must be done to prevent galvanic corrosion.
  - (J=0.16) The results of failing to follow Ford's guide lines are predictable, and not covered under warranty !
  - (J=0.0) And bonding is not required , as Ford has done that for you!
  - (J=0.0) However, their manufacturer's recommendations may be different than those outlined in the above bulletin.
  - (J=0.26) In some cases, this eliminates using that brand and/or model of antennas.
  - (J=0.25) The most important attribute is overall Antenna Efficiency , and that's well covered in the highlighted article.
  - (J=0.0) So what we're going to cover here are a few pitfalls to avoid.

**Rebuild sentences not traceable to original** (showing up to 8 of 98):

  - (J=0.08) Commercial Antennas — K0BG Mobile Amateur Radio Skip to main content ☰ 🔍 🌙 Commercial Antennas Last updated: April 2026 Based on original work by Alan Applegate, K0BG Preserved & expanded for the amateur radio community In This Article Ford F-Series and Other Aluminum-Body Vehicles Ford's F-series aluminum-body pickup trucks require special installation practices with respect to galvanic corrosion.
  - (J=0.16) Ford has published a bulletin explaining what must be done to prevent galvanic corrosion; the results of failing to follow Ford's guidelines are predictable and not covered under warranty.
  - (J=0.0) Bonding is not required because Ford has already done that for you.
  - (J=0.0) A heavily loaded vertical antenna with multiple radial elements and auxiliary loading sections on a tall mast.
  - (J=0.0) This is not a typical mobile configuration — it illustrates the extreme end of the complexity spectrum.
  - (J=0.0) Mobile antennas must accomplish the same electrical goals in a fraction of the physical envelope, which is why efficiency is always compromised.
  - (J=0.19) Radiation resistance (R r ) is a square function of electrical length: a 9-foot long antenna will have twice the R r of a 6-foot antenna, and twice the efficiency, all else being equal. ⚠ WARNING Do not get suckered into believing that large diameter coils (>3.5 inches) are better than smaller ones — they're not.
  - (J=0.0) Two important points bear repeating: Loading coils are considered lumped constants.

### `grounds.html` <- `ground.html`

- Doc Jaccard **0.24** | sentence coverage **35%** | section coverage **1/1** | expansion **0.99x** (1763 rebuilt words vs 1778 original)
- Original title: 'Grounds, RF & DC'
- Rebuild title:  'Grounds, RF & DC — K0BG Mobile Amateur Radio'

**Original sentences absent from rebuild** (showing up to 8 of 64):

  - (J=0.23) Grounds, RF & DC Contents: Basics ; What Is A Ground Plane? ; Your Average Vehicle ; Mounting Location Issues ; Odds & Ends ; Basics Many amateurs harbor the notion that DC grounding an antenna mount will magically act as, or replace, a ground Plane .
  - (J=0.0) It may DC ground the antenna's base, and it just might RF ground it too depending on the straps length and width versus the frequency of operation.
  - (J=0.15) However, it is by no means a replacement for an adequate ground plane under the antenna!
  - (J=0.0) Incidentally, the term ground plane is a bit of a misnomer (see next section).
  - (J=0.03) The body of the vehicle and the capacitive coupling to the surface under the vehicle, is acting as a ground plane, and a lossy one at that!
  - (J=0.0) Typical ground plane losses vary between 2 and 10 ohms, 10 through 80 meters respectively, but in the real world they may be as high as 20Ω on 80 meters.
  - (J=0.01) The primary cause are standing waves between the body of the vehicle, and the surface under it.
  - (J=0.0) This fact should not be confused with the term SWR!

**Rebuild sentences not traceable to original** (showing up to 8 of 47):

  - (J=0.15) DC grounding the mount may establish an RF ground for the antenna's base — depending on the strap's length and width relative to the frequency of operation — but it is by no means a replacement for an adequate ground plane under the antenna. 🔑 KEY CONCEPT The body of the vehicle and its capacitive coupling to the surface below act as the ground plane — and it's a lossy one.
  - (J=0.0) Typical ground plane losses range from 5 to 20 ohms across 10 through 80 meters respectively — and in practice they may run even higher.
  - (J=0.0) The primary cause is standing waves between the vehicle body and the surface beneath it.
  - (J=0.0) Do not confuse this with SWR.
  - (J=0.14) Excessive ground losses are directly related to the level of common mode currents.
  - (J=0.03) Common mode current causes RFI problems both inbound and outbound, and can drastically reduce the receiver's signal-to-noise ratio.
  - (J=0.18) In a mobile scenario, there is one more ground to be concerned with: a proper RF ground return for the coax shield.
  - (J=0.09) RF must return to its source.

### `miniature-radios.html` <- `miniature.html`

- Doc Jaccard **0.30** | sentence coverage **37%** | section coverage **2/2** | expansion **0.74x** (6116 rebuilt words vs 8228 original)
- Original title: 'Miniature Radios'
- Rebuild title:  'Miniature Radios — K0BG Mobile Amateur Radio'

**Original sentences absent from rebuild** (showing up to 8 of 296):

  - (J=0.13) Miniature Radios Contents: Basics ; A Few Words About AM Operation ; Alinco DX-SR8T ; Alinco DX-SR9T ; Elecraft KX3 ; Icom IC-706 ; Icom Ic-7000 ; Icom IC-7100 ; Icom IC-7200 ; Icom IC-7300 ; Kenwood TS-480 ; Yaesu FT-450 ; Yaesu FT-891 ; Yaesu FT-991 ; Other transceivers ; Common Problems ; What To Do About Heat ; Voltage Problems ; Basics Modern transceivers designed primarily for mobile use often cover all of the amateur bands (excluding the 1.25 meters) from 160 meters through 70 cm.
  - (J=0.0) A few only cover 160 thought 6 meters.
  - (J=0.0) If you do remote yours, read this article on cabling , and this one on wiring .
  - (J=0.27) The controls are also miniaturized making it difficult for large fingered folks to do the adjusting, which says nothing about doing it while under way.
  - (J=0.05) All of this requires the use of menus further frustrating the average user.
  - (J=0.0) This subject is covered in the Antenna Matching article.
  - (J=0.23) All are audio based except the Icom IC-7000/7100/7200/7300, FT-450D, and FT-991.
  - (J=0.04) While most AF based ones give a good account of themselves, digital DSP is a step above.

**Rebuild sentences not traceable to original** (showing up to 8 of 141):

  - (J=0.13) Miniature Radios — K0BG Mobile Amateur Radio Skip to main content ☰ 🔍 🌙 Miniature Radios Last updated: April 2026 Based on original work by Alan Applegate, K0BG Preserved & expanded for the amateur radio community In This Article Basics Modern transceivers designed primarily for mobile use often cover all of the amateur bands (excluding 1.25 meters) from 160 meters through 70 cm.
  - (J=0.0) A few only cover 160 through 6 meters.
  - (J=0.0) If you do remote yours, make sure you understand the cabling and wiring requirements thoroughly.
  - (J=0.05) All of this requires menus, further frustrating the average user. 🔑 KEY CONCEPT Impedance matching is not optional.
  - (J=0.0) This subject is covered in detail in the Antenna Matching article.
  - (J=0.04) While most AF-based units give a decent account of themselves, IF-based digital DSP is a step above.
  - (J=0.0) This brings up another issue: sensitivity.
  - (J=0.1) Receivers with crystal-lattice filters (discrete, roofing, and IF) tend to have better selectivity than those with just DSP.

### `antenna-shootouts.html` <- `shootout.html`

- Doc Jaccard **0.21** | sentence coverage **38%** | section coverage **2/2** | expansion **1.00x** (2474 rebuilt words vs 2468 original)
- Original title: 'Antenna Shootouts'
- Rebuild title:  'Antenna Shootouts — K0BG Mobile Amateur Radio'

**Original sentences absent from rebuild** (showing up to 8 of 88):

  - (J=0.17) The rules make very interesting reading, and one standout is the fact the receiving antenna was to be located 4,900 feet away!
  - (J=0.12) Additional stations 10 to 100 miles away were going to be used to verify the closer-in measurements.
  - (J=0.0) The results of the third trial were published in the July 1961 issue of QST.
  - (J=0.0) Included with the article was a montage of 16 photos shown at right (click to open in new page).
  - (J=0.06) Probably the most interesting fact was, almost without exception, each entrant's antenna sported a cap hat .
  - (J=0.0) One of those was nearly identical to the one I currently use.
  - (J=0.1) Incidentally, the winner of the third shootout was David Evans, WA6JJG, the man being kissed.
  - (J=0.05) His antenna is pictured in the fourth row, first column.

**Rebuild sentences not traceable to original** (showing up to 8 of 77):

  - (J=0.06) The rules make very interesting reading.
  - (J=0.17) One standout: the receiving antenna was to be located 4,900 feet away, with additional stations 10 to 100 miles away used to verify the closer-in measurements.
  - (J=0.0) Keep this fact in mind — it will matter when evaluating modern shootout methodology.
  - (J=0.0) Photo montage from the July 1961 QST covering the third California Mobilecade and Field Trials results.
  - (J=0.06) Almost without exception, every entrant's antenna sported a cap hat — including one nearly identical to the cap hat design described in the Cap Hat article.
  - (J=0.1) The winner, David Evans, WA6JJG (the man being kissed), won with a scant 7.26 watts input.
  - (J=0.06) His cap hat is visible in the fourth row, first column, correctly mounted at the very top of the antenna.
  - (J=0.18) Mobile HF antennas come with a variety of coil sizes, overall lengths, coil and mast diameters, and different positions for the coil within the antenna.

### `antenna-cap-hat.html` <- `caphats.html`

- Doc Jaccard **0.21** | sentence coverage **41%** | section coverage **1/1** | expansion **1.42x** (2183 rebuilt words vs 1542 original)
- Original title: 'Antenna Cap Hat'
- Rebuild title:  'Antenna Cap Hat — K0BG Mobile Amateur Radio'

**Original sentences absent from rebuild** (showing up to 8 of 50):

  - (J=0.16) Antenna Cap Hat Contents: Basics ; Design Considerations ; Conclusions ; Basics Cap hats are not new innovation s, and have been used in one form or another almost since the dawn of radio.
  - (J=0.12) His abstract of the patent reads in part, "...As charged surfaces...
  - (J=0.19) Then, in 1954, the ARRL published their first Mobile Manual which was a compilation of the various mobile articles which had appeared previously in QST.
  - (J=0.03) Fast-forwarding a few years, the July, 1961 issue of QST, contained a short article which covered the second-annual California Mobilecade and Field Trials .
  - (J=0.0) That article was highlighted by a photo montage (shown right) of 16 contestants entered into the field trail (click to open in new window).
  - (J=0.0) David Evans, WA6JJG, won that competition, and was rewarded with a kiss!
  - (J=0.0) Take note of the three loop, cap hat design directly above David's head, and one that is installed well above the coil where it should be!
  - (J=0.0) The next few paragraphs explain why position is so important.

**Rebuild sentences not traceable to original** (showing up to 8 of 74):

  - (J=0.16) Antenna Cap Hat — K0BG Mobile Amateur Radio Skip to main content ☰ 🔍 🌙 Antenna Cap Hat Last updated: April 2026 Based on original work by Alan Applegate, K0BG Preserved & expanded for the amateur radio community In This Article Basics Cap hats are not new innovations, and have been used in one form or another almost since the dawn of radio.
  - (J=0.12) His abstract reads in part: "...As charged surfaces...
  - (J=0.03) Photo montage from the July 1961 QST, showing 16 contestants in the third annual California Mobilecade and Field Trials.
  - (J=0.0) Note that nearly every antenna sports a cap hat.
  - (J=0.0) David Evans, WA6JJG (the man being kissed), won with just 7.26 watts input.
  - (J=0.0) His antenna, visible in the fourth row, first column, has a cap hat installed correctly at the very top.
  - (J=0.0) This competition established the cap hat's effectiveness definitively.
  - (J=0.19) Then, in 1954, the ARRL published their first Mobile Manual — a compilation of mobile articles from QST.

### `home-brew.html` <- `things.html`

- Doc Jaccard **0.34** | sentence coverage **48%** | section coverage **2/2** | expansion **0.91x** (4149 rebuilt words vs 4538 original)
- Original title: 'Home Brew Things'
- Rebuild title:  'Home Brew Things — K0BG Mobile Amateur Radio'

**Original sentences absent from rebuild** (showing up to 8 of 141):

  - (J=0.27) Home Brew Things Contents: Basics ; Suppliers ; Basic Antennas ; Brewing ; Masts ; Brackets ; Intermission ; Manual Override ; Amplifier Bypass ; The Simple Rocker Switch ; Debouncer ; Antenna Switch ; Amplifier Remote Control ; Other Things ; Home Brew Basics Starting with the dawn of amateur radio, it was the rule (not the exception) to build your own gear, including transmitters, receivers, antennas, amplifiers, and even test gear.
  - (J=0.24) It wasn't until the early 50s, that manufactures started to fill the (modern) needs of us amateurs.
  - (J=0.25) Transceivers, as we know them today, didn't make the appearance until the latter 50s.
  - (J=0.0) Collins, Heathkit, National Radio, and a myriad of others, started the trend we enjoy today.
  - (J=0.05) Radio Shack is a prime example.
  - (J=0.0) Since we're talking about building, here are a few sites of specific interest to home brewers, tinkerers, and most amateurs.
  - (J=0.06) Aaron's General Store carries a large stock of both inch and metric sized bolts, nuts, washers, and fasteners.
  - (J=0.0) They even have a line of security fasteners of just about every configuration you can think of.

**Rebuild sentences not traceable to original** (showing up to 8 of 96):

  - (J=0.06) Suppliers Home brewers have several reliable suppliers worth knowing: Aaron's General Store — Large stock of both inch and metric bolts, nuts, washers, and fasteners, including security fasteners.
  - (J=0.12) Circuit Specialties — Home brew parts, test equipment, soldering stations, and power supplies.
  - (J=0.0) Micro Fasteners — Set screws and fasteners in unusual sizes.
  - (J=0.0) All Electronics / All Spectrum Electronics — New, used, pulls, and overstock of electronic parts, connectors, LEDs, and fans.
  - (J=0.17) Mouser, Newark, and Digikey — First-line retailers of all things electronic.
  - (J=0.0) If you can't find a part here, you can't find it.
  - (J=0.18) A quick check of their web site today shows the current price at $65 each.
  - (J=0.0) Their 4804TL now sells for $500 each.

### `neat-gadgets.html` <- `neat.html`

- Doc Jaccard **0.33** | sentence coverage **56%** | section coverage **1/1** | expansion **1.14x** (3322 rebuilt words vs 2920 original)
- Original title: 'Neat Gadgets'
- Rebuild title:  'Neat Gadgets — K0BG Mobile Amateur Radio'

**Original sentences absent from rebuild** (showing up to 8 of 74):

  - (J=0.17) Neat Gadgets Contents: Basics ; RF Meter ; Antenna Analyzers ; Spectrum Analyzers ; Coax Cutter ; Soldering Aides ; Power Checkers ; Fire Extinguishers ; MiniVNAPro ; Auto Off; Amplifier Interfaces ; FT-857 Meter ; Mini-Manual ; Rescue Tape ; Two Wire Voltmeters ; Video Display ; Basics Anything anyone does to increase safety and/or reduce distraction is a good step in the right direction.
  - (J=0.29) They're only here as they are proven tools for doing the job correctly, the first time! ☜Return☜ RF Meter The MFJ-854 is an inexpensive device for measuring RF imposed on conductors.
  - (J=0.18) Even then, it takes due diligence, and strong fingers!
  - (J=0.0) It also reads out the SWR, but all too often that reading is incorrectly used, especially when adjusting shunt matching coils .
  - (J=0.08) It does have one drawback, however, as it does not display the actual Z (±j).
  - (J=0.05) As a result, you have to figure that out yourself, albeit rather self evident.
  - (J=0.0) You'll also need a N to UHF adapter for most measurements.
  - (J=0.0) If you do have interference, you might want to purchase their MFJ-731 tunable filter.

**Rebuild sentences not traceable to original** (showing up to 8 of 88):

  - (J=0.17) Neat Gadgets — K0BG Mobile Amateur Radio Skip to main content ☰ 🔍 🌙 Neat Gadgets Last updated: April 2026 Based on original work by Alan Applegate, K0BG Preserved & expanded for the amateur radio community In This Article Basics Anything anyone does to increase safety and/or reduce distraction is a good step in the right direction.
  - (J=0.14) It measures RF current as low as 1 mA and handles up to 3 amps maximum.
  - (J=0.05) Follow the directions: set the meter on the high scale first, and work down as necessary.
  - (J=0.0) Antenna Analyzers Knowing how much common mode current is present is one half of the diagnostic equation; knowing the antenna's actual impedance is the other half.
  - (J=0.0) The MFJ-259B antenna analyzer.
  - (J=0.19) It has become as ubiquitous as the directional wattmeter in amateur radio circles.
  - (J=0.08) It does have one drawback: it does not display the actual Z (±j), so you have to figure that out yourself — though it is rather self-evident once you know the X and R values.
  - (J=0.05) The MFJ-266 displays all three impedance parameters simultaneously (except for UHF) and includes a built-in interference detector.

### `auto-couplers.html` <- `couplers.html`

- Doc Jaccard **0.27** | sentence coverage **60%** | section coverage **2/2** | expansion **1.66x** (1558 rebuilt words vs 939 original)
- Original title: 'Auto-Couplers'
- Rebuild title:  'Auto-Couplers — K0BG Mobile Amateur Radio'

**Original sentences absent from rebuild** (showing up to 8 of 21):

  - (J=0.22) Auto-Couplers Contents: Basics ; Efficiencies ; Basics There seems to be as much confusion about internal couplers as there are external ones.
  - (J=0.29) Using one in conjunction with a screwdriver antenna isn't recommended either due to the high RF voltage (see third paragraph).
  - (J=0.0) The Kenwood TS480 SAT vs.
  - (J=0.21) This is a concern, because readily-available antenna mounting hardware are not designed to handle this much electromotive stress.
  - (J=0.0) For example, standard ballmounts and nylon washers will fail post-haste, especially so if moisture is present.
  - (J=0.02) The right photo depicts an old GE Master ballmount insulator.
  - (J=0.26) You can see the burned-out groove between the edge of the (removed) ball and one of the mounting bolts.
  - (J=0.0) We can get away from this issue by using a base insulator like the Breedlove unit shown at left.

**Rebuild sentences not traceable to original** (showing up to 8 of 40):

  - (J=0.0) This is a serious concern.
  - (J=0.0) They will fail post-haste, especially if moisture is present.
  - (J=0.0) Standard mounting hardware is not rated for these voltages.
  - (J=0.0) Use a purpose-built high-voltage base insulator if you must use an auto-coupler.
  - (J=0.0) A purpose-built high-voltage base insulator of the type required when using an auto-coupler.
  - (J=0.0) The voltage rating must exceed the peak RF voltage the auto-coupler can produce — which, at 100 watts PEP into a short antenna, can exceed 10 kV.
  - (J=0.08) Even a one-foot piece of coax will reduce efficiency by 30%.
  - (J=0.14) This interaction should not be confused with using shunt reactances to match a low-impedance HF antenna to 50 ohms — that is a different situation entirely. 📷 [Coax Capacitance Diagram] Diagram showing the distributed capacitance (25 pF/ft) of coax acting as a shunt reactance to ground when inserted between an auto-coupler and a short antenna, bypassing RF before it reaches the radiator.

### `portable-operation.html` <- `portable.html`

- Doc Jaccard **0.42** | sentence coverage **61%** | section coverage **1/1** | expansion **1.07x** (3301 rebuilt words vs 3079 original)
- Original title: 'Portable Operation'
- Rebuild title:  'Portable Operation — K0BG Mobile Amateur Radio'

**Original sentences absent from rebuild** (showing up to 8 of 67):

  - (J=0.21) Portable Operation Contents: Basics ; The Power Source ; The House Battery ; Other Batteries ; Battery Boosters ; Power Inverters ; Antenna Choices ; Pedestrian Mobile ; Other things ; Basics The premise of this web site has always been based on mobile-in-motion , but a select number of amateurs include stationary mobile as part of their operating.
  - (J=0.15) There is a hidden aspect with regard to portable operation, and that deals with minimizing ground losses when using ground-mounted vertical antennas.
  - (J=0.21) Personally, I've never operated stationary mobile, or portable, by any name.
  - (J=0.29) Most RVers know those rules, and follow them carefully as they know what might happen if they don't.
  - (J=0.0) It bears careful reading if you're unfamiliar with RV generator usage.
  - (J=0.17) Most vehicles, designed to be used as a towing vehicle have special trailer towing packages available.
  - (J=0.25) And, in almost every case, a house battery charging circuit.
  - (J=0.0) There's new device just introduced by West Mountain Radio which portable operators will cherish, and that's the ISOpwr-Auxiliary Battery Isolator.

**Rebuild sentences not traceable to original** (showing up to 8 of 67):

  - (J=0.15) There is a hidden aspect to portable operation: minimizing ground losses when using ground-mounted vertical antennas.
  - (J=0.13) The hardware perhaps is, and maybe the creature comforts, but the intrinsic and logistic requirements are identical.
  - (J=0.17) Most vehicles designed to be used as towing vehicles have special trailer towing packages available.
  - (J=0.0) A simple diode-type battery isolator.
  - (J=0.0) These are inexpensive but have significant forward voltage drop (0.6–0.7V), which can cause problems with alternator charging circuits on late-model vehicles.
  - (J=0.0) FET-based isolators are the better choice.
  - (J=0.0) West Mountain Radio introduced the ISOpwr Auxiliary Battery Isolator, which offers a few advantages over its competitors.
  - (J=0.0) The West Mountain Radio ISOpwr auxiliary battery isolator.

### `audio-filtering.html` <- `audio.html`

- Doc Jaccard **0.37** | sentence coverage **63%** | section coverage **2/2** | expansion **1.49x** (1698 rebuilt words vs 1143 original)
- Original title: 'Audio Filtering & Speakers'
- Rebuild title:  'Audio Filtering & Speakers — K0BG Mobile Amateur Radio'

**Original sentences absent from rebuild** (showing up to 8 of 24):

  - (J=0.03) Audio Filtering & Speakers Contents: Safe Mounting Of Speakers ; Basics ; DSP Speakers ; Non-DSP Powered Speakers ; Plain Old Speakers ; Safe Mounting Of Speakers There is a reason this section is first, and that reason is safety !
  - (J=0.06) Here's a little experiment you can carry out on your own.
  - (J=0.06) Here (and hear) is a suggestion to minimize the hash.
  - (J=0.17) The Skytec CW-1, made during the 70s, is a good example.
  - (J=0.17) Unlike the aforementioned CW filter, all of these designs used a combination of inductors and capacitors typically built into a station speaker.
  - (J=0.0) The schematic at left is that of the Icom SP-20 (click on it for a larger view).
  - (J=0.0) Note the switches to select the desired mode; lowpass, highpass, or both.
  - (J=0.1) Also note the passive elements are in series with the speaker for good reason; you have to be careful using directly shunted elements with single-ended audio amplifiers, as doing so can cause them to fail.

**Rebuild sentences not traceable to original** (showing up to 8 of 47):

  - (J=0.03) Audio Filtering & Speakers — K0BG Mobile Amateur Radio Skip to main content ☰ 🔍 🌙 Audio Filtering & Speakers Last updated: April 2026 Based on original work by Alan Applegate, K0BG Preserved & expanded for the amateur radio community In This Article Safe Speaker Mounting There is a reason this section comes first, and that reason is safety.
  - (J=0.15) It is a stopgap solution at best.
  - (J=0.0) Basics: Passive Audio Filters The schematic of the Icom SP-20 passive filter, showing switches S1–S6 to select lowpass (LPF1, LPF2), highpass (HPF2, HPF1), or combinations.
  - (J=0.09) The passive elements are in series with the speaker — a deliberate design choice, as shunting directly across single-ended audio amplifiers can cause failure.
  - (J=0.17) The Skytec CW-1, made during the 1970s, is a good example.
  - (J=0.0) A period advertisement for the Skytec CW-1 passive CW audio filter — a ported 2-inch speaker in a tuned PVC cavity with an adjustable sleeve to set bandpass center frequency.
  - (J=0.0) It sold for about $20 in the 1970s and was a useful tool when receivers lacked built-in CW filters.
  - (J=0.17) Unlike the CW filter mentioned above, most of these designs used a combination of inductors and capacitors built into a station speaker.

### `signal-noise-ratio.html` <- `signal.html`

- Doc Jaccard **0.45** | sentence coverage **63%** | section coverage **1/1** | expansion **1.11x** (2500 rebuilt words vs 2243 original)
- Original title: 'Signal To Noise Ratio'
- Rebuild title:  'Signal to Noise Ratio — K0BG Mobile Amateur Radio'

**Original sentences absent from rebuild** (showing up to 8 of 47):

  - (J=0.28) Signal To Noise Ratio Contents: Basics ; Automatic Gain Control ; Signal Strength; The Noise! ; The Results ; Measuring SNR ; Basics Signal-to-noise ratio (S+N/N ratio, or SNR for short) is one technical aspect not too many amateurs give a second thought to.
  - (J=0.12) Further, it is often high pitched, and rather tiring to listen to.
  - (J=0.12) Thus it behooves us to do what we can to reduce it.
  - (J=0.18) As alluded to above, SNR is usually expressed as a differential between the voltage of the desired signal, and the voltage of the noise.
  - (J=0.05) The formula we use is thus 20*log (10) (Vs+Vn/Vn), where Vs is the strength of the desired signal, and Vn as the voltage of the noise portion.
  - (J=0.0) As an example, let's assume the incoming Vs is 25uV, and the noise is 2uV.
  - (J=0.0) Applying the formula, the SNR would be 22.6 dB, resulting is an easily copied signal.
  - (J=0.28) Let's not get too far ahead of ourselves, and look at the specification (right) of a real-world receiver, the Icom IC-7000 (courtesy of the ARRL ).

**Rebuild sentences not traceable to original** (showing up to 8 of 43):

  - (J=0.18) Thus it behooves us to do what we can to reduce it. 🔑 KEY CONCEPT SNR is expressed as a differential between the voltage of the desired signal and the voltage of the noise: SNR = 20 × log 10 (V s + V n / V n ) Where V s is the strength of the desired signal and V n is the voltage of the noise portion.
  - (J=0.0) As an example: if the incoming V s is 25 µV and the noise is 2 µV, applying the formula gives an SNR of 22.6 dB — an easily copied signal.
  - (J=0.0) Real-World Receiver Specifications ARRL measurements for the Icom IC-7000 receiver.
  - (J=0.08) A signal strength of 0.15 µV yields an SNR of 10 dB — but this figure represents SNR above the internal noise floor of the receiver, not what actually happens in the real mobile world.
  - (J=0.08) The IC-7000 Owner's Manual SINAD and dynamic range table.
  - (J=0.0) Note that Dynamic Range becomes worse as bandwidth increases.
  - (J=0.0) A signal strength of 0.15 µV yields an SNR of 10 dB.
  - (J=0.05) And we have the SINAD measurement (Signal to Noise and Distortion), which although typically used with FM operation, can be applied to SSB as well.

### `insurance.html` <- `insure.html`

- Doc Jaccard **0.37** | sentence coverage **66%** | section coverage **2/2** | expansion **1.30x** (1762 rebuilt words vs 1352 original)
- Original title: 'Amateur Mobile Insurance'
- Rebuild title:  'Amateur Mobile Insurance — K0BG Mobile Amateur Radio'

**Original sentences absent from rebuild** (showing up to 8 of 22):

  - (J=0.0) Those who don't are in my opinion scofflaws, causing the rest of us to pay high premiums for uninsured motorists coverage.
  - (J=0.0) The logos shown are the registered Trademarks of just a few of the hundreds of different companies who write insurance policies (they are not an endorsement).
  - (J=0.0) Of course, higher-priced vehicles like BMWs, Mercedes, and Corvettes cost even more.
  - (J=0.24) Usually, that's the level of liability coverage (maximum amount payable, which is not always a good thing!), and cutting out the less-apparent peripheral coverage—read that as your amateur radio equipment!
  - (J=0.0) Read that as a mag mounted!
  - (J=0.28) Most cover theft to a specific limit, and most cover amateur radio equipment, if they're notified ahead of time—typically by writing.
  - (J=0.0) Incidentally, the actual cost for one specific coverage clause—comprehensive glass replacement as an example—doesn't vary a whole lot between insurance carriers.
  - (J=0.0) Thus the only way for insurers to save you money , is to reduce coverage!

**Rebuild sentences not traceable to original** (showing up to 8 of 48):

  - (J=0.0) Amateur Mobile Insurance — K0BG Mobile Amateur Radio Skip to main content ☰ 🔍 🌙 Amateur Mobile Insurance Last updated: April 2026 Based on original work by Alan Applegate, K0BG Preserved & expanded for the amateur radio community In This Article Basics State Farm — the largest vehicle insurer in the US — is one example of the hundreds of companies that write vehicle policies.
  - (J=0.0) The core point: most policies will not automatically cover amateur radio equipment unless you specifically notify the company in writing.
  - (J=0.0) Of course, higher-priced vehicles cost even more.
  - (J=0.13) In one specific case, the vehicle had to be driven to the agent's place of business so they could inspect the installation.
  - (J=0.0) And don't forget to put it in writing.
  - (J=0.0) Progressive Direct — one of the major vehicle insurers.
  - (J=0.0) Each company handles amateur radio equipment differently; there is no industry-wide standard.
  - (J=0.0) Rider policies covering amateur radio gear are offered by some companies; others require only written notification.

### `transmit-audio.html` <- `audioxmit.html`

- Doc Jaccard **0.48** | sentence coverage **69%** | section coverage **1/1** | expansion **1.04x** (2571 rebuilt words vs 2478 original)
- Original title: 'Transmit Audio'
- Rebuild title:  'Transmit Audio — K0BG Mobile Amateur Radio'

**Original sentences absent from rebuild** (showing up to 8 of 40):

  - (J=0.29) Transmit Audio Contents: Basics ; Brief Discussion of IMD ; Dynamic Range & Things ; The Microphone ; Microphone Mods ; Speech Compression & Clipping; Basics The whole intent of this article is to maximize the readability of your transmissions, and hopefully aid you in maintaining contacts once you make them.
  - (J=0.0) We're not dealing with any type of modulation here, except SSB, and there is a good reason why.
  - (J=0.11) They do have pre-emphasis, but that's a whole new subject, and we're not going there!
  - (J=0.28) While those adjustments are important, excessive microphone gain will effectively negate their viability. ☜Return☜ Brief Discussion of IMD The letters IMD stand for Inter-Modulation Distortion, but more correctly, third-order inter-modulation distortion.
  - (J=0.14) In which case, it can be heard a few kHz either side of the bandpass—a place no one seemingly listens for it.
  - (J=0.08) In this case, by a human voice.
  - (J=0.21) After all, we do have microphone gains on our SSB transceivers.
  - (J=0.17) The reason is, the bandwidth in most transceivers capable of SSB transmission, are limited to about 2,400 Hz (≈300 to ≈2,700).

**Rebuild sentences not traceable to original** (showing up to 8 of 30):

  - (J=0.1) Dynamic Range & Things The “Broderick Crawford Syndrome” — talking too far from the microphone.
  - (J=0.0) Crawford's booming delivery worked for television drama, but noise-canceling microphones in a mobile installation require close-talking at one inch or less.
  - (J=0.0) Speaking across or away from the element defeats the noise canceler and lets road noise straight through.
  - (J=0.0) Frequency response of a typical electret condenser microphone — essentially flat from 50 Hz to well above the 3 kHz communications bandwidth.
  - (J=0.0) No other commonly available microphone type comes close to this linearity, which is exactly why transceiver manufacturers use them.
  - (J=0.17) The bandwidth in most transceivers capable of SSB transmission is limited to about 2,400 Hz (approximately 300 to 2,700 Hz).
  - (J=0.1) That fact has proliferated the widespread use of speech processors, equalizers, and other wide-bandwidth devices — to the detriment of us all. 🔥 MYTH BUSTED Far too many amateurs don't understand the relationship between peak versus average power in an SSB signal.
  - (J=0.04) The result is highly increased IMD levels, at the expense of 1 dB or less of power increase.

### `what-i-use.html` <- `what.html`

- Doc Jaccard **0.53** | sentence coverage **75%** | section coverage **1/1** | expansion **1.20x** (2680 rebuilt words vs 2228 original)
- Original title: 'What I Use'
- Rebuild title:  'What I Use — K0BG Mobile Amateur Radio'

**Original sentences absent from rebuild** (showing up to 8 of 31):

  - (J=0.11) What I Use Contents: Personal Selections ; The Antennas ; Cap Hats ; The Amplifiers ; The Controller Boxes ; Video Display ; Odds & Ends ; Personal Selections There are good reasons why I have what I have.
  - (J=0.25) On-line reviews don't mean much either.
  - (J=0.26) Whatever selection you make, the best advise I can offer is this—if at all possible, try it, before you buy it! ☜Return☜ The Antennas Over the years, I've used about 20 different commercial HF antennas, and a lot of home brew ones too.
  - (J=0.0) If you have read the highlighted article, you'd know why we spent the time exploring the various possibilities.
  - (J=0.19) Cap hats increase the radiation resistance (Rr) by raising the antenna's current node.
  - (J=0.22) The three loops are made from 304 stainless steel, .125 by 72 inch long rod.
  - (J=0.0) The effective outer diameter is ≈58 inches.
  - (J=0.0) I have a lot more information about this in my Antenna and Mounting articles.

**Rebuild sentences not traceable to original** (showing up to 8 of 47):

  - (J=0.11) What I Use — K0BG Mobile Amateur Radio Skip to main content ☰ 🔍 🌙 What I Use Last updated: April 2026 Based on original work by Alan Applegate, K0BG Preserved & expanded for the amateur radio community In This Article Personal Selections There are good reasons why I have what I have.
  - (J=0.09) The Antennas My Scorpion 680 mount in the bed of the Honda Ridgeline — 304 stainless steel, 3-inch OD × 0.125-inch wall mast, positioned directly over the cross brace protecting the fuel tank.
  - (J=0.0) Best-made screwdriver antenna available.
  - (J=0.0) Cap Hats My custom cap hat — three loops of 304 stainless steel 0.125-inch rod, 72 inches long each.
  - (J=0.0) Complete assembly weighs 9 ounces.
  - (J=0.0) Effective outer diameter approximately 58 inches.
  - (J=0.0) Mounted atop the mast, equivalent electrical length is approximately 120 inches depending on frequency.
  - (J=0.19) Cap hats increase the radiation resistance (R r ) by raising the antenna's current node.

## 3. Recovered originals with no rebuilt counterpart

These >= 100-word pages exist in the Common Crawl recovery but no rebuilt article maps to them. They are content the rebuild dropped, merged into another article, or never had at all (biography, links, gallery pages, older sub-articles, image collections, etc.). Many are genuine Alan Applegate prose worth resurrecting.

| Original | Words | Title |
|---|---:|---|
| `yesteryear.html` | 5958 | Yesteryear |
| `feeding.html` | 5673 | Amplifiers, Care & Feeding |
| `guides.html` | 4086 | Antenna Buying Guides |
| `buying.html` | 3783 | Buying Advice |
| `homebrew.html` | 3556 | Antennas, Home Brew |
| `ampsetup.html` | 3454 | Amplifier Setup |
| `history.html` | 3079 | A Little Amateur History |
| `protection.html` | 2587 | Wiring Protection |
| `operating.html` | 2554 | Operating Techniques |
| `otr.html` | 2550 | OTR Trucks |
| `cable.html` | 2539 | Modular Cables & Connectors |
| `tooth.html` | 2332 | Bluetooth & You |
| `inter.html` | 2137 | Computer Interfacing |
| `gpnotes.html` | 2042 | Ground Plane Notes |
| `basicmath.html` | 1941 | Basic Math |
| `mounts.html` | 1863 | Radio Mounts |
| `caphathowto.html` | 1813 | Cap Hat How To |
| `warranty.html` | 1659 | Warranty Issues |
| `rv.html` | 1603 | RV Notes |
| `ports.html` | 1519 | Port Pinouts |
| `getting.html` | 1510 | Getting the Best Bang for Your Buck |
| `loops.html` | 1425 | Ground Loops |
| `biography.html` | 1257 | Biography of K0BG |
| `comp.html` | 1199 | Speech Processing & VOX |
| `links.html` | 1075 | KØBG Links |
| `ignition.html` | 931 | Ignition Notes on RFI |
| `unun.html` | 761 | How to Build an UNUN |
| `beads.html` | 693 | The Proper Split Beads to Suppress RFI |
| `pginstr.html` | 658 | Photo Gallery Instructions |
| `favorite.html` | 647 | My Favorite Quotes |
| `editorial.html` | 389 | Template |
| `about.html` | 297 | About K0BG.COM |
| `index.html` | 292 | KØBG.COM |
| `indexright.html` | 251 | WWW.KØBG.COM |
| `indexleft.html` | 150 | WWW.KØBG.COM |

## 4. Rebuilt articles with no recovered original

_(none - every rebuilt article was mapped to an original)_

## 5. Spot checks against the rebuild's own AUDIT.md

### 5a. `coil-adjustment.html` - rebuild AUDIT.md flagged this as fully AI-generated

- Doc Jaccard **0.02** | sentence coverage **2%** | expansion **2.46x** (4261 rebuilt words vs 1735 original)

**CONFIRMED.** Coverage is essentially nil and the rebuild is 2.5x longer than the original. The bulk of the rebuilt coil-adjustment text is not traceable to the recovered `coil.html`. Treat its measurements and procedures as fabricated.

### 5b. `glossary.html` - rebuild AUDIT.md noted missing 'Strapping' entry

- Original glossary contains 'Strapping': **True**
- Rebuild glossary contains 'Strapping': **True**

## 6. Rebuild's AUDIT.md (verbatim)

```
# K0BG Content Audit

Audited: 2026-03-24
Articles: 16

## Summary

- Total specific claims audited: ~350
- Verified against source material: ~280
- Unverified (plausible additions): ~65
- Contradictions found & fixed: 4
- Internal inconsistencies found & fixed: 2
- Missing content: 2 items
- High-risk article (no source material): 1

## Corrections Applied

| # | File | Before | After | Reason |
|---|------|--------|-------|--------|
| 1 | `common-mode.html` | 7-turn impedance listed as 2.2 kohm | Corrected to 2.7 kohm | Source shows 6 turns = 2.2 kohm, 7 turns = 2.7 kohm |
| 2 | `rfi.html` | Advised "stack multiple beads" | Replaced with "multiple turns preferred over multiple beads" | Contradicted source guidance |
| 3 | `rfi.html` | No color burst tolerance range mentioned | Added 146.70-146.80 MHz range | Omission from source material |
| 4 | `wiring.html` | Powerpole color convention was softened/ambiguous | Clarified: red/black for power, other colors for motor/control | Contradicted source convention |
| 5 | `wiring.html` | Fuse distance stated as "12 inches" | Changed to "as close to battery as possible" | Contradicted source best practice |
| 6 | `safety.html` | Fuse distance stated as "18 inches" | Changed to "as close to battery as possible" | Contradicted source best practice; also inconsistent with wiring.html |

## Outstanding Issues

### High Priority

| Issue | File | Details |
|-------|------|---------|
| 5AG fuse dimensions | `tricks.html` | Article states "1/4 x 1-1/4 inch" but standard 5AG is 13/32" x 1-1/2". Needs correction or clarification. |
| Missing glossary term | `glossary.html` | "Strapping" is present in source material but absent from the glossary. Needs to be added. |
| AI-generated article | `coil-adjustment.html` | Entire article has no dedicated source material. All 17 specific claims are unverified. Physics checks pass but specific numbers (12 ohm on 40m, 3-5 ohm on 75m, 48" whip, 50 kHz shift, 4 ft spacing) are AI-generated. Needs disclaimer or source validation. |
| UNUN softening | `antenna-controllers.html` | Article says "broadband UNUN can also work" for SWR-sensing controllers, but source states fixed shunt coil is "the only correct matching." Should be tightened to reflect source or explicitly noted as editorial addition. |

### Low Priority / Informational

| Category | Details |
|----------|---------|
| Unverified but plausible | ~65 claims across all articles are reasonable additions not directly traceable to source. These include product names (Penetrox, No-Ox-Id, Scotch 130C), specific vehicle references (Ford F-150 2015), and practical advice ("full weekend at minimum," flat washer placement). |
| Outdated prices | "$30 Hustler lesson" in tricks.html may not reflect current pricing. |
| Omissions from source | RVs and "plastic-skinned" vehicles dropped from installation.html challenging vehicle list; reed switch bench test warning and Polyfuse reset time omitted from antenna-problems.html; discarded RG8 braid shielding tip omitted from rfi.html; MFJ 259B filter mention omitted from antenna-matching.html; SDC-100 stall current procedure ("not in manual") omitted from antenna-controllers.html. |
| Minor measurement discrepancy | abcs.html states quarter-wave on 20m is "16.5 feet" -- actual quarter-wave at 14.2 MHz is ~17.4 feet. May be intentional (shortened element) but worth reviewing. |
| Amplifier model suffix | amplifiers.html references "ALS-500M" but source says "ALS-500." The "M" suffix should be verified. |
| Coil dimension ambiguity | amplifiers.html mentions a "3.5 inch" coil dimension -- unclear whether source means diameter or length. |

## Article-by-Article Findings

---

### abcs.html

**Verdict: PASS WITH NOTES**

| Status | Claim / Issue |
|--------|---------------|
| ✅ | 22 specific claims verified against source material |
| ⚠️ | Quarter-wave on 20m stated as "16.5 feet" -- actual is ~17.4 feet |
| 🔍 | "Full weekend at minimum" for installation time -- unverified |
| 🔍 | "Not a Haynes manual, not a Chilton guide" -- unverified (editorial) |
| 🔍 | "Two-pound transceiver at 200 mph" -- unverified |
| 🔍 | "VHF/UHF in hybrids generally workable" -- unverified |
| 🔍 | "Remotable transceivers strongly preferred" -- unverified |
| 🔍 | 3 additional unverified claims |

---

### safety.html

**Verdict: PASS WITH NOTES**

| Status | Claim / Issue |
|--------|---------------|
| ✅ | 3 claims verified via cross-reference with other articles |
| ✅ | All physics checks correct |
| ✅ | Fuse distance FIXED -- changed from "18 inches" to "as close to battery as possible" |
| 🔍 | 10 claims unverified (no dedicated source material for this article) |

---

### bonding.html

**Verdict: PASS**

| Status | Claim / Issue |
|--------|---------------|
| ✅ | 27 claims verified -- very clean article |
| 🔍 | "Four-door sedan has eight hinges" -- unverified |
| 🔍 | "Flat washer between star washer and braid" -- unverified |
| 🔍 | Stainless steel recommendation for exhaust -- unverified |
| 🔍 | Corrosion inhibitor recommendation -- unverified |
| 🔍 | 1 additional unverified claim |

---

### wiring.html

**Verdict: PASS (after fixes)**

| Status | Claim / Issue |
|--------|---------------|
| ✅ | 21 claims verified |
| ✅ | Powerpole color convention FIXED -- clarified red/black for power |
| ✅ | Fuse distance FIXED -- changed from "12 inches" to "as close to battery as possible" |
| 🔍 | PP75/PP120 connector sizes -- unverified |
| 🔍 | Penetrox/No-Ox-Id product references -- unverified |
| 🔍 | Specific fuse sizing recommendations -- unverified |
| 🔍 | 0.5V drop test threshold -- unverified |
| 🔍 | Ford F-150 2015 date reference -- unverified |

---

### common-mode.html

**Verdict: PASS (after fix)**

| Status | Claim / Issue |
|--------|---------------|
| ✅ | 20 claims verified |
| ✅ | 7-turn impedance FIXED -- corrected from 2.2 kohm to 2.7 kohm |
| 🔍 | 2 unverified claims |

---

### rfi.html

**Verdict: PASS (after fixes)**

| Status | Claim / Issue |
|--------|---------------|
| ✅ | 19 claims verified |
| ✅ | "Stack beads" advice FIXED -- replaced with "multiple turns preferred" |
| ✅ | Color burst tolerance range ADDED (146.70-146.80 MHz) |
| ✅ | Cable damage warning for twisting -- already present in article |
| 🔍 | Discarded RG8 braid for older ignition shielding -- omitted from source |
| 🔍 | 3 additional unverified claims |

---

### installation.html

**Verdict: PASS WITH NOTES**

| Status | Claim / Issue |
|--------|---------------|
| ✅ | 14 claims verified |
| ⚠️ | RVs and "plastic-skinned" vehicles omitted from challenging vehicle list |
| 🔍 | Chilton manual reference -- unverified |
| 🔍 | Silicone sealant recommendation -- unverified |
| 🔍 | Projectile weight claim -- unverified |
| 🔍 | Interior temperature claim -- unverified |

---

### antenna-problems.html

**Verdict: PASS**

| Status | Claim / Issue |
|--------|---------------|
| ✅ | 24 claims verified -- cleanest article in batch |
| ⚠️ | Reed switch bench test warning omitted from source |
| ⚠️ | Polyfuse reset time omitted from source |
| 🔍 | Alternator voltage range -- unverified |
| 🔍 | Normal motor resistance figure -- unverified |
| 🔍 | 1 additional unverified claim |

---

### antenna-matching.html

**Verdict: PASS**

| Status | Claim / Issue |
|--------|---------------|
| ✅ | 27 claims verified -- cleanest article overall |
| ⚠️ | MFJ 259B filter mention omitted from source |

---

### antenna-controllers.html

**Verdict: PASS WITH NOTES**

| Status | Claim / Issue |
|--------|---------------|
| ✅ | 20 claims verified |
| ⚠️ | UNUN claim softened: article says "broadband UNUN can also work" but source says fixed shunt coil is "the only correct matching" |
| ⚠️ | SDC-100 stall current procedure ("not in manual") omitted |

---

### amplifiers.html

**Verdict: PASS WITH NOTES**

| Status | Claim / Issue |
|--------|---------------|
| ✅ | 21 claims verified |
| ✅ | All physics correct (7 dB calculation, S-unit calculation, I-squared noise) |
| 🔍 | "ALS-500M" suffix -- source says "ALS-500" |
| 🔍 | MOSFET push-pull circuit details -- unverified |
| 🔍 | 80A current draw figure -- unverified |
| 🔍 | SGC SG-500 and Mirage product mentions -- unverified |
| ⚠️ | 3.5" coil dimension -- ambiguous whether source means diameter or length |

---

### vhf-options.html

**Verdict: PASS**

| Status | Claim / Issue |
|--------|---------------|
| ✅ | 22 claims verified |
| 🔍 | NMO 3/4" hole size -- correct but not in source |
| 🔍 | Vendor names -- unverified |
| 🔍 | Antenna gain figures -- unverified |
| 🔍 | Handheld 10-20 dB improvement claim -- unverified |

---

### otr-rv.html

**Verdict: PASS WITH NOTES**

| Status | Claim / Issue |
|--------|---------------|
| ✅ | 17 claims verified |
| 🔍 | 400 Ah house bank figure -- unverified |
| 🔍 | Intermodulation from dual alternators -- unverified |
| 🔍 | 10-15 dB dipole advantage -- unverified |
| 🔍 | FT-240-31 part number -- unverified |
| 🔍 | Type 31/43 ferrite recommendation -- unverified |
| 🔍 | 10 AWG wire spec -- unverified |
| 🔍 | 12x12" steel plate -- unverified |
| 🔍 | Rubber-mounted cab isolation -- unverified |
| 🔍 | 8-10 turns through FT-240-31 -- unverified |
| 🔍 | 1 additional unverified claim |

---

### tricks.html

**Verdict: PASS WITH NOTES**

| Status | Claim / Issue |
|--------|---------------|
| ✅ | 28 claims verified |
| ❌ | 5AG fuse dimensions stated as "1/4 x 1-1/4 inch" -- standard 5AG is 13/32" x 1-1/2". NEEDS CORRECTION. |
| 🔍 | Scotch 130C product reference -- unverified |
| 🔍 | Crimp wing orientation detail -- unverified |
| 🔍 | Phillips screw opinion -- unverified (editorial) |
| 🔍 | "$30 Hustler lesson" -- unverified, possibly outdated |
| 🔍 | Stainless steel loss quantification -- unverified |
| 🔍 | 1 additional unverified claim |

---

### coil-adjustment.html

**Verdict: CAUTION**

| Status | Claim / Issue |
|--------|---------------|
| ⚠️ | Only 1 claim partially verified |
| ❌ | 17 specific claims unverified -- entire article AI-generated with no dedicated source material |
| 🔍 | 12 ohm impedance on 40m -- unverified, AI-generated |
| 🔍 | 3-5 ohm impedance on 75m -- unverified, AI-generated |
| 🔍 | 48" whip length recommendation -- unverified, AI-generated |
| 🔍 | 50 kHz frequency shift figure -- unverified, AI-generated |
| 🔍 | 4 foot spacing recommendation -- unverified, AI-generated |
| ⚠️ | Physics checks pass but specific numbers cannot be traced to any source |
| ❌ | HIGH RISK: Needs either source validation, expert review, or a visible disclaimer |

---

### glossary.html

**Verdict: PASS WITH NOTES**

| Status | Claim / Issue |
|--------|---------------|
| ✅ | 37 terms present, all definitions technically correct |
| ❌ | "Strapping" term is MISSING -- present in source but absent from glossary |
| 🔍 | B-CAN data rates -- specific number not in source (industry standard) |
| 🔍 | Maxifuse lower bound -- specific number not in source (industry standard) |
| 🔍 | Shadowing 6 dB figure -- specific number not in source (industry standard) |
| ✅ | Radiation resistance vs feed impedance distinction correctly handled |
| ✅ | Internal consistency across terms is good |

---

## Legend

| Marker | Meaning |
|--------|---------|
| ✅ | Verified against source material or confirmed correct |
| ⚠️ | Unverified, softened from source, or omitted -- review recommended |
| ❌ | Incorrect, missing, or high-risk -- action needed |
| 🔍 | Unverified addition -- plausible but not traceable to source |
```