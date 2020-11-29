# exif_sort[January 2020] / martin gehrke [martin AT teamgehrke.com]
# sorts jpg/jpegs into date folders based on exif data

from PIL import Image
from PIL.ExifTags import TAGS
import sys, os, glob
import datetime

def format_dateTime(UNFORMATTED):
	DATE, TIME = UNFORMATTED.split()
        #only return the yearmonth
	return DATE.replace(':','')[:-2]
	
 
def get_exif(fn):
    ret = {}
    try:
            i = Image.open(fn)
    except:
            #raise IOError
            pass
    info = i._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    return ret

def get_created(fn):
        (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(fn)
        return ctime  

def sortPhotos(path):
	PHOTOS = []
	EXTENSIONS =['.jpg','.jpeg', '.gif', '.JPG', 'JPEG']
	for EXTENSION in EXTENSIONS:
		PHOTO = glob.glob('*%s' % EXTENSION)
		PHOTOS.extend(PHOTO)
	
	for PHOTO in PHOTOS:
                try:
                        EXIF_DATA = get_exif(PHOTO)
                        
                        if EXIF_DATA.has_key('DateTime'):
                                DATE = format_dateTime(EXIF_DATA['DateTime'])
                        elif EXIF_DATA.has_key('DateTimeOriginal'):
                                DATE = format_dateTime(EXIF_DATA['DateTimeOriginal'])
                                                
                        if not os.path.exists(DATE):
                                os.mkdir(DATE)

                        os.rename(PHOTO, "%s\%s" % (DATE,PHOTO))                       
                except AttributeError:
                        pass
                except UnboundLocalError:
                        print(PHOTO)
                except OSError:
                        print(PHOTO)


        # for leftover photos that don't have exif data
	PHOTOS = []
	for EXTENSION in EXTENSIONS:
		PHOTO = glob.glob('*%s' % EXTENSION)
		PHOTOS.extend(PHOTO)

	
	for PHOTO in PHOTOS:
                unformatted_date = get_created(PHOTO)
                WITH_TIME = str(datetime.datetime.fromtimestamp(unformatted_date))
                DATE_ONLY = WITH_TIME.split()[0]
                DATE = DATE_ONLY.replace('-','')[:-2]         
                
                if not os.path.exists(DATE):
                        os.mkdir(DATE)

                try: os.rename(PHOTO, "%s\%s" % (DATE,PHOTO))
                except WindowsError:
                        print(PHOTO)
                


if __name__=="__main__":
	PATH = sys.argv[0]

	if PATH == '': PATH = os.getcwd()
	
	sortPhotos(PATH)
