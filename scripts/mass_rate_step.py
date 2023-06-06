# calculates the rate of mass lost from disk to CGM and tracks those particles forward in time
# plots the flux profile of cgm particles

import pynbody
import pynbody.analysis.profile as profile

import numpy as np

import matplotlib.pyplot as plt

fn = '/scratch/08263/tg875625/CGM/GMs/pioneer50h243.1536gst1bwK1BH/pioneer50h243.1536gst1bwK1BH.00'

# low to high redshift 
ts_nums =['3456','3195','3072','2688','2554']
z = ['0.17','0.25','0.29','0.44','0.50']

out_fn = '/scratch/08263/tg875625/CGM/plots/step_mass_rate_profile_symlog.pdf'

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

# particles in disk at earliest time
p = [h1[0].g[disk]]

for i in range(1,len(ts_nums)):
    print(f'tracking dense particles at z = {z[i]}')

    # bridge adjacent timesteps 
    b =  s[i-1].bridge(s[i])

    # find particles 
    p.append(b(p[i-1]))

p_profile = []
for i in range(len(p)):
    p_profile.append(profile.Profile(p[i].g, rmax='280 kpc', ndim=3))

print('plotting rate profiles')

for i in range(len(p_profile)):
    print('plotting z=', z[i])
    rate = np.nanmean(p_profile[i]['vr'].in_units('kpc yr**-1'))*p_profile[i]['mass'].in_units('Msol')/p_profile[i]['rbins'].in_units('kpc')
    plt.plot(p_profile[i]['rbins'], rate,  label = f'{t[i]} Gyr')
    plt.yscale('symlog', linthresh=0.1)

plt.legend()
plt.xlabel(f"r [kpc]")
plt.ylabel(f"rate [Msol yr**-1]")

plt.savefig(out_fn)
