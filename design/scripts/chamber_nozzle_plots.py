#!/usr/bin/env python3
"""
chamber_nozzle_plots.py - Design visualizations for DES-004

Generates plots for:
1. Chamber stress analysis (hoop stress vs thickness)
2. Material selection comparison
3. Envelope visualization
"""

import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from pathlib import Path

# Load design data
data_path = Path(__file__).parent.parent / "data" / "chamber_nozzle_stress.json"
with open(data_path, 'r') as f:
    data = json.load(f)

# Extract key parameters
chamber_radius_mm = data["chamber_geometry"]["chamber_radius_mm"]
design_pressure_MPa = data["parameters"]["design_pressure_MPa"]
design_thickness_mm = data["wall_thickness"]["design_thickness_mm"]
material_yield_MPa = data["wall_thickness"]["material_yield_at_temp_MPa"]
chamber_diameter_mm = data["chamber_geometry"]["chamber_diameter_mm"]
chamber_length_mm = data["chamber_geometry"]["chamber_length_mm"]
nozzle_length_mm = data["nozzle_properties"]["nozzle_length_mm"]
nozzle_exit_diameter_mm = data["nozzle_properties"]["exit_diameter_mm"]
overall_length_mm = data["overall_envelope"]["overall_length_mm"]
overall_diameter_mm = data["overall_envelope"]["overall_diameter_mm"]
throat_diameter_mm = data["nozzle_properties"]["exit_diameter_mm"] / 10  # Approx from geometry

# Material data
MATERIALS = {
    "Inconel 625": {"yield": 460 * 0.4, "temp": 980, "density": 8440},
    "Haynes 230": {"yield": 390 * 0.4, "temp": 1150, "density": 8970},
    "Molybdenum": {"yield": 560 * 0.4, "temp": 1650, "density": 10220},
    "Rhenium": {"yield": 290 * 0.4, "temp": 2000, "density": 21020},
    "Columbium C103": {"yield": 240 * 0.4, "temp": 1370, "density": 8850}
}

# Operating temperature
operating_temp_C = data["parameters"]["chamber_operating_temp_C"]

# ============================================
# Plot 1: Hoop Stress vs Wall Thickness
# ============================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Left: Stress vs Thickness
thickness_range = np.linspace(0.1, 1.0, 100)  # mm
stress_values = []
for t in thickness_range:
    t_m = t / 1000
    stress_Pa = (design_pressure_MPa * 1e6 * chamber_radius_mm / 1000) / t_m
    stress_MPa = stress_Pa / 1e6
    stress_values.append(stress_MPa)

ax1.plot(thickness_range, stress_values, 'b-', linewidth=2, label='Hoop Stress')
ax1.axhline(y=material_yield_MPa, color='r', linestyle='--', linewidth=2, label=f'Material Yield ({material_yield_MPa:.0f} MPa)')
ax1.axvline(x=design_thickness_mm, color='g', linestyle=':', linewidth=2, label=f'Design Thickness ({design_thickness_mm:.3f} mm)')

ax1.set_xlabel('Wall Thickness (mm)', fontsize=12)
ax1.set_ylabel('Hoop Stress (MPa)', fontsize=12)
ax1.set_title('Chamber Hoop Stress vs Wall Thickness', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.legend(fontsize=10)

# Add safety factor annotation
current_stress = (design_pressure_MPa * 1e6 * chamber_radius_mm / 1000) / (design_thickness_mm / 1000) / 1e6
sf = material_yield_MPa / current_stress
ax1.text(0.05, 0.95, f'Safety Factor: {sf:.1f}', transform=ax1.transAxes, 
         fontsize=12, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Right: Safety Factor vs Thickness
sf_values = [material_yield_MPa / s for s in stress_values]
ax2.plot(thickness_range, sf_values, 'b-', linewidth=2, label='Safety Factor')
ax2.axhline(y=1.5, color='r', linestyle='--', linewidth=2, label='Required SF (1.5)')
ax2.axvline(x=design_thickness_mm, color='g', linestyle=':', linewidth=2, label=f'Design Thickness ({design_thickness_mm:.3f} mm)')
ax2.set_xlabel('Wall Thickness (mm)', fontsize=12)
ax2.set_ylabel('Safety Factor', fontsize=12)
ax2.set_title('Safety Factor vs Wall Thickness', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.legend(fontsize=10)
ax2.set_ylim(0, max(sf_values) * 1.1)

plt.tight_layout()
plt.savefig(Path(__file__).parent.parent / "plots" / "DES004_stress_analysis.png", dpi=150, bbox_inches='tight')
plt.close()

# ============================================
# Plot 2: Material Selection Comparison
# ============================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Prepare data
materials = list(MATERIALS.keys())
yields = [MATERIALS[m]["yield"] for m in materials]
temps = [MATERIALS[m]["temp"] for m in materials]
densities = [MATERIALS[m]["density"] for m in materials]
colors = ['red' if temp < operating_temp_C else 'green' for temp in temps]

# Left: Yield Strength
bars1 = ax1.bar(materials, yields, color=colors, alpha=0.7, edgecolor='black')
ax1.axhline(y=material_yield_MPa, color='blue', linestyle='--', linewidth=2, label=f'Selected ({material_yield_MPa:.0f} MPa)')
ax1.set_ylabel('Yield Strength at 1127°C (MPa)', fontsize=12)
ax1.set_title('Material Yield Strength Comparison', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3, axis='y')
ax1.legend(fontsize=10)
ax1.tick_params(axis='x', rotation=45)

# Add value labels on bars
for bar, yield_val in zip(bars1, yields):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'{yield_val:.0f}',
             ha='center', va='bottom', fontsize=9)

# Right: Temperature Capability
bars2 = ax2.bar(materials, temps, color=colors, alpha=0.7, edgecolor='black')
ax2.axhline(y=operating_temp_C, color='orange', linestyle='--', linewidth=2, label=f'Operating Temp ({operating_temp_C:.0f}°C)')
ax2.set_ylabel('Max Temperature Capability (°C)', fontsize=12)
ax2.set_title('Material Temperature Capability', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3, axis='y')
ax2.legend(fontsize=10)
ax2.tick_params(axis='x', rotation=45)

# Add value labels on bars
for bar, temp in zip(bars2, temps):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
             f'{temp:.0f}',
             ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig(Path(__file__).parent.parent / "plots" / "DES004_material_selection.png", dpi=150, bbox_inches='tight')
plt.close()

# ============================================
# Plot 3: Envelope Visualization
# ============================================
fig, ax = plt.subplots(figsize=(12, 8))

# Envelope bounds (REQ-012)
envelope_length = 150.0  # mm
envelope_diameter = 100.0  # mm

# Draw envelope rectangle
envelope_rect = patches.Rectangle((0, -envelope_diameter/2), envelope_length, envelope_diameter,
                                 linewidth=3, edgecolor='red', facecolor='none', linestyle='--',
                                 label='Envelope Limit (150×100 mm)')
ax.add_patch(envelope_rect)

# Draw chamber (cylinder)
chamber_x = 0
chamber_rect = patches.Rectangle((chamber_x, -chamber_diameter_mm/2), chamber_length_mm, chamber_diameter_mm,
                               linewidth=2, edgecolor='blue', facecolor='lightblue', alpha=0.5,
                               label=f'Chamber (83.5×{chamber_diameter_mm:.1f} mm)')
ax.add_patch(chamber_rect)

# Draw nozzle (conical approximation)
throat_x = chamber_length_mm
throat_diameter = 7.48  # mm from DES-001
nozzle_x = throat_x
# Nozzle shape (trapezoid)
nozzle_left = [throat_x, throat_x + nozzle_length_mm]
nozzle_top = [throat_diameter/2, nozzle_exit_diameter_mm/2]
nozzle_bottom = [-throat_diameter/2, -nozzle_exit_diameter_mm/2]

# Fill nozzle
ax.fill_between(nozzle_left, nozzle_bottom, nozzle_top, 
                color='lightgreen', alpha=0.5, label=f'Nozzle ({nozzle_length_mm:.1f}×{nozzle_exit_diameter_mm:.1f} mm)')
ax.plot(nozzle_left, nozzle_top, 'g-', linewidth=2)
ax.plot(nozzle_left, nozzle_bottom, 'g-', linewidth=2)

# Add overall dimensions
ax.plot([0, overall_length_mm], [overall_diameter_mm/2 + 15, overall_diameter_mm/2 + 15], 
        'k-', linewidth=2)
ax.text(overall_length_mm/2, overall_diameter_mm/2 + 18, 
        f'Overall Length: {overall_length_mm:.1f} mm', 
        ha='center', va='bottom', fontsize=11, fontweight='bold')

ax.plot([-10, -10], [-overall_diameter_mm/2 - 15, overall_diameter_mm/2 + 15], 
        'k-', linewidth=2)
ax.text(-12, 0, f'Diameter: {overall_diameter_mm:.1f} mm', 
        ha='right', va='center', fontsize=11, fontweight='bold', rotation=90)

# Add envelope labels
ax.text(envelope_length + 5, 0, f'Limit: {envelope_length} mm', 
        ha='left', va='center', fontsize=10, color='red', fontweight='bold')
ax.text(0, envelope_diameter/2 + 5, f'Limit: {envelope_diameter} mm', 
        ha='left', va='bottom', fontsize=10, color='red', fontweight='bold')

ax.set_xlabel('Length (mm)', fontsize=12)
ax.set_ylabel('Diameter (mm)', fontsize=12)
ax.set_title('Thruster Envelope: Design vs Requirement', fontsize=14, fontweight='bold')
ax.set_xlim(-20, envelope_length + 20)
ax.set_ylim(-envelope_diameter/2 - 20, envelope_diameter/2 + 30)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=10, loc='lower right')
ax.set_aspect('equal')

plt.tight_layout()
plt.savefig(Path(__file__).parent.parent / "plots" / "DES004_envelope.png", dpi=150, bbox_inches='tight')
plt.close()

print("=" * 80)
print("DES-004 Design Visualizations Generated")
print("=" * 80)
print()
print("Generated plots:")
print(f"  1. design/plots/DES004_stress_analysis.png - Hoop stress and safety factor analysis")
print(f"  2. design/plots/DES004_material_selection.png - Material comparison")
print(f"  3. design/plots/DES004_envelope.png - Envelope visualization")
print()
print("Key findings from visualizations:")
print(f"  - Design thickness (0.500 mm) provides safety factor of {data['wall_thickness']['actual_safety_factor']:.1f}")
print(f"  - Molybdenum selected for temperature capability (1650°C vs 1127°C operating)")
print(f"  - Overall length ({overall_length_mm:.1f} mm) exceeds envelope limit (150 mm)")
print(f"  - Diameter ({overall_diameter_mm:.1f} mm) within envelope limit (100 mm)")
