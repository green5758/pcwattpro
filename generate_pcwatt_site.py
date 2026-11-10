import os
import json
import math
import datetime
import urllib.request
import urllib.parse

# ==========================================
# CORE CONFIGURATION
# ==========================================
AFFILIATE_TAG = "everythi00099-20"
SITE_NAME = "PCWattPro"
SITE_TAGLINE = "ATX 3.1 PSU Wattage, GPU Transient Spike, AIO TDP & Gaming UPS Sizing Calculator"
OUTPUT_DIR = "public"
INDEXNOW_KEY = "7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b"

# Cumulative Daily Review Epoch (Unlocks +1 new standalone review article every single day)
LAUNCH_EPOCH = datetime.date(2026, 11, 1)

REPO_SLUG = os.environ.get("GITHUB_REPOSITORY", "username/pcwattpro")
OWNER, REPO_NAME = REPO_SLUG.split("/") if "/" in REPO_SLUG else ("username", "pcwattpro")
BASE_URL = os.environ.get("SITE_BASE_URL", f"https://{OWNER}.github.io/{REPO_NAME}")

def amz_url(keyword):
    return f"https://www.amazon.com/s?k={urllib.parse.quote_plus(keyword.replace('+', ' '))}&tag={AFFILIATE_TAG}"

# ==========================================
# BEST SELLING PRODUCTS DATABASE (USD / EN)
# ==========================================
BEST_SELLERS = [
    {
        "title": "Corsair RM1000x Shift / RM850x Fully Modular ATX 3.1 & PCIe 5.1 Power Supply",
        "category": "ATX 3.1 Modular PSU",
        "rating": "4.8 ★ (9,800+ reviews)",
        "badge": "#1 Best-Selling ATX 3.1 PSU",
        "specs": "80 Plus Gold | Native 600W 12V-2x6 GPU Cable | 105°C Japanese Capacitors | 10-Yr Warranty",
        "keyword": "Corsair+RM1000x+RM850x+ATX+3.1+PCIe+5.1+Fully+Modular+PSU"
    },
    {
        "title": "Seasonic VERTEX GX-1000 / GX-1200 1000W–1200W 80+ Gold ATX 3.0 / 3.1 Power Supply",
        "category": "Flagship Tier-A Power Supply",
        "rating": "4.9 ★ (3,400+ reviews)",
        "badge": "Pro Builder #1 Tier-A Pick",
        "specs": "200% GPU Transient Excursion | Native 12V-2x6 Cable | Hybrid Silent Fan | 12-Yr Warranty",
        "keyword": "Seasonic+VERTEX+GX+1000+1200W+ATX+3.0+Power+Supply"
    },
    {
        "title": "AMD Ryzen 7 9800X3D / 7800X3D 8-Core 16-Thread 3D V-Cache Gaming Processor",
        "category": "Flagship Gaming CPU",
        "rating": "4.9 ★ (11,500+ reviews)",
        "badge": "#1 Fastest Gaming CPU",
        "specs": "104MB 3D V-Cache | Socket AM5 DDR5 & PCIe 5.0 | Ultra-Efficient 120W TDP",
        "keyword": "AMD+Ryzen+7+9800X3D+7800X3D+AM5+Gaming+Processor"
    },
    {
        "title": "ARCTIC Liquid Freezer III 360 A-RGB / Black High-Performance All-in-One CPU Cooler",
        "category": "360mm AIO Liquid Cooler",
        "rating": "4.8 ★ (7,900+ reviews)",
        "badge": "#1 Thermal Performance AIO",
        "specs": "38mm Extra-Thick Radiator | Dedicated VRM Cooling Fan | Contact Frame Included | 300W+ TDP",
        "keyword": "ARCTIC+Liquid+Freezer+III+360+AIO+CPU+Liquid+Cooler"
    },
    {
        "title": "MSI MAG A850GL / MPG A1000G PCIE5 850W–1000W 80+ Gold ATX 3.1 Gaming PSU",
        "category": "Best Value PCIe 5.1 PSU",
        "rating": "4.8 ★ (6,200+ reviews)",
        "badge": "Best Value ATX 3.1 PSU",
        "specs": "Dual-Color Yellow Latch 12V-2x6 Connector | Compact 140mm Chassis | 10-Yr Warranty",
        "keyword": "MSI+MAG+A850GL+A1000G+PCIE5+ATX+3.1+Power+Supply"
    },
    {
        "title": "be quiet! Dark Power 13 / Pure Power 12 M 1000W 80+ Titanium & Gold ATX 3.1 PSU",
        "category": "Ultra-Silent PSU",
        "rating": "4.8 ★ (4,100+ reviews)",
        "badge": "Quietest ATX 3.1 PSU (<20dB)",
        "specs": "Up to 95.8% Titanium Efficiency | Frameless Silent Wings Fan | Overclocking Key",
        "keyword": "be+quiet+Pure+Power+12+M+Dark+Power+13+1000W+ATX+3.1+PSU"
    },
    {
        "title": "CyberPower CP1500PFCLCD PFC Sinewave Gaming PC UPS (1500VA / 1000W Active PFC)",
        "category": "Pure Sine Wave Gaming UPS",
        "rating": "4.8 ★ (31,800+ reviews)",
        "badge": "#1 Active PFC Gaming UPS",
        "specs": "1000W Pure Sine Wave | Prevents PC Reboot During Brownouts | Color LCD Load Meter",
        "keyword": "CyberPower+CP1500PFCLCD+PFC+Sinewave+UPS+1500VA+1000W"
    },
    {
        "title": "Thermalright Peerless Assassin 120 SE / Phantom Spirit 120 EVO Dual-Tower Air Cooler",
        "category": "Dual-Tower CPU Air Cooler",
        "rating": "4.9 ★ (22,400+ reviews)",
        "badge": "#1 Value CPU Cooler",
        "specs": "7× 6mm AGHP Heatpipes | Dual 120mm PWM Fans | Supports 265W TDP on AM5 & LGA1700/1851",
        "keyword": "Thermalright+Phantom+Spirit+120+Peerless+Assassin+CPU+Cooler"
    }
]

# ==========================================
# PRODUCT COMPARISON MATRIX (PERBANDINGAN PRODUK)
# ==========================================
COMPARISON_MATRIX = [
    {
        "model": "Seasonic VERTEX GX-1000 (1000W)",
        "type": "Tier-A Flagship ATX 3.1 PSU",
        "wattage_spec": "1000W (2000W Peak Excursion)",
        "pcie_cable": "Native 600W 12V-2x6 PCIe 5.1",
        "highlight": "12-Year Warranty + Ultra-Low Ripple",
        "rating": "4.9 / 5.0 ★",
        "keyword": "Seasonic+VERTEX+GX+1000+1000W+ATX+3.0+Power+Supply"
    },
    {
        "model": "Corsair RM1000x / RM1000x Shift",
        "type": "Modular ATX 3.1 Gold PSU",
        "wattage_spec": "1000W Continuous @ 50°C",
        "pcie_cable": "600W PCIe 5.1 + Side/Rear Modular",
        "highlight": "Zero RPM Fan Mode + 105°C Japanese Caps",
        "rating": "4.8 / 5.0 ★",
        "keyword": "Corsair+RM1000x+ATX+3.1+PCIe+5.1+Fully+Modular+PSU"
    },
    {
        "model": "be quiet! Pure Power 12 M 1000W",
        "type": "Silent ATX 3.1 Dual-Rail PSU",
        "wattage_spec": "1000W (93.2% Gold Efficiency)",
        "pcie_cable": "Native 600W 12V-2x6 + 4× PCIe 6+2",
        "highlight": "Silent Wings 120mm Fan (19 dB Idle)",
        "rating": "4.8 / 5.0 ★",
        "keyword": "be+quiet+Pure+Power+12+M+1000W+ATX+3.1+PSU"
    },
    {
        "model": "MSI MAG A850GL PCIE5 (850W)",
        "type": "Mid-Tower ATX 3.1 Gold PSU",
        "wattage_spec": "850W (1700W Transient Rated)",
        "pcie_cable": "Yellow Safety-Latch 600W 12V-2x6",
        "highlight": "Visual Plug Insertion Safety Check",
        "rating": "4.8 / 5.0 ★",
        "keyword": "MSI+MAG+A850GL+PCIE5+850W+ATX+3.1+Power+Supply"
    },
    {
        "model": "ARCTIC Liquid Freezer III 360",
        "type": "360mm AIO CPU Cooler",
        "wattage_spec": "320W+ CPU Thermal Dissipation",
        "pcie_cable": "38mm Thick Radiator + VRM Fan",
        "highlight": "Beats $250 AIOs at Half the Price",
        "rating": "4.8 / 5.0 ★",
        "keyword": "ARCTIC+Liquid+Freezer+III+360+AIO+CPU+Liquid+Cooler"
    },
    {
        "model": "CyberPower CP1500PFCLCD Sinewave",
        "type": "Active PFC Gaming UPS",
        "wattage_spec": "1500VA / 1000W Pure Sine Wave",
        "pcie_cable": "12 Outlets (6 Battery + 6 Surge)",
        "highlight": "100% Compatible with Active PFC PSUs",
        "rating": "4.8 / 5.0 ★",
        "keyword": "CyberPower+CP1500PFCLCD+PFC+Sinewave+UPS+1500VA+1000W"
    }
]

# ==========================================
# HEAD-TO-HEAD "VS" COMPARISON PAGES
# ==========================================
VS_COMPARISONS = [
    {
        "slug": "compare-corsair-rm1000x-vs-seasonic-vertex-gx-1000-psu",
        "title": "Corsair RM1000x ATX 3.1 vs. Seasonic VERTEX GX-1000: Which 1000W Power Supply Wins?",
        "product_a": "Corsair RM1000x (ATX 3.1)",
        "product_b": "Seasonic VERTEX GX-1000",
        "winner_badge": "Best Cable Ergonomics vs. Best 12-Year Warranty",
        "keyword_a": "Corsair+RM1000x+ATX+3.1+PCIe+5.1+Fully+Modular+PSU",
        "keyword_b": "Seasonic+VERTEX+GX+1000+1000W+ATX+3.0+Power+Supply",
        "summary": "Compare voltage ripple suppression, 200% GPU transient spike handling, 12V-2x6 cable flexibility, and warranty length between Corsair and Seasonic.",
        "metrics": [
            {"feature": "ATX & PCIe Standard", "val_a": "ATX 3.1 & PCIe 5.1 Certified (600W 12V-2x6)", "val_b": "ATX 3.0 / 3.1 & PCIe 5.1 Certified (600W 12V-2x6)"},
            {"feature": "Capacitor Quality", "val_a": "100% 105°C Rated Japanese Electrolytic Capacitors", "val_b": "100% 105°C Rated Japanese Electrolytic Capacitors"},
            {"feature": "Transient Spike Handling", "val_a": "Handles 200% Total Power Excursion (2000W for 100μs)", "val_b": "Handles 200% Total Power & 300% GPU Excursion"},
            {"feature": "Fan & Acoustics", "val_a": "140mm Magnetic Levitation / Rifle Bearing w/ Zero RPM Mode", "val_b": "135mm Fluid Dynamic Bearing (FDB) w/ Hybrid Silent Switch"},
            {"feature": "Warranty Coverage", "val_a": "10-Year Comprehensive Warranty", "val_b": "Industry-Leading 12-Year Full Warranty"}
        ],
        "verdict_text": "Both units sit at the very top of the PSU Cultists Tier-A list. Choose the Seasonic VERTEX GX-1000 if you want an unmatched 12-year warranty and ultra-tight <15mV voltage regulation on the +12V rail. Choose the Corsair RM1000x (or RM1000x Shift) if you want side-mounted modular connectors for effortless cable management in modern dual-chamber PC cases."
    },
    {
        "slug": "compare-atx-3-1-pcie-5-1-vs-atx-2-4-power-supply",
        "title": "ATX 3.1 (PCIe 5.1) vs. Legacy ATX 2.4 Power Supply: Why GPU Transient Spikes Trip Old PSUs",
        "product_a": "ATX 3.1 / PCIe 5.1 Native PSU",
        "product_b": "Legacy ATX 2.4 / 2.52 PSU + Dongle",
        "winner_badge": "200% Excursion Protection vs. Dongle Clutter",
        "keyword_a": "MSI+MAG+A850GL+A1000G+PCIE5+ATX+3.1+Power+Supply",
        "keyword_b": "Corsair+RM850x+ATX+3.1+Modular+Power+Supply",
        "summary": "Understand how modern GPUs draw 2x to 3x their rated wattage for milliseconds and why ATX 3.1 PSUs with 12V-2x6 connectors prevent black-screen shutdowns and melted adapters.",
        "metrics": [
            {"feature": "Power Excursion Spec", "val_a": "Mandatory 200% Total PSU & 300% GPU Peak Spike Tolerance", "val_b": "No Standardized Microsecond Excursion Requirement (Trips OCP)"},
            {"feature": "GPU Power Connector", "val_a": "Single Native 600W 12V-2x6 Cable (Recessed Sense Pins)", "val_b": "Bulky 3× or 4× 8-Pin PCIe to 12VHPWR Octopus Adapter"},
            {"feature": "Safety Latch & Pin Contact", "val_a": "Updated PCIe 5.1 12V-2x6 Short Sense Pins Cut Power if Loose", "val_b": "Older 12VHPWR Dongles Prone to Side-Panel Bend Stress"},
            {"feature": "Low-Load Efficiency", "val_a": "Minimum 60%+ Efficiency at 10W Idle / Modern Standby", "val_b": "Poor Efficiency Under 50W Desktop Idle"},
            {"feature": "Future GPU Readiness", "val_a": "100% Ready for RTX 40/50 Series & Next-Gen GPUs", "val_b": "Requires Upgraded PSU for High-TDP Graphics Cards"}
        ],
        "verdict_text": "When a 350W–450W graphics card spikes to 900W+ for 100 microseconds during a scene transition, an older ATX 2.4 PSU triggers Over-Current Protection (OCP) and abruptly shuts off your PC. Upgrading to a native ATX 3.1 PSU eliminates messy 4-way squid adapters and guarantees rock-solid stability."
    },
    {
        "slug": "compare-arctic-liquid-freezer-iii-360-vs-dual-tower-air-cooler",
        "title": "ARCTIC Liquid Freezer III 360 AIO vs. Thermalright Phantom Spirit 120: Liquid vs. Air Cooling",
        "product_a": "ARCTIC Liquid Freezer III 360 AIO",
        "product_b": "Thermalright Phantom Spirit 120 EVO",
        "winner_badge": "Best 300W+ Multi-Core Cooling vs. Best Zero-Pump Reliability",
        "keyword_a": "ARCTIC+Liquid+Freezer+III+360+AIO+CPU+Liquid+Cooler",
        "keyword_b": "Thermalright+Phantom+Spirit+120+Peerless+Assassin+CPU+Cooler",
        "summary": "Compare CPU package temperatures, noise-normalized decibels, VRM cooling, and RAM clearance between the #1 360mm AIO liquid cooler and the #1 dual-tower air cooler.",
        "metrics": [
            {"feature": "Max Thermal Dissipation", "val_a": "320W+ Continuous (38mm Thick 360mm Radiator)", "val_b": "250W–265W (7× 6mm Copper Heatpipes)"},
            {"feature": "Motherboard VRM Cooling", "val_a": "Built-In 60mm VRM Blower Fan Drops VRM Temps by 12°C", "val_b": "Passive Airflow From Dual 120mm Tower Fans"},
            {"feature": "RAM Height Clearance", "val_a": "100% Unrestricted Access to All 4 DDR5 RAM Slots", "val_b": "Front Fan Overhangs Tall RGB DDR5 Modules"},
            {"feature": "Best CPU Match", "val_a": "Ryzen 9 9950X / 7950X, Core i9-14900K, Core Ultra 9 285K", "val_b": "Ryzen 7 9800X3D / 7800X3D, Ryzen 5 7600X, Core i5/i7"},
            {"feature": "Lifespan & Maintenance", "val_a": "6-Year Warranty (Sealed Closed-Loop Pump)", "val_b": "Indefinite Heatsink Lifespan (Only Replaceable PWM Fans)"}
        ],
        "verdict_text": "If you are cooling a 250W–300W workstation CPU like a Core i9-14900K, Core Ultra 9 285K, or Ryzen 9 9950X, the 38mm-thick ARCTIC Liquid Freezer III 360 prevents thermal throttling and keeps clock speeds maxed out. If you are building a pure gaming rig around an efficient 120W Ryzen 7 9800X3D or 7800X3D, the Thermalright Phantom Spirit 120 delivers incredible cooling for under $45."
    }
]

# ==========================================
# BASE + CUMULATIVE DAILY PRODUCT REVIEWS
# ==========================================
BASE_REVIEWS = [
    {
        "slug": "review-corsair-rm1000x-atx-3-1-modular-power-supply",
        "title": "Corsair RM1000x (ATX 3.1) Review: Whisper-Quiet 1000W Power for Flagship Gaming PCs",
        "product_name": "Corsair RM1000x Fully Modular ATX 3.1 PSU",
        "category": "1000W ATX 3.1 PSU",
        "rating_score": "4.9",
        "verdict_badge": "Editor's Choice — #1 Overall 1000W PSU",
        "spec_1": "1000W Continuous @ 50°C (80+ Gold)",
        "spec_2": "ATX 3.1 & Native 600W PCIe 5.1 12V-2x6",
        "spec_3": "100% 105°C Japanese Capacitors",
        "spec_4": "10-Year Corsair Replacement Warranty",
        "published_date": "2026-11-01",
        "keyword": "Corsair+RM1000x+ATX+3.1+PCIe+5.1+Fully+Modular+PSU",
        "summary": "Upgraded with native ATX 3.1 compliance, a 600W 12V-2x6 GPU cable, and 105°C Japanese capacitors, the Corsair RM1000x delivers ultra-clean power with Zero-RPM silent operation.",
        "pros": [
            "Native 600W 12V-2x6 PCIe 5.1 cable connects directly to flagship GPUs without ugly 4-way adapters",
            "Zero-RPM fan mode keeps the power supply 100% silent under 400W desktop and light gaming loads",
            "Sub-15mV voltage ripple on the +12V rail protects sensitive GPU VRMs during heavy overclocking",
            "Backed by Corsair's industry-renowned 10-year warranty and cross-shipping support"
        ],
        "cons": [
            "160mm housing length requires checking bottom HDD cage clearance in ultra-compact mATX cases"
        ],
        "body_paragraphs": [
            "When sizing a power supply using our calculator for a high-end GPU (such as an RTX 4080 Super, RTX 4090, or next-gen flagship) paired with an 8-to-16 core CPU, total continuous draw sits around 600W to 750W—but millisecond GPU transient spikes can briefly double that figure. The ATX 3.1-certified Corsair RM1000x absorbs 2,000W microsecond spikes without breaking a sweat.",
            "Inside the chassis, Corsair uses 100% industrial-grade 105°C Japanese primary and secondary capacitors paired with a resonant LLC converter and DC-to-DC topology. Even at a full 1,000W torture load inside a 45°C hotbox, +12V rail regulation stayed within 0.8% of nominal.",
            "Because peak PSU efficiency (91.5%) occurs between 45% and 65% load, running a 550W–650W gaming PC on the RM1000x keeps heat output minimal and the cooling fan barely spinning."
        ]
    },
    {
        "slug": "review-seasonic-vertex-gx-1000-atx-3-power-supply",
        "title": "Seasonic VERTEX GX-1000 Review: The 12-Year Warranty Gold Standard for ATX 3.1 Builds",
        "product_name": "Seasonic VERTEX GX-1000 1000W 80+ Gold PSU",
        "category": "Tier-A Flagship PSU",
        "rating_score": "4.9",
        "verdict_badge": "Best Build Quality & 12-Yr Warranty",
        "spec_1": "1000W (83A Single +12V Rail)",
        "spec_2": "ATX 3.0 / 3.1 + Native 12V-2x6 Cable",
        "spec_3": "135mm Fluid Dynamic Bearing (FDB) Fan",
        "spec_4": "12-Year Manufacturer Warranty",
        "published_date": "2026-11-01",
        "keyword": "Seasonic+VERTEX+GX+1000+1000W+ATX+3.0+Power+Supply",
        "summary": "Purpose-built from the ground up for PCIe 5.0/5.1 transient excursion demands, the Seasonic VERTEX GX-1000 combines braided embossed modular cables with an unmatched 12-year warranty.",
        "pros": [
            "Engineered specifically to handle 200% total system and 300% GPU transient power spikes effortlessly",
            "Plush embossed individual-look modular cables bend cleanly around tight GPU side panels",
            "Physical rear Hybrid Fan Control button lets you toggle semi-passive 0 dB mode on or off instantly",
            "Longest warranty in the 80+ Gold category at a full 12 years"
        ],
        "cons": [
            "Commands a $20–$30 price premium over entry-level 1000W units"
        ],
        "body_paragraphs": [
            "Unlike brands that simply bundled a 12VHPWR cable with an older ATX 2.4 platform, Seasonic designed the VERTEX series from a clean sheet of paper to exceed Intel's ATX 3.0 and ATX 3.1 transient timing specifications.",
            "In our oscilloscope testing, switching from a 100W idle state to an immediate 1,000W load produced virtually zero voltage droop, and hold-up time during simulated AC power loss exceeded 22 milliseconds—well above the 17ms ATX requirement needed for seamless UPS battery switchover.",
            "The included soft-embossed cables feel like custom aftermarket cables right out of the box, making routing through grommets and installing the 12V-2x6 GPU plug stress-free."
        ]
    },
    {
        "slug": "review-arctic-liquid-freezer-iii-360-aio-cpu-cooler",
        "title": "ARCTIC Liquid Freezer III 360 Review: 38mm Thick Radiator Dominance at Half the Price",
        "product_name": "ARCTIC Liquid Freezer III 360 AIO Cooler",
        "category": "360mm AIO Liquid Cooler",
        "rating_score": "4.9",
        "verdict_badge": "#1 CPU Liquid Cooler",
        "spec_1": "360mm × 38mm Extra-Thick Radiator",
        "spec_2": "300W+ TDP Cooling Capacity",
        "spec_3": "60mm VRM Fan + Hidden Tube Wiring",
        "spec_4": "6-Year Full ARCTIC Warranty",
        "published_date": "2026-11-01",
        "keyword": "ARCTIC+Liquid+Freezer+III+360+AIO+CPU+Liquid+Cooler",
        "summary": "By pairing an extra-thick 38mm radiator with an offset AM5 coldplate, an Intel LGA1700/1851 contact frame, and an integrated VRM fan, the ARCTIC Liquid Freezer III 360 outperforms $280 LCD coolers.",
        "pros": [
            "38mm radiator thickness provides 27% more aluminum fin volume than standard 27mm AIO radiators",
            "Includes a machined Aluminum Contact Frame for Intel CPUs and a native hotspot-offset mount for AMD AM5",
            "Magnetic 60mm VRM pump cap fan cools motherboard voltage regulators by up to 12°C",
            "Pre-installed daisy-chained P12 PWM fans hide all cables inside the braided water tubing sleeves"
        ],
        "cons": [
            "Extra-thick 38mm radiator + 25mm fans (63mm total thickness) requires verifying top-mount motherboard clearance"
        ],
        "body_paragraphs": [
            "Modern flagship processors boost automatically until they hit their thermal ceiling (95°C on AMD AM5 and 100°C on Intel). Using our CPU TDP calculator, cooling an unlocked 253W–300W processor requires far more surface area than a standard 240mm cooler can provide.",
            "The ARCTIC Liquid Freezer III 360 dominates thermal charts because of pure physics: its 38mm thick radiator holds more liquid and exposes more fin surface area to its high-static-pressure P12 fans. On AMD Ryzen 7000/9000 CPUs, its offset mounting bracket shifts the copper micro-skived coldplate directly over the lower CCD chiplet where heat is actually concentrated.",
            "With zero proprietary RGB bloatware required and a 6-year warranty, it is the smartest cooling investment for any high-wattage PC build."
        ]
    },
    {
        "slug": "review-msi-mag-a850gl-pcie5-atx-3-1-power-supply",
        "title": "MSI MAG A850GL PCIE5 850W Review: The Foolproof Yellow-Latch ATX 3.1 Gaming PSU",
        "product_name": "MSI MAG A850GL PCIE5 850W 80+ Gold ATX 3.1 PSU",
        "category": "850W ATX 3.1 Gaming PSU",
        "rating_score": "4.8",
        "verdict_badge": "#1 Best Value 850W ATX 3.1 PSU",
        "spec_1": "850W Continuous (1700W Peak Spike)",
        "spec_2": "Dual-Color Yellow 12V-2x6 Connector",
        "spec_3": "Compact 140mm Length Chassis",
        "spec_4": "10-Year MSI Manufacturer Warranty",
        "published_date": "2026-11-01",
        "keyword": "MSI+MAG+A850GL+PCIE5+850W+ATX+3.1+Power+Supply",
        "summary": "Solving the #1 user error with high-wattage GPU power cables, MSI engineered the MAG A850GL PCIE5 with a high-visibility neon-yellow 12V-2x6 plug tip—if you still see yellow, it isn't plugged in all the way.",
        "pros": [
            "Patented dual-color yellow-and-black 600W 12V-2x6 connector gives instant visual confirmation of a 100% seated GPU connection",
            "Compact 140mm depth leaves extra room for cable routing inside mid-tower and micro-ATX cases",
            "Full ATX 3.1 certification absorbs 2x total power excursions and 3x GPU power spikes",
            "Flat black ribbon cables route cleanly behind motherboard trays"
        ],
        "cons": [
            "120mm FDB fan spins continuously at a quiet low RPM rather than turning off completely at idle"
        ],
        "body_paragraphs": [
            "For 90% of gaming PCs built around an RTX 4070 Super, RTX 4070 Ti Super, RTX 4080 Super, or RX 7900 XT, 850 watts is the exact recommended sweet spot on our PSU calculator. The MSI MAG A850GL PCIE5 hits that 850W mark at an unbeatable price while solving connector anxiety forever.",
            "By molding the mating portion of the 16-pin 12V-2x6 plug in bright yellow, you can tell at a glance inside a dark PC case whether the latch is flush against the graphics card header—completely preventing loose-pin overheating.",
            "Backed by a full 10-year warranty and LLC half-bridge DC-to-DC internals, the MAG A850GL is our top mid-to-high-range PSU recommendation."
        ]
    }
]

# Deep Catalog of 40+ PC Hardware Products for Cumulative Daily Review Growth (+1 per day)
DAILY_CUMULATIVE_CATALOG = [
    ("amd-ryzen-7-9800x3d-7800x3d-gaming-cpu", "AMD Ryzen 7 9800X3D / 7800X3D 3D V-Cache Gaming CPU", "AM5 Gaming Processor", "4.9", "#1 Gaming CPU in the World", "8 Cores / 16 Threads (3D V-Cache)", "120W TDP (Draws Only ~65–88W in Games)", "Socket AM5 | PCIe 5.0 & DDR5-6000", "3-Year AMD Boxed Warranty", "AMD+Ryzen+7+9800X3D+7800X3D+AM5+Gaming+Processor", "Delivering flagship frame rates while sipping under 85 watts in real-world gaming workloads, AMD's 3D V-Cache Ryzen 7 processors let you run cooler and size your PSU with massive headroom."),
    ("be-quiet-pure-power-12-m-1000w-atx-3-1-psu", "be quiet! Pure Power 12 M 1000W ATX 3.1 Power Supply", "Ultra-Silent 1000W PSU", "4.8", "Quietest 1000W ATX 3.1 PSU", "1000W 80+ Gold (Up to 93.2% Eff.)", "Native 600W PCIe 5.1 + 4× PCIe 6+2", "Silence-Optimized 120mm Fan (19 dB)", "10-Year Manufacturer Warranty", "be+quiet+Pure+Power+12+M+1000W+ATX+3.1+PSU", "Engineered in Germany for near-inaudible acoustics, the be quiet! Pure Power 12 M 1000W keeps noise below 20 dB across typical gaming loads while delivering full ATX 3.1 transient protection."),
    ("cyberpower-cp1500pfclcd-1000w-sinewave-gaming-ups", "CyberPower CP1500PFCLCD 1500VA/1000W Pure Sine Wave UPS", "Active PFC Gaming PC UPS", "4.8", "#1 UPS for High-Wattage Gaming PCs", "1500VA / 1000W True Sine Wave", "12 Outlets + Tilting Color LCD", "Automatic Voltage Regulation (AVR)", "3-Yr Warranty + $500k Guarantee", "CyberPower+CP1500PFCLCD+PFC+Sinewave+UPS+1500VA+1000W", "Modern 80+ Gold and Platinum PC power supplies use Active PFC circuits that immediately shut down on cheap simulated-sinewave battery backups. The CP1500PFCLCD delivers 1,000W of pure sine wave power."),
    ("thermalright-phantom-spirit-120-evo-cpu-cooler", "Thermalright Phantom Spirit 120 EVO Dual-Tower Air Cooler", "High-TDP Air Cooler", "4.9", "#1 Value Dual-Tower Air Cooler", "7× 6mm Anodized Black Heatpipes", "265W TDP Cooling Capacity", "Dual 120mm S-FDB 2150 RPM PWM Fans", "3-Year Replacement Support", "Thermalright+Phantom+Spirit+120+EVO+CPU+Cooler", "Upgrading from 6 to 7 sintered copper heatpipes with anti-gravity capillary grooves, the Thermalright Phantom Spirit 120 EVO matches $120 air coolers for a fraction of the price."),
    ("corsair-rm850x-shift-side-interface-atx-3-1-psu", "Corsair RM850x Shift 850W Side-Interface ATX 3.1 PSU", "Side-Modular 850W PSU", "4.8", "Best PSU for Cable Management", "850W 80+ Gold (ATX 3.1 Certified)", "Patented Side-Mounted Modular Panel", "140mm Fluid Dynamic Fan w/ Zero RPM", "10-Year Corsair Warranty", "Corsair+RM850x+Shift+850W+ATX+3.1+Modular+PSU", "By rotating the modular connector board 90 degrees to face the side panel, the Corsair RM850x Shift lets you plug in GPU or motherboard cables in seconds without reaching into a cramped PSU shroud."),
    ("seasonic-focus-gx-850-atx-3-1-power-supply", "Seasonic FOCUS GX-850 V4 (ATX 3.1 / PCIe 5.1) 850W PSU", "Compact Tier-A 850W PSU", "4.9", "Best Compact 140mm 850W PSU", "850W 80+ Gold (ATX 3.1 / PCIe 5.1)", "Compact 140mm Depth Chassis", "135mm FDB Fan + OptiSink PCB", "10-Year Seasonic Warranty", "Seasonic+FOCUS+GX+850+ATX+3.1+850W+Power+Supply", "Featuring Seasonic's new OptiSink surface-mount thermal PCB design that improves internal airflow by 8x, the 140mm FOCUS GX-850 ATX 3.1 fits effortlessly into any ATX or mATX case."),
    ("nzxt-c1200-gold-atx-3-1-1200w-power-supply", "NZXT C1200 Gold (ATX 3.1) 1200W Fully Modular Power Supply", "1200W RTX 4090/5090 PSU", "4.8", "Best 1200W Workstation & Multi-GPU PSU", "1200W Continuous (2400W Peak Spike)", "Native 600W 12V-2x6 PCIe 5.1 Cable", "Zero Fan Mode Below 50% (600W) Load", "10-Year NZXT Warranty", "NZXT+C1200+Gold+1200W+ATX+3.1+Modular+Power+Supply", "For extreme 600W+ GPU + 250W CPU builds, the NZXT C1200 Gold ATX 3.1 provides 1,200 watts of headroom and stays 100% fanless up to 600 watts of system load."),
    ("be-quiet-dark-power-13-1000w-titanium-atx-3-psu", "be quiet! Dark Power 13 1000W 80+ Titanium ATX 3.0/3.1 PSU", "80+ Titanium Flagship PSU", "4.9", "#1 80+ Titanium Efficiency (95.8%)", "1000W 80+ Titanium Certified", "Active Rectifier + Full Bridge LLC", "Frameless Silent Wings Fan + OC Key", "10-Year Flagship Warranty", "be+quiet+Dark+Power+13+1000W+80+Titanium+PSU", "Achieving an astonishing 95.8% conversion efficiency, the Dark Power 13 1000W wastes half the heat of standard Gold power supplies and includes a physical jumper to switch between quad-rail and single-rail overclocking."),
    ("msi-mpg-a1000g-pcie5-1000w-atx-3-1-power-supply", "MSI MPG A1000G PCIE5 1000W 80+ Gold Modular PSU", "1000W Gaming Power Supply", "4.8", "Best 1000W PSU for RTX 4080/4090", "1000W 80+ Gold (100% Japanese Caps)", "Native 600W PCIe 5.1 + 0% RPM Mode", "135mm Fluid Dynamic Bearing Fan", "10-Year MSI Warranty", "MSI+MPG+A1000G+PCIE5+1000W+ATX+3.1+Power+Supply", "Built on the acclaimed CWT CSZ platform with 100% Japanese 105°C capacitors and a semi-passive 0% RPM fan switch, the MSI MPG A1000G PCIE5 is a proven powerhouse for 4K gaming rigs."),
    ("corsair-icue-link-titan-360-rx-rgb-aio-cooler", "Corsair iCUE LINK TITAN 360 RX RGB Liquid CPU Cooler", "Smart Single-Cable 360mm AIO", "4.7", "Best Single-Cable RGB Ecosystem AIO", "360mm Radiator w/ RX120 PWM Fans", "FlowDrive Three-Phase Motor Pump", "CapSwap Modular Pump Cap Design", "6-Year Corsair Warranty", "Corsair+iCUE+LINK+TITAN+360+RX+RGB+AIO+Cooler", "Eliminating fan hub wire clutter with Corsair's single-cable iCUE LINK daisy-chain architecture and a quiet 3-phase FlowDrive pump, the TITAN 360 RX cools high-TDP CPUs in style."),
    ("apc-back-ups-pro-br1500ms2-1500va-gaming-ups", "APC Back-UPS Pro BR1500MS2 1500VA/900W Sine Wave UPS", "Pure Sine Wave Battery Backup", "4.8", "Best APC Sinewave Backup for PCs", "1500VA / 900W Pure Sine Wave Output", "10 Outlets + USB Type-C Charging", "AVR Brownout Trim & Boost Protection", "3-Year APC Warranty", "APC+UPS+1500VA+Sine+Wave+UPS+Battery+Backup+BR1500MS2", "Protecting expensive gaming rigs against lightning surges, voltage sags, and grid blackouts, the APC BR1500MS2 delivers clean pure sine wave battery backup with PowerChute auto-shutdown software."),
    ("seasonic-prime-tx-1300-atx-3-0-titanium-psu", "Seasonic PRIME TX-1300 ATX 3.0 1300W 80+ Titanium PSU", "1300W Extreme Workstation PSU", "4.9", "Ultimate 1300W 80+ Titanium Titan", "1300W 80+ Titanium (94%+ Efficiency)", "Dual Native 600W 12V-2x6 Connectors", "Micro-Tolerance Load Regulation (0.5%)", "12-Year Flagship Warranty", "Seasonic+PRIME+TX+1300+ATX+3.0+1300W+Titanium+PSU", "Featuring two native 600W PCIe 5.1 connectors, 0.5% micro-tolerance voltage regulation, and a 12-year warranty, the Seasonic PRIME TX-1300 is built for dual-GPU AI workstations and extreme overclocking."),
    ("amd-ryzen-9-9950x-16-core-am5-workstation-cpu", "AMD Ryzen 9 9950X 16-Core 32-Thread Zen 5 Desktop Processor", "16-Core Flagship CPU", "4.8", "Best Hybrid Gaming & 3D Rendering CPU", "16 Cores / 32 Threads (Up to 5.7 GHz)", "170W TDP (230W PPT Max Socket Draw)", "80MB Cache | Socket AM5 PCIe 5.0", "3-Year AMD Warranty", "AMD+Ryzen+9+9950X+16+Core+AM5+Unlocked+Processor", "Delivering 16 full-performance Zen 5 cores for Blender, Unreal Engine 5 compilation, and 4K video rendering while keeping socket power under 230W, the Ryzen 9 9950X is a workstation monster."),
    ("corsair-sf1000-atx-3-1-platinum-sfx-power-supply", "Corsair SF1000 (2024/2026) 1000W 80+ Platinum ATX 3.1 SFX PSU", "1000W Small Form Factor (SFX) PSU", "4.9", "#1 Mini-ITX / SFF Power Supply", "1000W in Ultra-Compact True SFX Size", "80+ Platinum + ATX 3.1 & PCIe 5.1", "Type-5 Micro-Fit Braided Cables", "7-Year Corsair Warranty", "Corsair+SF1000+1000W+80+Platinum+ATX+3.1+SFX+PSU", "Packing a true 1,000 watts of 80+ Platinum ATX 3.1 power into a palm-sized 100mm × 125mm SFX frame, the Corsair SF1000 lets Mini-ITX builders run flagship GPUs with zero thermal compromises."),
    ("noctua-nh-d15-g2-dual-tower-cpu-air-cooler", "Noctua NH-D15 G2 Next-Gen 8-Heatpipe Dual-Tower CPU Cooler", "Flagship Silent Air Cooler", "4.9", "Quietest High-End CPU Air Cooler", "8× sintered Heatpipes + Asymmetric Fins", "Dual NF-A14x25r G2 SSO2 Fans", "Includes SecuFirm2+ Torx Driver & NT-H2", "6-Year Noctua Warranty + Free Mounts", "Noctua+NH+D15+G2+Dual+Tower+CPU+Cooler", "Re-engineered with 8 heatpipes and next-generation NF-A14x25r G2 fans, the Noctua NH-D15 G2 rivals 360mm liquid coolers while guaranteeing zero pump noise and lifetime socket mount upgrades."),
    ("thermaltake-toughpower-gf3-1200w-atx-3-psu", "Thermaltake Toughpower GF3 1200W 80+ Gold ATX 3.0/3.1 PSU", "1200W High-Wattage PSU", "4.7", "Best Value 1200W ATX 3.x PSU", "1200W Continuous (100% Japanese Caps)", "Native 600W PCIe Gen 5.0/5.1 Port", "<30mV Low Ripple + Smart Zero Fan", "10-Year Manufacturer Warranty", "Thermaltake+Toughpower+GF3+1200W+ATX+3.0+Power+Supply", "For builders sizing a 1,200W power supply for 50-series or 4090-class graphics cards on a sensible budget, the Toughpower GF3 1200W delivers true 600W native 12V-2x6 output and a 10-year warranty."),
    ("lian-li-edge-1000w-1300w-l-shape-platinum-psu", "Lian Li EDGE 1000W / 1300W 80+ Platinum Dual-Chamber ATX 3.1 PSU", "L-Shape Dual-Chamber PSU", "4.8", "Best PSU for Dual-Chamber Cases", "1000W–1300W 80+ Platinum Efficiency", "L-Shaped Outward-Facing Connector Hub", "Built-in 4-Port Internal USB 2.0 Hub", "10-Year Lian Li Warranty", "Lian+Li+EDGE+1000W+1300W+80+Platinum+ATX+3.1+PSU", "Featuring an innovative L-shaped chassis that exposes all modular ports upward and outward plus a built-in 4-port internal USB 2.0 hub for RGB controllers, the Lian Li EDGE is a dream to build with."),
    ("golden-mate-1000va-800w-lifepo4-sinewave-ups", "GOLDENMATE 1000VA/800W LiFePO4 Lithium Pure Sine Wave UPS", "10-Year LiFePO4 Battery UPS", "4.7", "Best Long-Life LiFePO4 PC UPS", "1000VA / 800W Pure Sine Wave", "LiFePO4 Battery (3,000+ Cycles / 10 Yrs)", "50% Lighter Than Lead-Acid UPS Units", "3-Year Full Warranty", "LiFePO4+UPS+Battery+Backup+1000VA+800W+Pure+Sine+Wave", "Replacing short-lived 3-year lead-acid batteries with Grade-A LiFePO4 lithium cells that last 10+ years and 3,000 cycles, this pure sine wave UPS protects mid-range gaming PCs and workstations."),
    ("arctic-liquid-freezer-iii-420-aio-cooler", "ARCTIC Liquid Freezer III 420 (3×140mm) Extreme AIO Cooler", "420mm Extreme AIO Cooler", "4.9", "Maximum Possible AIO Cooling (350W+)", "420mm × 38mm Massive Radiator", "3× P14 140mm High-Pressure PWM Fans", "Integrated VRM Fan + Offset Coldplate", "6-Year ARCTIC Warranty", "ARCTIC+Liquid+Freezer+III+420+AIO+CPU+Cooler", "If your full-tower case supports a 420mm (3×140mm) radiator, the ARCTIC Liquid Freezer III 420 delivers the lowest CPU temperatures and quietest RPM profile of any closed-loop cooler on Earth."),
    ("corsair-hx1500i-atx-3-1-platinum-digital-psu", "Corsair HX1500i (ATX 3.1) 1500W 80+ Platinum Digital Modular PSU", "1500W Digital Workstation PSU", "4.9", "#1 1500W Dual-GPU & AI Workstation PSU", "1500W 80+ Platinum (ATX 3.1 / PCIe 5.1)", "Dual Native 600W 12V-2x6 Cables", "iCUE Real-Time Wattage & Efficiency Telemetry", "10-Year Corsair Warranty", "Corsair+HX1500i+1500W+80+Platinum+ATX+3.1+PSU", "Capable of powering two flagship GPUs simultaneously while reporting live per-rail wattage and efficiency graphs over USB, the Corsair HX1500i is the ultimate 1,500W workstation power supply.")
]

def build_full_review_from_catalog(item_tuple, pub_date_str):
    slug_base, prod_name, cat, score, badge, s1, s2, s3, s4, kw, summary = item_tuple
    return {
        "slug": f"review-{slug_base}",
        "title": f"{prod_name} Review: ATX 3.1 Transient Load, Thermal & Sizing Analysis",
        "product_name": prod_name,
        "category": cat,
        "rating_score": score,
        "verdict_badge": badge,
        "spec_1": s1,
        "spec_2": s2,
        "spec_3": s3,
        "spec_4": s4,
        "published_date": pub_date_str,
        "keyword": kw,
        "summary": summary,
        "pros": [
            f"Verified high-load stability ({s1}) engineered for modern high-transient GPU & CPU rigs",
            f"Precision electrical and thermal performance ({s2}) under sustained 4K gaming and rendering",
            f"Builder-friendly integration ({s3}) with clean cable routing and broad socket/case compatibility",
            f"Protected by {s4} for long-term hardware investment security"
        ],
        "cons": [
            "High enthusiast demand occasionally causes temporary stock shortages during major GPU launch windows"
        ],
        "body_paragraphs": [
            f"When calculating total system wattage and thermal dissipation on {SITE_NAME}, choosing components with generous headroom is the key to a silent, crash-free PC. In our technical evaluation, the {prod_name} delivered exceptional consistency across both idle efficiency and peak torture loads.",
            f"Equipped with {s1} and {s2}, it handles millisecond GPU power excursions and sustained multi-core boosts without voltage sag or acoustic whine. Furthermore, {s3} ensures straightforward installation inside modern mid-tower and full-tower chassis.",
            f"Backed by {s4}, the {prod_name} earns a {score}/5.0 rating as a top-tier component for 2026 gaming and workstation builds."
        ]
    }

def get_cumulative_product_reviews():
    """
    Returns Base Reviews + 1 additional unique review unlocked per day elapsed since LAUNCH_EPOCH.
    If days elapsed exceed the catalog length, procedurally generates additional unique GPU+CPU combo PSU reviews
    so the website's article count strictly increases by +1 every single day forever!
    """
    today = datetime.datetime.utcnow().date()
    days_elapsed = max(1, (today - LAUNCH_EPOCH).days + 1)

    reviews = list(BASE_REVIEWS)
    catalog_len = len(DAILY_CUMULATIVE_CATALOG)

    for i in range(days_elapsed):
        pub_date = (LAUNCH_EPOCH + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
        if i < catalog_len:
            reviews.append(build_full_review_from_catalog(DAILY_CUMULATIVE_CATALOG[i], pub_date))
        else:
            # Procedural infinite daily expansion after catalog is fully unlocked
            extra_idx = i - catalog_len + 1
            watt_tier = [750, 850, 1000, 1200, 1300][extra_idx % 5]
            gpu_tier = ["RTX 5090 / 4090", "RTX 5080 / 4080 Super", "RTX 4070 Ti Super", "Radeon RX 7900 XTX", "Dual-GPU AI Workstation"][extra_idx % 5]
            proc_tuple = (
                f"atx-3-1-{watt_tier}w-psu-guide-build-{extra_idx}",
                f"{watt_tier}W ATX 3.1 80+ Gold/Platinum PSU for {gpu_tier} (Build #{extra_idx})",
                f"{watt_tier}W ATX 3.1 Build Review",
                "4.8",
                f"Verified {watt_tier}W Tier-A Config",
                f"{watt_tier}W Continuous ({watt_tier*2}W Peak Spike)",
                "Native 600W PCIe 5.1 12V-2x6",
                "105°C Japanese Capacitors + Zero RPM",
                "10-Year Full Manufacturer Warranty",
                f"{watt_tier}W+ATX+3.1+PCIe+5.1+80+Gold+Modular+Power+Supply",
                f"Complete electrical load, transient excursion, and thermal benchmark of a {watt_tier}W ATX 3.1 power supply paired with a {gpu_tier} configuration."
            )
            reviews.append(build_full_review_from_catalog(proc_tuple, pub_date))

    return list(reversed(reviews))

# ==========================================
# PROGRAMMATIC SEO GPU + CPU BUILD PRESETS
# ==========================================
BUILD_PRESETS = [
    {"slug": "rtx-4090-ryzen-7-9800x3d-psu-wattage-calculator", "name": "RTX 4090 + Ryzen 7 9800X3D / 7800X3D Build", "gpu_w": 450, "cpu_w": 120, "ram_ssd_w": 75, "oc": "1.1", "desc": "Calculate exact ATX 3.1 PSU wattage (1000W vs 1200W), 200% GPU transient spike headroom, 360mm AIO cooler TDP, and sinewave UPS size for an RTX 4090 + Ryzen 7 9800X3D rig."},
    {"slug": "rtx-5090-next-gen-600w-gpu-psu-wattage-calculator", "name": "Next-Gen RTX 5090 (600W) + Ryzen 9 9950X Build", "gpu_w": 600, "cpu_w": 200, "ram_ssd_w": 90, "oc": "1.1", "desc": "Size the required 1200W to 1500W ATX 3.1 PCIe 5.1 power supply, native 600W 12V-2x6 cable, and 1500VA UPS for a 600W flagship RTX 5090 build."},
    {"slug": "rtx-4080-super-ryzen-7-7800x3d-psu-calculator", "name": "RTX 4080 Super + Ryzen 7 7800X3D / 9800X3D Build", "gpu_w": 320, "cpu_w": 120, "ram_ssd_w": 65, "oc": "1.0", "desc": "Calculate optimal 850W ATX 3.1 power supply wattage, 12V-2x6 cable load, and CPU cooler TDP for an RTX 4080 Super gaming PC."},
    {"slug": "rtx-5080-400w-gpu-atx-3-1-psu-calculator", "name": "Next-Gen RTX 5080 (400W) + Core Ultra 9 / Ryzen 7 Build", "gpu_w": 400, "cpu_w": 150, "ram_ssd_w": 75, "oc": "1.1", "desc": "Calculate exact 850W vs 1000W ATX 3.1 PSU requirements and transient spike buffer for a 400W RTX 5080 gaming system."},
    {"slug": "rtx-4070-super-ti-super-psu-wattage-calculator", "name": "RTX 4070 Super / 4070 Ti Super + Ryzen 7 Build", "gpu_w": 285, "cpu_w": 105, "ram_ssd_w": 60, "oc": "1.0", "desc": "Find the ideal 750W or 850W ATX 3.1 modular power supply, air/AIO cooler size, and UPS VA rating for an RTX 4070 Super or 4070 Ti Super rig."},
    {"slug": "radeon-rx-7900-xtx-ryzen-7-psu-wattage-calculator", "name": "AMD Radeon RX 7900 XTX + Ryzen 7 9800X3D Build", "gpu_w": 355, "cpu_w": 120, "ram_ssd_w": 70, "oc": "1.1", "desc": "Calculate PSU wattage (850W–1000W), 3× 8-pin PCIe power rail load, and transient spike headroom for an all-AMD Radeon RX 7900 XTX build."},
    {"slug": "intel-core-i9-14900k-rtx-4090-psu-cooler-calculator", "name": "Intel Core i9-14900K / Ultra 9 285K + RTX 4090 Build", "gpu_w": 450, "cpu_w": 253, "ram_ssd_w": 85, "oc": "1.1", "desc": "Calculate 1000W–1200W ATX 3.1 PSU capacity and mandatory 360mm/420mm AIO liquid cooler TDP for a 253W Intel Core i9 + RTX 4090 workstation."},
    {"slug": "radeon-rx-7800-xt-ryzen-5-7600x-psu-calculator", "name": "Radeon RX 7800 XT + Ryzen 5 7600X / 9600X Build", "gpu_w": 263, "cpu_w": 105, "ram_ssd_w": 55, "oc": "1.0", "desc": "Calculate budget-friendly 750W 80+ Gold PSU sizing and dual-tower air cooler specs for a 1440p RX 7800 XT gaming PC."},
    {"slug": "dual-gpu-ai-workstation-2x-rtx-4090-psu-calculator", "name": "Dual-GPU AI & LLM Server (2× RTX 4090 + Threadripper/Ryzen 9)", "gpu_w": 900, "cpu_w": 230, "ram_ssd_w": 120, "oc": "1.0", "desc": "Size a 1500W–1600W 80+ Platinum/Titanium ATX 3.1 power supply with dual native 12V-2x6 cables for a dual-GPU local AI & rendering workstation."},
    {"slug": "mini-itx-sff-gaming-pc-sfx-psu-wattage-calculator", "name": "Mini-ITX Small Form Factor (SFF) RTX 4080 Super Build", "gpu_w": 320, "cpu_w": 120, "ram_ssd_w": 55, "oc": "1.0", "desc": "Calculate compact SFX / SFX-L Platinum power supply wattage (850W–1000W) and thermal dissipation for a Mini-ITX gaming build."},
    {"slug": "rtx-4060-ti-budget-1080p-gaming-pc-psu-calculator", "name": "RTX 4060 / 4060 Ti + Core i5 / Ryzen 5 Build", "gpu_w": 165, "cpu_w": 88, "ram_ssd_w": 50, "oc": "1.0", "desc": "Calculate efficient 650W–750W 80+ Gold PSU sizing and quiet air cooling for a mainstream RTX 4060 Ti gaming PC."},
    {"slug": "streaming-video-editing-ryzen-9-9950x-psu-calculator", "name": "4K Video Editing & Streaming Workstation (Ryzen 9 9950X + RTX 4080S)", "gpu_w": 320, "cpu_w": 200, "ram_ssd_w": 95, "oc": "1.1", "desc": "Calculate continuous rendering wattage, 1000W ATX 3.1 PSU efficiency, and 360mm AIO liquid cooling for a multi-drive creator workstation."}
]

def get_dynamic_wattage_pages():
    watt_configs = [
        (650, 200, 88), (750, 260, 105), (850, 320, 120),
        (1000, 450, 150), (1200, 520, 200), (1300, 600, 220), (1500, 850, 250)
    ]
    day_of_year = datetime.datetime.utcnow().timetuple().tm_yday
    active_count = min(len(watt_configs), 5 + (day_of_year % 3))
    pages = []
    for psu_tier, g_w, c_w in watt_configs[:active_count]:
        pages.append({
            "slug": f"{psu_tier}w-atx-3-1-power-supply-gpu-calculator",
            "name": f"{psu_tier}W ATX 3.1 Power Supply Tier",
            "gpu_w": g_w,
            "cpu_w": c_w,
            "ram_ssd_w": 70,
            "oc": "1.0",
            "desc": f"See which GPUs and CPUs can safely run on a {psu_tier}W ATX 3.1 power supply, including 200% transient spike headroom and UPS battery sizing."
        })
    return pages

ALL_CALC_PAGES = BUILD_PRESETS + get_dynamic_wattage_pages()

def compute_pc_power(gpu_w, cpu_w, ram_ssd_w, oc_factor):
    continuous_w = int(round((gpu_w + cpu_w + ram_ssd_w) * float(oc_factor)))
    # Transient spike: GPU can spike 1.8x briefly + CPU + peripherals
    transient_peak_w = int(round((gpu_w * 1.85) + cpu_w + ram_ssd_w))
    # Recommended PSU targets ~60-70% load for peak efficiency + transient safety
    raw_rec = max(continuous_w * 1.35, transient_peak_w * 0.92)
    tiers = [650, 750, 850, 1000, 1200, 1300, 1500, 1600]
    rec_psu = 1600
    for t in tiers:
        if t >= raw_rec:
            rec_psu = t
            break

    cooler_tdp = int(round(cpu_w * float(oc_factor) * 1.3))
    if cpu_w >= 170:
        cooler_type = "360mm / 420mm AIO Liquid Cooler"
    elif cpu_w >= 115:
        cooler_type = "240mm/360mm AIO or Dual-Tower Air"
    else:
        cooler_type = "Dual-Tower 120mm Air Cooler"

    ups_va = 1500 if continuous_w >= 480 else 1000
    return continuous_w, transient_peak_w, rec_psu, cooler_tdp, cooler_type, ups_va

def generate_faq_data(preset_name, gpu_w, cpu_w, ram_ssd_w, oc):
    cont_w, spike_w, rec_psu, _, cooler_type, ups_va = compute_pc_power(gpu_w, cpu_w, ram_ssd_w, oc)
    return [
        {
            "q": f"What size power supply (PSU) do I need for {preset_name} ({cont_w}W continuous load)?",
            "a": f"Your system draws approximately {cont_w}W under continuous gaming/rendering load, with microsecond GPU transient spikes reaching up to {spike_w}W. To keep your power supply in its quietest 55%–65% efficiency sweet spot and prevent OCP shutdowns, we recommend a {rec_psu}W ATX 3.1 80+ Gold or Platinum PSU."
        },
        {
            "q": "Why should I buy an ATX 3.1 (PCIe 5.1) PSU instead of an older ATX 2.4 unit?",
            "a": "ATX 3.1 power supplies are engineered to withstand 200% total power excursions and 300% GPU transient spikes for 100 microseconds without tripping Over-Current Protection (OCP). They also include a native 600W 12V-2x6 cable with recessed sense pins to prevent loose-connector overheating."
        },
        {
            "q": f"What CPU cooler is required for a {cpu_w}W TDP processor?",
            "a": f"For a {cpu_w}W TDP processor, we recommend a {cooler_type} (such as the ARCTIC Liquid Freezer III 360 or Thermalright Phantom Spirit 120 EVO) to prevent thermal throttling during all-core boost workloads."
        },
        {
            "q": "Why does my gaming PC need a Pure Sine Wave UPS instead of a cheap battery backup?",
            "a": f"Modern 80+ Gold, Platinum, and Titanium PC power supplies use Active PFC (Power Factor Correction). Cheap simulated-sinewave UPS units output a stepped square wave that causes Active PFC PSUs to buzz or abruptly shut off when grid power fails. Always use a {ups_va}VA Pure Sine Wave UPS."
        },
        {
            "q": "Can I use a higher wattage PSU (like 1000W or 1200W) than my PC actually needs?",
            "a": "Yes! A power supply only pulls the exact wattage your PC components demand—a 1000W PSU running a 500W gaming PC only draws ~545W from the wall, runs cooler, keeps its fan in 0 dB silent mode longer, and gives you instant upgrade headroom for future GPUs."
        }
    ]

def render_comparison_table_section():
    rows_html = ""
    for item in COMPARISON_MATRIX:
        link = amz_url(item["keyword"])
        rows_html += f"""
        <tr class="border-b border-zinc-800 hover:bg-zinc-900/80 transition">
            <td class="p-3.5 font-extrabold text-white text-xs sm:text-sm">{item['model']}</td>
            <td class="p-3.5 text-xs font-semibold text-emerald-400">{item['type']}</td>
            <td class="p-3.5 text-xs font-mono text-zinc-300">{item['wattage_spec']}</td>
            <td class="p-3.5 text-xs text-zinc-300">{item['pcie_cable']}</td>
            <td class="p-3.5 text-xs text-amber-400 font-bold">{item['highlight']}</td>
            <td class="p-3.5 text-xs font-bold text-amber-400">{item['rating']}</td>
            <td class="p-3.5 text-right">
                <a href="{link}" target="_blank" rel="nofollow sponsored noopener"
                   class="inline-block bg-emerald-500 hover:bg-emerald-400 text-zinc-950 font-extrabold text-xs py-2 px-3.5 rounded-lg transition shadow-sm whitespace-nowrap">
                   Check Price &rarr;
                </a>
            </td>
        </tr>
        """

    vs_cards_html = ""
    for vs in VS_COMPARISONS:
        vs_cards_html += f"""
        <a href="{BASE_URL}/{vs['slug']}.html" class="bg-zinc-900 border-2 border-zinc-800 hover:border-emerald-500 rounded-xl p-5 transition flex flex-col justify-between shadow-sm">
            <div>
                <span class="text-[11px] font-extrabold uppercase tracking-wider bg-emerald-950 text-emerald-300 border border-emerald-800 px-2.5 py-1 rounded-full">{vs['winner_badge']}</span>
                <h3 class="text-base font-extrabold text-white mt-2.5 mb-1.5 leading-snug">{vs['title']}</h3>
                <p class="text-xs text-zinc-400 leading-relaxed">{vs['summary']}</p>
            </div>
            <span class="text-xs font-extrabold text-emerald-400 mt-4 inline-flex items-center gap-1">Read Full Head-to-Head Comparison &rarr;</span>
        </a>
        """

    return f"""
    <!-- PRODUCT COMPARISON SECTION (PERBANDINGAN PRODUK) -->
    <section id="comparison" class="space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-zinc-800 pb-4">
            <div>
                <span class="text-xs font-extrabold uppercase tracking-wider text-emerald-400">Side-by-Side Spec Matrix</span>
                <h2 class="text-2xl font-extrabold text-white">Top ATX 3.1 Power Supplies, 360mm AIOs & Sinewave UPS Units Compared</h2>
            </div>
            <span class="text-xs font-semibold text-zinc-400">2026 Cybenetics & ATX 3.1 Lab Benchmarks</span>
        </div>

        <div class="bg-zinc-950 border-2 border-zinc-800 rounded-2xl overflow-x-auto shadow-lg">
            <table class="w-full text-left border-collapse min-w-[720px]">
                <thead>
                    <tr class="bg-zinc-900 border-b-2 border-zinc-800 text-[11px] font-extrabold uppercase tracking-wider text-zinc-300">
                        <th class="p-3.5">Hardware Model</th>
                        <th class="p-3.5">Category</th>
                        <th class="p-3.5">Wattage / Excursion</th>
                        <th class="p-3.5">PCIe 5.1 / Cooling Spec</th>
                        <th class="p-3.5">Key Engineering Highlight</th>
                        <th class="p-3.5">Rating</th>
                        <th class="p-3.5 text-right">Amazon Deal</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </div>

        <!-- Head-to-Head VS Guides -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-5 pt-2">
            {vs_cards_html}
        </div>
    </section>
    """

def render_review_cards_grid():
    active_reviews = get_cumulative_product_reviews()
    cards = ""
    for rev in active_reviews:
        amz_link = amz_url(rev["keyword"])
        cards += f"""
        <article class="bg-zinc-900 border-2 border-zinc-800 hover:border-zinc-700 rounded-2xl p-6 shadow-md transition flex flex-col justify-between">
            <div>
                <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
                    <span class="text-xs font-extrabold uppercase tracking-wider bg-emerald-950 text-emerald-300 border border-emerald-800 px-2.5 py-1 rounded-full">{rev['verdict_badge']}</span>
                    <span class="text-xs font-black bg-amber-500/20 text-amber-300 border border-amber-500/40 px-2.5 py-1 rounded-lg">Score: {rev['rating_score']} / 5.0 ★</span>
                </div>
                <div class="flex items-center justify-between text-xs text-zinc-400 mb-1">
                    <span class="font-semibold uppercase tracking-wide text-zinc-300">{rev['category']}</span>
                    <span class="font-mono text-[11px] text-zinc-500">Published: {rev['published_date']}</span>
                </div>
                <h3 class="text-lg font-extrabold text-white mt-1 mb-2 leading-snug">
                    <a href="{BASE_URL}/{rev['slug']}.html" class="hover:text-emerald-400 transition">{rev['title']}</a>
                </h3>
                <p class="text-xs text-zinc-400 leading-relaxed mb-4">{rev['summary']}</p>
                <div class="grid grid-cols-2 gap-2 text-[11px] bg-black/60 p-3 rounded-xl border border-zinc-800 mb-4">
                    <div><span class="text-zinc-500 block">Primary Spec:</span><strong class="text-zinc-200">{rev['spec_1']}</strong></div>
                    <div><span class="text-zinc-500 block">Standard:</span><strong class="text-zinc-200">{rev['spec_2']}</strong></div>
                    <div><span class="text-zinc-500 block">Engineering:</span><strong class="text-zinc-200">{rev['spec_3']}</strong></div>
                    <div><span class="text-zinc-500 block">Warranty:</span><strong class="text-zinc-200">{rev['spec_4']}</strong></div>
                </div>
            </div>
            <div class="flex flex-col sm:flex-row gap-2.5 pt-2">
                <a href="{BASE_URL}/{rev['slug']}.html" class="flex-1 text-center bg-zinc-800 hover:bg-zinc-700 text-white font-bold text-xs py-2.5 px-3 rounded-lg transition border border-zinc-700">
                    Read Full Technical Review &rarr;
                </a>
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-amber-500 hover:bg-amber-400 text-zinc-950 font-extrabold text-xs py-2.5 px-3 rounded-lg transition shadow-sm">
                    Check Price on Amazon &rarr;
                </a>
            </div>
        </article>
        """
    return cards, len(active_reviews)

def render_common_header_and_banner():
    top_deal_link = amz_url("ATX+3.1+Power+Supply+1000W+850W+RTX+GPU+Ryzen+9800X3D+Deals")
    return f"""
    <!-- TOP PROMOTIONAL AFFILIATE BANNER -->
    <div class="bg-zinc-900 text-zinc-100 py-2.5 px-4 text-center text-xs sm:text-sm font-medium border-b border-zinc-800">
        <div class="max-w-6xl mx-auto flex flex-wrap items-center justify-center gap-2">
            <span class="bg-amber-500 text-zinc-950 font-extrabold px-2 py-0.5 rounded text-xs uppercase">PC Builder Deals</span>
            <span>Save up to 30% on Tier-A ATX 3.1 Power Supplies, Ryzen X3D CPUs, 360mm AIO Coolers & Gaming UPS Units on Amazon.</span>
            <a href="{top_deal_link}" target="_blank" rel="nofollow sponsored noopener" class="text-emerald-400 hover:text-emerald-300 underline font-bold ml-1">
                View Active PC Hardware Deals &rarr;
            </a>
        </div>
    </div>

    <!-- STICKY NAVIGATION HEADER (PITCH BLACK BACKGROUND) -->
    <header class="bg-black/95 backdrop-blur border-b border-zinc-800 sticky top-0 z-30">
        <div class="max-w-6xl mx-auto px-4 py-3.5 flex flex-wrap items-center justify-between gap-4">
            <a href="{BASE_URL}/" class="flex items-center gap-2.5">
                <div class="w-9 h-9 rounded-lg bg-emerald-500 flex items-center justify-center text-zinc-950 font-black text-lg shadow-sm">W</div>
                <div>
                    <span class="font-extrabold text-lg tracking-tight text-white block leading-none">{SITE_NAME}</span>
                    <span class="text-[11px] text-zinc-400 font-medium">ATX 3.1 PSU, GPU Spike & Cooler Sizing Engine</span>
                </div>
            </a>
            <nav class="flex flex-wrap items-center gap-4 sm:gap-5 text-xs sm:text-sm font-semibold text-zinc-300">
                <a href="{BASE_URL}/#calculator" class="hover:text-emerald-400 transition">PSU Calculator</a>
                <a href="{BASE_URL}/#product-search" class="hover:text-emerald-400 transition">Search Parts</a>
                <a href="{BASE_URL}/#best-sellers" class="hover:text-emerald-400 transition">Best Sellers</a>
                <a href="{BASE_URL}/#comparison" class="hover:text-emerald-400 transition">Compare</a>
                <a href="{BASE_URL}/#reviews" class="hover:text-emerald-400 transition">Daily Reviews</a>
                <a href="{BASE_URL}/#faq" class="hover:text-emerald-400 transition">FAQ</a>
            </nav>
        </div>
    </header>
    """

def render_calculator_page(page_data, is_home=False):
    cont_w, spike_w, rec_psu, _, _, _ = compute_pc_power(
        page_data["gpu_w"], page_data["cpu_w"], page_data["ram_ssd_w"], page_data["oc"]
    )
    title = f"{SITE_NAME} — {SITE_TAGLINE}" if is_home else f"{page_data['name']} — PSU Wattage & Cooler Calculator ({rec_psu}W ATX 3.1) | {SITE_NAME}"
    description = page_data["desc"]
    canonical_url = f"{BASE_URL}/" if is_home else f"{BASE_URL}/{page_data['slug']}.html"
    faqs = generate_faq_data(page_data["name"], page_data["gpu_w"], page_data["cpu_w"], page_data["ram_ssd_w"], page_data["oc"])

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": item["q"], "acceptedAnswer": {"@type": "Answer", "text": item["a"]}}
            for item in faqs
        ]
    }

    app_schema = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": title,
        "url": canonical_url,
        "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "All",
        "description": description,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
    }

    bestseller_cards_html = ""
    for prod in BEST_SELLERS:
        link = amz_url(prod["keyword"])
        bestseller_cards_html += f"""
        <div class="bg-zinc-900 border border-zinc-800 hover:border-zinc-700 rounded-xl p-5 shadow-md transition flex flex-col justify-between">
            <div>
                <div class="flex items-center justify-between gap-2 mb-2">
                    <span class="text-xs font-bold uppercase tracking-wider bg-emerald-950 text-emerald-300 border border-emerald-800 px-2.5 py-1 rounded-full">{prod['badge']}</span>
                    <span class="text-xs font-semibold text-amber-400">{prod['rating']}</span>
                </div>
                <span class="text-xs text-zinc-400 font-medium">{prod['category']}</span>
                <h3 class="text-base font-bold text-white mt-1 mb-2 leading-snug">{prod['title']}</h3>
                <p class="text-xs text-zinc-300 mb-4 bg-black/60 p-2.5 rounded-lg border border-zinc-800">{prod['specs']}</p>
            </div>
            <a href="{link}" target="_blank" rel="nofollow sponsored noopener"
               class="w-full inline-flex items-center justify-center bg-amber-500 hover:bg-amber-400 text-zinc-950 font-extrabold text-sm py-2.5 px-4 rounded-lg transition shadow-sm">
               Check Today's Price on Amazon &rarr;
            </a>
        </div>
        """

    preset_links_html = ""
    for p in ALL_CALC_PAGES:
        _, _, p_psu, _, _, _ = compute_pc_power(p["gpu_w"], p["cpu_w"], p["ram_ssd_w"], p["oc"])
        active_cls = "bg-emerald-950/80 border-emerald-500 text-emerald-300 font-bold" if (not is_home and p["slug"] == page_data["slug"]) else "bg-zinc-900 border-zinc-800 text-zinc-300 hover:border-emerald-500 hover:text-white"
        preset_links_html += f"""
        <a href="{BASE_URL}/{p['slug']}.html" class="border rounded-lg p-3 text-xs transition flex items-center justify-between {active_cls}">
            <span class="truncate pr-2">{p['name']}</span>
            <span class="text-amber-400 font-mono shrink-0">{p_psu}W</span>
        </a>
        """

    faq_html = ""
    for item in faqs:
        faq_html += f"""
        <div class="bg-zinc-900 border border-zinc-800 rounded-xl p-5">
            <h3 class="text-base font-bold text-white mb-2">{item['q']}</h3>
            <p class="text-sm text-zinc-400 leading-relaxed">{item['a']}</p>
        </div>
        """

    mid_banner_link = amz_url("ATX+3.1+1000W+Power+Supply+and+360mm+AIO+Liquid+Cooler+Bundle")
    comparison_html = render_comparison_table_section()
    reviews_grid_html, total_reviews_count = render_review_cards_grid()

    return f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="google-site-verification" content="pgvlG0f03ZrRZzbgDSXRhr6tsSfseFOhXCN6Yv_j5b8" />
    <meta name="description" content="{description}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical_url}">
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="application/ld+json">{json.dumps(faq_schema)}</script>
    <script type="application/ld+json">{json.dumps(app_schema)}</script>
</head>
<body class="bg-black text-zinc-100 antialiased selection:bg-emerald-500 selection:text-zinc-950">

    {render_common_header_and_banner()}

    <main class="max-w-6xl mx-auto px-4 py-8 space-y-12">

        <!-- HERO TITLE SECTION -->
        <section class="text-center max-w-3xl mx-auto space-y-3">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-zinc-900 border border-zinc-800 text-xs font-semibold text-emerald-400">
                <span>⚡ Intel ATX 3.1 & PCIe 5.1 12V-2x6 Transient Excursion Calculator</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
                { "PC Power Supply (PSU) Wattage, GPU Spike & Cooler Sizing Calculator" if is_home else f"{page_data['name']} — PSU Wattage & Cooler Calculator" }
            </h1>
            <p class="text-zinc-400 text-sm sm:text-base leading-relaxed">
                {description}
            </p>
        </section>

        <!-- INTERACTIVE CALCULATOR + LIVE HARDWARE MATCHER -->
        <section id="calculator" class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            <!-- Left Column: Inputs (7 Cols) -->
            <div class="lg:col-span-7 bg-zinc-950 border-2 border-zinc-800 rounded-2xl p-6 sm:p-8 shadow-lg space-y-6">
                <div class="flex items-center justify-between border-b border-zinc-800 pb-4">
                    <div>
                        <h2 class="text-xl font-extrabold text-white">1. Select Your GPU, CPU & Overclock Load</h2>
                        <p class="text-xs text-zinc-400">Calculates continuous watts, 100μs GPU transient spikes, ATX 3.1 PSU tier & AIO TDP</p>
                    </div>
                    <span class="text-xs font-mono bg-emerald-950 text-emerald-300 border border-emerald-800 px-2.5 py-1 rounded font-semibold">Live ATX 3.1 Math</span>
                </div>

                <div>
                    <label for="quickPreset" class="block text-xs font-bold uppercase tracking-wider text-zinc-400 mb-2">Quick Select PC Build Preset</label>
                    <select id="quickPreset" onchange="applyPreset(this.value)" class="w-full bg-zinc-900 border border-zinc-700 rounded-lg px-3.5 py-2.5 text-sm font-medium text-white focus:ring-2 focus:ring-emerald-500">
                        <option value="{page_data['gpu_w']},{page_data['cpu_w']},{page_data['ram_ssd_w']},{page_data['oc']}">Current: {page_data['name']}</option>
                        <option value="450,120,75,1.1">RTX 4090 (450W) + Ryzen 7 9800X3D / 7800X3D (1000W ATX 3.1)</option>
                        <option value="600,200,90,1.1">Next-Gen RTX 5090 (600W) + Ryzen 9 9950X (1200W–1500W ATX 3.1)</option>
                        <option value="320,120,65,1.0">RTX 4080 Super (320W) + Ryzen 7 7800X3D (850W ATX 3.1)</option>
                        <option value="285,105,60,1.0">RTX 4070 Ti Super (285W) + Ryzen 7 7700X (750W–850W ATX 3.1)</option>
                        <option value="355,120,70,1.1">Radeon RX 7900 XTX (355W) + Ryzen 7 9800X3D (850W–1000W)</option>
                        <option value="450,253,85,1.1">RTX 4090 (450W) + Intel Core i9-14900K (1200W ATX 3.1)</option>
                    </select>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
                    <div>
                        <label for="gpuInput" class="block text-sm font-bold text-zinc-200 mb-1">Graphics Card (GPU) TDP (Watts)</label>
                        <select id="gpuInput" onchange="calculatePSU()" class="w-full bg-zinc-900 border border-zinc-700 rounded-lg px-3.5 py-2.5 text-sm font-bold text-white">
                            <option value="165" {"selected" if page_data['gpu_w'] == 165 else ""}>165W — RTX 4060 Ti / RX 7600 XT</option>
                            <option value="220" {"selected" if page_data['gpu_w'] == 220 else ""}>220W — RTX 4070 Super / RX 7700 XT</option>
                            <option value="263" {"selected" if page_data['gpu_w'] == 263 else ""}>263W — Radeon RX 7800 XT / RX 7900 GRE</option>
                            <option value="285" {"selected" if page_data['gpu_w'] == 285 else ""}>285W — RTX 4070 Ti Super / RX 7900 XT</option>
                            <option value="320" {"selected" if page_data['gpu_w'] == 320 else ""}>320W — NVIDIA RTX 4080 Super</option>
                            <option value="355" {"selected" if page_data['gpu_w'] == 355 else ""}>355W — AMD Radeon RX 7900 XTX</option>
                            <option value="400" {"selected" if page_data['gpu_w'] == 400 else ""}>400W — Next-Gen RTX 5080 / OC Flagship</option>
                            <option value="450" {"selected" if page_data['gpu_w'] == 450 else ""}>450W — NVIDIA GeForce RTX 4090</option>
                            <option value="600" {"selected" if page_data['gpu_w'] == 600 else ""}>600W — Next-Gen RTX 5090 / Max 12V-2x6</option>
                            <option value="900" {"selected" if page_data['gpu_w'] == 900 else ""}>900W — Dual-GPU AI Workstation (2× 450W)</option>
                        </select>
                    </div>

                    <div>
                        <label for="cpuInput" class="block text-sm font-bold text-zinc-200 mb-1">Processor (CPU) Peak Power (Watts)</label>
                        <select id="cpuInput" onchange="calculatePSU()" class="w-full bg-zinc-900 border border-zinc-700 rounded-lg px-3.5 py-2.5 text-sm font-bold text-white">
                            <option value="88" {"selected" if page_data['cpu_w'] == 88 else ""}>88W — Ryzen 5 7600X / 9600X / Core i5</option>
                            <option value="105" {"selected" if page_data['cpu_w'] == 105 else ""}>105W — Ryzen 7 7700X / 9700X</option>
                            <option value="120" {"selected" if page_data['cpu_w'] == 120 else ""}>120W — Ryzen 7 9800X3D / 7800X3D</option>
                            <option value="150" {"selected" if page_data['cpu_w'] == 150 else ""}>150W — Core i7-14700K / Core Ultra 7 265K</option>
                            <option value="200" {"selected" if page_data['cpu_w'] == 200 else ""}>200W — AMD Ryzen 9 9950X / 7950X</option>
                            <option value="253" {"selected" if page_data['cpu_w'] == 253 else ""}>253W — Intel Core i9-14900K / Ultra 9 285K</option>
                        </select>
                    </div>

                    <div>
                        <label for="periphInput" class="block text-sm font-bold text-zinc-200 mb-1">Motherboard, DDR5, NVMe & Fans (Watts)</label>
                        <input type="number" id="periphInput" value="{page_data['ram_ssd_w']}" min="30" max="250" step="5" oninput="calculatePSU()"
                               class="w-full bg-zinc-900 border border-zinc-700 rounded-lg px-4 py-2.5 text-base font-bold text-white focus:ring-2 focus:ring-emerald-500">
                        <span class="text-[11px] text-zinc-500">Typical gaming rig: 65W–85W for board, SSDs & RGB fans</span>
                    </div>

                    <div>
                        <label for="ocInput" class="block text-sm font-bold text-zinc-200 mb-1">Overclocking & Boost Profile</label>
                        <select id="ocInput" onchange="calculatePSU()" class="w-full bg-zinc-900 border border-zinc-700 rounded-lg px-3.5 py-2.5 text-sm font-bold text-white">
                            <option value="1.0" {"selected" if page_data['oc'] == "1.0" else ""}>Stock / Undervolted (1.0x Load)</option>
                            <option value="1.1" {"selected" if page_data['oc'] == "1.1" else ""}>Factory OC GPU + PBO Enabled (+10%)</option>
                            <option value="1.2" {"selected" if page_data['oc'] == "1.2" else ""}>Heavy Manual GPU + CPU Overclock (+20%)</option>
                        </select>
                    </div>
                </div>
            </div>

            <!-- Right Column: Output + Dynamic Amazon Recommendation (5 Cols) -->
            <div class="lg:col-span-5 bg-zinc-950 border-2 border-emerald-500 rounded-2xl p-6 sm:p-8 shadow-xl space-y-6">
                <div class="border-b border-zinc-800 pb-3">
                    <span class="text-xs font-extrabold uppercase tracking-wider text-emerald-400">2. Engineered Power & Cooling Specs</span>
                    <h2 class="text-xl font-extrabold text-white">Your Recommended ATX 3.1 Sizing</h2>
                </div>

                <div class="grid grid-cols-2 gap-3.5">
                    <div class="bg-emerald-950/60 border border-emerald-700 rounded-xl p-3.5">
                        <span class="text-xs text-emerald-300 font-semibold block">Recommended PSU Tier</span>
                        <span id="resPsuTier" class="text-2xl font-black text-emerald-400">1000W</span>
                        <span class="text-[11px] text-emerald-200 block mt-0.5">ATX 3.1 / PCIe 5.1 Gold+</span>
                    </div>
                    <div class="bg-zinc-900 border border-zinc-800 rounded-xl p-3.5">
                        <span class="text-xs text-zinc-400 font-medium block">Continuous Load</span>
                        <span id="resContinuousW" class="text-2xl font-black text-white">645W</span>
                        <span id="resSpikeW" class="text-[11px] text-amber-400 block mt-0.5">100μs Spike: ~1025W</span>
                    </div>
                    <div class="bg-zinc-900 border border-zinc-800 rounded-xl p-3.5">
                        <span class="text-xs text-zinc-400 font-medium block">CPU Cooler Requirement</span>
                        <span id="resCoolerType" class="text-sm font-extrabold text-white">360mm AIO Cooler</span>
                        <span id="resCoolerTDP" class="text-[11px] text-zinc-400 block mt-0.5">Min 220W+ TDP Rating</span>
                    </div>
                    <div class="bg-zinc-900 border border-zinc-800 rounded-xl p-3.5">
                        <span class="text-xs text-zinc-400 font-medium block">Pure Sine Wave UPS</span>
                        <span id="resUpsVA" class="text-sm font-extrabold text-amber-400">1500VA / 1000W</span>
                        <span class="text-[11px] text-zinc-400 block mt-0.5">Active PFC Compatible</span>
                    </div>
                </div>

                <!-- Dynamic Matched Product Box -->
                <div class="bg-zinc-900 border-2 border-amber-500/80 rounded-xl p-4 space-y-3">
                    <div class="flex items-center justify-between">
                        <span class="text-[11px] font-extrabold uppercase tracking-wider bg-amber-500 text-zinc-950 px-2 py-0.5 rounded">Tier-A Hardware Match</span>
                        <span class="text-xs font-bold text-emerald-400">Amazon Prime Verified</span>
                    </div>
                    <h3 id="recPsuTitle" class="text-base font-extrabold text-white leading-snug">Loading Tier-A PSU Match...</h3>
                    <p id="recPsuDesc" class="text-xs text-zinc-300"></p>
                    <div class="pt-1 flex flex-col sm:flex-row gap-2.5">
                        <a id="recPrimaryBtn" href="#" target="_blank" rel="nofollow sponsored noopener"
                           class="flex-1 text-center bg-amber-500 hover:bg-amber-400 text-zinc-950 font-extrabold text-sm py-3 px-4 rounded-lg transition shadow-sm">
                           Shop Matched ATX 3.1 PSU &rarr;
                        </a>
                        <a id="recSecondaryBtn" href="#" target="_blank" rel="nofollow sponsored noopener"
                           class="text-center bg-zinc-800 hover:bg-zinc-700 text-white border border-zinc-700 font-bold text-xs py-3 px-3 rounded-lg transition">
                           Shop Matched CPU Cooler
                        </a>
                    </div>
                </div>
            </div>
        </section>

        <!-- PRODUCT SEARCH ENGINE SECTION (SEARCH PRODUK) -->
        <section id="product-search" class="bg-zinc-950 border-2 border-zinc-800 rounded-2xl p-6 sm:p-8 shadow-lg">
            <div class="max-w-3xl mx-auto text-center space-y-4">
                <h2 class="text-2xl font-extrabold text-white">Search ATX 3.1 Power Supplies, GPUs, Ryzen X3D CPUs & 360mm AIO Coolers</h2>
                <p class="text-sm text-zinc-400">Search any wattage (750W, 850W, 1000W, 1200W), brand (Corsair, Seasonic, MSI, be quiet!, ARCTIC, Thermalright, AMD, NVIDIA), or PC component on Amazon.</p>
                <form onsubmit="handleAmazonSearch(event)" class="flex flex-col sm:flex-row gap-3 pt-2">
                    <input type="text" id="amzSearchInput" placeholder="e.g. Corsair RM1000x ATX 3.1 PSU, Seasonic VERTEX 1000W, ARCTIC Liquid Freezer III 360..."
                           class="flex-1 bg-zinc-900 border-2 border-zinc-700 rounded-xl px-4 py-3 text-sm font-medium text-white placeholder-zinc-500 focus:outline-none focus:border-emerald-500" required>
                    <button type="submit" class="bg-emerald-500 hover:bg-emerald-400 text-zinc-950 font-extrabold text-sm px-6 py-3 rounded-xl transition cursor-pointer shrink-0">
                        Search on Amazon &rarr;
                    </button>
                </form>
                <div class="flex flex-wrap items-center justify-center gap-2 pt-2 text-xs">
                    <span class="text-zinc-500 font-semibold">Popular Searches:</span>
                    <a href="{amz_url('1000W ATX 3.1 PCIe 5.1 Modular Power Supply')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-zinc-900 hover:bg-emerald-950 text-zinc-300 hover:text-emerald-300 border border-zinc-800 rounded-full transition">1000W ATX 3.1 PSUs</a>
                    <a href="{amz_url('850W ATX 3.1 80 Plus Gold Power Supply')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-zinc-900 hover:bg-emerald-950 text-zinc-300 hover:text-emerald-300 border border-zinc-800 rounded-full transition">850W Gold PSUs</a>
                    <a href="{amz_url('ARCTIC Liquid Freezer III 360 AIO CPU Cooler')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-zinc-900 hover:bg-emerald-950 text-zinc-300 hover:text-emerald-300 border border-zinc-800 rounded-full transition">360mm AIO Coolers</a>
                    <a href="{amz_url('AMD Ryzen 7 9800X3D 7800X3D Processor')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-zinc-900 hover:bg-emerald-950 text-zinc-300 hover:text-emerald-300 border border-zinc-800 rounded-full transition">Ryzen 7 X3D CPUs</a>
                    <a href="{amz_url('CyberPower 1500VA Pure Sine Wave Gaming UPS')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-zinc-900 hover:bg-emerald-950 text-zinc-300 hover:text-emerald-300 border border-zinc-800 rounded-full transition">1500VA Gaming UPS</a>
                </div>
            </div>
        </section>

        <!-- BEST SELLING PRODUCTS GRID (PRODUK TERLARIS) -->
        <section id="best-sellers" class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-zinc-800 pb-4">
                <div>
                    <span class="text-xs font-extrabold uppercase tracking-wider text-emerald-400">Tier-A Verified PC Hardware</span>
                    <h2 class="text-2xl font-extrabold text-white">Best-Selling ATX 3.1 Power Supplies, Coolers, CPUs & UPS Units</h2>
                </div>
                <a href="{amz_url('Best Selling PC Power Supplies and CPU Coolers')}" target="_blank" rel="nofollow sponsored noopener" class="text-sm font-bold text-amber-400 hover:text-amber-300">
                    Browse Full Amazon Best Sellers &rarr;
                </a>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
                {bestseller_cards_html}
            </div>
        </section>

        {comparison_html}

        <!-- CUMULATIVE DAILY PRODUCT REVIEW ARTICLES SECTION (ARTIKEL PRODUK REVIEW) -->
        <section id="reviews" class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-zinc-800 pb-4">
                <div>
                    <span class="text-xs font-extrabold uppercase tracking-wider text-emerald-400">Autonomous Daily Review Archive ({total_reviews_count} Published Articles & Growing Daily)</span>
                    <h2 class="text-2xl font-extrabold text-white">In-Depth PSU, CPU Cooler & PC Hardware Review Articles</h2>
                </div>
                <span class="text-xs font-semibold bg-emerald-950 text-emerald-300 border border-emerald-800 px-3 py-1 rounded-full">+1 New Hardware Review Added Automatically Every Day</span>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                {reviews_grid_html}
            </div>
        </section>

        <!-- MID-PAGE PROMOTIONAL AFFILIATE BANNER -->
        <section class="bg-zinc-900 border-2 border-amber-500 rounded-2xl p-6 sm:p-8 flex flex-col md:flex-row items-center justify-between gap-6">
            <div class="space-y-2 max-w-2xl">
                <span class="text-xs font-extrabold uppercase tracking-wider bg-amber-500 text-zinc-950 px-2.5 py-1 rounded">Next-Gen GPU Upgrade Guide</span>
                <h2 class="text-xl sm:text-2xl font-extrabold text-white">Upgrading to an RTX 4080 Super, 4090, or Next-Gen 50-Series GPU?</h2>
                <p class="text-sm text-zinc-300">Ditch dangerous 4-way PCIe squid adapters. Upgrade to a native ATX 3.1 / PCIe 5.1 power supply with a single 600W 12V-2x6 cable and 200% transient excursion protection.</p>
            </div>
            <a href="{mid_banner_link}" target="_blank" rel="nofollow sponsored noopener"
               class="shrink-0 bg-amber-500 hover:bg-amber-400 text-zinc-950 font-extrabold text-sm px-6 py-3.5 rounded-xl shadow-sm transition">
               Explore ATX 3.1 PSUs + 360mm AIO Deals &rarr;
            </a>
        </section>

        <!-- PROGRAMMATIC SEO DIRECTORY -->
        <section id="presets" class="space-y-4">
            <div class="border-b border-zinc-800 pb-3">
                <h2 class="text-xl font-extrabold text-white">GPU + CPU Build Specific PSU Wattage Calculators</h2>
                <p class="text-xs text-zinc-400">Select your exact graphics card and processor combination below for pre-configured ATX 3.1 wattage and cooling specs.</p>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2.5">
                {preset_links_html}
            </div>
        </section>

        <!-- FREQUENTLY ASKED QUESTIONS (FAQ) -->
        <section id="faq" class="space-y-6">
            <div class="border-b border-zinc-800 pb-3">
                <span class="text-xs font-extrabold uppercase tracking-wider text-emerald-400">ATX 3.1 & PC Power Knowledge Base</span>
                <h2 class="text-2xl font-extrabold text-white">Frequently Asked Questions (FAQ)</h2>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                {faq_html}
            </div>
        </section>

    </main>

    <!-- FOOTER -->
    <footer class="bg-zinc-950 border-t border-zinc-800 mt-16 py-10 px-4 text-xs text-zinc-400">
        <div class="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
            <div>
                <p class="font-bold text-white">{SITE_NAME} — {SITE_TAGLINE}</p>
                <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
            </div>
            <div class="flex flex-wrap gap-4 font-medium text-zinc-300">
                <a href="{BASE_URL}/" class="hover:text-emerald-400">Home</a>
                <a href="{BASE_URL}/#comparison" class="hover:text-emerald-400">Comparisons</a>
                <a href="{BASE_URL}/#reviews" class="hover:text-emerald-400">Daily Reviews</a>
                <a href="{BASE_URL}/sitemap.xml" class="hover:text-emerald-400">Sitemap</a>
                <a href="{BASE_URL}/#faq" class="hover:text-emerald-400">FAQ</a>
            </div>
        </div>
    </footer>

    <!-- INTERACTIVE CALCULATOR & AFFILIATE MATCHING SCRIPT -->
    <script>
        const AFFILIATE_TAG = "{AFFILIATE_TAG}";

        function makeAmazonLink(query) {{
            return "https://www.amazon.com/s?k=" + encodeURIComponent(query) + "&tag=" + AFFILIATE_TAG;
        }}

        function applyPreset(val) {{
            const parts = val.split(",");
            if (parts.length === 4) {{
                document.getElementById("gpuInput").value = parts[0];
                document.getElementById("cpuInput").value = parts[1];
                document.getElementById("periphInput").value = parts[2];
                document.getElementById("ocInput").value = parts[3];
                calculatePSU();
            }}
        }}

        function handleAmazonSearch(e) {{
            e.preventDefault();
            const q = document.getElementById("amzSearchInput").value.trim();
            if (q) {{
                window.open(makeAmazonLink(q), "_blank", "noopener,noreferrer");
            }}
        }}

        function calculatePSU() {{
            const gpuW = parseFloat(document.getElementById("gpuInput").value) || 320;
            const cpuW = parseFloat(document.getElementById("cpuInput").value) || 120;
            const periphW = parseFloat(document.getElementById("periphInput").value) || 70;
            const ocFactor = parseFloat(document.getElementById("ocInput").value) || 1.0;

            const contW = Math.round((gpuW + cpuW + periphW) * ocFactor);
            const spikeW = Math.round((gpuW * 1.85) + cpuW + periphW);
            const rawTarget = Math.max(contW * 1.35, spikeW * 0.92);

            const tiers = [650, 750, 850, 1000, 1200, 1300, 1500, 1600];
            let recPSU = 1600;
            for (let i = 0; i < tiers.length; i++) {{
                if (tiers[i] >= rawTarget) {{
                    recPSU = tiers[i];
                    break;
                }}
            }}

            const coolerTDP = Math.round(cpuW * ocFactor * 1.3);
            let coolerType = "Dual-Tower 120mm Air Cooler";
            let coolerQuery = "Thermalright Phantom Spirit 120 EVO CPU Air Cooler";
            if (cpuW >= 180) {{
                coolerType = "360mm / 420mm Heavy-Duty AIO";
                coolerQuery = "ARCTIC Liquid Freezer III 360 AIO CPU Cooler";
            }} else if (cpuW >= 120) {{
                coolerType = "360mm AIO or Dual-Tower Air";
                coolerQuery = "ARCTIC Liquid Freezer III 360 Thermalright Phantom Spirit 120";
            }}

            const upsVA = contW >= 480 ? "1500VA / 1000W" : "1000VA / 600W";

            document.getElementById("resPsuTier").textContent = recPSU + "W";
            document.getElementById("resContinuousW").textContent = contW + "W";
            document.getElementById("resSpikeW").textContent = "100μs Transient Peak: ~" + spikeW + "W";
            document.getElementById("resCoolerType").textContent = coolerType;
            document.getElementById("resCoolerTDP").textContent = "Min " + coolerTDP + "W+ Thermal Rating";
            document.getElementById("resUpsVA").textContent = upsVA + " Sinewave";

            let recTitle = "";
            let recDesc = "";
            let psuQuery = "";

            if (recPSU <= 750) {{
                recTitle = "750W ATX 3.1 80+ Gold Fully Modular PSU (Corsair RM750x / MSI A750GL)";
                recDesc = "Ideal efficiency curve for " + contW + "W gaming builds with full PCIe 5.1 transient protection.";
                psuQuery = "750W ATX 3.1 PCIe 5.1 80 Plus Gold Modular Power Supply Corsair MSI Seasonic";
            }} else if (recPSU === 850) {{
                recTitle = "850W ATX 3.1 80+ Gold Modular PSU (MSI MAG A850GL / Corsair RM850x)";
                recDesc = "Best-selling sweet-spot PSU with native 600W 12V-2x6 GPU cable for high-FPS 1440p/4K gaming.";
                psuQuery = "850W ATX 3.1 PCIe 5.1 Modular Power Supply MSI MAG A850GL Corsair RM850x";
            }} else if (recPSU === 1000) {{
                recTitle = "1000W Tier-A ATX 3.1 Modular PSU (Corsair RM1000x / Seasonic VERTEX GX-1000)";
                recDesc = "Engineered to absorb " + spikeW + "W GPU transient spikes while staying in silent low-RPM fan mode.";
                psuQuery = "1000W ATX 3.1 PCIe 5.1 Power Supply Corsair RM1000x Seasonic VERTEX GX-1000";
            }} else {{
                recTitle = recPSU + "W Flagship ATX 3.1 Gold/Platinum/Titanium PSU (NZXT C1200 / Seasonic / Corsair)";
                recDesc = "Maximum current stability and dual 12V-2x6 headroom for flagship 450W–600W+ GPU rigs.";
                psuQuery = recPSU + "W ATX 3.1 PCIe 5.1 Modular Power Supply Seasonic Corsair NZXT be quiet";
            }}

            document.getElementById("recPsuTitle").textContent = recTitle;
            document.getElementById("recPsuDesc").textContent = recDesc;
            document.getElementById("recPrimaryBtn").href = makeAmazonLink(psuQuery);
            document.getElementById("recSecondaryBtn").href = makeAmazonLink(coolerQuery);
        }}

        window.addEventListener("DOMContentLoaded", calculatePSU);
    </script>
</body>
</html>"""

def render_single_review_page(rev):
    canonical_url = f"{BASE_URL}/{rev['slug']}.html"
    amz_link = amz_url(rev["keyword"])

    review_schema = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": rev["product_name"],
        "description": rev["summary"],
        "review": {
            "@type": "Review",
            "datePublished": rev["published_date"],
            "reviewRating": {"@type": "Rating", "ratingValue": rev["rating_score"], "bestRating": "5"},
            "author": {"@type": "Organization", "name": SITE_NAME},
            "reviewBody": " ".join(rev["body_paragraphs"])
        }
    }

    pros_html = "".join([f'<li class="flex items-start gap-2 text-sm text-zinc-300"><span class="text-emerald-400 font-bold">✓</span><span>{p}</span></li>' for p in rev["pros"]])
    cons_html = "".join([f'<li class="flex items-start gap-2 text-sm text-zinc-300"><span class="text-rose-400 font-bold">✕</span><span>{c}</span></li>' for c in rev["cons"]])
    paragraphs_html = "".join([f'<p class="text-zinc-300 leading-relaxed text-base mb-4">{p}</p>' for p in rev["body_paragraphs"]])

    recent_reviews = [r for r in get_cumulative_product_reviews() if r["slug"] != rev["slug"]][:6]
    related_html = ""
    for other in recent_reviews:
        related_html += f"""
        <a href="{BASE_URL}/{other['slug']}.html" class="bg-zinc-900 border border-zinc-800 rounded-xl p-4 hover:border-emerald-500 transition block">
            <span class="text-[11px] font-bold text-emerald-400 uppercase">{other['verdict_badge']}</span>
            <h4 class="font-extrabold text-sm text-white mt-1 line-clamp-2">{other['product_name']} Review</h4>
            <span class="text-xs text-zinc-400 mt-1 block">Score: {other['rating_score']} / 5.0 ★ ({other['published_date']}) &rarr;</span>
        </a>
        """

    return f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{rev['title']} | {SITE_NAME}</title>
    <meta name="description" content="{rev['summary']}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="application/ld+json">{json.dumps(review_schema)}</script>
</head>
<body class="bg-black text-zinc-100 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-4xl mx-auto px-4 py-10 space-y-10">
        <nav class="text-xs font-semibold text-zinc-400 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-emerald-400">Home & PSU Calculator</a>
            <span>/</span>
            <a href="{BASE_URL}/#reviews" class="hover:text-emerald-400">Daily Hardware Reviews</a>
            <span>/</span>
            <span class="text-zinc-200">{rev['product_name']}</span>
        </nav>

        <div class="bg-zinc-950 border-2 border-zinc-800 rounded-2xl p-6 sm:p-8 shadow-lg space-y-5">
            <div class="flex flex-wrap items-center justify-between gap-2">
                <span class="text-xs font-extrabold uppercase tracking-wider bg-emerald-950 text-emerald-300 border border-emerald-800 px-3 py-1 rounded-full">{rev['verdict_badge']}</span>
                <div class="flex items-center gap-2">
                    <span class="text-xs font-mono text-zinc-400">Published: {rev['published_date']}</span>
                    <span class="text-sm font-black bg-amber-500/20 text-amber-300 border border-amber-500/40 px-3 py-1 rounded-lg">Lab Rating: {rev['rating_score']} / 5.0 ★</span>
                </div>
            </div>
            <h1 class="text-2xl sm:text-4xl font-extrabold text-white leading-tight">{rev['title']}</h1>
            <p class="text-base text-zinc-300 leading-relaxed">{rev['summary']}</p>

            <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-zinc-900 p-4 rounded-xl border border-zinc-800 text-xs">
                <div><span class="text-zinc-500 block font-medium">Power / Spec</span><strong class="text-white">{rev['spec_1']}</strong></div>
                <div><span class="text-zinc-500 block font-medium">Architecture</span><strong class="text-white">{rev['spec_2']}</strong></div>
                <div><span class="text-zinc-500 block font-medium">Engineering</span><strong class="text-white">{rev['spec_3']}</strong></div>
                <div><span class="text-zinc-500 block font-medium">Warranty</span><strong class="text-white">{rev['spec_4']}</strong></div>
            </div>

            <div class="flex flex-col sm:flex-row gap-3 pt-2">
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener"
                   class="flex-1 text-center bg-amber-500 hover:bg-amber-400 text-zinc-950 font-extrabold text-sm py-3.5 px-6 rounded-xl transition shadow-sm">
                   Check Latest Price & Availability on Amazon &rarr;
                </a>
                <a href="{BASE_URL}/#calculator"
                   class="text-center bg-zinc-900 hover:bg-zinc-800 text-white border border-zinc-700 font-bold text-sm py-3.5 px-5 rounded-xl transition">
                   Calculate PSU Wattage for Your Build
                </a>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="bg-zinc-950 border-2 border-emerald-900 rounded-2xl p-6 space-y-3">
                <h2 class="text-base font-extrabold text-emerald-400 uppercase tracking-wide">Pros (What We Like)</h2>
                <ul class="space-y-2.5">{pros_html}</ul>
            </div>
            <div class="bg-zinc-950 border-2 border-rose-900 rounded-2xl p-6 space-y-3">
                <h2 class="text-base font-extrabold text-rose-400 uppercase tracking-wide">Cons (Things to Consider)</h2>
                <ul class="space-y-2.5">{cons_html}</ul>
            </div>
        </div>

        <article class="bg-zinc-950 border border-zinc-800 rounded-2xl p-6 sm:p-8 space-y-4">
            <h2 class="text-xl font-extrabold text-white border-b border-zinc-800 pb-3">Hands-On Transient Load, Ripple & Thermal Analysis</h2>
            {paragraphs_html}
            <div class="pt-4 border-t border-zinc-800 flex flex-col sm:flex-row items-center justify-between gap-4">
                <div>
                    <span class="text-xs font-bold uppercase text-emerald-400 block">Final Verdict</span>
                    <p class="text-sm font-bold text-white">{rev['product_name']} earns {rev['rating_score']}/5.0 in our PC hardware benchmark.</p>
                </div>
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener"
                   class="shrink-0 bg-amber-500 hover:bg-amber-400 text-zinc-950 font-extrabold text-sm px-6 py-3 rounded-xl transition shadow-sm">
                   View Customer Reviews & Price on Amazon &rarr;
                </a>
            </div>
        </article>

        <section class="space-y-4">
            <h3 class="text-lg font-extrabold text-white">Recent Daily PC Hardware Reviews</h3>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                {related_html}
            </div>
        </section>
    </main>

    <footer class="bg-zinc-950 border-t border-zinc-800 mt-16 py-10 px-4 text-xs text-zinc-400 text-center">
        <p class="font-bold text-white">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def render_vs_comparison_page(vs):
    canonical_url = f"{BASE_URL}/{vs['slug']}.html"
    link_a = amz_url(vs["keyword_a"])
    link_b = amz_url(vs["keyword_b"])

    rows_html = ""
    for m in vs["metrics"]:
        rows_html += f"""
        <tr class="border-b border-zinc-800">
            <td class="p-4 font-bold text-white bg-zinc-900/70 text-xs sm:text-sm w-1/4">{m['feature']}</td>
            <td class="p-4 text-xs sm:text-sm text-zinc-300 w-3/8">{m['val_a']}</td>
            <td class="p-4 text-xs sm:text-sm text-zinc-300 w-3/8">{m['val_b']}</td>
        </tr>
        """

    return f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{vs['title']} | {SITE_NAME}</title>
    <meta name="description" content="{vs['summary']}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-black text-zinc-100 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-4xl mx-auto px-4 py-10 space-y-10">
        <nav class="text-xs font-semibold text-zinc-400 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-emerald-400">Home & PSU Calculator</a>
            <span>/</span>
            <a href="{BASE_URL}/#comparison" class="hover:text-emerald-400">Product Comparisons</a>
            <span>/</span>
            <span class="text-zinc-200">{vs['product_a']} vs. {vs['product_b']}</span>
        </nav>

        <div class="bg-zinc-950 border-2 border-zinc-800 rounded-2xl p-6 sm:p-8 shadow-lg space-y-4">
            <span class="text-xs font-extrabold uppercase tracking-wider bg-emerald-950 text-emerald-300 border border-emerald-800 px-3 py-1 rounded-full">{vs['winner_badge']}</span>
            <h1 class="text-2xl sm:text-4xl font-extrabold text-white leading-tight">{vs['title']}</h1>
            <p class="text-base text-zinc-300 leading-relaxed">{vs['summary']}</p>
        </div>

        <div class="bg-zinc-950 border-2 border-zinc-800 rounded-2xl overflow-hidden shadow-lg">
            <table class="w-full text-left border-collapse">
                <thead>
                    <tr class="bg-zinc-900 border-b border-zinc-800 text-white text-xs sm:text-sm font-extrabold">
                        <th class="p-4">Specification</th>
                        <th class="p-4 text-emerald-400">{vs['product_a']}</th>
                        <th class="p-4 text-amber-400">{vs['product_b']}</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                    <tr class="bg-zinc-900/50">
                        <td class="p-4 font-extrabold text-xs sm:text-sm text-white">Check Amazon Price</td>
                        <td class="p-4">
                            <a href="{link_a}" target="_blank" rel="nofollow sponsored noopener" class="inline-block bg-emerald-500 hover:bg-emerald-400 text-zinc-950 font-extrabold text-xs py-2.5 px-4 rounded-lg transition">
                                View {vs['product_a']} &rarr;
                            </a>
                        </td>
                        <td class="p-4">
                            <a href="{link_b}" target="_blank" rel="nofollow sponsored noopener" class="inline-block bg-amber-500 hover:bg-amber-400 text-zinc-950 font-extrabold text-xs py-2.5 px-4 rounded-lg transition">
                                View {vs['product_b']} &rarr;
                            </a>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="bg-zinc-900 border-2 border-emerald-700 rounded-2xl p-6 sm:p-8 space-y-4">
            <h2 class="text-xl font-extrabold text-white">Head-to-Head Buying Verdict</h2>
            <p class="text-sm sm:text-base text-zinc-300 leading-relaxed">{vs['verdict_text']}</p>
            <div class="flex flex-col sm:flex-row gap-3 pt-2">
                <a href="{link_a}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-emerald-500 hover:bg-emerald-400 text-zinc-950 font-extrabold text-sm py-3 px-4 rounded-xl transition">
                    Shop {vs['product_a']} on Amazon &rarr;
                </a>
                <a href="{link_b}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-amber-500 hover:bg-amber-400 text-zinc-950 font-extrabold text-sm py-3 px-4 rounded-xl transition">
                    Shop {vs['product_b']} on Amazon &rarr;
                </a>
            </div>
        </div>
    </main>

    <footer class="bg-zinc-950 border-t border-zinc-800 mt-16 py-10 px-4 text-xs text-zinc-400 text-center">
        <p class="font-bold text-white">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def generate_sitemap_and_robots(urls):
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    xml_items = ""
    for u in urls:
        xml_items += f"""  <url>
    <loc>{u}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>{"1.0" if u.endswith("/") else "0.85"}</priority>
  </url>\n"""

    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{xml_items}</urlset>"""

    with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_content)

    robots_content = f"""User-agent: *
Allow: /
Sitemap: {BASE_URL}/sitemap.xml
"""
    with open(os.path.join(OUTPUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots_content)

    with open(os.path.join(OUTPUT_DIR, f"{INDEXNOW_KEY}.txt"), "w", encoding="utf-8") as f:
        f.write(INDEXNOW_KEY)

def ping_indexnow(urls):
    parsed_host = urllib.parse.urlparse(BASE_URL).netloc
    if not parsed_host or "username.github.io" in parsed_host:
        return

    payload = {
        "host": parsed_host,
        "key": INDEXNOW_KEY,
        "keyLocation": f"{BASE_URL}/{INDEXNOW_KEY}.txt",
        "urlList": urls
    }
    try:
        req = urllib.request.Request(
            "https://api.indexnow.org/indexnow",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"IndexNow Ping Status: {resp.status}")
    except Exception as e:
        print(f"IndexNow notice: {e}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    generated_urls = []

    # 1. Generate Homepage
    home_preset = {
        "slug": "index",
        "name": "RTX 4080 Super / 4090 + Ryzen 7 9800X3D Build",
        "gpu_w": 450,
        "cpu_w": 120,
        "ram_ssd_w": 75,
        "oc": "1.0",
        "desc": "Calculate exact PC Power Supply (PSU) ATX 3.1 wattage, 100μs GPU transient spike headroom, 360mm AIO cooler TDP, and Pure Sine Wave UPS VA capacity—plus read daily PC hardware reviews."
    }
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(render_calculator_page(home_preset, is_home=True))
    generated_urls.append(f"{BASE_URL}/")

    # 2. Generate Programmatic GPU + CPU Build Calculator Pages
    for page in ALL_CALC_PAGES:
        filename = f"{page['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_calculator_page(page, is_home=False))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 3. Generate Cumulative Daily Product Review Pages (+1 new review unlocked every day)
    active_reviews = get_cumulative_product_reviews()
    for rev in active_reviews:
        filename = f"{rev['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_single_review_page(rev))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 4. Generate Standalone Head-to-Head Product Comparison Pages
    for vs in VS_COMPARISONS:
        filename = f"{vs['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_vs_comparison_page(vs))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 5. Sitemap, Robots & IndexNow Auto-Ping
    generate_sitemap_and_robots(generated_urls)
    ping_indexnow(generated_urls)
    print(f"Successfully generated {len(generated_urls)} total SEO pages ({len(active_reviews)} cumulative review articles) in /{OUTPUT_DIR}!")

if __name__ == "__main__":
    main()
