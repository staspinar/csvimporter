# import ceODBC module, get it from
#   http://ceodbc.sourceforge.net/
import ceODBC
# connect to your database using your DSN and credentials
db = ceODBC.connect('DSN=dsn;UID=uid;PWD=pwd')
# create a cursor object
c = db.cursor()
# execute your sql on cursor object
c.execute('SELECT wellname FROM wells')
# iterate through your resultset and print to stdout
#   this method uses fetchmany(),  because fetchall()
#   would print out thousands of records
for each in c.fetchmany(3):
    print each