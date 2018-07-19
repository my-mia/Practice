#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 00:00:28 2018

@author: hewang
"""


from scipy.spatial import Voronoi
from scipy import ndimage
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mimage
import cv2
from scipy.spatial import Voronoi, voronoi_plot_2d
from skimage import measure,color
from skimage.measure import label, regionprops
from scipy.spatial import Voronoi
from scipy.spatial import cKDTree
import pymysql
import os
import datetime





'''database to insert data'''        
def update(conn,c,sql):
    newdata=c.execute(sql)
    conn.commit()
    return newdata
'''database to insert data''' 
#%%define function
def Label(name, fullpath):
    fullpath=directory+'/'+name
    img = cv2.imread(fullpath)
    img_N =  cv2.imread(fullpath)
    img_N[:,:,1] = 0
    img_N[:,:,2]= 0
    gray_image = cv2.cvtColor(img_N, cv2.COLOR_BGR2GRAY)
    imgb = gray_image
    (thresh, im_bw) = cv2.threshold(imgb, 255, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    median = cv2.medianBlur(im_bw,5)
    imgfill, contours, hierarchy = cv2.findContours(median,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        cv2.drawContours(median,[cnt],0,255,-1)
        kernel = np.ones((4,4),np.uint8)
    erosion = cv2.erode(imgfill,kernel,iterations = 1)

    kernel = np.ones((25,25),np.uint8)
    opening = cv2.morphologyEx(erosion, cv2.MORPH_OPEN, kernel)
    labels=measure.label(opening,connectivity=2)
    #dst=color.label2rgb(labels)
    blobs = img >0.75
    properties = regionprops(labels)
    
    for p in properties:
        min_row, min_col, max_row, max_col = p.bbox

    fig = plt.figure()
    ax = fig.add_subplot(111)    
    ax.imshow(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
    ax.set_title('Labeled objects')
    plt.xticks([])
    plt.yticks([])
    lbl,nlbls = ndimage.label(np.array(opening))
    r, c = np.vstack(ndimage.center_of_mass(np.array(opening),lbl,np.arange(nlbls)+1)).T
    centerpoints = np.array(ndimage.center_of_mass(np.array(opening),lbl,np.arange(nlbls)+1))
    centerpoints[:, [0, 1]] = centerpoints[:, [1, 0]]

    for ri, ci, li in zip(r, c, range(1, nlbls+1)):
        ax.annotate(li, xy=(ci, ri), fontsize=8, color = 'white')
        
"****==========================****"        
        
def Seg(name, directory, ParentImg, id_oriImg):
    
    fullpath=directory+'/'+name
    img = cv2.imread(fullpath)
    #imgray = cv2.imread(fullpath,0)
    img_N =  cv2.imread(fullpath)
    img_N[:,:,1] = 0
    img_N[:,:,2]= 0

    img2 =  cv2.imread(fullpath)
    img2[:,:,0]= 0
    img2[:,:,2]= 0
    
    mito_grayimg = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
    blur_mito = cv2.blur(mito_grayimg,(7,7))
    (thresh1, im_bwmito) = cv2.threshold(blur_mito, 255, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    kernel1 = np.ones((20,20),np.uint8)
    dilate_mito = cv2.dilate(im_bwmito,kernel1,iterations = 1)
    label_mito=measure.label(dilate_mito,connectivity=2)
    properties_mito = regionprops(label_mito)
    masscenter_mito=[]
    
    for pro in properties_mito:
        masscenter_mito.append(pro.centroid)
    
    masscenter_mitop=np.array(masscenter_mito)
    masscenter_mitop[:, [0, 1]] = masscenter_mitop[:, [1, 0]]
    gray_image = cv2.cvtColor(img_N, cv2.COLOR_BGR2GRAY)
    imgb = gray_image
    (thresh, im_bw) = cv2.threshold(imgb, 255, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    median = cv2.medianBlur(im_bw,5)
    imgfill, contours, hierarchy = cv2.findContours(median,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        cv2.drawContours(median,[cnt],0,255,-1)   
        kernel = np.ones((4,4),np.uint8)
        
    erosion = cv2.erode(imgfill,kernel,iterations = 1)
    kernel = np.ones((25,25),np.uint8)
    opening = cv2.morphologyEx(erosion, cv2.MORPH_OPEN, kernel)
    labels=measure.label(opening,connectivity=2)
    dst=color.label2rgb(labels)
    blobs = img >0.75
    properties = regionprops(labels)

    for p in properties:
        min_row, min_col, max_row, max_col = p.bbox

    lbl,nlbls = ndimage.label(np.array(opening))
    r, c = np.vstack(ndimage.center_of_mass(np.array(opening),lbl,np.arange(nlbls)+1)).T
    centerpoints = np.array(ndimage.center_of_mass(np.array(opening),lbl,np.arange(nlbls)+1))
    centerpoints[:, [0, 1]] = centerpoints[:, [1, 0]]

    points = centerpoints
    vor = Voronoi(points)
    #voronoi_plot_2d(vor)
    voronoi_kdtree = cKDTree(points)
    extraPoints = []
    imgSet = []
    height, width = img2.shape[:2]
    extraPoints = masscenter_mitop       
    test_point_dist, test_point_regions = voronoi_kdtree.query(extraPoints)
    true_regions=[]
    true_regions=test_point_regions+1
    true_regions
    true_regions[1]
    shuzu = [[] for _ in range(nlbls+1)]
    
    for i in range(true_regions.shape[0]):
        shuzu[true_regions[i]].append(i+1)
        
    File_Path = os.getcwd()+'/media' 
    #if not os.path.exists(File_Path):
        #os.makedirs(File_Path)    
         
    def showandshoweachcell(shuzu):
        for i1 in range(len(shuzu)):
           imgoriginal = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
           if len(shuzu[i1]) != 0:
               mask = (labels == i1)
               for i2 in range(len(shuzu[i1])):
                   mask = mask|(label_mito==shuzu[i1][i2])
               get_high_vals = mask ==0
               imgoriginal[get_high_vals] = 0
               plt.title('Cell%i'%i1)
               plt.axis('off')
               plt.imshow(imgoriginal)
               plt.savefig(File_Path+'/'+name+"_cell%s.png"%i1, dpi = 300)
               plt.show()
               SegImgName=name+'_cell%s.png'%i1
               conn = pymysql.connect(host='localhost', port=3306, \
                       user='root', passwd='Yinchuandog45#',\
                       db='Seg', charset='utf8')              
               c=conn.cursor()
               dt=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
               
               c.execute('insert into Seg_segimg(SegImgName,ParentImg,FileDirectorySegImg,CreateTimeSeg,oriImg_id)\
                             values("{}", "{}", "{}", "{}", "{}")'.format(SegImgName,ParentImg,File_Path,dt,id_oriImg))
               #data=(repr(SegImgName), repr(ParentImg), repr(dic), repr(dt), repr(id_oriImg))
               #sql = "insert into citsec('SegImgName', 'ParentImg', 'FileDirectorySegImg', 'CreateTimeSeg', 'oriImg_id') values(%s,%s,%s,%s,%s)"
               #c.execute("insert into Seg_segimg \
                          #values(repr(SegImgName), repr(ParentImg), repr(dic), repr(dt), repr(id_oriImg)")
               #c.execute(sql_insert) 
               c.close()
               conn.commit()
    showandshoweachcell(shuzu)
    

#%%This is for defining Class

class OriImg:
    def __init__ (self, name, dictionary):
        self.name = name
        self.dictionary = dictionary
        self.fullpath = dictionary+name
        
        
        
    def ShowImg(self):
       # self.Img=self.
        #plt.titile('orignial image')
        #self.imgshow = cv2.imread(self.fullpath)
        return plt.show(), plt.title('original image'),\
        plt.imshow(cv2.cvtColor(cv2.imread(self.fullpath), cv2.COLOR_BGR2RGB))
        
      
class LabelCells:
        def __init__ (self, name, dictionary):
            self.name = name
            self.dictionary = dictionary
            
        
        def Label(self):
            return Label(self.name, self.dictionary)
        
class SegCells:
    def __init__ (self, name, dictionary,ParentImg, id_oriImg):
            self.name = name
            self.dictionary = dictionary
            self.ParentImg=ParentImg
            self.id_oriImg=id_oriImg
        
    def Seg(self):
        return Seg(self.name, self.dictionary, self.ParentImg, self.id_oriImg)  


#%%connect database

"""
    
conn = pymysql.connect(host='localhost', port=3306, \
                       user='root', passwd='Yinchuandog45#',\
                       db='Seg', charset='utf8')
c=conn.cursor()
print("Open database successfully")

c.execute("select img_url, FileDirectoryImg,\
           ImgName, id\
           from Seg_oriimg")
select = c.fetchall()

for row in select:
    print("img_url", row[0])
    print("dic", row[1])
    print("ImgName",row[2])
    print("id",row[3])
    
#dic='/Users/hewang/Documents/lab/YFPdataSet/'
#name='YFP0145-1_2.tif'
    dic=row[1]
    name=row[0]
    ParentImg=row[2]
    id_oriImg=row[3]
    #fullpath=dic+'/'+name

    #OrImg=OriImg(name, dic)
    #OrImg.ShowImg()

    #LabCell=LabelCells(name, dic)
    #LabCell.Label()

    SgCell=SegCells(name, dic, ParentImg, id_oriImg)
    SgCell.Seg()
c.close()
conn.commit()
conn.close()
    
#Label(fullpath)
#Seg(fullpath)
#Img = OriImg(name, dic) #generate a new image  


#Img.ShowImg() #show image


#Img_N = LabelCells(name, dic)
#Img_N.Nuclei(())
"""