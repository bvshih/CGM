# calculates the rate of mass lost from disk to CGM using radial profile

import pynbody
import pynbody.analysis.profile as profile

import numpy as np

def calculate_rate(p):
    p_profile = profile.Profile(p.g, rmin='0.1 kpc', rmax='300 kpc', ndim=3)

    rate = p_profile['vr'].in_units('kpc s**-1')*p_profile['mass'].in_units('Msol')/p_profile['rbins'].in_units('kpc')

    return np.mean(rate)


fn = '/scratch/08263/tg875625/CGM/GMs/pioneer50h243.1536gst1bwK1BH/pioneer50h243.1536gst1bwK1BH.00'
ts_nums =['3456','3195','3072','2688','2554','2304','1920']
z = ['0.17','0.25','0.29','0.44','0.50','0.62', '0.86']

out_fn = '/scratch/08263/tg875625/CGM/datfiles/mass_rate.dat'

with open(out_fn, 'w') as outfile:
    outfile.write('z1 z2 rate[Msol/s]\n')

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

for i in range(len(ts_nums)-1):
    print(f'tracking dense particles from z = {z[i]}')
    
    # find disk particles 
    p = [h1[i].g[disk]]

    # track to next ts 
    b =  s[i].bridge(s[i+1])
    p.append(b(p[0]))

    # filter out particles still in disk 
    p[1].g[~disk]

    p[1].g['vr'].convert_units('kpc s**-1')
    p[1].g['mass'].convert_units('Msol')

    calculate_rate(p[1])

    with open(out_fn, 'a') as outfile:
        outfile.write(f"{z[i]} {z[i+1]} {calculate_rate(p[1]):.4f}")