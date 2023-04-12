import matplotlib.pyplot as plt
import cgm 
import numpy as np
import matplotlib as mpl

def histogram(property, property_str, out_fn):
    fig, ax = plt.subplots()

    ax.hist(property, bins = 30)

    ax.semilogy()

    if property_str == 'metallicity':
        ax.set_xlabel(r'Metallicity [$log_{10}(\frac{Z}{Z_{\odot}})$]')
        plt.savefig(out_fn+'metallicity_histogram.pdf')
    elif property_str == 'coolontime':
        ax.set_xlabel('coolontime [Gyr]')
        plt.savefig(out_fn+'coolontime_hist.pdf')   
    
    print('histogram saved')

def scatter(property_1, property_1_str, property_2, property_2_str, out_fn):
    fig, ax = plt.subplots()

    ax.scatter(property_1, property_2, alpha = 0.5, s = 5)

    plt.savefig(out_fn+property_1_str+'_'+property_2_str+'_scatter.pdf')  
    print('scatter plot saved')

def hist_2d(property_1, property_1_str, property_2, property_2_str, out_fn):
    fig, ax = plt.subplots()

    im = ax.hist2d(property_1, property_2, bins=[100,100], norm=mpl.colors.LogNorm())
    plt.colorbar(im, cax=ax)

    ax.set_xlabel(property_1_str)
    ax.set_ylabel(property_2_str)

    plt.savefig(out_fn+property_1_str+'_'+property_2_str+'_hist2d.pdf')  
    print('hist2d plot saved')

out_fn = '/scratch/08263/tg875625/CGM/plots/'

sim_fn = '/scratch/08263/tg875625/CGM/GMs/pioneer50h243.1536gst1bwK1BH/pioneer50h243.1536gst1bwK1BH.003456'

halo_cgm = cgm.isolate_cgm(sim_fn)

solar_metallicity = 0.0134

metallicity = np.log10(halo_cgm.g['metals']/solar_metallicity)

coolontime = halo_cgm.g['coolontime'].in_units('Gyr') 

# scatter(coolontime, 'coolontime', metallicity, 'metallicity', out_fn)
# hist_2d(coolontime, 'coolontime', metallicity, 'metallicity', out_fn)
histogram(metallicity, 'metallicity', out_fn)
histogram(coolontime, 'coolontime', out_fn)