#Plots 2D electronic band structure of material in terms of energy relative to Fermi Level (eV) against k-path (denoted by high symmetry points of FCC crystal).
import numpy as np
import matplotlib.pyplot as plt

Ha_eV = 27.211386245988 
############################# k points splitting ###############################
kpp = 30

dks = [0.2, 0.1, 0.14, 0.17, 0.27]
k = 0
kpath = [k]
for dk in dks:
    k += dk
    kpath.append(k)
    
print(kpath)

Npaths = len(kpath)
ks = []
for i in range(Npaths-1):
    ki = kpath[i]
    kf = kpath[i+1]
    ks = ks + list(np.linspace(ki,kf, kpp))[:-1]

ks.append(kpath[-1])

print(ks)
print(len(ks))

############################# band structure plotting ###############################
materials = ["gold"]              #Change this!!
bands_file = "bands_au.dat"       #Change this!!

labels = ["Γ", "X", "W", "L", "Γ", "K"]

fermis = (0.538/2)*Ha_eV         #0.5380, 0.4635, 0.6380 all in hartree for gold, silver and platinum 
No = 9

xs = [(kpp-1)*i for i in range(Npaths)]
#band_list = [Main.test(material) for material in materials]
with open(bands_file, 'r') as file:
    band_list = []
    for line in file:
        splitted_lines = line.strip().split()
        band_list.append([float(element) for element in splitted_lines])

print(np.shape(band_list), type(band_list))        

fig, axs = plt.subplots(1,len(materials),figsize=(13,4), sharey=True)
plt.subplots_adjust(wspace=0.02)

#axs.set_title(materials)
for i in range(No):
    band = [row[i+3]*Ha_eV-fermis for row in band_list]
    axs.plot(ks, band, color='red')

for x in xs: 
    axs.axvline(ks[x], linewidth=0.3, linestyle='--', c='k')

axs.set_xticks([ks[x] for x in xs])

axs.set_xticklabels(labels)      # Replace tick labels with high-symmetry points

# for i in range(-3,8):
#     axs.axhline(i*4, linewidth=0.3, linestyle='--', c='k')
axs.axhline(0, linewidth=1, linestyle='--', c='k')

axs.set_ylim(-10, 9)
#axs.set_xlim(ks[xs[0]], ks[xs[3]])

axs.fill_between(ks, -2.4, 2.4, color='lightblue', alpha=0.5) #add shaded region to represent the possible region
                                                        #for optical transition

axs.set_xlabel('k path')
axs.set_ylabel('Energy (eV)')

plt.show()

