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
import pymysql
import copy


class Addon(object):
    def __init__(self, conn):
        self.num = 1
        self.con = conn

    def request(self, flow):
        try:
            header = {}
            cookie2 = {}
            param = {}
            target_domain = "pay.naver.com blog.naver.com cafe.naver.com movie.naver.com shopping.naver.com vibe.naver.com comic.naver.com series.naver.com booking.naver.com papago.naver.com nid.naver.com mail.naver.com apis.naver.com"
            url = ""
            # print(url)
            # print(type(url)) # url 파싱할때 파라미터 없는거랑 대상 도메인 필터링 추가해야함.
            full_url = flow.request.url
            # print(full_url)
            parts = urlparse(full_url)
            # print(parts)
            index = full_url.find("?")
            # if 대상 도메인 and 파라미터존재:
            # print(parts.netloc)
            split_host = (parts.netloc).split(".")
            count = 0
            print(split_host)
            for part_domain in split_host:
                if target_domain.find(part_domain) != 1:
                    count = count + 1
            # print(parts.netloc)
            if count >= 3 and index != -1:
                # print("ssssssssssssssssssssssssss")
                # parsing cookie
                cookie = flow.request.cookies
                for key, value in cookie.items():
                    cookie2[key] = value

                # parsing header
                head = dict(flow.request.headers)
                for key, value in head.items():
                    if key == ":authority":
                        header["authority"] = value
                        continue
                    if key == "Cookie":
                        continue

                    header[key] = value

                # finish cookie2, header

                # url and query parsing and insert xss
                url = full_url[:index]
                # print(url)
                # print(url)
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

                    # print("sexxxxxxxxxxxxxx")
                    # print(res.text)
                    # print(res.status_code)
                    # if (res.status_code) == 200:
                    check = res.text
                    # if key == "inApp":
                    # print(check)
                    # print("sex machine")
                    # print(check.find('siba"lnom'))
                    # print(full_url)
                    if (
                        check.find('siba"lnom') != -1
                        or check.find("'fuckyou") != -1
                        or check.find("<sexn>") != -1
                    ):
                        # print("url ===> " + tmp_url)
                        # print(xss_param)
                        print(f"origin_url ==>{origin_url}")
                        print(f"parameter ==>{key}")
                        print(f"value ==> {xss_param[key]}")
                        # print("씨벨롬")

                        # # print(self.con)
                        # # print(self.cur)
                        # o = "origin_url"
                        # p = "parameter"
                        # # insert_q = (
                        # #     f"insert into xss({o},{p}) values ({origin_url},{xss_param[key]})"
                        # # )
                        # # print(insert_q)
                        try:
                            with self.con.cursor() as cur:
                                sql = "INSERT INTO `xss` (`origin_url`, `parameter`,`value`) VALUES (%s, %s,%s)"
                                cur.execute(sql, (origin_url, key, xss_param[key]))
                            self.con.commit()
                        except Exception as ex:
                            # self.con.close()
                            # print(ex)
                            self.con = pymysql.connect(
                                user="root",
                                passwd="123456",
                                host="127.0.0.1",
                                db="xss",
                                charset="utf8",
                            )
                            with self.con.cursor() as cur:
                                sql = "INSERT INTO `xss` (`origin_url`, `parameter`,`value`) VALUES (%s, %s,%s)"
                                cur.execute(sql, (origin_url, key, xss_param[key]))

                        #     # connection is not autocommit by default. So you must commit to save
                        #     # your changes.
                        #     self.con.commit()
                        #     print(ex)
                        # # ss = self.con.cursor.execute(insert_q)
                        # # print("444444")
                        # # dd = self.con.commit()
                        # # print("2222222")

                    xss_param[key] = tmp_parameter[key]
        except Exception as ex:
            print("==========")
            print(ex)
            pass

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
    try:
        conn = pymysql.connect(
            user="root", passwd="123456", host="127.0.0.1", db="xss", charset="utf8"
        )

        # conn.commit()
        options = Options(listen_host="0.0.0.0", listen_port=8080, http2=True)
        m = DumpMaster(options, with_termlog=False, with_dumper=False)
        config = ProxyConfig(options)
        m.server = ProxyServer(config)
        colorama.init()
        # time.sleep(10)
        test = 1
        # m.addons.add(Addon(conn))
        m.addons.add(Addon(conn))

        # m.addons.add(TermLog("log"))

        # run mitmproxy in backgroud, especially integrated with other server
        loop = asyncio.get_event_loop()
        t = threading.Thread(target=loop_in_thread, args=(loop, m))
        t.start()
        # cursor.close()
        conn.close()
        print("hello")

        # Other servers might be started too.
        # time.sleep(20)
        print("going to shutdown mitmproxy")
        # with open("sample", 'a+') as outfile:
        #         json.dump(data, outfile)
        m.shutdown()
    except Exception as e:
        print("--------------")
        print(e)
