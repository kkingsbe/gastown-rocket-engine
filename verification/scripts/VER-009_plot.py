#!/usr/bin/env python3
"""
VER-009: Instrumentation Verification Plot
Generates visualization of sensor specifications and accuracy
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Configuration
plt.style.use('seaborn-v0_8')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9


def plot_sensor_accuracy():
    """Plot sensor accuracy vs. measurement range"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Pressure transducer data
    pressure_fs = 2.0  # MPa
    pressure_accuracy_pct = 0.25  # %
    pressure_accuracy_MPa = pressure_fs * (pressure_accuracy_pct / 100)
    
    # Temperature sensors data
    catalyst_range = 350  # °C
    catalyst_accuracy = 2.2  # °C
    wall_range = 1200  # °C
    wall_accuracy = 2.2  # °C
    
    # Create sensor positions
    sensors = [
        ('Pressure\nTransducer', pressure_fs, pressure_accuracy_MPa, 'MPa', '#e74c3c'),
        ('Catalyst Bed\nThermocouple', catalyst_range, catalyst_accuracy, '°C', '#3498db'),
        ('Chamber Wall\nThermocouple', wall_range, wall_accuracy, '°C', '#2ecc71')
    ]
    
    # Plot bar chart for sensor accuracy
    x_pos = np.arange(len(sensors))
    accuracies = [s[2] for s in sensors]
    colors = [s[4] for s in sensors]
    
    bars = ax.bar(x_pos, accuracies, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
    
    # Add sensor labels
    ax.set_xticks(x_pos)
    ax.set_xticklabels([s[0] for s in sensors])
    
    # Set y-axis with logarithmic scale
    ax.set_yscale('log')
    ax.set_ylabel('Accuracy (log scale)', fontsize=11, fontweight='bold')
    
    # Add value labels on bars
    for i, (bar, acc) in enumerate(zip(bars, accuracies)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height * 1.1,
                f'±{acc:.3f} {sensors[i][3]}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Add reference lines
    ax.axhline(y=pressure_accuracy_MPa, color='red', linestyle='--', linewidth=1.5, alpha=0.5, label='Pressure accuracy')
    ax.axhline(y=catalyst_accuracy, color='blue', linestyle='--', linewidth=1.5, alpha=0.5, label='Temp accuracy')
    
    # Add full scale annotation
    full_scales = [f"FS: {s[1]:.1f} {s[3]}" for s in sensors]
    for i, text in enumerate(full_scales):
        ax.text(x_pos[i], ax.get_ylim()[0] * 1.5, text, ha='center', va='bottom', fontsize=9)
    
    # Title and labels
    ax.set_title('VER-009: Sensor Accuracy Specifications', fontsize=14, fontweight='bold')
    ax.set_xlabel('Sensor Type', fontsize=11, fontweight='bold')
    ax.legend(loc='upper left', framealpha=0.9)
    
    # Grid
    ax.grid(True, which='both', linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)
    
    # Info box
    info_text = (
        f"Verification: REQ-028, REQ-029\n"
        f"Date: 2026-02-14\n"
        f"Status: PASS\n\n"
        f"Pressure Transducer:\n"
        f"  Range: 0-2.0 MPa\n"
        f"  Accuracy: ±{pressure_accuracy_MPa:.3f} MPa\n"
        f"  Thrust resolution: ±0.024 N\n\n"
        f"Temperature Sensors:\n"
        f"  Count: 2 (catalyst, wall)\n"
        f"  Type: Type K thermocouple\n"
        f"  Accuracy: ±2.2°C"
    )
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.9)
    ax.text(0.98, 0.98, info_text, transform=ax.transAxes, fontsize=8,
            verticalalignment='top', horizontalalignment='right', bbox=props)
    
    # Adjust layout and save
    plt.tight_layout()
    
    output_dir = Path(__file__).parent.parent / "plots"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "VER-009_sensor_accuracy.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"Plot saved: {output_path}")
    return output_path


def plot_sensor_comparison():
    """Plot comparison of sensor specifications side-by-side"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Pressure transducer specifications
    pt_specs = {
        'Range (MPa)': [2.0],
        'Accuracy (MPa)': [0.005],
        'Accuracy (%)': [0.25],
        'Output': ['4-20 mA']
    }
    
    # Temperature sensors specifications
    temp_specs = {
        'Sensor': ['Catalyst Bed', 'Chamber Wall'],
        'Range (°C)': [350, 1200],
        'Accuracy (°C)': [2.2, 2.2],
        'Type (K)': ['Type K', 'Type K']
    }
    
    # Plot 1: Pressure Transducer
    bars1 = ax1.bar(pt_specs.keys(), [pt_specs['Range (MPa)'][0], pt_specs['Accuracy (MPa)'][0], pt_specs['Accuracy (%)'][0], 20], 
                    color=['#e74c3c', '#3498db', '#2ecc71', '#9b59b6'], alpha=0.7, edgecolor='black', linewidth=1.5)
    
    ax1.set_ylabel('Value', fontweight='bold')
    ax1.set_title('Pressure Transducer Specifications', fontsize=12, fontweight='bold')
    ax1.set_xticks(range(len(pt_specs.keys())))
    ax1.set_xticklabels(['Range\n(MPa)', 'Accuracy\n(MPa)', 'Accuracy\n(%)', 'Output'], fontsize=9)
    
    # Add value labels
    for bar, val in zip(bars1[:3], [pt_specs['Range (MPa)'][0], pt_specs['Accuracy (MPa)'][0], pt_specs['Accuracy (%)'][0]]):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height * 1.05, f'{val}', ha='center', va='bottom', fontweight='bold')
    
    # Add text for output bar
    ax1.text(bars1[3].get_x() + bars1[3].get_width()/2., bars1[3].get_height()/2, '4-20 mA', 
             ha='center', va='center', fontweight='bold', color='white')
    
    ax1.grid(True, axis='y', linestyle='--', alpha=0.3)
    
    # Plot 2: Temperature Sensors
    x = np.arange(2)
    width = 0.35
    
    bars2 = ax2.bar(x - width/2, temp_specs['Range (°C)'], width, label='Range (°C)', color='#3498db', alpha=0.7, edgecolor='black', linewidth=1.5)
    bars3 = ax2.bar(x + width/2, [50, 50], width, label='Accuracy (°C)', color='#e74c3c', alpha=0.7, edgecolor='black', linewidth=1.5)
    
    ax2.set_ylabel('Temperature (°C)', fontweight='bold')
    ax2.set_title('Temperature Sensor Specifications', fontsize=12, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(['Catalyst Bed\n(25 mm)', 'Chamber Wall\n(42 mm)'])
    ax2.legend()
    
    # Add value labels
    for bars in [bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            if height > 10:  # Only label visible bars
                ax2.text(bar.get_x() + bar.get_width()/2., height * 1.01, f'{height:.0f}', ha='center', va='bottom', fontsize=8, fontweight='bold')
            else:  # Accuracy bar is small, put label on top
                ax2.text(bar.get_x() + bar.get_width()/2., height + 15, f'±{temp_specs["Accuracy (°C)"][int(bar.get_x()+width/2)]}°C', ha='center', va='bottom', fontsize=8, fontweight='bold')
    
    ax2.grid(True, axis='y', linestyle='--', alpha=0.3)
    
    # Overall title
    fig.suptitle('VER-009: Instrumentation Specifications Comparison', fontsize=14, fontweight='bold', y=1.02)
    
    # Adjust layout and save
    plt.tight_layout()
    
    output_dir = Path(__file__).parent.parent / "plots"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "VER-009_sensor_comparison.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"Plot saved: {output_path}")
    return output_path


def main():
    print("="*80)
    print("VER-009: Instrumentation Verification Plot Generation")
    print("="*80)
    
    plot_sensor_accuracy()
    plot_sensor_comparison()
    
    print("\nAll plots generated successfully.")


if __name__ == "__main__":
    main()
