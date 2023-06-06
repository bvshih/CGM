import pynbody
import os
import numpy as np

def get_iord(line):
    line = line.split()
    return str(line[3])
def parse_last_line(line):
    line = line.split()
    return str(line[0]), line[4]

fn = '/scratch/08263/tg875625/CGM/GMs/pioneer50h243.1536gst1bwK1BH/pioneer50h243.1536gst1bwK1BH.00'

ts_nums =['3456','3195','3072','2688','2554','2304','1920']
z = ['0.17','0.25','0.29','0.44','0.50','0.62', '0.86']

ts_nums.reverse()
z.reverse()

outfn = '/scratch/08263/tg875625/CGM/datfiles/gas_data.dat'
iords = []
if os.path.exists(outfn):
    with open(outfn) as outfile:
        for line in outfile:
            iords.append(get_iord(line))
        last_line = line
    last_z, last_loc = parse_last_line(last_line)

    print('outfile already exists')
    print(f'last z: {last_z}\n last loc: {last_loc}')

else:
    with open(outfn, 'a') as outfile:	
        outfile.write('z t output iord location r[kpc] vr[km s**-1] rho[Msol kpc**-3] mass[Msol] T[K] coolontime[Gyr] metallicity\n')
    print('outfile does not exist, writing new file')
try:
    last_index = z.index(last_z)
    z = z[last_index:]
    ts_nums = ts_nums[last_index:]
except:
    pass


t = []

s = []
h1 = []

# create filters for disk 
rdisk = "15 kpc"
height = "5 kpc" # height is from midplane
disk = pynbody.filt.Disc(rdisk, height, cen=(0,0,0))  

for j in range(len(ts_nums)): 
    s.append(pynbody.load(fn+ts_nums[j]))
    t.append(round(s[j].properties['time'].in_units('Gyr'),2))
    print('t: ', t[j])
    print(f'z = {z[j]} loaded')
    s[j].physical_units()
    h1.append(s[j].halos()[1])

    pynbody.analysis.angmom.faceon(h1[j])
    print('centered and rotated')

    # find disk particles 
    p_disk = h1[j].g[disk]
    p_cgm = h1[j].g[~disk]
    
    if last_z == z[j]:
        if last_loc == 'disk':
            iord_index_disk, = np.where(p_disk.g['iord'] ==  last_loc)
            iord_index_cgm = 0
        else:
            iord_index_disk = 'oops' 
            iord_index_cgm, = np.where(p_cgm.g['iord'] ==  last_loc)

    else:
        iord_index_disk = 0
        iord_index_cgm = 0
    
    try:
        print("writing data for", len(p_disk.g)-iord_index_disk,"disk particles")
        for i in range(iord_index_disk,len(p_disk.g)):
            with open(outfn, 'a') as outfile: 
                outfile.write(f"{z[j]} {t[j]} {ts_nums[j]} {p_disk.g['iord'][i]} disk "
                            f"{p_disk.g['r'].in_units('kpc')[i]:.2f} {p_disk.g['vr'].in_units('km s**-1')[i]:.2f} "
                            f"{p_disk.g['rho'].in_units('Msol kpc**-3')[i]:.2f} {p_disk.g['mass'].in_units('Msol')[i]:.2f} "
                            f"{p_disk.g['temp'].in_units('K')[i]:.2f} {p_disk.g['coolontime'].in_units('Gyr')[i]:.2f} "
                            f"{p_disk.g['metals'][i]:.5f}\n")
                
        if i%1000 == 0:
             print(f"finished {i} particles")
    except:
        print('all disk particle data written for this output')
    
    print("writing data for",len(p_cgm.g)-iord_index_cgm,"cgm particles")
    for i in range(iord_index_cgm, len(p_cgm.g)):
        with open(outfn, 'a') as outfile: 
            outfile.write(f"{z[j]} {t[j]} {ts_nums[j]} {p_cgm['iord'][i]} cgm "
                          f"{p_cgm['r'].in_units('kpc')[i]:.2f} {p_cgm.g['vr'].in_units('km s**-1')[i]:.2f} "
                          f"{p_cgm['rho'].in_units('Msol kpc**-3')[i]:.2f} {p_cgm['mass'].in_units('Msol')[i]:.2f} "
                          f"{p_cgm['temp'].in_units('K')[i]:.2f} {p_cgm['coolontime'].in_units('Gyr')[i]:.2f} "
                          f"{p_cgm['metals'][i]:.5f}\n")
        if i%1000 == 0:
             print(f"finished {i} particles")
    

