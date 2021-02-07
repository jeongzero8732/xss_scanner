# -*- coding: utf-8 -*-
from mitmproxy.options import Options
from mitmproxy.proxy.config import ProxyConfig
from mitmproxy.proxy.server import ProxyServer
from mitmproxy.tools.dump import DumpMaster
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qsl, parse_qs, urlencode, urlunparse
from pprint import pprint as pp
import requests
import colorama
import threading
import asyncio
import time
import json
import time

import copy


class Addon(object):
    def __init__(self):
        self.num = 1

    def request(self, flow):
        # try:
        header = {}
        cookie2 = {}
        param = {}
        target_domain = "pay.naver.com blog.naver.com cafe.naver.com movie.naver.com shopping.naver.com vibe.naver.com comic.naver.com series.naver.com booking.naver.com papago.naver.com nid.naver.com mail.naver.com apis.naver.com"
        url = ""

        full_url = flow.request.url

        parts = urlparse(full_url)

        index = full_url.find("?")

        split_host = (parts.netloc).split(".")
        count = 0

        for part_domain in split_host:

            if part_domain in target_domain:
                count = count + 1

        if count >= 3 and index != -1:
            cookie = flow.request.cookies
            for key, value in cookie.items():
                cookie2[key] = value

            head = dict(flow.request.headers)
            for key, value in head.items():
                if key == ":authority":
                    header["authority"] = value
                    continue
                if key == "Cookie":
                    continue

                header[key] = value

            url = full_url[:index]

            qu = parts.query
            qs = dict(parse_qsl(qu))
            tmp_ = {}
            xss_param = {}

            for key, value in qs.items():
                tmp_[key] = value
                xss_param[key] = value

            tmp_parameter = {}
            tmp_parameter = copy.deepcopy(xss_param)

            for key, value in tmp_.items():
                # pp(tmp_parameter)
                xss_param[key] = "siba\"lnom'fuckyou<sexn>"
                # print("=======================")
                # pp(xss_param)
                origin_url = copy.deepcopy(full_url)
                res = requests.get(url=url, headers=header, cookies=cookie2, params=xss_param)

                check = res.text

                if (
                    check.find('siba"lnom') != -1
                    or check.find("'fuckyou") != -1
                    or check.find("<sexn>") != -1
                ):

                    print(f"origin_url ==>{origin_url}")
                    print(f"parameter ==>{key}")
                    print(f"value ==> {xss_param[key]}")

                xss_param[key] = tmp_parameter[key]
        # except Exception as ex:
        #     print("==========")
        #     print(ex)

    def response(self, flow):
        self.num = self.num + 1
        # flow.response.headers["count"] = str(self.num)
        RED = "\033[34m"  # mode 31 = red forground
        GREEN = "\033[35m"
        # print(flow.response.headers)
        RESET = "\033[0m"  # mode 0  = reset


# see source mitmproxy/master.py for details
def loop_in_thread(loop, m):
    asyncio.set_event_loop(loop)  # This is the key.
    m.run_loop(loop.run_forever)


if __name__ == "__main__":
    # try:
    options = Options(listen_host="0.0.0.0", listen_port=8080, http2=True)
    m = DumpMaster(options, with_termlog=False, with_dumper=False)
    config = ProxyConfig(options)
    m.server = ProxyServer(config)
    colorama.init()

    m.addons.add(Addon())

    loop = asyncio.get_event_loop()
    t = threading.Thread(target=loop_in_thread, args=(loop, m))
    t.start()

    print("hello")

    # Other servers might be started too.
    time.sleep(3000)
    print("going to shutdown mitmproxy")

    m.shutdown()
    # except Exception as e:
    #     print("--------------")
    #     print(e)
