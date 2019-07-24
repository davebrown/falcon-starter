import falcon
import falcon_cors
from falcon_cors import CORS
import logging
import os
import pyodbc
import sys
import threading

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger('my-service')

def say(*args):
  name = threading.currentThread().name
  if name is None:
    name = '_no-thread-name_'
  suffix = ' '.join([str(e) for e in args])
  logger.info('<%d-%s> %s' % (os.getpid(), name, suffix))
  
class FooResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        say('serving quote - say', 'A', 'B', 'C')
        ret = {
            'sentence': (
                "The quick brown fox "
                "jumped over the lazy dog."
            ),
            'foo': 'Bar'
        }

        resp.media = ret

def dbConn():
  server = os.environ['DB_SERVER']
  database = os.environ['DB_NAME']
  username = os.environ['DB_USER']
  password = os.environ['DB_PASSWORD']
  driver= '{ODBC Driver 17 for SQL Server}'
  return pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)

class StoogeResource:

  def on_get(self, req, resp):
    say('Stooge Get')
    conn = dbConn()
    try:
      cur = conn.cursor()
      cur.execute("SELECT name, funny FROM stooges")
      ret = []
      row = cur.fetchone()
      while row:
        ret.append({ 'name': row[0], 'funny': row[1] })
        row = cur.fetchone()
    finally:
      conn.close()
    resp.media = ret
  
PUBLIC_CORS = CORS(allow_all_origins=True, allow_all_headers=True, allow_all_methods=True)  
api = falcon.API(middleware=[falcon_cors.middleware.CORSMiddleware(PUBLIC_CORS)])
api.add_route('/foo', FooResource())
api.add_route('/stooges', StoogeResource())

