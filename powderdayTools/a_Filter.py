import h5py
import sys
import glob
import numpy as np
import tqdm
import os
cwd = os.getcwd()
# print(cwd)
os.chdir("/home/esavitch/caesar")
# os.chdir('/blue/narayanan/esavitch/caesar/caesar')
# print(os.getcwd())
import caesar
###########
# Line arguments
###########
snap_num = sys.argv[1]
galNums = int(sys.argv[2])
output = sys.argv[3]
############
#galNums = [14,15,18]
#galNums = list(range(101)) 
#galNums = 'all'
#snap_num = 305
snapshot_path = f'/orange/narayanan/desika.narayanan/gizmo_runs/simba/m25n512/output/snapshot_{str(snap_num).zfill(3)}.hdf5'
#snapshot_path = '/orange/narayanan/desika.narayanan/gizmo_runs/simba/m25n512/output/snapshot_'
# output_path = f'/home/esavitch/orange/2024/Summer2024/powderPuff/snap{str(snap_num).zfill(3)}/'
output_path = output+f'snap{str(snap_num).zfill(3)}/'
caesar_file = f'/home/esavitch/orange/caesarFiles/caesar_{str(snap_num).zfill(3)}.hdf5'
#see if the output path exists, and if not, make it
if not os.path.exists(output_path):
    os.makedirs(output_path)
    print("creating output directory: "+output_path)
obj = caesar.load(caesar_file)
snap_str = str(snap_num).zfill(3)
# input_file = h5py.File(snapshot_path+str(snap_str)+'.hdf5', 'r')
input_file = h5py.File(snapshot_path, 'r')
galcount = len(obj.galaxies)
if(galNums=='all'): galNums=range(galcount)
for galaxy in [galNums]:
    print("GALAXY NUM:",str(galaxy))
    print()
    glist = obj.galaxies[int(galaxy)].glist
    slist = obj.galaxies[int(galaxy)].slist
    with h5py.File(output_path+'galaxy_'+str(galaxy)+'.hdf5', 'w') as output_file:
        output_file.copy(input_file['Header'], 'Header')
        print('starting with gas attributes now')
        output_file.create_group('PartType0')
        for k in tqdm.tqdm(input_file['PartType0']):
            output_file['PartType0'][k] = input_file['PartType0'][k][:][glist]
        print('moving to star attributes now')
        output_file.create_group('PartType4')
        for k in tqdm.tqdm(input_file['PartType4']):
            output_file['PartType4'][k] = input_file['PartType4'][k][:][slist]
    print('done copying attributes, going to edit header now')
    outfile_reload = output_path+'galaxy_'+str(galaxy)+'.hdf5'
    re_out = h5py.File(outfile_reload,'r+')
    re_out['Header'].attrs.modify('NumPart_ThisFile', np.array([len(glist), 0, 0, 0, len(slist), 0]))
    re_out['Header'].attrs.modify('NumPart_Total', np.array([len(glist), 0, 0, 0, len(slist), 0]))
    re_out.close()