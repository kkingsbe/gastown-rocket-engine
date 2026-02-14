#!/usr/bin/env python3
"""
DES-005: Physical Envelope and Mechanical Interface Design Visualization
Generates visual diagrams for the thruster mechanical layout and interface specifications.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle, Rectangle, Polygon, FancyArrowPatch
import json

# Physical constants and design parameters from prior design tasks
DESIGN_DATA = {
    # Chamber dimensions (from DES-004)
    "chamber_diameter_mm": 22.4,
    "chamber_length_mm": 83.5,
    "chamber_radius_mm": 11.2,

    # Nozzle dimensions (from DES-001/DES-004)
    "throat_diameter_mm": 7.48,
    "throat_radius_mm": 3.74,
    "exit_diameter_mm": 74.8,
    "exit_radius_mm": 37.4,
    "nozzle_length_mm": 125.6,
    "half_angle_deg": 15.0,

    # Mounting interface (REQ-013)
    "mounting_bolt_circle_diameter_mm": 80.0,
    "mounting_bolt_circle_radius_mm": 40.0,
    "mounting_bolt_size": "M6",
    "mounting_bolt_count": 4,
    "mounting_flange_diameter_mm": 90.0,
    "mounting_flange_thickness_mm": 5.0,

    # Envelope constraints (REQ-012)
    "envelope_diameter_mm": 100.0,
    "envelope_length_mm": 150.0,

    # Propellant inlet (REQ-026)
    "inlet_fitting": "1/4 AN flare",

    # Mass
    "chamber_mass_kg": 0.0391,
    "nozzle_mass_kg": 0.0220,
    "flange_mass_kg": 0.1691,
    "injector_mass_kg": 0.0376,
    "inlet_mass_kg": 0.0120,
    "total_dry_mass_kg": 0.2798,
}

def create_side_view():
    """Create side view diagram of thruster assembly."""
    fig, ax = plt.subplots(figsize=(12, 8))

    # Set up coordinate system (origin at nozzle exit, positive to rear)
    nozzle_exit_x = 0
    throat_x = DESIGN_DATA["nozzle_length_mm"]
    chamber_end_x = throat_x + DESIGN_DATA["chamber_length_mm"]
    flange_end_x = chamber_end_x + DESIGN_DATA["mounting_flange_thickness_mm"]

    y_center = 0

    # Draw envelope constraint (150 mm length from nozzle exit to limit)
    envelope_limit = DESIGN_DATA["envelope_length_mm"]
    envelope = Rectangle((envelope_limit, -50), 5, 100,
                         edgecolor='red', facecolor='none',
                         linestyle='--', linewidth=2, label='Envelope Limit (150 mm)')
    ax.add_patch(envelope)

    # Draw envelope width constraint (100 mm diameter)
    envelope_width = Rectangle((0, -DESIGN_DATA["envelope_diameter_mm"]/2),
                               chamber_end_x + 20, DESIGN_DATA["envelope_diameter_mm"],
                               edgecolor='orange', facecolor='none',
                               linestyle=':', linewidth=1, alpha=0.5, label='Envelope Width (100 mm)')

    # Draw nozzle (conical)
    nozzle_upper = [
        (nozzle_exit_x, DESIGN_DATA["exit_radius_mm"]),
        (throat_x, DESIGN_DATA["throat_radius_mm"])
    ]
    nozzle_lower = [
        (nozzle_exit_x, -DESIGN_DATA["exit_radius_mm"]),
        (throat_x, -DESIGN_DATA["throat_radius_mm"])
    ]

    nozzle_poly = Polygon(nozzle_upper + [(throat_x, -DESIGN_DATA["throat_radius_mm"]),
                                           (nozzle_exit_x, -DESIGN_DATA["exit_radius_mm"])],
                          edgecolor='blue', facecolor='lightblue', alpha=0.7,
                          linewidth=2, label='Nozzle (Molybdenum)')
    ax.add_patch(nozzle_poly)

    # Draw chamber
    chamber_upper = [
        (throat_x, DESIGN_DATA["chamber_radius_mm"]),
        (chamber_end_x, DESIGN_DATA["chamber_radius_mm"])
    ]
    chamber_lower = [
        (throat_x, -DESIGN_DATA["chamber_radius_mm"]),
        (chamber_end_x, -DESIGN_DATA["chamber_radius_mm"])
    ]

    chamber_poly = Rectangle((throat_x, -DESIGN_DATA["chamber_radius_mm"]),
                             DESIGN_DATA["chamber_length_mm"],
                             2*DESIGN_DATA["chamber_radius_mm"],
                             edgecolor='green', facecolor='lightgreen', alpha=0.7,
                             linewidth=2, label='Chamber (Molybdenum)')
    ax.add_patch(chamber_poly)

    # Draw mounting flange
    flange_upper = [
        (chamber_end_x, DESIGN_DATA["mounting_flange_diameter_mm"]/2),
        (flange_end_x, DESIGN_DATA["mounting_flange_diameter_mm"]/2)
    ]
    flange_lower = [
        (chamber_end_x, -DESIGN_DATA["mounting_flange_diameter_mm"]/2),
        (flange_end_x, -DESIGN_DATA["mounting_flange_diameter_mm"]/2)
    ]

    flange_poly = Rectangle((chamber_end_x, -DESIGN_DATA["mounting_flange_diameter_mm"]/2),
                            DESIGN_DATA["mounting_flange_thickness_mm"],
                            DESIGN_DATA["mounting_flange_diameter_mm"],
                            edgecolor='purple', facecolor='plum', alpha=0.7,
                            linewidth=2, label='Mounting Flange (316L SS)')
    ax.add_patch(flange_poly)

    # Draw mounting bolts (4-hole pattern)
    bolt_positions = [
        (flange_end_x - 2, DESIGN_DATA["mounting_bolt_circle_radius_mm"]),
        (flange_end_x - 2, -DESIGN_DATA["mounting_bolt_circle_radius_mm"]),
    ]
    for bx, by in bolt_positions:
        bolt = Circle((bx, by), 3.25, edgecolor='black', facecolor='gray',
                      linewidth=1.5, label='M6 Bolt' if bx == bolt_positions[0][0] else '')
        ax.add_patch(bolt)

    # Draw propellant inlet
    inlet_length = 15
    inlet_height = 6
    inlet_x = chamber_end_x - DESIGN_DATA["chamber_length_mm"] + 15
    inlet_y = DESIGN_DATA["chamber_radius_mm"]

    inlet_poly = Polygon([
        (inlet_x, inlet_y),
        (inlet_x + inlet_length, inlet_y),
        (inlet_x + inlet_length, inlet_y + inlet_height),
        (inlet_x, inlet_y + inlet_height)
    ], edgecolor='brown', facecolor='tan', alpha=0.7,
       linewidth=2, label='Propellant Inlet (1/4" AN Flare)')
    ax.add_patch(inlet_poly)

    # Add dimension lines
    ax.annotate(f'{DESIGN_DATA["nozzle_length_mm"]} mm',
               xy=(throat_x, DESIGN_DATA["exit_radius_mm"] + 5),
               xytext=(nozzle_exit_x, DESIGN_DATA["exit_radius_mm"] + 5),
               arrowprops=dict(arrowstyle='<->', color='black'),
               fontsize=10, ha='center', va='bottom')

    ax.annotate(f'{DESIGN_DATA["chamber_length_mm"]} mm',
               xy=(throat_x, DESIGN_DATA["chamber_radius_mm"] + 8),
               xytext=(chamber_end_x, DESIGN_DATA["chamber_radius_mm"] + 8),
               arrowprops=dict(arrowstyle='<->', color='black'),
               fontsize=10, ha='center', va='bottom')

    # Overall length annotation
    ax.annotate(f'Overall: {flange_end_x:.1f} mm (exceeds 150 mm)',
               xy=(nozzle_exit_x, DESIGN_DATA["exit_radius_mm"] + 15),
               xytext=(flange_end_x, DESIGN_DATA["exit_radius_mm"] + 15),
               arrowprops=dict(arrowstyle='<->', color='red'),
               fontsize=10, ha='center', va='bottom', color='red')

    # Labels
    ax.text(nozzle_exit_x + DESIGN_DATA["nozzle_length_mm"]/2, 0, 'NOZZLE',
            ha='center', va='center', fontsize=8, fontweight='bold')
    ax.text(throat_x + DESIGN_DATA["chamber_length_mm"]/2, 0, 'CHAMBER',
            ha='center', va='center', fontsize=8, fontweight='bold')
    ax.text(chamber_end_x + DESIGN_DATA["mounting_flange_thickness_mm"]/2,
            0, 'FLANGE', ha='center', va='center', fontsize=8, fontweight='bold')

    # Set plot limits and labels
    ax.set_xlim(-10, flange_end_x + 30)
    ax.set_ylim(-50, 50)
    ax.set_aspect('equal')
    ax.set_xlabel('Axial Position (mm)')
    ax.set_ylabel('Radial Position (mm)')
    ax.set_title('DES-005: Thruster Side View - Mechanical Layout')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper right', fontsize=8)

    plt.tight_layout()
    plt.savefig('design/plots/DES005_side_view.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Created: design/plots/DES005_side_view.png")

def create_top_view():
    """Create top view diagram of mounting interface."""
    fig, ax = plt.subplots(figsize=(10, 10))

    # Draw mounting flange (circle)
    flange_circle = Circle((0, 0), DESIGN_DATA["mounting_flange_diameter_mm"]/2,
                           edgecolor='purple', facecolor='plum', alpha=0.7,
                           linewidth=2, label='Mounting Flange (90 mm Ø)')
    ax.add_patch(flange_circle)

    # Draw chamber (inner circle)
    chamber_circle = Circle((0, 0), DESIGN_DATA["chamber_diameter_mm"]/2,
                            edgecolor='green', facecolor='lightgreen', alpha=0.7,
                            linewidth=2, label='Chamber (22.4 mm Ø)')
    ax.add_patch(chamber_circle)

    # Draw bolt circle (dashed)
    bolt_circle = Circle((0, 0), DESIGN_DATA["mounting_bolt_circle_radius_mm"],
                         edgecolor='blue', facecolor='none',
                         linestyle='--', linewidth=1.5, label='Bolt Circle (80 mm Ø)')
    ax.add_patch(bolt_circle)

    # Draw bolt holes (4-hole pattern, 90° spacing)
    bolt_angle = [0, 90, 180, 270]
    for i, angle in enumerate(bolt_angle):
        angle_rad = angle * 3.14159 / 180
        bx = DESIGN_DATA["mounting_bolt_circle_radius_mm"] * (3.14159/180 if angle == 0 else 0)
        by = DESIGN_DATA["mounting_bolt_circle_radius_mm"] * (1 if angle == 90 else -1 if angle == 270 else 0)

        # Recalculate positions properly
        if angle == 0:
            bx, by = DESIGN_DATA["mounting_bolt_circle_radius_mm"], 0
        elif angle == 90:
            bx, by = 0, DESIGN_DATA["mounting_bolt_circle_radius_mm"]
        elif angle == 180:
            bx, by = -DESIGN_DATA["mounting_bolt_circle_radius_mm"], 0
        else:  # 270
            bx, by = 0, -DESIGN_DATA["mounting_bolt_circle_radius_mm"]

        bolt_hole = Circle((bx, by), 3.25, edgecolor='black', facecolor='gray',
                           linewidth=1.5, label='M6 Bolt Hole' if i == 0 else '')
        ax.add_patch(bolt_hole)

        # Label bolt numbers
        ax.text(bx, by + 6, f'Bolt {i+1}', ha='center', va='bottom', fontsize=8)

    # Add dimension for bolt circle diameter
    ax.annotate(f'{DESIGN_DATA["mounting_bolt_circle_diameter_mm"]} mm BCD',
               xy=(0, DESIGN_DATA["mounting_bolt_circle_radius_mm"]),
               xytext=(0, -DESIGN_DATA["mounting_bolt_circle_radius_mm"]),
               arrowprops=dict(arrowstyle='<->', color='blue'),
               fontsize=10, ha='right', va='center', color='blue')

    # Add dimension for flange diameter
    ax.annotate(f'{DESIGN_DATA["mounting_flange_diameter_mm"]} mm Ø',
               xy=(DESIGN_DATA["mounting_flange_diameter_mm"]/2, 0),
               xytext=(-DESIGN_DATA["mounting_flange_diameter_mm"]/2, 0),
               arrowprops=dict(arrowstyle='<->', color='purple'),
               fontsize=10, ha='right', va='top', color='purple')

    # Labels
    ax.text(0, 0, 'CHAMBER', ha='center', va='center', fontsize=8, fontweight='bold')

    # Set plot limits and labels
    limit = DESIGN_DATA["mounting_flange_diameter_mm"]/2 + 10
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.set_aspect('equal')
    ax.set_xlabel('X Position (mm)')
    ax.set_ylabel('Y Position (mm)')
    ax.set_title('DES-005: Mounting Interface - Top View (4-Hole Pattern)')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper right', fontsize=8)

    plt.tight_layout()
    plt.savefig('design/plots/DES005_mounting_top_view.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Created: design/plots/DES005_mounting_top_view.png")

def create_envelope_diagram():
    """Create envelope constraint diagram."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Left plot: Side view envelope
    ax1.set_title('Side View Envelope Compliance', fontsize=12, fontweight='bold')

    # Draw envelope rectangle (requirement)
    env_rect = Rectangle((DESIGN_DATA["envelope_length_mm"], -DESIGN_DATA["envelope_diameter_mm"]/2),
                         5, DESIGN_DATA["envelope_diameter_mm"],
                         edgecolor='red', facecolor='none',
                         linestyle='--', linewidth=3, label='Requirement (100×150 mm)')
    ax1.add_patch(env_rect)

    # Draw actual thruster outline
    actual_length = DESIGN_DATA["nozzle_length_mm"] + DESIGN_DATA["chamber_length_mm"] + DESIGN_DATA["mounting_flange_thickness_mm"]
    actual_diameter = DESIGN_DATA["exit_diameter_mm"]

    # Nozzle
    nozzle_poly = Polygon([
        (0, actual_diameter/2),
        (DESIGN_DATA["nozzle_length_mm"], DESIGN_DATA["throat_diameter_mm"]/2),
        (DESIGN_DATA["nozzle_length_mm"], -DESIGN_DATA["throat_diameter_mm"]/2),
        (0, -actual_diameter/2)
    ], edgecolor='blue', facecolor='lightblue', alpha=0.7, linewidth=2, label='Actual Thruster')
    ax1.add_patch(nozzle_poly)

    # Chamber + Flange
    chamber_poly = Rectangle((DESIGN_DATA["nozzle_length_mm"], -DESIGN_DATA["chamber_diameter_mm"]/2),
                             DESIGN_DATA["chamber_length_mm"] + DESIGN_DATA["mounting_flange_thickness_mm"],
                             DESIGN_DATA["chamber_diameter_mm"],
                             edgecolor='green', facecolor='lightgreen', alpha=0.7, linewidth=2)
    ax1.add_patch(chamber_poly)

    # Annotations
    ax1.text(actual_length/2, actual_diameter/2 + 5,
             f'Actual: {actual_length:.1f} × {actual_diameter:.1f} mm',
             ha='center', va='bottom', fontsize=10, fontweight='bold', color='blue')
    ax1.text(DESIGN_DATA["envelope_length_mm"]/2, -DESIGN_DATA["envelope_diameter_mm"]/2 - 5,
             f'Requirement: {DESIGN_DATA["envelope_length_mm"]} × {DESIGN_DATA["envelope_diameter_mm"]} mm',
             ha='center', va='top', fontsize=10, fontweight='bold', color='red')

    ax1.set_xlim(-10, actual_length + 20)
    ax1.set_ylim(-DESIGN_DATA["envelope_diameter_mm"]/2 - 10, DESIGN_DATA["envelope_diameter_mm"]/2 + 10)
    ax1.set_xlabel('Length (mm)')
    ax1.set_ylabel('Diameter (mm)')
    ax1.set_aspect('equal')
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc='upper right', fontsize=9)

    # Right plot: Compliance bar chart
    ax2.set_title('Envelope Compliance Summary', fontsize=12, fontweight='bold')

    categories = ['Diameter (mm)', 'Length (mm)']
    actual = [DESIGN_DATA["exit_diameter_mm"], actual_length]
    requirement = [DESIGN_DATA["envelope_diameter_mm"], DESIGN_DATA["envelope_length_mm"]]
    compliance = [actual[0] <= requirement[0], actual[1] <= requirement[1]]
    colors = ['green' if c else 'red' for c in compliance]

    x = [0, 1]
    width = 0.35

    bars1 = ax2.bar([i - width/2 for i in x], actual, width, label='Actual', alpha=0.8)
    bars2 = ax2.bar([i + width/2 for i in x], requirement, width, label='Requirement', alpha=0.8)

    # Color the bars based on compliance
    for i, (bar, comp) in enumerate(zip(bars1, compliance)):
        bar.set_color('green' if comp else 'red')

    ax2.set_xticks(x)
    ax2.set_xticklabels(categories)
    ax2.set_ylabel('Dimension (mm)')
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')

    # Add compliance text
    for i, (act, req, comp) in enumerate(zip(actual, requirement, compliance)):
        status = 'PASS' if comp else 'FAIL'
        margin = abs(req - act)
        ax2.text(i, max(act, req) + 5, f'{status}\nMargin: {margin:.1f} mm',
                 ha='center', va='bottom', fontsize=10, fontweight='bold',
                 color='green' if comp else 'red')

    plt.tight_layout()
    plt.savefig('design/plots/DES005_envelope_compliance.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Created: design/plots/DES005_envelope_compliance.png")

def create_mass_breakdown_chart():
    """Create mass breakdown pie chart."""
    fig, ax = plt.subplots(figsize=(10, 8))

    labels = ['Chamber\n(Mo)', 'Nozzle\n(Mo)', 'Mounting Flange\n(316L SS)',
              'Injector\n(316L SS)', 'Propellant Inlet\n(316L SS)']
    sizes = [DESIGN_DATA["chamber_mass_kg"], DESIGN_DATA["nozzle_mass_kg"],
             DESIGN_DATA["flange_mass_kg"], DESIGN_DATA["injector_mass_kg"],
             DESIGN_DATA["inlet_mass_kg"]]
    colors = ['lightgreen', 'lightblue', 'plum', 'lightcoral', 'tan']
    explode = (0.05, 0.05, 0, 0, 0)

    wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, colors=colors,
                                       autopct='%1.1f%%', shadow=True, startangle=90)

    for autotext in autotexts:
        autotext.set_fontsize(10)
        autotext.set_fontweight('bold')

    # Add total mass annotation
    total_mass = sum(sizes)
    budget = 0.5
    margin = budget - total_mass
    ax.text(0, -1.3, f'Total Dry Mass: {total_mass:.4f} kg\n'
                     f'Budget: {budget:.2f} kg\n'
                     f'Margin: {margin:.4f} kg ({margin/budget*100:.1f}%)',
             ha='center', va='center', fontsize=11, fontweight='bold',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    ax.set_title('DES-005: Dry Mass Breakdown\n(REQ-011: ≤ 0.5 kg)',
                 fontsize=12, fontweight='bold')

    plt.tight_layout()
    plt.savefig('design/plots/DES005_mass_breakdown.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Created: design/plots/DES005_mass_breakdown.png")

def main():
    """Generate all visualizations."""
    print("=" * 60)
    print("DES-005: Physical Envelope and Mechanical Interface Design")
    print("Visualization Generation")
    print("=" * 60)

    # Create all plots
    create_side_view()
    create_top_view()
    create_envelope_diagram()
    create_mass_breakdown_chart()

    print("\n" + "=" * 60)
    print("All visualizations generated successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()
