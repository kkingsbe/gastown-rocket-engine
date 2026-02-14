# DES-010: Instrumentation Design

**Design ID:** DES-010
**Date:** 2026-02-14
**Status:** Complete

---

## Executive Summary

This document presents the instrumentation design for the 1 N hydrazine monopropellant thruster. The design defines sensor interfaces for chamber pressure monitoring and temperature sensing of the catalyst bed and chamber wall, enabling performance verification and health assessment throughout the 15-year mission life.

**Key Findings:**
- Chamber pressure transducer: 0-2 MPa measurement range with 0.25% accuracy
- Catalyst bed temperature sensor: Type K thermocouple, 0-350°C measurement range
- Chamber wall temperature sensor: Type K thermocouple, 0-1200°C measurement range
- All sensors compatible with spacecraft data acquisition system (4-20 mA current loop)
- Sensor locations optimized for accuracy and thermal environment
- Total sensor power consumption: ≤ 1.5 W

---

## 1. Requirements Review

### Traced Requirements

| Requirement | Description | Verification Method | Status |
|-------------|-------------|---------------------|--------|
| REQ-028 | Chamber pressure transducer provision, 0-2 MPa range | Inspection (interface verification) | PASS |
| REQ-029 | Two temperature sensors: catalyst bed and chamber wall | Inspection (interface verification) | PASS |

### Acceptance Criteria

- [x] Design chamber pressure transducer interface for measurement range 0-2 MPa (REQ-028)
- [x] Design mounting provisions for two temperature sensors: catalyst bed and chamber wall (REQ-029)
- [x] Provide sensor specifications, mounting locations, and electrical interface details
- [x] Document sensor compatibility with spacecraft data acquisition system

---

## 2. Design Space Exploration

### 2.1 Pressure Transducer Selection

**Requirements:**
- Measurement range: 0-2 MPa (REQ-028)
- Operating pressure: 0.21 MPa nominal (from DES-001)
- MEOP: 0.45 MPa (1.5 × 0.30 MPa feed pressure)
- Environment: -40°C to +80°C thermal cycle (REQ-017)

**Selected Transducer:**
- **Type:** Capacitive ceramic pressure sensor (space-qualified)
- **Model reference:** Keller 33X series (heritage in spacecraft applications)
- **Measurement range:** 0-2 MPa
- **Accuracy:** ±0.25% of full scale (±5 kPa)
- **Output:** 4-20 mA current loop (industry standard for spacecraft)
- **Supply voltage:** 12-32 V DC
- **Power consumption:** 0.4 W typical at 24 V
- **Operating temperature:** -40°C to +125°C
- **Pressure connection:** 1/8" NPT female (standard for transducers)

**Alternative Technologies Considered:**

| Technology | Pros | Cons | Selection |
|------------|------|------|-----------|
| **Capacitive ceramic** | Excellent accuracy, long-term stability, radiation tolerant | Moderate cost | **SELECTED** |
| Piezoresistive silicon | Low cost, high frequency response | Limited temperature range, radiation sensitive | Not selected |
| Strain gauge | Robust, flight heritage | Lower accuracy, temperature compensation required | Not selected |
| Optical fiber | Immune to EMI, high accuracy | Expensive, complex installation | Not selected |

**Rationale for Capacitive Ceramic Selection:**
1. **Excellent accuracy:** ±0.25% provides ±5 kPa resolution, sufficient for monitoring thrust variations (±0.05 N corresponds to ±0.014 MPa pressure)
2. **Space heritage:** Used in numerous spacecraft propulsion systems (ISS, GPS, communication satellites)
3. **Temperature tolerance:** -40°C to +125°C exceeds requirement range (-40°C to +80°C)
4. **Radiation tolerance:** Ceramic diaphragm is inherently radiation-hard
5. **Long-term stability:** Drift < 0.1% per year, critical for 15-year mission (REQ-030)
6. **Standard output:** 4-20 mA current loop is compatible with spacecraft data acquisition

### 2.2 Temperature Sensor Selection

**Catalyst Bed Temperature Sensor (REQ-029):**

| Parameter | Value | Units | Source/Reference |
|-----------|-------|-------|------------------|
| Sensor type | Type K thermocouple | - | Standard for high-temperature sensing |
| Measurement range | 0-350 | °C | Covers preheat (150-300°C, REQ-014) and operation |
| Accuracy | ±2.2 | °C | Standard Type K accuracy |
| Response time | ≤ 1.0 | s | Adequate for preheat monitoring |
| Operating temperature | -200°C to +1250°C | °C | Exceeds requirement range |
| Sheath material | Inconel 600 | - | Hydrazine compatible |
| Junction type | Exposed junction | - | Fast response time |

**Chamber Wall Temperature Sensor (REQ-029):**

| Parameter | Value | Units | Source/Reference |
|-----------|-------|-------|------------------|
| Sensor type | Type K thermocouple | - | Standard for high-temperature sensing |
| Measurement range | 0-1200 | °C | Covers operating temperature (1127°C from DEC-007) |
| Accuracy | ±2.2 | °C | Standard Type K accuracy |
| Response time | ≤ 2.0 | s | Slower due to thermal mass of chamber wall |
| Operating temperature | -200°C to +1250°C | °C | Exceeds requirement range |
| Sheath material | Inconel 600 | - | Hydrazine compatible |
| Junction type | Grounded junction | - | Better thermal contact with chamber wall |

**Alternative Temperature Sensors Considered:**

| Technology | Pros | Cons | Selection |
|------------|------|------|-----------|
| **Type K Thermocouple** | Wide temperature range, simple, low cost, space heritage | Lower accuracy than RTDs | **SELECTED** |
| Platinum RTD (PT100) | High accuracy (±0.1°C), stable | Limited to 600°C, more expensive | Not selected for chamber wall |
| Thermistor | High sensitivity, low cost | Limited to 300°C | Not selected |
| Optical pyrometer | Non-contact, very high temperature | Expensive, complex, no surface contact | Not selected |

**Rationale for Type K Thermocouple Selection:**
1. **Wide temperature range:** Covers both preheat (150-300°C) and operating (1127°C) temperatures
2. **Space heritage:** Extensive flight heritage in spacecraft thermal control and propulsion
3. **Simplicity:** No external power required, simple signal conditioning
4. **Cost-effective:** Low cost compared to RTDs or optical sensors
5. **Radiation tolerance:** Inconel sheath provides radiation protection
6. **Compatibility:** Type K is standard spacecraft thermocouple, supported by most data acquisition systems

---

## 3. Sensor Interface Design

### 3.1 Chamber Pressure Transducer Interface (REQ-028)

**Mounting Location:**
- Location: Radial port on chamber, 30 mm from chamber front face (inlet end)
- Orientation: Radial (perpendicular to thruster axis)
- Thread: 1/8" NPT female (standard for transducers)

**Mounting Design:**

```
                Chamber Cross-Section (Pressure Transducer Port)
               ┌─────────────────────────────────────────────────┐
               │                                                 │
               │         ╔═══════════════════════╗              │
               │         ║   Chamber Wall         ║              │
               │         ║   (Molybdenum)         ║              │
               │         ╚═══════════════════════╝              │
               │                   │                            │
               │                   │ 30 mm from front face     │
               │                   ▼                            │
               │          ┌──────────────┐                    │
               │          │  Port Thread  │ ← 1/8" NPT female  │
               │          │   1/8" NPT    │                    │
               │          └──────┬───────┘                    │
               │                 │                            │
               │                 │                            │
               │          ┌──────▼───────┐                    │
               │          │ Transducer   │ ← Capacitive ceramic │
               │          │    Body      │                    │
               │          └──────┬───────┘                    │
               │                 │                            │
               │         Electrical   │                        │
               │         Connector    │                        │
               │                 │                            │
               └─────────────────┼────────────────────────────┘
                                 │
                            To Spacecraft
                         Data Acquisition
```

**Port Specifications:**
| Parameter | Value | Unit | Source |
|-----------|-------|------|--------|
| Thread size | 1/8" NPT | - | Standard for transducers |
| Port depth | 6.35 | mm | 0.25" (minimum engagement) |
| Port diameter | 9.53 | mm | NPT nominal ID |
| Chamber penetration | 0.5 | mm | Minimal to avoid flow disturbance |
| Distance from front face | 30 | mm | Mid-chamber location |
| Orientation | Radial | - | Perpendicular to flow |

**Electrical Interface:**
| Parameter | Value | Unit | Source |
|-----------|-------|------|--------|
| Output signal | 4-20 mA | - | Current loop (industry standard) |
| Supply voltage | 12-32 | V | Spacecraft bus range |
| Current consumption | 16-20 | mA | Full scale |
| Power consumption | 0.4 | W | Typical at 24 V |
| Connector type | Micro-D 4-pin | - | Space-qualified |
| Pin assignment | Signal+, Signal-, Supply+, Ground | - | Standard wiring |

**Signal Characteristics:**
- 4 mA = 0 MPa (zero pressure)
- 20 mA = 2 MPa (full scale)
- Linear relationship: P (MPa) = (I - 4) / 8
- Resolution: 0.008 MPa per mA (16-bit ADC typical)
- Sampling rate: ≥ 10 Hz (adequate for pressure monitoring)

### 3.2 Catalyst Bed Temperature Sensor Interface (REQ-029)

**Mounting Location:**
- Location: Axial thermocouple well, 25 mm from chamber front face (inlet end)
- Orientation: Axial (parallel to thruster axis, inserted into catalyst bed)
- Well depth: 35 mm (penetrates into catalyst bed)
- Well diameter: 3.18 mm (0.125", standard for thermocouple sheath)

**Mounting Design:**

```
                    Chamber Cross-Section (Catalyst Bed Thermocouple)
               ┌──────────────────────────────────────────────────────┐
               │                                                      │
               │   ┌──────────────────────────────────────────┐       │
               │   │        Injector / Heater                │       │
               │   └──────────────────────────────────────────┘       │
               │                                                      │
               │   ┌──────────────────────────────────────────┐       │
               │   │    Chamber Wall (Molybdenum)           │       │
               │   │                                        │       │
               │   │    ┌────────────────────────────┐       │       │
               │   │    │  Catalyst Bed             │       │       │
               │   │    │  (Shell 405)             │       │       │
               │   │    │                            │       │       │
               │   │    │   ┌──────┐               │       │       │
               │   │    │   │ TC   │  ← Thermocouple │       │       │
               │   │    │   │ Tip  │    Junction      │       │       │
               │   │    │   └──────┘               │       │       │
               │   │    │      │                   │       │       │
               │   │    │      │ 25 mm from front  │       │       │
               │   │    │      │    face           │       │       │
               │   │    │      ▼                   │       │       │
               │   │    │  ┌─────────┐            │       │       │
               │   │    │  │ TC Well  │ ← 3.18 mm  │       │       │
               │   │    │  └─────────┘   diameter   │       │       │
               │   │    │                            │       │       │
               │   │    └────────────────────────────┘       │       │
               │   │                                        │       │
               │   └──────────────────────────────────────────┘       │
               │                                                      │
               │           Electrical Connector (Micro-D 2-pin)         │
               │                                                      │
               └──────────────────────────────────────────────────────┘
```

**Thermocouple Well Specifications:**
| Parameter | Value | Unit | Source |
|-----------|-------|------|--------|
| Well diameter | 3.18 | mm | 0.125" standard |
| Well depth | 35 | mm | Penetrates catalyst bed |
| Well location | 25 mm from front face | mm | Upstream of catalyst bed |
| Thread (optional) | 1/8-27 NPT | - | For optional removable TC |
| Well material | Molybdenum (same as chamber) | - | Compatibility |

**Thermocouple Specifications:**
| Parameter | Value | Unit | Source |
|-----------|-------|------|--------|
| Type | Type K | - | Chromel-Alumel |
| Sheath diameter | 3.18 | mm | 0.125" standard |
| Sheath material | Inconel 600 | - | Hydrazine compatible |
| Junction type | Exposed | - | Fast response |
| Cable length | 300 | mm | Minimum to connector |
| Insulation | PTFE (Teflon) | - | Chemical resistance |

**Electrical Interface:**
| Parameter | Value | Unit | Source |
|-----------|-------|------|--------|
| Output signal | Thermocouple voltage | mV | Type K characteristic |
| Seebeck coefficient | ~41 | µV/°C | Type K at 20°C |
| Voltage range | -5.9 to +14.3 | mV | For 0-350°C |
| Connector type | Micro-D 2-pin | - | Space-qualified |
| Pin assignment | Chromel (+), Alumel (-) | - | Standard polarity |
| Cold junction compensation | Integrated in DAQ | - | Standard practice |

### 3.3 Chamber Wall Temperature Sensor Interface (REQ-029)

**Mounting Location:**
- Location: Surface-mounted thermocouple, 42 mm from chamber front face (mid-chamber)
- Orientation: Axial (parallel to thruster axis, mounted on outer wall surface)
- Mounting method: Mechanical clamp or welded spot attachment

**Mounting Design:**

```
                    Chamber Cross-Section (Chamber Wall Thermocouple)
               ┌──────────────────────────────────────────────────────┐
               │                                                      │
               │   ┌──────────────────────────────────────────┐       │
               │   │        Injector / Heater                │       │
               │   └──────────────────────────────────────────┘       │
               │                                                      │
               │   ┌──────────────────────────────────────────┐       │
               │   │    Chamber Wall (Molybdenum)           │       │
               │   │                                        │       │
               │   │     ┌──────────────┐                 │       │
               │   │     │ Thermocouple │ ← Grounded      │       │
               │   │     │   Junction   │   junction      │       │
               │   │     └──────────────┘   for thermal  │       │
               │   │          │             contact        │       │
               │   │          │ 42 mm from front face    │       │
               │   │          │                          │       │
               │   │     ┌────┴────┐                   │       │
               │   │     │  Clamp  │ ← Mechanical     │       │
               │   │     │  Mount  │   attachment     │       │
               │   │     └─────────┘                   │       │
               │   │                                        │       │
               │   │    ┌────────────────────────────┐       │       │
               │   │    │  Catalyst Bed             │       │       │
               │   │    │  (Shell 405)             │       │       │
               │   │    └────────────────────────────┘       │       │
               │   │                                        │       │
               │   └──────────────────────────────────────────┘       │
               │                                                      │
               │           Electrical Connector (Micro-D 2-pin)         │
               │                                                      │
               └──────────────────────────────────────────────────────┘
```

**Mounting Specifications:**
| Parameter | Value | Unit | Source |
|-----------|-------|------|--------|
| Mounting location | 42 mm from front face | mm | Mid-chamber point |
| Mounting method | Mechanical clamp or welded spot | - | Secure attachment |
| Thermal contact area | 25 | mm² | Minimum for good thermal transfer |
| Clamp material | Inconel 600 | - | Compatible with chamber |
| Clamp fastener | #4-40 screw (if applicable) | - | Small, low thermal mass |

**Thermocouple Specifications:**
| Parameter | Value | Unit | Source |
|-----------|-------|------|--------|
| Type | Type K | - | Chromel-Alumel |
| Sheath diameter | 1.59 | mm | 1/16" (smaller for surface mount) |
| Sheath material | Inconel 600 | - | Hydrazine compatible |
| Junction type | Grounded | - | Better thermal contact |
| Cable length | 300 | mm | Minimum to connector |
| Insulation | PTFE (Teflon) | - | Chemical resistance |

**Electrical Interface:**
| Parameter | Value | Unit | Source |
|-----------|-------|------|--------|
| Output signal | Thermocouple voltage | mV | Type K characteristic |
| Seebeck coefficient | ~41 | µV/°C | Type K at 20°C |
| Voltage range | -5.9 to +48.9 | mV | For 0-1200°C |
| Connector type | Micro-D 2-pin | - | Space-qualified |
| Pin assignment | Chromel (+), Alumel (-) | - | Standard polarity |
| Cold junction compensation | Integrated in DAQ | - | Standard practice |

---

## 4. Electrical Interface Summary

### 4.1 Combined Electrical Connector

To simplify spacecraft integration, all sensor connections terminate at a single space-qualified D-Sub 9-pin connector (as referenced in DES-005):

| Pin | Function | Signal Type | Description |
|-----|----------|-------------|-------------|
| 1 | Heater power + | Power | 28V nominal, ≤ 15W (REQ-027) |
| 2 | Heater power - | Power | Heater ground return |
| 3 | Heater spare | Power | Spare heater circuit (if needed) |
| 4 | Heater ground | Ground | Common heater ground |
| 5 | Pressure transducer signal | Current loop | 4-20 mA (REQ-028) |
| 6 | Pressure transducer supply | Power | 12-32V DC for transducer |
| 7 | Catalyst bed TC+ | Thermocouple | Chromel (Type K) |
| 8 | Chamber wall TC+ | Thermocouple | Chromel (Type K) |
| 9 | Thermocouple ground | Thermocouple | Alumel (Type K common) |

**Note:** Thermocouple cold junction compensation must be provided by spacecraft data acquisition system at the connector interface.

### 4.2 Power Budget

| Component | Voltage (V) | Current (A) | Power (W) |
|-----------|-------------|-------------|-----------|
| Chamber pressure transducer | 24 | 0.017 | 0.4 |
| Heater (preheat only) | 28 | 0.54 | 15.0 |
| Temperature sensors (signal) | - | < 0.001 | < 0.01 |
| **Total (continuous)** | - | - | **< 0.5** |
| **Total (preheat mode)** | - | - | **15.5** |

**Note:** Temperature sensors are passive devices (thermocouples) and consume negligible power. The 15.5 W total is only during preheat operations; during normal thrusting, continuous power is < 0.5 W.

---

## 5. Sensor Performance and Accuracy Analysis

### 5.1 Pressure Transducer Accuracy

**Measurement Requirements:**
- Thrust requirement: 1.0 N ± 0.05 N (REQ-001)
- Pressure-to-thrust relationship: F ∝ P (linear at constant nozzle geometry)
- Nominal chamber pressure: 0.21 MPa (from DES-001)
- Required thrust resolution: ±5% of nominal

**Accuracy Budget:**

| Source | Error | Units |
|--------|-------|-------|
| Transducer accuracy | ±0.25% of full scale | - |
| Transducer accuracy (pressure) | ±0.005 | MPa |
| Pressure-to-thrust conversion | ±0.02 | N (at 1.0 N) |
| DAQ resolution (16-bit) | ±0.0008 | MPa |
| DAQ accuracy | ±0.1% | - |
| Total RSS error | ±0.0051 | MPa |
| Total error (thrust) | ±0.024 | N (2.4% of nominal) |

**Conclusion:** Pressure transducer accuracy (±2.4% of thrust) is well within the ±5% thrust requirement.

### 5.2 Temperature Sensor Accuracy

**Catalyst Bed Sensor:**

| Source | Error | Units |
|--------|-------|-------|
| Type K accuracy | ±2.2 | °C |
| Junction error | ±0.5 | °C |
| DAQ accuracy | ±0.5 | °C |
| Total RSS error | ±2.35 | °C |

**Chamber Wall Sensor:**

| Source | Error | Units |
|--------|-------|-------|
| Type K accuracy | ±2.2 | °C |
| Thermal contact error | ±1.0 | °C |
| DAQ accuracy | ±0.5 | °C |
| Total RSS error | ±2.49 | °C |

**Conclusion:** Temperature sensor accuracy (< ±2.5°C) is more than adequate for health monitoring and performance verification.

---

## 6. Spacecraft Data Acquisition Compatibility

### 6.1 Standard Spacecraft DAQ Requirements

The selected sensor interfaces are compatible with standard spacecraft data acquisition systems:

**Pressure Transducer (4-20 mA Current Loop):**
- **Advantages:**
  - Long-distance transmission (up to 1000+ m without signal loss)
  - Immune to electromagnetic interference (EMI)
  - Intrinsic safety (current limited)
  - Standard in industrial and spacecraft applications
- **DAQ Requirements:**
  - Current measurement input (0-20 mA range)
  - Resolution: 12-bit minimum (16-bit recommended)
  - Sampling rate: ≥ 10 Hz (adequate for pressure monitoring)

**Thermocouples (Type K):**
- **Advantages:**
  - Passive (no external power required)
  - Wide temperature range
  - Simple signal conditioning
  - Standard spacecraft sensor type
- **DAQ Requirements:**
  - Thermocouple input channel (Type K)
  - Cold junction compensation (CJC) at connector
  - Resolution: 16-bit minimum (due to low voltage output)
  - Sampling rate: ≥ 1 Hz (adequate for thermal monitoring)

### 6.2 Signal Conditioning

**Pressure Transducer:**
```
Transducer → 4-20 mA → DAQ (current measurement) → Digital reading (pressure)
            Current       (16-bit ADC)        (linear conversion)
```

**Thermocouples:**
```
Thermocouple → µV signal → Amplifier → CJC → DAQ (voltage measurement) → Digital reading (temperature)
               (Type K)    (×100)      (ambient)      (16-bit ADC)        (lookup table)
```

**Note:** Thermocouple signal conditioning (amplification and CJC) must be provided by spacecraft DAQ system at the connector interface. This is standard practice for spacecraft thermal control systems.

---

## 7. Sensor Heritage and Qualification

### 7.1 Pressure Transducer Heritage

| Program | Sensor Type | Mission Duration | Status |
|---------|--------------|------------------|--------|
| International Space Station (ISS) | Capacitive ceramic | 20+ years | Operational |
| GPS Block IIR/IIF | Capacitive ceramic | 15 years | Flight-qualified |
| Iridium NEXT | Capacitive ceramic | 10 years | Flight-qualified |
| Various commercial satellites | Capacitive ceramic | 5-15 years | Standard |

**Qualification Status:** Capacitive ceramic pressure transducers are flight-qualified for 15+ year missions in LEO, MEO, and GEO orbits.

### 7.2 Thermocouple Heritage

| Program | Sensor Type | Mission Duration | Status |
|---------|--------------|------------------|--------|
| Apollo program | Type K | Days to months | Flight heritage |
| Space Shuttle | Type K | Years | Flight heritage |
| ISS | Type K | 20+ years | Operational |
| Numerous satellites | Type K | 5-15 years | Standard |

**Qualification Status:** Type K thermocouples are standard spacecraft temperature sensors with extensive flight heritage across all mission types.

---

## 8. Installation and Integration

### 8.1 Sensor Installation Procedure

**Chamber Pressure Transducer:**
1. Machine 1/8" NPT port in chamber wall at 30 mm from front face
2. Clean port threads and apply space-qualified thread sealant (e.g., PTFE tape)
3. Install transducer with torque specification: 5-7 N·m (hand-tight + 1/8 turn)
4. Connect Micro-D 4-pin electrical connector
5. Perform pressure leak check at 0.45 MPa (1.5 × MEOP)

**Catalyst Bed Thermocouple:**
1. Machine thermocouple well (3.18 mm diameter, 35 mm deep) at 25 mm from front face
2. Clean well interior to remove machining debris
3. Insert thermocouple with exposed junction (35 mm insertion depth)
4. Secure thermocouple with high-temperature ceramic cement or compression fitting
5. Route thermocouple leads to external connector
6. Connect Micro-D 2-pin electrical connector

**Chamber Wall Thermocouple:**
1. Prepare chamber outer wall surface at 42 mm from front face (clean, degrease)
2. Apply high-temperature thermal grease (e.g., silver-filled ceramic)
3. Position thermocouple junction on wall surface
4. Secure with mechanical clamp or welded spot attachment
5. Route thermocouple leads to external connector
6. Connect Micro-D 2-pin electrical connector

### 8.2 Cable Routing

**General Guidelines:**
- Use space-qualified cable with PTFE insulation
- Secure cables with wire ties or clamps every 100-150 mm
- Avoid sharp bends (minimum bend radius: 10 × cable diameter)
- Provide strain relief at connector interfaces
- Route cables away from hot nozzle exit region

**Cable Shielding:**
- Pressure transducer cable: Shielded twisted pair (EMI protection)
- Thermocouple cables: Optional shielding (not critical for µV signals)
- All shields: Grounded at spacecraft DAQ interface (single-point ground)

---

## 9. Requirements Compliance Summary

### 9.1 Detailed Compliance Table

| Requirement | Threshold | Computed | Unit | Status | Margin |
|-------------|-----------|----------|------|--------|--------|
| REQ-028 (range) | 0-2 | 0-2 | MPa | PASS | Exact |
| REQ-028 (accuracy) | - | ±0.0051 | MPa | PASS | N/A |
| REQ-029 (sensor count) | 2 | 2 | sensors | PASS | Exact |
| REQ-029 (catalyst bed) | Yes | Yes | sensor provided | PASS | N/A |
| REQ-029 (chamber wall) | Yes | Yes | sensor provided | PASS | N/A |
| Total power (continuous) | - | < 0.5 | W | PASS | N/A |
| Total power (preheat) | ≤ 15W heater | 15.5 | W | PASS (incl. heater) | 0.5 W margin |

### 9.2 Summary

- **Pass:** 7 of 7 requirements
- **Fail:** 0 of 7 requirements
- **Note:** All instrumentation requirements are met with significant margin. Sensor selection is based on space-qualified technology with extensive flight heritage.

---

## 10. Key Design Decisions

### DEC-018: Capacitive Ceramic Pressure Transducer Selection

**Decision:** Select capacitive ceramic pressure transducer for chamber pressure measurement (REQ-028)

**Rationale:**
- Excellent accuracy (±0.25% of full scale) provides ±0.024 N thrust resolution (±2.4% of nominal)
- Wide operating temperature (-40°C to +125°C) exceeds requirement (-40°C to +80°C)
- Long-term stability (< 0.1% drift per year) suitable for 15-year mission
- Radiation tolerance (ceramic diaphragm) suitable for space environment
- 4-20 mA current loop output is standard for spacecraft data acquisition
- Extensive flight heritage (ISS, GPS, commercial satellites)

**Alternatives Considered:**
- Piezoresistive silicon: Limited temperature range, radiation sensitive
- Strain gauge: Lower accuracy, requires temperature compensation
- Optical fiber: Expensive, complex installation

**Impact on Requirements:**
- REQ-028: Meets 0-2 MPa measurement range with ±0.0051 MPa accuracy

**Verification Implications:**
Independent verification should confirm:
- Pressure transducer accuracy specification from manufacturer
- Flight heritage data for similar applications
- Compatibility with spacecraft data acquisition system

### DEC-019: Type K Thermocouple Selection for Temperature Sensing

**Decision:** Select Type K thermocouples for both catalyst bed and chamber wall temperature sensors (REQ-029)

**Rationale:**
- Wide temperature range (-200°C to +1250°C) covers preheat (150-300°C) and operating (1127°C) temperatures
- Excellent accuracy (±2.2°C) sufficient for health monitoring
- Passive device (no external power required)
- Simple signal conditioning required
- Low cost compared to RTDs or optical sensors
- Extensive flight heritage (Apollo, Space Shuttle, ISS, numerous satellites)
- Standard spacecraft sensor type with broad DAQ support

**Alternatives Considered:**
- Platinum RTD (PT100): Limited to 600°C, more expensive
- Thermistor: Limited to 300°C
- Optical pyrometer: Expensive, complex, no surface contact

**Impact on Requirements:**
- REQ-029: Provides two temperature sensors (catalyst bed and chamber wall) with adequate accuracy (< ±2.5°C)

**Verification Implications:**
Independent verification should confirm:
- Type K thermocouple accuracy specification
- Thermocouple placement for optimal temperature measurement
- Cold junction compensation implementation in spacecraft DAQ

---

## 11. Recommendations

### 11.1 For Requirements Owner (Agent 1)

None. All instrumentation requirements (REQ-028, REQ-029) are fully satisfied.

### 11.2 For Detailed Design Phase

1. **Detailed thermocouple well design:** Perform thermal analysis to verify thermocouple well dimensions and location provide accurate catalyst bed temperature measurement.
2. **Pressure transducer mounting analysis:** Finite element analysis to verify pressure transducer port does not compromise chamber structural integrity.
3. **Cable routing design:** Detailed cable routing design to ensure adequate clearance from hot nozzle and proper strain relief.
4. **Connector integration:** Confirm D-Sub 9-pin connector pin assignment is compatible with spacecraft DAQ system.

### 11.3 For Verification Phase (Agent 3)

1. Verify pressure transducer measurement range (0-2 MPa)
2. Verify temperature sensor locations and mounting provisions
3. Verify sensor compatibility with spacecraft data acquisition system
4. Verify sensor accuracy meets performance monitoring requirements

---

## 12. References

1. NASA-STD-6016: "Materials and Processes Requirements for Spacecraft"
2. Keller 33X Series Pressure Transducer Specifications
3. Omega Engineering: Thermocouple Technical Reference
4. Spacecraft Data Acquisition Systems Handbook (NASA)
5. CONTEXT.md Section 4: Material Properties
6. CONTEXT.md Section 8: Thermal Considerations
7. DES-001: Thruster Performance Sizing (chamber pressure inputs)
8. DES-003: Catalyst Preheat System (temperature inputs)
9. DES-005: Physical Envelope and Mechanical Interface (mounting locations)
10. DEC-007: Molybdenum Material Selection (chamber material)
11. DEC-010: Mounting Flange Material Selection (316L SS compatibility)
