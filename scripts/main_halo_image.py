import pynbody 
import pynbody.units as units

import pynbody.plot.sph as sph
import matplotlib.pyplot as plt

sim_fn = '/scratch/08263/tg875625/CGM/GMs/pioneer50h243.1536gst1bwK1BH/pioneer50h243.1536gst1bwK1BH.003456'

# load sim to pynbody
s = pynbody.load(sim_fn)
s.physical_units()
h = s.halos()

h1 = h[1]

pynbody.analysis.halo.center(h1,mode='hyb')
pynbody.analysis.angmom.faceon(h1, cen=(0,0,0))

rvir = pynbody.analysis.halo.virial_radius(h1) # in kpc

# filter for temp <=1.2e4 K
temp_filt = pynbody.filt.LowPass('temp', '1.2e4 K')

# filter for density n >= 0.1 amu cm^-3

amu = units.NamedUnit("amu", 1.66e-27*units.kg)
h1.g['rho'].convert_units('amu cm**-3')  # convert array to new units

rho_filt = pynbody.filt.HighPass('rho', '0.1 amu cm**-3')

# apply filters
cool_dense_gas = h1.g[temp_filt & rho_filt]

# plotting

fig, ax = plt.subplots()
sph.image(cool_dense_gas, qty='rho', units = 'amu cm**-3',  vmin=1e-5, width = '280 kpc', cmap='PuBu', subplot = ax) 

plt.savefig('/scratch/08263/tg875625/CGM/plots/h1_faceon_rvir_z0.17.pdf')


# side on 
pynbody.analysis.angmom.sideon(h1, cen=(0,0,0))

fig, ax = plt.subplots()
sph.image(cool_dense_gas, qty='rho', units='amu cm**-3', vmin=1e-5, width = '280 kpc', cmap='PuBu', subplot = ax) 
plt.savefig('/scratch/08263/tg875625/CGM/plots/h1_sideon_rvir_z0.17.pdf')
