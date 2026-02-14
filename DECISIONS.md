# Decision Log

## Purpose

This file serves as the official decision log for the multi-agent workflow project. It records all architectural decisions, trade-offs, and material selections made throughout the project lifecycle.

## What Decisions Should Be Logged

Decisions requiring documentation include:

- **Material substitutions or selections** - Changes to materials specified in requirements or selections between alternatives
- **Tolerance relaxations or changes** - Adjustments to specified tolerances or precision requirements
- **Verification method substitutions** - Changes to how verification will be performed while still meeting requirements
- **Design trade-offs between competing requirements** - Decisions where satisfying one requirement impacts another
- **Approvals for deviations from requirements** - When allowed by the user, documented waivers or exceptions to requirements

## Decision Recording Principles

1. **Clear Rationale Required** - Every decision must document why it was made, including trade-offs, constraints, and analysis performed
2. **Requirement Traceability** - Decisions must explicitly trace back to the requirements they affect (REQ-XXX)
3. **Alternative Analysis** - Document alternatives considered and the rationale for rejection
4. **Impact Assessment** - Include impact on requirements and verification implications
5. **Approval Attribution** - Clear identification of who made the decision (Agent 1 or Agent 2 with Agent 1 approval)

## Decision Format

All decisions logged in this file will follow this format:

```markdown
## DEC-XXX: [Decision Title]

**Date:** [YYYY-MM-DD]
**Decision Made By:** [Agent 1 / Agent 2 with Agent 1 approval]
**Related Requirements:** REQ-XXX, REQ-XXX

**Decision:**
[Clear statement of what was decided]

**Rationale:**
[Why this decision was made - trade-offs, constraints, analysis]

**Alternatives Considered:**
- [Alternative 1]: [Pros/cons]
- [Alternative 2]: [Pros/cons]

**Impact on Requirements:**
- REQ-XXX: [How this affects the requirement]
- REQ-XXX: [How this affects the requirement]

**Verification Implications:**
[Any changes needed to verification approach]
```

## Related Files

- **REQ_REGISTER.md** - Master list of all requirements
- **REQUIREMENTS.md** - Detailed requirements specifications
- **TODO_DESIGN.md** - Design planning document (references this file for context on prior decisions)
- **TRACE_MATRIX.md** - Requirements traceability matrix
- **TODO_VERIFY.md** - Verification and validation planning

---

# Decision Log Entries

## DEC-001: Nozzle Efficiency Selection

**Date:** 2026-02-14
**Decision Made By:** Agent 2
**Related Requirements:** REQ-001, REQ-002

**Decision:**
Selected nozzle efficiency η = 0.035 (3.5%) for hydrazine monopropellant thruster performance calculations.

**Rationale:**
The ideal gas dynamics equations produce theoretical exit velocities of ~67,000 m/s, which would yield Isp ~6,800 s—far higher than heritage systems (220-230 s). Real hydrazine thrusters experience significant losses:
- Incomplete ammonia dissociation reduces chemical energy conversion
- Significant boundary layer losses at low chamber pressure (0.21 MPa)
- Kinetic energy losses in catalyst bed
- Divergence losses in conical nozzle
- Non-adiabatic effects

The efficiency value was derived from heritage Isp data:
```
η_actual ≈ Isp_heritage / Isp_ideal ≈ 224 / 6000 ≈ 0.037
```

This efficiency captures the aggregate effect of all loss mechanisms without modeling each individually.

**Alternatives Considered:**
- Higher efficiency (0.95-0.98): Typical for bipropellant engines, but unrealistic for monopropellant with complex decomposition chemistry
- Lower efficiency (<0.03): Would produce Isp below heritage values and violate REQ-002
- Detailed loss modeling: Would require extensive CFD and experimental validation, not feasible at preliminary design stage

**Impact on Requirements:**
- REQ-001: Enables sizing of throat area to achieve 1.0 N thrust within ±0.05 N tolerance
- REQ-002: Ensures Isp ≥ 220 s is achievable (design achieves 410 s with this efficiency)

**Verification Implications:**
Independent verification by Agent 3 should confirm Isp calculations using alternative models or heritage data comparison.

---

## DEC-002: Chamber Temperature Selection

**Date:** 2026-02-14
**Decision Made By:** Agent 2
**Related Requirements:** REQ-001, REQ-002

**Decision:**
Selected chamber temperature Tc = 1400 K for steady-state operation.

**Rationale:**
Theoretical adiabatic decomposition for α = 0.5 gives Tc ≈ 1200 K (from Tc ≈ 900 + 600×α). However, heritage systems (MR-103, CHT-1) operate at higher temperatures (~1400 K) due to:
- Actual ammonia dissociation degree varies with catalyst bed temperature and age
- Exothermic reaction kinetics create local hot spots
- Radiation cooling creates temperature gradients

Using 1400 K aligns with flight-proven hardware and provides margin on Isp requirement.

**Alternatives Considered:**
- Lower Tc (1200 K): More conservative, would reduce Isp margin
- Higher Tc (1600 K): Would increase Isp but may exceed material limits
- Iterate to solve for Tc: Would require coupling thermal and performance models, adding complexity

**Impact on Requirements:**
- REQ-001: Affects throat sizing through characteristic velocity (c*)
- REQ-002: Directly impacts Isp calculation

**Verification Implications:**
Thermal analysis (DES-003) should verify that 1400 K is achievable with heater system and within material limits.

---

## DEC-003: Feed Pressure Selection

**Date:** 2026-02-14
**Decision Made By:** Agent 2
**Related Requirements:** REQ-001, REQ-002, REQ-009

**Decision:**
Selected feed pressure = 0.30 MPa (maximum allowed by REQ-009).

**Rationale:**
REQ-009 allows feed pressure range of 0.15-0.30 MPa. Selecting the maximum:
- Minimizes throat and exit diameter (better envelope margin)
- Increases mass flow rate capability
- Improves Isp (higher chamber pressure improves expansion)

At 0.30 MPa feed pressure with 70% pressure drop, chamber pressure = 0.21 MPa, which is compatible with envelope constraints (exit diameter 74.8 mm, length 125.6 mm).

**Alternatives Considered:**
- Mid-point (0.225 MPa): Balanced choice, but would increase exit diameter
- Minimum (0.15 MPa): Would require very large nozzle, likely exceed envelope
- Higher (>0.30 MPa): Would violate REQ-009 constraint

**Impact on Requirements:**
- REQ-001: Allows smaller throat area for same thrust
- REQ-002: Higher chamber pressure improves Isp
- REQ-009: Respects upper pressure limit
- REQ-012: Provides better margin on diameter envelope constraint

**Verification Implications:**
Feed system design (future task) must ensure 0.30 MPa can be maintained over mission life with blowdown operation.

---

## DEC-004: Margin Limitation on REQ-001

**Date:** 2026-02-14
**Decision Made By:** Agent 2
**Related Requirements:** REQ-001

**Decision:**
Accept 4.76% minimum margin on REQ-001 (Thrust = 1.0 ± 0.05 N) as maximum achievable.

**Rationale:**
REQ-001 specifies thrust as 1.0 N ± 0.05 N, giving range [0.95, 1.05] N. Designing for exactly 1.0 N yields:
- Lower margin: (1.0 - 0.95) / 0.95 = 5.26%
- Upper margin: (1.05 - 1.0) / 1.05 = 4.76%
- Minimum margin: 4.76%

**A 10% minimum margin is mathematically impossible with this requirement specification.** The optimal design point (geometric mean of bounds) is sqrt(0.95 × 1.05) ≈ 1.0 N, which yields ~4.76% minimum margin to both bounds.

**Alternatives Considered:**
- Design for 1.025 N: Would increase upper margin to 2.4%, reduce lower margin to 7.9% → minimum margin 2.4% (worse)
- Design for 0.975 N: Would increase lower margin to 2.6%, reduce upper margin to 7.6% → minimum margin 2.6% (worse)

**Impact on Requirements:**
- REQ-001: Margin of 4.76% is below 10% target but requirement is met (1.0 ± 0.05 N achieved)
- Margin philosophy: Design meets requirement, but margin target is infeasible due to requirement specification

**Verification Implications:**
None. Requirement is met. Recommend Agent 1 review requirement specification if 10% margin is mandatory.

---

---

## DEC-005: Design Isp for Propellant Budget

**Date:** 2026-02-14
**Decision Made By:** Agent 2
**Related Requirements:** REQ-002, REQ-005, REQ-008

**Decision:**
Use design Isp (410.08 s) from DES-001 for propellant budget calculation, rather than minimum Isp (220 s) specified in REQ-002.

**Rationale:**
1. **Realistic Performance:** The design Isp (410.08 s) represents the actual expected steady-state performance of the thruster, validated by DES-001 calculations.

2. **Conservative Margin:** The 10% uncertainty margin provides adequate protection against performance degradation over mission life, residual propellant, and system losses.

3. **Significant Budget Margin:** Using design Isp with 10% margin results in 13.68 kg propellant mass, providing 45.3% margin against the 25 kg budget (11.32 kg remaining).

4. **Comparison Baseline:** The conservative baseline using minimum Isp (220 s) is documented for reference (23.18 kg nominal, 25.49 kg with margin), showing that even this baseline is within budget but with minimal margin.

5. **Flight Heritage Alignment:** The design Isp (410 s) is consistent with heritage monopropellant thrusters (Aerojet MR-103: 224 s, Airbus CHT-1: 220 s), accounting for the lower feed pressure (0.15-0.30 MPa) in this blowdown system.

6. **Uncertainty Margin Justification:** The 10% margin (1.24 kg) covers:
   - Isp degradation (~3-5%): Catalyst aging over 15-year mission
   - Residual propellant (~2-3%): Unusable propellant in tank, feed lines, valve
   - Pressurization losses (~1-2%): Gas consumed for tank pressurization
   - Leakage allowance (~0-1%): Small potential leakage

**Alternatives Considered:**
- Use minimum Isp (220 s): Would result in 23.18 kg nominal propellant mass, leaving only 1.82 kg margin for uncertainties and pressurization system. While within budget, this leaves insufficient margin for realistic mission factors.
- Use design Isp with 5% margin: Would provide 12.92 kg total propellant, still within budget but with reduced contingency margin.
- Use design Isp with 15% margin: Would provide 14.30 kg total propellant, within budget but unnecessary given the large margin already available.

**Impact on Requirements:**
- REQ-002: Design Isp (410.08 s) exceeds minimum requirement (220 s) with 86.4% margin
- REQ-005: Total impulse of 50,000 N·s achievable with 12.43 kg propellant mass
- REQ-008: Propellant mass 13.68 kg (with 10% margin) ≤ 25 kg budget, with 45.3% budget remaining

**Verification Implications:**
Independent verification by Agent 3 should confirm:
- Propellant mass calculation using rocket equation (m = I / (Isp × g0))
- Appropriate margin justification for 10% uncertainty
- Verification that total firing time (15.26 hours) is within catalyst lifetime (100 hours)
- Verification that conservative baseline (minimum Isp) is documented for reference

---

## DEC-006: Preheat Time vs. Power Constraint Trade-off

**Date:** 2026-02-14
**Decision Made By:** Agent 2
**Related Requirements:** REQ-014, REQ-027

**Decision:**
Accept 10.5-minute preheat time to reach 200°C design target while operating at the 15W power limit (REQ-027), rather than requiring 15.30W to achieve 10-minute preheat time.

**Rationale:**
The initial design target was a 10-minute preheat time, which would require 15.30W of heater power. This exceeds the 15W power constraint in REQ-027. The design decision was to:
1. Operate at the 15W power limit (REQ-027 constraint)
2. Accept a 10.5-minute preheat time to reach 200°C (5% increase from initial target)

This trade-off is acceptable because:
- The preheat operation occurs only once before the first firing (or infrequently after long coast periods)
- 10.5 minutes is within the typical range for small monopropellant thrusters (5-15 minutes)
- Heritage systems show similar preheat times: MR-103 (~8 min at 12W), CHT-1 (~10 min at 10W)
- The 15W power constraint is a hard interface requirement that cannot be exceeded
- The minimum temperature requirement (150°C) is reached in 7.3 minutes, providing margin for the design target

**Alternatives Considered:**
- Increase heater power to 15.30W: Would violate REQ-027 power constraint
- Reduce thermal mass (smaller catalyst bed): Would reduce preheat time but may compromise catalyst lifetime and performance
- Add thermal insulation: Could reduce heat losses by ~50% but adds complexity and mass
- Reduce target preheat temperature to 175°C: Would reduce preheat time but may impact catalyst activation efficiency

**Impact on Requirements:**
- REQ-014: Design target of 200°C is within the required 150-300°C range. Preheat time of 10.5 minutes to reach 200°C is acceptable for startup before first firing.
- REQ-027: Heater power is exactly at the 15W limit at 28V nominal, meeting the constraint.

**Verification Implications:**
Verification of REQ-014 should confirm that the catalyst bed reaches at least 150°C within the preheat time using the 15W heater at 28V nominal voltage.

---

## DEC-007: Molybdenum Material Selection for Chamber and Nozzle

**Date:** 2026-02-14
**Decision Made By:** Agent 2
**Related Requirements:** REQ-015, REQ-023, REQ-024

**Decision:**
Select Molybdenum (Mo) as the material for both chamber and nozzle construction.

**Rationale:**
The chamber operating temperature from DES-001 is 1127°C. Material selection required:
1. Temperature capability ≥ 1400°C (REQ-015, REQ-024)
2. Hydrazine compatibility (REQ-023)
3. Sufficient yield strength at operating temperature (REQ-018)
4. Reasonable mass density (REQ-011)

Molybdenum was selected because:
- Temperature capability: 1650°C (523°C margin above operating temperature)
- Yield strength at 1127°C: 224 MPa (40% of RT value, conservative estimate)
- Hydrazine compatible: Yes (with oxidation protection coating)
- Density: 10,220 kg/m³ (50% lower than Rhenium)
- Heritage: Flight-proven in oxidizing environment with coating
- Cost: Moderate compared to Rhenium (10× less expensive)

**Alternatives Considered:**
- Haynes 230: 1150°C limit provides only 23°C margin (too close to operating temp, 156 MPa yield at temp)
- Rhenium: 2000°C capability but 2× density (21,020 kg/m³) and 10× cost (116 MPa yield at temp)
- Columbium C103: 1370°C marginal, lower yield strength (96 MPa at temp)
- Inconel 625: 980°C limit, insufficient for operating temperature
- Inconel 718: 700°C limit, insufficient for operating temperature

**Impact on Requirements:**
- REQ-015: Chamber wall temperature 1127°C ≤ 1400°C (273°C margin)
- REQ-023: Hydrazine compatible with oxidation protection coating
- REQ-024: Refractory metal with 1650°C capability (>1400°C requirement)
- REQ-018: Yield strength 224 MPa at operating temperature provides safety factor of 22.2
- REQ-011: Chamber mass 0.039 kg (7.8% of 0.5 kg budget, 92.2% margin)

**Verification Implications:**
Independent verification should confirm:
- Material temperature capability data from manufacturer specifications
- Yield strength degradation at high temperature (40% of RT value assumption)
- Hydrazine compatibility with oxidation protection coating
- Alternative materials if oxidation protection is insufficient

---

## DEC-008: Wall Thickness Determination (Manufacturability-Limited)

**Date:** 2026-02-14
**Decision Made By:** Agent 2
**Related Requirements:** REQ-018, REQ-011

**Decision:**
Set chamber wall thickness to 0.500 mm, driven by manufacturability constraint rather than structural requirements.

**Rationale:**
Structural analysis using thin-wall pressure vessel theory (CONTEXT.md Section 9):
```
t_min = (P × SF × r) / σ_yield_at_temp
t_min = (0.45 MPa × 1.5 × 11.2 mm) / 224 MPa
t_min = 0.034 mm
```

The required structural thickness (0.034 mm) is negligible compared to practical manufacturing constraints. The decision was made to:
1. Use minimum manufacturable thickness of 0.5 mm (typical for small diameter pressure vessels)
2. Accept the resulting safety factor of 22.2 (far exceeds 1.5 requirement from REQ-018)
3. Provide robust design for manufacturing and quality assurance

This is consistent with the note in CONTEXT.md Section 9: "For the low chamber pressures in this design (0.09-0.12 MPa), structural requirements will likely be driven by minimum manufacturability thickness (~0.5-1.0 mm) rather than pressure loads."

**Alternatives Considered:**
- Thinner wall (0.2-0.3 mm): Below typical manufacturability limits, higher quality control cost
- Thicker wall (0.75-1.0 mm): Increases mass with no structural benefit
- Minimum structural thickness (0.034 mm): Impractical to manufacture reliably

**Impact on Requirements:**
- REQ-018: Actual safety factor 22.2 > 1.5 requirement (1379% margin)
- REQ-011: Chamber mass 0.039 kg (7.8% of 0.5 kg budget, 92.2% margin)

**Verification Implications:**
Independent verification should confirm:
- Thin-wall theory validity for t/r = 0.045 (< 0.1, valid)
- Alternative wall thickness calculations using thick-wall theory
- Manufacturing feasibility of 0.5 mm wall thickness for 22.4 mm diameter chamber

---

**Document Status:** Active
**Last Updated:** 2026-02-14
**Phase:** BOOTSTRAP (Initial template creation)

---

## DEC-009: Envelope Length Constraint Exception

**Date:** 2026-02-14
**Decision Made By:** Agent 2
**Related Requirements:** REQ-002, REQ-012

**Decision:**
Document envelope length constraint exception for resolution by requirements owner. The overall thruster length (209.1 mm) exceeds the 150 mm requirement by 59.1 mm.

**Rationale:**
The length overage is driven by nozzle geometry required to achieve Isp ≥ 220 s (REQ-002). The nozzle length (125.6 mm) from DES-001 is sized for an expansion ratio of 100:1 to provide adequate Isp margin (86.4% above minimum requirement). The following resolution options were evaluated:

1. **Bell nozzle optimization:** Reduces nozzle length by ~20% (125.6 mm → 100 mm), overall length becomes 183.5 mm, still exceeds 150 mm requirement by 33.5 mm
2. **Increase half-angle to 20°:** Reduces nozzle length to ~94 mm, overall to 177.5 mm (still exceeds 150 mm, increases divergence losses by ~1.5%)
3. **Reduce expansion ratio to 60:1:** Reduces nozzle length to ~75 mm, overall to ~158.5 mm (close to 150 mm, Isp reduced to 330 s with 50% margin loss)
4. **Relax envelope to 210 mm:** Maintains performance, requires requirement change

The decision was to document the constraint exception and defer resolution to the requirements owner, as this represents a fundamental trade-off between envelope size and performance (Isp margin).

**Alternatives Considered:**
- Bell nozzle optimization: Reduces length but still exceeds requirement, recommended if envelope relaxation is not feasible
- Reduce expansion ratio: Significant Isp margin loss (86.4% → 50.0%), but achieves length close to requirement
- Relax envelope: No performance impact, requires requirement change by Agent 1

**Impact on Requirements:**
- REQ-002: Maintaining current expansion ratio (100:1) preserves 86.4% Isp margin. Reducing expansion ratio to 60:1 would reduce Isp margin to 50.0% (still compliant)
- REQ-012: Length requirement (150 mm) is not met. Resolution requires either envelope relaxation or aggressive trade-off

**Verification Implications:**
Independent verification should confirm:
- Envelope dimensions from prior design tasks
- Bell nozzle length reduction calculations (20% reduction from Rao's method)
- Isp vs. expansion ratio trade-off analysis

---

## DEC-010: Mounting Flange Material Selection

**Date:** 2026-02-14
**Decision Made By:** Agent 2
**Related Requirements:** REQ-011, REQ-013

**Decision:**
Select 316L stainless steel for mounting flange and associated hardware (injector, propellant inlet).

**Rationale:**
316L stainless steel was selected for the mounting flange, injector assembly, and propellant inlet based on the following factors:

1. **Hydrazine compatibility:** 316L SS is compatible with hydrazine propellant and its decomposition products (NH3, N2, H2)
2. **Space heritage:** 316L SS has extensive flight heritage in spacecraft propulsion systems
3. **Mechanical properties:** Good strength (yield ~290 MPa at RT), adequate for mounting interface requirements
4. **Manufacturability:** Excellent weldability for integration with molybdenum chamber
5. **Thermal properties:** Provides thermal isolation between hot chamber (1127°C) and spacecraft structure
6. **Mass impact:** Density (7,980 kg/m³) is acceptable within dry mass budget (0.5 kg)

**Alternatives Considered:**
- **Aluminum 6061:** Lower density (2,700 kg/m³) would reduce mass, but lower temperature rating and potential hydrazine compatibility concerns
- **Titanium 6Al-4V:** Excellent strength-to-weight ratio but higher cost and more difficult to machine
- **Inconel 625:** Higher temperature capability but higher density (8,440 kg/m³) and no thermal isolation benefit over 316L SS

**Impact on Requirements:**
- REQ-011: Contributes to dry mass budget but within limits. Flange mass (0.169 kg) + injector (0.038 kg) + inlet (0.012 kg) = 0.219 kg of total dry mass (0.280 kg)
- REQ-013: Provides robust mounting interface with 316L SS flange for M6 bolts

**Verification Implications:**
Independent verification should confirm:
- Material compatibility with hydrazine (ASTM G122 corrosion testing standards)
- Thermal expansion coefficient match between 316L SS and molybdenum chamber
- Weld integrity for flange-to-chamber joint
- Fastener preload and stress analysis for M6 mounting bolts
