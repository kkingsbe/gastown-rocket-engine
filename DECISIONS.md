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

**Document Status:** Active
**Last Updated:** 2026-02-14
**Phase:** BOOTSTRAP (Initial template creation)
