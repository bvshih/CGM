import pynbody
import pandas as pd 

out_fn = '/scratch/08263/tg875625/CGM/datfiles/P0_mass_table_z0.17.dat'

sim_fn = '/scratch/08263/tg875625/CGM/GMs/pioneer50h243.1536gst1bwK1BH/pioneer50h243.1536gst1bwK1BH.003456'

amiga_fn = '/scratch/08263/tg875625/CGM/GMs/pioneer50h243.1536gst1bwK1BH/pioneer50h243.1536gst1bwK1BH.003456.amiga.stat'

with open(out_fn, 'w') as outfile:
    outfile.write('method halo_num Rvir[kpc] Mvir[Msol] Mgas[Msol] Mstar[Msol] Mcgmgas[Msol] Mcgmgas/Mgas\n')

sim_name = 'P0'

s = pynbody.load(sim_fn)
s.physical_units()
h = s.halos()

h1 = h[1] # doesnt include all of s 

properties = {}

# using pynbody's rvir 
pynbody.analysis.halo.center(h1,mode='hyb')
rvir = pynbody.analysis.halo.virial_radius(h1) # in kpc

properties['Mvir'] = h1['mass'].sum()
properties['Mgas'] = h1.g['mass'].sum()
properties['Mstar'] = h1.s['mass'].sum()

# create filters to remove inner sphere 
rdisk = "10 kpc"
cgm_filt = pynbody.filt.Sphere(rdisk, cen=(0,0,0))  # this assumes... the disk is a sphere? sure why not... 

# filter current halo to remove sphere
halo_cgm = h1[~cgm_filt] 

# cool gas mass
properties['Mcgmgas']= halo_cgm.g['mass'].sum()

with open(out_fn, 'a') as outfile:
            outfile.write(f"pynbody {h1.properties['halo_id']} {rvir:.1f} {properties['Mvir']:.2e} {properties['Mgas']:.2e} {properties['Mstar']:.2e} {properties['Mcgmgas']:.2e} {properties['Mcgmgas']/properties['Mgas']:.4f}\n")

# calculate same properties but using amiga.stat file 

amiga_df = pd.read_csv(amiga_fn, sep='\s+')
rvir = str(amiga_df['Rvir(kpc)'][0])+' kpc'
cgm_filt = pynbody.filt.Annulus(rdisk, rvir, cen=(0,0,0))

# filter simulation to only include annulus
halo_cgm = s[cgm_filt] 

amiga_cgm_gas = halo_cgm.g['mass'].sum()

with open(out_fn, 'a') as outfile:
            outfile.write(f"amiga.stat {amiga_df['Grp'][0]} {amiga_df['Rvir(kpc)'][0]:.1f} {amiga_df['Mvir(M_sol)'][0]:.2e} {amiga_df['GasMass(M_sol)'][0]:.2e} {amiga_df['StarMass(M_sol)'][0]:.2e} {amiga_cgm_gas:.2e} {amiga_cgm_gas/amiga_df['GasMass(M_sol)'][0]:.4f}\n")


