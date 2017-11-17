import scipy.optimize as opt
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import xlrd as xlrd

add_File = '20170807_SnTe-TCE_Absorbance.xlsx'
add_Folder = add_File[:8] + '\\'
add_Base = r'C:\Users\Sean\PhD UR\Data\UV-Vis-NIR Absorbance\\'
abcgh = [0.1, 800, 100, 1.8e7, 2.8]
print(add_Base + add_Folder + add_File)

raw_data = xlrd.open_workbook(filename = add_Base + add_Folder + add_File).sheet_by_index(0)
# print(len(raw_data.col(0)))
trailingZeros = 2651

def characterizeList(l):
    for i in range(len(l)):
        if type(l[i]) != type(1.0): print(i, ', ', type(l[i]))
    print(l)
    # print(len(l))
    # print(type(l[0]))
    print('done')

wavelength = []
x_col = 0
for row in range(350,len(raw_data.col(x_col))): ##start after 2 to remove column header//302 to remove quartz peak
    wavelength.append(raw_data.cell_value(row, x_col))
wavelength = wavelength[:trailingZeros] #manual removal of trailing zeros
# characterizeList(wavelength)

counts = []
y_col = 1
for row in range(350,len(raw_data.col(y_col))): ##start after 2 to remove column header//302 to remove quartz peak
    # rdVal = float(raw_data.cell_value(row, 1))
    # counts.append(rdVal)
    counts.append(raw_data.cell_value(row, y_col))
counts = counts[:trailingZeros] #manual removal of trailing zeros
minCounts = min(counts)
for i in range(len(counts)):
    counts[i] = counts[i] - minCounts
# characterizeList(counts)

def gaussian(x,a,b,c):
    return (a*np.exp(-(x-b)**2/(2*c**2)))

# def gaussian2(p, a, p0, w):
#     x = (p0 - p)/(w/2)
#     return (a*np.exp(-np.log(2)*x**2))

# def lorentzian(p, a, p0, w):
#     x = (p0 - p) / (w / 2)
#     return (a*(1/(1+x**2)))

# def voigt(x, sigma, gamma, q):
#     g = np.exp(-x**2/(2*sigma**2))/(sigma*np.sqrt(2*np.pi))
#     l = gamma/(np.pi*((q - x)**2 + gamma**2))
#     return sp.integrate.quad(g*l, -np.inf, np.inf)

def SnTe_UVVis1(x,a,b,c,g,h):
    '''a: gaussian (SnTe abs.) height
    b: wavelength of peak max
    c: gaussian curve standard deviation/width'''
    gauss = (a*np.exp(-(x-b)**2/(2*c**2)))
    power = g*x**(-h)
    return (gauss+power)

# (param, covar) = opt.curve_fit(gaussian, wavelength, counts, p0 = [0.076, 2233, 50])#, bounds = (0, np.inf))
# print(param)

# (param2, covar2) = opt.curve_fit(gaussian2, wavelength, counts, p0 = [7.6e5, 823, 1])#, bounds = (0, np.inf))
# print(param2)

# (param3, covar3) = opt.curve_fit(lorentzian, wavelength, counts, p0 = [7.6e5, 823, 1])#, bounds = (0, np.inf))
# print(param3)

(param4, covar4) = opt.curve_fit(SnTe_UVVis1, wavelength, counts, p0 = [abcgh[0], abcgh[1], abcgh[2], abcgh[3], abcgh[4]])#, bounds = (0, np.inf))
print(param4)

x = np.arange(0,3500,1)
plt.figure(1)
plt.rcParams.update({'font.size': 14})
plt.plot(wavelength, counts,'o', color = 'b', label = 'Raw data')
# plt.plot(x, gaussian(x,param[0],param[1],param[2]), color = 'r', linewidth=1.0, label = 'Gaussian')
# plt.plot(x, gaussian2(x,param2[0],param2[1],param2[2]), color = 'g', linewidth=1.0, label = 'Gaussian 2')
# plt.plot(x, lorentzian(x,param3[0],param3[1],param3[2]), color = 'c', linewidth=1.0, label = 'Lorentzian')
plt.plot(x, SnTe_UVVis1(x,param4[0],param4[1],param4[2], param4[3], param4[4]), color = 'r', linewidth=1.0, label = 'Fit')
plt.grid(b=True, which='major', color='k', linestyle='-')
plt.grid(b=True, which='minor', color='0.65', linestyle='--')
plt.legend(loc = 1)
plt.minorticks_on()
plt.xlabel('$\lambda\ [nm]$')
plt.ylabel('$counts$')

ax = plt.subplot(111)
# text = '$I_{0} = %.2f$\n$<R_{g}^{2}> = %.3e$'%(param[0],param[1])
text = '$\lambda_{max} = %.2f\ nm$'%(param4[1])
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax.text(0.5, 0.75, text, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)

plt.tight_layout()
plt.xlim(0,3500)
plt.ylim(0, max(counts))
# plt.ylim(0,0.02)
plt.show()