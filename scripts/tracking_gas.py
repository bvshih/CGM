# tracks particles forwards in time

import pynbody
import pynbody.units as units

import matplotlib.pyplot as plt

def get_min(p1, p2,qty, qtyunits):
    '''
    p2: list of simsnaps    
    '''
    if qtyunits != None:
        current_min = min(p1[0].g[qty].in_units(qtyunits))
    else:
        current_min = min(p1[0].g[qty])

    for i in range(len(p2)):
        if qtyunits != None:
            temp_min = min(p2[i].g[qty].in_units(qtyunits))
        else:
            temp_min = min(p2[i].g[qty]) 

        if temp_min < current_min:
            current_min=temp_min

    return current_min

def get_max(p1,p2,qty, qtyunits):
    '''
    p2: list of simsnaps    
    '''
    if qtyunits != None:
        current_max = max(p1.g[qty].in_units(qtyunits))
    else:
        current_max = max(p1.g[qty])

    for i in range(len(p2)):
        if qtyunits != None:
            temp_max = max(p2[i].g[qty].in_units(qtyunits))
        else:
            temp_max = max(p2[i].g[qty]) 

        if temp_max > current_max:
            current_max=temp_max

    return current_max
def make_scatter(p1, p2, qty, out_fn, z1, z2, qtyunits=None):

    fig, axs = plt.subplots(ncols=2, nrows=len(p2)+1, figsize=(10,5*len(p2)+5.5))

    for ax in axs:
        for i in range(len(ax)):
            ax[i].set_xlim(-300,300)
            ax[i].set_ylim(-300,300)

    vmin = get_min(p1,p2,qty,qtyunits)
    vmax = get_max(p1,p2,qty,qtyunits)

    plane = ['y','z']
    if qtyunits != None:
    
        for i in range(len(plane)):
            p1_plt = axs[0,i].scatter(p1.g['x'].in_units('kpc'), p1.g[plane[i]].in_units('kpc'), 
                                      c=p1.g[qty].in_units(qtyunits), s=2, vmin=vmin, vmax=vmax, alpha = 0.5)
            axs[0,i].set_ylabel(plane[i]+ ' [kpc]')
            for j in range(len(p2)):
                    axs[j+1,i].scatter(p2[j].g['x'].in_units('kpc'), p2[j].g[plane[i]].in_units('kpc'),
                                       c=p2[j].g[qty].in_units(qtyunits), s=2, vmin=vmin, vmax=vmax, alpha = 0.)
                    axs[j+1,i].set_ylabel(plane[i]+ ' [kpc]')
    else:
        for i in range(len(plane)):
            p1_plt = axs[0,i].scatter(p1.g['x'].in_units('kpc'), p1.g[plane[i]].in_units('kpc'), c=p1.g[qty],
                                       s=2, vmin=vmin, vmax=vmax, alpha = 0.5)
            axs[0,i].set_ylabel(plane[i]+ ' [kpc]')
            for j in range(len(p2)):
                axs[j+1,i].scatter(p2[j].g['x'].in_units('kpc'), p2[j].g[plane[i]].in_units('kpc'),
                                   c=p2[j].g[qty], s=2, vmin=vmin, vmax=vmax, alpha = 0.5)
                axs[j+1,i].set_ylabel(plane[i] + ' [kpc]')

    axs[len(p2),0].set_xlabel('x [kpc]')
    axs[len(p2),1].set_xlabel('x [kpc]')
    
    axs[0,0].text(200,280,'z = '+ z1)

    for j in range(len(p2)):
        axs[j+1,0].text(200,280,'z = '+ z2[j])

    # colorbar
    plt.subplots_adjust(bottom=0.1)
    cax = plt.axes([0.15, 0.02, 0.7, 0.03])

    if qtyunits != None:    
        plt.colorbar(p1_plt, cax=cax, label = qty+' ' +qtyunits, orientation = 'horizontal', alpha = 1)
    else:
        plt.colorbar(p1_plt, cax=cax, label=qty+' '+str(p1.g[qty].units), orientation = 'horizontal', alpha=1)
    
    plt.savefig(out_fn+qty+'_scatter.pdf')
    print('scatter plot saved as '+out_fn+qty+'_scatter.pdf')


scatterplots=True

s1_fn = '/scratch/08263/tg875625/CGM/GMs/pioneer50h243.1536gst1bwK1BH/pioneer50h243.1536gst1bwK1BH.001920'
z1 = '0.86'

# file path for next timesteps starting at the latest
s2_fn = '/scratch/08263/tg875625/CGM/GMs/pioneer50h243.1536gst1bwK1BH/pioneer50h243.1536gst1bwK1BH.00'

# ts_nums = ['2554','2304']
# z2 = ['0.50','0.62']

ts_nums = ['3456','3195','3072','2688','2554','2304']
z2 = ['0.17','0.25','0.29','0.44','0.50','0.62']
ts_nums.reverse()
z2.reverse()
print(ts_nums)

# out file 
out_fn = '/scratch/08263/tg875625/CGM/plots/tracking_gas_z'+z1+'_'

# load sim 1
s1 = pynbody.load(s1_fn)
print(f'z = {z1} loaded')
s1.physical_units()
h1_s1 = s1.halos()[1]

pynbody.analysis.angmom.faceon(h1_s1)
print('centered and rotated')

amu = units.NamedUnit("amu", 1.66e-27*units.kg)

# filter
h1_s1.g['rho'].convert_units('amu cm**-3')  # convert density array to new units

rho_filt = pynbody.filt.HighPass('rho', '0.1 amu cm**-3')

# cool dense gas in disk of previous timestep
d1_s1 = h1_s1.g[rho_filt]
print('filtered')

s2 = []
h1_s2 = []
b = []
d1_s2 = []

for i in range(len(ts_nums)):

    # load previous timesteps
    s2.append(pynbody.load(s2_fn+ts_nums[i]))
    s2[i].physical_units()
    print(f'z = {z2[i]} loaded')
    h1_s2.append(s2[i].halos()[1])

    pynbody.analysis.angmom.faceon(h1_s2[i])
    print('centered and rotated')

    # bridge 
    b.append(s1.bridge(s2[i]))
    print('briged')

    # dense gas disk particles from sim 1 in sim 2
    d1_s2.append(b[i](d1_s1))
    
if scatterplots:
    qtys = ['vr']

    for qty in qtys:        
        make_scatter(d1_s1, d1_s2, qty, out_fn, z1, z2)
