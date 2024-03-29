import cv2
import os
import numpy as np
import random
from PIL import Image

########EDIT THESE PARAMS############
basepath='D:\Pictures\Edinburgh\\'  #Path of All Pictures
mainimgpath=basepath+'lol1.jpg'
entries = os.listdir(basepath)

ncol=20  #No. of pics in a single row or column
nrow=20

small_res=10  #size of each small pic

overlay_param=0.3 #parameter to tune when making overlayd image

fmts=['.jpg','.png','jpeg']  #List of last 4 letters of files you want to read from the folder

#####################DONE EDITING PARAMS##########

canvas=np.zeros((nrow*small_res,ncol*small_res,3),dtype='uint8')  #creating a canvas for the whole portrait

imgs=[]  #initilizing arrays
vals=[[0,0,0]]


for ent in entries[:np.int(ncol*nrow+10)]:
    if ent[-4:] in fmts:   #getting all images from folder specified
        img=cv2.imread(basepath+ent)
        h,w,lol=img.shape           # cutting all the images
        dim=np.min([h,w])           #  in squares
        img=img[:dim,:dim,:]        #  just by clipping them
        val=np.array(np.sum(np.sum(img,axis=0),axis=0)/(dim*dim))   #average intesnity of the image
        vals.append(val)  #saving average intensities in another array
        imgs.append(cv2.resize(img,(small_res,small_res)))  #resizing each small image to small_res(which is 300px here)
        del img  #deleting images to ease up memory
del vals[0]
vals=np.array(vals)

reps=np.ceil((ncol*nrow)/len(imgs)).astype(int)
#print(reps,len(imgs),np.floor((ncol*nrow)/len(imgs)),(ncol*nrow)/len(imgs))
imgss=[imgs.copy() for i in range(reps)] # repeating the images into a new array
valss=[vals.copy() for i in range(reps)]   # repeating the vaerage intenities into a new array

bigimg=cv2.imread(mainimgpath)

mainimg=cv2.resize(bigimg,(ncol,nrow)).astype('uint8')

k=0
for i in range(nrow):
    for j in range(ncol):
        
        clr=mainimg[i,j]   
            
        if len(imgss[k])==0:  
            k+=1
        idx=np.argmin(np.sum(np.abs(valss[k]-clr),axis=1))  #find picture corresponding intesity of pixel
        bestimg=imgss[k][idx]
        beta=clr-(np.sum(np.sum(bestimg,axis=0),axis=0)/(small_res**2))
        bestimg=np.clip(bestimg + beta, 0, 255)
        valss[k]=np.delete(valss[k],idx,axis=0)
        del imgss[k][idx]
        canvas[i*small_res:(i+1)*small_res,j*small_res:(j+1)*small_res]=bestimg


canvas=canvas.astype('uint8')

h= small_res*nrow
w=small_res*ncol
bigres=cv2.resize(bigimg,(w,h))  #read the image again

canvas_im=Image.fromarray(canvas[:,:,::-1])
bigres_im=Image.fromarray(bigres[:,:,::-1])
overlayed_im=Image.blend(canvas_im,bigres_im,alpha=overlay_param)

canvas_im.save(mainimgpath.split('\\')[-1][:-4]+"Out.jpg")# Save Image without overlay
overlayed_im.save(mainimgpath.split('\\')[-1][:-4]+"Out_Overlayed.jpg")#This saves an overlayed image

print('Done!')
