"""
Plant transfer function (control-to-output) for the
TPS54360 12V→5V buck converter.

Derived per datasheet section 7.3.15 equations 11-14.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# -------------------------------------------------------------
# Plant parameters (from your Day 6 calculations)
# -------------------------------------------------------------
gm_ps  = 12.0          # A/V, power stage transconductance (datasheet pg. 7)
V_out  = 5.0           # V
I_out  = 3.0           # A
R_L    = V_out / I_out # ohms, load resistance at full load
C_out  = 66e-6         # F, effective output capacitance (after derating)
R_esr  = 1.5e-3        # ohms, parallel ESR of two ceramic caps

# -------------------------------------------------------------
# Derived quantities
# -------------------------------------------------------------
A_dc = gm_ps * R_L
f_p  = 1.0 / (2 * np.pi * R_L * C_out)
f_z  = 1.0 / (2 * np.pi * R_esr * C_out)

print("Plant parameters:")
print(f"  R_L   = {R_L:.3f} ohms")
print(f"  C_out = {C_out*1e6:.1f} uF (effective)")
print(f"  R_ESR = {R_esr*1e3:.2f} mohms")
print()
print("Derived:")
print(f"  DC gain A_dc = {A_dc:.2f} V/V = {20*np.log10(A_dc):.2f} dB")
print(f"  Pole  f_P    = {f_p:.0f} Hz ({f_p/1e3:.2f} kHz)")
print(f"  Zero  f_Z    = {f_z:.0f} Hz ({f_z/1e6:.2f} MHz)")

# -------------------------------------------------------------
# Build the transfer function
# -------------------------------------------------------------
wz = 2 * np.pi * f_z
wp = 2 * np.pi * f_p

num = [A_dc / wz, A_dc]
den = [1.0 / wp, 1.0]

G_plant = signal.TransferFunction(num, den)

# -------------------------------------------------------------
# Sweep frequency
# -------------------------------------------------------------
freq_hz = np.logspace(0, 7, 1000)
omega   = 2 * np.pi * freq_hz

w_out, mag_db, phase_deg = signal.bode(G_plant, omega)
freq_out = w_out / (2 * np.pi)

# -------------------------------------------------------------
# Plot
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

ax1.semilogx(freq_out, mag_db, 'b-', linewidth=2)
ax1.axhline(0,  color='gray', linestyle=':', alpha=0.7)
ax1.axvline(f_p, color='red',   linestyle='--', alpha=0.6,
            label=f'Pole at {f_p:.0f} Hz')
ax1.axvline(f_z, color='green', linestyle='--', alpha=0.6,
            label=f'Zero at {f_z/1e6:.1f} MHz')
ax1.axvline(50e3, color='purple', linestyle=':', alpha=0.6,
            label='Target crossover (50 kHz)')
ax1.set_ylabel('Gain (dB)')
ax1.set_title('Plant Transfer Function (V_out / V_COMP) — TPS54360 12V→5V buck')
ax1.grid(which='both', alpha=0.4)
ax1.legend(loc='upper right')

ax2.semilogx(freq_out, phase_deg, 'b-', linewidth=2)
ax2.axhline(-45,  color='gray', linestyle=':', alpha=0.7)
ax2.axhline(-90,  color='gray', linestyle=':', alpha=0.7)
ax2.axvline(f_p,  color='red',   linestyle='--', alpha=0.6)
ax2.axvline(f_z,  color='green', linestyle='--', alpha=0.6)
ax2.axvline(50e3, color='purple', linestyle=':', alpha=0.6)
ax2.set_xlabel('Frequency (Hz)')
ax2.set_ylabel('Phase (degrees)')
ax2.grid(which='both', alpha=0.4)

plt.tight_layout()
plt.savefig('plant_bode.png', dpi=150, bbox_inches='tight')
print("\nSaved: plant_bode.png")
plt.show()