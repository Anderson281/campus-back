from django.db import connection

from core.myLib import pgOperations as pg
from core.myLib.pgOperations import WhereClause

from djangoapi import settings

def getDjangoPg(autoCommit=True)->pg.PgOperations:
    pgc: pg.PgConnection = pg.PgConnection(connection)
    pgo: pg.PgOperations = pg.PgOperations(pgc, autoCommit=autoCommit,global_print_queries=settings.DEBUG)
    return pgo

def getDjangoCursor():
    return connection.cursor()

def getOpenedKnoxSessions(username)->int:
    pgo=getDjangoPg()
    wc=WhereClause('username=%s',[username])
    r=pgo.pgSelect('public.auth_user','id',wc)
    if len(r)==0:
        return 0
    userId=r[0]['id']
    wc = WhereClause('user_id=%s',[userId])
    r=pgo.pgSelect('public.knox_authtoken','count(user_id)',wc,False)
    if len(r)>0:
        os=r[0][0]#user oppened session number
    else:
        os=0
    return os
