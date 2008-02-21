import csv, arcgisscripting, time

gp = arcgisscripting.create()

def KillObject( object ):
    """ Kills an input object """
    if gp.Exists(object):
        gp.Delete_management(object)

def CreateGdbTable( db, table, fields ):
	"""	Creates an empty standalone GDB table and adds fields provided in a list - with a set schema """
	KillObject(db + '/' + table)
	gp.CreateTable(db, table)
	for field in fields:
		if field[1] == 'TEXT':
			gp.AddField_management(db + '/' + table,field[0],field[1],'#','#',field[2],field[3],'NULLABLE','NON_REQUIRED','#')
		else:
			gp.AddField_management(db + '/' + table,field[0],field[1],'#','#','#',field[3],'NULLABLE','NON_REQUIRED','#')

def AddUpdatedDate( inFc ):
    """ Adds the current date of which processing is occuring to the 'UPDATED' field in the input FC. """
    gpDate = time.strftime('"%m/%d/%Y %I:%M %p"', time.localtime())
    gp.AddField_management(inFc, 'UPDATED', 'DATE', '#', '#', '#', 'Time Updated', 'NULLABLE', 'NON_REQUIRED', '#')
    gp.CalculateField_management(inFc, 'UPDATED', gpDate)
    
# ------ GET TO WORK ------ #

fields = [['LAT','DOUBLE','0','Latitude'],
          ['LON','DOUBLE','0','Longitude'],
          ['API','TEXT','20','API Number'],
          ['WELLTYCODE','TEXT','10','IHS Well Type Code'],
          ['PRODUCT','TEXT','10','Product Type']]
            
CreateGdbTable( 'C:/Testing/pug.gdb', 'pug', fields )

rows = gp.InsertCursor('C:/Testing/pug.gdb/pug')
file = open('C:/Testing/pug/wells.csv','rb')
reader = csv.reader(file)
ln = 0
for line in reader:
    t = 0
    print 'Working on line:',str(ln + 1)
    row = rows.NewRow()
    for field in fields:
        val = line[t].strip()
        row.SetValue(field[0], val)
        t = t + 1
    rows.InsertRow(row)
    ln = ln + 1
    del row
    del t
    del line
del rows

file.close()

gp.MakeXyEventLayer_management('C:/Testing/pug.gdb/pug', 'LON', 'LAT', 'tempXyFc', '')
sr = 'GEOGCS["GCS_North_American_1927",DATUM["D_North_American_1927",SPHEROID["Clarke_1866",6378206.4,294.9786982]],\
      PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'
KillObject( 'C:/Testing/pug.gdb/wells/wells' )
KillObject( 'C:/Testing/pug.gdb/wells' )
gp.CreateFeatureDataset_management('C:/Testing/pug.gdb', 'wells', sr)
gp.CopyFeatures_management('tempXyFc', 'C:/Testing/pug.gdb/wells/wells')
AddUpdatedDate( 'C:/Testing/pug.gdb/wells/wells' )