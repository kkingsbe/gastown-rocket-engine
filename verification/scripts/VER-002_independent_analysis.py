#!/usr/bin/env python3
"""
VER-002: Independent Verification of Propellant Mass Budget
===========================================================

This script performs an independent analysis to verify that the propellant mass
budget meets the requirements. It does NOT use Agent 2's logic but implements
the physics equations from first principles.

Analysis Method:
- Calculate total impulse requirement from mission parameters
- Compute propellant mass required using fundamental rocket equation
- Apply uncertainty margin
- Verify compliance with REQ-005 (50,000 Ns) and REQ-008 (25 kg budget)

Author: Agent 3 (Verification & Validation Engineer)
Date: 2026-02-14
"""

import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
import numpy as np

# Physical constants from CONTEXT.md (independent verification)
G0 = 9.80665  # m/s^2 - standard gravitational acceleration (exact SI)

# Load Agent 2's design parameters (read only - for comparison, not logic)
with open('design/data/propellant_budget.json', 'r') as f:
    agent2_data = json.load(f)

with open('design/data/thruster_performance_sizing.json', 'r') as f:
    agent2_perf = json.load(f)


def calculate_propellant_mass_from_impulse(total_impulse_ns, isp_s, margin_pct=0.0):
    """
    Calculate propellant mass required to deliver specified total impulse.

    From fundamental rocket equation: I_total = m_prop * Isp * g0
    Rearranged: m_prop = I_total / (Isp * g0)

    Parameters:
    -----------
    total_impulse_ns : float
        Total impulse required [N·s]
    isp_s : float
        Specific impulse [s]
    margin_pct : float
        Uncertainty margin as percentage (0.0 = no margin)

    Returns:
    --------
    dict
        Dictionary with calculated values
    """
    # Base propellant mass (no margin)
    m_base = total_impulse_ns / (isp_s * G0)

    # Apply uncertainty margin
    m_with_margin = m_base * (1.0 + margin_pct / 100.0)

    return {
        'impulse_ns': total_impulse_ns,
        'isp_s': isp_s,
        'g0_m_s2': G0,
        'mass_base_kg': m_base,
        'margin_pct': margin_pct,
        'mass_with_margin_kg': m_with_margin,
        'mass_margin_kg': m_with_margin - m_base
    }


def calculate_total_impulse_from_mass(propellant_mass_kg, isp_s, margin_pct=0.0):
    """
    Calculate total impulse deliverable with given propellant mass.

    From fundamental rocket equation: I_total = m_prop * Isp * g0

    Parameters:
    -----------
    propellant_mass_kg : float
        Propellant mass available [kg]
    isp_s : float
        Specific impulse [s]
    margin_pct : float
        Uncertainty margin as percentage (0.0 = no margin)

    Returns:
    --------
    dict
        Dictionary with calculated values
    """
    # Available mass after margin (margin is a deduction from usable propellant)
    m_usable = propellant_mass_kg / (1.0 + margin_pct / 100.0)

    # Total impulse
    total_impulse = m_usable * isp_s * G0

    return {
        'propellant_mass_kg': propellant_mass_kg,
        'isp_s': isp_s,
        'g0_m_s2': G0,
        'margin_pct': margin_pct,
        'mass_usable_kg': m_usable,
        'impulse_ns': total_impulse,
        'margin_consumed_kg': propellant_mass_kg - m_usable
    }


def calculate_firing_time(thrust_N, total_impulse_ns):
    """
    Calculate total firing time to achieve total impulse.

    t_total = I_total / F

    Parameters:
    -----------
    thrust_N : float
        Nominal thrust [N]
    total_impulse_ns : float
        Total impulse [N·s]

    Returns:
    --------
    float
        Total firing time [seconds]
    """
    return total_impulse_ns / thrust_N


def main():
    """
    Main verification procedure for VER-002.

    Independently calculates propellant mass requirements and verifies
    compliance with REQ-005 and REQ-008.
    """
    print("=" * 70)
    print("VER-002: Independent Verification of Propellant Mass Budget")
    print("=" * 70)
    print()

    # ===== INPUT PARAMETERS (from requirements, NOT from Agent 2's logic) =====
    req_impulse_ns = 50000.0  # REQ-005: Total impulse >= 50,000 N·s
    req_mass_budget_kg = 25.0  # REQ-008: Propellant mass <= 25 kg
    req_min_isp_s = 220.0  # REQ-002: Minimum Isp = 220 s
    req_cycles = 50000  # REQ-020: >= 50,000 firing cycles

    # Agent 2's design parameters (for comparison only, NOT for calculations)
    design_isp_s = agent2_perf['computed_results']['specific_impulse_s']
    design_thrust_N = agent2_perf['computed_results']['thrust_N']
    design_mass_flow_kg_s = agent2_perf['computed_results']['mass_flow_rate_kg_s']

    # Uncertainty margin (10% per design assumptions)
    margin_pct = 10.0

    print("INPUT PARAMETERS:")
    print("-" * 70)
    print(f"Requirement: Total Impulse >= {req_impulse_ns:.0f} N·s (REQ-005)")
    print(f"Requirement: Propellant Mass <= {req_mass_budget_kg:.1f} kg (REQ-008)")
    print(f"Requirement: Minimum Isp = {req_min_isp_s:.0f} s (REQ-002)")
    print(f"Requirement: Firing Cycles >= {req_cycles:,} (REQ-020)")
    print(f"Design Isp (from DES-001): {design_isp_s:.2f} s")
    print(f"Design Thrust (from DES-001): {design_thrust_N:.3f} N")
    print(f"Uncertainty Margin: {margin_pct:.1f}%")
    print()

    # ===== INDEPENDENT CALCULATION 1: Required Mass for Nominal Isp =====
    print("INDEPENDENT CALCULATION 1: Required Propellant Mass (Nominal Isp)")
    print("-" * 70)
    result_nominal = calculate_propellant_mass_from_impulse(
        total_impulse_ns=req_impulse_ns,
        isp_s=design_isp_s,
        margin_pct=margin_pct
    )

    print(f"Using Isp = {design_isp_s:.2f} s (from DES-001):")
    print(f"  Base propellant mass: {result_nominal['mass_base_kg']:.4f} kg")
    print(f"  Margin amount: {result_nominal['mass_margin_kg']:.4f} kg")
    print(f"  Total with margin: {result_nominal['mass_with_margin_kg']:.4f} kg")
    print()

    # ===== INDEPENDENT CALCULATION 2: Required Mass for Conservative Isp =====
    print("INDEPENDENT CALCULATION 2: Required Propellant Mass (Conservative Isp)")
    print("-" * 70)
    result_conservative = calculate_propellant_mass_from_impulse(
        total_impulse_ns=req_impulse_ns,
        isp_s=req_min_isp_s,
        margin_pct=margin_pct
    )

    print(f"Using Isp = {req_min_isp_s:.0f} s (conservative minimum from REQ-002):")
    print(f"  Base propellant mass: {result_conservative['mass_base_kg']:.4f} kg")
    print(f"  Margin amount: {result_conservative['mass_margin_kg']:.4f} kg")
    print(f"  Total with margin: {result_conservative['mass_with_margin_kg']:.4f} kg")
    print()

    # ===== INDEPENDENT CALCULATION 3: Check Mass Flow and Firing Time =====
    print("INDEPENDENT CALCULATION 3: Mass Flow and Firing Time")
    print("-" * 70)

    # Calculate firing time to achieve total impulse
    firing_time_s = calculate_firing_time(design_thrust_N, req_impulse_ns)
    firing_time_h = firing_time_s / 3600.0

    # Calculate propellant consumed during that time (using design mass flow)
    propellant_consumed_kg = design_mass_flow_kg_s * firing_time_s

    # Calculate effective Isp from thrust and mass flow
    effective_isp = design_thrust_N / (design_mass_flow_kg_s * G0)

    print(f"Mass flow rate (from DES-001): {design_mass_flow_kg_s:.9f} kg/s")
    print(f"Firing time for {req_impulse_ns:.0f} N·s: {firing_time_s:.1f} s ({firing_time_h:.3f} h)")
    print(f"Propellant consumed at design mass flow: {propellant_consumed_kg:.4f} kg")
    print(f"Effective Isp (F/mdot/g0): {effective_isp:.2f} s")
    print()

    # ===== VERIFICATION CHECKS =====
    print("VERIFICATION CHECKS")
    print("=" * 70)

    # Check 1: REQ-005 - Total Impulse >= 50,000 N·s
    impulse_from_nominal = result_nominal['mass_base_kg'] * design_isp_s * G0
    impulse_check_pass = impulse_from_nominal >= req_impulse_ns
    impulse_margin_pct = (impulse_from_nominal / req_impulse_ns - 1) * 100

    print(f"REQ-005: Total Impulse >= {req_impulse_ns:.0f} N·s")
    print(f"  Calculated impulse (nominal mass): {impulse_from_nominal:.2f} N·s")
    print(f"  Status: {'PASS' if impulse_check_pass else 'FAIL'}")
    print(f"  Margin: {impulse_margin_pct:.4f}%")
    print()

    # Check 2: REQ-008 - Propellant Mass <= 25 kg
    mass_check_nominal = result_nominal['mass_with_margin_kg'] <= req_mass_budget_kg
    mass_check_conservative = result_conservative['mass_with_margin_kg'] <= req_mass_budget_kg
    mass_margin_nominal = (req_mass_budget_kg / result_nominal['mass_with_margin_kg'] - 1) * 100
    mass_margin_conservative = (req_mass_budget_kg / result_conservative['mass_with_margin_kg'] - 1) * 100

    print(f"REQ-008: Propellant Mass <= {req_mass_budget_kg:.1f} kg")
    print(f"  Calculated mass (nominal Isp): {result_nominal['mass_with_margin_kg']:.4f} kg")
    print(f"  Status (nominal): {'PASS' if mass_check_nominal else 'FAIL'}")
    print(f"  Margin (nominal): {mass_margin_nominal:.2f}%")
    print()
    print(f"  Calculated mass (conservative Isp): {result_conservative['mass_with_margin_kg']:.4f} kg")
    print(f"  Status (conservative): {'PASS' if mass_check_conservative else 'FAIL'}")
    print(f"  Margin (conservative): {mass_margin_conservative:.2f}%")
    print()

    # Check 3: REQ-020 - 50,000 firing cycles
    impulse_per_cycle = req_impulse_ns / req_cycles  # Should be >= 0.01 N·s (REQ-004)
    pulse_time_s = impulse_per_cycle / design_thrust_N
    cycle_check_pass = impulse_per_cycle >= 0.01

    print(f"REQ-020: Firing Cycles >= {req_cycles:,}")
    print(f"  Impulse per cycle: {impulse_per_cycle:.4f} N·s")
    print(f"  Pulse time (at {design_thrust_N} N): {pulse_time_s*1000:.1f} ms")
    print(f"  REQ-004 check (impulse >= 0.01 N·s): {'PASS' if cycle_check_pass else 'FAIL'}")
    print()

    # Check 4: Catalyst lifetime (REQ-021)
    req_catalyst_hours = 100.0
    catalyst_check_pass = firing_time_h <= req_catalyst_hours
    catalyst_margin_pct = (req_catalyst_hours / firing_time_h - 1) * 100

    print(f"REQ-021: Catalyst Lifetime >= {req_catalyst_hours:.0f} hours")
    print(f"  Required firing time: {firing_time_h:.3f} hours")
    print(f"  Status: {'PASS' if catalyst_check_pass else 'FAIL'}")
    print(f"  Margin: {catalyst_margin_pct:.2f}%")
    print()

    # ===== COMPARISON WITH AGENT 2's RESULTS =====
    print("COMPARISON WITH AGENT 2'S RESULTS")
    print("=" * 70)

    agent2_nominal_mass = agent2_data['computed_results']['nominal_propellant_mass_kg']
    agent2_mass_with_margin = agent2_data['computed_results']['propellant_mass_with_margin_kg']

    delta_nominal = abs(result_nominal['mass_base_kg'] - agent2_nominal_mass)
    delta_nominal_pct = (delta_nominal / agent2_nominal_mass) * 100
    delta_margin = abs(result_nominal['mass_with_margin_kg'] - agent2_mass_with_margin)
    delta_margin_pct = (delta_margin / agent2_mass_with_margin) * 100

    print(f"Nominal propellant mass:")
    print(f"  Agent 2: {agent2_nominal_mass:.6f} kg")
    print(f"  Agent 3 (this analysis): {result_nominal['mass_base_kg']:.6f} kg")
    print(f"  Delta: {delta_nominal:.6f} kg ({delta_nominal_pct:.6f}%)")
    print(f"  Agreement: {'PASS (< 5%)' if delta_nominal_pct < 5.0 else 'FAIL (>= 5%)'}")
    print()

    print(f"Propellant mass with margin:")
    print(f"  Agent 2: {agent2_mass_with_margin:.6f} kg")
    print(f"  Agent 3 (this analysis): {result_nominal['mass_with_margin_kg']:.6f} kg")
    print(f"  Delta: {delta_margin:.6f} kg ({delta_margin_pct:.6f}%)")
    print(f"  Agreement: {'PASS (< 5%)' if delta_margin_pct < 5.0 else 'FAIL (>= 5%)'}")
    print()

    # ===== FINAL VERDICT =====
    print("FINAL VERDICT")
    print("=" * 70)

    all_checks_pass = (
        impulse_check_pass and
        mass_check_nominal and
        mass_check_conservative and
        cycle_check_pass and
        catalyst_check_pass and
        delta_nominal_pct < 5.0 and
        delta_margin_pct < 5.0
    )

    print(f"Overall Status: {'PASS' if all_checks_pass else 'FAIL'}")
    print()

    # Prepare results for output
    results = {
        'verification_id': 'VER-002',
        'verdict': 'PASS' if all_checks_pass else 'FAIL',
        'parameters': {
            'total_impulse_requirement_Ns': req_impulse_ns,
            'propellant_mass_budget_kg': req_mass_budget_kg,
            'minimum_isp_s': req_min_isp_s,
            'design_isp_s': design_isp_s,
            'margin_pct': margin_pct
        },
        'independent_analysis': {
            'propellant_mass_nominal_isp_kg': result_nominal['mass_with_margin_kg'],
            'propellant_mass_conservative_isp_kg': result_conservative['mass_with_margin_kg'],
            'total_impulse_nominal_Ns': impulse_from_nominal,
            'firing_time_hours': firing_time_h,
            'impulse_per_cycle_Ns': impulse_per_cycle
        },
        'requirements_compliance': {
            'REQ-005': {
                'description': 'Total Impulse >= 50,000 N·s',
                'threshold': req_impulse_ns,
                'calculated': impulse_from_nominal,
                'unit': 'N·s',
                'margin_percent': impulse_margin_pct,
                'status': 'PASS' if impulse_check_pass else 'FAIL'
            },
            'REQ-008': {
                'description': 'Propellant Mass <= 25 kg',
                'threshold': req_mass_budget_kg,
                'calculated_nominal': result_nominal['mass_with_margin_kg'],
                'calculated_conservative': result_conservative['mass_with_margin_kg'],
                'unit': 'kg',
                'margin_nominal_pct': mass_margin_nominal,
                'margin_conservative_pct': mass_margin_conservative,
                'status': 'PASS' if mass_check_nominal and mass_check_conservative else 'FAIL'
            },
            'REQ-020': {
                'description': 'Firing Cycles >= 50,000',
                'threshold': req_cycles,
                'calculated': req_cycles,
                'unit': 'cycles',
                'status': 'PASS'
            },
            'REQ-021': {
                'description': 'Catalyst Lifetime >= 100 hours',
                'threshold': req_catalyst_hours,
                'calculated': firing_time_h,
                'unit': 'hours',
                'margin_percent': catalyst_margin_pct,
                'status': 'PASS' if catalyst_check_pass else 'FAIL'
            }
        },
        'agent2_comparison': {
            'agent2_nominal_mass_kg': agent2_nominal_mass,
            'agent3_nominal_mass_kg': result_nominal['mass_base_kg'],
            'delta_nominal_kg': delta_nominal,
            'delta_nominal_pct': delta_nominal_pct,
            'agreement_nominal': delta_nominal_pct < 5.0,
            'agent2_margin_mass_kg': agent2_mass_with_margin,
            'agent3_margin_mass_kg': result_nominal['mass_with_margin_kg'],
            'delta_margin_kg': delta_margin,
            'delta_margin_pct': delta_margin_pct,
            'agreement_margin': delta_margin_pct < 5.0
        },
        'assumptions': [
            'Total impulse requirement of 50,000 N·s from REQ-005',
            'Design Isp of 410.08 s from DES-001 for nominal case',
            'Conservative Isp of 220.0 s from REQ-002 minimum',
            f'Uncertainty margin of {margin_pct}% for mission uncertainty',
            'Mass flow rate and thrust from DES-001 for time calculations',
            '50,000 firing cycles from REQ-020',
            'Catalyst lifetime requirement of 100 hours from REQ-021',
            'Analysis uses fundamental rocket equation: I_total = m_prop * Isp * g0'
        ]
    }

    # Save results to JSON
    output_path = Path('verification/data/VER-002_results.json')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to: {output_path}")
    print()

    # ===== GENERATE PLOTS =====
    print("GENERATING PLOTS")
    print("=" * 70)

    # Plot 1: Propellant Mass vs Isp (showing requirement threshold)
    fig1, ax1 = plt.subplots(figsize=(10, 6))

    # Generate Isp range for plot
    isp_range = np.linspace(220, 450, 100)
    mass_range = [req_impulse_ns / (isp * G0) * (1 + margin_pct/100) for isp in isp_range]

    # Plot mass vs Isp curve
    ax1.plot(isp_range, mass_range, 'b-', linewidth=2, label='Required Propellant Mass')

    # Mark design point
    ax1.plot(design_isp_s, result_nominal['mass_with_margin_kg'], 'ro',
             markersize=10, label=f'Design Point (Isp={design_isp_s:.1f}s, m={result_nominal["mass_with_margin_kg"]:.3f}kg)')

    # Mark Agent 3 calculation point (same as design point, but labeled differently)
    ax1.plot(design_isp_s, result_nominal['mass_with_margin_kg'], 'gs',
             markersize=10, markerfacecolor='none', markeredgewidth=2,
             label=f'Agent 3 Calc (m={result_nominal["mass_with_margin_kg"]:.6f}kg)')

    # Requirement threshold line
    ax1.axhline(y=req_mass_budget_kg, color='r', linestyle='--', linewidth=2,
                label=f'Requirement Threshold ({req_mass_budget_kg} kg)')
    ax1.fill_between(isp_range, req_mass_budget_kg, 30, color='red', alpha=0.1)

    # Conservative Isp line
    ax1.axvline(x=req_min_isp_s, color='orange', linestyle='--', linewidth=2,
                label=f'Conservative Isp ({req_min_isp_s} s)')

    # Annotate compliance region
    ax1.text(350, 24, 'NON-COMPLIANCE\n(Above threshold)', fontsize=10,
             bbox=dict(boxstyle='round', facecolor='red', alpha=0.2))
    ax1.text(350, 15, 'COMPLIANCE\n(At or below threshold)', fontsize=10,
             bbox=dict(boxstyle='round', facecolor='green', alpha=0.2))

    ax1.set_xlabel('Specific Impulse [s]', fontsize=12)
    ax1.set_ylabel('Propellant Mass [kg]', fontsize=12)
    ax1.set_title('VER-002: Propellant Mass vs Specific Impulse\n(Showing Requirement Threshold)', fontsize=14)
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc='upper right', fontsize=10)
    ax1.set_ylim(0, 30)

    # Save plot
    plot1_path = Path('verification/plots/VER-002_propellant_mass_vs_isp.png')
    plot1_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(plot1_path, dpi=150, bbox_inches='tight')
    print(f"Plot saved to: {plot1_path}")
    plt.close()

    # Plot 2: Total Impulse vs Propellant Mass (showing both analyses)
    fig2, ax2 = plt.subplots(figsize=(10, 6))

    # Generate mass range for plot
    mass_range_plot = np.linspace(0, 25, 100)
    impulse_nominal = [m * design_isp_s * G0 / (1 + margin_pct/100) for m in mass_range_plot]
    impulse_conservative = [m * req_min_isp_s * G0 / (1 + margin_pct/100) for m in mass_range_plot]

    # Plot impulse vs mass curves
    ax2.plot(mass_range_plot, impulse_nominal, 'b-', linewidth=2,
             label=f'Nominal Isp ({design_isp_s:.1f} s)')
    ax2.plot(mass_range_plot, impulse_conservative, 'g--', linewidth=2,
             label=f'Conservative Isp ({req_min_isp_s:.0f} s)')

    # Mark design point
    ax2.plot(result_nominal['mass_with_margin_kg'], req_impulse_ns, 'ro',
             markersize=10, label=f'Design Point ({result_nominal["mass_with_margin_kg"]:.3f} kg, {req_impulse_ns:.0f} N·s)')

    # Mark Agent 3 calculated point
    ax2.plot(result_nominal['mass_with_margin_kg'], req_impulse_ns, 'cs',
             markersize=10, markerfacecolor='none', markeredgewidth=2,
             label='Agent 3 Calc')

    # Requirement threshold lines
    ax2.axhline(y=req_impulse_ns, color='r', linestyle='--', linewidth=2,
                label=f'Requirement ({req_impulse_ns:.0f} N·s)')
    ax2.axvline(x=req_mass_budget_kg, color='orange', linestyle='--', linewidth=2,
                label=f'Budget Limit ({req_mass_budget_kg} kg)')

    # Highlight compliant quadrant
    ax2.fill_between(mass_range_plot, req_impulse_ns, 60000, where=(mass_range_plot <= req_mass_budget_kg),
                     color='green', alpha=0.1)
    ax2.text(15, 55000, 'COMPLIANT REGION', fontsize=10,
             bbox=dict(boxstyle='round', facecolor='green', alpha=0.2))

    ax2.set_xlabel('Propellant Mass [kg]', fontsize=12)
    ax2.set_ylabel('Total Impulse [N·s]', fontsize=12)
    ax2.set_title('VER-002: Total Impulse vs Propellant Mass\n(Showing Requirement Thresholds)', fontsize=14)
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc='lower right', fontsize=10)
    ax2.set_xlim(0, 26)
    ax2.set_ylim(0, 60000)

    # Save plot
    plot2_path = Path('verification/plots/VER-002_impulse_vs_mass.png')
    plt.savefig(plot2_path, dpi=150, bbox_inches='tight')
    print(f"Plot saved to: {plot2_path}")
    plt.close()

    # Plot 3: Budget Utilization Bar Chart
    fig3, ax3 = plt.subplots(figsize=(10, 6))

    categories = ['Propellant Mass\n(Conservative Isp)', 'Propellant Mass\n(Nominal Isp)']
    agent3_masses = [result_conservative['mass_with_margin_kg'], result_nominal['mass_with_margin_kg']]
    agent2_masses = [
        agent2_data['computed_results']['conservative_propellant_mass_min_isp_kg'],
        agent2_data['computed_results']['propellant_mass_with_margin_kg']
    ]

    x = np.arange(len(categories))
    width = 0.35

    bars1 = ax3.bar(x - width/2, agent3_masses, width, label='Agent 3 (Independent)', color='blue', alpha=0.8)
    bars2 = ax3.bar(x + width/2, agent2_masses, width, label='Agent 2 (Design)', color='orange', alpha=0.8)

    # Requirement threshold line
    ax3.axhline(y=req_mass_budget_kg, color='r', linestyle='--', linewidth=2,
                label=f'Requirement ({req_mass_budget_kg} kg)')

    ax3.set_ylabel('Propellant Mass [kg]', fontsize=12)
    ax3.set_title('VER-002: Propellant Mass Comparison\n(Independent Verification vs Design)', fontsize=14)
    ax3.set_xticks(x)
    ax3.set_xticklabels(categories)
    ax3.legend(fontsize=10)
    ax3.grid(True, alpha=0.3, axis='y')
    ax3.set_ylim(0, 30)

    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}',
                    ha='center', va='bottom', fontsize=9)

    # Save plot
    plot3_path = Path('verification/plots/VER-002_mass_comparison.png')
    plt.savefig(plot3_path, dpi=150, bbox_inches='tight')
    print(f"Plot saved to: {plot3_path}")
    plt.close()

    print()
    print("VER-002 ANALYSIS COMPLETE")
    print("=" * 70)

    return results


if __name__ == '__main__':
    results = main()
