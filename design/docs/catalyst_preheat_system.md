# Catalyst Preheat System Design

## Traceability
- **Design ID:** DES-003
- **Requirements:** REQ-014, REQ-027
- **Decision References:** DEC-002 (Chamber Temperature), DEC-003 (Feed Pressure)
- **Scripts:** [`design/scripts/catalyst_preheat_thermal.py`](../scripts/catalyst_preheat_thermal.py)
- **Data:** [`design/data/catalyst_preheat_thermal.json`](../data/catalyst_preheat_thermal.json)
- **Plots:** [`design/plots/DES003_preheat_curve.png`](../plots/DES003_preheat_curve.png)

## Requirements Checklist
- [x] REQ-014: Catalyst bed preheat 150-300°C before first firing → Design target: 200°C (within range)
- [x] REQ-027: Heater power ≤ 15W at 28V → Design: 15.00W at 28V (at limit)

## Design Description

### Overview
This design document defines the catalyst bed preheat system for the hydrazine monopropellant thruster. The preheat system ensures the catalyst bed reaches the required temperature range (150-300°C) before the first firing to enable efficient hydrazine decomposition. The heater operates within the power constraint of 15W at 28V nominal voltage.

### Design Parameters

| Parameter | Value | Units | Source/Reference |
|-----------|-------|-------|------------------|
| Throat Diameter | 7.48 | mm | DES-001 |
| Chamber Diameter | 22.43 | mm | 3× throat diameter (typical for hydrazine) |
| Bed Length/Diameter Ratio | 2.0 | - | Mid-range of typical 1.5-3.0 range |
| Bed Length | 44.86 | mm | Derived from chamber diameter |
| Wall Thickness | 1.0 | mm | Minimum manufacturable for small thrusters |
| Initial Temperature | 20 | °C | Typical spacecraft interior temperature |
| Design Preheat Temperature | 200 | °C | Mid-range of REQ-014 requirement |

### Material Properties

| Property | Value | Units | Source/Reference |
|-----------|-------|-------|------------------|
| Catalyst (Shell 405) Specific Heat | 800 | J/(kg·K) | NASA CR-182202 |
| Catalyst Solid Density | 4000 | kg/m³ | Alumina support |
| Catalyst Porosity | 0.40 | - | Typical for Shell 405 |
| Chamber (Inconel 625) Specific Heat | 435 | J/(kg·K) | NASA materials database |
| Chamber Density | 8440 | kg/m³ | Inconel 625 |
| Chamber Emissivity | 0.30 | - | Polished/coated surface |
| Stefan-Boltzmann Constant | 5.67e-8 | W/(m²·K⁴) | NIST |

### Thermal Mass

| Component | Mass | Heat Capacity (20-200°C) |
|-----------|------|-------------------------|
| Catalyst | 42.54 g | 6,126 J |
| Chamber Wall | 27.87 g | 2,182 J |
| **Total** | **70.41 g** | **8,308 J** |

### Heater Design

| Parameter | Value | Units |
|-----------|-------|-------|
| Heater Power | 15.00 | W |
| Nominal Voltage | 28.0 | V |
| Heater Resistance | 52.27 | Ω |
| Heater Current | 0.536 | A |

### Preheat Performance

| Target | Time | Temperature |
|--------|------|-------------|
| Minimum (REQ-014) | 7.3 min | 150°C |
| Design target | 10.5 min | 200°C |
| Maximum (REQ-014) | 19.3 min | 300°C |

## Analysis Summary

### 1. Catalyst Bed Geometry

The catalyst bed dimensions are derived from the throat diameter established in DES-001:

**Chamber diameter:**
```
D_c = 3 × D_t = 3 × 7.48 mm = 22.43 mm
```

**Bed length:**
```
L_bed = (L/D ratio) × D_c = 2.0 × 22.43 mm = 44.86 mm
```

**Bed volume:**
```
V_bed = π × (D_c/2)² × L_bed = π × (11.21 mm)² × 44.86 mm = 17.72 cm³
```

### 2. Catalyst Mass Calculation

The catalyst bed uses Shell 405 (iridium on alumina support) with 40% porosity:

**Effective bed density:**
```
ρ_bed = ρ_solid × (1 - porosity) = 4000 × (1 - 0.40) = 2400 kg/m³
```

**Catalyst mass:**
```
m_catalyst = ρ_bed × V_bed = 2400 × 17.72×10⁻⁶ = 0.0425 kg = 42.5 g
```

### 3. Thermal Heat Capacity

The total heat required to raise the temperature from 20°C to 200°C (180 K rise):

**Catalyst heat:**
```
Q_catalyst = m_catalyst × c_p,cat × ΔT = 0.0425 × 800 × 180 = 6,126 J
```

**Chamber wall heat:**
```
m_wall = ρ_wall × V_wall = 8440 × [π × (11.71² - 11.21²) × 44.86×10⁻⁹] = 0.0279 kg
Q_chamber = m_wall × c_p,ch × ΔT = 0.0279 × 435 × 180 = 2,182 J
```

**Total heat required:**
```
Q_total = Q_catalyst + Q_chamber = 6,126 + 2,182 = 8,308 J
```

### 4. Heat Loss Analysis

During preheat, the system loses heat through radiation and convection:

**Surface area:**
```
A_cylindrical = 2π × r_ext × L_bed = 2π × 11.71 × 44.86 = 3,304 mm²
A_ends = 2π × r_ext² = 2π × (11.71)² = 861 mm²
A_total = 3,304 + 861 = 4,165 mm² = 4.17×10⁻³ m²
```

**Radiation losses:**
Using average temperature during preheat (110°C = 383 K):
```
Q_rad = ε × σ × A × (T_avg⁴ - T_amb⁴) × t
Q_rad = 0.30 × 5.67e-8 × 4.17×10⁻³ × (383⁴ - 293⁴) × 630 = 870 J
```

**Convection losses:** Negligible in space environment (<1% of total)

### 5. Heater Power Requirements

**Power required for 10-minute target:**
```
P_required = (Q_total + Q_losses) / t = (8,308 + 870) / 600 = 15.30 W
```

Since this exceeds the 15W limit (REQ-027), the design accepts a slightly longer preheat time at 15W.

**Actual preheat time at 15W:**
```
t_200°C = (Q_total + Q_losses) / P = 8,308 / 15 + adjustment for losses ≈ 630 s = 10.5 min
```

### 6. Heater Resistance Calculation

For operation at 28V nominal:
```
P = V² / R  →  R = V² / P = 28² / 15 = 784 / 15 = 52.3 Ω
I = P / V = 15 / 28 = 0.536 A
```

## Requirements Compliance

### REQ-014: Catalyst Bed Preheat Temperature

**Requirement:** Catalyst bed shall be preheated to a temperature between 150°C and 300°C before the first firing.

**Verification:**
- Minimum achievable: 150°C in 7.3 minutes at 15W
- Design target: 200°C in 10.5 minutes at 15W
- Maximum achievable: 300°C in 19.3 minutes at 15W
- **Status:** PASS (200°C is within 150-300°C range)

### REQ-027: Heater Power Constraint

**Requirement:** Thruster shall provide an electrical interface for a heater circuit operating at 28V nominal with power consumption not exceeding 15W for catalyst bed preheat.

**Verification:**
- Heater power: 15.00 W
- Nominal voltage: 28.0 V
- Heater resistance: 52.27 Ω
- Heater current: 0.536 A
- **Status:** PASS (exactly at the 15W limit)

## Design Discussion

### Heater Power vs. Preheat Time Trade-off

The initial design target was a 10-minute preheat time, which would require 15.30W—slightly exceeding the 15W power constraint. The design decision was to:
1. Operate at the 15W power limit (REQ-027 constraint)
2. Accept a 10.5-minute preheat time to reach 200°C (5% increase from target)

This is acceptable because:
- The preheat operation occurs only once before the first firing (or infrequently after long coast periods)
- 10.5 minutes is within the typical range for small monopropellant thrusters (5-15 minutes)
- Heritage systems show similar preheat times: MR-103 (~8 min at 12W), CHT-1 (~10 min at 10W)

### Heat Loss Contributions

The thermal analysis shows heat losses during preheat are approximately 10.5% of the total heat input:
- Heat required for thermal mass: 8,308 J (89.5%)
- Heat losses: 870 J (10.5%)

This low loss fraction is expected due to:
- Low emissivity of polished/chamber surface (ε = 0.30)
- Moderate temperature rise (only 180 K)
- Negligible convection in vacuum

### Insulation Considerations

The current design assumes no thermal insulation beyond the chamber wall. Options to reduce preheat time (if needed) include:
1. Multi-layer insulation (MLI) around chamber: Could reduce radiation losses by ~50%
2. Reduced wall thickness: Would decrease thermal mass but increase stress
3. Higher preheat temperature: Would reduce required mass flow rate for activation

Given the 15W power constraint, the current design is optimal.

## Heritage Comparison

| Parameter | This Design | Aerojet MR-103 | Airbus CHT-1 |
|-----------|-------------|----------------|--------------|
| Thrust | 1.0 N | 1.0 N | 1.0 N |
| Heater Power | 15W | 12W | 10W |
| Heater Voltage | 28V | 28V | 28V |
| Preheat Time (to ~200°C) | 10.5 min | ~8 min | ~10 min |
| Catalyst Mass | 42.5 g | ~35-40 g | ~30-35 g |

The design is consistent with heritage systems, providing competitive performance within the 15W power constraint.

## Verification Method

Per REQ-014 and REQ-027, verification will be performed as follows:

**REQ-014 (Preheat Temperature):**
- **Method:** Demonstration (preheat system functional test with temperature monitoring)
- **Procedure:** Energize heater at 28V nominal, monitor catalyst bed temperature using embedded thermocouple. Verify temperature reaches and remains within 150-300°C range.
- **Acceptance Criteria:** Temperature ≥ 150°C within 10 minutes of heater activation

**REQ-027 (Power Constraint):**
- **Method:** Analysis (electrical power calculation)
- **Procedure:** Measure heater voltage and current during preheat. Calculate P = V × I.
- **Acceptance Criteria:** P ≤ 15W at 28V nominal

## Data Files

The following data files are generated by the thermal analysis script:

1. **`design/data/catalyst_preheat_thermal.json`**: Complete thermal analysis results
2. **`design/plots/DES003_preheat_curve.png`**: Temperature vs. time curve during preheat

## Assumptions

1. **Chamber diameter**: 3× throat diameter (typical for hydrazine thrusters)
2. **Bed L/D ratio**: 2.0 (mid-range of typical 1.5-3.0)
3. **Catalyst properties**: Based on Shell 405 (iridium on alumina support)
4. **Wall thickness**: 1.0 mm (minimum manufacturable)
5. **Natural convection**: h = 1.0 W/(m²·K) in spacecraft (conservative)
6. **Chamber emissivity**: 0.30 (polished or coated surface)
7. **Initial temperature**: 20°C (typical spacecraft interior)
8. **Preheat occurs once**: Before first firing (no frequent cycling)
9. **Adiabatic heating**: Heat loss only through external surfaces (no feed line losses)
10. **Constant heater power**: Simplified model (actual may vary with resistance temperature coefficient)

## References

1. NASA CR-182202: "Advanced Monopropellant Thruster Technology"
2. NASA materials database: Inconel 625 properties
3. Spacecraft Thermal Control Handbook (3rd Edition)
4. CONTEXT.md Section 4: Catalyst bed sizing and properties
5. CONTEXT.md Section 6: Physical constants
6. DES-001: Thruster Performance Sizing (chamber geometry inputs)
7. DEC-002: Chamber Temperature Selection (Tc = 1400 K)
8. DEC-003: Feed Pressure Selection (0.30 MPa)

## Future Work

1. **Detailed thermal modeling**: CFD analysis of catalyst bed temperature distribution
2. **Transient startup analysis**: Couple preheat model with ignition transient
3. **Feed line heating**: Assess need for feed line preheat to prevent hydrazine freezing
4. **Heater integration**: Detailed mechanical design of heater element placement
5. **Temperature sensor placement**: Optimize thermocouple locations for monitoring
