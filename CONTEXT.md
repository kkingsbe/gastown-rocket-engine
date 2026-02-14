# CONTEXT.md — Domain Reference: Hydrazine Monopropellant Thruster

This document provides the physics, equations, material properties, and reference
data that all agents should use when working on this project. Using a shared
reference ensures Agent 2 and Agent 3 start from the same physics, making
independent verification meaningful.

---

## 1. Hydrazine Decomposition Chemistry

Hydrazine (N2H4) decomposes catalytically over Shell 405 (or S-405) iridium catalyst:

**Primary reaction (exothermic):**
```
3 N2H4 → 4 NH3 + N2          ΔH = -336 kJ/mol
```

**Secondary reaction (endothermic, partial NH3 dissociation):**
```
NH3 → 1/2 N2 + 3/2 H2        ΔH = +46 kJ/mol
```

The **degree of ammonia dissociation** (alpha) controls performance:
- alpha = 0: No NH3 dissociation → lower temperature, lower Isp
- alpha = 0.4–0.6: Typical operating range for flight thrusters
- alpha = 1.0: Complete dissociation → highest temperature, highest Isp

### Decomposition Products (as a function of alpha)

For 1 mole of N2H4 decomposed, the product gas composition is:

| Species | Moles per mol N2H4 |
|---|---|
| NH3 | (4/3)(1 - alpha) |
| N2 | (1/3) + (2/3)*alpha |
| H2 | 2*alpha |
| **Total** | **(4/3) + (2/3)*alpha** |

### Product Gas Properties (function of alpha)

**Mean molecular weight:**
```
M_bar = [17.03 * (4/3)(1-alpha) + 28.01 * ((1/3)+(2/3)*alpha) + 2.016 * 2*alpha] / [(4/3) + (2/3)*alpha]
```

**Adiabatic decomposition temperature** (approximate, for design use):
```
T_c ~ 900 + 600*alpha    [K]    (valid for alpha = 0 to 0.7)
```
More precisely: T_c ranges from ~900 K (alpha=0) to ~1900 K (alpha=1).

**Ratio of specific heats** (approximate):
```
gamma ~ 1.27 - 0.05*alpha    (for alpha = 0.3 to 0.7, at chamber conditions)
```

For more precise work, compute gamma from the mixture Cp and Cv at temperature.

---

## 2. Rocket Propulsion Equations

### Ideal Rocket Equation (Thrust)

```
F = mdot * Ve + (Pe - Pa) * Ae
```

Where:
- F = thrust [N]
- mdot = mass flow rate [kg/s]
- Ve = exhaust velocity [m/s]
- Pe = nozzle exit pressure [Pa]
- Pa = ambient pressure [Pa] (0 in vacuum)
- Ae = nozzle exit area [m^2]

In vacuum (Pa = 0):
```
F = mdot * Ve + Pe * Ae
```

### Specific Impulse

```
Isp = F / (mdot * g0)    [seconds]
```

Where g0 = 9.80665 m/s^2 (standard gravity, exact).

**Characteristic velocity (c-star):**
```
c_star = Pc * At / mdot
```

Where:
- Pc = chamber pressure [Pa]
- At = throat area [m^2]

**Ideal c-star:**
```
c_star = sqrt(gamma * R_specific * Tc) / (gamma * sqrt((2/(gamma+1))^((gamma+1)/(gamma-1))))
```

Where R_specific = R_universal / M_bar [J/(kg*K)]

### Isentropic Nozzle Flow

**Area ratio (exit-to-throat):**
```
Ae/At = (1/Me) * [(2/(gamma+1)) * (1 + (gamma-1)/2 * Me^2)]^((gamma+1)/(2*(gamma-1)))
```

Where Me = Mach number at nozzle exit. This is implicit in Me and must be
solved numerically (use scipy.optimize.brentq or fsolve).

**Exit temperature:**
```
Te = Tc / (1 + (gamma-1)/2 * Me^2)
```

**Exit pressure:**
```
Pe = Pc * (1 + (gamma-1)/2 * Me^2)^(-gamma/(gamma-1))
```

**Exit velocity:**
```
Ve = Me * sqrt(gamma * R_specific * Te)
```

**Mass flow rate through choked throat:**
```
mdot = (Pc * At) / c_star
```

Or equivalently:
```
mdot = Pc * At * sqrt(gamma / (R_specific * Tc)) * (2/(gamma+1))^((gamma+1)/(2*(gamma-1)))
```

### Thrust Coefficient

```
CF = sqrt(2*gamma^2/(gamma-1) * (2/(gamma+1))^((gamma+1)/(gamma-1)) * (1 - (Pe/Pc)^((gamma-1)/gamma))) + (Pe/Pc) * (Ae/At)
```

Thrust can also be expressed as:
```
F = CF * Pc * At
```

---

## 3. Nozzle Geometry

### Conical Nozzle (simple, use for initial design)

- **Convergent half-angle:** 30-45 degrees typical
- **Divergent half-angle (alpha_nozzle):** 15-20 degrees typical
- **Divergence loss factor:** lambda = (1 + cos(alpha_nozzle)) / 2

For a 15 degree half-angle cone: lambda = 0.9830 (1.7% loss vs ideal).

### Bell Nozzle (higher performance, optional refinement)

Typically 80% of equivalent 15 degree cone length. Use Rao's method for contour
optimization. For this project, conical nozzle is acceptable for initial design.

### Key Dimensions

```
Throat diameter:     Dt = 2 * sqrt(At / pi)
Exit diameter:       De = 2 * sqrt(Ae / pi)
Chamber diameter:    Dc ~ 2-4 * Dt (typical contraction ratio)
Nozzle length:       L_nozzle = (De/2 - Dt/2) / tan(alpha_nozzle)
Chamber length:      L_chamber ~ L_star * At / Ac
```

Where L_star (characteristic length) is approximately 0.5-1.0 m for hydrazine
thrusters (this is the ratio of chamber volume to throat area, not a physical length).

---

## 4. Material Properties

### Chamber Materials (Hydrazine Compatible)

| Material | Max Temp (C) | Density (kg/m^3) | Yield Strength at RT (MPa) | Notes |
|---|---|---|---|---|
| Inconel 625 | 980 | 8440 | 460 | Excellent hydrazine compatibility |
| Inconel 718 | 700 | 8190 | 1035 | Limited above 700C |
| Haynes 230 | 1150 | 8970 | 390 | Excellent high-temp |
| Molybdenum (Mo) | 1650 | 10220 | 560 | Needs coating in oxidizing env |
| Rhenium (Re) | 2000 | 21020 | 290 | Excellent, expensive |
| Columbium C103 (Nb alloy) | 1370 | 8850 | 240 | Heritage material for small thrusters |

### Nozzle Materials

For nozzles seeing >1000C, refractory metals or high-temp alloys are required.
Rhenium/iridium is flight-proven for small thrusters. Columbium C103 with silicide
coating is a lower-cost alternative.

### Catalyst

- **Shell 405 (S-405):** Iridium on alumina support, granule size 14-25 mesh
- **Catalyst bed loading:** 30-60 kg/(s*m^2) typical specific loading
- **Bed length/diameter ratio:** 1.5-3.0 typical

---

## 5. Reference Data: Similar Flight Thrusters

| Parameter | Aerojet MR-103 | Airbus CHT-1 | This Design Target |
|---|---|---|---|
| Thrust | 1.0 N | 1.0 N | 1.0 N |
| Isp (vacuum) | 224 s | 220 s | >= 220 s |
| Feed pressure | 0.55-2.4 MPa | 0.5-2.2 MPa | 0.15-0.30 MPa |
| Mass | 0.33 kg | 0.30 kg | <= 0.50 kg |
| Propellant | N2H4 | N2H4 | N2H4 |
| Chamber pressure | ~0.69 MPa | ~0.55 MPa | TBD by design |
| Valve power | 12 W | 10 W | <= 15 W |

**Note:** This design has significantly lower feed pressure than heritage thrusters
(0.15-0.30 MPa vs 0.5-2.4 MPa). This is a blowdown system constraint and will
drive the chamber pressure and throat area sizing. The lower feed pressure means
larger throat area to maintain thrust, which affects Isp and nozzle geometry.

---

## 6. Key Physical Constants

```python
g0 = 9.80665           # m/s^2  — standard gravitational acceleration (exact, SI)
R_universal = 8314.46  # J/(kmol*K) — universal gas constant (NIST)
pi = 3.14159265359     # use numpy: np.pi

# Molecular weights [g/mol]
M_N2H4 = 32.045       # Hydrazine
M_NH3 = 17.031        # Ammonia
M_N2 = 28.014         # Nitrogen
M_H2 = 2.016          # Hydrogen

# Hydrazine liquid properties (at 25C)
rho_N2H4 = 1004.0     # kg/m^3 — liquid density
T_freeze_N2H4 = 1.4   # C — freezing point (CRITICAL for thermal design)
T_boil_N2H4 = 113.5   # C — boiling point at 1 atm
```

---

## 7. Design Heuristics and Rules of Thumb

These are NOT requirements — they are starting points for design. Agent 2 may
deviate with justification.

- **Chamber pressure:** For low-feed-pressure blowdown systems, Pc is typically
  60-80% of feed pressure (accounting for injector/catalyst bed pressure drop).
  At minimum feed pressure of 0.15 MPa, expect Pc ~ 0.09-0.12 MPa.
- **Expansion ratio (Ae/At):** For vacuum nozzles, 50:1 to 300:1 is typical.
  Higher ratios give better Isp but increase nozzle length and mass.
  Practical limit is often driven by envelope constraint.
- **Nozzle half-angle:** 15 degrees is standard for conical nozzles. Going below
  12 degrees gives diminishing returns; above 20 degrees increases divergence losses.
- **Chamber L-star:** 0.5-1.0 m for hydrazine. Higher L-star gives more complete
  decomposition (higher alpha) but increases chamber volume and mass.
- **Pressure drop:** Budget ~20-40% of feed pressure for catalyst bed + injector drop.
- **Typical alpha for flight thrusters:** 0.4-0.6 at steady state. Varies with
  catalyst bed temperature, loading, and age.

---

## 8. Thermal Considerations

### Steady-State Heat Transfer

For a radiation-cooled thruster (typical for this thrust class):

**Chamber wall heat flux** (approximate):
```
q = h_g * (T_gas - T_wall)
```

Where h_g (gas-side heat transfer coefficient) can be estimated using the
Bartz correlation:
```
h_g = (0.026 / Dt^0.2) * (mu^0.2 * Cp / Pr^0.6) * (Pc * g0 / c_star)^0.8 * (Dt/R_curve)^0.1 * (At/A)^0.9 * sigma
```

For initial design, a simplified radiation equilibrium approach is often sufficient:

**Radiation equilibrium wall temperature:**
```
T_wall = (q / (epsilon * sigma_SB))^0.25
```

Where:
- epsilon = emissivity of chamber wall (~0.3-0.8 depending on material and coating)
- sigma_SB = 5.67e-8 W/(m^2*K^4) — Stefan-Boltzmann constant

### Material Temperature Limits

The steady-state chamber wall temperature must remain below the material's
maximum service temperature (see Section 4 table). This is a key driver for
material selection.

---

## 9. Structural Considerations

### Thin-Wall Pressure Vessel (Chamber)

**Hoop stress:**
```
sigma_hoop = Pc * r / t
```

Where:
- Pc = chamber pressure [Pa]
- r = chamber inner radius [m]
- t = wall thickness [m]

**Required wall thickness (with safety factor):**
```
t_min = (Pc * SF * r) / sigma_yield_at_temp
```

Where SF = 1.5 (per REQUIREMENTS.md) and sigma_yield_at_temp is the yield
strength at the operating wall temperature (typically much lower than room
temperature values — check material data).

**Note:** For the low chamber pressures in this design (0.09-0.12 MPa), structural
requirements will likely be driven by minimum manufacturability thickness
(~0.5-1.0 mm) rather than pressure loads. Verify this.

---

## 10. Propellant Budget

### Tsiolkovsky Rocket Equation

```
delta_v = Isp * g0 * ln(m_initial / m_final)
```

Or, solving for propellant mass:
```
m_propellant = m_spacecraft * (exp(delta_v / (Isp * g0)) - 1)
```

### Total Impulse

```
I_total = m_propellant * Isp * g0    [N*s]
```

This must exceed 50,000 N*s per requirements.

### Mission Life Propellant Budget

At 1 N thrust, the total firing time for 50,000 N*s total impulse is:
```
t_total = I_total / F = 50,000 / 1.0 = 50,000 seconds ~ 13.9 hours
```

This is well within the 100-hour catalyst life requirement.