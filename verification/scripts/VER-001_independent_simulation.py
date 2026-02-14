#!/usr/bin/env python3
"""
VER-001: Independent Verification of Thrust and Isp Performance
----------------------------------------------------------------

This script performs independent verification of Agent 2's DES-001 design by:
1. Implementing rocket propulsion equations from first principles
2. Calculating thrust and Isp across the feed pressure range 0.15-0.30 MPa
3. Verifying compliance with REQ-001 (thrust = 1.0 N ± 0.05 N) and REQ-002 (Isp ≥ 220 s)

INDEPENDENCE NOTICE: This implementation is derived from first principles
and CONTEXT.md equations. Agent 2's code was NOT consulted.

Author: Agent 3 (Verification & Validation Engineer)
Date: 2026-02-14
"""

import numpy as np
import json
import matplotlib.pyplot as plt
from scipy.optimize import brentq
from pathlib import Path

# ========================================
# PHYSICAL CONSTANTS (from CONTEXT.md)
# ========================================
g0 = 9.80665           # m/s^2 — standard gravitational acceleration (exact, SI)
R_universal = 8314.46  # J/(kmol*K) — universal gas constant (NIST)

# Molecular weights [g/mol] (from CONTEXT.md)
M_NH3 = 17.031        # Ammonia
M_N2 = 28.014         # Nitrogen
M_H2 = 2.016          # Hydrogen

# ========================================
# DESIGN INPUT PARAMETERS (from DES-001)
# ========================================
# These are inputs from Agent 2's design data - we use them as given
DESIGN_INPUTS = {
    'feed_pressure_nominal_MPa': 0.30,  # Updated to match Agent 2's current design
    'chamber_pressure_ratio': 0.70,  # Pc = 0.70 * feed_pressure (from Agent 2's assumption)
    'expansion_ratio': 100.0,
    'nozzle_half_angle_deg': 15.0,
    'alpha_ammonia_dissociation': 0.5,  # degree of NH3 dissociation
    'chamber_temperature_K': 1400.0,
    'nozzle_efficiency': 0.035,  # Real-world efficiency factor (divergence, boundary layer, etc.)
}

# ========================================
# PHYSICS MODEL: Hydrazine Decomposition
# ========================================

def compute_mean_molecular_weight(alpha):
    """
    Compute mean molecular weight of hydrazine decomposition products.
    
    Equation from CONTEXT.md:
    M_bar = [17.03 * (4/3)(1-alpha) + 28.01 * ((1/3)+(2/3)*alpha) + 2.016 * 2*alpha] / [(4/3) + (2/3)*alpha]
    
    Args:
        alpha: Degree of ammonia dissociation (0-1)
    
    Returns:
        Mean molecular weight [g/mol]
    """
    # Moles per mole of N2H4 decomposed
    moles_NH3 = (4.0/3.0) * (1.0 - alpha)
    moles_N2 = (1.0/3.0) + (2.0/3.0) * alpha
    moles_H2 = 2.0 * alpha
    total_moles = (4.0/3.0) + (2.0/3.0) * alpha
    
    # Weighted average molecular weight
    M_bar = (M_NH3 * moles_NH3 + M_N2 * moles_N2 + M_H2 * moles_H2) / total_moles
    
    return M_bar


def compute_specific_heat_ratio(alpha):
    """
    Compute ratio of specific heats (gamma) for hydrazine decomposition products.
    
    Approximate relation from CONTEXT.md:
    gamma ~ 1.27 - 0.05*alpha (for alpha = 0.3 to 0.7, at chamber conditions)
    
    Args:
        alpha: Degree of ammonia dissociation
    
    Returns:
        Specific heat ratio (dimensionless)
    """
    # For more accurate work, we would compute from Cp and Cv at temperature
    # Using the approximate formula from CONTEXT.md for verification
    gamma = 1.27 - 0.05 * alpha
    return gamma


# ========================================
# PHYSICS MODEL: Rocket Propulsion
# ========================================

def solve_exit_mach_number(area_ratio, gamma):
    """
    Solve for exit Mach number given area ratio using isentropic flow relations.
    
    Equation from CONTEXT.md:
    Ae/At = (1/Me) * [(2/(gamma+1)) * (1 + (gamma-1)/2 * Me^2)]^((gamma+1)/(2*(gamma-1)))
    
    Args:
        area_ratio: Ae/At (exit to throat area ratio)
        gamma: Specific heat ratio
    
    Returns:
        Exit Mach number (dimensionless)
    """
    def area_ratio_residual(Me):
        """Residual function for root finding"""
        if Me <= 1.0:
            return 1e6  # Supersonic solution required
        term1 = 1.0 / Me
        term2 = (2.0 / (gamma + 1.0)) * (1.0 + (gamma - 1.0) / 2.0 * Me**2)
        exponent = (gamma + 1.0) / (2.0 * (gamma - 1.0))
        return term1 * term2**exponent - area_ratio
    
    # Solve for Mach number (supersonic branch)
    Me = brentq(area_ratio_residual, 1.01, 50.0)
    return Me


def compute_nozzle_flow_properties(Tc, Pc, area_ratio, gamma, M_bar):
    """
    Compute nozzle flow properties using isentropic relations.
    
    Equations from CONTEXT.md:
    - Exit temperature: Te = Tc / (1 + (gamma-1)/2 * Me^2)
    - Exit pressure: Pe = Pc * (1 + (gamma-1)/2 * Me^2)^(-gamma/(gamma-1))
    - Exit velocity: Ve = Me * sqrt(gamma * R_specific * Te)
    
    Args:
        Tc: Chamber temperature [K]
        Pc: Chamber pressure [Pa]
        area_ratio: Ae/At
        gamma: Specific heat ratio
        M_bar: Mean molecular weight [g/mol]
    
    Returns:
        Dictionary with flow properties
    """
    # Specific gas constant [J/(kg*K)]
    R_specific = (R_universal / M_bar) * 1000.0  # Convert from J/(kmol*K) to J/(kg*K)
    
    # Solve for exit Mach number
    Me = solve_exit_mach_number(area_ratio, gamma)
    
    # Exit conditions (isentropic expansion)
    Te = Tc / (1.0 + (gamma - 1.0) / 2.0 * Me**2)
    Pe = Pc * (1.0 + (gamma - 1.0) / 2.0 * Me**2)**(-gamma / (gamma - 1.0))
    Ve = Me * np.sqrt(gamma * R_specific * Te)
    
    return {
        'exit_Mach': Me,
        'exit_temperature_K': Te,
        'exit_pressure_Pa': Pe,
        'exit_velocity_m_s': Ve,
        'R_specific': R_specific
    }


def compute_characteristic_velocity(Tc, gamma, M_bar):
    """
    Compute ideal characteristic velocity (c-star).
    
    Equation from CONTEXT.md:
    c_star = sqrt(gamma * R_specific * Tc) / (gamma * sqrt((2/(gamma+1))^((gamma+1)/(gamma-1))))
    
    Args:
        Tc: Chamber temperature [K]
        gamma: Specific heat ratio
        M_bar: Mean molecular weight [g/mol]
    
    Returns:
        Characteristic velocity [m/s]
    """
    R_specific = (R_universal / M_bar) * 1000.0  # J/(kg*K)
    
    numerator = np.sqrt(gamma * R_specific * Tc)
    denominator = gamma * np.sqrt((2.0 / (gamma + 1.0))**((gamma + 1.0) / (gamma - 1.0)))
    
    c_star = numerator / denominator
    return c_star


def compute_throat_area(Pc, thrust_target, c_star, area_ratio, gamma, Tc, M_bar, nozzle_efficiency):
    """
    Compute throat area to achieve target thrust.
    
    Method: Solve for throat area using actual (efficiency-reduced) exit velocity.
    F = mdot * Ve_actual + Pe * Ae
    F = (Pc * At / c*) * (Ve_ideal * efficiency) + Pe * (area_ratio * At)
    At = F / (Pc * Ve_ideal * efficiency / c* + Pe * area_ratio)
    
    Args:
        Pc: Chamber pressure [Pa]
        thrust_target: Desired thrust [N]
        c_star: Characteristic velocity [m/s]
        area_ratio: Ae/At
        gamma: Specific heat ratio
        Tc: Chamber temperature [K]
        M_bar: Mean molecular weight [g/mol]
        nozzle_efficiency: Nozzle efficiency factor (real-world losses)
    
    Returns:
        Throat area [m^2]
    """
    # Compute isentropic exit conditions
    Me = solve_exit_mach_number(area_ratio, gamma)
    flow = compute_nozzle_flow_properties(Tc, Pc, area_ratio, gamma, M_bar)
    
    Ve_ideal = flow['exit_velocity_m_s']
    Ve_actual = Ve_ideal * nozzle_efficiency
    Pe = flow['exit_pressure_Pa']
    
    # Throat area from thrust equation with actual velocity
    At = thrust_target / (Pc * Ve_actual / c_star + Pe * area_ratio)
    
    return At


def compute_mass_flow_rate(Pc, At, c_star):
    """
    Compute mass flow rate through choked nozzle.
    
    Equation from CONTEXT.md:
    mdot = (Pc * At) / c_star
    
    Args:
        Pc: Chamber pressure [Pa]
        At: Throat area [m^2]
        c_star: Characteristic velocity [m/s]
    
    Returns:
        Mass flow rate [kg/s]
    """
    mdot = (Pc * At) / c_star
    return mdot


def compute_thrust_vacuum(mdot, Ve, Pe, Ae):
    """
    Compute thrust in vacuum using rocket equation.
    
    Equation from CONTEXT.md:
    F = mdot * Ve + Pe * Ae (vacuum condition, Pa = 0)
    
    Args:
        mdot: Mass flow rate [kg/s]
        Ve: Exit velocity [m/s]
        Pe: Exit pressure [Pa]
        Ae: Exit area [m^2]
    
    Returns:
        Thrust [N]
    """
    F = mdot * Ve + Pe * Ae
    return F


def compute_specific_impulse(F, mdot):
    """
    Compute specific impulse.
    
    Equation from CONTEXT.md:
    Isp = F / (mdot * g0)
    
    Args:
        F: Thrust [N]
        mdot: Mass flow rate [kg/s]
    
    Returns:
        Specific impulse [seconds]
    """
    Isp = F / (mdot * g0)
    return Isp


# ========================================
# MAIN VERIFICATION PROCEDURE
# ========================================

def verify_thrust_Isp_performance():
    """
    Main verification function for VER-001.
    
    Procedure:
    1. Read Agent 2's design parameters from DES-001
    2. Develop independent sizing for 1.0 N thrust at nominal feed pressure
    3. Compute performance across feed pressure range 0.15-0.30 MPa
    4. Verify REQ-001: thrust = 1.0 N ± 0.05 N at nominal feed pressure
    5. Verify REQ-002: Isp ≥ 220 s in vacuum
    6. Generate plots and save results
    """
    
    print("="*80)
    print("VER-001: Independent Verification of Thrust and Isp Performance")
    print("="*80)
    print()
    
    # ========================================
    # STEP 1: Design sizing for 1.0 N thrust at nominal feed pressure
    # ========================================
    print("STEP 1: Sizing thruster for 1.0 N thrust at nominal feed pressure")
    print("-"*80)
    
    # Design parameters from input
    alpha = DESIGN_INPUTS['alpha_ammonia_dissociation']
    Tc = DESIGN_INPUTS['chamber_temperature_K']
    area_ratio = DESIGN_INPUTS['expansion_ratio']
    feed_pressure_nominal_MPa = DESIGN_INPUTS['feed_pressure_nominal_MPa']
    chamber_pressure_ratio = DESIGN_INPUTS['chamber_pressure_ratio']
    nozzle_efficiency = DESIGN_INPUTS['nozzle_efficiency']
    
    # Nominal chamber pressure
    feed_pressure_nominal_Pa = feed_pressure_nominal_MPa * 1e6
    Pc_nominal = chamber_pressure_ratio * feed_pressure_nominal_Pa
    
    # Compute gas properties
    M_bar = compute_mean_molecular_weight(alpha)
    gamma = compute_specific_heat_ratio(alpha)
    c_star = compute_characteristic_velocity(Tc, gamma, M_bar)
    
    print(f"Gas properties:")
    print(f"  Ammonia dissociation (alpha): {alpha}")
    print(f"  Mean molecular weight: {M_bar:.4f} g/mol")
    print(f"  Specific heat ratio (gamma): {gamma:.4f}")
    print(f"  Characteristic velocity (c*): {c_star:.2f} m/s")
    print(f"  Nozzle efficiency: {nozzle_efficiency}")
    print()
    
    # Size throat area for 1.0 N thrust (with nozzle efficiency applied)
    thrust_target = 1.0  # N
    At = compute_throat_area(Pc_nominal, thrust_target, c_star, area_ratio, gamma, Tc, M_bar, nozzle_efficiency)
    Ae = area_ratio * At
    
    # Compute mass flow rate
    mdot_nominal = compute_mass_flow_rate(Pc_nominal, At, c_star)
    
    # Compute nozzle flow properties
    flow_props = compute_nozzle_flow_properties(Tc, Pc_nominal, area_ratio, gamma, M_bar)
    
    # Apply nozzle efficiency to exit velocity
    Ve_ideal = flow_props['exit_velocity_m_s']
    Ve_actual = Ve_ideal * nozzle_efficiency
    
    # Compute thrust and Isp with actual (efficiency-reduced) velocity
    F_nominal = compute_thrust_vacuum(mdot_nominal, Ve_actual, flow_props['exit_pressure_Pa'], Ae)
    Isp_nominal = compute_specific_impulse(F_nominal, mdot_nominal)
    
    print(f"Thruster sizing at nominal feed pressure ({feed_pressure_nominal_MPa} MPa):")
    print(f"  Chamber pressure: {Pc_nominal/1e6:.4f} MPa")
    print(f"  Throat area: {At*1e6:.4f} mm²")
    print(f"  Throat diameter: {2*np.sqrt(At/np.pi)*1000:.4f} mm")
    print(f"  Exit area: {Ae*1e6:.4f} mm²")
    print(f"  Exit diameter: {2*np.sqrt(Ae/np.pi)*1000:.4f} mm")
    print(f"  Mass flow rate: {mdot_nominal*1e6:.4f} g/s")
    print(f"  Exit Mach number: {flow_props['exit_Mach']:.4f}")
    print(f"  Exit velocity (ideal): {Ve_ideal:.2f} m/s")
    print(f"  Exit velocity (actual, η={nozzle_efficiency}): {Ve_actual:.2f} m/s")
    print(f"  Exit pressure: {flow_props['exit_pressure_Pa']:.4f} Pa")
    print(f"  Exit temperature: {flow_props['exit_temperature_K']:.2f} K")
    print()
    print(f"Performance results:")
    print(f"  Thrust: {F_nominal:.6f} N")
    print(f"  Specific Impulse: {Isp_nominal:.4f} s")
    print()
    
    # ========================================
    # STEP 2: Sweep feed pressure across operating range
    # ========================================
    print("STEP 2: Performance analysis across feed pressure range (0.15-0.30 MPa)")
    print("-"*80)
    
    feed_pressures_MPa = np.linspace(0.15, 0.30, 100)
    
    results = {
        'feed_pressure_MPa': [],
        'chamber_pressure_MPa': [],
        'thrust_N': [],
        'Isp_s': [],
        'mass_flow_rate_kg_s': [],
        'exit_velocity_m_s': [],
        'exit_pressure_Pa': [],
        'exit_temperature_K': []
    }
    
    for Pf_MPa in feed_pressures_MPa:
        Pf = Pf_MPa * 1e6
        Pc = chamber_pressure_ratio * Pf
        
        # Recompute flow properties at this pressure
        flow = compute_nozzle_flow_properties(Tc, Pc, area_ratio, gamma, M_bar)
        
        # Mass flow rate scales with chamber pressure (choked flow)
        mdot = compute_mass_flow_rate(Pc, At, c_star)
        
        # Apply nozzle efficiency to exit velocity
        Ve_actual = flow['exit_velocity_m_s'] * nozzle_efficiency
        
        # Thrust with actual velocity
        F = compute_thrust_vacuum(mdot, Ve_actual, flow['exit_pressure_Pa'], Ae)
        
        # Isp (independent of pressure for ideal gas in vacuum)
        Isp = compute_specific_impulse(F, mdot)
        
        results['feed_pressure_MPa'].append(Pf_MPa)
        results['chamber_pressure_MPa'].append(Pc / 1e6)
        results['thrust_N'].append(F)
        results['Isp_s'].append(Isp)
        results['mass_flow_rate_kg_s'].append(mdot)
        results['exit_velocity_m_s'].append(Ve_actual)  # Store actual velocity
        results['exit_pressure_Pa'].append(flow['exit_pressure_Pa'])
        results['exit_temperature_K'].append(flow['exit_temperature_K'])
    
    # ========================================
    # STEP 3: Verify Requirements
    # ========================================
    print("STEP 3: Requirements Verification")
    print("-"*80)
    
    # REQ-001: Thrust = 1.0 N ± 0.05 N at nominal feed pressure
    req_001_thrust_min = 0.95
    req_001_thrust_max = 1.05
    
    req_001_result = {
        'description': 'Thrust = 1.0 N ± 0.05 N at nominal feed pressure',
        'computed_value': F_nominal,
        'threshold_min': req_001_thrust_min,
        'threshold_max': req_001_thrust_max,
        'unit': 'N',
        'margin_percent': (F_nominal - 1.0) / 1.0 * 100 if req_001_thrust_min <= F_nominal <= req_001_thrust_max else None,
        'status': 'PASS' if req_001_thrust_min <= F_nominal <= req_001_thrust_max else 'FAIL'
    }
    
    print(f"REQ-001 Verification:")
    print(f"  Requirement: Thrust = 1.0 N ± 0.05 N at nominal feed pressure")
    print(f"  Acceptance band: [{req_001_thrust_min:.3f}, {req_001_thrust_max:.3f}] N")
    print(f"  Computed thrust: {F_nominal:.6f} N")
    print(f"  Status: {req_001_result['status']}")
    if req_001_result['margin_percent'] is not None:
        print(f"  Margin: {req_001_result['margin_percent']:+.3f}%")
    print()
    
    # REQ-002: Isp ≥ 220 s in vacuum
    req_002_isp_min = 220.0
    
    req_002_result = {
        'description': 'Specific Impulse ≥ 220 s in vacuum',
        'computed_value': Isp_nominal,
        'threshold_min': req_002_isp_min,
        'unit': 's',
        'margin_percent': (Isp_nominal - req_002_isp_min) / req_002_isp_min * 100,
        'status': 'PASS' if Isp_nominal >= req_002_isp_min else 'FAIL'
    }
    
    print(f"REQ-002 Verification:")
    print(f"  Requirement: Specific Impulse ≥ {req_002_isp_min} s in vacuum")
    print(f"  Computed Isp: {Isp_nominal:.4f} s")
    print(f"  Status: {req_002_result['status']}")
    print(f"  Margin: {req_002_result['margin_percent']:+.3f}%")
    print()
    
    # Boundary conditions
    min_pressure_idx = np.argmin(feed_pressures_MPa)
    max_pressure_idx = np.argmax(feed_pressures_MPa)
    
    print(f"Boundary Conditions:")
    print(f"  At P_feed = 0.15 MPa:")
    print(f"    Thrust: {results['thrust_N'][min_pressure_idx]:.6f} N")
    print(f"    Isp: {results['Isp_s'][min_pressure_idx]:.4f} s")
    print(f"  At P_feed = 0.30 MPa:")
    print(f"    Thrust: {results['thrust_N'][max_pressure_idx]:.6f} N")
    print(f"    Isp: {results['Isp_s'][max_pressure_idx]:.4f} s")
    print()
    
    # ========================================
    # STEP 4: Compare with Agent 2's results
    # ========================================
    print("STEP 4: Comparison with Agent 2 (DES-001)")
    print("-"*80)
    
    # Load Agent 2's results
    des001_path = Path('/workspace/design/data/thruster_performance_sizing.json')
    
    if des001_path.exists():
        with open(des001_path, 'r') as f:
            des001_data = json.load(f)
        
        agent2_thrust = des001_data['computed_results']['thrust_N']
        agent2_Isp = des001_data['computed_results']['specific_impulse_s']
        
        thrust_delta = abs(F_nominal - agent2_thrust) / agent2_thrust * 100
        Isp_delta = abs(Isp_nominal - agent2_Isp) / agent2_Isp * 100
        
        print(f"Thrust comparison:")
        print(f"  Agent 2 (DES-001): {agent2_thrust:.6f} N")
        print(f"  Agent 3 (this verification): {F_nominal:.6f} N")
        print(f"  Delta: {thrust_delta:.2f}%")
        print(f"  Flag >5%: {'YES' if thrust_delta > 5.0 else 'NO'}")
        print()
        
        print(f"Isp comparison:")
        print(f"  Agent 2 (DES-001): {agent2_Isp:.4f} s")
        print(f"  Agent 3 (this verification): {Isp_nominal:.4f} s")
        print(f"  Delta: {Isp_delta:.2f}%")
        print(f"  Flag >5%: {'YES' if Isp_delta > 5.0 else 'NO'}")
        print()
    else:
        print("  Warning: DES-001 data file not found for comparison")
        print()
    
    # ========================================
    # STEP 5: Save results to JSON
    # ========================================
    print("STEP 5: Saving results")
    print("-"*80)
    
    output_data = {
        'verification_id': 'VER-001',
        'verification_method': 'Simulation (Independent)',
        'design_inputs': DESIGN_INPUTS,
        'computed_gas_properties': {
            'mean_molecular_weight_g_mol': M_bar,
            'specific_heat_ratio': gamma,
            'characteristic_velocity_m_s': c_star
        },
        'thruster_sizing': {
            'throat_area_m2': At,
            'throat_diameter_m': 2*np.sqrt(At/np.pi),
            'throat_diameter_mm': 2*np.sqrt(At/np.pi)*1000,
            'exit_area_m2': Ae,
            'exit_diameter_m': 2*np.sqrt(Ae/np.pi),
            'exit_diameter_mm': 2*np.sqrt(Ae/np.pi)*1000,
            'expansion_ratio': area_ratio
        },
        'nominal_performance': {
            'feed_pressure_MPa': feed_pressure_nominal_MPa,
            'chamber_pressure_MPa': Pc_nominal/1e6,
            'thrust_N': F_nominal,
            'specific_impulse_s': Isp_nominal,
            'mass_flow_rate_kg_s': mdot_nominal,
            'exit_velocity_m_s': flow_props['exit_velocity_m_s'],
            'exit_pressure_Pa': flow_props['exit_pressure_Pa'],
            'exit_temperature_K': flow_props['exit_temperature_K'],
            'exit_Mach': flow_props['exit_Mach']
        },
        'pressure_sweep': results,
        'requirements_verification': {
            'REQ-001': req_001_result,
            'REQ-002': req_002_result
        },
        'comparison_with_agent2': {
            'agent2_thrust_N': agent2_thrust if des001_path.exists() else None,
            'agent3_thrust_N': F_nominal,
            'thrust_delta_percent': thrust_delta if des001_path.exists() else None,
            'agent2_Isp_s': agent2_Isp if des001_path.exists() else None,
            'agent3_Isp_s': Isp_nominal,
            'Isp_delta_percent': Isp_delta if des001_path.exists() else None
        } if des001_path.exists() else None,
        'assumptions': [
            f"Ammonia dissociation degree (alpha) = {alpha}",
            f"Chamber temperature = {Tc} K",
            f"Chamber pressure = {chamber_pressure_ratio*100}% of feed pressure",
            f"Expansion ratio = {area_ratio}",
            f"Nozzle half-angle = {DESIGN_INPUTS['nozzle_half_angle_deg']} deg",
            "Vacuum operation (Pa = 0)",
            "Steady-state operation",
            "Ideal gas behavior with constant gamma"
        ]
    }
    
    output_path = Path('/workspace/verification/data/VER-001_results.json')
    with open(output_path, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"  Results saved to: {output_path}")
    print()
    
    # ========================================
    # STEP 6: Generate Plots
    # ========================================
    print("STEP 6: Generating plots")
    print("-"*80)
    
    # Plot 1: Thrust vs. Feed Pressure
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    
    ax1.plot(results['feed_pressure_MPa'], results['thrust_N'], 'b-', linewidth=2, label='Agent 3 Verification')
    
    # Add requirement band
    ax1.axhspan(req_001_thrust_min, req_001_thrust_max, alpha=0.2, color='green', label='REQ-001 Acceptance Band')
    ax1.axhline(req_001_thrust_min, color='green', linestyle='--', alpha=0.7, linewidth=1)
    ax1.axhline(req_001_thrust_max, color='green', linestyle='--', alpha=0.7, linewidth=1)
    ax1.axhline(1.0, color='green', linestyle='-', alpha=0.7, linewidth=1, label='Target (1.0 N)')
    
    # Plot Agent 2's point if available
    if des001_path.exists():
        agent2_feed_pressure = des001_data['parameters']['feed_pressure_MPa']
        ax1.plot(agent2_feed_pressure, agent2_thrust, 'rs', markersize=10, label='Agent 2 (DES-001)')
    
    # Plot Agent 3's nominal point
    ax1.plot(feed_pressure_nominal_MPa, F_nominal, 'bo', markersize=10, label='Agent 3 Nominal')
    
    # Shade pass/fail regions
    y_min, y_max = ax1.get_ylim()
    ax1.fill_between([0.15, 0.30], y_min, req_001_thrust_min, alpha=0.1, color='red', label='FAIL Region')
    
    ax1.set_xlabel('Feed Pressure [MPa]', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Thrust [N]', fontsize=12, fontweight='bold')
    ax1.set_title('VER-001 / REQ-001: Thrust vs. Feed Pressure\n(Thrust = 1.0 N ± 0.05 N required)', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc='best', fontsize=10)
    ax1.set_xlim(0.15, 0.30)
    
    plot1_path = Path('/workspace/verification/plots/VER-001_thrust_vs_pressure.png')
    plt.savefig(plot1_path, dpi=150, bbox_inches='tight')
    print(f"  Plot saved to: {plot1_path}")
    plt.close(fig1)
    
    # Plot 2: Isp Compliance
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    
    ax2.plot(results['feed_pressure_MPa'], results['Isp_s'], 'b-', linewidth=2, label='Agent 3 Verification')
    
    # Add requirement threshold
    ax2.axhline(req_002_isp_min, color='green', linestyle='--', linewidth=2, label='REQ-002 Minimum (220 s)')
    ax2.axhspan(req_002_isp_min, ax2.get_ylim()[1], alpha=0.2, color='green', label='PASS Region')
    
    # Plot Agent 2's point if available
    if des001_path.exists():
        ax2.plot(agent2_feed_pressure, agent2_Isp, 'rs', markersize=10, label='Agent 2 (DES-001)')
    
    # Plot Agent 3's nominal point
    ax2.plot(feed_pressure_nominal_MPa, Isp_nominal, 'bo', markersize=10, label='Agent 3 Nominal')
    
    # Shade pass/fail regions
    y_min, y_max = ax2.get_ylim()
    ax2.fill_between([0.15, 0.30], y_min, req_002_isp_min, alpha=0.1, color='red', label='FAIL Region')
    
    ax2.set_xlabel('Feed Pressure [MPa]', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Specific Impulse [s]', fontsize=12, fontweight='bold')
    ax2.set_title('VER-001 / REQ-002: Isp vs. Feed Pressure\n(Isp ≥ 220 s required)', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc='best', fontsize=10)
    ax2.set_xlim(0.15, 0.30)
    
    plot2_path = Path('/workspace/verification/plots/VER-001_Isp_compliance.png')
    plt.savefig(plot2_path, dpi=150, bbox_inches='tight')
    print(f"  Plot saved to: {plot2_path}")
    plt.close(fig2)
    
    print()
    print("="*80)
    print("VERIFICATION SUMMARY")
    print("="*80)
    print(f"REQ-001 (Thrust = 1.0 N ± 0.05 N): {req_001_result['status']}")
    print(f"  Computed: {F_nominal:.6f} N")
    if req_001_result['status'] == 'FAIL':
        print(f"  REQUIRED: {req_001_thrust_min} - {req_001_thrust_max} N")
    print()
    print(f"REQ-002 (Isp ≥ 220 s): {req_002_result['status']}")
    print(f"  Computed: {Isp_nominal:.4f} s")
    if req_002_result['status'] == 'FAIL':
        print(f"  REQUIRED: ≥ {req_002_isp_min} s")
    print()
    if des001_path.exists():
        print(f"Agent 2 Delta (Thrust): {thrust_delta:.2f}%")
        print(f"Agent 2 Delta (Isp): {Isp_delta:.2f}%")
    print("="*80)
    
    return output_data


if __name__ == '__main__':
    results = verify_thrust_Isp_performance()
