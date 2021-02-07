# -*- coding: utf-8 -*-
from mitmproxy.options import Options
from mitmproxy.proxy.config import ProxyConfig
from mitmproxy.proxy.server import ProxyServer
from mitmproxy.tools.dump import DumpMaster
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
import requests
import colorama
import threading
import asyncio
import time
import json
import time


class Addon(object):
    def __init__(self):
        self.num = 1

    def request(self, flow):
        flow.request.headers["count"] = str(self.num)
        url_ = flow.request.url
        method_ = flow.request.method
        arg = flow.request.headers["Referer"]
        terminator = arg.index("?")
        args = arg[terminator + 1 :]
        RED = "\033[31m"  # mode 31 = red forground
        GREEN = "\033[32m"
        GREEN2 = "\033[37m"
        GREEN3 = "\033[36m"

        RESET = "\033[0m"  # mode 0  = reset
        # print(flow.request.headers)
        print(
            RED
            + "[request]"
            + RESET
            + GREEN
            + "["
            + flow.request.method
            + "]"
            + RESET
            + GREEN2
            + "["
            + flow.request.url
            + "]"
            + RESET
        )
        print(RED + "[parameter]" + RESET + GREEN3 + "[" + args + "]" + RESET)
        print(
            "=================================================================================================================================="
        )

        # data['request'].append({
        #     "method":1
        # })
        # data['request'].append({
        #     method_: flow.request.method,
        #     url_: flow.request.url
        # })

    def response(self, flow):
        self.num = self.num + 1
        # flow.response.headers["count"] = str(self.num)
        RED = "\033[34m"  # mode 31 = red forground
        GREEN = "\033[35m"
        # print(flow.response.headers)
        RESET = "\033[0m"  # mode 0  = reset
        print(
            RED
            + "[response : RequestID]"
            + RESET
            + GREEN
            + "["
            + flow.response.headers["x-amzn-RequestId"]
            + "]"
            + RESET
        )

        target = flow.response.text
        # print(target)
        # if ("address-ui-widgets-enterAddressFullName" in target):
        # print(target)

        BLUE = "\033[34m"  # mode 31 = red forground
        CYan = "\033[36m"

        RESET = "\033[0m"  # mode 0  = reset
        # print( BLUE + '[response]' + RESET + CYan+'['+flow.response.method+']'+RESET)
        # print(flow.response.url)
        # print()


# see source mitmproxy/master.py for details
def loop_in_thread(loop, m):
    asyncio.set_event_loop(loop)  # This is the key.
    m.run_loop(loop.run_forever)


if __name__ == "__main__":
    options = Options(listen_host="0.0.0.0", listen_port=8080, http2=True)
    m = DumpMaster(options, with_termlog=False, with_dumper=False)
    config = ProxyConfig(options)
    m.server = ProxyServer(config)
    colorama.init()
    # time.sleep(10)

    m.addons.add(Addon())
    # m.addons.add(TermLog("log"))

    # run mitmproxy in backgroud, especially integrated with other server
    loop = asyncio.get_event_loop()
    t = threading.Thread(target=loop_in_thread, args=(loop, m))
    t.start()
    print('hello')

    # Other servers might be started too.
    time.sleep(20)
    print("going to shutdown mitmproxy")
    # with open("sample", 'a+') as outfile:
    #         json.dump(data, outfile)
    m.shutdown()
