import pandas as pd
import pynbody 

def remove_col_nums(columns):
    '''removes all nonalpha characters from list of strings'''
    column_names = {}
    for col in columns:
        new_col = ''.join([i for i in col if i.isalpha()])
        column_names[col] = new_col
    return column_names


out_fn = '/scratch/08263/tg875625/CGM/datfiles/P0_mass_table.dat'

with open(out_fn, 'w') as outfile:
    outfile.write('halo_num Mvir Mgas Mstar Mcoolgas Mcoolgas/Mgas\n')

sim_name = 'P0'
sim_path = '/scratch/08263/tg875625/CGM/GMs/pioneer50h243.1536gst1bwK1BH/pioneer50h243.1536gst1bwK1BH.004096'
s = pynbody.load(sim_path)
s.physical_units()
h = s.halos()

hubble_const = s.properties['h']

halos_fn = '/scratch/08263/tg875625/CGM/GMs/pioneer50h243.1536gst1bwK1BH/pioneer50h243.1536gst1bwK1BH.004096.z0.000.AHF_halos'
halos_df = pd.read_csv(halos_fn,sep='\s+')

# remove nonalpha characters from column names
halos_df = halos_df.rename(columns=remove_col_nums(halos_df.columns))


for idx,halo in enumerate(h):
    properties = {}

    # # get some properties from AHF halos 
    # for property_name in ['ID','Mvir', 'Rvir','Mgas','Mstar']:
    #     properties[property_name] = halos_df[property_name][idx]
    
    rvir = halos_df['Rvir'][idx]
    center = (halos_df['Xc'][idx], halos_df['Yc'][idx], halos_df['Zc'][idx])

    # rvir filter
    rvir_filt = pynbody.filt.Sphere(rvir, cen=center)
    halo = s[rvir_filt]

    properties['Mvir'] = halo['mass'].sum()
    properties['Mgas'] = halo.g['mass'].sum()
    properties['Mstar'] = halo.s['mass'].sum()

    # create filters to isolate CGM particles
    rdisk = 10
    cgm_filt = pynbody.filt.Annulus(rdisk, rvir, cen=center)  # this assumes... the disk is a sphere? sure why not...

    # filter current halo
    halo_cgm = s[cgm_filt] 

    print('filtered halo', idx)

    # cool gas mass
    properties['Mcoolgas']= halo_cgm['mass'].sum()

    with open(out_fn, 'a') as outfile:
                outfile.write(f"{idx} {properties['Mvir']:.2e} {properties['Mgas']:.2e} {properties['Mstar']:.2e} {properties['Mcoolgas']:.2e} {properties['Mcoolgas']/properties['Mgas']:.4f}\n")

