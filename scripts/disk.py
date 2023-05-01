import pynbody
import pynbody.units as units

import matplotlib.pyplot as plt
import pynbody.plot.sph as sph

import numpy as np


def radial_dist_plot(p, out_fn):
    ''' 
    radial distribution histogram
    p: sim snap of gas particles only
    '''
    print(len(p),' particles')

    cgm, disk = categorize_p(p)
    fig, ax = plt.subplots()

    rmax = 300
    bins = np.linspace(0, rmax, num = 100)
    print('making radial dist plot')
    ax.hist(cgm['r'], bins = bins, alpha = 0.5, label='cgm', color='coral' )
    ax.hist(disk['r'], bins = bins, label = 'disk', alpha = 0.5, color='gold')

    ax.semilogy()
    ax.set_xlabel('r [kpc]')
    ax.set_ylim(1,3e4)

    ax.set_title('radial distribution of z = '+z2[i]+' disk particles in z = 0.17')
    plt.savefig(out_fn+'radial_dist.pdf')
    print('radial dist plot saved')
    plt.clf()


def categorize_p(p, rdisk="15 kpc", height='5 kpc'):
    '''filter particles in disk vs cgm'''
    disk_filt = pynbody.filt.Disc(rdisk, height, cen=(0,0,0))
    cgm = p[~disk_filt]
    disk = p[disk_filt]

    return cgm, disk


# file path for sim
s1_fn = '/scratch/08263/tg875625/CGM/GMs/pioneer50h243.1536gst1bwK1BH/pioneer50h243.1536gst1bwK1BH.003456'
z1 = '0.17'

# file path for previous timestep 
s2_fn = '/scratch/08263/tg875625/CGM/GMs/pioneer50h243.1536gst1bwK1BH/pioneer50h243.1536gst1bwK1BH.00'
ts_nums = ['3195','3072','2688','2554','2304', '1920', '1739']
z2=['0.25','0.29','0.44','0.50','0.62','0.86', '1.00']

# load sim 1
s1 = pynbody.load(s1_fn)
s1.physical_units()
print('s1 loaded')
h1_s1 = s1.halos()[1]

pynbody.analysis.angmom.faceon(h1_s1)
print('s1 centered and rotated')

amu = units.NamedUnit("amu", 1.66e-27*units.kg)


for i in range(len(ts_nums)):
    out_fn = '/scratch/08263/tg875625/CGM/plots/disk_z'+z1+'_z'+z2[i]+'_'

    # load previous timestep
    s2 = pynbody.load(s2_fn+ts_nums[i])
    s2.physical_units()
    print('s2 loaded')
    h1_s2 = s2.halos()[1]

    pynbody.analysis.angmom.faceon(h1_s2)
    print('s2 centered rotated')

    # filter
    rdisk = "15 kpc"
    height = "5 kpc"
    disk_filt = pynbody.filt.Disc(rdisk, height, cen=(0,0,0))  

    temp_filt = pynbody.filt.LowPass('temp', '1.2e4 K')

    h1_s2.g['rho'].convert_units('amu cm**-3')  # convert array to new units

    rho_filt = pynbody.filt.HighPass('rho', '0.1 amu cm**-3')

    # metals_filt = pynbody.filt.HighPass('metals', 0.0134)

    # cool dense gas in disk of previous timestep
    d1_s2 = h1_s2.g[disk_filt & temp_filt & rho_filt]
    print('filtered s2')

    # bridge 
    b = s1.bridge(s2)
    print('briged')

    # cool dense gas disk particles from sim 2 in sim 1 
    d1_s1 = b(d1_s2)

    # radial dist plot 
    radial_dist_plot(d1_s1.g, out_fn)

# s1_min = min(d1_s1.g['rho'])
# s1_max = max(d1_s1.g['rho'])  

# s2_min = min(d1_s2.g['rho'])
# s2_max = max(d1_s2.g['rho'])

# fig, ax = plt.subplots(ncols=2, nrows=2, sharex=True, sharey=True)
# im1 = sph.image(d1_s1.g, qty='rho', vmin=s1_min, vmax=s1_max, width = '300 kpc', cmap='Purples', subplot = ax[0,0],ret_im=True, show_cbar=False) 
# im2 = sph.image(d1_s2.g, qty='rho', vmin=s2_min, vmax=s2_max, width = '300 kpc', cmap='Blues', subplot = ax[1,0], ret_im=True, show_cbar=False) 
# print('faceon images made')

# pynbody.analysis.angmom.sideon(h1_s1)
# print('rotated s1 to sideon')
# pynbody.analysis.angmom.sideon(h1_s2)
# print('rotated s2 to sideon')

# sph.image(d1_s1.g, qty='rho',  vmin=s1_min, vmax=s1_max, width = '300 kpc', cmap='Purples', subplot = ax[0,1], show_cbar=False) 
# sph.image(d1_s2.g, qty='rho',   vmin=s2_min, vmax=s2_max, width = '300 kpc', cmap='Blues', subplot = ax[1,1], show_cbar=False) 
# print('sideon images made')

# plt.subplots_adjust(right=0.8)
# cax1 = plt.axes([0.85, 0.55, 0.03, 0.3])
# cax2 = plt.axes([0.85, 0.1, 0.03, 0.3])

# plt.colorbar(im1, cax=cax1, label='amu cm**-3')
# plt.colorbar(im2, cax=cax2, label='amu cm**-3')

# ax[1,0].set_ylabel('z/kpc')
# ax[0,0].set_ylabel('z/kpc')

# ax[0,0].text(-150,150,'z = 0.17')
# ax[1,0].text(-150,150,'z = 0.25')
# plt.savefig(out_fn+'sph_img.pdf')
# print('sph image plot complete')
