# import ceODBC module, get it from
#   http://ceodbc.sourceforge.net/
import ceODBC
# connect to your database using your DSN and credentials
#   this method uses your Windows credentials, an option available
#   when setting up your dsn
db = ceODBC.connect('DSN=Wells')
# create a cursor object
c = db.cursor()
# execute your sql on cursor object
c.execute('SELECT wellname, slat, slon FROM wells WHERE wellid IN (1,2,3)')
# iterate through your resultset and print to stdout
#   this method uses fetchall() since we know we are
#   only getting back 3 wells
for each in c.fetchall():
    print each