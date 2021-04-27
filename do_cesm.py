import os
import sys
import numpy as np
field=sys.argv[1]
epoch=int(sys.argv[2])
output=sys.argv[3]
datafolder="/home/jliu447/lossycompression/cesm-multisnapshot-5fields/%s" % field
trainfile="/home/jliu447/lossycompression/cesm-multisnapshot-5fields/%s/%s_0to49.dat" % (field,field)

os.system("python3 Autoencoder_Prototype.py -r %s -i %d" % (trainfile,epoch))
print("Train Over.")

#ebs=[i*1e-4 for i in range(1,10,2)]+[i*1e-3 for i in range(1,10,2)]+[i*1e-2 for i in range(1,10,2)]+[0.1]
ebs=[1e-2,1e-3]
idxrange=[x for x in range(52,63)]

pid=str(os.getpid()).strip()
data=np.zeros((len(ebs)+1,12,9),dtype=np.float32)
for i in range(9):
    data[1:,0,i]=ebs
    data[0,1:,i]=idxrange

for i in range(52,63):
    filename="%s_%d.dat" % (field,i)
    filepath=os.path.join(datafolder,filename)
    a=np.fromfile(filepath,dtype=np.float32)
    a=a-np.min(a)
    filepath=filepath+".positive"
    a.tofile(filepath)
    for j,eb in enumerate(ebs): 
        os.system("python3 Autoencoder_Prototype.py -c %s -e %f" % (filepath,eb))
        zpath=filepath+".z"
        dpath=zpath+".d"
        dvname=filepath.split("/")[-1]+".dvalue"
        dvpath=filepath+".dvalue"

        os.system("du -s %s*&>%s.txt" % (filepath,pid))
        origsize=0
        compressedsize=0
        with open ("%s.txt"%pid,"r") as f:
            lines=f.read().splitlines()
            for line in lines:
                size,path=lines.split("\t")
                size=float(size)
                if path==filepath:
                    origsize=size
                if path==zpath or path==dvpath or path==filepath+".dindex" or path==filepath+".min" or path==filepath+".mod" or path==filepath+".str":
                    compressedsize+=size
        cr1=origsize/compressedsize
        os.system("rm -f %s.txt" % pid)   

        os.system("python3 Autoencoder_Prototype.py -d %s" % zpath)
        os.system("compareData -f %s %s>%s.txt" % (filepath,dpath,pid))
        with open ("%s.txt"%pid,"r") as f:
            lines=f.read().splitlines()
            psnr1=eval(lines[6].split(',')[0].split('=')[1])
            maxrerr1=eval(lines[4].split('=')[1])
        data[j+1][i-51][0]=cr1
        data[j+1][i-51][1]=psnr2
        data[j+1][i-51][2]=maxrerr1
        os.system("rm -f %s.txt" % pid)    
 
        os.system("sz_demo %s -1 %d %f %d 0 1 " % (dvpath,dlength,0.1,dlength))
        os.system("mv %s.sz3 %s.sz3;mv %s.sz3.out %s.sz3.out" % (dvname,dvpath,dvname,dvpath))
        #os.system("sz_demo %s -1 %d %f %d 0 1 " % (dvname,dlength,sze,dlength))
        os.system("du -s %s*&>%s.txt" % (filepath,pid))
        origsize=0
        compressedsize=0
        dvname=filepath.split("/")[-1]+".dvalue"
        dvpath=filepath+".dvalue"
        with open ("%s.txt"%pid,"r") as f:
            lines=f.read().splitlines()
            for line in lines:
                size,path=line.split("\t")
                size=float(size)
                if path==filepath:
                    origsize=size
                if path==zpath or path==dvpath+".sz3" or path==filepath+".dindex" or path==filepath+".min" or path==filepath+".mod" or path==filepath+".str":
                    compressedsize+=size
        cr2=origsize/compressedsize
        os.system("rm -f %s.txt" % pid)


        os.system("python3 Autoencoder_Prototype.py -d %s -z 1" % zpath)
        os.system("compareData -f %s %s>%s.txt" % (filepath,dpath,pid))
        with open ("%s.txt"%pid,"r") as f:
            lines=f.read().splitlines()
            psnr2=eval(lines[6].split(',')[0].split('=')[1])
            maxrerr2=eval(lines[4].split('=')[1])
        data[j+1][i-51][3]=cr2
        data[j+1][i-51][4]=psnr2
        data[j+1][i-51][5]=maxrerr2
        os.system("rm -f %s.txt" % pid)



        os.system("sz_demo %s -1 %d %f %d 0 1 " % (dvname,dlength,eb/10,dlength))
        os.system("mv %s.sz3 %s.sz3;mv %s.sz3.out %s.sz3.out" % (dvname,dvpath,dvname,dvpath))
        os.system("du -s %s*&>%s.txt" % (filepath,pid))
        origsize=0
        compressedsize=0
        dvname=filepath.split("/")[-1]+".dvalue"
        dvpath=filepath+".dvalue"
        with open ("%s.txt"%pid,"r") as f:
            lines=f.read().splitlines()
            for line in lines:
                size,path=line.split("\t")
                size=float(size)
                if path==filepath:
                    origsize=size
                if path==zpath or path==dvpath+".sz3" or path==filepath+".dindex" or path==filepath+".min" or path==filepath+".mod" or path==filepath+".str":
                    compressedsize+=size
        cr3=origsize/compressedsize
        os.system("rm -f %s.txt" % pid)


        os.system("python3 Autoencoder_Prototype.py -d %s -z 1" % zpath)
        os.system("compareData -f %s %s>%s.txt" % (filepath,dpath,pid))
        with open ("%s.txt"%pid,"r") as f:
            lines=f.read().splitlines()
            psnr3=eval(lines[6].split(',')[0].split('=')[1])
            maxrerr3=eval(lines[4].split('=')[1])
        data[j+1][i-51][6]=cr3
        data[j+1][i-51][7]=psnr3
        data[j+1][i-51][8]=maxrerr3
        os.system("rm -f %s.txt" % pid)

np.savetxt("%s_cr1.txt" % output,data[:,:,0],delimiter='\t')
np.savetxt("%s_psnr1.txt" % output,data[:,:,1],delimiter='\t')
np.savetxt("%s_maxrerr1.txt" % output,data[:,:,2],delimiter='\t')
np.savetxt("%s_cr2.txt" % output,data[:,:,3],delimiter='\t')
np.savetxt("%s_psnr2.txt" % output,data[:,:,4],delimiter='\t')
np.savetxt("%s_maxrerr2.txt" % output,data[:,:,5],delimiter='\t')
np.savetxt("%s_cr3.txt" % output,data[:,:,6],delimiter='\t')
np.savetxt("%s_psnr3.txt" % output,data[:,:,7],delimiter='\t')
np.savetxt("%s_maxrerr3.txt" % output,data[:,:,8],delimiter='\t')



        
        

