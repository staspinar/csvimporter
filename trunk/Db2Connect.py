import ceODBC
db = ceODBC.connect('DSN=dsn;UID=uid;PWD=pwd')
c = db.cursor()
c.execute('SELECT wellname FROM wells')
for each in c.fetchmany(3):
    print each