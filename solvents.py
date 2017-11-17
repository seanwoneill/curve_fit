import xlrd as xlrd
import matplotlib.pyplot as plt

raw_data = xlrd.open_workbook(filename = r'C:\Users\Sean\PhD UR\Data\UV-Vis-NIR Absorbance\20171117\20171117_Solvent spectra.xlsx').sheet_by_index(0)

trailingZeros = 2651

def data_Lists(raw, col_no):
    temp_list = []
    for i in range(2, len(raw.col(col_no))):
        if type(raw.cell_value(i, col_no)) != type('string'):
            if raw.cell_value(i, col_no) < 0: temp_list.append(raw.cell_value(i, col_no))
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
    solvent_adj_list = []
    solvent_index = 0
    for x in range(len(data_wave_list)):
        current_data_wave = data_wave_list[x]
        solvent_index = solvent_wave_list.index(current_data_wave)
        solvent_adj_list.append(data_abs_list[x] - solvent_abs_list[solvent_index])
    return(solvent_adj_list)


wavelength = data_Lists(raw_data,0)
acetone1_600 = data_Lists(raw_data,1)
acetone1_300 = data_Lists(raw_data,2)
acetone1_60 = data_Lists(raw_data,3)
acetone1_30 = data_Lists(raw_data,4)
chloroform1_600 = data_Lists(raw_data,5)
chloroform1_300 = data_Lists(raw_data,6)
chloroform1_60 = data_Lists(raw_data,7)
OA1_1500 = data_Lists(raw_data,8)
OA1_600 = data_Lists(raw_data,9)
OA1_300 = data_Lists(raw_data,10)

# y = chloroform1_600
# plt.figure(1)
# plt.rcParams.update({'font.size': 14})
# plt.plot(wavelength, y, '-', color = 'b', label = 'Raw data')
# plt.grid(b=True, which='major', color='k', linestyle='-')
# plt.grid(b=True, which='minor', color='0.65', linestyle='--')
# plt.legend(loc = 2)
# plt.minorticks_on()
# plt.xlabel('$\lambda\ [nm]$')
# plt.ylabel('$counts$')
#
# plt.tight_layout()
# plt.xlim(350,3000)
# plt.ylim(0, max(y))
# # plt.ylim(0,0.02)
# plt.show()