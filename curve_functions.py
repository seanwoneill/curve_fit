import numpy as np

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