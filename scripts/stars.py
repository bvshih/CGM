import pynbody
import matplotlib.pylab as plt

sim_fn = '/scratch/08263/tg875625/CGM/GMs/pioneer50h243.1536gst1bwK1BH/pioneer50h243.1536gst1bwK1BH.003456'
outpath = '/scratch/08263/tg875625/CGM/plots/'
s = pynbody.load(sim_fn)
s.physical_units()

h = s.halos()

h1 = h[1]

pynbody.analysis.angmom.sideon(h1)
pynbody.plot.stars.render(s, width='600 kpc', dynamic_range=8.0, filename=outpath+'stars_sideon_z0.17.pdf')

pynbody.analysis.angmom.faceon(h1)
pynbody.plot.stars.render(s, width='600 kpc', dynamic_range=8.0, filename=outpath+'stars_faceon_z0.17.pdf')