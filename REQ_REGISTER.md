# REQ_REGISTER.md — Requirements Register

## Purpose

This document is the source of truth for all requirements for the Monopropellant Satellite Thruster project. It contains atomic, verifiable requirements decomposed from the user requirements in REQUIREMENTS.md. Each requirement can be independently verified and traces back to a user-level requirement.

All requirements are maintained in this register and referenced by their REQ-XXX identifier throughout the project lifecycle.

---

## Requirements

### Performance Requirements

REQ-001: The thruster shall produce a steady-state thrust of 1.0 N ± 0.05 N during nominal operation.
  Parent: REQUIREMENTS.md Section 2 (Performance Requirements)
  Rationale: Defines the nominal thrust capability required for station-keeping and attitude control maneuvers.
  Verification Method: Simulation (thrust performance analysis using chamber pressure, mass flow rate, and nozzle geometry)
  Priority: Must
  Status: OPEN

REQ-002: The thruster shall produce a minimum specific impulse (Isp) of 220 seconds in vacuum.
  Parent: REQUIREMENTS.md Section 2 (Performance Requirements)
  Rationale: Ensures efficient propellant usage to meet mission duration requirements within mass budget.
  Verification Method: Simulation (specific impulse calculation using chamber conditions and nozzle expansion ratio)
  Priority: Must
  Status: OPEN

REQ-003: The thruster shall be capable of producing thrust in the range of 0.8 N to 1.2 N via feed pressure regulation.
  Parent: REQUIREMENTS.md Section 2 (Performance Requirements)
  Rationale: Provides flexibility for different maneuver requirements and allows thrust throttling within the blowdown system.
  Verification Method: Simulation (thrust vs. feed pressure analysis across 0.15-0.30 MPa range)
  Priority: Must
  Status: OPEN

REQ-004: The thruster shall deliver a minimum impulse bit of 0.01 N·s or less for fine attitude control maneuvers.
  Parent: REQUIREMENTS.md Section 2 (Performance Requirements)
  Rationale: Enables precise attitude control for spacecraft pointing requirements.
  Verification Method: Simulation (minimum achievable impulse calculation based on minimum on-time and thrust level)
  Priority: Must
  Status: OPEN

REQ-005: The thruster shall provide a total impulse of at least 50,000 N·s over the 15-year mission life.
  Parent: REQUIREMENTS.md Section 2 (Performance Requirements)
  Rationale: Ensures sufficient impulse capability for all station-keeping and attitude control activities throughout the mission.
  Verification Method: Analysis (propellant mass × Isp × g0 = total impulse; verify with 25 kg budget and minimum Isp)
  Priority: Must
  Status: OPEN

REQ-006: The thruster shall reach 90% of nominal steady-state thrust within 200 ms of startup command.
  Parent: REQUIREMENTS.md Section 2 (Performance Requirements)
  Rationale: Ensures responsive thrust delivery for time-critical attitude control maneuvers.
  Verification Method: Simulation (transient thermal and flow analysis during startup from cold conditions)
  Priority: Must
  Status: OPEN

### Propellant Requirements

REQ-007: The thruster shall use hydrazine (N2H4) as the propellant.
  Parent: REQUIREMENTS.md Section 3 (Propellant Requirements)
  Rationale: Specifies the propellant chemistry for the catalytic decomposition system.
  Verification Method: Inspection (material specification and compatibility documentation)
  Priority: Must
  Status: OPEN

REQ-008: The thruster system shall operate within a propellant mass budget of 25 kg or less.
  Parent: REQUIREMENTS.md Section 3 (Propellant Requirements)
  Rationale: Ensures the propellant load fits within the spacecraft mass allocation.
  Verification Method: Analysis (propellant mass calculation from total impulse and Isp requirements)
  Priority: Must
  Status: OPEN

REQ-009: The thruster shall operate with a propellant feed pressure range of 0.15 MPa to 0.30 MPa.
  Parent: REQUIREMENTS.md Section 3 (Propellant Requirements)
  Rationale: Defines the blowdown system operating envelope for the feed system.
  Verification Method: Demonstration (functional testing across specified pressure range)
  Priority: Must
  Status: OPEN

REQ-010: The propellant temperature shall be maintained between 5°C and 50°C during thruster operation.
  Parent: REQUIREMENTS.md Section 3 (Propellant Requirements)
  Rationale: Ensures propellant remains in liquid state and maintains consistent flow properties.
  Verification Method: Simulation (thermal analysis of propellant tank and feed lines)
  Priority: Must
  Status: OPEN

### Physical Requirements

REQ-011: The thruster dry mass shall not exceed 0.5 kg.
  Parent: REQUIREMENTS.md Section 4 (Physical Requirements)
  Rationale: Ensures the thruster system stays within spacecraft mass budget (excluding valves and feed system).
  Verification Method: Inspection (mass calculation from design dimensions and material densities)
  Priority: Must
  Status: OPEN

REQ-012: The thruster envelope shall fit within a cylinder of 100 mm diameter and 150 mm length.
  Parent: REQUIREMENTS.md Section 4 (Physical Requirements)
  Rationale: Ensures the thruster can be accommodated within the spacecraft volume constraints.
  Verification Method: Inspection (dimensional verification against design drawings)
  Priority: Must
  Status: OPEN

REQ-013: The thruster shall have a mounting interface with M6 bolts arranged in a 4-hole pattern on an 80 mm bolt circle diameter.
  Parent: REQUIREMENTS.md Section 4 (Physical Requirements)
  Rationale: Provides standard mechanical interface for spacecraft integration.
  Verification Method: Inspection (dimensional verification of mounting pattern)
  Priority: Must
  Status: OPEN

### Thermal Requirements

REQ-014: The catalyst bed shall be preheated to a temperature between 150°C and 300°C before the first firing.
  Parent: REQUIREMENTS.md Section 5 (Thermal Requirements)
  Rationale: Ensures catalyst activation for efficient hydrazine decomposition and reliable startup.
  Verification Method: Demonstration (preheat system functional test with temperature monitoring)
  Priority: Must
  Status: OPEN

REQ-015: The chamber wall temperature shall not exceed 1400°C during steady-state operation.
  Parent: REQUIREMENTS.md Section 5 (Thermal Requirements)
  Rationale: Limits material thermal stress and ensures structural integrity during operation.
  Verification Method: Simulation (steady-state thermal analysis of chamber heat flux and radiation cooling)
  Priority: Must
  Status: OPEN

REQ-016: The nozzle exit temperature shall not exceed 800°C during steady-state operation.
  Parent: REQUIREMENTS.md Section 5 (Thermal Requirements)
  Rationale: Controls thermal radiation and protects downstream spacecraft components.
  Verification Method: Simulation (nozzle exit temperature calculation from isentropic expansion)
  Priority: Must
  Status: OPEN

REQ-017: The thruster shall survive a thermal cycle range of -40°C to +80°C when not operating.
  Parent: REQUIREMENTS.md Section 5 (Thermal Requirements)
  Rationale: Ensures structural integrity through expected spacecraft thermal environment extremes.
  Verification Method: Simulation (thermal stress analysis over specified temperature cycle)
  Priority: Must
  Status: OPEN

### Structural Requirements

REQ-018: The chamber shall withstand the Maximum Expected Operating Pressure (MEOP) multiplied by a safety factor of 1.5.
  Parent: REQUIREMENTS.md Section 6 (Structural Requirements)
  Rationale: Ensures structural integrity with adequate margin above expected pressure conditions.
  Verification Method: Simulation (stress analysis using thin-wall pressure vessel equations)
  Priority: Must
  Status: OPEN

REQ-019: The nozzle shall withstand thermal stress from a cold start (20°C to steady-state temperature) within 5 seconds.
  Parent: REQUIREMENTS.md Section 6 (Structural Requirements)
  Rationale: Ensures nozzle survives rapid temperature transients during startup without failure.
  Verification Method: Simulation (transient thermal stress analysis during startup)
  Priority: Must
  Status: OPEN

### Lifetime Requirements

REQ-020: The thruster shall complete a minimum of 50,000 firing cycles with no more than 5% degradation in specific impulse.
  Parent: REQUIREMENTS.md Section 7 (Lifetime Requirements)
  Rationale: Ensures performance reliability over 15-year mission life with repeated firings.
  Verification Method: Simulation (catalyst degradation modeling and life prediction analysis)
  Priority: Must
  Status: OPEN

REQ-021: The catalyst bed shall maintain activity for a cumulative firing time of at least 100 hours.
  Parent: REQUIREMENTS.md Section 7 (Lifetime Requirements)
  Rationale: Ensures catalyst longevity for extended mission operations.
  Verification Method: Simulation (catalyst life modeling based on temperature and thermal cycling)
  Priority: Must
  Status: OPEN

REQ-022: The thruster design shall employ leak-before-burst failure philosophy to eliminate single-point failure modes.
  Parent: REQUIREMENTS.md Section 7 (Lifetime Requirements)
  Rationale: Enhances safety by ensuring detectable leaks occur before catastrophic failure.
  Verification Method: Inspection (design review for leak-before-burst features and failure mode analysis)
  Priority: Must
  Status: OPEN

### Material Constraints

REQ-023: The chamber material shall be compatible with hydrazine decomposition products (NH3, N2, H2) at operating temperatures.
  Parent: REQUIREMENTS.md Section 8 (Material Constraints)
  Rationale: Prevents material degradation or chemical reactions with decomposition products.
  Verification Method: Inspection (material compatibility review against product gas chemistry)
  Priority: Must
  Status: OPEN

REQ-024: The nozzle material shall be a refractory metal or high-temperature alloy suitable for operation at 1400°C or higher.
  Parent: REQUIREMENTS.md Section 8 (Material Constraints)
  Rationale: Ensures nozzle maintains structural integrity at high operating temperatures.
  Verification Method: Inspection (material specification review against temperature capability)
  Priority: Must
  Status: OPEN

REQ-025: All materials used in the thruster shall be space-qualified or have heritage flight data.
  Parent: REQUIREMENTS.md Section 8 (Material Constraints)
  Rationale: Ensures reliability in the space environment with proven flight heritage.
  Verification Method: Inspection (material heritage documentation review)
  Priority: Must
  Status: OPEN

### Interface Requirements

REQ-026: The thruster shall have a propellant inlet with 1/4" AN flare fitting compatible with the spacecraft propellant distribution system.
  Parent: REQUIREMENTS.md Section 9 (Interface Requirements)
  Rationale: Provides standardized fluid interface for propellant feed system integration.
  Verification Method: Inspection (fitting specification verification)
  Priority: Must
  Status: OPEN

REQ-027: The thruster shall provide an electrical interface for a heater circuit operating at 28V nominal with power consumption not exceeding 15W for catalyst bed preheat.
  Parent: REQUIREMENTS.md Section 9 (Interface Requirements)
  Rationale: Defines electrical interface requirements for catalyst bed preheating system.
  Verification Method: Analysis (electrical power calculation: 28V × current ≤ 15W)
  Priority: Must
  Status: OPEN

REQ-028: The thruster shall provide provisions for a chamber pressure transducer with a measurement range of 0 to 2 MPa.
  Parent: REQUIREMENTS.md Section 9 (Interface Requirements)
  Rationale: Enables chamber pressure monitoring for performance verification and health assessment.
  Verification Method: Inspection (pressure transducer mounting interface verification)
  Priority: Must
  Status: OPEN

REQ-029: The thruster shall provide provisions for two temperature sensors: one for the catalyst bed and one for the chamber wall.
  Parent: REQUIREMENTS.md Section 9 (Interface Requirements)
  Rationale: Enables thermal monitoring for performance verification and health assessment.
  Verification Method: Inspection (temperature sensor mounting interface verification)
  Priority: Must
  Status: OPEN

### Mission Requirements (Derived from Overview)

REQ-030: The thruster system shall be designed to support a 15-year mission life.
  Parent: REQUIREMENTS.md Section 1 (Overview)
  Rationale: Defines the operational lifetime requirement for the thruster system.
  Verification Method: Analysis (lifetime assessment based on 50,000 firing cycles and 100-hour cumulative firing time)
  Priority: Must
  Status: OPEN

---

## Summary

- Total Requirements: 30
- Requirements by Category:
  - Performance: 6 (REQ-001 to REQ-006)
  - Propellant: 4 (REQ-007 to REQ-010)
  - Physical: 3 (REQ-011 to REQ-013)
  - Thermal: 4 (REQ-014 to REQ-017)
  - Structural: 2 (REQ-018 to REQ-019)
  - Lifetime: 3 (REQ-020 to REQ-022)
  - Material Constraints: 3 (REQ-023 to REQ-025)
  - Interface: 4 (REQ-026 to REQ-029)
  - Mission: 1 (REQ-030)
- Priority Distribution:
  - Must: 30
  - Should: 0
  - Could: 0
- All requirements are currently OPEN

---

## Traceability Notes

This requirements register provides complete traceability from user requirements (REQUIREMENTS.md) to atomic system requirements. Each requirement can be independently verified through one or more of the following methods:

- **Inspection**: Non-destructive verification through review of documentation, drawings, or specifications
- **Analysis**: Quantitative verification using calculations or equations
- **Simulation**: Computational verification through physics-based modeling
- **Demonstration**: Functional verification through testing or operation

The register will be updated throughout the project lifecycle to track requirement status, verification results, and any changes or additions.
