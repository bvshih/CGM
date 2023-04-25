import metallicity
import coolontime_track

# file path for sim
sim1_fn = '/scratch/08263/tg875625/CGM/GMs/pioneer50h243.1536gst1bwK1BH/pioneer50h243.1536gst1bwK1BH.003195'
z1 = '0.25'
# file path for previous timestep 
sim2_fn = '/scratch/08263/tg875625/CGM/GMs/pioneer50h243.1536gst1bwK1BH/pioneer50h243.1536gst1bwK1BH.003072'
z2 = '0.29'
out_fn = '/scratch/08263/tg875625/CGM/plots/metallicity_'+z1+'_'+z2+'_'

sim1_p, sim2_p, sim1_h1, sim2_h1, sim1, sim2 = metallicity.get_particles(sim1_fn, sim2_fn, return_halos=True, return_sim=True)
coolontime_track.make_scatter(sim1_p, sim2_p,'metals', out_fn, z1,z2)

coolontime_track.vel_profile(sim1_p, sim2_p, out_fn, z1,z2)