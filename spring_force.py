#!/usr/bin/env python3

"""
A script to calculate the spring rate k [N/m] (instead of N/mm) 
and optionally the force [N] at a given deflection for a coil spring.

Formulas used (all in SI units):
  1) Mean coil diameter:   D_mean = ID + d       [meters]
  2) Spring rate (k):      k = (G * d^4) / (8 * D_mean^3 * n)
       - G in Pa (N/m^2)
       - d in m
       - D_mean in m
       - n (dimensionless, number of active coils)
     => k in N/m
  3) Spring force:         F = k * Δ
       - Δ in m
       => F in N
"""

import argparse

def spring_rate(G_pa, wire_diameter_m, inner_diameter_m, num_active_coils):
    """
    Compute the spring rate k for a compression coil spring in N/m.

    Args:
        G_pa             (float): Shear modulus in Pa (N/m^2)
        wire_diameter_m  (float): Wire diameter d in meters
        inner_diameter_m (float): Inner coil diameter ID in meters
        num_active_coils (float): Number of active coils n

    Returns:
        float: Spring rate k in N/m
    """
    # Mean coil diameter [m]
    D_mean_m = inner_diameter_m + wire_diameter_m
    
    # Spring rate k in N/m
    k = (G_pa * (wire_diameter_m ** 4)) / (8.0 * (D_mean_m ** 3) * num_active_coils)
    return k

def spring_force(k, deflection_m):
    """
    Compute the force at a given deflection using Hooke's law: F = k * Δ.

    Args:
        k             (float): Spring rate in N/m
        deflection_m  (float): Deflection Δ in meters

    Returns:
        float: Spring force in N
    """
    return k * deflection_m

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Calculate the spring rate (N/m) and force (N) of a coil spring using SI units."
    )
    parser.add_argument("d", type=float, 
                        help="Wire diameter of spring in mm (d)")
    parser.add_argument("ID", type=float, 
                        help="Inner diameter of the coil in mm (ID)")
    parser.add_argument("n", type=float, 
                        help="Number of active coils in the spring (n)")
    parser.add_argument("-G", "--shear_modulus", type=float, default=77e9,
                        help="Shear modulus G in Pa (default: 77e9 for 77 GPa)")
    parser.add_argument("-D", "--deflection", type=float, default=0.0,
                        help="Deflection in mm for which to calculate the force (default: 0.0)")

    args = parser.parse_args()

    # Convert mm -> m for the input diameters
    wire_diameter_m = args.d / 1000.0
    inner_diameter_m = args.ID / 1000.0
    
    # Convert mm -> m for deflection
    deflection_m = args.deflection / 1000.0

    # Compute spring rate in N/m
    k_value = spring_rate(args.shear_modulus, wire_diameter_m, inner_diameter_m, args.n)
    print(f"Spring Rate (k): {k_value:.2f} N/m")

    # If a deflection is provided (> 0), compute force in N
    if deflection_m > 0:
        force = spring_force(k_value, deflection_m)
        print(f"Spring Force at deflection {args.deflection:.2f} mm: {force:.2f} N")
