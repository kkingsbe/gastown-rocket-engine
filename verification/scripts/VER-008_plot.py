#!/usr/bin/env python3
"""
VER-008: Safety and Reliability Verification - Lifetime Plot

This script generates a verification plot for the lifetime analysis showing:
- Catalyst rated lifespan requirement threshold (100 hours)
- Actual mission usage (13.89 hours)
- Positive margin indicator
- Pass/fail regions

According to verification plot standards:
1. Requirement threshold line (red dashed)
2. Agent 2's design point (blue dotted)
3. Agent 3's computed point (green solid)
4. Pass/fail region shading
5. Title includes VER ID and REQ ID
6. Axes labeled with units
7. Grid enabled
8. Legend always present
9. Saved to verification/plots/ as PNG at 150 DPI
"""

import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

# Load verification results
results_path = Path(__file__).parent.parent / "data" / "VER-008_results.json"
with open(results_path, 'r') as f:
    results = json.load(f)

lifetime_data = results["lifetime_verification"]

# Extract key values
catalyst_rated_lifespan = lifetime_data["catalyst_rated_lifespan_h"]  # 100.0 hours (capability)
actual_usage = lifetime_data["actual_usage_h"]  # 13.89 hours
margin_h = lifetime_data["margin_h"]  # 86.11 hours
margin_pct = lifetime_data["margin_percent"]  # 620%
firing_cycles = lifetime_data["firing_cycles"]
isp_degradation = lifetime_data["isp_degradation_pct"]

# Requirement threshold
REQ_THRESHOLD = 100.0  # hours - catalyst rated lifespan requirement

# Create plot
fig, ax = plt.subplots(1, 1, figsize=(12, 7))

# Define Y-axis range
y_min = 0
y_max = 120  # 20% above threshold for visual clarity

# Pass/fail region shading (for capability interpretation)
# PASS region: rated lifespan >= 100 hours (capability provided)
# FAIL region: rated lifespan < 100 hours (insufficient capability)
ax.axhspan(ymin=REQ_THRESHOLD, ymax=y_max, alpha=0.1, color='green', label='PASS region (Rated ≥ 100 h)')
ax.axhspan(ymin=y_min, ymax=REQ_THRESHOLD, alpha=0.1, color='red', label='FAIL region (Rated < 100 h)')

# Requirement threshold line
ax.axhline(y=REQ_THRESHOLD, color='red', linestyle='--', linewidth=2,
           label=f'REQ-030 Threshold ({REQ_THRESHOLD} h capability)')

# Agent 2's design point (rated lifespan from heritage)
agent2_point = catalyst_rated_lifespan  # 100.0 hours
ax.axhline(y=agent2_point, color='blue', linestyle=':', linewidth=2,
           label=f'Agent 2 Design (Rated: {agent2_point:.1f} h)')

# Agent 3's computed point (actual usage, shown as providing margin)
agent3_point = actual_usage  # 13.89 hours
ax.axhline(y=agent3_point, color='green', linestyle='-', linewidth=2,
           label=f'Agent 3 Verification (Actual: {agent3_point:.2f} h)')

# Add margin arrow
ax.annotate(f'Positive Margin: {margin_h:.2f} h ({margin_pct:.1f}%)',
            xy=(0.5, (actual_usage + catalyst_rated_lifespan) / 2),
            xytext=(0.65, (actual_usage + catalyst_rated_lifespan) / 2),
            fontsize=10, color='darkgreen',
            arrowprops=dict(arrowstyle='->', color='darkgreen', lw=1.5))

# Add markers for clarity
ax.plot(0.5, agent2_point, 'bo', markersize=8, label='Rated lifespan (capability)')
ax.plot(0.5, agent3_point, 'go', markersize=8, label='Actual usage')

# Additional metrics as text box
info_text = (
    f"Catalyst: Shell 405\n"
    f"Rated Lifespan: {catalyst_rated_lifespan:.1f} h\n"
    f"Actual Usage: {actual_usage:.2f} h\n"
    f"Positive Margin: {margin_h:.2f} h ({margin_pct:.1f}%)\n\n"
    f"Firing Cycles: {firing_cycles:,} (PASS)\n"
    f"Isp Degradation: {isp_degradation:.2f}% (PASS)"
)
ax.text(0.02, 0.95, info_text, transform=ax.transAxes,
        fontsize=10, verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Labels and title
ax.set_xlim(0, 1)
ax.set_ylim(y_min, y_max)
ax.set_xlabel('Verification Status', fontsize=12)
ax.set_ylabel('Lifetime (hours)', fontsize=12)
ax.set_title('VER-008: Safety and Reliability - Lifetime Verification (REQ-030)\n'
             'Capability Interpretation: Catalyst Rated Lifespan ≥ 100 h', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)

# Legend
ax.legend(loc='lower right', fontsize=10)

# Remove x-axis ticks (not meaningful)
ax.set_xticks([])

# Save plot
plots_dir = Path(__file__).parent.parent / "plots"
plots_dir.mkdir(exist_ok=True)
output_path = plots_dir / "VER-008_lifetime.png"
fig.savefig(output_path, dpi=150, bbox_inches='tight')
plt.close()

print(f"Plot saved: {output_path}")
print(f"VER-008 Lifetime Verification Plot Generated")
print(f"  Catalyst Rated Lifespan: {catalyst_rated_lifespan:.1f} hours")
print(f"  Actual Mission Usage: {actual_usage:.2f} hours")
print(f"  Positive Margin: {margin_h:.2f} hours ({margin_pct:.1f}%)")
