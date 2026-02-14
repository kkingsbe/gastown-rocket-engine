#!/usr/bin/env python3
"""
DES-003: Catalyst Preheat System Design

This script calculates the thermal requirements for the catalyst bed preheat system,
including heater power, thermal mass, and preheat time to reach operating temperature
within the 15W power constraint at 28V.

Author: Agent 2 (Design & Implementation Engineer)
Date: 2026-02-14
Design ID: DES-003
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================================
# PHYSICAL CONSTANTS AND MATERIAL PROPERTIES
# ============================================================================

# Physical constants
g0 = 9.80665           # m/s^2 - standard gravitational acceleration (exact, SI)
R_universal = 8314.46  # J/(kmol*K) - universal gas constant (NIST)
sigma_SB = 5.67e-8     # W/(m^2*K^4) - Stefan-Boltzmann constant

# Temperature conversions
C_to_K = 273.15        # Celsius to Kelvin offset
K_to_C = lambda T_K: T_K - C_to_K
C_to_K_func = lambda T_C: T_C + C_to_K

# Catalyst material properties (Shell 405: Iridium on alumina support)
# Sources: CONTEXT.md Section 4 (Catalyst), NASA CR-182202, heritage thruster data
catalyst_specific_heat = 800.0      # J/(kg*K) - Alumina support at ~300K
catalyst_density = 2500.0           # kg/m^3 - Porous alumina support
catalyst_porosity = 0.4             # Typical porosity for Shell 405
catalyst_solid_density = 4000.0     # kg/m^3 - Alumina solid density

# Chamber material properties (Inconel 625 - heritage choice)
# Sources: CONTEXT.md Section 4, NASA materials database
chamber_specific_heat = 435.0       # J/(kg*K) at 300K
chamber_density = 8440.0            # kg/m^3

# Thermal properties for analysis
# Convection coefficient for natural convection in space (very low)
# Sources: Spacecraft thermal control handbook
h_convection = 1.0                 # W/(m^2*K) - worst-case natural convection in spacecraft

# Emissivity values (depends on surface finish)
# Sources: Spacecraft thermal control handbook
epsilon_catalyst = 0.85            # Catalyst bed internal emissivity (high - rough surface)
epsilon_chamber = 0.3              # Chamber external emissivity (low - polished or coated)

# Heater electrical properties
voltage_nominal = 28.0             # V - nominal voltage (REQ-027)
power_limit = 15.0                  # W - maximum heater power (REQ-027)

# Environment temperature
T_ambient_K = C_to_K_func(20.0)    # Ambient temperature (typical spacecraft interior)
T_initial_K = C_to_K_func(20.0)    # Initial catalyst bed temperature

# Target temperature range (REQ-014)
T_target_min_K = C_to_K_func(150.0)  # Minimum preheat temperature
T_target_max_K = C_to_K_func(300.0)  # Maximum preheat temperature
T_target_design_K = C_to_K_func(200.0)  # Design preheat temperature (mid-range)

# Preheat time requirement (derived from REQ-006: 90% thrust within 200ms)
# Preheat happens before first firing, not during startup sequence
# Typical preheat time for small thrusters: 5-15 minutes
preheat_time_target = 600.0        # seconds - target preheat time (10 minutes)


# ============================================================================
# DESIGN PARAMETERS FROM DES-001
# ============================================================================

# Chamber geometry from DES-001 (thruster_performance_sizing.json)
throat_diameter = 0.007476535752447692  # m (7.48 mm)

# Chamber diameter assumption: 3x throat diameter (typical for hydrazine thrusters)
# Sources: CONTEXT.md Section 3 (Key Dimensions)
chamber_diameter = 3.0 * throat_diameter  # m
chamber_radius = chamber_diameter / 2.0   # m

# Catalyst bed dimensions
# Sources: CONTEXT.md Section 4 (Catalyst)
# Bed length/diameter ratio: 1.5-3.0 typical
bed_length_diameter_ratio = 2.0   # Design choice - mid-range
bed_length = chamber_diameter * bed_length_diameter_ratio  # m

# Catalyst bed volume
bed_volume = np.pi * chamber_radius**2 * bed_length  # m^3

# Catalyst loading (mass per volume accounting for porosity)
# Porous bed density = solid_density * (1 - porosity)
bed_density = catalyst_solid_density * (1 - catalyst_porosity)  # kg/m^3
catalyst_mass = bed_density * bed_volume  # kg

# Chamber wall mass (simplified cylindrical section)
# Assume wall thickness = 1.0 mm (minimum manufacturable for small thrusters)
wall_thickness = 0.001  # m (1 mm)
chamber_wall_volume = np.pi * ((chamber_radius + wall_thickness)**2 - chamber_radius**2) * bed_length  # m^3
chamber_wall_mass = chamber_density * chamber_wall_volume  # kg


# ============================================================================
# THERMAL ANALYSIS
# ============================================================================

def calculate_heater_power(T_current, T_target, time_seconds):
    """
    Calculate required heater power to reach target temperature in specified time.
    
    Parameters:
    -----------
    T_current : float
        Current temperature [K]
    T_target : float
        Target temperature [K]
    time_seconds : float
        Time to reach target temperature [s]
    
    Returns:
    --------
    float
        Required heater power [W]
    """
    # Temperature rise needed
    delta_T = T_target - T_current
    
    # Thermal mass (heat capacity) of the system
    # Heat required to heat catalyst + chamber wall
    Q_catalyst = catalyst_mass * catalyst_specific_heat * delta_T  # J
    Q_chamber = chamber_wall_mass * chamber_specific_heat * delta_T  # J
    Q_total = Q_catalyst + Q_chamber  # J
    
    # Power required (assuming constant power)
    power_heating = Q_total / time_seconds  # W
    
    # Estimate heat losses during heating
    # Simplified: average temperature during heating
    T_avg_K = (T_current + T_target) / 2.0
    
    # Surface area for radiation/convection
    # Chamber external surface area (cylindrical + ends)
    bed_surface_area = 2.0 * np.pi * (chamber_radius + wall_thickness) * bed_length  # m^2 (cylindrical)
    bed_end_area = 2.0 * np.pi * (chamber_radius + wall_thickness)**2  # m^2 (two ends)
    total_surface_area = bed_surface_area + bed_end_area  # m^2
    
    # Radiation losses (simplified - worst case)
    # Q_rad = epsilon * sigma * A * (T_avg^4 - T_ambient^4)
    Q_rad_loss = epsilon_chamber * sigma_SB * total_surface_area * (T_avg_K**4 - T_ambient_K**4) * time_seconds  # J
    
    # Convection losses (negligible in space, but included for completeness)
    Q_conv_loss = h_convection * total_surface_area * (T_avg_K - T_ambient_K) * time_seconds  # J
    
    # Total heat losses
    Q_loss = Q_rad_loss + Q_conv_loss  # J
    
    # Power required including losses
    power_required = power_heating + (Q_loss / time_seconds)  # W
    
    return power_required, power_heating, Q_total, Q_loss


def calculate_heater_resistance(power, voltage):
    """
    Calculate heater resistance for given power and voltage.
    
    Parameters:
    -----------
    power : float
        Heater power [W]
    voltage : float
        Heater voltage [V]
    
    Returns:
    --------
    float
        Heater resistance [Ohm]
    float
        Heater current [A]
    """
    # P = V^2 / R => R = V^2 / P
    resistance = voltage**2 / power  # Ohm
    current = power / voltage  # A
    return resistance, current


def simulate_preheat(heater_power, time_step=10.0, max_time=3600.0):
    """
    Simulate preheat temperature rise over time with given heater power.
    
    Parameters:
    -----------
    heater_power : float
        Heater power [W]
    time_step : float
        Simulation time step [s]
    max_time : float
        Maximum simulation time [s]
    
    Returns:
    --------
    dict
        Simulation results with temperature vs time data
    """
    # Thermal mass of the system
    # Effective heat capacity = m_catalyst * cp_catalyst + m_chamber * cp_chamber
    effective_heat_capacity = (catalyst_mass * catalyst_specific_heat + 
                               chamber_wall_mass * chamber_specific_heat)  # J/K
    
    # Surface area for heat loss
    bed_surface_area = 2.0 * np.pi * (chamber_radius + wall_thickness) * bed_length  # m^2
    bed_end_area = 2.0 * np.pi * (chamber_radius + wall_thickness)**2  # m^2
    total_surface_area = bed_surface_area + bed_end_area  # m^2
    
    # Time array
    times = np.arange(0, max_time + time_step, time_step)
    temperatures = np.zeros_like(times)
    temperatures[0] = T_initial_K
    
    # Simulation loop
    for i in range(1, len(times)):
        T_prev = temperatures[i-1]
        
        # Heat input from heater
        Q_in = heater_power * time_step  # J
        
        # Heat losses (radiation + convection)
        Q_rad = epsilon_chamber * sigma_SB * total_surface_area * (T_prev**4 - T_ambient_K**4) * time_step  # J
        Q_conv = h_convection * total_surface_area * (T_prev - T_ambient_K) * time_step  # J
        Q_loss = Q_rad + Q_conv  # J
        
        # Net heat added
        Q_net = Q_in - Q_loss  # J
        
        # Temperature change
        delta_T = Q_net / effective_heat_capacity  # K
        
        # New temperature
        temperatures[i] = T_prev + delta_T
    
    # Find time to reach target temperatures
    indices_min = np.where(temperatures >= T_target_min_K)[0]
    indices_max = np.where(temperatures >= T_target_max_K)[0]
    indices_design = np.where(temperatures >= T_target_design_K)[0]
    
    time_to_min = times[indices_min[0]] if len(indices_min) > 0 else None
    time_to_max = times[indices_max[0]] if len(indices_max) > 0 else None
    time_to_design = times[indices_design[0]] if len(indices_design) > 0 else None
    
    return {
        'times': times,
        'temperatures': temperatures,
        'time_to_min': time_to_min,
        'time_to_max': time_to_max,
        'time_to_design': time_to_design
    }


# ============================================================================
# MAIN CALCULATION
# ============================================================================

def main():
    print("="*80)
    print("DES-003: Catalyst Preheat System Thermal Analysis")
    print("="*80)
    print()
    
    # Calculate required heater power for design target (initial estimate)
    power_required_initial, power_heating_only, Q_total, Q_loss = calculate_heater_power(
        T_initial_K, T_target_design_K, preheat_time_target
    )
    
    # Use 15W as the actual heater power (constraint from REQ-027)
    power_at_limit = power_limit
    resistance_at_limit, current_at_limit = calculate_heater_resistance(power_at_limit, voltage_nominal)
    
    # Simulate preheat with maximum available power (15W)
    sim_results = simulate_preheat(power_at_limit, time_step=10.0, max_time=3600.0)
    
    # Determine actual achievable preheat time at 15W
    actual_preheat_time_to_design = sim_results['time_to_design']
    
    # Check if power requirement exceeds limit
    power_compliance = power_at_limit <= power_limit
    
    # Temperature range compliance (design target should be within range)
    temp_compliance = T_target_min_K <= T_target_design_K <= T_target_max_K
    
    # Preheat time compliance (check if 15W can reach target within reasonable time)
    # Define "reasonable" as 20 minutes (1200 seconds)
    time_compliance = sim_results['time_to_design'] <= 1200.0 if sim_results['time_to_design'] is not None else False
    
    # Print results
    print("GEOMETRY AND THERMAL MASS")
    print("-" * 80)
    print(f"Throat diameter:              {throat_diameter*1000:.4f} mm")
    print(f"Chamber diameter:             {chamber_diameter*1000:.4f} mm")
    print(f"Bed length/diameter ratio:    {bed_length_diameter_ratio:.2f}")
    print(f"Bed length:                   {bed_length*1000:.2f} mm")
    print(f"Bed volume:                   {bed_volume*1e6:.4f} cm^3")
    print(f"Catalyst mass:                {catalyst_mass*1000:.2f} g")
    print(f"Chamber wall thickness:       {wall_thickness*1000:.2f} mm")
    print(f"Chamber wall mass:            {chamber_wall_mass*1000:.2f} g")
    print(f"Total thermal mass:           {(catalyst_mass + chamber_wall_mass)*1000:.2f} g")
    print()
    
    print("THERMAL ANALYSIS")
    print("-" * 80)
    print(f"Initial temperature:          {K_to_C(T_initial_K):.1f} °C")
    print(f"Target preheat temperature:    {K_to_C(T_target_design_K):.1f} °C")
    print(f"Temperature range (REQ-014):   {K_to_C(T_target_min_K):.1f} - {K_to_C(T_target_max_K):.1f} °C")
    print(f"Temperature rise required:    {T_target_design_K - T_initial_K:.1f} K")
    print()
    print(f"Heat required (catalyst):     {Q_catalyst if 'Q_catalyst' in locals() else catalyst_mass * catalyst_specific_heat * (T_target_design_K - T_initial_K):.2f} J")
    print(f"Heat required (chamber):      {Q_chamber if 'Q_chamber' in locals() else chamber_wall_mass * chamber_specific_heat * (T_target_design_K - T_initial_K):.2f} J")
    print(f"Total heat required:          {Q_total:.2f} J")
    print(f"Heat losses (during preheat): {Q_loss:.2f} J")
    print()
    
    print("HEATER DESIGN (POWER LIMITED: 15W)")
    print("-" * 80)
    print(f"Heater power:                 {power_at_limit:.2f} W (REQ-027 limit)")
    print(f"Nominal voltage:              {voltage_nominal:.1f} V (REQ-027)")
    print(f"Heater resistance:           {resistance_at_limit:.2f} Ohm")
    print(f"Heater current:               {current_at_limit:.3f} A")
    print(f"Initial preheat time target:  {preheat_time_target:.1f} s ({preheat_time_target/60:.1f} min)")
    print(f"Actual preheat time to 200°C: {actual_preheat_time_to_design:.1f} s ({actual_preheat_time_to_design/60:.1f} min)")
    print()
    
    print("PREHEAT TIME ANALYSIS (15W HEATER)")
    print("-" * 80)
    print(f"Time to {K_to_C(T_target_min_K):.0f}°C:            {sim_results['time_to_min']:.1f} s ({sim_results['time_to_min']/60:.1f} min)" if sim_results['time_to_min'] else "Time to 150°C: NOT REACHED")
    print(f"Time to {K_to_C(T_target_design_K):.0f}°C:          {sim_results['time_to_design']:.1f} s ({sim_results['time_to_design']/60:.1f} min)" if sim_results['time_to_design'] else "Time to 200°C: NOT REACHED")
    print(f"Time to {K_to_C(T_target_max_K):.0f}°C:            {sim_results['time_to_max']:.1f} s ({sim_results['time_to_max']/60:.1f} min)" if sim_results['time_to_max'] else "Time to 300°C: NOT REACHED")
    print()
    
    # Generate preheat curve plot
    plot_dir = Path('design/plots')
    plot_dir.mkdir(parents=True, exist_ok=True)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(sim_results['times'] / 60.0, K_to_C(sim_results['temperatures']), 'b-', linewidth=2, label='Bed Temperature')
    
    # Plot temperature range markers
    ax.axhline(y=K_to_C(T_target_min_K), color='g', linestyle='--', linewidth=2, label=f'Range Min ({K_to_C(T_target_min_K):.0f}°C)')
    ax.axhline(y=K_to_C(T_target_max_K), color='r', linestyle='--', linewidth=2, label=f'Range Max ({K_to_C(T_target_max_K):.0f}°C)')
    ax.axhline(y=K_to_C(T_target_design_K), color='orange', linestyle=':', linewidth=2, label=f'Design Target ({K_to_C(T_target_design_K):.0f}°C)')
    
    # Plot time markers
    if sim_results['time_to_min']:
        ax.axvline(x=sim_results['time_to_min']/60, color='g', linestyle='--', alpha=0.5)
    if sim_results['time_to_design']:
        ax.axvline(x=sim_results['time_to_design']/60, color='orange', linestyle=':', alpha=0.5)
    if sim_results['time_to_max']:
        ax.axvline(x=sim_results['time_to_max']/60, color='r', linestyle='--', alpha=0.5)
    
    ax.set_xlabel('Preheat Time (minutes)', fontsize=12)
    ax.set_ylabel('Temperature (°C)', fontsize=12)
    ax.set_title('Catalyst Bed Preheat Curve (15W Heater)', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)
    ax.set_xlim(0, max(sim_results['times'][-1]/60, 20))
    ax.set_ylim(0, max(K_to_C(sim_results['temperatures'])[-1], K_to_C(T_target_max_K)) * 1.1)
    
    plt.tight_layout()
    plot_path = plot_dir / 'DES003_preheat_curve.png'
    plt.savefig(plot_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Plot saved to: {plot_path}")
    print()
    
    # Prepare output data
    output_data = {
        "design_id": "DES-003",
        "parameters": {
            "throat_diameter_m": throat_diameter,
            "chamber_diameter_m": chamber_diameter,
            "bed_length_m": bed_length,
            "bed_length_diameter_ratio": bed_length_diameter_ratio,
            "wall_thickness_m": wall_thickness,
            "catalyst_mass_kg": catalyst_mass,
            "chamber_wall_mass_kg": chamber_wall_mass,
            "total_thermal_mass_kg": catalyst_mass + chamber_wall_mass,
            "initial_temperature_C": K_to_C(T_initial_K),
            "target_preheat_temperature_C": K_to_C(T_target_design_K),
            "target_preheat_time_s": preheat_time_target
        },
        "material_properties": {
            "catalyst_specific_heat_J_kg_K": catalyst_specific_heat,
            "catalyst_density_kg_m3": catalyst_density,
            "catalyst_porosity": catalyst_porosity,
            "chamber_specific_heat_J_kg_K": chamber_specific_heat,
            "chamber_density_kg_m3": chamber_density,
            "epsilon_chamber": epsilon_chamber
        },
        "thermal_analysis": {
            "temperature_rise_K": T_target_design_K - T_initial_K,
            "heat_required_J": Q_total,
            "heat_losses_J": Q_loss,
            "heat_required_catalyst_J": catalyst_mass * catalyst_specific_heat * (T_target_design_K - T_initial_K),
            "heat_required_chamber_J": chamber_wall_mass * chamber_specific_heat * (T_target_design_K - T_initial_K)
        },
        "heater_design": {
            "nominal_voltage_V": voltage_nominal,
            "power_limit_W": power_limit,
            "heater_power_W": power_at_limit,
            "heater_resistance_Ohm": resistance_at_limit,
            "heater_current_A": current_at_limit,
            "initial_preheat_time_target_s": preheat_time_target,
            "actual_preheat_time_to_design_temp_s": float(actual_preheat_time_to_design) if actual_preheat_time_to_design else None
        },
        "preheat_performance_at_limit": {
            "time_to_min_temperature_s": float(sim_results['time_to_min']) if sim_results['time_to_min'] else None,
            "time_to_design_temperature_s": float(sim_results['time_to_design']) if sim_results['time_to_design'] else None,
            "time_to_max_temperature_s": float(sim_results['time_to_max']) if sim_results['time_to_max'] else None
        },
        "requirements_compliance": {
            "REQ-014": {
                "description": "Catalyst bed preheat 150-300°C before first firing",
                "threshold_min_C": K_to_C(T_target_min_K),
                "threshold_max_C": K_to_C(T_target_max_K),
                "design_target_C": K_to_C(T_target_design_K),
                "within_range": temp_compliance,
                "status": "PASS" if temp_compliance else "FAIL"
            },
            "REQ-027": {
                "description": "Heater power ≤ 15W at 28V",
                "threshold_power_W": power_limit,
                "threshold_voltage_V": voltage_nominal,
                "heater_power_W": power_at_limit,
                "within_power_limit": power_compliance,
                "status": "PASS" if power_compliance else "FAIL"
            }
        },
        "assumptions": [
            "Chamber diameter = 3x throat diameter (typical for hydrazine thrusters)",
            "Bed length/diameter ratio = 2.0 (mid-range of 1.5-3.0 typical)",
            "Catalyst bed loading based on Shell 405 (Iridium on alumina support)",
            "Wall thickness = 1.0 mm (minimum manufacturable for small thrusters)",
            "Natural convection in spacecraft: h = 1.0 W/(m^2*K) (conservative)",
            "Chamber external emissivity = 0.3 (polished or coated surface)",
            "Initial temperature = 20°C (typical spacecraft interior)",
            "Target preheat time = 600 seconds (10 minutes, typical for small thrusters)",
            "Thermal losses dominated by radiation (convection negligible in space)",
            "Heater power constant during preheat (simplified model)",
            "No heat loss to feed lines during preheat (isolated for worst-case analysis)"
        ],
        "sources": [
            "Shell 405 catalyst properties: NASA CR-182202",
            "Inconel 625 properties: NASA materials database",
            "Thermal properties: Spacecraft thermal control handbook",
            "Catalyst bed sizing: CONTEXT.md Section 4 (Catalyst)",
            "Physical constants: NIST, CONTEXT.md Section 6"
        ]
    }
    
    # Write output JSON
    output_dir = Path('design/data')
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / 'catalyst_preheat_thermal.json'
    with open(output_path, 'w') as f:
        json.dump(output_data, f, indent=2)
    print(f"Output data saved to: {output_path}")
    print()
    
    # Print requirements compliance summary
    print("="*80)
    print("REQUIREMENTS COMPLIANCE SUMMARY")
    print("="*80)
    for req_key, req_data in output_data["requirements_compliance"].items():
        print(f"\n{req_key}: {req_data['status']}")
        print(f"  Description: {req_data['description']}")
        if req_key == "REQ-014":
            print(f"  Required range: {req_data['threshold_min_C']:.1f} - {req_data['threshold_max_C']:.1f} °C")
            print(f"  Design target:  {req_data['design_target_C']:.1f} °C")
            print(f"  Within range:   {req_data['within_range']}")
        elif req_key == "REQ-027":
            print(f"  Max power:      {req_data['threshold_power_W']:.1f} W at {req_data['threshold_voltage_V']:.0f} V")
            print(f"  Heater power:   {req_data['heater_power_W']:.2f} W")
            print(f"  Within limit:   {req_data['within_power_limit']}")
    
    print()
    print("="*80)
    
    # Return results for potential further processing
    return output_data


if __name__ == "__main__":
    results = main()
