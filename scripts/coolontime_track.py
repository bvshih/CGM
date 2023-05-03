import cgm
import pynbody
import numpy as np

import matplotlib.pyplot as plt
import pynbody.plot.sph as sph
import pynbody.analysis.profile as profile

def select_coolontimes(sim, time):

    time_filter = pynbody.filt.HighPass('coolontime',f'{time:.6f} Gyr')
    selected_gas = sim.g[time_filter]
    print('coolontime particle selection complete')
    return selected_gas

def get_p1(sim1_fn, sim2_fn, return_halos=True, return_sim=True):
    '''
    sim2 is the previous timestep of sim1
    returns the p1 in sim1 and sim2
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
    sim1_p = select_coolontimes(sim1_cgm, sim2_time)

    # track selected particles
    sim2_p = b(sim1_p)
    
    print('p2 found')

    results = [sim1_p, sim2_p]
    if return_halos:
        results.append(sim1_h1)
        results.append(sim2_h1)
    if return_sim:
        results.append(sim1)
        results.append(sim2)

    return (*results,) # maybe i should return it as a dictionary...

    
def radial_dist_plot(p1, p2, out_fn):
    fig, ax = plt.subplots(2)

    rvir = 300
    disk_height = 5
    bins = np.linspace(0, rvir, num = rvir/disk_height)

    ax[0].hist(p1, bins = bins, alpha = 0.5, color='slateblue')
    ax[1].hist(p2['cgm'], bins = bins, label = 'cgm', alpha = 0.5, color='coral' )
    ax[1].hist(p2['disk'], bins = bins, label = 'disk', alpha = 0.5, color='gold')

    ax[0].semilogy()
    ax[1].semilogy()
    ax[1].legend()
    ax[1].set_xlabel('r [kpc]')

    ax[1].set_ylim([*(ax[0].get_ylim())])
    ax[0].set_xticklabels([])

    ax[0].set_title('z = 0.17')
    ax[1].set_title('z = 0.25')
    plt.savefig(out_fn+'radial_dist.pdf')

def categorize_p(p, rdisk="15 kpc", height='5 kpc'):
    '''filter particles in disk vs cgm'''
    disk_filt = pynbody.filt.Disc(rdisk, height, cen=(0,0,0))
    cgm = p[~disk_filt]
    disk = p[disk_filt]

    return cgm, disk

def make_sph_img(sim1_h1, sim2_h1, view, outfn):

    fig, ax = plt.subplots(ncols=2, sharey=True)

    vmin = 10
    vmax = 13

    img1 = sph.image(sim1_h1.g, qty='coolontime', units='Gyr', width='600 kpc', cmap='viridis', log=False, resolution = 1000, subplot=ax[0], title= 'z = 0.17', qtytitle='coolontime [Gyr]' ,show_cbar = False, ret_im=True, vmin=vmin, vmax=vmax)

    sph.image(sim2_h1.g, qty = 'coolontime', units='Gyr', width = '600 kpc', cmap='viridis', log=False, resolution = 1000, subplot = ax[1], title='z = 0.25', show_cbar=False, vmin=vmin, vmax=vmax) 

    plt.subplots_adjust(right=0.8)
    cax = plt.axes([0.85, 0.2, 0.05, 0.6])

    plt.colorbar(img1, cax=cax)

    if view == 'faceon':

        plt.savefig(outfn+'coolontime_sph_faceon.pdf')
    else:
        plt.savefig(outfn+'coolontime_sph_sideon.pdf')

def make_scatter(p1, p2, qty, out_fn, z1, z2, qtyunits=None):

    for plane in [['x','y'],['x','z']]:
        fig, axs = plt.subplots(ncols=2, sharey=True, figsize=(25,10))

        for ax in axs:
            ax.set_xlim(-300,300)
            ax.set_ylim(-300,300)


        if qtyunits != None:
            p1_plt = axs[0].scatter(p1.g[plane[0]].in_units('kpc'), p1.g[plane[1]].in_units('kpc'), c=p1.g[qty].in_units(qtyunits), s=5, vmin=p1.g[qty].min(), vmax=p1.g[qty].max())
            p2_plt = axs[1].scatter(p2.g[plane[0]].in_units('kpc'), p2.g[plane[1]].in_units('kpc'),  c=p2.g[qty].in_units(qtyunits), s=5, vmin=p1.g[qty].min(), vmax=p1.g[qty].max())
        else:
            p1_plt = axs[0].scatter(p1.g[plane[0]].in_units('kpc'), p1.g[plane[1]].in_units('kpc'), c=p1.g[qty], s=5, vmin=p1.g[qty].min(), vmax=p1.g[qty].max())
            p2_plt = axs[1].scatter(p2.g[plane[0]].in_units('kpc'), p2.g[plane[1]].in_units('kpc'),  c=p2.g[qty], s=5, vmin=p1.g[qty].min(), vmax=p1.g[qty].max())
        
        axs[0].set_title('z = '+ z1)
        axs[1].set_title('z = '+ z2)
        
        axs[0].set_ylabel(plane[1] + ' [kpc]')
        axs[0].set_xlabel('x [kpc]')
        axs[1].set_xlabel('x [kpc]')

        plt.subplots_adjust(right=0.8)
        cax = plt.axes([0.85, 0.1, 0.02, 0.8])

        if qtyunits != None:    
            plt.colorbar(p1_plt, cax=cax, label = qtyunits)
        else:
            plt.colorbar(p1_plt, cax=cax, label=qty+' '+str(p1.g[qty].units))

        plt.savefig(out_fn+qty+'_scatter_'+plane[0]+plane[1]+'.pdf')
        print('scatter plot saved')


def velocity_plot(sim1_h1, sim2_h1,view, out_fn):

    sim1_h1.properties['boxsize'] =  pynbody.units.Unit("1000 Mpc")
    sim2_h1.properties['boxsize'] =  pynbody.units.Unit("1000 Mpc")

    fig, ax = plt.subplots(ncols=2, sharey=True)

    img1 = sph.velocity_image(sim1_h1, width = '600 kpc', cmap = "Greys_r", mode='stream', subplot=ax[0], threaded=False, title='z = 0.17')  

    sph.velocity_image(sim2_h1, width='600 kpc', cmap = "Greys_r", mode='stream', subplot=ax[1], threaded=False, title='z = 0.25')

    if view=='sideon':
        plt.savefig(out_fn+'vel_sph_sideon.pdf')  
    else:
        plt.savefig(out_fn+'vel_sph_faceon.pdf')


def vel_profile(p1, p2, out_fn,z1,z2):
    fig, ax = plt.subplots()

    p1_p = profile.Profile(p1, vmin='0.1 kpc', vmax='280 kpc', ndim=3)
    p2_p =  profile.Profile(p2, vmin='0.1 kpc', vmax='280 kpc', ndim=3)

    ax.plot(p1_p['rbins'], p1_p['vr'], label='z='+z1)
    ax.plot(p2_p['rbins'], p2_p['vr'], label='z='+z2)

    ax.set_xlabel('r [kpc]')
    ax.set_ylabel('vr [km s**-1]')

    ax.legend()

    plt.savefig(out_fn+'vel_profile_3d.pdf')
    print('velocity profile saved')