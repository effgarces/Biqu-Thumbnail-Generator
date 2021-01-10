#!/usr/local/bin/python3
import base64
import io, os, shutil
import sys, getopt
try:
	from PyQt5.QtCore import QSize,Qt
	from PyQt5.QtCore import QFile, QFileInfo, QIODevice,QTextStream
	from PyQt5.QtGui import QImage
except:
  print ("!!! PyQt5 not installed run pip install PyQt5 !!!")
  sys.exit()
  
CODEC = "UTF-8"

def i4b(n):
    return [n >> 24 & 0xFF,n >> 16 & 0xFF,n >> 8 & 0xFF,n >> 0 & 0xFF]

def i2b(n):
    return [n >> 8 & 0xFF,n >> 0 & 0xFF]

def overread(msize,gfile):
    moutdata = ""
    img = QImage()
    img.loadFromData(base64topng(readPSTump(gfile),''))
    img = img.scaled(msize.width(),msize.height(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
    moutdata +=  ";"+(hex(msize.width())[2:]).rjust(4,'0')+(hex(msize.height())[2:]).rjust(4,'0')+"\r\n"
    pos = QSize(0,0)
    for ypos in range(0,img.height()):
     qrgb =";"
     for xpos in range(0,img.width()):
       data = img.pixel(xpos,ypos)
       pos.setWidth(pos.width()+1)
       dummy = (hex(((data & 0x00F80000) >> 8 ) | ((data & 0x0000FC00) >> 5 ) | ((data & 0x000000F8) >> 3 ))[2:]).rjust(4,'0')
       if dummy == "0020" or dummy == "0841" or dummy == "0861":
         dummy = "0000"
       qrgb = qrgb + dummy
     pos.setWidth(0)
     pos.setHeight(pos.height()+1)
     moutdata = moutdata + qrgb + "\r\n"    
    return moutdata



def overseek(gfile):
        outdatar = ""
        outdatar = outdatar + overread(QSize(70,70),gfile)
        outdatar = outdatar + overread(QSize(95,80),gfile)
        outdatar = outdatar + overread(QSize(95,95),gfile)
        outdatar = outdatar + overread(QSize(160,140),gfile)
        return outdatar

def do_convert(gfile):
       outdata = ""
       outdata = overseek(gfile)
       outdata = outdata + "; bigtree thumbnail end\r\n\r\n"
       fh = QFile(gfile)
       fh.open(QIODevice.ReadOnly)
       stream = QTextStream(fh)
       stream.setCodec(CODEC)
       lino = 0
       fg = stream.readAll() + "\r\n"
       fh.close()
       bigtree3dfile = os.path.splitext(gfile)[0]+"_btt"+os.path.splitext(gfile)[1]
       fh = QFile(bigtree3dfile)
       fh.open(QIODevice.WriteOnly)
       stream = QTextStream(fh)
       stream.setCodec(CODEC)
       stream << outdata
       stream << fg
       fh.close()
       os.remove(gfile)



## write base64 to png
def base64topng(stringdata,imagepath): 
  
  image = base64.b64decode(stringdata)       

  return image

def readPSTump(infile):
  
  count = 0
  base64data =''
  started = 0
  ended = 0
  Psfile = open(infile,"r")
  while True:
      count =count+1  
      # Get next line from file 
      line = Psfile.readline() 
      if line.find("; thumbnail begin") == 0:      
         started = 1
         continue

      if line.find("; thumbnail end") == 0:
         ended = 1
      
      if ended == 1:
        break
      # if line is empty 
      # end of file is reached 
    
      if not line:
         break
      
      if started == 0:
      	continue
      	
      base64data += line[2:]
  Psfile.close()
  if base64data == '':
     print('!!! no thumbnail data found in gcode !!!')
     sys.exit() 
  ##with open('base64.txt', 'w') as fh:
  ##   fh.writelines("%s" % line for line in base64data)
  return base64data

def readPSGcode(infile):
  gcodedata =''
  started = 0

  Psfile = open(infile,"r")
  while True: 
     # Get next line from file 
     line = Psfile.readline() 

     if line.find("; thumbnail end") == 0:
        started = 1
        continue
      
     if started == 0:
     	continue 

      # if line is empty 
      # end of file is reached 
     if not line: 
        break
     
     gcodedata += line
  Psfile.close() 
  return gcodedata
  
def main(argv):
   
   inputfile = ''
   outputfile = ''
   try:  
     inputfile = sys.argv[1]
   except:
      print('./biqu_convert inputfile')
      sys.exit()
   
   do_convert(inputfile)

  

if __name__ == "__main__":
   main(sys.argv[1:])





