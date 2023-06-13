#!/usr/bin/env python2.7.5
# -*- coding: utf-8 -*-
# by k
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json
import threading
import subprocess
import time
import os

host = ('localhost', 80)  # 접속 정보 (수정x)
status = False  # 기본 상태 (수정x)
daemon = ''  # 데몬 정보 입력


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if  self.path == '/robots.txt':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            response = "User-agent: *\nDisallow: /"
            self.wfile.write(response.encode())
        elif self.path == '/':
            self.send_response(401)
            self.end_headers()
        elif self.path == '/API/daemon-status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = json.dumps({'serviceName': '', 'daemonStatus': status})
            self.wfile.write(response.encode())
        else:
            self.send_response(404)
            self.end_headers()


def check_sta_process():
    global daemon
    global status
    while True:
        # 이미 실행중인 프로세스가 있는 경우 또 다시 실행되지 않도록
        # 하기 위해 실행되는 프로세스가 있으면 1, 없으면 0을 반환하도록 함
        statusProc = subprocess.check_output("pgrep -fl {} | wc -l".format(daemon), shell=True)
        print 'Run Command', statusProc

        if int(statusProc) == 0:
            status = False
            os.system(daemon)  # 실행할 데몬
            print '실행되지 아니함'
        else:
            status = True
            print '정상 실행중'
        time.sleep(60)  # 1분 대기


# 스레드를 사용하여 check_sta_process 함수를 백그라운드에서 실행합니다.
process_thread = threading.Thread(target=check_sta_process)
process_thread.start()


def run(server_class=HTTPServer, handler_class=MyHandler):
    server_address = ('', 80)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()
    print '서비스를 시작합니다'


if __name__ == '__main__':
    run()