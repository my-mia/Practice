from django.shortcuts import render
from Seg.models import OriImg
from django.http import HttpResponse
import os

#from django.http import HttpResponse
# Create your views here.
#def hello(request):
    #IMG.objects.filter(name='bg')
    #img = IMG.objects.all()
    #return render(request, 'Welcome.html',{'img':img})
"""
def uploadImg(request):
    id=request
    img=OriImg.objects.all()
    return render(request,'Test.html',{'img':img})

"""
#@csrf_exempt
def Home(request):
    return render(request, 'Home.html')

def uploadImg(request):
    if request.method == 'POST':
        img = OriImg(
            img_url=request.FILES.get('img'),
            ImgName = request.FILES.get('img').name,
            FileDirectoryImg =os.path.join(os.path.dirname(os.path.abspath(__name__)), 'media')
        )
        img.save()
    return render(request, 'production/form_wizards.html')

def showImg(request):
    imgs = OriImg.objects.all()
    content = {
        'imgs':imgs,
    }
    #for i in imgs:
        #print(i.img.url)
    return render(request, 'production/form_wizards.html', content)

def Index(request):
    return render(request, 'production/index2.html')

def Seg(request):
    return render(request, 'Seg.html')

def Analysis(request):
    return render(request, 'Analysis.html')
#def index(request):
    #return render(request, 'Testshow.html') 

def Callpy(request):
    if request.method == 'POST':
        import pymysql
        import sys
        sys.path.append('/Users/hewang/Desktop/dj/mymia')
        from mymiaSeg import SegCells 
        imgs = OriImg.objects.all()
        
def Callpy(request):
    if request.method == 'POST':
       
        import pymysql
        import sys
        sys.path.append('/Users/hewang/Desktop/dj/mymia')
        from mymiaSeg import SegCells
        #from mymiaSeg import Seg
        
        
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
            conn.ping(reconnect=True)
            SgCell=SegCells(name, dic, ParentImg, id_oriImg)
            
            SgCell.Seg()
        c.close()
        conn.commit()
        conn.close()
        #os.system('/Users/hewang/Desktop/dj/mymia/mymiaSeg.py')
        
    return render(request,'Seg.html')
    
  
"""
def Callpy(request):
    app = request.GET.get('app')
    if app == 'Seg':
        os.system('open /Users/hewang/Desktop/dj/mymia/mymiaSeg.py')
        #return render(request,'callpy.html',{'text':'Cells have been Segmented!'})
    elif app == 'Label':
        os.system('open /Users/hewang/Desktop/dj/mymia/mymiaSeg.py')
        #return render(request,'callpy.html',{'text':'Cell Labeled!'})
    return render(request,'Seg.html')
    #return redirect('/segimg/')

def Callpy(request):
    if request.method == 'GET':
        os.system('open /Users/hewang/Desktop/dj/mymia/mymiaSeg.py')
    return render(request,'Seg.html')
"""