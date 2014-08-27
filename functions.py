import MySQLdb, sys, os, json, ConfigParser
from collections import OrderedDict

class Query():
    """ A class for making repeatable MySQL queries """

    def __init__(self):

        c=ConfigParser.ConfigParser()
        c.read('db.cfg')
        self.db_name=c.get('MySQL','db_name')
        self.db_user=c.get('MySQL','db_user')
        self.db_pass=c.get('MySQL','db_pass')
        self.db_host=c.get('MySQL','db_host')

    def execute(self,statement):
        try:
            conn = MySQLdb.connect(self.db_host,self.db_user,self.db_pass,self.db_name)
            cursor = conn.cursor()
            cursor.execute(statement)
            columns = [desc[0] for desc in cursor.description]
            result = []
            for r in cursor.fetchall():
                row = OrderedDict(zip(columns, r))
                result.append(row)
            cursor.close()
            conn.close()
            return json.dumps(result)
        except MySQLdb.Error, e:

            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)

    def execute_raw(self,statement):
        try:
            conn = MySQLdb.connect(self.db_host,self.db_user,self.db_pass,self.db_name)
            cursor = conn.cursor()
            cursor.execute(statement)
            columns = [desc[0] for desc in cursor.description]
            result = []
            for r in cursor.fetchall():
                row = dict(zip(columns, r))
                result.append(row)
            cursor.close()
            conn.close()
            return result
        except MySQLdb.Error, e:

            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)