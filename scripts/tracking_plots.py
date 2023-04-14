import coolontime_track
import matplotlib.pyplot as plt
import numpy as np

def radial_dist_plot(particles, progenitors, out_fn):
    fig, ax = plt.subplots()
    
    bins = np.linspace()

    ax.hist(particles)

# file path for sim
sim1_fn = '/scratch/08263/tg875625/CGM/GMs/pioneer50h243.1536gst1bwK1BH/pioneer50h243.1536gst1bwK1BH.003456'

# file path for previous timestep 
sim2_fn = '/scratch/08263/tg875625/CGM/GMs/pioneer50h243.1536gst1bwK1BH/pioneer50h243.1536gst1bwK1BH.003195'

# path to plots directory
out_fn = '/scratch/08263/tg875625/CGM/plots/'

particles, progenitors = coolontime_track.get_particles(sim1_fn, sim2_fn)

