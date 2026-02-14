#!/usr/bin/env python3
"""
chamber_nozzle_stress.py - Chamber and Nozzle Structural Sizing
DES-004: Structural analysis of chamber and nozzle for hydrazine monopropellant thruster

This script calculates:
- Required chamber wall thickness to withstand MEOP with 1.5x safety factor
- Material selection based on temperature and structural requirements
- Chamber mass and dimensions
- Verification against envelope and mass constraints

Physical Constants and Assumptions (from CONTEXT.md):
- g0 = 9.80665 m/s² (standard gravitational acceleration, exact)
- Thin-wall pressure vessel theory: sigma_hoop = P * r / t
- Required thickness: t_min = (P * SF * r) / sigma_yield_at_temp

Requirements Traced:
- REQ-015: Chamber wall temperature ≤ 1400°C
- REQ-016: Nozzle exit temperature ≤ 800°C
- REQ-018: Chamber withstand MEOP × 1.5 safety factor
- REQ-023: Chamber material compatible with hydrazine products
- REQ-024: Nozzle material is refractory metal or high-temperature alloy (≥1400°C)
- REQ-011: Dry mass ≤ 0.5 kg
- REQ-012: Envelope: 100 mm diameter × 150 mm length
"""

import json
import math
import sys
from pathlib import Path

# Physical constants (from CONTEXT.md)
G0 = 9.80665  # m/s², standard gravitational acceleration (exact)
PI = math.pi

# Material properties (from CONTEXT.md Section 4)
# All materials have heritage flight data (space-qualified)
MATERIALS = {
    "Inconel_625": {
        "name": "Inconel 625",
        "max_temp_C": 980.0,
        "density_kg_m3": 8440.0,
        "yield_strength_RTMpa": 460.0,
        "hydrazine_compatible": True,
        "heritage": "Excellent hydrazine compatibility"
    },
    "Inconel_718": {
        "name": "Inconel 718",
        "max_temp_C": 700.0,
        "density_kg_m3": 8190.0,
        "yield_strength_RTMpa": 1035.0,
        "hydrazine_compatible": True,
        "heritage": "Limited above 700°C"
    },
    "Haynes_230": {
        "name": "Haynes 230",
        "max_temp_C": 1150.0,
        "density_kg_m3": 8970.0,
        "yield_strength_RTMpa": 390.0,
        "hydrazine_compatible": True,
        "heritage": "Excellent high-temperature"
    },
    "Molybdenum": {
        "name": "Molybdenum (Mo)",
        "max_temp_C": 1650.0,
        "density_kg_m3": 10220.0,
        "yield_strength_RTMpa": 560.0,
        "hydrazine_compatible": True,
        "heritage": "Needs coating in oxidizing environment"
    },
    "Rhenium": {
        "name": "Rhenium (Re)",
        "max_temp_C": 2000.0,
        "density_kg_m3": 21020.0,
        "yield_strength_RTMpa": 290.0,
        "hydrazine_compatible": True,
        "heritage": "Excellent, expensive"
    },
    "Columbium_C103": {
        "name": "Columbium C103 (Nb alloy)",
        "max_temp_C": 1370.0,
        "density_kg_m3": 8850.0,
        "yield_strength_RTMpa": 240.0,
        "hydrazine_compatible": True,
        "heritage": "Heritage material for small thrusters"
    }
}

# Yield strength degradation at high temperature (simplified model)
# At 1000°C, yield strength is typically 30-50% of RT value
TEMP_DEGRADATION_FACTOR = 0.4  # Conservative: 40% of RT yield strength at operating temp

# Requirements thresholds (from REQ_REGISTER.md)
MEOP_MPa = 0.30  # Maximum Expected Operating Pressure from REQ-009
SAFETY_FACTOR = 1.5  # From REQ-018
CHAMBER_MAX_TEMP_C = 1400.0  # From REQ-015
NOZZLE_MAX_TEMP_C = 800.0  # From REQ-016
MASS_BUDGET_kg = 0.5  # From REQ-011
ENVELOPE_DIAMETER_mm = 100.0  # From REQ-012
ENVELOPE_LENGTH_mm = 150.0  # From REQ-012
MIN_MANUFACTURABLE_THICKNESS_MM = 0.5  # Practical minimum for thin-wall vessels


def load_des001_data():
    """Load DES-001 thruster performance data"""
    des001_path = Path(__file__).parent.parent / "data" / "thruster_performance_sizing.json"
    with open(des001_path, 'r') as f:
        return json.load(f)


def select_material(materials_dict, chamber_temp_C, include_nozzle=False):
    """
    Select material for chamber (and optionally nozzle) based on temperature requirements.
    
    Returns:
        dict: Best material choice with justification
    """
    # Filter materials that can handle chamber temperature
    viable_materials = {
        key: mat for key, mat in materials_dict.items()
        if mat["max_temp_C"] >= chamber_temp_C and mat["hydrazine_compatible"]
    }
    
    if not viable_materials:
        raise ValueError(f"No material found for chamber temperature {chamber_temp_C}°C")
    
    # Rank by yield strength (higher is better for structural requirements)
    sorted_materials = sorted(
        viable_materials.items(),
        key=lambda x: x[1]["yield_strength_RTMpa"],
        reverse=True
    )
    
    best_material_key, best_material = sorted_materials[0]
    
    # Calculate effective yield strength at operating temperature
    effective_yield = best_material["yield_strength_RTMpa"] * TEMP_DEGRADATION_FACTOR
    
    result = {
        "material_key": best_material_key,
        "material_name": best_material["name"],
        "max_temp_C": best_material["max_temp_C"],
        "density_kg_m3": best_material["density_kg_m3"],
        "yield_strength_RTMpa": best_material["yield_strength_RTMpa"],
        "effective_yield_op_temp_MPa": effective_yield,
        "hydrazine_compatible": best_material["hydrazine_compatible"],
        "heritage": best_material["heritage"],
        "rejected_materials": [
            {
                "name": mat["name"],
                "reason": f"Max temp {mat['max_temp_C']}°C < required {chamber_temp_C}°C"
                if mat["max_temp_C"] < chamber_temp_C
                else "Lower yield strength"
            }
            for key, mat in materials_dict.items()
            if key != best_material_key and mat["hydrazine_compatible"]
        ]
    }
    
    return result


def calculate_chamber_geometry(des001_data, chamber_radius_mm):
    """
    Calculate chamber dimensions based on throat area and contraction ratio.
    
    From CONTEXT.md Section 3:
    - Chamber diameter Dc ~ 2-4 * Dt (typical contraction ratio)
    - L_chamber ~ L_star * At / Ac (where L_star = 0.5-1.0 m for hydrazine)
    """
    throat_diameter_mm = des001_data["computed_results"]["throat_diameter_mm"]
    throat_area_m2 = des001_data["computed_results"]["throat_area_m2"]
    
    # Contraction ratio (Dc / Dt)
    contraction_ratio = chamber_radius_mm * 2 / throat_diameter_mm
    
    # Calculate chamber area
    chamber_diameter_m = 2 * chamber_radius_mm / 1000
    chamber_area_m2 = PI * (chamber_diameter_m / 2) ** 2
    
    # Characteristic length L_star (0.5-1.0 m for hydrazine, from CONTEXT.md)
    L_star = 0.75  # m (midpoint of 0.5-1.0 m range)
    
    # Chamber length (volume = L_star * throat_area = Ac * L_chamber)
    chamber_length_m = L_star * throat_area_m2 / chamber_area_m2
    chamber_length_mm = chamber_length_m * 1000
    
    return {
        "chamber_radius_mm": chamber_radius_mm,
        "chamber_diameter_mm": chamber_diameter_m * 1000,
        "contraction_ratio": contraction_ratio,
        "chamber_area_m2": chamber_area_m2,
        "chamber_length_m": chamber_length_m,
        "chamber_length_mm": chamber_length_mm,
        "throat_diameter_mm": throat_diameter_mm,
        "L_star_m": L_star
    }


def calculate_wall_thickness(design_pressure_Pa, chamber_radius_m, material_yield_MPa, safety_factor):
    """
    Calculate minimum wall thickness using thin-wall pressure vessel theory.
    
    From CONTEXT.md Section 9:
    - Hoop stress: sigma_hoop = Pc * r / t
    - Required thickness: t_min = (Pc * SF * r) / sigma_yield_at_temp
    """
    # Convert pressure to Pa and yield strength to Pa
    design_pressure_Pa = float(design_pressure_Pa)
    material_yield_Pa = material_yield_MPa * 1e6
    
    # Calculate required thickness
    required_thickness_m = (design_pressure_Pa * safety_factor * chamber_radius_m) / material_yield_Pa
    required_thickness_mm = required_thickness_m * 1000
    
    # Apply manufacturability constraint
    design_thickness_mm = max(required_thickness_mm, MIN_MANUFACTURABLE_THICKNESS_MM)
    design_thickness_m = design_thickness_mm / 1000
    
    # Calculate actual safety factor with design thickness
    actual_safety_factor = (design_thickness_m * material_yield_Pa) / (design_pressure_Pa * chamber_radius_m)
    
    # Calculate actual hoop stress
    actual_hoop_stress_Pa = (design_pressure_Pa * chamber_radius_m) / design_thickness_m
    actual_hoop_stress_MPa = actual_hoop_stress_Pa / 1e6
    
    return {
        "required_thickness_mm": required_thickness_mm,
        "design_thickness_mm": design_thickness_mm,
        "required_thickness_m": required_thickness_m,
        "design_thickness_m": design_thickness_m,
        "actual_safety_factor": actual_safety_factor,
        "actual_hoop_stress_MPa": actual_hoop_stress_MPa,
        "material_yield_at_temp_MPa": material_yield_MPa,
        "stress_margin_percent": ((material_yield_MPa - actual_hoop_stress_MPa) / material_yield_MPa) * 100
    }


def calculate_chamber_mass(chamber_geometry, thickness_mm, density_kg_m3):
    """
    Calculate chamber mass using cylindrical shell volume.
    """
    chamber_radius_m = chamber_geometry["chamber_radius_mm"] / 1000
    chamber_length_m = chamber_geometry["chamber_length_m"]
    thickness_m = thickness_mm / 1000
    
    # Outer dimensions
    outer_radius = chamber_radius_m + thickness_m
    
    # Cylindrical shell volume (including end caps - simplified as cylinder)
    volume_m3 = PI * (outer_radius**2 - chamber_radius_m**2) * chamber_length_m
    
    # Add approximated mass for end caps (hemispherical)
    end_cap_volume = (4/3) * PI * (outer_radius**3 - chamber_radius_m**3)
    total_volume_m3 = volume_m3 + end_cap_volume
    
    mass_kg = total_volume_m3 * density_kg_m3
    
    return {
        "volume_m3": total_volume_m3,
        "mass_kg": mass_kg
    }


def calculate_nozzle_properties(des001_data):
    """
    Calculate nozzle properties and verify temperature constraints.
    """
    exit_diameter_mm = des001_data["computed_results"]["exit_diameter_mm"]
    nozzle_length_mm = des001_data["computed_results"]["nozzle_length_mm"]
    exit_temperature_K = des001_data["computed_results"]["exit_temperature_K"]
    exit_temperature_C = exit_temperature_K - 273.15
    
    # Verify envelope constraints
    envelope_check_diameter = exit_diameter_mm <= ENVELOPE_DIAMETER_mm
    envelope_check_length = nozzle_length_mm <= ENVELOPE_LENGTH_mm
    
    # Verify temperature constraint
    temp_check = exit_temperature_C <= NOZZLE_MAX_TEMP_C
    
    return {
        "exit_diameter_mm": exit_diameter_mm,
        "nozzle_length_mm": nozzle_length_mm,
        "exit_temperature_C": exit_temperature_C,
        "exit_temperature_K": exit_temperature_K,
        "envelope_diameter_check": envelope_check_diameter,
        "envelope_length_check": envelope_check_length,
        "temp_constraint_check": temp_check,
        "temp_margin_C": NOZZLE_MAX_TEMP_C - exit_temperature_C
    }


def check_mass_budget(chamber_mass_kg):
    """
    Verify chamber mass against dry mass budget.
    """
    mass_check = chamber_mass_kg <= MASS_BUDGET_kg
    mass_margin_kg = MASS_BUDGET_kg - chamber_mass_kg
    mass_margin_percent = (mass_margin_kg / MASS_BUDGET_kg) * 100
    
    return {
        "chamber_mass_kg": chamber_mass_kg,
        "mass_budget_kg": MASS_BUDGET_kg,
        "mass_check": mass_check,
        "mass_margin_kg": mass_margin_kg,
        "mass_margin_percent": mass_margin_percent
    }


def check_envelope_constraints(chamber_diameter_mm, chamber_length_mm, nozzle_diameter_mm, nozzle_length_mm):
    """
    Verify overall thruster fits within envelope constraints.
    """
    # Overall dimensions (chamber + nozzle in series)
    overall_length_mm = chamber_length_mm + nozzle_length_mm
    overall_diameter_mm = max(chamber_diameter_mm, nozzle_diameter_mm)
    
    diameter_check = overall_diameter_mm <= ENVELOPE_DIAMETER_mm
    length_check = overall_length_mm <= ENVELOPE_LENGTH_mm
    
    return {
        "overall_diameter_mm": overall_diameter_mm,
        "overall_length_mm": overall_length_mm,
        "diameter_check": diameter_check,
        "length_check": length_check,
        "diameter_margin_mm": ENVELOPE_DIAMETER_mm - overall_diameter_mm,
        "length_margin_mm": ENVELOPE_LENGTH_mm - overall_length_mm
    }


def main():
    print("=" * 80)
    print("DES-004: Chamber and Nozzle Structural Sizing")
    print("=" * 80)
    print()
    
    # Load DES-001 data
    print("Loading DES-001 thruster performance data...")
    des001_data = load_des001_data()
    chamber_pressure_MPa = des001_data["parameters"]["chamber_pressure_MPa"]
    chamber_temperature_K = des001_data["parameters"]["chamber_temperature_K"]
    chamber_temperature_C = chamber_temperature_K - 273.15
    throat_diameter_mm = des001_data["computed_results"]["throat_diameter_mm"]
    
    print(f"  Chamber pressure: {chamber_pressure_MPa:.2f} MPa")
    print(f"  Chamber temperature: {chamber_temperature_C:.1f}°C")
    print(f"  Throat diameter: {throat_diameter_mm:.2f} mm")
    print()
    
    # Step 1: Material selection
    print("Step 1: Material Selection")
    print("-" * 80)
    material_selection = select_material(MATERIALS, chamber_temperature_C)
    print(f"Selected material: {material_selection['material_name']}")
    print(f"  Max temperature: {material_selection['max_temp_C']}°C (required: {chamber_temperature_C:.1f}°C)")
    print(f"  Density: {material_selection['density_kg_m3']} kg/m³")
    print(f"  RT yield strength: {material_selection['yield_strength_RTMpa']} MPa")
    print(f"  Effective yield at {chamber_temperature_C:.0f}°C: {material_selection['effective_yield_op_temp_MPa']:.1f} MPa")
    print(f"  Heritage: {material_selection['heritage']}")
    print()
    
    # Step 2: Chamber geometry sizing
    print("Step 2: Chamber Geometry Sizing")
    print("-" * 80)
    # Initial chamber diameter guess: 3x throat diameter (typical contraction ratio)
    chamber_radius_mm = (throat_diameter_mm * 3) / 2
    chamber_geometry = calculate_chamber_geometry(des001_data, chamber_radius_mm)
    
    print(f"Chamber dimensions:")
    print(f"  Chamber diameter: {chamber_geometry['chamber_diameter_mm']:.1f} mm")
    print(f"  Chamber radius: {chamber_geometry['chamber_radius_mm']:.1f} mm")
    print(f"  Chamber length: {chamber_geometry['chamber_length_mm']:.1f} mm")
    print(f"  Contraction ratio (Dc/Dt): {chamber_geometry['contraction_ratio']:.1f}")
    print(f"  Characteristic length (L*): {chamber_geometry['L_star_m']:.2f} m")
    print()
    
    # Step 3: Wall thickness calculation
    print("Step 3: Wall Thickness Calculation")
    print("-" * 80)
    # Design pressure: MEOP × safety factor (from REQ-018)
    design_pressure_MPa = MEOP_MPa * SAFETY_FACTOR
    design_pressure_Pa = design_pressure_MPa * 1e6
    chamber_radius_m = chamber_geometry["chamber_radius_mm"] / 1000
    material_yield_MPa = material_selection["effective_yield_op_temp_MPa"]
    
    print(f"Pressure vessel design:")
    print(f"  MEOP: {MEOP_MPa:.2f} MPa")
    print(f"  Safety factor: {SAFETY_FACTOR}")
    print(f"  Design pressure: {design_pressure_MPa:.2f} MPa")
    print()
    
    wall_thickness = calculate_wall_thickness(
        design_pressure_Pa, chamber_radius_m, material_yield_MPa, SAFETY_FACTOR
    )
    
    print(f"Wall thickness analysis:")
    print(f"  Required thickness (structural): {wall_thickness['required_thickness_mm']:.4f} mm")
    print(f"  Minimum manufacturable thickness: {MIN_MANUFACTURABLE_THICKNESS_MM} mm")
    print(f"  Design thickness: {wall_thickness['design_thickness_mm']:.3f} mm")
    print(f"  Actual safety factor: {wall_thickness['actual_safety_factor']:.2f}")
    print(f"  Actual hoop stress: {wall_thickness['actual_hoop_stress_MPa']:.2f} MPa")
    print(f"  Material yield at temp: {wall_thickness['material_yield_at_temp_MPa']:.1f} MPa")
    print(f"  Stress margin: {wall_thickness['stress_margin_percent']:.1f}%")
    print()
    
    # Step 4: Chamber mass calculation
    print("Step 4: Chamber Mass Calculation")
    print("-" * 80)
    mass_calc = calculate_chamber_mass(
        chamber_geometry, wall_thickness['design_thickness_mm'], material_selection['density_kg_m3']
    )
    
    print(f"Chamber mass:")
    print(f"  Volume: {mass_calc['volume_m3']:.9f} m³")
    print(f"  Mass: {mass_calc['mass_kg']:.6f} kg")
    print()
    
    # Step 5: Mass budget verification
    print("Step 5: Mass Budget Verification (REQ-011)")
    print("-" * 80)
    mass_budget = check_mass_budget(mass_calc['mass_kg'])
    
    print(f"Mass budget analysis:")
    print(f"  Chamber mass: {mass_budget['chamber_mass_kg']:.6f} kg")
    print(f"  Budget limit: {mass_budget['mass_budget_kg']:.3f} kg")
    print(f"  Mass check: {'PASS' if mass_budget['mass_check'] else 'FAIL'}")
    print(f"  Mass margin: {mass_budget['mass_margin_kg']:.6f} kg ({mass_budget['mass_margin_percent']:.2f}%)")
    print()
    
    # Step 6: Envelope verification
    print("Step 6: Envelope Verification (REQ-012)")
    print("-" * 80)
    nozzle_props = calculate_nozzle_properties(des001_data)
    envelope_check = check_envelope_constraints(
        chamber_geometry['chamber_diameter_mm'],
        chamber_geometry['chamber_length_mm'],
        nozzle_props['exit_diameter_mm'],
        nozzle_props['nozzle_length_mm']
    )
    
    print(f"Overall envelope:")
    print(f"  Overall diameter: {envelope_check['overall_diameter_mm']:.1f} mm (limit: {ENVELOPE_DIAMETER_mm} mm)")
    print(f"  Overall length: {envelope_check['overall_length_mm']:.1f} mm (limit: {ENVELOPE_LENGTH_mm} mm)")
    print(f"  Diameter check: {'PASS' if envelope_check['diameter_check'] else 'FAIL'}")
    print(f"  Length check: {'PASS' if envelope_check['length_check'] else 'FAIL'}")
    print(f"  Diameter margin: {envelope_check['diameter_margin_mm']:.1f} mm")
    print(f"  Length margin: {envelope_check['length_margin_mm']:.1f} mm")
    print()
    
    # Step 7: Temperature verification
    print("Step 7: Temperature Constraint Verification")
    print("-" * 80)
    print(f"Chamber wall temperature (REQ-015):")
    print(f"  Operating temperature: {chamber_temperature_C:.1f}°C")
    print(f"  Maximum allowed: {CHAMBER_MAX_TEMP_C}°C")
    print(f"  Check: {'PASS' if chamber_temperature_C <= CHAMBER_MAX_TEMP_C else 'FAIL'}")
    print(f"  Margin: {CHAMBER_MAX_TEMP_C - chamber_temperature_C:.1f}°C")
    print()
    
    print(f"Nozzle exit temperature (REQ-016):")
    print(f"  Exit temperature: {nozzle_props['exit_temperature_C']:.1f}°C")
    print(f"  Maximum allowed: {NOZZLE_MAX_TEMP_C}°C")
    print(f"  Check: {'PASS' if nozzle_props['temp_constraint_check'] else 'FAIL'}")
    print(f"  Margin: {nozzle_props['temp_margin_C']:.1f}°C")
    print()
    
    # Step 8: Material requirements verification
    print("Step 8: Material Requirements Verification")
    print("-" * 80)
    print(f"Chamber material (REQ-023, REQ-024):")
    print(f"  Selected: {material_selection['material_name']}")
    print(f"  Hydrazine compatible: {'Yes' if material_selection['hydrazine_compatible'] else 'No'}")
    print(f"  Max temp capability: {material_selection['max_temp_C']}°C")
    print(f"  Operating temperature: {chamber_temperature_C:.1f}°C")
    print(f"  Refractory/high-temp: {'Yes' if material_selection['max_temp_C'] >= 1400 else 'No'}")
    print(f"  Check: {'PASS' if material_selection['max_temp_C'] >= 1400 else 'FAIL'}")
    print()
    
    # Prepare output data
    output_data = {
        "design_id": "DES-004",
        "parameters": {
            "MEOP_MPa": MEOP_MPa,
            "safety_factor": SAFETY_FACTOR,
            "design_pressure_MPa": design_pressure_MPa,
            "chamber_operating_temp_C": chamber_temperature_C,
            "chamber_operating_temp_K": chamber_temperature_K
        },
        "material_selection": {
            "material_name": material_selection["material_name"],
            "max_temp_C": material_selection["max_temp_C"],
            "density_kg_m3": material_selection["density_kg_m3"],
            "yield_strength_RTMpa": material_selection["yield_strength_RTMpa"],
            "effective_yield_op_temp_MPa": material_selection["effective_yield_op_temp_MPa"],
            "hydrazine_compatible": material_selection["hydrazine_compatible"],
            "heritage": material_selection["heritage"]
        },
        "chamber_geometry": {
            "chamber_diameter_mm": chamber_geometry["chamber_diameter_mm"],
            "chamber_radius_mm": chamber_geometry["chamber_radius_mm"],
            "chamber_length_mm": chamber_geometry["chamber_length_mm"],
            "chamber_length_m": chamber_geometry["chamber_length_m"],
            "contraction_ratio": chamber_geometry["contraction_ratio"],
            "L_star_m": chamber_geometry["L_star_m"]
        },
        "wall_thickness": {
            "required_thickness_mm": wall_thickness["required_thickness_mm"],
            "design_thickness_mm": wall_thickness["design_thickness_mm"],
            "actual_safety_factor": wall_thickness["actual_safety_factor"],
            "actual_hoop_stress_MPa": wall_thickness["actual_hoop_stress_MPa"],
            "material_yield_at_temp_MPa": wall_thickness["material_yield_at_temp_MPa"],
            "stress_margin_percent": wall_thickness["stress_margin_percent"]
        },
        "chamber_mass": {
            "mass_kg": mass_calc["mass_kg"],
            "volume_m3": mass_calc["volume_m3"]
        },
        "nozzle_properties": {
            "exit_diameter_mm": nozzle_props["exit_diameter_mm"],
            "nozzle_length_mm": nozzle_props["nozzle_length_mm"],
            "exit_temperature_C": nozzle_props["exit_temperature_C"]
        },
        "overall_envelope": {
            "overall_diameter_mm": envelope_check["overall_diameter_mm"],
            "overall_length_mm": envelope_check["overall_length_mm"],
            "diameter_check": envelope_check["diameter_check"],
            "length_check": envelope_check["length_check"]
        },
        "requirements_compliance": {
            "REQ-015": {
                "description": "Chamber wall temperature ≤ 1400°C",
                "threshold_max": CHAMBER_MAX_TEMP_C,
                "computed": chamber_temperature_C,
                "unit": "°C",
                "status": "PASS" if chamber_temperature_C <= CHAMBER_MAX_TEMP_C else "FAIL",
                "margin_C": CHAMBER_MAX_TEMP_C - chamber_temperature_C
            },
            "REQ-016": {
                "description": "Nozzle exit temperature ≤ 800°C",
                "threshold_max": NOZZLE_MAX_TEMP_C,
                "computed": nozzle_props["exit_temperature_C"],
                "unit": "°C",
                "status": "PASS" if nozzle_props["temp_constraint_check"] else "FAIL",
                "margin_C": nozzle_props["temp_margin_C"]
            },
            "REQ-018": {
                "description": "Chamber withstand MEOP × 1.5 safety factor",
                "threshold_min": SAFETY_FACTOR,
                "computed": wall_thickness["actual_safety_factor"],
                "unit": "dimensionless",
                "status": "PASS" if wall_thickness["actual_safety_factor"] >= SAFETY_FACTOR else "FAIL",
                "margin_percent": ((wall_thickness["actual_safety_factor"] - SAFETY_FACTOR) / SAFETY_FACTOR) * 100
            },
            "REQ-023": {
                "description": "Chamber material compatible with hydrazine products",
                "status": "PASS" if material_selection["hydrazine_compatible"] else "FAIL"
            },
            "REQ-024": {
                "description": "Nozzle material is refractory metal or high-temp alloy (≥1400°C)",
                "threshold_min": 1400.0,
                "computed": material_selection["max_temp_C"],
                "unit": "°C",
                "status": "PASS" if material_selection["max_temp_C"] >= 1400.0 else "FAIL"
            },
            "REQ-011": {
                "description": "Dry mass ≤ 0.5 kg (chamber only)",
                "threshold_max": MASS_BUDGET_kg,
                "computed": mass_calc["mass_kg"],
                "unit": "kg",
                "status": "PASS" if mass_budget["mass_check"] else "FAIL",
                "margin_percent": mass_budget["mass_margin_percent"]
            },
            "REQ-012": {
                "description": "Envelope: 100 mm diameter × 150 mm length",
                "diameter_threshold_max": ENVELOPE_DIAMETER_mm,
                "length_threshold_max": ENVELOPE_LENGTH_mm,
                "diameter_computed": envelope_check["overall_diameter_mm"],
                "length_computed": envelope_check["overall_length_mm"],
                "unit": "mm",
                "status": "PASS" if envelope_check["diameter_check"] and envelope_check["length_check"] else "FAIL"
            }
        },
        "assumptions": [
            f"Chamber diameter = 3 × throat diameter (typical contraction ratio from CONTEXT.md)",
            f"Characteristic length L* = 0.75 m (midpoint of 0.5-1.0 m range for hydrazine)",
            f"Yield strength at operating temperature = {TEMP_DEGRADATION_FACTOR*100}% of RT value (conservative)",
            f"Minimum manufacturable thickness = {MIN_MANUFACTURABLE_THICKNESS_MM} mm (practical constraint)",
            f"Design pressure = MEOP × safety factor = {MEOP_MPa} × {SAFETY_FACTOR} = {design_pressure_MPa} MPa",
            f"Thin-wall pressure vessel theory (CONTEXT.md Section 9)",
            f"End caps modeled as hemispherical (simplified for mass calculation)",
            f"Nozzle made from same material as chamber (simplification)",
            "DES-001 provides chamber pressure (0.21 MPa), temperature (1400 K), and throat dimensions"
        ]
    }
    
    # Print requirements compliance summary
    print("=" * 80)
    print("REQUIREMENTS COMPLIANCE SUMMARY")
    print("=" * 80)
    
    for req_id, req_data in output_data["requirements_compliance"].items():
        status_symbol = "✓" if req_data["status"] == "PASS" else "✗"
        print(f"\n{status_symbol} {req_id}: {req_data['description']}")
        print(f"   Status: {req_data['status']}")
        
        if "threshold_min" in req_data:
            print(f"   Requirement: ≥ {req_data['threshold_min']}")
            print(f"   Computed: {req_data['computed']:.4f}")
        elif "threshold_max" in req_data:
            print(f"   Requirement: ≤ {req_data['threshold_max']}")
            print(f"   Computed: {req_data['computed']:.4f}")
        else:
            print(f"   Requirement: {req_data.get('description', 'N/A')}")
        
        if "margin_percent" in req_data:
            print(f"   Margin: {req_data['margin_percent']:.2f}%")
        if "margin_C" in req_data:
            print(f"   Margin: {req_data['margin_C']:.1f}°C")
    
    print()
    print("=" * 80)
    
    # Output JSON file
    output_path = Path(__file__).parent.parent / "data" / "chamber_nozzle_stress.json"
    with open(output_path, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"\nDesign data written to: {output_path}")
    
    # Check for any failures
    failures = [
        req_id for req_id, req_data in output_data["requirements_compliance"].items()
        if req_data["status"] != "PASS"
    ]
    
    if failures:
        print(f"\n⚠ WARNING: {len(failures)} requirement(s) not met: {', '.join(failures)}")
        return 1
    else:
        print("\n✓ All requirements satisfied!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
