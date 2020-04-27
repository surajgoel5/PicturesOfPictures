import cv2
import os
import numpy as np


basepath='D:\Pictures\Edinburgh\\'  #Path of All Pictures
mainimgpath=basepath+'lol1.jpg'
entries = os.listdir(basepath)

ncol=5  #No. of pics in a single row or column
nrow=4 

small_res=50  #size of each small pic

overlay_param=10 #parameter to tune when making overlayd image

fmts=['.jpg','.png','jpeg']  #List of last 4 letters of files you want to read from the folder

canvas=np.zeros((nrow*small_res,ncol*small_res,3),dtype='uint8')  #creating a canvas for the whole portrait

imgs=[]  #initilizing arrays
vals=[[0,0,0]]


for ent in entries[:1]:#np.int(ncol*nrow+10)]:
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

reps=np.floor((ncol*nrow)/len(imgs)).astype(int)

imgss=[imgs.copy() for i in range(reps)] # repeating the images into a new array
valss=[vals.copy() for i in range(reps)]   # repeating the vaerage intenities into a new array

bigimg=cv2.imread(mainimgpath)

mainimg=cv2.resize(bigimg,(ncol,nrow)).astype('uint8')

k=0
print('do')

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
##Till now you have made collage but it might not be clear because it has very low resolution. 
##The resolution being the number of pics ina row. So we overlay the main image again and 
## change intensities of each pixel in the image to get it close to the real image. 

h= small_res*nrow
w=small_res*ncol
bigres=cv2.resize(bigimg,(w,h))  #read the image again



cv2.imwrite("Out.jpg",canvas)   # Save Image without overlay

cv2.imwrite("Out_Overlayed.jpg",np.clip(canvas + np.rint((bigres-canvas)/overlay_param),0,255))  #This saves an overlayed image
