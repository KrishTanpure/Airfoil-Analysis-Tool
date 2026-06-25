# **Airfoil Analysis Tool**



A Python tool that generates NACA 4-digit airfoil geometry and analyzes its aerodynamic characteristics using thin airfoil theory, validated against XFOIL.



## What it does



The user has to enter a NACA 4-digit code (e.g. 2412) and an angle of attack, and this tool:



**Generates airfoil geometry** — builds the camber line, thickness distribution, and full upper/lower surface coordinates from the standard NACA 4-digit equations.



**Computes lift and moment** — derives the Fourier coefficients (A0, A1, A2) of the vorticity distribution via the Glauert transformation, then computes lift coefficient (Cl), pitching moment about the quarter-chord (Cm,c/4), and zero-lift angle of attack (α\_L=0) using thin airfoil theory.



**Computes pressure distribution** — calculates the chordwise delta Cp distribution from the same Fourier coefficients.

Exports geometry — writes the airfoil coordinates to a .dat file in the standard format (trailing edge → upper surface → leading edge → lower surface → trailing edge) for import into XFOIL/XFLR5.





### Validation against XFOIL



The tool's geometry and aerodynamic predictions were validated against XFOIL (via XFLR5) for NACA 2412 at α = 5°:



|Quantity|This tool (inviscid thin airfoil theory)|XFOIL (viscous, Re = 266,803)|Difference|
|-|-|-|-|
|CL|0.7762|0.7874|1.4%|
|Cm,c/4|-0.0531|-0.0510|4.1%|



The geometry was confirmed: XFLR5 measured the imported coordinates at 12.01% thickness (max thickness pos. 30.13%) and 2.00% camber (max camber pos. 40.44%), matching the NACA 2412 specification.



The tool was also tested on NACA 0012 (a symmetric airfoil) as an edge case: CL, Cm, and α\_L=0 all reduced correctly to the expected zero-camber behavior, and multiple angles of attack on NACA 2412 (0°, -2°, 5°) produced results consistent with the tool's own zero lift angle calculation.



### Known limitations





**Inviscid theory vs. viscous reference**: this tool implements inviscid thin airfoil theory. The XFOIL comparison above used a viscous run, since XFLR5's inviscid mode is a known unreliable path in that software. Some of the discrepancy above reflects viscous effects this tool doesn't model, not error in the theory itself.



**Leading-edge singularity**: thin airfoil theory predicts an unbounded pressure coefficient at the leading edge (x → 0), a known consequence of modeling the airfoil as infinitely thin with a sharp leading edge. Real airfoils have a rounded nose specifically to avoid this; XFOIL's pressure distribution does not show this singularity. This is a documented limitation of the theory, not a bug.



**Fourier series truncation:** the pressure distribution calculation truncates the Fourier series at A2, which is sufficiently accurate for smooth NACA 4-digit camber lines but introduces small additional error beyond what the A0/A1/A2-based Cl and Cm calculations carry.



&#x20;   

### Usage



Set the variable nacaairfoil (a 4-digit string, e.g. "2412") and angleofattack (in radians) at the top of the script, then run. The script will plot the camber line, thickness distribution, full airfoil geometry, and pressure distribution, print Cl, Cm, α\_L=0, and write MyAirfoilCoordinates.dat. The code will also generate plots for 





