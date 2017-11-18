import scipy.optimize as opt
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import xlrd as xlrd
import solvents, setup_parameters, curve_functions


add_File = setup_parameters.file
add_Folder = add_File[:8] + '\\'
add_Base = r'C:\Users\Sean\PhD UR\Data\UV-Vis-NIR Absorbance\\'

raw_data = xlrd.open_workbook(filename = add_Base + add_Folder + add_File).sheet_by_index(0)

def characterizeList(l):
    for i in range(len(l)):
        if type(l[i]) != type(1.0): print(i, ', ', type(l[i]))
    print(l)
    # print(len(l))
    # print(type(l[0]))
    print('done')

wavelength = []
setup_parameters.x_col = 0
for row in range(setup_parameters.start_row,len(raw_data.col(setup_parameters.x_col))):
    if type(raw_data.cell_value(row, setup_parameters.x_col)) != type('string'):
        wavelength.append(raw_data.cell_value(row, setup_parameters.x_col))
# characterizeList(wavelength)

counts = []
setup_parameters.y_col = 1
    #Make list of absorbance data
for row in range(setup_parameters.start_row,len(raw_data.col(setup_parameters.y_col))):
    if type(raw_data.cell_value(row, setup_parameters.y_col)) != type('string'):
        if raw_data.cell_value(row, setup_parameters.y_col) < 0:
            counts.append(0.)
        else:   counts.append(raw_data.cell_value(row, setup_parameters.y_col))
#    #Adjust absorbance data baseline to zero
# minCounts = min(counts)
# for i in range(len(counts)):
#     counts[i] = counts[i] - minCounts
initial_Counts = counts
    # Adjust absorbance data for solvent peaks
for j in range(len(setup_parameters.solvents_remove)):
    counts = solvents.remove_solvents(counts, wavelength, setup_parameters.solvents_remove[j], solvents.wavelength)
# characterizeList(counts)

# (param, covar) = opt.curve_fit(curve_functions.gaussian, wavelength, counts, p0 = [setup_parameters.abcgh['a'], setup_parameters.abcgh['b'], setup_parameters.abcgh['c'], setup_parameters.abcgh['shift']])#, bounds = (0, np.inf))
# print(param)

# (param2, covar2) = opt.curve_fit(curve_functions.gaussian2, wavelength, counts, p0 = [7.6e5, 823, 1,])#, bounds = (0, np.inf))
# print(param2)

# (param3, covar3) = opt.curve_fit(curve_functions.lorentzian, wavelength, counts, p0 = [7.6e5, 823, 1])#, bounds = (0, np.inf))
# print(param3)

(param4, covar4) = opt.curve_fit(curve_functions.SnTe_UVVis1, wavelength, counts,\
                                 p0 = [setup_parameters.abcgh['a'], setup_parameters.abcgh['b'], setup_parameters.abcgh['c'], setup_parameters.abcgh['g'], setup_parameters.abcgh['h'], setup_parameters.abcgh['shift']])#, bounds = (0, np.inf))
print(param4)

x = np.arange(100,3600,1)
plt.figure(1)
plt.rcParams.update({'font.size': 14})
plt.plot(wavelength, counts,'p', color = 'b', label = 'Solvent adj. raw data')
plt.plot(wavelength, initial_Counts,'o', color = 'k', label = 'Raw data')
# plt.plot(x, curve_functions.gaussian(x,param[0],param[1],param[2], param[3]), color = 'r', linewidth=1.0, label = 'Gaussian fit')
# plt.plot(x, curve_functions.gaussian2(x,param2[0],param2[1],param2[2]), color = 'g', linewidth=1.0, label = 'Gaussian fit')
# plt.plot(x, curve_functions.lorentzian(x,param3[0],param3[1],param3[2]), color = 'c', linewidth=1.0, label = 'Lorentzian fit')
plt.plot(x, curve_functions.SnTe_UVVis1(x,param4[0],param4[1],param4[2], param4[3], param4[4], param4[5]), color = 'r', linewidth=1.0, label = 'Fit')
#     #Plot solvent data
# for q in range(len(setup_parameters.solvents_remove)):
#     plt.plot(solvents.wavelength, setup_parameters.solvents_remove[q])
plt.grid(b=True, which='major', color='k', linestyle='-')
plt.grid(b=True, which='minor', color='0.65', linestyle='--')
# plt.legend(loc = 1)
plt.minorticks_on()
plt.xlabel('$\lambda\ [nm]$')
plt.ylabel('$counts$')

# ax = plt.subplot(111)
# # text = '$I_{0} = %.2f$\n$<R_{g}^{2}> = %.3e$'%(param[0],param[1])
# text = '$\lambda_{max} = %.2f\ nm$'%(param4[1])
# props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
# ax.text(0.5, 0.75, text, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)

plt.tight_layout()
# plt.xlim(0,3500)
plt.ylim(0, setup_parameters.abcgh['a']*1.3)
# plt.ylim(0, max(counts))
# plt.ylim(-0.01,0.11)
plt.show()