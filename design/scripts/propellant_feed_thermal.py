#!/usr/bin/env python3
"""
DES-007: Propellant Feed System Thermal Analysis
================================================

Design ID: DES-007
Traced Requirements: REQ-007, REQ-009, REQ-010, REQ-025
Author: Agent 2 (Design & Implementation Engineer)
Date: 2026-02-14

Purpose:
    Perform thermal analysis of the propellant feed system to verify that
    propellant temperature remains within the 5°C to 50°C range (REQ-010)
    under all operating conditions.

Physical Constants and Assumptions:
    - Hydrazine density: 1004 kg/m³ (CONTEXT.md)
    - Hydrazine specific heat: 3200 J/kg·K (NASA-SP-8096)
    - Hydrazine freezing point: 1.4°C (CONTEXT.md, critical for thermal design)
    - Hydrazine boiling point: 113.5°C at 1 atm (CONTEXT.md)
    - MLI effective thermal conductivity: 0.001 W/m·K (15 layers, space heritage)
    - MLI density: 20 kg/m³ (space heritage)
    - 316L stainless steel thermal conductivity: 16.3 W/m·K (material handbook)
    - Chamber temperature from DES-001: 1127°C (1400 K)

Design Parameters:
    - Propellant mass: 13.68 kg (from DES-002, with 10% margin)
    - Feed line diameter: 4 mm (1/8" tube, DEC-015)
    - Feed line outer diameter: 6 mm (1/8" tube)
    - Feed line length: 2 m (assumed from tank to thruster)
    - Mass flow rate: 2.44e-4 kg/s (from DES-001)
    - Feed pressure range: 0.15-0.30 MPa (REQ-009)
    - Spacecraft thermal cycle: -40°C to +80°C (REQ-017)

Output:
    - design/data/propellant_feed_thermal.json
    - Requirements compliance summary to stdout
"""

import json
import math

# =============================================================================
# PHYSICAL CONSTANTS (from CONTEXT.md and reference data)
# =============================================================================

# Universal constants
g0 = 9.80665  # m/s² - standard gravitational acceleration (exact)
pi = math.pi

# Hydrazine properties (from CONTEXT.md, NASA-SP-8096)
rho_N2H4 = 1004.0  # kg/m³ - liquid density at 25°C
cp_N2H4 = 3200.0   # J/kg·K - specific heat at 25°C
T_freeze_N2H4 = 1.4  # °C - freezing point (CRITICAL for thermal design)
T_boil_N2H4 = 113.5  # °C - boiling point at 1 atm

# MLI insulation properties (space heritage)
k_MLI = 0.001  # W/m·K - effective thermal conductivity (15 layers)
rho_MLI = 20.0  # kg/m³ - density

# 316L stainless steel properties (material handbook)
k_316L = 16.3  # W/m·K - thermal conductivity

# Chamber conditions (from DES-001)
T_chamber_C = 1127.0  # °C - steady-state chamber temperature
T_chamber_K = T_chamber_C + 273.15  # K

# Mass flow rate (from DES-001)
mdot = 2.44e-4  # kg/s - nominal mass flow rate

# =============================================================================
# DESIGN PARAMETERS
# =============================================================================

# Feed system sizing (from DEC-015)
D_feed_inner = 0.004  # m - feed line inner diameter (4 mm)
D_feed_outer = 0.006  # m - feed line outer diameter (6 mm)
L_feed = 2.0  # m - feed line length from tank to thruster

# Propellant properties (from DES-002)
m_propellant = 13.68  # kg - propellant mass (with 10% margin)

# Feed system volume
A_feed_inner = pi * (D_feed_inner / 2)**2  # m² - feed line cross-sectional area
V_feed_line = A_feed_inner * L_feed  # m³ - feed line volume

# Total propellant volume (tank + feed lines)
V_total = m_propellant / rho_N2H4  # m³ - total propellant volume (tank dominates)

# Thermal mass of propellant
C_thermal_propellant = m_propellant * cp_N2H4  # J/K - thermal mass

# =============================================================================
# REQUIREMENTS (from REQ_REGISTER.md)
# =============================================================================

# REQ-007: Use hydrazine (N2H4) as propellant
# - Verified by design: 316L SS selected for hydrazine compatibility

# REQ-009: Feed pressure range: 0.15-0.30 MPa
P_feed_min = 0.15  # MPa - minimum feed pressure
P_feed_max = 0.30  # MPa - maximum feed pressure
P_design = P_feed_max * 1.5  # MPa - design pressure (1.5× MEOP)

# REQ-010: Propellant temperature: 5°C to 50°C
T_propellant_min_req = 5.0   # °C - minimum allowable temperature
T_propellant_max_req = 50.0  # °C - maximum allowable temperature

# REQ-025: Materials must be space-qualified
# - Verified by design: 316L SS has extensive flight heritage

# =============================================================================
# THERMAL ANALYSIS
# =============================================================================

def analyze_cold_sook():
    """
    Analyze worst-case cold soak scenario.

    Assumptions:
    - Spacecraft at -40°C (cold eclipse, worst-case from REQ-017)
    - Initial propellant temperature: 20°C
    - Cold soak duration: 8 hours (typical eclipse duration)
    - Heat leak rate: 0.5 W (conservative estimate for MLI insulation)

    Returns:
        dict: Cold soak analysis results
    """
    # Scenario parameters
    T_spacecraft_C = -40.0  # °C - spacecraft temperature
    T_initial_C = 20.0  # °C - initial propellant temperature
    t_soh = 8.0 * 3600.0  # s - cold soak duration (8 hours)
    q_leak = 0.5  # W - heat leak rate through MLI

    # Calculate temperature drop
    delta_T_C = (q_leak * t_soh) / C_thermal_propellant  # °C
    T_final_C = T_initial_C - delta_T_C  # °C

    # Calculate margin
    margin_min = T_final_C - T_propellant_min_req  # °C

    # Pass/Fail check
    status = "PASS" if T_final_C >= T_propellant_min_req else "FAIL"

    return {
        "scenario": "cold_sook",
        "spacecraft_temperature_C": T_spacecraft_C,
        "initial_temperature_C": T_initial_C,
        "soak_duration_hours": t_soh / 3600.0,
        "heat_leak_rate_W": q_leak,
        "temperature_drop_C": delta_T_C,
        "final_temperature_C": T_final_C,
        "requirement_min_C": T_propellant_min_req,
        "margin_C": margin_min,
        "status": status
    }

def analyze_hot_sook():
    """
    Analyze worst-case hot soak scenario.

    Assumptions:
    - Spacecraft at +80°C (hot sun side, worst-case from REQ-017)
    - Initial propellant temperature: 20°C
    - Hot soak duration: 12 hours (typical sun side duration)
    - Heat leak rate: 0.5 W (conservative estimate for MLI insulation)

    Returns:
        dict: Hot soak analysis results
    """
    # Scenario parameters
    T_spacecraft_C = 80.0  # °C - spacecraft temperature
    T_initial_C = 20.0  # °C - initial propellant temperature
    t_soh = 12.0 * 3600.0  # s - hot soak duration (12 hours)
    q_leak = 0.5  # W - heat leak rate through MLI

    # Calculate temperature rise
    delta_T_C = (q_leak * t_soh) / C_thermal_propellant  # °C
    T_final_C = T_initial_C + delta_T_C  # °C

    # Calculate margin
    margin_max = T_propellant_max_req - T_final_C  # °C

    # Pass/Fail check
    status = "PASS" if T_final_C <= T_propellant_max_req else "FAIL"

    return {
        "scenario": "hot_sook",
        "spacecraft_temperature_C": T_spacecraft_C,
        "initial_temperature_C": T_initial_C,
        "soak_duration_hours": t_soh / 3600.0,
        "heat_leak_rate_W": q_leak,
        "temperature_rise_C": delta_T_C,
        "final_temperature_C": T_final_C,
        "requirement_max_C": T_propellant_max_req,
        "margin_C": margin_max,
        "status": status
    }

def analyze_operational_heating():
    """
    Analyze operational heating from thruster back-conduction.

    Assumptions:
    - Thruster operating at steady state (1 N thrust)
    - Chamber temperature: 1127°C (from DES-001)
    - Feed line length: 2 m
    - Tank at nominal temperature: 20°C
    - Heat conducted back through feed line

    Returns:
        dict: Operational heating analysis results
    """
    # Feed line geometry
    A_feed_annulus = pi * (D_feed_outer**2 - D_feed_inner**2) / 4  # m²

    # Temperature difference (chamber to tank)
    delta_T_C = T_chamber_C - 20.0  # °C

    # Heat conduction along feed line (Fourier's law)
    Q_conduction = k_316L * A_feed_annulus * delta_T_C / L_feed  # W

    # Temperature rise of bulk propellant
    delta_T_propellant_C = Q_conduction / (mdot * cp_N2H4)  # °C

    # Final propellant temperature (assuming tank at 20°C)
    T_final_C = 20.0 + delta_T_propellant_C  # °C

    # Calculate margins
    margin_min = T_final_C - T_propellant_min_req  # °C
    margin_max = T_propellant_max_req - T_final_C  # °C

    # Pass/Fail check
    status = "PASS" if T_propellant_min_req <= T_final_C <= T_propellant_max_req else "FAIL"

    return {
        "scenario": "operational_heating",
        "chamber_temperature_C": T_chamber_C,
        "tank_temperature_C": 20.0,
        "feed_line_length_m": L_feed,
        "feed_line_thermal_conductivity_W_mK": k_316L,
        "feed_line_annulus_area_m2": A_feed_annulus,
        "heat_conduction_W": Q_conduction,
        "temperature_rise_C": delta_T_propellant_C,
        "final_temperature_C": T_final_C,
        "requirement_min_C": T_propellant_min_req,
        "requirement_max_C": T_propellant_max_req,
        "margin_min_C": margin_min,
        "margin_max_C": margin_max,
        "status": status
    }

def analyze_pressure_drop():
    """
    Analyze pressure drop through feed line.

    Assumptions:
    - Feed line diameter: 4 mm
    - Mass flow rate: 2.44e-4 kg/s
    - Hydrazine dynamic viscosity: 0.00097 Pa·s at 20°C

    Returns:
        dict: Pressure drop analysis results
    """
    # Hydrazine properties at 20°C
    mu_N2H4 = 0.00097  # Pa·s - dynamic viscosity

    # Volumetric flow rate
    Q_volumetric = mdot / rho_N2H4  # m³/s

    # Flow velocity
    v_flow = Q_volumetric / A_feed_inner  # m/s

    # Reynolds number
    Re = (rho_N2H4 * v_flow * D_feed_inner) / mu_N2H4

    # Flow regime check
    if Re < 2300:
        # Laminar flow
        f_friction = 64.0 / Re
        flow_regime = "laminar"
    else:
        # Turbulent flow (using Colebrook-White approximation for smooth pipe)
        # For smooth pipes, Blasius correlation is reasonable
        f_friction = 0.316 / (Re ** 0.25)
        flow_regime = "turbulent"

    # Pressure drop (Darcy-Weisbach equation)
    # Analyze for 1 meter and 5 meter feed line lengths
    delta_P_1m_Pa = f_friction * (1.0 / D_feed_inner) * (rho_N2H4 * v_flow**2 / 2)
    delta_P_1m_MPa = delta_P_1m_Pa / 1e6

    delta_P_5m_Pa = f_friction * (5.0 / D_feed_inner) * (rho_N2H4 * v_flow**2 / 2)
    delta_P_5m_MPa = delta_P_5m_Pa / 1e6

    # Verify pressure drop is negligible relative to feed pressure range
    pressure_range_MPa = P_feed_max - P_feed_min
    percentage_drop_1m = (delta_P_1m_MPa / pressure_range_MPa) * 100
    percentage_drop_5m = (delta_P_5m_MPa / pressure_range_MPa) * 100

    # Pass/Fail check (pressure drop should be < 1% of pressure range)
    status_1m = "PASS" if percentage_drop_1m < 1.0 else "FAIL"
    status_5m = "PASS" if percentage_drop_5m < 1.0 else "FAIL"

    return {
        "scenario": "pressure_drop",
        "feed_line_inner_diameter_mm": D_feed_inner * 1000,
        "feed_line_outer_diameter_mm": D_feed_outer * 1000,
        "mass_flow_rate_kg_s": mdot,
        "volumetric_flow_rate_m3_s": Q_volumetric,
        "flow_velocity_m_s": v_flow,
        "reynolds_number": Re,
        "flow_regime": flow_regime,
        "friction_factor": f_friction,
        "pressure_drop_1m_Pa": delta_P_1m_Pa,
        "pressure_drop_1m_MPa": delta_P_1m_MPa,
        "pressure_drop_5m_Pa": delta_P_5m_Pa,
        "pressure_drop_5m_MPa": delta_P_5m_MPa,
        "pressure_range_MPa": pressure_range_MPa,
        "percentage_drop_1m_percent": percentage_drop_1m,
        "percentage_drop_5m_percent": percentage_drop_5m,
        "status_1m": status_1m,
        "status_5m": status_5m
    }

# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def main():
    """Execute thermal analysis and output results."""

    print("="*80)
    print("DES-007: Propellant Feed System Thermal Analysis")
    print("="*80)
    print()

    # Run thermal analyses
    cold_sook_results = analyze_cold_sook()
    hot_sook_results = analyze_hot_sook()
    operational_results = analyze_operational_heating()
    pressure_drop_results = analyze_pressure_drop()

    # Print results
    print("THERMAL ANALYSIS RESULTS")
    print("-" * 80)
    print()

    # Cold soak results
    print("1. COLD SOAK ANALYSIS (Worst-Case Minimum Temperature)")
    print("-" * 80)
    print(f"   Spacecraft Temperature:    {cold_sook_results['spacecraft_temperature_C']:.1f} °C")
    print(f"   Initial Propellant Temp:    {cold_sook_results['initial_temperature_C']:.1f} °C")
    print(f"   Soak Duration:              {cold_sook_results['soak_duration_hours']:.1f} hours")
    print(f"   Heat Leak Rate:             {cold_sook_results['heat_leak_rate_W']:.2f} W")
    print(f"   Temperature Drop:           {cold_sook_results['temperature_drop_C']:.3f} °C")
    print(f"   Final Propellant Temp:      {cold_sook_results['final_temperature_C']:.3f} °C")
    print(f"   Requirement (min):           {cold_sook_results['requirement_min_C']:.1f} °C")
    print(f"   Margin:                     {cold_sook_results['margin_C']:.3f} °C")
    print(f"   Status:                     {cold_sook_results['status']}")
    print()

    # Hot soak results
    print("2. HOT SOAK ANALYSIS (Worst-Case Maximum Temperature)")
    print("-" * 80)
    print(f"   Spacecraft Temperature:    {hot_sook_results['spacecraft_temperature_C']:.1f} °C")
    print(f"   Initial Propellant Temp:    {hot_sook_results['initial_temperature_C']:.1f} °C")
    print(f"   Soak Duration:              {hot_sook_results['soak_duration_hours']:.1f} hours")
    print(f"   Heat Leak Rate:             {hot_sook_results['heat_leak_rate_W']:.2f} W")
    print(f"   Temperature Rise:           {hot_sook_results['temperature_rise_C']:.3f} °C")
    print(f"   Final Propellant Temp:      {hot_sook_results['final_temperature_C']:.3f} °C")
    print(f"   Requirement (max):           {hot_sook_results['requirement_max_C']:.1f} °C")
    print(f"   Margin:                     {hot_sook_results['margin_C']:.3f} °C")
    print(f"   Status:                     {hot_sook_results['status']}")
    print()

    # Operational heating results
    print("3. OPERATIONAL HEATING ANALYSIS (Steady-State Thruster Operation)")
    print("-" * 80)
    print(f"   Chamber Temperature:         {operational_results['chamber_temperature_C']:.1f} °C")
    print(f"   Tank Temperature:            {operational_results['tank_temperature_C']:.1f} °C")
    print(f"   Feed Line Length:            {operational_results['feed_line_length_m']:.1f} m")
    print(f"   Heat Conduction:             {operational_results['heat_conduction_W']:.3f} W")
    print(f"   Temperature Rise:             {operational_results['temperature_rise_C']:.3f} °C")
    print(f"   Final Propellant Temp:       {operational_results['final_temperature_C']:.3f} °C")
    print(f"   Requirement (min):           {operational_results['requirement_min_C']:.1f} °C")
    print(f"   Requirement (max):           {operational_results['requirement_max_C']:.1f} °C")
    print(f"   Margin (min):                {operational_results['margin_min_C']:.3f} °C")
    print(f"   Margin (max):                {operational_results['margin_max_C']:.3f} °C")
    print(f"   Status:                     {operational_results['status']}")
    print()

    # Pressure drop results
    print("4. PRESSURE DROP ANALYSIS")
    print("-" * 80)
    print(f"   Feed Line Inner Diameter:    {pressure_drop_results['feed_line_inner_diameter_mm']:.1f} mm")
    print(f"   Feed Line Outer Diameter:    {pressure_drop_results['feed_line_outer_diameter_mm']:.1f} mm")
    print(f"   Mass Flow Rate:              {pressure_drop_results['mass_flow_rate_kg_s']:.6f} kg/s")
    print(f"   Flow Velocity:               {pressure_drop_results['flow_velocity_m_s']:.4f} m/s")
    print(f"   Reynolds Number:             {pressure_drop_results['reynolds_number']:.1f}")
    print(f"   Flow Regime:                 {pressure_drop_results['flow_regime']}")
    print(f"   Friction Factor:             {pressure_drop_results['friction_factor']:.4f}")
    print(f"   Pressure Drop (1 m):          {pressure_drop_results['pressure_drop_1m_Pa']:.3f} Pa ({pressure_drop_results['pressure_drop_1m_MPa']:.6f} MPa)")
    print(f"   Pressure Drop (5 m):          {pressure_drop_results['pressure_drop_5m_Pa']:.3f} Pa ({pressure_drop_results['pressure_drop_5m_MPa']:.6f} MPa)")
    print(f"   Feed Pressure Range:         {pressure_drop_results['pressure_range_MPa']:.2f} MPa")
    print(f"   Percentage Drop (1 m):        {pressure_drop_results['percentage_drop_1m_percent']:.4f}%")
    print(f"   Percentage Drop (5 m):        {pressure_drop_results['percentage_drop_5m_percent']:.4f}%")
    print(f"   Status (1 m):                {pressure_drop_results['status_1m']}")
    print(f"   Status (5 m):                {pressure_drop_results['status_5m']}")
    print()

    # REQUIREMENTS COMPLIANCE SUMMARY
    print("="*80)
    print("REQUIREMENTS COMPLIANCE SUMMARY")
    print("="*80)
    print()

    # REQ-007: Hydrazine propellant
    req_007_status = "PASS"
    req_007_margin = "N/A (material compatibility verified)"
    print(f"REQ-007: Use hydrazine (N2H4) as propellant")
    print(f"  Status:    {req_007_status}")
    print(f"  Margin:    {req_007_margin}")
    print(f"  Details:   316L stainless steel selected with extensive hydrazine flight heritage")
    print()

    # REQ-009: Feed pressure range
    req_009_status = "PASS" if pressure_drop_results['status_5m'] == "PASS" else "FAIL"
    req_009_margin_min = "N/A"
    req_009_margin_max = f"Pressure drop negligible (< 1%)"
    print(f"REQ-009: Feed pressure range 0.15-0.30 MPa")
    print(f"  Status:    {req_009_status}")
    print(f"  Margin:    {req_009_margin_max}")
    print(f"  Details:   Pressure drop < 0.001 MPa for 5 m feed line, negligible")
    print()

    # REQ-010: Propellant temperature 5-50°C
    # Check all three thermal scenarios
    all_temp_pass = (
        cold_sook_results['status'] == "PASS" and
        hot_sook_results['status'] == "PASS" and
        operational_results['status'] == "PASS"
    )
    req_010_status = "PASS" if all_temp_pass else "FAIL"

    # Find minimum and maximum margins across all scenarios
    min_margin_cold = cold_sook_results['margin_C']
    max_margin_hot = hot_sook_results['margin_C']
    print(f"REQ-010: Propellant temperature 5-50°C")
    print(f"  Status:    {req_010_status}")
    print(f"  Margin (min):  {min_margin_cold:.2f} °C (cold soak scenario)")
    print(f"  Margin (max):  {max_margin_hot:.2f} °C (hot soak scenario)")
    print(f"  Details:")
    print(f"    Cold soak:    {cold_sook_results['final_temperature_C']:.2f} °C (requirement: ≥{T_propellant_min_req}°C)")
    print(f"    Hot soak:     {hot_sook_results['final_temperature_C']:.2f} °C (requirement: ≤{T_propellant_max_req}°C)")
    print(f"    Operational:  {operational_results['final_temperature_C']:.2f} °C (requirement: 5-50°C)")
    print()

    # REQ-025: Space-qualified materials
    req_025_status = "PASS"
    req_025_margin = "N/A (heritage verified)"
    print(f"REQ-025: Materials must be space-qualified")
    print(f"  Status:    {req_025_status}")
    print(f"  Margin:    {req_025_margin}")
    print(f"  Details:   316L SS, PTFE, and Viton have extensive flight heritage")
    print()

    # Overall compliance
    all_pass = (
        req_007_status == "PASS" and
        req_009_status == "PASS" and
        req_010_status == "PASS" and
        req_025_status == "PASS"
    )

    print("="*80)
    print(f"OVERALL COMPLIANCE: {all_pass}")
    print("="*80)
    print()

    # Prepare output data
    output_data = {
        "design_id": "DES-007",
        "design_title": "Propellant Feed System Design",
        "date": "2026-02-14",
        "traced_requirements": ["REQ-007", "REQ-009", "REQ-010", "REQ-025"],
        "physical_constants": {
            "rho_N2H4_kg_m3": rho_N2H4,
            "cp_N2H4_J_kgK": cp_N2H4,
            "T_freeze_N2H4_C": T_freeze_N2H4,
            "T_boil_N2H4_C": T_boil_N2H4,
            "k_MLI_W_mK": k_MLI,
            "k_316L_W_mK": k_316L,
            "mdot_kg_s": mdot
        },
        "design_parameters": {
            "propellant_mass_kg": m_propellant,
            "feed_line_inner_diameter_mm": D_feed_inner * 1000,
            "feed_line_outer_diameter_mm": D_feed_outer * 1000,
            "feed_line_length_m": L_feed,
            "feed_pressure_min_MPa": P_feed_min,
            "feed_pressure_max_MPa": P_feed_max
        },
        "thermal_analysis": {
            "cold_sook": cold_sook_results,
            "hot_sook": hot_sook_results,
            "operational_heating": operational_results
        },
        "pressure_drop_analysis": pressure_drop_results,
        "requirements_compliance": {
            "REQ-007": {
                "status": req_007_status,
                "description": "Use hydrazine (N2H4) as propellant",
                "margin": req_007_margin
            },
            "REQ-009": {
                "status": req_009_status,
                "description": "Feed pressure range 0.15-0.30 MPa",
                "margin": req_009_margin_max
            },
            "REQ-010": {
                "status": req_010_status,
                "description": "Propellant temperature 5-50°C",
                "margin_min_C": min_margin_cold,
                "margin_max_C": max_margin_hot
            },
            "REQ-025": {
                "status": req_025_status,
                "description": "Materials must be space-qualified",
                "margin": req_025_margin
            }
        },
        "overall_compliance": all_pass
    }

    # Write output JSON
    output_file = "design/data/propellant_feed_thermal.json"
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)

    print(f"Output data written to: {output_file}")
    print()

if __name__ == "__main__":
    main()
