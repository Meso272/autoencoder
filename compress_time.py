import os

fields=["CLDHGH","FREQSH","aramco","QVAPOR","U","EXAFEL","baryon_density","temperature","dark_matter_density"]

data=["../cesm-multisnapshot-5fields/CLDHGH/CLDHGH_55.dat.positive","../cesm-multisnapshot-5fields/FREQSH/FREQSH_55.dat","../aramco-snapshot-1520.f32.positive","../Hurricane/clean-data-Jinyang/QVAPORf45.bin.positive","../Hurricane/clean-data-Jinyang/Uf45.bin.positive","../group_renamed_325.dat.positive","../NYX/512x512x512/baryon_density.dat.log10.positive","../NYX/512x512x512/temperature.dat.log10.positive","../NYX/512x512x512/dark_matter_density.dat.log10.positive"]
ebs=[1e-2,1e-3]

for i,field in enumerate(fields):
    for eb in ebs:
        comm="python Autoencoder_Prototype.py -c %s -n %s -e %f" % (data[i],field,eb)
        os.system(comm)
        comm="python Autoencoder_Prototype.py -d %s.z -n %s " % (data[i],field)


