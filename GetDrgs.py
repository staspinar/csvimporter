import os, shutil
wgetDir = 'C:/Program Files/wget/o'
quads = [['36094a1','ELKINS','ar'],['36094a2','FAYETTEVILLE','ar']]
exts = ['tif', 'tfw', 'fgd']
url = 'http://www.archive.org/download/'
home = 'C:/temp/quads/'
for quad in quads:
    for ext in exts:
        fullurl = url + 'usgs_drg_' + quad[2] + \
        '_' + quad[0][:5] + '_' + quad[0][5:] + \
        '/o' + quad[0] + '.' + ext
        os.system('wget %s -o log.log' % (fullurl))
        # Move and rename --> AR_ELKINS_o35094h3.tif
        shutil.move(wgetDir + quad[0] + '.' + ext, 
            home + quad[2].upper() + '_' + \
            quad[1].replace(' ','_') + \
            '_' + 'o' + quad[0] + '.' + ext)