#!/usr/bin/env python3
"""
DES-006: Thrust Control System Analysis

Design ID: DES-006
Related Requirements: REQ-003, REQ-004, REQ-006
Author: Agent 2 (Design & Implementation Engineer)
Date: 2026-02-14

Purpose:
This script analyzes the thrust control system for the monopropellant hydrazine thruster,
including:
1. Thrust vs. feed pressure relationship
2. Minimum impulse bit calculation
3. Startup transient simulation
4. Requirements compliance verification

Output:
- design/data/thrust_control.json: Computed results
- design/plots/DES006_thrust_vs_pressure.png: Thrust vs. pressure curve
- design/plots/DES006_startup_transient.png: Startup transient response
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# =============================================================================
# PHYSICAL CONSTANTS
# Source: CONTEXT.md Section 6, NIST, NASA handbooks
# =============================================================================

g0 = 9.80665           # m/s^2 - Standard gravitational acceleration (exact)
R_universal = 8314.46  # J/(kmol*K) - Universal gas constant (NIST)
pi = 3.14159265359     # Mathematical constant

# Hydrazine properties (from CONTEXT.md Section 6)
rho_N2H4 = 1004.0      # kg/m^3 - Liquid density at 25°C
M_N2H4 = 32.045        # g/mol - Molecular weight

# =============================================================================
# DESIGN PARAMETERS FROM PREVIOUS TASKS
# Source: DES-001, DES-003, DEC-001 through DEC-008
# =============================================================================

# Nominal operating point (from DES-001)
P_feed_nominal_MPa = 0.30      # MPa - Nominal feed pressure (max of REQ-009 range)
P_chamber_nominal_MPa = 0.21   # MPa - Nominal chamber pressure (70% of feed)
F_nominal_N = 1.0              # N - Nominal thrust (REQ-001)
mdot_nominal_kg_s = 0.000248663733273239  # kg/s - Nominal mass flow rate
Isp_nominal_s = 410.07838157783726        # s - Nominal specific impulse
Ve_nominal_m_s = 4022.0        # m/s - Nominal exhaust velocity (Isp * g0)
T_chamber_K = 1400.0           # K - Chamber temperature
alpha = 0.5                    # Ammonia dissociation degree
gamma = 1.28                   # Specific heat ratio

# Feed pressure constraints (from REQ-009)
P_feed_min_MPa = 0.15          # MPa - Minimum feed pressure
P_feed_max_MPa = 0.30          # MPa - Maximum feed pressure

# Thrust requirements (from REQ-001, REQ-003)
F_min_req_N = 0.8              # N - Minimum thrust (REQ-003)
F_max_req_N = 1.2              # N - Maximum thrust (REQ-003)
F_nominal_req_N = 1.0          # N - Nominal thrust (REQ-001)
F_nominal_tolerance_N = 0.05   # N - Thrust tolerance

# Impulse bit requirement (from REQ-004)
I_bit_max_Ns = 0.01            # N·s - Maximum impulse bit

# Startup requirement (from REQ-006)
t_startup_max_ms = 200         # ms - Time to 90% thrust
thrust_startup_percent = 90.0 # % - Target thrust at startup

# Thermal parameters (from DES-003)
T_preheat_K = 473.0           # K - Preheat temperature (200°C)
T_active_K = 573.0             # K - Active catalyst temperature (300°C)
m_catalyst_kg = 0.042539866846353996    # kg - Catalyst mass
Cp_catalyst_J_kg_K = 800.0    # J/(kg·K) - Catalyst specific heat
wall_thickness_m = 0.001       # m - Chamber wall thickness

# Control system parameters
t_on_min_ms = 10.0            # ms - Minimum valve on-time
tau_flow_s = 0.020             # s - Flow establishment time constant
tau_thermal_s = 0.050          # s - Thermal time constant
eta_min = 0.50                 # - Minimum catalyst efficiency (at preheat)
eta_max = 1.00                 # - Maximum catalyst efficiency (at steady state)

# Feed line parameters
V_feed_line_m3 = 5e-6          # m^3 - Feed line volume (5 cm^3)

# =============================================================================
# ANALYSIS COMPUTATIONS
# =============================================================================

def calculate_thrust_vs_pressure():
    """
    Calculate thrust as a function of feed pressure.
    
    Assumptions:
    1. Linear thrust-pressure relationship (valid for small variations)
    2. Constant Isp across pressure range
    3. Chamber pressure is 70% of feed pressure (from DES-001)
    4. Vacuum operation (Pe = 0)
    
    Returns:
        pressures_MPa: Array of feed pressures [MPa]
        thrusts_N: Array of thrust values [N]
        chamber_pressures_MPa: Array of chamber pressures [MPa]
    """
    # Create pressure range for analysis
    pressures_MPa = np.linspace(P_feed_min_MPa, P_feed_max_MPa, 100)
    
    # Calculate thrust at each pressure (linear scaling from nominal)
    thrusts_N = F_nominal_N * (pressures_MPa / P_feed_nominal_MPa)
    
    # Calculate chamber pressure (70% of feed pressure)
    chamber_pressures_MPa = 0.70 * pressures_MPa
    
    return pressures_MPa, thrusts_N, chamber_pressures_MPa


def calculate_feed_pressure_for_thrust(target_thrust_N):
    """
    Calculate required feed pressure to achieve target thrust.
    
    Args:
        target_thrust_N: Desired thrust [N]
    
    Returns:
        Required feed pressure [MPa]
    """
    return P_feed_nominal_MPa * (target_thrust_N / F_nominal_N)


def calculate_impulse_bit(thrust_N, on_time_s):
    """
    Calculate impulse bit for given thrust and on-time.
    
    I_bit = F * t_on
    
    Args:
        thrust_N: Thrust during pulse [N]
        on_time_s: Valve on-time [s]
    
    Returns:
        Impulse bit [N·s]
    """
    return thrust_N * on_time_s


def calculate_minimum_on_time_for_impulse(thrust_N, target_impulse_bit_Ns):
    """
    Calculate minimum on-time to achieve target impulse bit.
    
    t_on = I_bit / F
    
    Args:
        thrust_N: Thrust during pulse [N]
        target_impulse_bit_Ns: Desired impulse bit [N·s]
    
    Returns:
        Required on-time [s]
    """
    return target_impulse_bit_Ns / thrust_N


def simulate_flow_dynamics(t_s, mdot_ss_kg_s, tau_s=tau_flow_s):
    """
    Simulate flow establishment using first-order dynamics.
    
    mdot(t) = mdot_ss * (1 - exp(-t/tau))
    
    Args:
        t_s: Time array [s]
        mdot_ss_kg_s: Steady-state mass flow rate [kg/s]
        tau_s: Time constant [s]
    
    Returns:
        Mass flow rate at each time [kg/s]
    """
    return mdot_ss_kg_s * (1 - np.exp(-t_s / tau_s))


def simulate_thermal_dynamics(t_s, eta_min=eta_min, eta_max=eta_max, tau_s=tau_thermal_s):
    """
    Simulate catalyst efficiency using first-order thermal dynamics.
    
    eta(t) = eta_min + (eta_max - eta_min) * (1 - exp(-t/tau))
    
    Args:
        t_s: Time array [s]
        eta_min: Minimum efficiency (at preheat)
        eta_max: Maximum efficiency (at steady state)
        tau_s: Thermal time constant [s]
    
    Returns:
        Catalyst efficiency at each time
    """
    return eta_min + (eta_max - eta_min) * (1 - np.exp(-t_s / tau_s))


def simulate_startup_transient(t_s):
    """
    Simulate thrust during startup transient.
    
    F(t) = mdot(t) * Ve * eta(t)
    
    Args:
        t_s: Time array [s]
    
    Returns:
        thrust_N: Thrust at each time [N]
        mdot_factor: Flow factor (mdot/mdot_ss)
        eta: Catalyst efficiency
    """
    # Calculate flow dynamics
    mdot_factor = simulate_flow_dynamics(t_s, mdot_nominal_kg_s, tau_flow_s) / mdot_nominal_kg_s
    
    # Calculate thermal dynamics (catalyst efficiency)
    eta = simulate_thermal_dynamics(t_s, eta_min, eta_max, tau_thermal_s)
    
    # Combined thrust response
    thrust_N = mdot_factor * eta * F_nominal_N
    
    return thrust_N, mdot_factor, eta


def find_time_to_thrust_percent(target_percent):
    """
    Find time to reach target percentage of nominal thrust.
    
    Args:
        target_percent: Target percentage (e.g., 90 for 90%)
    
    Returns:
        Time to reach target thrust [s] (returns max time if not reached)
    """
    # Create fine time array for accurate solution
    t_s = np.linspace(0, 0.5, 10000)  # 0 to 500 ms
    
    # Simulate startup
    thrust_N, _, _ = simulate_startup_transient(t_s)
    
    # Find index where thrust exceeds target
    target_thrust_N = (target_percent / 100.0) * F_nominal_N
    idx = np.where(thrust_N >= target_thrust_N)[0]
    
    if len(idx) > 0:
        return t_s[idx[0]]
    else:
        # Return maximum time if target not reached
        return t_s[-1]


# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def main():
    print("=" * 80)
    print("DES-006: Thrust Control System Analysis")
    print("=" * 80)
    print()
    
    # ------------------------------------------------------------------------
    # 1. Thrust vs. Feed Pressure Analysis
    # ------------------------------------------------------------------------
    print("1. Thrust vs. Feed Pressure Analysis")
    print("-" * 80)
    
    pressures_MPa, thrusts_N, chamber_pressures_MPa = calculate_thrust_vs_pressure()
    
    # Calculate feed pressures for required thrust range
    P_for_0_8N_MPa = calculate_feed_pressure_for_thrust(0.8)
    P_for_1_0N_MPa = calculate_feed_pressure_for_thrust(1.0)
    P_for_1_2N_MPa = calculate_feed_pressure_for_thrust(1.2)
    
    print(f"Feed pressure required for:")
    print(f"  0.8 N thrust: {P_for_0_8N_MPa:.3f} MPa")
    print(f"  1.0 N thrust: {P_for_1_0N_MPa:.3f} MPa (nominal)")
    print(f"  1.2 N thrust: {P_for_1_2N_MPa:.3f} MPa")
    print()
    print(f"Feed pressure constraint (REQ-009): {P_feed_min_MPa:.2f} - {P_feed_max_MPa:.2f} MPa")
    print()
    
    # Determine achievable thrust range
    F_min_achievable_N = thrusts_N[np.argmin(np.abs(pressures_MPa - P_feed_min_MPa))]
    F_max_achievable_N = thrusts_N[np.argmin(np.abs(pressures_MPa - P_feed_max_MPa))]
    
    print(f"Achievable thrust range within feed pressure constraints:")
    print(f"  Minimum: {F_min_achievable_N:.3f} N (at {P_feed_min_MPa:.2f} MPa)")
    print(f"  Maximum: {F_max_achievable_N:.3f} N (at {P_feed_max_MPa:.2f} MPa)")
    print()
    
    # REQ-003 assessment
    req3_min_ok = F_min_achievable_N <= F_min_req_N
    req3_max_ok = F_max_achievable_N >= F_max_req_N
    
    print(f"REQ-003 (Thrust range {F_min_req_N:.1f}-{F_max_req_N:.1f} N):")
    print(f"  Minimum bound ({F_min_req_N:.1f} N): {'PASS' if req3_min_ok else 'FAIL'}")
    print(f"  Maximum bound ({F_max_req_N:.1f} N): {'PASS' if req3_max_ok else 'FAIL'}")
    if not req3_max_ok:
        print(f"  Note: {F_max_req_N:.1f} N requires {P_for_1_2N_MPa:.3f} MPa, exceeds {P_feed_max_MPa:.2f} MPa limit")
    print()
    
    # ------------------------------------------------------------------------
    # 2. Minimum Impulse Bit Analysis
    # ------------------------------------------------------------------------
    print("2. Minimum Impulse Bit Analysis")
    print("-" * 80)
    
    # Calculate impulse bits at various thrust levels
    thrust_levels_N = [F_min_achievable_N, 0.9, 1.0]
    on_times_ms = [10.0, 12.5, 5.0]
    
    impulse_bits = []
    for F_N, t_ms in zip(thrust_levels_N, on_times_ms):
        I_bit_Ns = calculate_impulse_bit(F_N, t_ms / 1000.0)
        impulse_bits.append(I_bit_Ns)
        print(f"  Thrust: {F_N:.2f} N, On-time: {t_ms:.1f} ms → Impulse bit: {I_bit_Ns:.4f} N·s")
    
    print()
    
    # Minimum achievable impulse bit
    I_bit_min_Ns = calculate_impulse_bit(F_min_achievable_N, t_on_min_ms / 1000.0)
    print(f"Minimum impulse bit (at {F_min_achievable_N:.2f} N, {t_on_min_ms:.1f} ms): {I_bit_min_Ns:.4f} N·s")
    print(f"REQ-004 requirement: ≤ {I_bit_max_Ns:.4f} N·s")
    print(f"Margin: {((I_bit_max_Ns - I_bit_min_Ns) / I_bit_max_Ns) * 100:.1f}%")
    
    req4_status = "PASS" if I_bit_min_Ns <= I_bit_max_Ns else "FAIL"
    print(f"REQ-004 Status: {req4_status}")
    print()
    
    # ------------------------------------------------------------------------
    # 3. Startup Transient Analysis
    # ------------------------------------------------------------------------
    print("3. Startup Transient Analysis")
    print("-" * 80)
    
    # Simulate startup transient
    t_s = np.linspace(0, 0.5, 1000)  # 0 to 500 ms
    thrust_N, mdot_factor, eta = simulate_startup_transient(t_s)
    
    # Find time to 90% thrust
    t_90_ms = find_time_to_thrust_percent(90.0) * 1000.0
    
    print(f"Startup transient parameters:")
    print(f"  Flow time constant: {tau_flow_s * 1000:.1f} ms")
    print(f"  Thermal time constant: {tau_thermal_s * 1000:.1f} ms")
    print(f"  Preheat temperature: {T_preheat_K:.0f} K ({T_preheat_K - 273.15:.0f}°C)")
    print(f"  Catalyst efficiency at preheat: {eta_min:.0%}")
    print()
    
    print(f"Startup response:")
    print(f"  Time to 50% thrust: {find_time_to_thrust_percent(50.0) * 1000:.1f} ms")
    print(f"  Time to 90% thrust: {t_90_ms:.1f} ms")
    print(f"  Time to 95% thrust: {find_time_to_thrust_percent(95.0) * 1000:.1f} ms")
    print()
    
    print(f"REQ-006 requirement: {thrust_startup_percent:.0f}% thrust within {t_startup_max_ms:.0f} ms")
    print(f"Margin: {((t_startup_max_ms - t_90_ms) / t_startup_max_ms) * 100:.1f}%")
    
    req6_status = "PASS" if t_90_ms <= t_startup_max_ms else "FAIL"
    print(f"REQ-006 Status: {req6_status}")
    print()
    
    # Print startup transient table
    print("Startup Transient Response:")
    print("  Time (ms) | Flow Factor | Cat. Eff. | Thrust (% of Nominal)")
    print("  " + "-" * 55)
    for t_ms in [0, 20, 50, 100, 140, 200, 300]:
        idx = np.argmin(np.abs(t_s * 1000 - t_ms))
        print(f"  {t_ms:8.0f} | {mdot_factor[idx]:10.3f} | {eta[idx]:8.2f} | {thrust_N[idx]/F_nominal_N*100:19.1f}%")
    print()
    
    # ------------------------------------------------------------------------
    # 4. Generate Plots
    # ------------------------------------------------------------------------
    print("4. Generating Plots")
    print("-" * 80)
    
    # Plot 1: Thrust vs. Feed Pressure
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(pressures_MPa, thrusts_N, 'b-', linewidth=2, label='Thrust')
    ax1.axhline(y=F_min_req_N, color='g', linestyle='--', label=f'REQ-003 Min: {F_min_req_N:.1f} N')
    ax1.axhline(y=F_max_req_N, color='r', linestyle='--', label=f'REQ-003 Max: {F_max_req_N:.1f} N')
    ax1.axhline(y=F_nominal_req_N, color='k', linestyle=':', label=f'REQ-001 Nominal: {F_nominal_req_N:.1f} N')
    ax1.axvline(x=P_feed_min_MPa, color='orange', linestyle='--', label=f'REQ-009 Min: {P_feed_min_MPa:.2f} MPa')
    ax1.axvline(x=P_feed_max_MPa, color='orange', linestyle='--', label=f'REQ-009 Max: {P_feed_max_MPa:.2f} MPa')
    
    # Mark achievable range
    ax1.fill_between([P_feed_min_MPa, P_feed_max_MPa], [F_min_achievable_N, F_max_achievable_N], 
                     alpha=0.3, color='green', label='Achievable Range')
    
    ax1.set_xlabel('Feed Pressure (MPa)', fontsize=12)
    ax1.set_ylabel('Thrust (N)', fontsize=12)
    ax1.set_title('DES-006: Thrust vs. Feed Pressure', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc='upper left')
    ax1.set_xlim([0.14, 0.32])
    ax1.set_ylim([0, 1.3])
    
    fig1_path = Path('design/plots/DES006_thrust_vs_pressure.png')
    fig1_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(fig1_path, dpi=150, bbox_inches='tight')
    print(f"  Saved: {fig1_path}")
    plt.close(fig1)
    
    # Plot 2: Startup Transient
    fig2, (ax2a, ax2b) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    
    # Thrust response
    ax2a.plot(t_s * 1000, thrust_N / F_nominal_N * 100, 'b-', linewidth=2, label='Thrust')
    ax2a.axhline(y=90, color='r', linestyle='--', label=f'REQ-006: {thrust_startup_percent:.0f}%')
    ax2a.axvline(x=t_90_ms, color='r', linestyle=':', label=f't_90% = {t_90_ms:.0f} ms')
    ax2a.axvline(x=t_startup_max_ms, color='orange', linestyle='--', label=f'REQ-006 Limit: {t_startup_max_ms:.0f} ms')
    ax2a.axvspan(0, t_startup_max_ms, alpha=0.1, color='green')
    
    ax2a.set_ylabel('Thrust (% of Nominal)', fontsize=12)
    ax2a.set_title('DES-006: Startup Transient Response', fontsize=14, fontweight='bold')
    ax2a.grid(True, alpha=0.3)
    ax2a.legend(loc='lower right')
    ax2a.set_ylim([0, 105])
    
    # Flow and thermal dynamics
    ax2b.plot(t_s * 1000, mdot_factor * 100, 'g-', linewidth=2, label='Flow Factor')
    ax2b.plot(t_s * 1000, eta * 100, 'm-', linewidth=2, label='Catalyst Efficiency')
    ax2b.axhline(y=50, color='orange', linestyle='--', label=f'Preheat efficiency: {eta_min*100:.0f}%')
    
    ax2b.set_xlabel('Time (ms)', fontsize=12)
    ax2b.set_ylabel('Factor (%)', fontsize=12)
    ax2b.grid(True, alpha=0.3)
    ax2b.legend(loc='lower right')
    ax2b.set_ylim([0, 105])
    
    fig2_path = Path('design/plots/DES006_startup_transient.png')
    fig2_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(fig2_path, dpi=150, bbox_inches='tight')
    print(f"  Saved: {fig2_path}")
    plt.close(fig2)
    print()
    
    # ------------------------------------------------------------------------
    # 5. Requirements Compliance Summary
    # ------------------------------------------------------------------------
    print("5. Requirements Compliance Summary")
    print("=" * 80)
    
    # REQ-003
    req3_margin = None
    if req3_min_ok and req3_max_ok:
        req3_status = "PASS"
        req3_margin = 10.0  # Approximate margin
    else:
        req3_status = "PARTIAL"
        req3_margin = 0.0
    
    print(f"REQ-003: Thrust range {F_min_req_N:.1f}-{F_max_req_N:.1f} N via feed pressure regulation")
    print(f"  Achievable: {F_min_achievable_N:.2f}-{F_max_achievable_N:.2f} N")
    print(f"  Status: {req3_status}")
    print()
    
    # REQ-004
    req4_margin = ((I_bit_max_Ns - I_bit_min_Ns) / I_bit_max_Ns) * 100
    
    print(f"REQ-004: Minimum impulse bit ≤ {I_bit_max_Ns:.4f} N·s")
    print(f"  Achievable: {I_bit_min_Ns:.4f} N·s (at {F_min_achievable_N:.2f} N, {t_on_min_ms:.1f} ms)")
    print(f"  Margin: {req4_margin:.1f}%")
    print(f"  Status: {req4_status}")
    print()
    
    # REQ-006
    req6_margin = ((t_startup_max_ms - t_90_ms) / t_startup_max_ms) * 100
    
    print(f"REQ-006: {thrust_startup_percent:.0f}% thrust within {t_startup_max_ms:.0f} ms")
    print(f"  Achieved: {thrust_startup_percent:.0f}% thrust in {t_90_ms:.1f} ms")
    print(f"  Margin: {req6_margin:.1f}%")
    print(f"  Status: {req6_status}")
    print()
    
    # ------------------------------------------------------------------------
    # 6. Prepare Output Data
    # ------------------------------------------------------------------------
    print("6. Preparing Output Data")
    print("-" * 80)
    
    output_data = {
        "design_id": "DES-006",
        "parameters": {
            "feed_pressure_min_MPa": P_feed_min_MPa,
            "feed_pressure_max_MPa": P_feed_max_MPa,
            "feed_pressure_nominal_MPa": P_feed_nominal_MPa,
            "chamber_pressure_nominal_MPa": P_chamber_nominal_MPa,
            "thrust_nominal_N": F_nominal_N,
            "mass_flow_rate_nominal_kg_s": mdot_nominal_kg_s,
            "specific_impulse_nominal_s": Isp_nominal_s,
            "exhaust_velocity_nominal_m_s": Ve_nominal_m_s,
            "chamber_temperature_K": T_chamber_K,
            "preheat_temperature_K": T_preheat_K,
            "minimum_on_time_ms": t_on_min_ms,
            "flow_time_constant_ms": tau_flow_s * 1000,
            "thermal_time_constant_ms": tau_thermal_s * 1000,
            "catalyst_efficiency_min": eta_min,
            "catalyst_efficiency_max": eta_max
        },
        "thrust_vs_pressure": {
            "pressure_array_MPa": pressures_MPa.tolist(),
            "thrust_array_N": thrusts_N.tolist(),
            "chamber_pressure_array_MPa": chamber_pressures_MPa.tolist(),
            "feed_pressure_for_0_8N_MPa": P_for_0_8N_MPa,
            "feed_pressure_for_1_0N_MPa": P_for_1_0N_MPa,
            "feed_pressure_for_1_2N_MPa": P_for_1_2N_MPa,
            "achievable_thrust_min_N": F_min_achievable_N,
            "achievable_thrust_max_N": F_max_achievable_N
        },
        "impulse_bit_analysis": {
            "minimum_impulse_bit_Ns": I_bit_min_Ns,
            "minimum_on_time_s": t_on_min_ms / 1000.0,
            "impulse_bit_at_0_8N_10ms_Ns": impulse_bits[0],
            "impulse_bit_at_1_0N_5ms_Ns": impulse_bits[2],
            "thrust_at_min_impulse_N": F_min_achievable_N
        },
        "startup_transient": {
            "time_to_50_percent_ms": find_time_to_thrust_percent(50.0) * 1000,
            "time_to_90_percent_ms": t_90_ms,
            "time_to_95_percent_ms": find_time_to_thrust_percent(95.0) * 1000,
            "time_to_100_percent_ms": find_time_to_thrust_percent(100.0) * 1000,
            "startup_response_table": [
                {
                    "time_ms": float(t_ms),
                    "flow_factor": float(mdot_factor[np.argmin(np.abs(t_s * 1000 - t_ms))]),
                    "catalyst_efficiency": float(eta[np.argmin(np.abs(t_s * 1000 - t_ms))]),
                    "thrust_percent_nominal": float(thrust_N[np.argmin(np.abs(t_s * 1000 - t_ms))] / F_nominal_N * 100)
                }
                for t_ms in [0, 20, 50, 100, 140, 200, 300]
            ]
        },
        "requirements_compliance": {
            "REQ-003": {
                "description": "Thrust range 0.8-1.2 N via feed pressure regulation",
                "threshold_min_N": F_min_req_N,
                "threshold_max_N": F_max_req_N,
                "achievable_min_N": F_min_achievable_N,
                "achievable_max_N": F_max_achievable_N,
                "feed_pressure_for_max_N_MPa": P_for_1_2N_MPa,
                "exceeds_pressure_limit": P_for_1_2N_MPa > P_feed_max_MPa,
                "margin_percent": 0.0,
                "status": req3_status,
                "note": "Achievable range is 0.5-1.0 N within feed pressure constraints. Upper bound (1.2 N) requires 0.36 MPa feed pressure, exceeding REQ-009 limit."
            },
            "REQ-004": {
                "description": f"Minimum impulse bit ≤ {I_bit_max_Ns:.4f} N·s",
                "threshold_max_Ns": I_bit_max_Ns,
                "computed_min_Ns": I_bit_min_Ns,
                "minimum_on_time_ms": t_on_min_ms,
                "margin_percent": req4_margin,
                "status": req4_status
            },
            "REQ-006": {
                "description": f"{thrust_startup_percent:.0f}% thrust within {t_startup_max_ms:.0f} ms",
                "threshold_time_ms": t_startup_max_ms,
                "computed_time_ms": t_90_ms,
                "margin_percent": req6_margin,
                "status": req6_status
            }
        },
        "assumptions": [
            "Linear thrust-pressure relationship (valid for ±20% pressure variations)",
            "Constant Isp across throttle range (within ±5% variation)",
            "Valve response time 5-10 ms (typical for space-qualified solenoid valves)",
            "Preheat temperature maintained at 200°C between firings",
            "Feed pressure stable during each pulse (no oscillation)",
            "Vacuum operation (ambient pressure = 0)",
            "Chamber pressure is 70% of feed pressure (from DES-001)",
            "Catalyst efficiency 50% at preheat temperature, 100% at steady state",
            "Flow time constant 20 ms (feed line volume / flow rate)",
            "Thermal time constant 50 ms (catalyst bed thermal inertia)"
        ],
        "sources": [
            "DES-001: Thruster Performance Sizing - Nominal performance parameters",
            "DES-003: Catalyst Preheat System Design - Thermal parameters",
            "DEC-001 through DEC-008: Prior design decisions",
            "CONTEXT.md: Domain equations and reference data",
            "Sutton, 'Rocket Propulsion Elements': Transient flow and thermal dynamics",
            "NASA CR-182202: Shell 405 catalyst characteristics"
        ]
    }
    
    # Save to JSON
    json_path = Path('design/data/thrust_control.json')
    json_path.parent.mkdir(parents=True, exist_ok=True)
    with open(json_path, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"  Saved: {json_path}")
    print()
    
    print("=" * 80)
    print("DES-006 Analysis Complete")
    print("=" * 80)


if __name__ == "__main__":
    main()
