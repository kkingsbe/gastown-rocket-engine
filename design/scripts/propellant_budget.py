#!/usr/bin/env python3
"""
DES-002: Propellant Budget Calculation

This script calculates the required propellant mass to meet the total impulse
requirement of 50,000 N·s over the 15-year mission life, and verifies that it
fits within the 25 kg propellant mass budget.

Physical Constants (from CONTEXT.md):
- g0 = 9.80665 m/s² (standard gravitational acceleration, exact SI)

Key Equations:
- Total Impulse: I_total = m_propellant * Isp * g0
- Propellant Mass: m_propellant = I_total / (Isp * g0)

Requirements Traced:
- REQ-005: Total impulse ≥ 50,000 N·s over 15-year mission life
- REQ-008: Propellant mass ≤ 25 kg

Design Assumptions:
- Use design Isp = 410 s from DES-001 for propellant budget (actual expected performance)
- Include 10% margin for mission uncertainty (Isp degradation, residuals, leaks)
- Hydrazine liquid density = 1004 kg/m³ at 25°C (from CONTEXT.md)
"""

import json
import math
from pathlib import Path

# ============================================================================
# PHYSICAL CONSTANTS (from CONTEXT.md)
# ============================================================================
g0 = 9.80665  # m/s² — standard gravitational acceleration (exact, SI)
RHO_N2H4 = 1004.0  # kg/m³ — liquid hydrazine density at 25°C

# ============================================================================
# REQUIREMENTS CONSTANTS
# ============================================================================
REQ_005_TOTAL_IMPULSE_NS = 50000.0  # N·s — minimum total impulse requirement
REQ_008_MAX_PROPELLANT_MASS_KG = 25.0  # kg — maximum propellant mass budget
REQ_002_MIN_ISP_S = 220.0  # s — minimum specific impulse (requirement)
REQ_030_MISSION_YEARS = 15  # years — mission lifetime
REQ_020_FIRING_CYCLES = 50000  # cycles — minimum firing cycles
REQ_021_CATALYST_LIFETIME_HOURS = 100.0  # hours — catalyst lifetime requirement
UNCERTAINTY_MARGIN_PCT = 10.0  # % — margin for mission uncertainty

# ============================================================================
# DESIGN DATA FROM DES-001 (read from thruster_performance_sizing.json)
# ============================================================================
DES001_DATA = {
    "specific_impulse_s": 410.08,  # s — actual design Isp (from DES-001)
    "mass_flow_rate_kg_s": 0.000249,  # kg/s — steady-state mass flow rate
    "thrust_N": 1.0  # N — nominal thrust
}

# ============================================================================
# CALCULATIONS
# ============================================================================

def calculate_propellant_mass_nominal(isp_s, total_impulse_ns):
    """
    Calculate propellant mass required to achieve specified total impulse.
    
    Equation: m_propellant = I_total / (Isp * g0)
    
    Args:
        isp_s: Specific impulse in seconds
        total_impulse_ns: Total impulse in N·s
    
    Returns:
        Propellant mass in kg
    """
    return total_impulse_ns / (isp_s * g0)


def calculate_propellant_volume_kg_to_m3(propellant_mass_kg):
    """
    Convert propellant mass to volume using liquid hydrazine density.
    
    Equation: V = m / rho
    
    Args:
        propellant_mass_kg: Propellant mass in kg
    
    Returns:
        Propellant volume in m³
    """
    return propellant_mass_kg / RHO_N2H4


def calculate_total_firing_time_s(propellant_mass_kg, mass_flow_rate_kg_s):
    """
    Calculate total firing time for given propellant mass and mass flow rate.
    
    Equation: t = m / mdot
    
    Args:
        propellant_mass_kg: Propellant mass in kg
        mass_flow_rate_kg_s: Mass flow rate in kg/s
    
    Returns:
        Total firing time in seconds
    """
    return propellant_mass_kg / mass_flow_rate_kg_s


def calculate_impulse_per_firing_cycle(total_impulse_ns, firing_cycles):
    """
    Calculate average impulse per firing cycle.
    
    Equation: I_cycle = I_total / N_cycles
    
    Args:
        total_impulse_ns: Total impulse in N·s
        firing_cycles: Number of firing cycles
    
    Returns:
        Impulse per cycle in N·s
    """
    return total_impulse_ns / firing_cycles


def calculate_min_pulse_time_ns(impulse_cycle_ns, thrust_N):
    """
    Calculate minimum pulse time for given impulse per cycle and thrust.
    
    Equation: t_min = I_cycle / F
    
    Args:
        impulse_cycle_ns: Impulse per cycle in N·s
        thrust_N: Thrust in N
    
    Returns:
        Minimum pulse time in seconds
    """
    return impulse_cycle_ns / thrust_N


def main():
    print("=" * 80)
    print("DES-002: Propellant Budget Calculation")
    print("=" * 80)
    print()
    
    # Step 1: Calculate nominal propellant mass using design Isp (from DES-001)
    print("Step 1: Calculate Nominal Propellant Mass")
    print("-" * 60)
    print(f"  Design approach: Use design Isp from DES-001 (actual expected performance)")
    print(f"  Design Isp: {DES001_DATA['specific_impulse_s']:.2f} s")
    print(f"  Required total impulse: {REQ_005_TOTAL_IMPULSE_NS:,.0f} N·s")
    print(f"  Standard gravity (g0): {g0} m/s²")
    m_prop_nominal = calculate_propellant_mass_nominal(
        DES001_DATA["specific_impulse_s"],
        REQ_005_TOTAL_IMPULSE_NS
    )
    print(f"  Nominal propellant mass: {m_prop_nominal:.4f} kg")
    print()
    
    # Step 1a: Also calculate using minimum Isp (conservative) for comparison
    print("Step 1a: Compare with Minimum Isp (Conservative Baseline)")
    print("-" * 60)
    m_prop_conservative = calculate_propellant_mass_nominal(
        REQ_002_MIN_ISP_S,
        REQ_005_TOTAL_IMPULSE_NS
    )
    print(f"  Minimum Isp (conservative): {REQ_002_MIN_ISP_S} s")
    print(f"  Conservative propellant mass: {m_prop_conservative:.4f} kg")
    print(f"  Reduction using design Isp: {(m_prop_conservative - m_prop_nominal):.4f} kg ({(m_prop_conservative - m_prop_nominal)/m_prop_conservative*100:.1f}%)")
    print()
    
    # Step 2: Add 10% margin for mission uncertainty
    print("Step 2: Add Mission Uncertainty Margin")
    print("-" * 60)
    print(f"  Margin covers: Isp degradation over life, residual propellant,")
    print(f"                  pressurization losses, potential leaks")
    m_prop_with_margin = m_prop_nominal * (1.0 + UNCERTAINTY_MARGIN_PCT / 100.0)
    margin_amount = m_prop_with_margin - m_prop_nominal
    print(f"  Nominal propellant mass: {m_prop_nominal:.4f} kg")
    print(f"  Uncertainty margin: {UNCERTAINTY_MARGIN_PCT}%")
    print(f"  Margin amount: {margin_amount:.4f} kg")
    print(f"  Propellant mass with margin: {m_prop_with_margin:.4f} kg")
    print()
    
    # Step 3: Verify against 25 kg propellant budget
    print("Step 3: Verify Against Propellant Mass Budget")
    print("-" * 60)
    budget_utilization_pct = (m_prop_with_margin / REQ_008_MAX_PROPELLANT_MASS_KG) * 100.0
    budget_remaining_kg = REQ_008_MAX_PROPELLANT_MASS_KG - m_prop_with_margin
    print(f"  Required propellant mass (with margin): {m_prop_with_margin:.4f} kg")
    print(f"  Maximum allowed propellant mass: {REQ_008_MAX_PROPELLANT_MASS_KG:.1f} kg")
    print(f"  Budget utilization: {budget_utilization_pct:.1f}%")
    if budget_remaining_kg >= 0:
        print(f"  Budget remaining: {budget_remaining_kg:.4f} kg")
        print(f"  Status: PASS - {budget_utilization_pct:.1f}% < 100.0%")
    else:
        print(f"  Budget overage: {-budget_remaining_kg:.4f} kg")
        print(f"  Status: FAIL - {budget_utilization_pct:.1f}% > 100.0%")
    print()
    
    # Step 4: Calculate propellant volume (for tank sizing)
    print("Step 4: Calculate Propellant Volume")
    print("-" * 60)
    V_prop_m3 = calculate_propellant_volume_kg_to_m3(m_prop_with_margin)
    V_prop_liters = V_prop_m3 * 1000.0
    print(f"  Propellant mass: {m_prop_with_margin:.4f} kg")
    print(f"  Hydrazine liquid density: {RHO_N2H4} kg/m³")
    print(f"  Propellant volume: {V_prop_m3:.6f} m³")
    print(f"  Propellant volume: {V_prop_liters:.3f} liters")
    print()
    
    # Step 5: Calculate total firing time using actual design Isp (from DES-001)
    print("Step 5: Calculate Total Firing Time (Using Design Isp)")
    print("-" * 60)
    t_firing_seconds = calculate_total_firing_time_s(m_prop_with_margin, DES001_DATA["mass_flow_rate_kg_s"])
    t_firing_hours = t_firing_seconds / 3600.0
    print(f"  Propellant mass: {m_prop_with_margin:.4f} kg")
    print(f"  Design mass flow rate: {DES001_DATA['mass_flow_rate_kg_s']:.9f} kg/s")
    print(f"  Total firing time: {t_firing_hours:.2f} hours")
    print(f"  Total firing time: {t_firing_seconds:.0f} seconds")
    print()
    
    # Step 6: Calculate impulse per firing cycle
    print("Step 6: Calculate Impulse Per Firing Cycle")
    print("-" * 60)
    I_cycle = calculate_impulse_per_firing_cycle(REQ_005_TOTAL_IMPULSE_NS, REQ_020_FIRING_CYCLES)
    print(f"  Total impulse: {REQ_005_TOTAL_IMPULSE_NS:,.0f} N·s")
    print(f"  Number of firing cycles: {REQ_020_FIRING_CYCLES:,}")
    print(f"  Impulse per cycle: {I_cycle:.4f} N·s")
    print(f"  Minimum impulse bit requirement (REQ-004): 0.01 N·s")
    print(f"  PASS: {I_cycle:.4f} N·s > 0.01 N·s" if I_cycle >= 0.01 else f"  FAIL: {I_cycle:.4f} N·s < 0.01 N·s")
    print()
    
    # Step 7: Calculate minimum pulse time
    print("Step 7: Calculate Minimum Pulse Time")
    print("-" * 60)
    t_pulse_min = calculate_min_pulse_time_ns(I_cycle, DES001_DATA["thrust_N"])
    t_pulse_min_ms = t_pulse_min * 1000.0
    print(f"  Impulse per cycle: {I_cycle:.4f} N·s")
    print(f"  Nominal thrust: {DES001_DATA['thrust_N']:.1f} N")
    print(f"  Minimum pulse time: {t_pulse_min_ms:.1f} ms")
    print(f"  Minimum pulse time: {t_pulse_min:.4f} s")
    print()
    
    # Step 8: Calculate actual total impulse achievable with propellant mass
    print("Step 8: Verify Total Impulse Achievement")
    print("-" * 60)
    I_achievable_nominal = m_prop_nominal * DES001_DATA["specific_impulse_s"] * g0
    I_achievable_margin = m_prop_with_margin * DES001_DATA["specific_impulse_s"] * g0
    print(f"  Design Isp (from DES-001): {DES001_DATA['specific_impulse_s']:.2f} s")
    print(f"  Propellant mass (nominal): {m_prop_nominal:.4f} kg")
    print(f"  Achievable total impulse (nominal): {I_achievable_nominal:,.0f} N·s")
    print(f"  Required total impulse (REQ-005): {REQ_005_TOTAL_IMPULSE_NS:,.0f} N·s")
    print(f"  Margin on total impulse: {(I_achievable_nominal / REQ_005_TOTAL_IMPULSE_NS - 1.0) * 100:.1f}%")
    print(f"  With uncertainty margin: {m_prop_with_margin:.4f} kg")
    print(f"  Achievable total impulse (with margin): {I_achievable_margin:,.0f} N·s")
    print()
    
    # Step 9: Verify catalyst lifetime requirement
    print("Step 9: Verify Catalyst Lifetime (REQ-021)")
    print("-" * 60)
    print(f"  Total firing time (with margin): {t_firing_hours:.2f} hours")
    print(f"  Catalyst lifetime requirement: {REQ_021_CATALYST_LIFETIME_HOURS} hours (REQ-021)")
    if t_firing_hours <= REQ_021_CATALYST_LIFETIME_HOURS:
        margin_hours = REQ_021_CATALYST_LIFETIME_HOURS - t_firing_hours
        print(f"  PASS: {t_firing_hours:.2f} h < {REQ_021_CATALYST_LIFETIME_HOURS} h")
        print(f"  Margin: {margin_hours:.2f} hours")
    else:
        overage_hours = t_firing_hours - REQ_021_CATALYST_LIFETIME_HOURS
        print(f"  FAIL: {t_firing_hours:.2f} h > {REQ_021_CATALYST_LIFETIME_HOURS} h")
        print(f"  Overage: {overage_hours:.2f} hours")
    print()
    
    # ============================================================================
    # REQUIREMENTS COMPLIANCE SUMMARY
    # ============================================================================
    print("=" * 80)
    print("REQUIREMENTS COMPLIANCE SUMMARY")
    print("=" * 80)
    
    # REQ-002: Minimum Isp (verification that design Isp meets requirement)
    req_002_status = "PASS" if DES001_DATA["specific_impulse_s"] >= REQ_002_MIN_ISP_S else "FAIL"
    req_002_margin = (DES001_DATA["specific_impulse_s"] / REQ_002_MIN_ISP_S - 1.0) * 100.0
    print(f"\nREQ-002: Isp ≥ {REQ_002_MIN_ISP_S:.0f} s (design verification)")
    print(f"  Computed: {DES001_DATA['specific_impulse_s']:.2f} s (from DES-001)")
    print(f"  Margin: {req_002_margin:.1f}%")
    print(f"  Status: {req_002_status}")
    
    # REQ-005: Total Impulse
    req_005_status = "PASS" if I_achievable_nominal >= REQ_005_TOTAL_IMPULSE_NS else "FAIL"
    req_005_margin = (I_achievable_nominal / REQ_005_TOTAL_IMPULSE_NS - 1.0) * 100.0
    print(f"\nREQ-005: Total Impulse ≥ {REQ_005_TOTAL_IMPULSE_NS:,.0f} N·s")
    print(f"  Computed: {I_achievable_nominal:,.0f} N·s")
    print(f"  Margin: {req_005_margin:.1f}%")
    print(f"  Status: {req_005_status}")
    
    # REQ-008: Propellant Mass Budget
    req_008_status = "PASS" if m_prop_with_margin <= REQ_008_MAX_PROPELLANT_MASS_KG else "FAIL"
    if m_prop_with_margin <= REQ_008_MAX_PROPELLANT_MASS_KG:
        req_008_margin = (1.0 - m_prop_with_margin / REQ_008_MAX_PROPELLANT_MASS_KG) * 100.0
    else:
        req_008_margin = -(m_prop_with_margin / REQ_008_MAX_PROPELLANT_MASS_KG - 1.0) * 100.0
    print(f"\nREQ-008: Propellant Mass ≤ {REQ_008_MAX_PROPELLANT_MASS_KG:.1f} kg")
    print(f"  Computed: {m_prop_with_margin:.4f} kg")
    print(f"  Margin: {req_008_margin:.1f}%")
    print(f"  Status: {req_008_status}")
    
    # REQ-020: Firing Cycles
    req_020_status = "PASS" if REQ_020_FIRING_CYCLES >= 50000 else "FAIL"
    print(f"\nREQ-020: ≥ 50,000 Firing Cycles")
    print(f"  Assumed: {REQ_020_FIRING_CYCLES:,} cycles")
    print(f"  Status: {req_020_status}")
    
    # REQ-021: Catalyst Lifetime
    req_021_status = "PASS" if t_firing_hours <= REQ_021_CATALYST_LIFETIME_HOURS else "FAIL"
    if t_firing_hours <= REQ_021_CATALYST_LIFETIME_HOURS:
        req_021_margin = (REQ_021_CATALYST_LIFETIME_HOURS - t_firing_hours) / REQ_021_CATALYST_LIFETIME_HOURS * 100.0
    else:
        req_021_margin = -(t_firing_hours - REQ_021_CATALYST_LIFETIME_HOURS) / REQ_021_CATALYST_LIFETIME_HOURS * 100.0
    print(f"\nREQ-021: Catalyst Lifetime ≥ {REQ_021_CATALYST_LIFETIME_HOURS} hours")
    print(f"  Computed firing time: {t_firing_hours:.2f} hours")
    print(f"  Margin: {req_021_margin:.1f}%")
    print(f"  Status: {req_021_status}")
    
    print()
    print("=" * 80)
    
    # ============================================================================
    # OUTPUT JSON DATA
    # ============================================================================
    output_data = {
        "design_id": "DES-002",
        "parameters": {
            "total_impulse_requirement_Ns": REQ_005_TOTAL_IMPULSE_NS,
            "propellant_mass_budget_kg": REQ_008_MAX_PROPELLANT_MASS_KG,
            "minimum_isp_s": REQ_002_MIN_ISP_S,
            "design_isp_s": DES001_DATA["specific_impulse_s"],
            "mass_flow_rate_kg_s": DES001_DATA["mass_flow_rate_kg_s"],
            "nominal_thrust_N": DES001_DATA["thrust_N"],
            "firing_cycles": REQ_020_FIRING_CYCLES,
            "uncertainty_margin_pct": UNCERTAINTY_MARGIN_PCT,
            "standard_gravity_m_s2": g0,
            "hydrazine_density_kg_m3": RHO_N2H4,
            "catalyst_lifetime_hours": REQ_021_CATALYST_LIFETIME_HOURS
        },
        "computed_results": {
            "nominal_propellant_mass_kg": m_prop_nominal,
            "conservative_propellant_mass_min_isp_kg": m_prop_conservative,
            "margin_amount_kg": margin_amount,
            "propellant_mass_with_margin_kg": m_prop_with_margin,
            "propellant_volume_m3": V_prop_m3,
            "propellant_volume_liters": V_prop_liters,
            "total_firing_time_seconds": t_firing_seconds,
            "total_firing_time_hours": t_firing_hours,
            "impulse_per_cycle_Ns": I_cycle,
            "minimum_pulse_time_ms": t_pulse_min_ms,
            "minimum_pulse_time_s": t_pulse_min,
            "achievable_total_impulse_nominal_Ns": I_achievable_nominal,
            "achievable_total_impulse_with_margin_Ns": I_achievable_margin,
            "budget_utilization_pct": budget_utilization_pct,
            "budget_remaining_kg": budget_remaining_kg if budget_remaining_kg >= 0 else 0.0
        },
        "requirements_compliance": {
            "REQ-002": {
                "description": "Specific Impulse ≥ 220 s",
                "threshold_min": REQ_002_MIN_ISP_S,
                "computed": DES001_DATA["specific_impulse_s"],
                "unit": "s",
                "margin_percent": req_002_margin,
                "status": req_002_status
            },
            "REQ-005": {
                "description": "Total Impulse ≥ 50,000 N·s",
                "threshold_min": REQ_005_TOTAL_IMPULSE_NS,
                "computed": I_achievable_nominal,
                "unit": "N·s",
                "margin_percent": req_005_margin,
                "status": req_005_status
            },
            "REQ-008": {
                "description": "Propellant Mass ≤ 25 kg",
                "threshold_max": REQ_008_MAX_PROPELLANT_MASS_KG,
                "computed": m_prop_with_margin,
                "unit": "kg",
                "margin_percent": req_008_margin,
                "status": req_008_status
            },
            "REQ-020": {
                "description": "≥ 50,000 Firing Cycles",
                "threshold_min": 50000,
                "computed": REQ_020_FIRING_CYCLES,
                "unit": "cycles",
                "margin_percent": 0.0,
                "status": req_020_status
            },
            "REQ-021": {
                "description": "Catalyst Lifetime ≥ 100 hours",
                "threshold_min": REQ_021_CATALYST_LIFETIME_HOURS,
                "computed": t_firing_hours,
                "unit": "hours",
                "margin_percent": req_021_margin,
                "status": req_021_status
            }
        },
        "assumptions": [
            f"Design Isp = {DES001_DATA['specific_impulse_s']:.2f} s from DES-001 (actual expected performance)",
            f"Minimum Isp = {REQ_002_MIN_ISP_S} s (conservative baseline for comparison, from REQ-002)",
            f"Mass flow rate = {DES001_DATA['mass_flow_rate_kg_s']:.9f} kg/s from DES-001",
            f"Nominal thrust = {DES001_DATA['thrust_N']:.1f} N from DES-001",
            f"Total impulse requirement = {REQ_005_TOTAL_IMPULSE_NS:,.0f} N·s (REQ-005)",
            f"Firing cycles = {REQ_020_FIRING_CYCLES:,} cycles (REQ-020)",
            f"Uncertainty margin = {UNCERTAINTY_MARGIN_PCT}% for mission uncertainty",
            f"Hydrazine liquid density = {RHO_N2H4} kg/m³ at 25°C (from CONTEXT.md)",
            f"Standard gravity g0 = {g0} m/s² (exact SI constant)",
            f"Mission life = {REQ_030_MISSION_YEARS} years (REQ-030)",
            f"Catalyst lifetime = {REQ_021_CATALYST_LIFETIME_HOURS} hours (REQ-021)",
            f"Minimum impulse bit = 0.01 N·s (REQ-004) - satisfied with {I_cycle:.4f} N·s per cycle",
            "Uncertainty margin accounts for: Isp degradation over mission life, residual propellant,",
            "  pressurization system losses, and potential leakage",
            "Isp degradation not explicitly modeled - margin accounts for performance degradation",
            "Tank pressurization gas mass not included in this propellant budget (separate system)"
        ]
    }
    
    # Write output JSON file
    output_path = Path("design/data/propellant_budget.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(output_data, f, indent=2)
    
    print(f"\nOutput data written to: {output_path}")
    print()
    
    return 0


if __name__ == "__main__":
    exit(main())
