import ceODBC
db = ceODBC.connect('DSN=Wells')
c = db.cursor()
c.execute('SELECT wellname, slat, slon FROM wells WHERE wellid IN (1,2,3)')
for each in c.fetchall():
    print each