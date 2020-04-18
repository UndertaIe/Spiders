
from main.Generator import startCookiePool
from multiprocessing import Value, Queue, Process
from api.cookieAPI import start_cookie_server
from db.DbManager import storeCookie

if __name__ == "__main__":

    CookieCounter = Value('i', 0)
    buffer = Queue()
    p0 = Process(target=start_cookie_server)
    p1 = Process(target=startCookiePool, args=(buffer, CookieCounter))
    p2 = Process(target=storeCookie,args=(buffer,CookieCounter))
    p0.start()
    p1.start()
    p2.start()
    p0.join()
    p1.join()
    p2.join()