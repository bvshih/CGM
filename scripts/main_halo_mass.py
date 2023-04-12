import pynbody

out_fn = '/scratch/08263/tg875625/CGM/datfiles/P0_disk_mass_table_z0.17.dat'

sim_fn = '/scratch/08263/tg875625/CGM/GMs/pioneer50h243.1536gst1bwK1BH/pioneer50h243.1536gst1bwK1BH.003456'

with open(out_fn, 'w') as outfile:
    outfile.write('method halo_num Rvir[kpc] Mvir[Msol] Mgas[Msol] Mstar[Msol] Mcgmgas[Msol] Mcgmgas/Mgas\n')

sim_name = 'P0'

s = pynbody.load(sim_fn)
s.physical_units()
h = s.halos()

h1 = h[1] # doesnt include all of s 

properties = {}

# center and align h1
pynbody.analysis.halo.center(h1,mode='hyb')
pynbody.analysis.angmom.sideon(h1, cen=(0,0,0))

# calculate rvir using pynbody
rvir = pynbody.analysis.halo.virial_radius(h1) # in kpc

properties['Mvir'] = h1['mass'].sum()
properties['Mgas'] = h1.g['mass'].sum()
properties['Mstar'] = h1.s['mass'].sum()

# create filters to remove inner disk 
rdisk = "10 kpc"
height = "10 kpc"
disk = pynbody.filt.Disc(rdisk, height, cen=(0,0,0))  # im pretty sure height means total height of the disk  

# filter current halo to remove disk
halo_cgm = h1[~disk] 

# cool gas mass
properties['Mcgmgas']= halo_cgm.g['mass'].sum()

with open(out_fn, 'a') as outfile:
            outfile.write(f"pynbody {h1.properties['halo_id']} {rvir:.1f} {properties['Mvir']:.2e} {properties['Mgas']:.2e} {properties['Mstar']:.2e} {properties['Mcgmgas']:.2e} {properties['Mcgmgas']/properties['Mgas']:.4f}\n")

