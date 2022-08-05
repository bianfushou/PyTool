from gevent import monkey
monkey.patch_socket()#不能patch_all,这样会没办法用线程池
from concurrent.futures import ProcessPoolExecutor
import time
from gevent import pywsgi
import gevent

from flask import  Flask

app=Flask(__name__)


def con():
    print("start")
    k = 1
    
    for i in range(2000000):
        k = k + i * i
    for i in range(200000000):
        k = k + i * i
    return ("iii"+str(time.time()) + "   "+ str(k))

ik = 0

@app.route('/hello', methods = ['POST', 'GET'])
def hello():
    global ik
    il = ik + 1
    ik = il
    print(il)
    pool = app.config['Pool']
    gs = gevent.spawn(pool.submit, con)
    gs.join()
    res = gs.value
    gp = gevent.spawn(res.result)
    gp.join()
    print('end'+ str(il))
    return 'hello world' + res.result()
   


def serve_forever():
    serve = pywsgi.WSGIServer( ('127.0.0.1', 8020 ), app)
    serve.serve_forever()

if __name__=='__main__':
    epool = ProcessPoolExecutor(max_workers=16)
    app.config['Pool'] = epool
    #app.run(host='0.0.0.0', debug=True, port='8000')
    serve_forever()