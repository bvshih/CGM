# tracks particles that go from disk to CGM between two subsequent timesteps 
# plots the flux profile of cgm particles

import pynbody
import pynbody.analysis.profile as profile

import numpy as np

import matplotlib.pyplot as plt
from palettable.cmocean.sequential import Dense_3

def plot_profile(p_profile,out_fn):
    cmap = Dense_3.mpl_colors

    for i in range(len(p_profile)):
        print('plotting z=', z[i])
        rate = np.nanmean(p_profile[i]['vr'].in_units('kpc yr**-1'))*p_profile[i]['mass'].in_units('Msol')/p_profile[i]['rbins'].in_units('kpc')

        plt.plot(p_profile[i]['rbins'], rate,color=cmap[i],  label = f'{t[i+1]} Gyr')
        plt.yscale('symlog', linthresh=0.1)
 
    plt.legend()
    plt.xlabel(f"r [kpc]")
    plt.ylabel(f"rate [Msol yr**-1]")

    plt.savefig(out_fn+'profile.pdf')

def plot_quantile(p_quantile, out_fn):
    cmap = Dense_3.mpl_colors

    for i in range(len(p_quantile)):
        print(i)
        rate = np.nanmean(p_quantile[i]['vr'].in_units('kpc yr**-1')[:,1])*p_quantile[i]['mass'].in_units('Msol')[:,1]/p_quantile[i]['rbins'].in_units('kpc')
                
        rate_max = np.nanmean(p_quantile[i]['vr'].in_units('kpc yr**-1')[:,0])*p_quantile[i]['mass'].in_units('Msol')[:,0]/p_quantile[i]['rbins'].in_units('kpc')
        rate_min = np.nanmean(p_quantile[i]['vr'].in_units('kpc yr**-1')[:,2])*p_quantile[i]['mass'].in_units('Msol')[:,2]/p_quantile[i]['rbins'].in_units('kpc')
    
        plt.plot(p_quantile[i]['rbins'], rate, color=cmap[i], label = f'{t[i+1]} Gyr')
        plt.fill_between(p_quantile[i]['rbins'], rate_max, rate_min, color =cmap[i] , alpha=0.5)

    plt.yscale('symlog', linthresh=0.1)

    plt.legend()
    plt.xlabel(f"r [kpc]")
    plt.ylabel(f"rate [Msol yr**-1]")
    plt.savefig(out_fn+'quantile.pdf')


make_quantile = True
make_profile = False

fn = '/scratch/08263/tg875625/CGM/GMs/pioneer50h243.1536gst1bwK1BH/pioneer50h243.1536gst1bwK1BH.00'
ts_nums =['3456','3195','3072','2688','2554','2304','1920']
z = ['0.17','0.25','0.29','0.44','0.50','0.62', '0.86']


# ts_nums =['2554','2304','1920']
# z = ['0.50','0.62', '0.86']

rmax = '100'
out_fn = '/scratch/08263/tg875625/CGM/plots/disk2cgm_mass_rate_'+rmax+'kpc_'

ts_nums.reverse()
z.reverse()

t = []

s = []
h1 = []

for j in range(len(ts_nums)): 
    s.append(pynbody.load(fn+ts_nums[j]))
    t.append(round(s[j].properties['time'].in_units('Gyr'),2))
    print('t: ', t[j])
    print(f'z = {z[j]} loaded')
    s[j].physical_units()
    h1.append(s[j].halos()[1])

    pynbody.analysis.angmom.faceon(h1[j])
    print('centered and rotated')


# create filters for disk 
rdisk = "15 kpc"
height = "5 kpc" # height is from midplane
disk = pynbody.filt.Disc(rdisk, height, cen=(0,0,0))  

if make_profile:
    p_profile = []
if make_quantile:
    p_quantile = []

for i in range(len(ts_nums)-1):
    print(f'tracking dense particles from z = {z[i]}')
    
    # find disk particles 
    p = [h1[i].g[disk]]
    print(f'found disk particles')

    # track to next ts 
    b =  s[i].bridge(s[i+1])
    p.append(b(p[0]))
    print(p[1])

    # filter out particles still in disk 
    p[1].g[~disk]

    p[1].g['mass'].convert_units('Msol')
    p[1].g['vr'].convert_units('kpc s**-1')

    if make_profile:
        p_profile.append(profile.Profile(p[1].g, rmax= rmax+' kpc', ndim=3))
    if make_quantile:
        p_quantile.append(profile.QuantileProfile(p[1].g, rmax=rmax+' kpc', ndim=3))
        
print('plotting rate profiles')
print('len p_quantile:', len(p_quantile))
if make_profile:
    plot_profile(p_profile, out_fn)
if make_quantile:
    plot_quantile(p_quantile, out_fn)