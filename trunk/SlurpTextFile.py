# import modules
import csv, arcgisscripting, time
# instaniate gp object
gp = arcgisscripting.create()

# here we have three functions that we will call later
def KillObject( object ):
    """ Kills an input object """
    if gp.Exists(object):
        gp.Delete_management(object)

def CreateGdbTable( db, table, fields ):
	"""	Creates an empty standalone GDB table and adds fields provided in a list - with a set schema """
	# kill the table, if it exists
	KillObject(db + '/' + table)
	gp.CreateTable(db, table)
	for field in fields:
	    # if its a text field, then set the width as well
		if field[1] == 'TEXT':
			gp.AddField_management(db + '/' + table,field[0],field[1],'#','#',field[2],field[3],'NULLABLE','NON_REQUIRED','#')
		else:
		    # dont have to set the width for fields other than text
			gp.AddField_management(db + '/' + table,field[0],field[1],'#','#','#',field[3],'NULLABLE','NON_REQUIRED','#')

def AddUpdatedDate( inFc ):
    """ Adds the current date of which processing is occuring to the 'UPDATED' field in the input FC. """
    # get the current date/time
    gpDate = time.strftime('"%m/%d/%Y %I:%M %p"', time.localtime())
    # add our 'updated' field
    gp.AddField_management(inFc, 'UPDATED', 'DATE', '#', '#', '#', 'Time Updated', 'NULLABLE', 'NON_REQUIRED', '#')
    # calc the timestamp into the new field
    gp.CalculateField_management(inFc, 'UPDATED', gpDate)
    
# ------ GET TO WORK ------ #

# our fields list where we have [field_name,field_type,field_length,field_alias]
fields = [['LAT','DOUBLE','0','Latitude'],
          ['LON','DOUBLE','0','Longitude'],
          ['API','TEXT','20','API Number'],
          ['WELLTYCODE','TEXT','10','IHS Well Type Code'],
          ['PRODUCT','TEXT','10','Product Type']]

# call function to create the geodb table            
CreateGdbTable( 'C:/Testing/pug.gdb', 'pug', fields )

# create a cursor object on our new table
rows = gp.InsertCursor('C:/Testing/pug.gdb/pug')
# open up the input file
file = open('C:/Testing/pug/wells.csv','rb')
# read the entire file into memory
reader = csv.reader(file)
# start a counter for our line number
ln = 0
# iterate thru the lines in the reader object
for line in reader:
    # start another counter to keep track the position
    #   we are at in the line (an index value)
    t = 0
    # print to stdout what line we are working on
    print 'Working on line:',str(ln + 1)
    # create a new row object
    row = rows.NewRow()
    # iterate thru the fields
    for field in fields:
        # grab the field's value from its indexed position
        #   in the current line (line[t]), strip whitespace
        val = line[t].strip()
        # set the value for the field - grab field[0] since
        #   that is the field name in the list item
        row.SetValue(field[0], val)
        # increment line index counter by one in order to
        #   move to the next data column in input file
        t = t + 1
    # insert the row
    rows.InsertRow(row)
    # increment row counter by one
    ln = ln + 1
    # kill some objects
    del row
    del t
    del line
del rows
# close the input file object
file.close()

# call makexyeventlayer method, pass it the table, x and y fields, and temp layer name
gp.MakeXyEventLayer_management('C:/Testing/pug.gdb/pug', 'LON', 'LAT', 'tempXyFc', '')
# spatial reference - simply copied from a prj file
sr = 'GEOGCS["GCS_North_American_1927",DATUM["D_North_American_1927",SPHEROID["Clarke_1866",6378206.4,294.9786982]],\
      PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'
# kill the featureclass, if it exists
KillObject( 'C:/Testing/pug.gdb/wells/wells' )
# kill the featuredataset, if it exists - have to kill the FC first, or we 
#   cannot kill the FD
KillObject( 'C:/Testing/pug.gdb/wells' )
# create FD
gp.CreateFeatureDataset_management('C:/Testing/pug.gdb', 'wells', sr)
# copy features from temporary layer to a true FC
gp.CopyFeatures_management('tempXyFc', 'C:/Testing/pug.gdb/wells/wells')
# add the updated date/time field and calc the value into it
AddUpdatedDate( 'C:/Testing/pug.gdb/wells/wells' )
# DONE