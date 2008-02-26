# import modules from std library
import os, shutil
# 'C:/Program Files/wget' is the default install dir
#   for wget - get wget from: http://www.gnu.org/software/wget/
# this is where we want to initially download our files to 
#   then we move them later
# this script needs to reside in the wget dir as well to be run
wgetDir = 'C:/Program Files/wget/o'
# nested list of quads we want to grab; where the members are:
#   [quad_id,quad_name,state] - change this to grab what you want
quads = [['36094a1','ELKINS','ar'],['36094a2','FAYETTEVILLE','ar']]
# the extensions of the different filetypes to grab; if you don't 
#   want the fgd metadata files, omit that from the list
exts = ['tif', 'tfw', 'fgd']
# the root URL of the download site
url = 'http://www.archive.org/download/'
# location we want to move the drgs to after download, change to 
#   your liking
home = 'C:/temp/quads/'
# iterate through the quads in quads list
for quad in quads:
    # iterate through extension types
    for ext in exts:
        # build the URL string we will pass to wget
        fullurl = url + 'usgs_drg_' + quad[2] + \
        '_' + quad[0][:5] + '_' + quad[0][5:] + \
        '/o' + quad[0] + '.' + ext
        # pass URL to wget - note we print out to a log 
        #   file as well - see wget docs for full set
        #   of commands you can pass to wget
        os.system('wget %s -o log.log' % (fullurl))
        # Move and rename --> AR_ELKINS_o35094h3.tif
        shutil.move(wgetDir + quad[0] + '.' + ext, 
            home + quad[2].upper() + '_' + \
            quad[1].replace(' ','_') + \
            '_' + 'o' + quad[0] + '.' + ext)