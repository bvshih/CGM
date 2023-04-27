import metallicity
import coolontime_track

# file path for sim
sim1_fn = '/scratch/08263/tg875625/CGM/GMs/pioneer50h243.1536gst1bwK1BH/pioneer50h243.1536gst1bwK1BH.003456'
z1 = '0.17'
# file path for previous timestep 
sim2_fn = '/scratch/08263/tg875625/CGM/GMs/pioneer50h243.1536gst1bwK1BH/pioneer50h243.1536gst1bwK1BH.003195'
z2 = '0.25'
out_fn = '/scratch/08263/tg875625/CGM/plots/metallicity_z'+z1+'_z'+z2+'_'

sim1_p, sim2_p, sim1_h1, sim2_h1, sim1, sim2 = metallicity.get_particles(sim1_fn, sim2_fn, return_halos=True, return_sim=True)
# coolontime_track.make_scatter(sim1_p, sim2_p,'metals', out_fn, z1,z2)

# coolontime_track.vel_profile(sim1_p, sim2_p, out_fn, z1,z2)


out_fn = '/scratch/08263/tg875625/CGM/plots/vr_metallicity_z'+z1+'_z'+z2+'_'

coolontime_track.make_scatter(sim1_p, sim2_p, 'vr', out_fn, z1, z2)