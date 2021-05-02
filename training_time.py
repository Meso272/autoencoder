import os

fields=["CLDHGH","FREQSH","aramco","QVAPOR","U","EXAFEL","baryon_density","temperature","dark_matter_density"]

data=["../cesm-multisnapshot-5fields/CLDHGH/CLDHGH_0to49.dat","../cesm-multisnapshot-5fields/FREQSH/FREQSH_0to49.dat","../aramco-snapshot-1520.f32.positive","../Hurricane/clean-data-Jinyang/QVAPORtrain.bin","../Hurricane/clean-data-Jinyang/Utrain.bin","../group_renamed_325.dat.positive","../NYX/baryon_density_logtrain.dat","../NYX/temperature_logtrain.dat","../NYX/dark_matter_density_logtrain.dat"]


for i,field in enumerate(fields):
 
    comm="python Autoencoder_Prototype.py -r %s -n %s -i 5" % (data[i],field+"test")
    os.system(comm)
   

