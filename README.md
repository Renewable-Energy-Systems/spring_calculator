
# Coil Spring Calculator

A Python script to calculate the spring rate (k) in N/m and the force at a given deflection for a compression coil spring using SI units.

---

## Features
- Computes spring rate (k) using shear modulus, wire diameter, inner diameter, and active coils.
- Optional force calculation at a specified deflection.
- Inputs in millimeters (converted to meters internally) for ease of use.

---

## Installation
Ensure Python 3 is installed. No additional dependencies are required.

Download the script:
```bash
wget https://github.com/username/repo/raw/main/spring_calculator.py
chmod +x spring_calculator.py
```

---

## Usage
```
usage: spring_calculator.py [-h] [-G SHEAR_MODULUS] [-D DEFLECTION] d ID n

Calculate the spring rate (N/m) and force (N) of a coil spring.

positional arguments:
  d                     Wire diameter of spring in mm (d)
  ID                    Inner diameter of the coil in mm (ID)
  n                     Number of active coils in the spring (n)

optional arguments:
  -h, --help            show this help message and exit
  -G SHEAR_MODULUS, --shear_modulus SHEAR_MODULUS
                        Shear modulus G in Pa (default: 77e9 for 77 GPa)
  -D DEFLECTION, --deflection DEFLECTION
                        Deflection in mm for which to calculate the force (default: 0.0)
```

---

## Formulas
1. **Mean Coil Diameter**:  
   \( D_{\text{mean}} = ID + d \)  
   *Units: meters*

2. **Spring Rate (k)**:  
   \( k = \frac{G \cdot d^4}{8 \cdot D_{\text{mean}}^3 \cdot n} \)  
   *Units: N/m*

3. **Spring Force**:  
   \( F = k \cdot \Delta \)  
   *Units: Newtons (N)*

---

## Parameters
| Argument | Description                        | Units | Default |
|----------|------------------------------------|-------|---------|
| `d`      | Wire diameter                      | mm    | Required|
| `ID`     | Inner diameter of the coil         | mm    | Required|
| `n`      | Number of active coils             | -     | Required|
| `-G`     | Shear modulus (e.g., 77e9 for steel)| Pa    | 77e9    |
| `-D`     | Deflection for force calculation   | mm    | 0.0     |

---

## Examples

1. **Calculate Spring Rate Only**:  
   ```bash
   ./spring_calculator.py 2.5 20 10
   ```
   Output:
   ```
   Spring Rate (k): 3945.10 N/m
   ```

2. **Calculate Spring Rate and Force at 5 mm Deflection**:  
   ```bash
   ./spring_calculator.py 2.5 20 10 -D 5
   ```
   Output:
   ```
   Spring Rate (k): 3945.10 N/m
   Spring Force at deflection 5.00 mm: 19.73 N
   ```

---

## Credits
Developed with ❤️ by [@kiranpranay](https://github.com/kiranpranay).  
Feel free to contribute or report issues!
