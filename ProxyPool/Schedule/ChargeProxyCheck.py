# -*- coding: utf-8 -*-



from threading import Thread

try:
    from Queue import Queue, Empty  # py2
except:
    from queue import Queue, Empty  # py3

from Util import LogHandler
from Util.MyIP import getMyIP
from Manager import ProxyManager
from ProxyHelper import Proxy,checkChargeProxyUseful

FAIL_COUNT = 0


class ChargeProxyCheck(ProxyManager, Thread):
    def __init__(self, queue, thread_name):
        ProxyManager.__init__(self)
        Thread.__init__(self, name=thread_name)
        self.queue = queue
        self.log = LogHandler('charge_proxy_check')

    def run(self):
        self.log.info("ChargeProxyCheck - {}  : start".format(self.name))
        self.db.changeTable(self.charge_proxy_queue)
        while True:
            try:
                proxy_str = self.queue.get(block=False)
            except Empty:
                self.log.info("ChargeProxyCheck - {}  : exit".format(self.name))
                break

            proxy_obj = Proxy.newProxyFromJson(proxy_str)
            proxy_obj, status = checkChargeProxyUseful(proxy_obj,self.myIP)
            if status or proxy_obj.fail_count < FAIL_COUNT:
                self.db.put(proxy_obj)
                self.log.info('ChargeProxyCheck - {}  : {} validation Pass ******'.format(self.name,
                                                                                   proxy_obj.proxy.ljust(20)))
            else:
                self.log.info('ChargeProxyCheck - {}  : {} validation Fail ---'.format(self.name,
                                                                                   proxy_obj.proxy.ljust(20)))
                self.db.delete(proxy_obj.proxy)
            self.queue.task_done()


def doChargeProxyCheck():
    proxy_queue = Queue()

    pm = ProxyManager()
    pm.db.changeTable(pm.charge_proxy_queue)
    for _proxy in pm.db.getAll():
        proxy_queue.put(_proxy)

    thread_list = list()
    for index in range(3):
        thread_list.append(ChargeProxyCheck(proxy_queue, "thread_%s" % index))

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()


if __name__ == '__main__':
    doChargeProxyCheck()
