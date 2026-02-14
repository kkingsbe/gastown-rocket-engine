# Monopropellant Satellite Thruster — Requirements

## 1. Overview

A hydrazine monopropellant thruster for station-keeping and attitude control on a
small geostationary satellite (200 kg class). The thruster must provide reliable,
repeatable impulse for a 15-year mission life with minimal mass and volume impact
to the spacecraft bus.

## 2. Performance Requirements

- Steady-state thrust: 1.0 N nominal
- Minimum specific impulse (Isp): 220 seconds
- Thrust range: 0.8 N to 1.2 N (achievable via feed pressure regulation)
- Minimum impulse bit: ≤ 0.01 N·s (for fine attitude control)
- Total impulse: ≥ 50,000 N·s over mission life
- Startup time to 90% thrust: ≤ 200 ms

## 3. Propellant Requirements

- Propellant: Hydrazine (N2H4)
- Propellant mass budget: ≤ 25 kg (allocated from spacecraft mass budget)
- Propellant feed pressure range: 0.15 MPa to 0.30 MPa (blowdown system)
- Propellant temperature operating range: 5°C to 50°C

## 4. Physical Requirements

- Thruster dry mass: ≤ 0.5 kg (excluding valves and feed system)
- Thruster envelope: shall fit within a 100 mm diameter × 150 mm length cylinder
- Mounting interface: standard M6 bolt pattern, 4 places on 80 mm bolt circle

## 5. Thermal Requirements

- Catalyst bed preheat temperature: 150°C to 300°C (preheated before first firing)
- Chamber wall temperature shall not exceed 1400°C during steady-state operation
- Nozzle exit temperature shall not exceed 800°C during steady-state operation
- Thruster shall survive a thermal cycle range of -40°C to +80°C (non-operating)

## 6. Structural Requirements

- Chamber shall withstand maximum expected operating pressure (MEOP) × 1.5 safety factor
- Nozzle shall withstand thermal stress from startup transient (cold start from 20°C
  to steady-state in < 5 seconds)

## 7. Lifetime Requirements

- Minimum 50,000 firing cycles without degradation > 5% in Isp
- Catalyst bed shall maintain activity for ≥ 100 hours cumulative firing time
- No single-point failure modes (leak-before-burst design philosophy)

## 8. Material Constraints

- Chamber material: must be compatible with hydrazine decomposition products
  (NH3, N2, H2) at operating temperature
- Nozzle material: refractory metal or high-temperature alloy suitable for
  1400°C+ operation
- All materials must be space-qualified or have heritage flight data

## 9. Interface Requirements

- Propellant inlet: 1/4" AN flare fitting, compatible with spacecraft propellant
  distribution system
- Electrical interface: heater circuit (28V nominal, ≤ 15W) for catalyst bed preheat
- Instrumentation: provision for chamber pressure transducer (0–2 MPa range)
  and two temperature sensors (catalyst bed, chamber wall)

## 10. Nice-to-Haves (non-binding)

- Mass below 0.35 kg would provide positive margin for other subsystems
- Isp above 230 s would extend mission life or reduce propellant load
- Heritage design similarity to Aerojet MR-103 or similar qualified thruster class