import numpy as np
import sympy as sp

def gaussian(x,a,b,c,shift):
    return (a*np.exp(-(x-b)**2/(2*c**2)) + shift)

def gaussian2(p, a, p0, w):
    x = (p0 - p)/(w/2)
    return (a*np.exp(-np.log(2)*x**2))

def lorentzian(p, a, p0, w):
    x = (p0 - p) / (w / 2)
    return (a*(1/(1+x**2)))

def voigt(x, sigma, gamma, q):
    g = np.exp(-x**2/(2*sigma**2))/(sigma*np.sqrt(2*np.pi))
    l = gamma/(np.pi*((q - x)**2 + gamma**2))
    return sp.integrate.quad(g*l, -np.inf, np.inf)

def SnTe_UVVis1(x,a,b,c,g,h,shift):
    '''a: gaussian (SnTe abs.) height
    b: wavelength of peak max
    c: gaussian curve standard deviation/width'''
    gauss = (a*np.exp(-(x-b)**2/(2*c**2)) + shift)
    power = g*x**(-h)
    return (gauss+power)

## Fit solvent peak data with polynomial, find + second derivative that coincide with zero 1st derivative to find
## local maxima - fit gaussian to that point??
def deriv(x,y,t):
    a = 5
    param = np.polyfit(x,y,a)
    # z = sp.symbols('z')
    # fDeriv = sp.diff(float(param[0])*z**5 + float(param[1])*z**4 + float(param[2])*z**3 + float(param[3])*z**2 + float(param[4])*z + float(param[5]), z)
    # sDeriv = sp.diff(fDeriv, z)
    # print(fDeriv)
    fDeriv = []
    for i in range(len(param)):
        fDeriv.append(param[i]*(a-i))
    print(fDeriv)
    if t == 1: return fDeriv
    elif t == 2: return sDeriv
    else: return "wrong!"