# buck-converter-5v3a
First-principles design of a 12V to 5V 3A asynchronous buck converter (TI TPS54360);  full calculations, Type II loop compensation, and 4-layer KiCad PCB.
# 12V to 5V 3A Synchronous Buck Converter

A complete design of a non-isolated step-down DC-DC converter producing a
regulated 5V/3A output from a 12V input, built around the TI TPS54360.
Designed from first principles in KiCad, with full calculations, control-loop
compensation, and a 4-layer PCB layout.

## Specifications
| Parameter | Value |
|-----------|-------|
| Input | 10.8–13.2V (12V nominal) |
| Output | 5V ±2%, 0–3A |
| Ripple | <50mV pp |
| Switching frequency | 500 kHz |
| Topology | Asynchronous buck (HS FET + Schottky) |
| Predicted efficiency | 89.7% at full load |
| Phase margin | ~62° |

## Highlights
- Every component value derived from first principles (TPS54360 datasheet
  equations + worst-case operating-point analysis)
- Type II compensator designed for ~50 kHz crossover, verified by Python
  Bode analysis and an independent hand calculation
- 4-layer PCB with tight switching loop, internal ground plane, and thermal
  vias under the controller and Schottky
- ERC clean, DRC clean

## Repository structure
- `report/` — full design report (PDF)
- `calculations/` — LaTeX calculations and Python analysis scripts
- `kicad/` — KiCad project, schematic, and PCB files
- `images/` — schematic, PCB, and 3D renders
- `gerbers/` — fabrication output

## Tools
KiCad 9, Python (NumPy/SciPy/matplotlib), LaTeX

## Status
Complete paper design verified by analysis. Prototype build and bench
validation planned as next step.
