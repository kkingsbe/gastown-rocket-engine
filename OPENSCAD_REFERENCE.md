# OPENSCAD_REFERENCE.md

## Overview

OpenSCAD is a 2D/3D script-based modeler. It is declarative, not imperative. Geometry is defined by functions and modules, not by drawing sequences.

### File Extensions

* `.scad`: Source code
* `.stl`: Stereolithography (3D print format)
* `.off`: Object File Format (Geomview)
* `.dxf`: Drawing Exchange Format (2D)
* `.svg`: Scalable Vector Graphics (2D)
* `.png`: Image export

---

## 1. Core Syntax & Primitives

### 3D Primitives

```scad
cube(size = [x,y,z], center = true/false); // Box
cube(10); // 10x10x10 cube

sphere(r = radius); // OR d = diameter
sphere(d = 10, $fn=100); // Smooth sphere

cylinder(h = height, r = radius, center = true/false);
cylinder(h = 10, r1 = bottom_rad, r2 = top_rad, center = true); // Cone

```

### 2D Primitives (for Extrusion)

```scad
square(size = [x,y], center = true/false);
circle(r = radius, $fn=100);
polygon(points = [[0,0],[10,0],[0,10]]);

```

### Transformations

Transformations wrap the object they affect. They read right-to-left (inner-to-outer).

```scad
translate([x, y, z]) { ... }
rotate([x, y, z]) { ... }    // Rotates around axes in order X, Y, Z
scale([x, y, z]) { ... }     // 1.0 = 100%
mirror([x, y, z]) { ... }    // Vector normal to the mirror plane
color("red", alpha=1.0) { ... }

```

### Boolean Operations

These are the core of Constructive Solid Geometry (CSG).

```scad
union() { ... }         // Joins children (Implicit default in newer versions)
difference() {          // Subtracts 2nd..nth child from the 1st child
    cube(10);           // Positive (Part)
    sphere(6);          // Negative (Hole)
}
intersection() { ... }  // Keeps only the overlapping volume
hull() { ... }          // "Shrink wraps" the children
minkowski() { ... }     // Traces shape A with shape B (Computationally expensive!)

```

---

## 2. Advanced Modeling

### Linear Extrusion (2D → 3D)

Converts a 2D shape into a 3D solid.

```scad
linear_extrude(height = 10, center = true, twist = 0, scale = 1.0)
    square([20,10], center=true);

```

### Rotate Extrusion (2D → 3D)

Spins a 2D profile around the Z-axis (like a lathe). The 2D shape must be in the positive X plane (X > 0).

```scad
rotate_extrude(angle = 360, convexity = 2)
    translate([10, 0, 0]) circle(r = 1); // Torus

```

### Projection (3D → 2D)

Flattens 3D geometry for DXF/SVG export.

```scad
projection(cut = true) // Cross-section at Z=0
    sphere(10);

projection(cut = false) // Shadow (silhouette)
    sphere(10);

```

---

## 3. Programming Logic

### Variables

Variables are set at compile time. They are constants within their scope. You cannot update a variable like `x = x + 1`.

```scad
thickness = 3.0; // Global variable
width = 10.0;

```

### Modules (Subroutines)

Use modules to define reusable components.

```scad
module screw_hole(d=3) {
    cylinder(h=100, d=d, center=true, $fn=50);
}

// Usage
difference() {
    cube(10);
    screw_hole(d=4);
}

```

### Loops (For)

Generates geometry, does not execute imperative code.

```scad
for (i = [0 : 1 : 5]) { // Start : Step : End
    translate([i * 10, 0, 0])
        sphere(r = 2);
}

```

### Conditionals

```scad
if (part_type == "bracket") {
    // ... geometry
} else {
    // ... geometry
}

```

---

## 4. Special Variables

* `$fn`: Number of fragments (resolution). Higher = smoother but slower.
* Usage: `sphere(r=10, $fn=100);`


* `$t`: Animation time (0.0 to 1.0). Used for animations.
* `$vpr`: Viewport rotation (array [rotx, roty, rotz]).
* `$vpt`: Viewport translation (array [x, y, z]).

---

## 5. CLI Usage (Automation)

For Gastown agents, run OpenSCAD in headless mode via the command line.

### Basic Render (PNG Preview)

```bash
openscad -o output.png --imgsize=1024,768 --colorscheme="Cornfield" model.scad

```

### 3D Export (STL/3MF)

```bash
openscad -o output.stl model.scad

```

### 2D Export (DXF/SVG)

```bash
openscad -o output.dxf model.scad

```

### Parameter Overrides

You can override top-level variables from the command line without editing the file. This is useful for batch generating variations.

```bash
# Sets the variable 'thickness' to 5.0 inside model.scad
openscad -o output.stl -D "thickness=5.0" model.scad

```

---

## 6. Debugging Modifiers

Prefix any object with these characters to change how it is rendered.

* `*` (Disable): The object is ignored/removed from the tree.
* `!` (Root): Only this object (and its children) is rendered.
* `#` (Highlight): The object is rendered in transparent pink (useful for debugging holes in `difference()`).
* `%` (Transparent): The object is rendered in transparent gray (ghost mode).

**Example:**

```scad
difference() {
    cube(10);
    #cylinder(h=12, d=4, center=true); // Shows the cutting cylinder in pink
}

```

## 7. Mathematical Functions

Standard math functions available for parametric calculations:

| Function | Description |
| --- | --- |
| `sin(x)`, `cos(x)`, `tan(x)` | Trigonometry (degrees) |
| `asin(x)`, `acos(x)`, `atan2(y,x)` | Inverse Trig |
| `sqrt(x)` | Square root |
| `pow(x, y)` | x to the power of y |
| `abs(x)` | Absolute value |
| `min(a, b)`, `max(a, b)` | Minimum / Maximum |
| `floor(x)`, `ceil(x)`, `round(x)` | Rounding |
| `sign(x)` | -1, 0, or 1 |
| `norm(v)` | Length of vector v |
| `cross(v1, v2)` | Cross product of 3D vectors |