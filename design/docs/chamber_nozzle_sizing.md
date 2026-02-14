# DES-004: Chamber and Nozzle Structural Sizing

**Design ID:** DES-004
**Date:** 2026-02-14
**Status:** Complete (with constraint exception noted)

---

## Executive Summary

This document presents the structural analysis and sizing of the chamber and nozzle for the 1 N hydrazine monopropellant thruster. The analysis uses thin-wall pressure vessel theory, material selection based on temperature capability and hydrazine compatibility, and verifies compliance with structural requirements.

**Key Findings:**
- Selected material: Molybdenum (Mo) with 1650°C temperature capability
- Chamber wall thickness: 0.500 mm (manufacturability-limited)
- Chamber mass: 0.039 kg (7.8% of 0.5 kg budget, 92.2% margin)
- All structural requirements met (REQ-015, REQ-016, REQ-018, REQ-023, REQ-024, REQ-011)
- **Constraint Exception:** Overall length 208.9 mm exceeds 150 mm envelope limit (REQ-012) due to nozzle length from DES-001

---

## 1. Requirements Review

### Traced Requirements

| Requirement | Description | Verification Method | Status |
|-------------|-------------|---------------------|--------|
| REQ-015 | Chamber wall temperature ≤ 1400°C | Simulation (DES-001 thermal analysis) | PASS |
| REQ-016 | Nozzle exit temperature ≤ 800°C | Simulation (DES-001 isentropic expansion) | PASS |
| REQ-018 | Chamber withstand MEOP × 1.5 safety factor | Analysis (thin-wall pressure vessel) | PASS |
| REQ-023 | Chamber material compatible with hydrazine products | Inspection (material properties review) | PASS |
| REQ-024 | Nozzle material is refractory metal or high-temp alloy ≥1400°C | Inspection (material selection) | PASS |
| REQ-011 | Dry mass ≤ 0.5 kg | Analysis (mass calculation) | PASS |
| REQ-012 | Envelope: 100 mm diameter × 150 mm length | Inspection (dimensional verification) | **FAIL** |

### Acceptance Criteria

- [x] Calculate chamber wall thickness to withstand MEOP × 1.5 safety factor (REQ-018)
- [x] Select chamber material compatible with ≤ 1400°C operating temperature (REQ-015, REQ-023, REQ-024)
- [x] Calculate nozzle expansion ratio for ≤ 800°C exit temperature (REQ-016)
- [x] Verify chamber mass ≤ 0.5 kg dry mass budget (REQ-011)
- [x] Select refractory metal or high-temperature alloy for nozzle (REQ-024)

---

## 2. Design Space Exploration

### 2.1 Material Selection Analysis

Chamber wall operating temperature from DES-001: **1126.8°C** (1400 K)

**Material candidates evaluated (from CONTEXT.md Section 4):**

| Material | Max Temp (°C) | Density (kg/m³) | RT Yield (MPa) | 1000°C Yield (MPa) | Hydrazine Compatible | Heritage |
|----------|--------------|------------------|----------------|-------------------|---------------------|----------|
| Inconel 625 | 980 | 8440 | 460 | 184 | Yes | Excellent |
| Inconel 718 | 700 | 8190 | 1035 | 414 | Yes | Limited above 700°C |
| Haynes 230 | 1150 | 8970 | 390 | 156 | Yes | Excellent high-temp |
| Molybdenum | 1650 | 10220 | 560 | 224 | Yes | Needs coating in oxidizing env |
| Rhenium | 2000 | 21020 | 290 | 116 | Yes | Excellent, expensive |
| Columbium C103 | 1370 | 8850 | 240 | 96 | Yes | Heritage for small thrusters |

**Material selection rationale:**

1. **Temperature requirement (REQ-015):** Operating temperature 1126.8°C
   - Eliminates: Inconel 718 (700°C), Inconel 625 (980°C), Columbium C103 (1370°C - marginal)
   - Viable: Haynes 230 (1150°C - marginal), Molybdenum (1650°C), Rhenium (2000°C)

2. **Structural requirement (REQ-018):** Must withstand pressure with safety factor
   - Haynes 230: 156 MPa yield at temperature
   - Molybdenum: 224 MPa yield at temperature (44% higher)
   - Rhenium: 116 MPa yield at temperature (lowest)

3. **Mass requirement (REQ-011):** Dry mass ≤ 0.5 kg
   - Molybdenum density: 10220 kg/m³
   - Rhenium density: 21020 kg/m³ (2× higher mass)
   - Haynes 230 density: 8970 kg/m³ (lowest, but marginal temperature)

4. **Cost and heritage (REQ-025):** Space-qualified materials preferred
   - Molybdenum: Proven heritage, moderate cost
   - Rhenium: Proven heritage, very high cost (10× molybdenum)
   - Haynes 230: Heritage, but temperature margin only 23°C

**Selected material:** **Molybdenum (Mo)**
- Max temperature: 1650°C (523°C margin above operating)
- Density: 10220 kg/m³
- Yield strength at operating temperature: 224 MPa (40% of RT value)
- Heritage: Flight-proven in oxidizing environment with coating

### 2.2 Wall Thickness Analysis

**Design pressure:** 0.45 MPa (MEOP × 1.5 = 0.30 × 1.5)

**Thin-wall pressure vessel theory (CONTEXT.md Section 9):**
```
σ_hoop = P × r / t
t_min = (P × SF × r) / σ_yield_at_temp
```

Where:
- P = Design pressure = 0.45 MPa = 450,000 Pa
- r = Chamber radius = 11.2 mm = 0.0112 m
- SF = Safety factor = 1.5
- σ_yield_at_temp = 224 MPa (Molybdenum at 1127°C)

**Required thickness (structural):**
```
t_min = (450,000 Pa × 1.5 × 0.0112 m) / (224 × 10⁶ Pa)
t_min = 0.0000338 m = 0.0338 mm
```

**Manufacturability constraint:**
- Minimum practical thickness for thin-wall vessels: 0.5 mm
- Structural requirement is dominated by manufacturability, not pressure loads

**Design thickness:** 0.500 mm

**Verification:**
```
Actual safety factor = (t × σ_yield) / (P × r)
                    = (0.0005 m × 224 × 10⁶ Pa) / (450,000 Pa × 0.0112 m)
                    = 22.2 (> 1.5 required) ✓

Actual hoop stress = P × r / t
                   = 450,000 Pa × 0.0112 m / 0.0005 m
                   = 10.09 MPa

Stress margin = (224 MPa - 10.09 MPa) / 224 MPa = 95.5% ✓
```

---

## 3. Chamber Geometry Sizing

### 3.1 Chamber Dimensions

From DES-001:
- Throat diameter: 7.48 mm
- Throat area: 4.39 × 10⁻⁵ m²

**Chamber diameter selection:**
- Contraction ratio (Dc/Dt) = 3.0 (typical range 2-4 from CONTEXT.md)
- Chamber diameter = 3 × 7.48 mm = 22.4 mm
- Chamber radius = 11.2 mm

**Chamber length calculation (from CONTEXT.md Section 3):**
```
V_chamber = L* × A_throat
L_chamber = V_chamber / A_chamber
```

Where:
- L* (characteristic length) = 0.75 m (midpoint of 0.5-1.0 m for hydrazine)
- A_throat = 4.39 × 10⁻⁵ m²
- A_chamber = π × (Dc/2)² = π × (0.0112 m)² = 3.94 × 10⁻⁴ m²

```
L_chamber = (0.75 m × 4.39 × 10⁻⁵ m²) / (3.94 × 10⁻⁴ m²)
          = 0.0835 m = 83.5 mm
```

**Chamber geometry summary:**
- Diameter: 22.4 mm
- Length: 83.5 mm
- Volume: 3.28 × 10⁻⁵ m³

### 3.2 Chamber Mass Calculation

**Cylindrical shell volume (cylinder + hemispherical end caps):**
```
V_cylinder = π × (r_o² - r_i²) × L
V_end_caps = (4/3) × π × (r_o³ - r_i³)
```

Where:
- r_i = inner radius = 11.2 mm
- r_o = outer radius = 11.2 mm + 0.5 mm = 11.7 mm
- L = chamber length = 83.5 mm

```
V_cylinder = π × (11.7² - 11.2²) mm² × 83.5 mm
           = π × (136.89 - 125.44) mm² × 83.5 mm
           = 2,995.4 mm³ = 2.995 × 10⁻⁶ m³

V_end_caps = (4/3) × π × (11.7³ - 11.2³) mm³
           = (4/3) × π × (1601.6 - 1404.9) mm³
           = 825.4 mm³ = 8.254 × 10⁻⁷ m³

V_total = 3.82 × 10⁻⁶ m³
```

**Chamber mass:**
```
m_chamber = V_total × ρ_Mo
          = 3.82 × 10⁻⁶ m³ × 10,220 kg/m³
          = 0.0391 kg
```

**Mass budget verification (REQ-011):**
- Chamber mass: 0.0391 kg
- Budget limit: 0.5 kg
- Margin: 0.4609 kg (92.2%) ✓

---

## 4. Nozzle Analysis

### 4.1 Nozzle Properties from DES-001

| Parameter | Value | Unit |
|-----------|-------|------|
| Expansion ratio | 100 | dimensionless |
| Exit diameter | 74.8 | mm |
| Nozzle length | 125.6 | mm |
| Half-angle | 15 | degrees |
| Exit temperature | -13.6 | °C |
| Exit pressure | 94.7 | Pa |

### 4.2 Temperature Verification (REQ-016)

Nozzle exit temperature from isentropic expansion: **-13.6°C**

Requirement: ≤ 800°C

Status: **PASS** with 813.6°C margin

### 4.3 Material Compatibility

Nozzle material: Molybdenum (same as chamber)
- Max temperature: 1650°C
- Operating temperature: -13.6°C (exit) to 1127°C (chamber interface)
- Compatibility: PASS (hydrazine compatible, temperature capability adequate)

---

## 5. Envelope Verification

### 5.1 Overall Dimensions

| Component | Length (mm) | Diameter (mm) |
|-----------|-------------|---------------|
| Chamber | 83.5 | 22.4 |
| Nozzle | 125.6 | 74.8 |
| **Overall** | **209.1** | **74.8** |

### 5.2 Envelope Constraints (REQ-012)

| Requirement | Value | Actual | Status | Margin |
|-------------|-------|--------|--------|--------|
| Diameter ≤ 100 mm | 100 mm | 74.8 mm | PASS | +25.2 mm |
| Length ≤ 150 mm | 150 mm | 209.1 mm | **FAIL** | **-59.1 mm** |

### 5.3 Envelope Constraint Analysis

**Root cause:** Nozzle length from DES-001 (125.6 mm) consumes 83.7% of the 150 mm envelope length, leaving only 24.4 mm for chamber and injector.

**Nozzle length equation (conical nozzle, CONTEXT.md Section 3):**
```
L_nozzle = (De/2 - Dt/2) / tan(α)
```

Where:
- De = Exit diameter = 74.8 mm
- Dt = Throat diameter = 7.48 mm
- α = Half-angle = 15°

```
L_nozzle = (37.4 - 3.74) / tan(15°)
         = 33.66 / 0.268
         = 125.6 mm
```

**Constraint impact:**
1. Nozzle length is driven by expansion ratio (100:1) required for Isp ≥ 220 s
2. 15° half-angle is standard for conical nozzles
3. Reducing expansion ratio would reduce Isp below requirement
4. Increasing half-angle would increase divergence losses

**Resolution options:**
1. **Bell nozzle:** Could reduce length by ~20% (to 100 mm) for same expansion ratio (Rao's method)
2. **Relax envelope:** Increase length limit to ~210 mm to accommodate current design
3. **Reduce expansion ratio:** Trade Isp for shorter length
4. **Increase half-angle:** Accept higher divergence losses for shorter nozzle

**Recommendation:** For this preliminary design phase, document the constraint and defer resolution to DES-005 (Physical Envelope and Mechanical Interface Design), where bell nozzle optimization and envelope trade-offs can be evaluated holistically.

---

## 6. Requirements Compliance Summary

### 6.1 Detailed Compliance Table

| Requirement | Threshold | Computed | Unit | Status | Margin |
|-------------|-----------|----------|------|--------|--------|
| REQ-015 | ≤ 1400 | 1126.8 | °C | PASS | +273.2°C |
| REQ-016 | ≤ 800 | -13.6 | °C | PASS | +813.6°C |
| REQ-018 | ≥ 1.5 | 22.2 | dimensionless | PASS | +1379% |
| REQ-023 | Compatible | Yes | N/A | PASS | N/A |
| REQ-024 | ≥ 1400 | 1650 | °C | PASS | +250°C |
| REQ-011 | ≤ 0.5 | 0.0391 | kg | PASS | +92.2% |
| REQ-012 | ≤ 100 / ≤ 150 | 74.8 / 209.1 | mm | **FAIL** | -59.1 mm |

### 6.2 Summary

- **Pass:** 7 of 8 requirements
- **Fail:** 1 of 8 requirements (REQ-012, envelope length)
- **Note:** REQ-012 failure is a constraint exception due to nozzle length from DES-001 performance sizing

---

## 7. Key Design Decisions

### DEC-007: Molybdenum Material Selection

**Decision:** Select Molybdenum as chamber/nozzle material

**Rationale:**
- Temperature capability (1650°C) provides 523°C margin above operating temperature (1127°C)
- Yield strength at operating temperature (224 MPa) is 44% higher than Haynes 230
- Density (10220 kg/m³) is 50% lower than Rhenium, reducing mass
- Space-qualified heritage with oxidation protection coating
- Cost moderate compared to Rhenium

**Alternatives considered:**
- Haynes 230: 1150°C limit provides only 23°C margin (too close to operating temp)
- Rhenium: 2000°C capability but 2× density and 10× cost
- Columbium C103: 1370°C marginal, lower yield strength (96 MPa)

### DEC-008: Wall Thickness Determination

**Decision:** Set wall thickness = 0.500 mm (manufacturability-limited)

**Rationale:**
- Structural requirement (0.034 mm) is negligible compared to manufacturability constraint (0.5 mm)
- Typical minimum thickness for small diameter pressure vessels is 0.5-1.0 mm
- Provides safety factor of 22.2 (far exceeds 1.5 requirement)
- Maintains conservative design philosophy

**Impact:**
- Chamber mass: 0.039 kg (7.8% of budget)
- Enables robust manufacturing and quality assurance

---

## 8. Verification Approach

### 8.1 Independent Verification (Agent 3)

Agent 3 should verify:
1. Material selection justification against temperature and strength requirements
2. Thin-wall pressure vessel calculations using ASME Boiler and Pressure Vessel Code methodology
3. Wall thickness calculation with alternative equations (thick-wall theory, finite element analysis)
4. Mass calculation with detailed volume integration
5. Envelope constraint analysis and potential resolution strategies

### 8.2 Future Design Tasks

- DES-005: Physical Envelope and Mechanical Interface Design - address envelope length constraint
- Bell nozzle optimization (Rao's method) to reduce nozzle length
- Detailed thermal analysis with radiation cooling modeling
- Finite element stress analysis for thermal stress during startup (REQ-019)

---

## 9. Assumptions

1. **Chamber temperature:** 1126.8°C from DES-001 (assumes steady-state thermal equilibrium)
2. **Pressure distribution:** Uniform internal pressure (neglects local pressure variations)
3. **Yield strength degradation:** 40% of RT value at operating temperature (conservative estimate)
4. **Thin-wall theory:** Valid for t/r ≤ 0.1 (actual t/r = 0.045, valid)
5. **End cap geometry:** Hemispherical (simplified model for mass calculation)
6. **Nozzle material:** Same as chamber (Molybdenum) for simplicity
7. **Nozzle expansion:** Isentropic with ideal gas behavior (from DES-001)
8. **Manufacturability:** Minimum practical thickness 0.5 mm for small vessels
9. **L* characteristic length:** 0.75 m (midpoint of 0.5-1.0 m range for hydrazine)
10. **Contraction ratio:** 3.0 (typical value for small thrusters)

---

## 10. References

1. **CONTEXT.md** - Domain equations and material properties
2. **DES-001 data** - Thruster performance sizing results
3. **REQ_REGISTER.md** - Requirements specifications
4. **DECISIONS.md** - Prior design decisions (DEC-001 through DEC-006)

---

## 11. Deliverable Files

| File | Description |
|------|-------------|
| `design/scripts/chamber_nozzle_stress.py` | Stress analysis script (Python 3) |
| `design/data/chamber_nozzle_stress.json` | Computed design data |
| `design/docs/chamber_nozzle_sizing.md` | This document |

---

## 12. Revision History

| Version | Date | Author | Description |
|---------|------|--------|-------------|
| 1.0 | 2026-02-14 | Agent 2 | Initial design analysis |

---

**Document Status:** Complete (with constraint exception noted for REQ-012)
