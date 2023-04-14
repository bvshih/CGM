import cgm
import pynbody
import numpy as np
import matplotlib.pyplot as plt

def select_coolontimes(sim, time):

    time_filter = pynbody.filt.HighPass('coolontime',f'{time:.6f} Gyr')
    selected_gas = sim.g[time_filter]
    print('coolontime particle selection complete')
    return selected_gas


def get_particles(sim1_fn, sim2_fn, return_halos, return_sim):
    '''
    sim2 is the previous timestep of sim1
    returns the particles and their progenitors
    '''

    # get cgm of sim 1
    sim1_cgm, sim1, sim1_h1 = cgm.isolate_cgm(sim1_fn, True)

    # load sim2
    sim2 = pynbody.load(sim2_fn)
    sim2.physical_units()
    sim2_h1 = sim2.halos()[1]

    print('simulation 2 loaded')
   
    pynbody.analysis.halo.center(sim2_h1, mode='hyb')
    pynbody.analysis.angmom.faceon(sim2_h1, cen=(0,0,0))
    print('simulation 2 centered and aligned')
    
    # bridge sim2 and sim1
    b = sim2.bridge(sim1_cgm)
    print('created bridge')

    sim2_time = sim2.properties['time'].in_units('Gyr')

    # coolontime cut
    sim1_particles = select_coolontimes(sim1_cgm, sim2_time)

    # find progenitors of selected particles
    progenitors = b(sim1_particles)
    
    print('progenitors found')

    if return_halos and return_sim:
        return sim1_particles, progenitors, sim1_h1, sim2_h1, sim1, sim2
    elif return_halos and not(return_sim):
        return sim1_particles, progenitors, sim1_h1, sim2_h1
    elif not(return_halos) and return_sim:
        return sim1_particles, progenitors, sim1, sim2
    else:
        return sim1_particles, progenitors

def distance(x,y,z):
    # coordinates should be from centered sim
    return np.sqrt(x**2+y**2+z**2)

def calculate_r(particles):
    r = [distance(particles['x'][i], particles['y'][i], particles['z'][i]) for i in range(len(particles))]
    return r 
    

def radial_dist_plot(particles, progenitors, out_fn):
    fig, ax = plt.subplots(2)

    rvir = 300
    disk_height = 5
    bins = np.linspace(0, rvir, num = rvir/disk_height)

    ax[0].hist(particles, bins = bins, alpha = 0.5, color='slateblue')
    ax[1].hist(progenitors['cgm'], bins = bins, label = 'cgm', alpha = 0.5, color='coral' )
    ax[1].hist(progenitors['disk'], bins = bins, label = 'disk', alpha = 0.5, color='gold')

    ax[0].semilogy()
    ax[1].semilogy()
    ax[1].legend()
    ax[1].set_xlabel('r [kpc]')

    ax[1].set_ylim([*(ax[0].get_ylim())])
    ax[0].set_xticklabels([])

    ax[0].set_title('z = 0.17')
    ax[1].set_title('z = 0.25')
    plt.savefig(out_fn+'radial_dist.pdf')

def categorize_particles(particles, rdisk="15 kpc", height='5 kpc'):
    '''filter particles in disk vs cgm'''
    disk_filt = pynbody.filt.Disc(rdisk, height, cen=(0,0,0))
    cgm = particles[~disk_filt]
    disk = particles[disk_filt]

    return cgm, disk

# file path for sim
sim1_fn = '/scratch/08263/tg875625/CGM/GMs/pioneer50h243.1536gst1bwK1BH/pioneer50h243.1536gst1bwK1BH.003456'

# file path for previous timestep 
sim2_fn = '/scratch/08263/tg875625/CGM/GMs/pioneer50h243.1536gst1bwK1BH/pioneer50h243.1536gst1bwK1BH.003195'

out_fn = '/scratch/08263/tg875625/CGM/plots/'

particles, progenitors, sim1_h1, sim2_h1 = get_particles(sim1_fn, sim2_fn, return_halos=True, return_sim=False)

progenitors_cgm, progenitors_disk = categorize_particles(progenitors)

particles_r = calculate_r(particles)

progenitors_r = {'cgm':calculate_r(progenitors_cgm), 'disk': calculate_r(progenitors_disk)}

radial_dist_plot(particles_r, progenitors_r, out_fn)
