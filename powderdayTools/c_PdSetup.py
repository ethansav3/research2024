#purpose: to set up slurm files and model *.py files from the
#positions written by caesar_cosmology_npzgen.py for a cosmological
#simulation.  This is written for the University of Florida's
#HiPerGator2 cluster.
import numpy as np
from subprocess import call
import sys
import os
cwd = os.getcwd()
os.chdir("/home/esavitch/caesar")
print(os.getcwd())
import caesar
import glob
os.chdir(cwd)
nnodes=1
#################
# Edit these !!!
snap_num = sys.argv[1]
output = sys.argv[2]
#################
obj = caesar.load(f'/home/esavitch/orange/caesarFiles/caesar_{str(snap_num).zfill(3)}.hdf5')
snap_redshift = obj.simulation.redshift
print(f"Redshift: z = {snap_redshift:.5f}")
#galNums = [14,15,18]
snap_dir = output+f'/snap{snap_num}/'
infiles = sorted(glob.glob(snap_dir+'/galaxy_*.hdf5')) 
#galNums = list(range(101))
#if(galNums=='all'): galNums=range(galcount)
#snap_redshift = 4.440892098500626e-16
#snap_num = 305
npzfile = output+f"/snap{snap_num}/gal_positions.npz"
model_dir_base = output
#hydro_dir = output+f"snap{snap_num}/"
hydro_dir = output
#hydro_dir = f"/orange/narayanan/esavitch/2024/Summer2024/powderPuff/"
#npzfile = '/orange/narayanan/s.lower/TNG/position_npzs/tng_snap33_pos.npz' 
#model_dir_base = '/orange/narayanan/s.lower/TNG/pd_runs/'
#hydro_dir = '/orange/narayanan/s.lower/TNG/filtered_snapshots/'
hydro_dir_remote = hydro_dir
model_run_name='simba_m25n512'
#################
COSMOFLAG=0 #flag for setting if the gadget snapshots are broken up into multiples or not and follow a nomenclature snapshot_000.0.hdf5
FILTERFLAG = 1 #flag for setting if the gadget snapshots are filtered or not, and follow a nomenclature snap305_galaxy1800_filtered.hdf5
SPHGR_COORDINATE_REWRITE = True
#===============================================
if (COSMOFLAG == 1) and (FILTERFLAG == 1):
    raise ValueError("COSMOFLAG AND FILTER FLAG CAN'T BOTH BE SET")
data = np.load(npzfile,allow_pickle=True)
pos = data['pos'][()] #positions dictionary
#ngalaxies is the dict that says how many galaxies each snapshot has, in case it's less than NGALAXIES_MAX
ngalaxies = data['ngalaxies'][()]
for snap in [snap_num]:
    print(snap)
    #model_dir = model_dir_base+'/snap{:03d}'.format(snap)
    model_dir = model_dir_base+f'/snap{snap_num}'
    #model_dir = model_dir_base+'/snap231_new'
    print(model_dir)
    model_dir_remote = model_dir
    tcmb = 2.73*(1.+snap_redshift)
    NGALAXIES = ngalaxies['snap'+str(snap)]
    print(NGALAXIES)
    #for nh in range(NGALAXIES):
    #for nh in galNums:
    for f in infiles:
        nh = int(f.split('_')[1].split('.')[0])
        # print(pos['galaxy'+str(nh)]['snap'+str(snap)][0])
        try:
            xpos = pos['galaxy'+str(nh)]['snap'+str(snap)][0]
        except: continue
        ypos = pos['galaxy'+str(nh)]['snap'+str(snap)][1]
        zpos = pos['galaxy'+str(nh)]['snap'+str(snap)][2]
        cmd = output+"/cosmology_setup_all_cluster.hipergator.sh "+str(nnodes)+' '+model_dir+' '+hydro_dir+' '+model_run_name+' '+str(COSMOFLAG)+' '+str(FILTERFLAG)+' '+model_dir_remote+' '+hydro_dir_remote+' '+str(xpos)+' '+str(ypos)+' '+str(zpos)+' '+str(nh)+' '+str(snap)+' '+str(tcmb)
        #cmd = "./cosmology_setup_all_cluster.hipergator.sh "+str(nnodes)+' '+model_dir+' '+hydro_dir+' '+model_run_name+' '+str(COSMOFLAG)+' '+str(FILTERFLAG)+' '+model_dir_remote+' '+hydro_dir_remote+' '+str(xpos)+' '+str(ypos)+' '+str(zpos)+' '+str(nh)+' '+str(snap)+' '+str(tcmb)
        call(cmd,shell=True)
        print(cmd)