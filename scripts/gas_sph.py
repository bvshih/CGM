import pynbody

import matplotlib.pyplot as plt
import pynbody.plot.sph as sph

def sph_img(s, h1, z, t, outfn):
    
    vmin = 1e-5
    vmax = 1e0

    fig, ax = plt.subplots(ncols=2, sharey=True,figsize=(20,10))

    # faceon = sph.image(s[i].g, qty='rho', units='g cm**-2', vmin=vmin, vmax=vmax,
    #                 width='600 kpc', subplot = ax[0], ret_im=True, show_cbar=False)
    faceon = sph.velocity_image(s.g, qty = 'rho', width='300 kpc', mode='stream', units='g cm**-2', 
                density = 1.0, vector_resolution=100, vmin=vmin, vmax=vmax,subplot=ax[0], 
                show_cbar=False, vector_color='white', ret_im=True)
    print('plotted faceon')

    pynbody.analysis.angmom.sideon(h1)
    print('rotated to sideon')
    
    # sph.image(s[i].g, qty='rho', units='g cm**-2', vmin=vmin, vmax=vmax,
    #                    width='600 kpc', subplot = ax[1], show_cbar=False)
    sph.velocity_image(s.g, qty = 'rho', width='300 kpc', mode='stream', units='g cm**-2', 
                density = 1.0, vector_resolution=100, vmin=vmin, vmax=vmax,subplot=ax[1], 
                show_cbar=False, vector_color='white')
    print('plotted sideon')


    ax[0].set_ylabel('y/kpc')
    ax[1].set_ylabel('z/kpc')
    ax[0].set_xlabel('x/kpc')
    ax[1].set_xlabel('x/kpc')

    ax[1].text(200,200, str(round(t,2)) + ' Gyr')

    plt.subplots_adjust(right=0.8)
    cax = plt.axes([0.85, 0.15, 0.03, 0.65])
    plt.colorbar(faceon, cax=cax, label='g cm**-2')

    outfn = outfn+z+'_sph_vector_300kpc_3.pdf'
    plt.savefig(outfn)
    print('saved as '+outfn)

fn = '/scratch/08263/tg875625/CGM/GMs/pioneer50h243.1536gst1bwK1BH/pioneer50h243.1536gst1bwK1BH.00'
ts_nums =['3456','3195','3072','2688','2554','2304','1920']
z = ['0.17','0.25','0.29','0.44','0.50','0.62', '0.86']

# ts_nums = ['0972','1152','1536','1739']
#z = ['','','','1.00']

outfn = '/scratch/08263/tg875625/CGM/plots/tracking_gas/tracking_gas_'

ts_nums.reverse()
z.reverse()
for j in range(len(ts_nums)): 
    s = pynbody.load(fn+ts_nums[j])
    print(f'z = {z[j]} loaded')
    s.physical_units()
    t = s.properties['time'].in_units('Gyr')
    h1 = s.halos()[1]

    pynbody.analysis.angmom.faceon(h1)
    print('centered and rotated')

    print('making sph image')   
    sph_img(s, h1, z[j], t, outfn)

