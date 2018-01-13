import solvents
#    #File containing absorbance data
file = '20171115_SnTe_Absorbance.xlsx'

#    #Column numbers from 'file' designating the x (wavelength) and y (absorbance) data to be fit
x_col = 0
y_col = 1

#    #Subject absorbance fitting parameters
abcgh = {'a':0.08, 'b':2100., 'c':300., 'g':100, 'h':-5, 'shift':0.}
# print(add_Base + add_Folder + add_File)

solvents_remove = [solvents.acetone1_300]#, solvents.chloroform1_600, solvents.OA1_1500]

#    #Solvent absorbance curve fitting parameters
acetone_abcgh = {'a':0.09, 'b':2263., 'c':30., 'g':1.8e7, 'h':2.8, 'shift':0.075}
chloroform_abcgh = {'a':0.1, 'b':2372., 'c':30., 'g':1.8e7, 'h':2.8, 'shift':0.09}
OA_abcgh = {'a':0.07, 'b':2832., 'c':50., 'g':1.8e7, 'h':2.8, 'shift':0.06}
solvent_correction_dict = { 2263:acetone_abcgh, 2372:chloroform_abcgh, 2832:OA_abcgh }

#    #Row on which to being reading in raw daa
#    #start after 2 to remove column header; after ~300 to remove quartz peak
start_row = 2