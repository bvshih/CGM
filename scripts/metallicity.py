import cgm
import pynbody

def select_metallicity(sim):

    metal_sol = 0.0134
    metalliticty_filt = pynbody.filt.HighPass('metals', metal_sol)
    selected_gas = sim.g[metalliticty_filt]

    return selected_gas

def get_particles(sim1_fn, sim2_fn, return_halos=True, return_sim=True):
    '''
    sim2 is the previous timestep of sim1
    returns the particles in sim1 and sim2
    '''

    # get cgm of sim 1
    sim1_cgm, sim1, sim1_h1 = cgm.isolate_cgm(sim1_fn, True)

    # load sim2
    sim2 = pynbody.load(sim2_fn)
    sim2.physical_units()
    sim2_h1 = sim2.halos()[1]

    print('simulation 2 loaded')
   
    pynbody.analysis.halo.center(sim2_h1, mode='hyb')
    pynbody.analysis.angmom.faceon(sim2_h1, cen=(0,0,0))
    print('simulation 2 centered and aligned')
    
    # bridge sim2 and sim1
    b = sim2.bridge(sim1_cgm)
    print('created bridge')

    # metallicity cut
    sim1_p = select_metallicity(sim1_cgm)

    # find progenitors of selected particles
    sim2_p = b(sim1_p)
    
    print('tracked particles')

    results = [sim1_p, sim2_p]
    if return_halos:
        results.append(sim1_h1)
        results.append(sim2_h1)
    if return_sim:
        results.append(sim1)
        results.append(sim2)

    return (*results,)