import pynbody
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import SeabornFig2Grid as sfg
import matplotlib.gridspec as gridspec

def phase_2dhist(p, outfn, z1, z2, t1, t2, phasex='rho', phasey='temp'):
    fig, ax = plt.subplots(ncols=2,sharex=True, sharey=True, figsize=(20,12))
    plt.subplots_adjust(bottom=0.2)

    title = [f'All particles in disk\n z = {z1} t = {t1}', f'Particles no longer in disk\n z = {z2} t = {t2}']
    
    xbins = np.logspace(np.log10(1e3),np.log10(1e9), 50)
    ybins = np.logspace(np.log10(1e3),np.log10(1e8), 50)

    colorbar_pos = [[0.1, 0.1, 0.35, 0.05], [0.55, 0.1, 0.35, 0.05]]

    for i in range(len(p)):
        ax[i].loglog()  
        img = ax[i].hist2d(p[i].g[phasex], p[i].g[phasey], bins = [xbins,ybins])
        ax[i].set_title(title[i])

        ax[i].set_xlabel(f"{phasex} [{p[i].g[phasex].units}]")
        ax[i].set_ylabel(f"{phasey} [{p[i].g[phasey].units}]")

        cax = plt.axes(colorbar_pos[i])

        plt.colorbar(img[3], cax=cax, orientation='horizontal')

    plt.savefig(outfn)
def phase_diagram(p, outfn, z1, z2,t1, t2, phasex='rho', phasey='temp'):
    fig, ax = plt.subplots(ncols=2,sharex=True, sharey=True, figsize=(20,10))

    title = [f'All particles in disk\n z = {z1} t = {t1}', f'Particles no longer in disk\n z = {z2} t = {t2}']
    vmin = min(p[0].g['r'].in_units('kpc').min(), p[1].g['r'].in_units('kpc').min())
    vmax = max(p[0].g['r'].in_units('kpc').max(), p[1].g['r'].in_units('kpc').max()) 
    for i in range(len(p)):
        ax[i].loglog()  
        img = ax[i].scatter(p[i].g[phasex], p[i].g[phasey], c=p[i].g['r'].in_units('kpc'), vmin =vmin, vmax=vmax, alpha=0.5)
        ax[i].set_title(title[i])

        ax[i].set_xlabel(f"{phasex} [{p[i].g[phasex].units}]")
        ax[i].set_ylabel(f"{phasey} [{p[i].g[phasey].units}]")
    
    plt.subplots_adjust(right=0.8)
    cax = plt.axes([0.85, 0.2, 0.01, 0.6])

    plt.colorbar(img, cax=cax, label = 'r [kpc]')

    plt.savefig(outfn)

def sns_phase_diagram(p, z,t, phasex='rho', phasey='temp'):
    log_phasex = np.log10(p.g[phasex])
    log_phasey = np.log10(p.g[phasey])
    g = sns.jointplot(x = log_phasex, y =log_phasey, hue= p.g['r'].in_units('kpc'), joint_kws=dict(alpha=0.75))
    # g = sns.jointplot(x = p.g[phasex], y =p.g[phasey],hue = p.g['r'] , joint_kws=dict(alpha=0.75))
    
    # ax = g.ax_joint
    # ax.set_xscale('log')
    # ax.set_yscale('log')

    return g 
plot_phase_diagram = False
plot_sns_diagram = False
plot_2dhist = True

fn = '/scratch/08263/tg875625/CGM/GMs/pioneer50h243.1536gst1bwK1BH/pioneer50h243.1536gst1bwK1BH.00'

out_fn = '/scratch/08263/tg875625/CGM/plots/'

ts_nums =['3456','3195','3072','2688','2554','2304','1920']
z = ['0.17','0.25','0.29','0.44','0.50','0.62', '0.86']

# ts_nums =['2304','1920']
# z = ['0.62', '0.86']

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

if plot_sns_diagram:
    p = []
for i in range(len(ts_nums)-1):
    print(f'tracking dense particles from z = {z[i]}')
    
    # find disk particles 
    p_i = [h1[i].g[disk]]

    # track to next ts 
    b =  s[i].bridge(s[i+1])
    p_i.append(b(p_i[0]))

    # filter out particles still in disk 
    p_i[1].g[~disk]

    if plot_phase_diagram:
        phase_diagram(p_i ,out_fn+'z'+z[i]+'_z'+z[i+1]+'_phase_plot_r.pdf', z[i], z[i+1],t[i], t[i+1])
    if plot_2dhist:
        phase_2dhist(p_i, out_fn+'z'+z[i]+'_z'+z[i+1]+'_phase_2dhist_50.pdf',z[i], z[i+1],t[i], t[i+1]) 
    if plot_sns_diagram:
        p.append(p_i)

if plot_sns_diagram:
    fig = plt.figure(figsize=(2*6, len(p)*6))
    gs = gridspec.GridSpec(len(p), 2)
    
    g = []
    for i in range(len(p)):
        for j in range(len(p[i])):
            g.append(sns_phase_diagram(p[i][j], z[i], t[i]))

    for k in range(len(g)):
        mg = sfg.SeabornFig2Grid(g[k], fig, gs[k])

    gs.tight_layout(fig, rect=[0, 0, 0.7, 0.7])

    plt.savefig(out_fn+'all_z_sns_phase.pdf')