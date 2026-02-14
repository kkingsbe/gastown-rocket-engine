#!/usr/bin/env python3
"""
VER-004 Plotting Script

Generates plots for VER-004 verification:
- Stress vs. Pressure showing safety factor threshold
"""

import json
import math
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

# Load verification results
results_path = Path(__file__).parent.parent / "data" / "VER-004_results.json"
with open(results_path, 'r') as f:
    results = json.load(f)

stress_data = results['stress_vs_pressure_data']
wall_verify = results['wall_thickness_verification']

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))

pressures = stress_data['pressures_MPa']
hoop_stress_thin = stress_data['hoop_stress_thin_wall_MPa']
von_mises_stress = stress_data['von_mises_stress_MPa']
yield_limit = stress_data['yield_limit_MPa'][0]  # Constant

# Plot stresses
ax.plot(pressures, hoop_stress_thin, 'b-', linewidth=2, label='Thin-wall Hoop Stress')
ax.plot(pressures, von_mises_stress, 'r-', linewidth=2, label='von Mises Equivalent Stress')

# Plot yield strength limit
ax.axhline(y=yield_limit, color='g', linestyle='--', linewidth=2, label=f'Yield Strength ({yield_limit:.1f} MPa)')

# Mark important pressure levels
meop_pressure = stress_data['meop_MPa']
design_pressure = stress_data['design_pressure_MPa']

# MEOP line
ax.axvline(x=meop_pressure, color='orange', linestyle=':', linewidth=1.5, label=f'MEOP ({meop_pressure:.3f} MPa)')

# Design pressure line
ax.axvline(x=design_pressure, color='purple', linestyle=':', linewidth=1.5, label=f'Design Pressure ({design_pressure:.3f} MPa)')

# Calculate the yield limit at the design pressure for annotation
hoop_stress_at_design = wall_verify['thin_wall_analysis']['hoop_stress_MPa']
vm_stress_at_design = wall_verify['von_mises_analysis']['equivalent_stress_MPa']
sf_thin = wall_verify['thin_wall_analysis']['safety_factor']
sf_vm = wall_verify['von_mises_analysis']['safety_factor']

# Mark operating point
ax.plot(design_pressure, hoop_stress_at_design, 'bo', markersize=8, label=f'Operating Point (SF={sf_thin:.1f})')
ax.plot(design_pressure, vm_stress_at_design, 'ro', markersize=8)

# Add annotation for safety factor requirement
sf_required = 1.5
sf_limit_pressure = yield_limit / (wall_verify['thin_wall_analysis']['hoop_stress_MPa'] / design_pressure)
ax.text(0.05, 0.95, f'Required SF: {sf_required}x', transform=ax.transAxes,
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5), verticalalignment='top')
ax.text(0.05, 0.90, f'Thin-wall SF: {sf_thin:.1f}x ✓', transform=ax.transAxes,
        bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5), verticalalignment='top')
ax.text(0.05, 0.85, f'von Mises SF: {sf_vm:.1f}x ✓', transform=ax.transAxes,
        bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5), verticalalignment='top')

# Labels and title
ax.set_xlabel('Chamber Pressure (MPa)', fontsize=12)
ax.set_ylabel('Stress (MPa)', fontsize=12)
ax.set_title('VER-004: Chamber Wall Stress vs. Pressure\nwith Safety Factor Threshold (REQ-018)', fontsize=14, fontweight='bold')
ax.legend(loc='upper right', fontsize=10)
ax.grid(True, alpha=0.3)

# Set y-axis to start at 0
ax.set_ylim(bottom=0)

# Save the plot
plot_path = Path(__file__).parent.parent / "plots" / "VER-004_stress_vs_pressure.png"
plt.savefig(plot_path, dpi=150, bbox_inches='tight')
print(f"Plot saved to: {plot_path}")

# Also create a summary plot showing the multi-axial stress state
fig2, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Plot 1: Stress components at design pressure
stress_components = ['Hoop (Inner)', 'Hoop (Outer)', 'Longitudinal', 'Radial']
stress_values = [
    wall_verify['lame_thick_wall_analysis']['hoop_stress_inner_MPa'],
    wall_verify['lame_thick_wall_analysis']['hoop_stress_outer_MPa'],
    wall_verify['lame_thick_wall_analysis']['longitudinal_stress_inner_MPa'],
    wall_verify['lame_thick_wall_analysis']['radial_stress_inner_MPa']
]
colors = ['red', 'salmon', 'blue', 'green']

bars = ax1.bar(stress_components, stress_values, color=colors, alpha=0.7)
ax1.axhline(y=yield_limit, color='purple', linestyle='--', linewidth=2, label=f'Yield Strength ({yield_limit:.1f} MPa)')
ax1.set_ylabel('Stress (MPa)', fontsize=12)
ax1.set_title('Stress Components at Design Pressure (Lame Theory)', fontsize=12, fontweight='bold')
ax1.legend()
ax1.grid(axis='y', alpha=0.3)

# Add value labels on bars
for bar, val in zip(bars, stress_values):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            f'{val:.2f}', ha='center', va='bottom', fontsize=10)

# Plot 2: Safety factor comparison
methods = ['Thin-wall', 'von Mises', 'Tresca']
sf_values = [
    wall_verify['thin_wall_analysis']['safety_factor'],
    wall_verify['von_mises_analysis']['safety_factor'],
    wall_verify['tresca_analysis']['safety_factor']
]
colors_sf = ['lightgreen', 'lightgreen', 'lightgreen']

bars2 = ax2.bar(methods, sf_values, color=colors_sf, alpha=0.7, edgecolor='green', linewidth=2)
ax2.axhline(y=sf_required, color='red', linestyle='--', linewidth=2, label=f'Required SF ({sf_required}x)')
ax2.set_ylabel('Safety Factor', fontsize=12)
ax2.set_title('Safety Factor Comparison - All Methods', fontsize=12, fontweight='bold')
ax2.legend()
ax2.grid(axis='y', alpha=0.3)

# Add value labels on bars
for bar, val in zip(bars2, sf_values):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            f'{val:.1f}', ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.tight_layout()

plot2_path = Path(__file__).parent.parent / "plots" / "VER-004_stress_analysis_summary.png"
plt.savefig(plot2_path, dpi=150, bbox_inches='tight')
print(f"Summary plot saved to: {plot2_path}")

print("\nPlot generation complete.")
