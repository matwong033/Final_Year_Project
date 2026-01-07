'''Analytical solutions for extinction cross sections'''
import numpy as np

def calculate_factor(epsm, eps):
    #Calculate the multiplication factor f.
    return (3 * epsm) / (eps + 2 * epsm)

def multiply_columns(input_file, output_file, epsm, epsm_old, material, ev):
    #Multiply the second and third columns of a CSV file by the product of f and f_old.
    data = np.loadtxt(input_file).astype(np.complex128)

    # Calculate eps based on frequency (you can customize this formula)
    eps_dict_pt = {1.4: -18.692 + 32.984 * 1j, 1.6: -15.808 + 26.717 * 1j, 1.8: -13.325 + 22.239 * 1j,
                2.0: -11.275 + 18.722 * 1j, 2.2: -9.504 + 16.362 * 1j, 2.4: -8.411 + 14.372 * 1j,
                2.6: -1.8557 + 2.6076 * 1j, 2.8: -6.261 + 11.346 * 1j}
    
    eps_dict_au = {1.4: -29.5872 + 0.8704 * 1j, 1.6: -20.7872 + 0.7296 * 1j, 1.8: -14.5843 + 0.6876 * 1j,
                   2.0: -9.9687 + 0.8216 * 1j, 2.2: -6.394 + 1.2192 * 1j, 2.4: -3.2096 + 1.86 * 1j,
                   2.6: -1.8557 + 2.6076 * 1j, 2.8: -0.834 + 3.8192 * 1j}
    
    eps_dict = {1: eps_dict_au, 2: eps_dict_pt}
    eps = eps_dict[material][ev]

    # Calculate the factors f and f_old
    f = calculate_factor(epsm, eps)
    f_old = calculate_factor(epsm_old, eps)

    #Multiply the second and third columns by the product of f and f_old
    data[:, 1] *= (abs(f)**2 * 1/(abs(f_old)**2))
    data[:, 2] *= (abs(f)**2 * 1/(abs(f_old)**2))

    #Save the modified data to a new file
    np.savetxt(output_file, data.view(float).reshape(-1, data.shape[1] * 2))
    print(f"Modified data saved to {output_file}")


material = 1   # 1 for Au, 2 for Pt
ev = 2.8

input_file = f"au_10d_{ev}ev.dat"     # Replace with your actual file name

epsm_old = 1.0 + 0*1j  #this stays constant

# Generate files for epsm from 1.0 to 6.0
for epsm_real in range(1, 7):
    epsm = epsm_real + 0j
    output_file = f"epsm{epsm_real}_au_10d_{ev}ev.dat"      # Replace with actual output file name
    multiply_columns(input_file, output_file, epsm, epsm_old, material, ev)
