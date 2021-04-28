import os
import sys
import numpy as np
field=sys.argv[1]
epoch=int(sys.argv[2])
output=sys.argv[3]
mode=0# 0 all 1 train only 2 test only
if (len(sys.argv)>=5):
    mode=int(sys.argv[4])
print(mode)
coeff=1
if (len(sys.argv)>=6):
    coeff=float(sys.argv[5])

datafolder="/home/jliu447/lossycompression/cesm-multisnapshot-5fields/%s" % field
trainfile="/home/jliu447/lossycompression/cesm-multisnapshot-5fields/%s/%s_0to49.dat" % (field,field)
if(mode<2):
    os.system("python3 Autoencoder_Prototype.py -r %s -i %d -n %s" % (trainfile,epoch,field))
    print("Train Over.")


if (mode!=1):
    
    ebs=[1e-2,1e-3]
    #ebs=[i*1e-4 for i in range(1,10,2)]+[i*1e-3 for i in range(1,10,2)]+[i*1e-2 for i in range(1,10,2)]+[0.1]
    idxrange=[x for x in range(52,53)]
    #idxrange=[x for x in range(52,63)]

    pid=str(os.getpid()).strip()
    data=np.zeros((len(ebs)+1,len(idxrange)+1,9),dtype=np.float32)
    for i in range(9):
        data[1:,0,i]=ebs
        data[0,1:,i]=idxrange

    for i,idx in enumerate(idxrange):
        filename="%s_%d.dat" % (field,idx)
        filepath=os.path.join(datafolder,filename)
        a=np.fromfile(filepath,dtype=np.float32)
        a=a-np.min(a)
        filepath=filepath+".positive"
        a.tofile(filepath)
        for j,eb in enumerate(ebs): 
            os.system("python3 Autoencoder_Prototype.py -c %s -e %f -n %s" % (filepath,eb,field))
            zpath=filepath+".z"
            dpath=zpath+".d"
            dvname=filepath.split("/")[-1]+".dvalue"
            dvpath=filepath+".dvalue"
            os.system("du -s %s*&>%s.txt" % (filepath,pid))
            origsize=0
            compressedsize=0
            with open ("%s.txt"%pid,"r") as f:
                lines=f.read().splitlines()
                print(lines)
                for line in lines:
                    size,path=line.split("\t")
                    size=float(size)
                    if path==filepath:
                        origsize=size
                    if path==zpath or path==dvpath or path==filepath+".dindex" or path==filepath+".min" or path==filepath+".mod" or path==filepath+".str":
                        compressedsize+=size
            cr1=origsize/compressedsize
            os.system("rm -f %s.txt" % pid)   

            os.system("python3 Autoencoder_Prototype.py -d %s -n %s" % (zpath,field))
            os.system("compareData -f %s %s&>%s.txt" % (filepath,dpath,pid))
            with open ("%s.txt"%pid,"r") as f:
                lines2=f.read().splitlines()
                print(lines2)
                psnr1=eval(lines2[6].split(',')[0].split('=')[1])
                maxrerr1=eval(lines2[4].split('=')[1])
            data[j+1][i+1][0]=cr1
            data[j+1][i+1][1]=psnr1
            data[j+1][i+1][2]=maxrerr1
            os.system("rm -f %s.txt" % pid)    

            
            a=np.fromfile(dvpath,dtype=np.float16)
            dlength=a.shape[0]
            a.astype(np.float32).tofile(dvpath)


            '''
            os.system("sz_demo %s -1 %d %f %d 0 1 " % (dvpath,dlength,0.1,dlength))
            os.system("mv %s*.sz3 %s.sz3;mv %s*.sz3.out %s.sz3.out" % (dvname,dvpath,dvname,dvpath))
        #os.system("sz_demo %s -1 %d %f %d 0 1 " % (dvname,dlength,sze,dlength))
            os.system("du -s %s*&>%s.txt" % (filepath,pid))
            origsize=0
            compressedsize=0
            
            with open ("%s.txt"%pid,"r") as f:
                lines3=f.read().splitlines()
                print(lines3)
                for line in lines3:
                    size,path=line.split("\t")
                    size=float(size)
                    if path==filepath:
                        origsize=size
                    if path==zpath or path==dvpath+".sz3" or path==filepath+".dindex" or path==filepath+".min" or path==filepath+".mod" or path==filepath+".str":
                        compressedsize+=size
            cr2=origsize/compressedsize
            os.system("rm -f %s.txt" % pid)


            os.system("python3 Autoencoder_Prototype.py -d %s -z 1 -n %s" % (zpath,field))
            os.system("compareData -f %s %s&>%s.txt" % (filepath,dpath,pid))
            with open ("%s.txt"%pid,"r") as f:
                
                lines4=f.read().splitlines()
                print(lines4)
                psnr2=eval(lines4[6].split(',')[0].split('=')[1])
                maxrerr2=eval(lines4[4].split('=')[1])
            data[j+1][i+1][3]=cr2
            data[j+1][i+1][4]=psnr2
            data[j+1][i+1][5]=maxrerr2
            os.system("rm -f %s.txt" % pid)
            '''

            latent_eb=eb/coeff
            os.system("sz_demo %s -1 %d %f %d 0 1 " % (dvpath,dlength,eb,dlength))
            os.system("mv %s*.sz3 %s.sz3;mv %s*.sz3.out %s.sz3.out" % (dvname,dvpath,dvname,dvpath))
            os.system("du -s %s*&>%s.txt" % (filepath,pid))
            origsize=0
            compressedsize=0
            
            with open ("%s.txt"%pid,"r") as f:
                lines5=f.read().splitlines()
                print(lines5)
                for line in lines5:
                    size,path=line.split("\t")
                    size=float(size)
                    if path==filepath:
                        origsize=size
                    if path==zpath or path==dvpath+".sz3" or path==filepath+".dindex" or path==filepath+".min" or path==filepath+".mod" or path==filepath+".str":
                        compressedsize+=size
            cr3=origsize/compressedsize
            os.system("rm -f %s.txt" % pid)


            os.system("python3 Autoencoder_Prototype.py -d %s -z 1 -n %s" % (zpath,field))
            os.system("compareData -f %s %s&>%s.txt" % (filepath,dpath,pid))
            with open ("%s.txt"%pid,"r") as f:
                lines6=f.read().splitlines()
                print(lines6)
                psnr3=eval(lines6[6].split(',')[0].split('=')[1])
                maxrerr3=eval(lines6[4].split('=')[1])
            data[j+1][i+1][6]=cr3
            data[j+1][i+1][7]=psnr3
            data[j+1][i+1][8]=maxrerr3
            os.system("rm -f %s.txt" % pid)
            os.system("rm -f %s.*" % filepath)
        os.system("rm -f %s*" % filepath)

    np.savetxt("%s_cr1.txt" % output,data[:,:,0],delimiter='\t')
    np.savetxt("%s_psnr1.txt" % output,data[:,:,1],delimiter='\t')
    np.savetxt("%s_maxrerr1.txt" % output,data[:,:,2],delimiter='\t')
    '''
    np.savetxt("%s_cr2.txt" % output,data[:,:,3],delimiter='\t')
    np.savetxt("%s_psnr2.txt" % output,data[:,:,4],delimiter='\t')
    np.savetxt("%s_maxrerr2.txt" % output,data[:,:,5],delimiter='\t')
    '''
    np.savetxt("%s_cr3.txt" % output,data[:,:,6],delimiter='\t')
    np.savetxt("%s_psnr3.txt" % output,data[:,:,7],delimiter='\t')
    np.savetxt("%s_maxrerr3.txt" % output,data[:,:,8],delimiter='\t')



        
        

