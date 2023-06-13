from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import threading
import subprocess
import time
import os 

host = ('localhost', 8000) # 접속 정보 (수정x)
status = False # 기본 상태 (수정x)
daemon = '' # 데몬정보 입력

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = json.dumps({'status': status})
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
        statusProc = subprocess.check_output("pgrep -fl ",daemon,"* | wc -l", shell=True)
        print('Run Command', statusProc)

        if int(statusProc) == 0:
            status = False
            os.system(daemon) # 실행할 데몬
        else:
            status = True
        
        time.sleep(60)  # 1분 대기

# 스레드를 사용하여 check_sta_process 함수를 백그라운드에서 실행합니다.
process_thread = threading.Thread(target=check_sta_process)
process_thread.start()

def run(server_class=HTTPServer, handler_class=MyHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == '__main__':
    run()
