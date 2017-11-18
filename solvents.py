import xlrd as xlrd
import scipy.optimize as opt
import matplotlib.pyplot as plt
import numpy as np
import curve_functions, setup_parameters

raw_data = xlrd.open_workbook(filename = r'C:\Users\Sean\PhD UR\Data\UV-Vis-NIR Absorbance\20171117\20171117_Solvent spectra.xlsx').sheet_by_index(0)

def debug_plotting(x, y):
    plt.figure(1)
    plt.rcParams.update({'font.size': 14})
    plt.plot(x, y, '-', color='b', label='Raw data')
    plt.grid(b=True, which='major', color='k', linestyle='-')
    plt.grid(b=True, which='minor', color='0.65', linestyle='--')
    plt.legend(loc=2)
    plt.minorticks_on()
    plt.xlabel('$\lambda\ [nm]$')
    plt.ylabel('$counts$')

    plt.tight_layout()
    # plt.xlim(350, 3000)
    # plt.ylim(0, max(y))
    # plt.ylim(0,0.02)
    plt.show()

class class_Solvent:
    def __init__(self,dat,typ):
        solvent_normalization_peak = {'acetone': 2263, 'chloroform': 2373, 'OA': 2832}
        self.solvent_data = dat
        self.peak = solvent_normalization_peak[typ]

def data_Lists(raw, col_no):
    temp_list = []
    for i in range(2, len(raw.col(col_no))):
        if type(raw.cell_value(i, col_no)) != type('string'):
            # if raw.cell_value(i, col_no) < 0: temp_list.append(raw.cell_value(i, col_no))
            if raw.cell_value(i, col_no) < 0: temp_list.append(0.)
            else: temp_list.append(raw.cell_value(i, col_no))
    return(temp_list)


def remove_solvents(data_abs_list, data_wave_list, solvent_abs_list, solvent_wave_list):
    """
    Remove solvent absorbance data from subject UV/Vis data.
    :param data_abs_list: list of subject absorbance data
    :param data_wave_list: list of subject wavelength data
    :param solvent_abs_list: list of solvent absorbance data
    :param solvent_wave_list: list of solvent wavelength data
    :return: List of corrected data
    """

    # peak_halfwidth = 30
    # solvent_wavelength_bounds = [solvent_abs_list.peak - peak_halfwidth, solvent_abs_list.peak + peak_halfwidth]
    # abs_index_bounds = [data_wave_list.index(solvent_wavelength_bounds[1]), data_wave_list.index(solvent_wavelength_bounds[0])]
    # trimmed_data_wave = data_wave_list[abs_index_bounds[0]:abs_index_bounds[1]]
    # # trimmed_solvent_abs = class_Solvent(solvent_abs_list.solvent_data[solvent_index_bounds[0]:solvent_index_bounds[1]],\
    # #                                      solvent_abs_list.peak)
    # trimmed_data_abs = data_abs_list[abs_index_bounds[0]:abs_index_bounds[1]]
    # debug_plotting(trimmed_data_wave, trimmed_data_abs)
    #
    # #acetone_abcgh = {'a':0.09, 'b':2263., 'c':30., 'g':1.8e7, 'h':2.8, 'shift':0.075}
    # # (param, covar) = opt.curve_fit(curve_functions.gaussian, trimmed_data_wave, trimmed_data_abs, \
    # #                                  p0 = [0.09, 2263, 30, 1.8e7, 2.8, 0.075])
    #
    # # debug_plotting(np.arange(solvent_wavelength_bounds[1],solvent_wavelength_bounds[0],1),\
    # #                curve_functions.gaussian(np.arange(solvent_wavelength_bounds[1],solvent_wavelength_bounds[0],1),param[0],param[1],param[2], param[3]))

    solvent_adj_list = []
    # solvent_index = 0
    for x in range(len(data_wave_list)):
        #This just reads in the subject data wavelength, looks up the index of that wavelength in the solvent data,
        #and returns the corresponding solvent absorbance.  Then that solvent absorbance is subtracted from the subject
        #data absorbance.  A list of solvent-adjusted subject data absorbance is returned.
        current_data_wave = data_wave_list[x]
        solvent_index = solvent_wave_list.index(current_data_wave)
        # print(solvent_abs_list.peak)
        solvent_adj_list.append(data_abs_list[x] - solvent_abs_list.solvent_data[solvent_index])

    return(solvent_adj_list)

    wavelength = data_Lists(raw_data, 0)
    acetone1_600 = class_Solvent(data_Lists(raw_data, 1), 'acetone')
    acetone1_300 = class_Solvent(data_Lists(raw_data, 2), 'acetone')
    acetone1_60 = class_Solvent(data_Lists(raw_data, 3), 'acetone')
    acetone1_30 = class_Solvent(data_Lists(raw_data, 4), 'acetone')
    chloroform1_600 = class_Solvent(data_Lists(raw_data, 5), 'chloroform')
    chloroform1_300 = class_Solvent(data_Lists(raw_data, 6), 'chloroform')
    chloroform1_60 = class_Solvent(data_Lists(raw_data, 7), 'chloroform')
    OA1_1500 = class_Solvent(data_Lists(raw_data, 8), 'OA')
    OA1_600 = class_Solvent(data_Lists(raw_data, 9), 'OA')
    OA1_300 = class_Solvent(data_Lists(raw_data, 10), 'OA')

# debug_plotting(wavelength, acetone1_600)