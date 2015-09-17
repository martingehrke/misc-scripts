# exif_sort[January 2012] / martin gehrke [martin AT teamgehrke.com]
# sorts jpg/jpegs into date folders based on exif data

from PIL import Image
from PIL.ExifTags import TAGS
import sys, os, glob

def format_dateTime(UNFORMATTED):
	DATE, TIME = UNFORMATTED.split()
        #only return the yearmonth
	return DATE.replace(':','')[:-2]
	
 
def get_exif(fn):
    ret = {}
    i = Image.open(fn)
    info = i._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    return ret


def sortPhotos(path):
	PHOTOS = []
	EXTENSIONS =['.jpg','.jpeg']
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
                        print DATE
                        
                        if not os.path.exists(DATE):
                                os.mkdir(DATE)

                        os.rename(PHOTO, "%s\%s" % (DATE,PHOTO))
                except AttributeError:
                        pass


if __name__=="__main__":
	PATH = sys.argv[0]

	if PATH == '': PATH = os.getcwd()
	
	sortPhotos(PATH)

