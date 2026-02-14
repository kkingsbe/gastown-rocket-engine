# TODO_VERIFY.md — Work Queue for Agent 3 (Verification & Validation)

**Purpose:** This file contains verification and validation tasks assigned to Agent 3. Each task traces to a requirement from `REQ_REGISTER.md` and verifies that the design artifact (from `TODO_DESIGN.md`) meets the requirement.

## Instructions for Agent 3

1. **Work Assignment:** Process tasks in this queue in order, unless a task is marked as BLOCKED.
2. **Blocked Tasks:** Tasks marked with `⚠️ BLOCKED_BY` cannot proceed until the referenced design artifact is completed in `TODO_DESIGN.md`.
3. **Independent Verification:** Verification MUST be independent from design work. Do NOT simply re-run Agent 2's scripts. Create your own verification procedures and simulations.
4. **Task Completion:** After completing each task:
   - Mark it as `[x]` completed
   - Generate the required evidence artifacts
   - Update `TRACE_MATRIX.md` with verification status
   - Report any findings or issues in the evidence documentation
5. **Blocking Issues:** If you discover the design does NOT meet the requirement:
   - Document the failure clearly
   - Provide quantitative evidence
   - Create a follow-up task in `TODO_DESIGN.md` if design changes are needed
6. **Evidence Storage:** Save all verification evidence in the `verification/` directory:
   - `verification/reports/` — Verification reports and analyses
   - `verification/plots/` — Plots and visualizations
   - `verification/data/` — Raw numerical results

---

## Task Format Specification

Each verification task follows this format:

```markdown
- [ ] **VER-XXX: [Title]**
  - Traces to: REQ-XXX
  - Design Artifact: DES-XXX (⚠️ BLOCKED_BY: TODO_DESIGN.md > "DES-XXX" if not yet complete)
  - Verification Method: Inspection | Analysis | Simulation | Demonstration
  - Procedure:
    1. [Step-by-step how to verify]
    2. [What to measure / compute / observe]
    3. [Pass/fail criteria with exact thresholds]
  - Required Evidence: [What artifact proves it - verification report, simulation output, plots]
  - Simulation Requirements (if method is Simulation):
    - Write an INDEPENDENT simulation — do NOT just re-run Agent 2's scripts
    - Generate plots saved to `verification/plots/`
    - Every plot must show requirement threshold as an annotated horizontal/vertical line
    - Run at boundary conditions, not just nominal
    - Output raw numerical results to `verification/data/`
    - Compare your results against Agent 2's claimed values — flag deltas > 5%
```

## Verification Methods Explained

- **Inspection:** Visual or manual examination of documents, code, or physical artifacts. Use when the requirement can be verified by review alone.
- **Analysis:** Mathematical or logical evaluation of the design. Use when you can compute or derive the answer analytically.
- **Simulation:** Running computational models to evaluate behavior under specified conditions. Use for dynamic or complex behaviors that require numerical evaluation.
- **Demonstration:** Operating or exercising the system to observe its behavior. Use when you need to see the system in action.

---

## Verification Tasks

- [ ] **VER-001: Verify Thrust and Isp Performance**
  - Traces to: REQ-001, REQ-002
  - Design Artifact: DES-001 (⚠️ BLOCKED_BY: TODO_DESIGN.md > "DES-001")
  - Verification Method: Simulation
  - Procedure:
    1. Develop an independent thrust performance simulation using rocket propulsion equations (F = ṁVe + (Pe-Pa)Ae)
    2. Input the chamber pressure, mass flow rate, and nozzle geometry from DES-001 outputs
    3. Calculate thrust across feed pressure range 0.15-0.30 MPa (REQ-009)
    4. Calculate specific impulse using Isp = Ve/g0 in vacuum conditions
    5. Verify thrust is 1.0 N ± 0.05 N at nominal feed pressure (REQ-001)
    6. Verify Isp ≥ 220 s in vacuum (REQ-002)
    7. Plot thrust vs. feed pressure and annotate the 0.95-1.05 N acceptance band
    8. Run at boundary conditions (0.15 MPa and 0.30 MPa) in addition to nominal
  - Required Evidence: Verification report `verification/reports/VER-001_thrust_Isp_verification.md`, plots `verification/plots/VER-001_thrust_vs_pressure.png` and `verification/plots/VER-001_Isp_compliance.png`, raw results `verification/data/VER-001_results.json`
  - Simulation Requirements:
    - Write an INDEPENDENT simulation — do NOT just re-run Agent 2's scripts
    - Generate plots saved to `verification/plots/`
    - Every plot must show requirement threshold as an annotated horizontal/vertical line
    - Run at boundary conditions, not just nominal
    - Output raw numerical results to `verification/data/`
    - Compare your results against Agent 2's claimed values — flag deltas > 5%

- [ ] **VER-002: Verify Propellant Mass Budget**
  - Traces to: REQ-005, REQ-008
  - Design Artifact: DES-002 (⚠️ BLOCKED_BY: TODO_DESIGN.md > "DES-002")
  - Verification Method: Analysis
  - Procedure:
    1. Independently calculate total impulse required: Σ(Impulse bits for 50,000 cycles)
    2. Calculate required propellant mass using m = Total_Impulse / (Isp × g0)
    3. Use conservative Isp = 220 s (minimum from REQ-002)
    4. Add 10% margin for mission uncertainty
    5. Verify calculated propellant mass delivers ≥ 50,000 N·s total impulse (REQ-005)
    6. Verify propellant mass ≤ 25 kg budget (REQ-008)
    7. Document all assumptions: average impulse bit, firing cycle count, Isp degradation allowance
  - Required Evidence: Verification report `verification/reports/VER-002_propellant_budget_verification.md` with calculations and final mass budget breakdown
  - Simulation Requirements: None (Analysis method, not Simulation)

- [ ] **VER-003: Verify Catalyst Preheat Temperature**
  - Traces to: REQ-014, REQ-027
  - Design Artifact: DES-003 (⚠️ BLOCKED_BY: TODO_DESIGN.md > "DES-003")
  - Verification Method: Simulation
  - Procedure:
    1. Develop an independent thermal simulation of catalyst bed heating
    2. Input heater power, thermal mass, and thermal resistance from DES-003
    3. Simulate temperature rise from ambient (20°C) to preheat temperature
    4. Verify heater power ≤ 15W at 28V (REQ-027)
    5. Verify final temperature is within 150°C - 300°C range (REQ-014)
    6. Calculate preheat time to reach minimum 150°C
    7. Plot temperature vs. time and annotate the 150°C and 300°C acceptance limits
    8. Run simulation at cold start (20°C) and worst-case thermal conditions
  - Required Evidence: Verification report `verification/reports/VER-003_catalyst_preheat_verification.md`, plot `verification/plots/VER-003_temperature_profile.png`, raw results `verification/data/VER-003_results.json`
  - Simulation Requirements:
    - Write an INDEPENDENT simulation — do NOT just re-run Agent 2's scripts
    - Generate plots saved to `verification/plots/`
    - Every plot must show requirement threshold as an annotated horizontal/vertical line
    - Run at boundary conditions, not just nominal
    - Output raw numerical results to `verification/data/`
    - Compare your results against Agent 2's claimed values — flag deltas > 5%

- [ ] **VER-004: Verify Chamber Structural Design**
  - Traces to: REQ-015, REQ-018, REQ-024
  - Design Artifact: DES-004 (⚠️ BLOCKED_BY: TODO_DESIGN.md > "DES-004")
  - Verification Method: Simulation
  - Procedure:
    1. Develop an independent structural stress analysis using thin-wall pressure vessel equations
    2. Input chamber geometry, wall thickness, and material properties from DES-004
    3. Calculate hoop stress at MEOP (Maximum Expected Operating Pressure)
    4. Verify design withstands MEOP × 1.5 safety factor (REQ-018)
    5. Verify chamber wall temperature ≤ 1400°C during steady-state operation (REQ-015)
    6. Verify selected material is a refractory metal or high-temperature alloy rated ≥ 1400°C (REQ-024)
    7. Verify material is compatible with hydrazine decomposition products (REQ-023)
    8. Plot stress vs. pressure and annotate the safety factor threshold
  - Required Evidence: Verification report `verification/reports/VER-004_chamber_structural_verification.md`, plot `verification/plots/VER-004_stress_vs_pressure.png`, raw results `verification/data/VER-004_results.json`
  - Simulation Requirements:
    - Write an INDEPENDENT simulation — do NOT just re-run Agent 2's scripts
    - Generate plots saved to `verification/plots/`
    - Every plot must show requirement threshold as an annotated horizontal/vertical line
    - Run at boundary conditions (MEOP × 1.5), not just nominal
    - Output raw numerical results to `verification/data/`
    - Compare your results against Agent 2's claimed values — flag deltas > 5%

- [ ] **VER-005: Verify Physical Envelope and Mechanical Interface Compliance**
  - Traces to: REQ-011, REQ-012, REQ-013, REQ-026
  - Design Artifact: DES-005 (⚠️ BLOCKED_BY: TODO_DESIGN.md > "DES-005")
  - Verification Method: Inspection
  - Procedure:
    1. Review `design/docs/physical_envelope_interface.md` and mechanical drawings
    2. Verify overall thruster dimensions fit within 100 mm diameter × 150 mm length cylinder (REQ-012)
    3. Verify calculated dry mass ≤ 0.5 kg (REQ-011)
    4. Verify mounting interface matches specification: M6 bolts, 4-hole pattern, 80 mm bolt circle diameter (REQ-013)
    5. Verify propellant inlet is 1/4" AN flare fitting (REQ-026)
    6. Document any deviations or non-compliance issues
    7. Create dimensional verification checklist
  - Required Evidence: Verification report `verification/reports/VER-005_envelope_interface_verification.md` with compliance checklist and dimensional analysis
  - Simulation Requirements: None (Inspection method, not Simulation)

---

## Notes

- Tasks are added to this queue by Agent 1 after requirements are finalized and design artifacts are created.
- Each task traces to exactly one requirement from `REQ_REGISTER.md`.
- The BLOCKED_BY mechanism prevents starting verification before the design artifact is complete.
- Verification results feed back into the traceability matrix in `TRACE_MATRIX.md`.
- All verification work must be INDEPENDENT from the design work performed by Agent 2.
