#Calculates the area under hot carrier generation rate curve, thus total number of electrons with E >= Φ_B
import numpy as np
import matplotlib.pyplot as plt
from numpy import trapz
import glob

# dat_files = sorted(glob.glob(f"epsm2_*.dat"))
# print(dat_files)

dat_files = [sorted(glob.glob(f"epsm{i}_*.dat")) for i in range(1,7)]
#print(dat_files)

fermi = 8.68 #7.319ev is for Au ; 8.68ev is for Pt ; 8.75ev is new hanwen fermi 16dec (all calculations in *c63*)
R = 1 # 30885 for 5rad Au ; 34881 for 5rad Pt
Phi_B = 1.3 # Schottky barrier (1.3 instead of 1.1ev for pt ; 1.1 instead of 0.9ev for au)

output = {}

for each_epsm in dat_files:
    for file in each_epsm:
        energy, energy_i, ne, ne_i, nh, nh_i, err_e, err_e_i, err_h, err_h_i = np.loadtxt(file, unpack=True)

        # Apply Fermi level shift and mask above Schottky barrier
        mask = (energy >= Phi_B + fermi)
        energy -= fermi
        ne_r = ne / R
        nh_r = nh / R

        # Integrate ne_r over energy above Phi_B
        integral = trapz(ne_r[mask], energy[mask])

        print(f'{file}: Integral above Φ_B = {Phi_B} eV is {integral:.6f}')



