# -*- coding: utf-8 -*-


import sys
from apscheduler.schedulers.blocking import BlockingScheduler

sys.path.append('../')

from Schedule import doRawProxyCheck, doUsefulProxyCheck,doChargeProxyCheck
from Manager import ProxyManager
from Util import LogHandler


class DoFetchProxy(ProxyManager):
    """ fetch proxy"""

    def __init__(self):
        ProxyManager.__init__(self)
        self.log = LogHandler('fetch_proxy')

    def main(self):
        self.log.info("start fetch proxy")
        self.fetch()
        self.log.info("finish fetch proxy")

class DoFetchChargeProxy(ProxyManager):
    """ fetch charge proxy"""

    def __init__(self):
        ProxyManager.__init__(self)
        self.log = LogHandler('fetch_charge_proxy')

    def main(self):
        self.log.info("start fetch charge proxy")
        self.fetchCharge()
        self.log.info("finish fetch charge proxy")

def rawProxyScheduler():
    DoFetchProxy().main()
    doRawProxyCheck()


def usefulProxyScheduler():
    doUsefulProxyCheck()

def chargeProxyFetchScheduler():
    DoFetchChargeProxy().main()

def chargeProxyCheckScheduler():
    doChargeProxyCheck()

def runScheduler():
    rawProxyScheduler()
    usefulProxyScheduler()

    scheduler_log = LogHandler("scheduler_log")
    scheduler = BlockingScheduler(logger=scheduler_log)

    # 可用免费代理检测
    scheduler.add_job(usefulProxyScheduler, 'interval', minutes=2, id="useful_proxy_check", name="useful_proxy定时检查")

    # 调用收费代理API
    scheduler.add_job(chargeProxyFetchScheduler, 'interval', minutes=4, id="charge_proxy_fetch", name="charge_proxy定时采集")

    # 收费代理检测
    scheduler.add_job(chargeProxyCheckScheduler, 'interval', minutes=1, id="charge_proxy_check",name="charge_proxy定时检查")

    # 免费代理采集
    scheduler.add_job(rawProxyScheduler, 'interval', minutes=30, id="raw_proxy_check", name="raw_proxy定时采集")

    scheduler.start()


if __name__ == '__main__':
    runScheduler()
