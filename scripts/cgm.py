import pynbody

def isolate_cgm(sim_fn):
    s = pynbody.load(sim_fn)
    s.physical_units()
    h = s.halos()

    h1 = h[1] 

    print('simulation loaded')

    # center and align h1
    pynbody.analysis.halo.center(h1,mode='hyb')
    pynbody.analysis.angmom.faceon(h1, cen=(0,0,0))

    print('centered and aligned')

    # create filters to remove inner disk 
    rdisk = "15 kpc"
    height = "5 kpc"
    disk = pynbody.filt.Disc(rdisk, height, cen=(0,0,0))  # im pretty sure height means total height of the disk  

    # filter current halo to remove disk
    halo_cgm = h1[~disk] 

    print('removed disc of radius', rdisk, 'and height', height)
    return halo_cgm