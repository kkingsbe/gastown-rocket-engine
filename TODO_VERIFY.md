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

- [x] **VER-001: Verify Thrust and Isp Performance**
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

- [x] **VER-002: Verify Propellant Mass Budget**
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
  - Status: **FAIL** - Conservative case (Isp=220s) exceeds 25 kg budget by 1.93%. Nominal case (Isp=410.08s) passes with 82.8% margin. Finding logged and Agent 1 notified.

- [x] **VER-003: Verify Catalyst Preheat Temperature**
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

- [x] **VER-004: Verify Chamber Structural Design**
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
  - Status: **PASS** - All requirements verified. Two significant discrepancies identified (>5%): Yield strength (+20.21%), Safety factor (+30.04%). Both discrepancies are positive (design is MORE conservative than Agent 2 reported) and do NOT impact requirements compliance. Discrepancies are due to different yield strength degradation modeling (Agent 2: fixed 40% factor, Agent 3: temperature-dependent interpolation). Disposition: ACCEPTED.

- [x] **VER-005: Verify Physical Envelope and Mechanical Interface Compliance**
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
  - Status: **PARTIAL PASS** - REQ-011 (mass), REQ-013 (mounting), REQ-026 (inlet) PASS. REQ-012 FAIL (length 209.1 mm > 150 mm requirement). Finding: 53.01% delta vs. design mass calculation (0.4284 kg vs. 0.280 kg claimed), but both values satisfy REQ-011.

- [x] **VER-006: Thermal Management Verification**
  - Traces to: REQ-006, REQ-010
  - Design Artifact: DES-008 (Thermal Analysis)
  - Verification Method: Simulation
  - Procedure:
    1. Develop an independent thermal simulation of startup transient
    2. Input thermal properties from DES-008
    3. Simulate temperature rise from ambient to 90% thrust condition
    4. Verify time to reach 90% thrust ≤ 200 ms (REQ-006)
    5. Verify propellant temperature maintained within 5°C-50°C range (REQ-010)
    6. Plot startup transient with requirement threshold annotated
  - Required Evidence: Verification report `verification/reports/VER-006_thermal_management_verification.md`, plots `verification/plots/VER-006_startup_transient.png` and `verification/plots/VER-006_propellant_temperature.png`, raw results `verification/data/VER-006_results.json`
  - Simulation Requirements:
    - Write an INDEPENDENT simulation — do NOT just re-run Agent 2's scripts
    - Generate plots saved to `verification/plots/`
    - Every plot must show requirement threshold as an annotated horizontal/vertical line
    - Run at boundary conditions, not just nominal
    - Output raw numerical results to `verification/data/`
    - Compare your results against Agent 2's claimed values — flag deltas > 5%
  - Status: **PASS** - Startup time 87 ms (56.5% margin vs. 200 ms requirement). Finding: 37.86% delta vs. design claimed startup time (87 ms vs. 140 ms). Both values satisfy requirement.

- [x] **VER-007: Thrust Control System Verification**
  - Traces to: REQ-003, REQ-004, REQ-009
  - Design Artifact: DES-006 (Thrust Control System)
  - Verification Method: Simulation
  - Procedure:
    1. Develop an independent thrust control simulation
    2. Input thrust control parameters from DES-006
    3. Simulate thrust vs. feed pressure relationship
    4. Verify thrust range 0.8-1.2 N achievable (REQ-003)
    5. Verify minimum impulse bit ≤ 0.01 N·s (REQ-004)
    6. Verify feed pressure range 0.15-0.30 MPa (REQ-009)
    7. Plot thrust vs. pressure with requirement range annotated
  - Required Evidence: Verification report `verification/reports/VER-007_thrust_control_verification.md`, plot `verification/plots/VER-007_thrust_vs_pressure.png`, raw results `verification/data/VER-007_results.json`
  - Simulation Requirements:
    - Write an INDEPENDENT simulation — do NOT just re-run Agent 2's scripts
    - Generate plots saved to `verification/plots/`
    - Every plot must show requirement threshold as an annotated horizontal/vertical line
    - Run at boundary conditions, not just nominal
    - Output raw numerical results to `verification/data/`
    - Compare your results against Agent 2's claimed values — flag deltas > 5%
  - Status: **PARTIAL PASS** - REQ-003 PARTIAL (0.8-1.0 N achievable, 1.2 N requires 0.36 MPa > 0.30 MPa limit). REQ-004 PASS (0.008 N·s at 10 ms on-time, 20% margin). REQ-009 PASS (feed pressure 0.15-0.30 MPa).

- [x] **VER-008: Safety and Reliability Verification**
  - Traces to: REQ-022, REQ-025, REQ-030
  - Design Artifact: DES-009 (Safety and Reliability)
  - Verification Method: Analysis
  - Procedure:
    1. Independently analyze safety factors and failure modes
    2. Verify leak-before-burst philosophy implemented (REQ-022)
    3. Verify all materials are space-qualified (REQ-025)
    4. Verify 15-year mission life requirements (REQ-030)
    5. Calculate cumulative firing time and verify ≥ 100 h
    6. Verify firing cycles ≥ 50,000
    7. Verify Isp degradation ≤ 5%
  - Required Evidence: Verification report `verification/reports/VER-008_safety_reliability_verification.md`, plot `verification/plots/VER-008_lifetime_analysis.png`, raw results `verification/data/VER-008_results.json`
  - Simulation Requirements: None (Analysis method, not Simulation)
  - Status: **FAIL (REQ-030 only)** - REQ-022 PASS (LBB with SF 22.2), REQ-025 PASS (all materials space-qualified), REQ-030 FAIL (cumulative time 13.89 h < 100 h requirement, -86% margin). Note: 50,000 cycles and 0.14% Isp degradation pass requirements.

- [x] **VER-009: Instrumentation Verification**
  - Traces to: REQ-028, REQ-029
  - Design Artifact: DES-010 (Instrumentation Design)
  - Verification Method: Analysis
  - Procedure:
    1. Independently analyze sensor specifications
    2. Verify pressure transducer with 0-2 MPa range (REQ-028)
    3. Verify two temperature sensors (catalyst bed, chamber wall) (REQ-029)
    4. Calculate thrust resolution from pressure accuracy
    5. Verify thrust resolution ≤ 0.05 N
  - Required Evidence: Verification report `verification/reports/VER-009_instrumentation_verification.md`, plots `verification/plots/VER-009_sensor_accuracy.png` and `verification/plots/VER-009_sensor_comparison.png`, raw results `verification/data/VER-009_results.json`
  - Simulation Requirements: None (Analysis method, not Simulation)
  - Status: **PASS** - REQ-028 PASS (0-2 MPa range, ±0.024 N thrust resolution, 52% margin), REQ-029 PASS (2 temperature sensors, Type K thermocouples).

- [x] **VER-010: Verify Propellant Feed System Material Compatibility**
  - Traces to: REQ-007
  - Design Artifact: DES-007 (⚠️ BLOCKED_BY: TODO_DESIGN.md > "DES-007")
  - Verification Method: Inspection
  - Procedure:
    1. Review `design/docs/propellant_feed_system.md` and material specifications
    2. Verify material specifications explicitly state hydrazine (N₂H₄) compatibility
    3. Verify design documentation includes material compatibility references
    4. Verify all wetted materials are rated for hydrazine service
    5. Check for compatibility documentation and certification references
    6. Document any materials lacking explicit hydrazine compatibility evidence
  - Required Evidence: Separate verification report `verification/reports/VER-010_propellant_material_verification.md` with material compatibility checklist
  - Simulation Requirements: None (Inspection method, not Simulation)
  - Status: **CONDITIONAL PASS** - 9 of 11 wetted materials verified compatible. Ti-6Al-4V (tank option) and Buna-N (regulator seals) are Class C (Not Recommended) per NASA-STD-6016. Two critical findings identified, path to full PASS documented in verification report.

- [x] **VER-011: Verify Thermal Cycle Survival**
  - Traces to: REQ-017
  - Design Artifact: DES-008 (Thermal Analysis)
  - Verification Method: Simulation
  - Procedure:
    1. Develop an independent thermal stress simulation for thermal cycle conditions
    2. Input thermal properties and geometry from DES-008
    3. Simulate thermal cycle from -40°C to +80°C (REQ-017)
    4. Calculate thermal stresses at boundary conditions
    5. Verify design withstands thermal cycle without structural failure
    6. Generate stress vs. temperature plots for hot and cold extremes
    7. Compare results against design outputs from Agent 2
    8. Verify thermal stress margins at both temperature extremes
  - Required Evidence: Verification report `verification/reports/VER-011_thermal_cycle.md`, plots `verification/plots/VER-011_temperature_vs_stress.png`, `verification/plots/VER-011_temperature_vs_stress_316L.png`, `verification/plots/VER-011_safety_factor_vs_temperature.png`, and `verification/plots/VER-011_agent_comparison.png`, raw results `verification/data/VER-011_results.json`
  - Simulation Requirements:
    - Write an INDEPENDENT simulation — do NOT just re-run Agent 2's scripts
    - Generate plots saved to `verification/plots/`
    - Every plot must show requirement threshold as an annotated horizontal/vertical line
    - Run at boundary conditions (-40°C and +80°C), not just nominal
    - Output raw numerical results to `verification/data/`
    - Compare your results against Agent 2's claimed values — flag deltas > 5%
  - Status: **PASS** - REQ-017 passes with minimum safety factor of 1.2213 (11.03% margin vs. 1.1 requirement). Finding: Significant discrepancies identified (>5%): full_cycle_stress (+8.65%), full_cycle_sf (-8.11%), mismatch_stress (+124.70%), mismatch_sf (-55.43%). The mismatch_sf discrepancy is due to different modeling approach for material interface stress (Agent 2: simple CTE difference calculation, Agent 3: stiffness-based calculation with geometric factor). Despite discrepancies, the minimum safety factor of 1.2213 still meets the 1.1 requirement threshold.

- [x] **VER-012: Verify Nozzle Thermal Stress for Cold Start**
  - Traces to: REQ-019
  - Design Artifact: DES-008 (Thermal Analysis)
  - Verification Method: Simulation
  - Procedure:
    1. Develop an independent transient thermal stress simulation for cold start
    2. Input thermal properties and nozzle geometry from DES-008
    3. Simulate 5-second cold start scenario with worst-case thermal gradient (REQ-019)
    4. Calculate transient thermal stresses in nozzle material
    5. Verify nozzle withstands thermal stress for full 5-second duration
    6. Calculate safety factor for thermal stress resistance
    7. Generate time-domain thermal stress plots
    8. Compare results against design outputs (Agent 2 reports marginal PASS with SF 1.13)
    9. Verify thermal stress remains below yield strength throughout transient
  - Required Evidence: Verification report `verification/reports/VER-012_cold_start_thermal_stress.md`, plots `verification/plots/VER-012_temperature_vs_time.png`, `verification/plots/VER-012_thermal_stress_vs_time.png`, `verification/plots/VER-012_stress_vs_yield_strength.png`, `verification/plots/VER-012_safety_factor_history.png`, `verification/plots/VER-012_independent_vs_design.png`, raw results `verification/data/VER-012_results.json`
  - Simulation Requirements:
    - Write an INDEPENDENT simulation — do NOT just re-run Agent 2's scripts
    - Generate plots saved to `verification/plots/`
    - Every plot must show requirement threshold as an annotated horizontal/vertical line
    - Run transient simulation for full 5-second cold start duration
    - Output raw numerical results to `verification/data/`
    - Compare your results against Agent 2's claimed values — flag deltas > 5%
    - **NOTE:** Verification is critical - Agent 2 reports marginal PASS with SF 1.13; independent verification required to confirm
  - Status: **PASS** - Independent simulation verified safety factor of 1.230 (11.79% margin above 1.1 requirement). Two significant discrepancies identified (>5%): safety_factor (+9.06%), thermal_stress (-13.77%). Both discrepancies are favorable to the design (independent simulation shows higher SF, lower stress). The marginal PASS claim by design is actually conservative - independent simulation demonstrates more robust margin. Root cause: different initial temperature (-40°C vs. 20°C) and different yield strength interpolation. Disposition: ACCEPTED.

---

## Notes

- Tasks are added to this queue by Agent 1 after requirements are finalized and design artifacts are created.
- Each task traces to exactly one requirement from `REQ_REGISTER.md`.
- The BLOCKED_BY mechanism prevents starting verification before the design artifact is complete.
- Verification results feed back into the traceability matrix in `TRACE_MATRIX.md`.
- All verification work must be INDEPENDENT from the design work performed by Agent 2.
