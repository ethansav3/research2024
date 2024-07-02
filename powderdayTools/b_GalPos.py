import h5py
import numpy as np
import sys, os
import numpy as np
import glob
import tqdm

##############
# Line arguments
###############
snap = sys.argv[1]
output = sys.argv[2]
###############
#snap = 305
snap_dir = output+f'snap{snap}/'
outfile = output+f'snap{snap}/gal_positions.npz'
#snap_dir = '/orange/narayanan/[...]' #where are the filtered galaxies?
#outfile = '/orange/narayanan/[...]'+'_gal_positions.npz' #where do you want the output to go?
################
pos = {}
ngalaxies = {}
infiles = sorted(glob.glob(snap_dir+'/galaxy_*.hdf5')) 
count = 0
#galNums = [14,15,18]
#galNums = list(range(101))
#if(galNums=='all'): galNums=range(galcount)
#for i in tqdm.tqdm(range(len(infiles))):
#for i in galNums:
for f in infiles:
    i = count
    try:
        #infile = h5py.File(snap_dir+'/galaxy_'+str(i)+'.hdf5', 'r')
        infile = h5py.File(f, 'r')
        i = int(f.split('_')[1].split('.')[0])
    except:
        print('ERROR ',str(i), f)
        continue
    count+=1
    pos['galaxy'+str(i)] = {}
    gas_masses = infile['PartType0']['Masses']
    gas_coords = infile['PartType0']['Coordinates']
    star_masses = infile['PartType4']['Masses']
    star_coords = infile['PartType4']['Coordinates']
    total_mass = np.sum(gas_masses) + np.sum(star_masses)
    x_pos = (np.sum(gas_masses * gas_coords[:,0]) + np.sum(star_masses * star_coords[:,0])) / total_mass
    y_pos = (np.sum(gas_masses * gas_coords[:,1]) + np.sum(star_masses * star_coords[:,1])) / total_mass
    z_pos = (np.sum(gas_masses * gas_coords[:,2]) + np.sum(star_masses * star_coords[:,2])) / total_mass
    pos['galaxy'+str(i)]['snap'+str(snap)] = np.array([x_pos, y_pos, z_pos])
    infile.close()
ngalaxies['snap'+str(snap)] = count
print("SAVING")
np.savez(outfile, ngalaxies=ngalaxies, pos=pos)