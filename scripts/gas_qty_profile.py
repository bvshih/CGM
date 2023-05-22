# makes radial profile of given quantity 
# tracks high density gas particles (above 0.1 amu cm**-3)

import pynbody

import matplotlib.pyplot as plt
import pynbody.units as units
import pynbody.analysis.profile as profile

def qty_profile(p, z, t, qty, out_fn):
    fig, ax = plt.subplots()

    for i in range(len(p)):
        p_profile = profile.Profile(p[i].g, rmin='0.1 kpc', rmax='280 kpc', ndim=3)

        ax.plot(p_profile['rbins'], p_profile[qty], label=str(t[i])+' Gyr')

    ax.semilogy()
    ax.set_xlabel('r [kpc]')
    ax.set_ylabel(f'{qty} [{p[0].g[qty].units}]')

    ax.legend()

    out_fn= out_fn+'z'+z[0]+'_z'+z[-1]+'_'+qty+'_profile_logy.pdf'

    plt.savefig(out_fn)
    print('profile saved as', out_fn)

    return p_profile

def profile_plot(profiles, z, t, qty, out_fn):
    fig, ax = plt.subplots()

    for i in range(len(profiles)):
        ax.plot(profiles[i]['rbins'], profiles[i][qty], label = str(t[i])+' Gyr')

    ax.semilogy()
    ax.set_xlabel('r [kpc]')
    ax.set_ylabel(f'{qty} [{profiles[0][qty].units}]')

    ax.legend()

    out_fn = out_fn+'z'+z[0]+'_z'+z[-1]+'_'+qty+'_profile_all_logy.pdf'
    plt.savefig(out_fn)
    print('profile plot saved as', out_fn)


fn = '/scratch/08263/tg875625/CGM/GMs/pioneer50h243.1536gst1bwK1BH/pioneer50h243.1536gst1bwK1BH.00'
ts_nums =['3456','3195','3072','2688','2554','2304','1920']
z = ['0.17','0.25','0.29','0.44','0.50','0.62', '0.86']

out_fn = '/scratch/08263/tg875625/CGM/plots/tracking_disk_'

ts_nums.reverse()
z.reverse()

t = []

s = []
h1 = []

amu = units.NamedUnit("amu", 1.66e-27*units.kg)

for j in range(len(ts_nums)): 
    s.append(pynbody.load(fn+ts_nums[j]))
    t.append(round(s[j].properties['time'].in_units('Gyr'),2))
    print('t: ', t[j])
    print(f'z = {z[j]} loaded')
    s[j].physical_units()
    h1.append(s[j].halos()[1])

    pynbody.analysis.angmom.faceon(h1[j])
    print('centered and rotated')
    s[j].g['rho'].convert_units('amu cm**-3')  # convert density array to new units

zf_profile=[]

rho_filt = pynbody.filt.HighPass('rho', '0.1 amu cm**-3')

for i in range(len(ts_nums)):
    b = []
    print(f'i: {i}')
    print(f'tracking dense particles from z = {z[i]}')
    p = [h1[i].g[rho_filt]]
    print(p)

    for j in range(i+1,len(ts_nums)):
        print(f'i: {i} j: {j}')
        b.append(s[i].bridge(s[j]))
        print(f'len(b): {len(b)} ')
        assert j-i-1 == len(b)-1, 'fuck'

        p.append(b[j-i-1](p[0]))
        print(f'found particles from z = {z[i]} in z = {z[j]}')
    print('making qty profile')
    profile_temp = qty_profile(p, z[i:], t[i:], 'mass', out_fn)
    zf_profile.append(profile_temp)

profile_plot(zf_profile, z, t, 'mass', out_fn)