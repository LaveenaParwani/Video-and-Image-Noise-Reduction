#complete code for working video
import cv2                               #for image operations
import numpy as np                       #for image stored in array
from matplotlib import pyplot as plt     #for plotting the graph
import math                              #for math iopoerations
import glob                              #to access the files from folder
import os                                #for file or folder handling
import shutil                            #to remove the folder with files



videopath=input("Enter any Path====")
print("Your Path is===",videopath)
#break video into frames with noisy frames and creating folder
path1="C:\\PSNR\\frame_with_noise"
if os.path.exists(path1) and os.path.isdir(path1):
    shutil.rmtree(path1)
    print("Delete")
if not os.path.isfile(path1):
    os.makedirs(path1)
    print("Create")

vidcap1 = cv2.VideoCapture(videopath)  #capturing video
success,image1 = vidcap1.read()#Read the video
                               # Capture frame-by-frame
count = 0
success = True
while success:
  
  cv2.imwrite("%s\\imgN%d.jpg" %(path1,count), image1)      # save frame as JPEG file
  vidcap1.set(cv2.CAP_PROP_POS_MSEC,(count)) #used to hold speed of frame generation
                                             #Current position of the video file in milliseconds
  
  success,image1 = vidcap1.read()
  print ('Read a new frame: ', success)
  count += 1
  if(count==200):
      break
print("the total frames=",count)
cv2.waitKey(0)  
 
#------------------------------without noise frames conversion---------------- 

#break video into frames with noise removal with filter
path2="C:\\PSNR\\frame_without_noise"
if os.path.exists(path2) and os.path.isdir(path2):
    shutil.rmtree(path2)
    print("Delete")
if not os.path.isfile(path2):
    os.makedirs(path2)
    print("Create")



vidcap = cv2.VideoCapture(videopath)
success,image = vidcap.read()#READ THE VIDEO
count1 = 0
success = True
while success:
  blur = cv2.bilateralFilter(image,9,75,75)  #filter
  opr=cv2.fastNlMeansDenoisingColored(blur,None,10,10,7,21)    #remove noise
  cv2.imwrite("%s\\imgWN%d.jpg" %(path2,count1),opr)     # save frame as JPEG file
  vidcap.set(cv2.CAP_PROP_POS_MSEC,(count1)) #used to hold speed of frane generation
  success,image = vidcap.read()
  print ('Read a new frame: ', success)
  count1 += 1
  if(count1==200):
      break
  print("count 2====",count1)
cv2.waitKey(0)  


#-----------------psnr of all frames-----------------------------------
psnr1=[]    #empty list to store psnr values

f1 = [cv2.imread(file) for file in glob.glob("%s\\*.jpg"%path1)] #frames with noise
f2 = [cv2.imread(file) for file in glob.glob("%s\\*.jpg"%path2)]  #frame witthout noise
i=0             #for checking loop working

#psnr of all frames and average of all frames


def psnr(a,b):              # Calculate psnr for two images
    mse = np.mean( (a -b) ** 2 )
    if mse == 0:
        return 100
    PIXEL_MAX = 255.0
    return 20 * math.log10(PIXEL_MAX / math.sqrt(mse))


for x in range(count):      #take no. of frames from loop count
    
        plt.subplot(121),plt.imshow(f1[x]),plt.title('Noised image') #images with noise
        plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(f2[x]),plt.title('Denoised image') #imges without noise
        plt.xticks([]), plt.yticks([])
        d=psnr(f1[x],f2[x])    #calling psnr calculation function
        print("psnr",d)      #print psnr of every two frams i.e original and blured
        psnr1.append(d)     #store all value of psnr
        
        plt.show()
        i+=1
        print("the value==",i)
        cv2.waitKey(0) 
        
        
print("complete") 
#print(psnr1)
print("The average of all frames psnr==",sum(psnr1)/count)   #find average of all psnr values
cv2.waitKey(0)   



#---------------------graph----------
x1 = np.arange(count)
# setting the corresponding y - coordinates
y = psnr1

plt.xlabel('Frames')
plt.ylabel('Psnr values')
 
# potting the points
plt.plot(x1, y)
 
# function to show the plot
plt.show()    
