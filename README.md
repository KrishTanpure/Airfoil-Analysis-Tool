Airfoil Analysis Tool (In development - Summer 2026)

A Python based aerodynamic analysis tool implementing thin airfoil theory for NACA 4 digit airfoil series.


What It Does?

Generates NACA 4-digit airfoil geometry
Computes pressure coefficient (Cp) distributions
Compares inviscid thin airfoil theory against XFOIL viscous solver
Analyzes symmetric vs cambered airfoil performance across angles of attack


Theory

Cp = 1 - (V/Vinfinity)^2
Cl = 2π⍺ for symmetric airfoils (key result of thin airfoil theory)
NACA 4-digit series geometry equations


Tools Used

Python, NumPy, Matplotlib, XFOIL
