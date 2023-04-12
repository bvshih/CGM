import matplotlib.pyplot as plt
import cgm 
import numpy as np
import math

out_fn = '/scratch/08263/tg875625/CGM/plots/coolontime_histogram.pdf'

sim_fn = '/scratch/08263/tg875625/CGM/GMs/pioneer50h243.1536gst1bwK1BH/pioneer50h243.1536gst1bwK1BH.003456'

halo_cgm = cgm.isolate_cgm(sim_fn)
print('cgm cut')

coolontime = halo_cgm.g['coolontime'].in_units('Gyr') 

nonzero_coolontime = coolontime[coolontime>0]
zero_coolontime = coolontime[~(coolontime>0)]

fig, ax = plt.subplots()

bins = np.arange(0,12)
bins[0] = nonzero_coolontime.min()

ax.hist(nonzero_coolontime, bins = bins)
ax.hist(zero_coolontime, bins=1)

ax.semilogy()

ax.set_xlabel('coolontime [Gyr]')

plt.savefig(out_fn)