from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import cgi
import json
import ssl
import urllib
import os

hostName = "r3c0d3r.mooo.com"
serverPort = 3000
from tablegen import GenerateTable


class MyServer(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.clients = []

    def do_GET(self):
        # return src/collect.js if path is /collect.js
        if self.path == "/collect.js":
            self.send_response(200)
            self.send_header("content-type", "text/javascript; charset=utf-8\r\n")
            self.end_headers()
            with open("src/collect.js", "rb") as file:
                self.wfile.write(file.read())
        # image path
        elif self.path.startswith("/output/") or self.path.startswith("/medal/"):
            print(self.path)
            self.send_response(200)
            self.send_header("content-type", "image/png")
            self.end_headers()
            # Send image
            with open(self.path[1:], "rb") as file:
                self.wfile.write(file.read())
        else:
            self.send_response(200)
            self.send_header("content-type", "text/html; charset=utf-8\r\n")
            self.end_headers()
            self.wfile.write(bytes("<html><head><title>개인 팝픈뮤직 도표</title></head>", "utf-8"))
            self.wfile.write(bytes("<h1>개인 팝픈뮤직 도표</h1>", "utf-8"))
            # element로 "자신의 데이터를 넣은 레벨별 팝픈뮤직 도표를 생성합니다."
            self.wfile.write(bytes('<p>자신의 데이터를 넣은 레벨별 팝픈뮤직 도표를 생성합니다.</p>', "utf-8"))
            self.wfile.write(bytes('<p>문의 : <a href="x.com/r3c0d3r">@r3c0d3r</a> / 디스코드 @r3c0d3r</p>' , "utf-8"))
            # add button
            self.wfile.write(bytes('<h2>사용 방법</h2>', "utf-8"))
            self.wfile.write(bytes('<p>0. 베이직 코스 가입이 필요합니다.</p>', "utf-8"))
            self.wfile.write(bytes('<p>1. <a href="https://p.eagate.573.jp/gate/p/mypage/index.html">코나미 페이지</a>에 로그인 해 주세요.</p>', "utf-8"))
            self.wfile.write(bytes('<p>2. 개발자 도구 (크롬 기준 F12)를 누른 뒤, Console에 아래 내용을 복사-붙여넣기 후 엔터를 눌러 주세요.</p>', "utf-8"))
            self.wfile.write(bytes('<p>2-a. 페이지가 안전하지 않다거나 전송되는 데이터가 안전하지 않다는 메세지는 제가 이 서버 인증서 받기 귀찮아서 그런거니, 대충 진행해 주세요.</p>', "utf-8"))
            self.wfile.write(bytes("<p>javascript:(()=>{const d=new Date();const s=document.createElement('script');s.src='https://r3c0d3r.mooo.com:3000/collect.js';document.head.appendChild(s);})();", "utf-8"))
            self.wfile.write(bytes("<p>본 기능을 사용하는 것으로 버그 분석 및 통계를 위해 다음과 같은 정보가 수집되는 것에 동의하는 것으로 간주합니다.<br>p.eagate.573.jp를 통해 수집되는 플레이어명, 팝토모 ID, 사용 캐릭터명, 플레이 횟수, 최종 플레이 일시, 악곡 데이터</p>", "utf-8"))
            self.wfile.write(bytes("<h2>데이터 등록한 적 있는 경우</h2>", "utf-8"))
            self.wfile.write(bytes('<p>갱신 없이 표만 뽑으려면, 아래에 팝토모 아이디를 "-"까지 정확히 입력후 입력을 누르세요.</p>', "utf-8"))
            form_txt = '<form action="/submit" method="post">'
            form_txt += '<label for="datalist">팝토모 아이디: </label>'
            form_txt += '<input type="text" id="datalist" name="datalist" required><br>'
            form_txt += '<input type="submit" value="제출">'
            form_txt += '</form>'
            self.wfile.write(bytes(form_txt, "utf-8"))

    
    def do_POST(self):
        if self.path == "/submit":
            form = cgi.FieldStorage(
                fp=self.rfile, 
                headers=self.headers,
                encoding='utf-8',
                environ={'REQUEST_METHOD':'POST',
                         'CONTENT_TYPE':self.headers['Content-Type'],
                         })
            # get datalist using utf-8
            # TODO: 
            flag_detected = False
            try:
                userdata = form.getvalue("datalist")
                userdata = urllib.parse.unquote(userdata)
                userdata = json.loads(userdata)
                print("Detected User:", userdata['profile'][0])
                # Save data to userdata/{userdata['profile'][1]}.json
                with open(f"userdata/{userdata['profile'][1]}.json", "w", encoding='utf-8') as file:
                    file.write(json.dumps(userdata))
                flag_detected = True
            except:
                userdata = form.getvalue("datalist").replace('"', "")
                # find json from /userdata/{userdata}.json
                if os.path.exists(f"userdata/{userdata}.json"):
                    with open(f"userdata/{userdata}.json", "r", encoding='utf-8') as file:
                        userdata = file.read()
                        userdata = json.loads(userdata)
                        print("Detected User:", userdata['profile'][0])
                        flag_detected = True
                else:
                    print("Detected User: Unknown (NOT FOUND)")

            # Print response
            self.send_response(200)
            self.send_header("content-type", "text/html; charset=utf-8\r\n")
            self.end_headers()
            self.wfile.write(bytes("<html><head><title>개인 팝픈뮤직 도표</title></head>", "utf-8"))
            self.wfile.write(bytes("<h1>개인 팝픈뮤직 도표</h1>", "utf-8"))
            self.wfile.write(bytes("<p>자신의 데이터를 넣은 레벨별 팝픈뮤직 도표를 생성합니다.</p>", "utf-8"))
            self.wfile.write(bytes("<p>문의 : <a href='x.com/r3c0d3r'>@r3c0d3r</a> / 디스코드 @r3c0d3r</p>", "utf-8"))
            if flag_detected:
                self.wfile.write(bytes(f"<p>입력된 유저 데이터: {userdata['profile'][0]} (팝토모 ID: {userdata['profile'][1]})</p>", "utf-8"))
                ff = userdata['profile'][6].replace('時頃','시')
                data_count = len(userdata['scores'])
                self.wfile.write(bytes(f"<p>최종 플레이 일시: {ff}, 채보 데이터 수: {data_count}</p>", "utf-8"))
                self.wfile.write(bytes(f"<p>유저 데이터를 정상적으로 불러왔습니다.</p>", "utf-8"))
                self.wfile.write(bytes(f"<h2>도표 설정</h2>", "utf-8"))
                form_txt = '<form action="/table" method="post">'
                form_txt += '<h3>기본 설정</h3>'
                form_txt += '<label for="level0">레벨: </label>'
                # form_txt += '41<input type="radio" id="level41" name="level" value="41" required> / '
                # form_txt += '42<input type="radio" id="level42" name="level" value="42" required> / '
                # form_txt += '43<input type="radio" id="level43" name="level" value="43" required> / '
                # form_txt += '44<input type="radio" id="level44" name="level" value="44" required> / '
                form_txt += '45<input type="radio" id="level45" name="level" value="45" required> / '
                form_txt += '46<input type="radio" id="level46(이미지 미완)" name="level" checked="checked" value="46" required> / '
                form_txt += '47<input type="radio" id="level47(이미지 미완)" name="level" value="47" required> / '
                form_txt += '48<input type="radio" id="level48" name="level" value="48" required> / '
                form_txt += '49<input type="radio" id="level49" name="level" value="49" required> / '
                form_txt += '50<input type="radio" id="level50" name="level" value="50" required> <br><br> '
                
                form_txt += '<label for="row">줄 너비 (모바일:4, 기타:8~12): </label>'
                form_txt += '<input type="range" id="row" value="4" min="4" max="14" name="row" oninput="this.nextElementSibling.value = this.value">  '
                form_txt += '<output>4</output><br><br>'

                form_txt += '<label for="diffkr0">사용 난이도표 (45 이하는 팝픈위키만 가능합니다):   </label>'
                form_txt += '팝픈위키 서열값<input type="radio" name="diffkr" id="diffkr0" value="false" checked="checked" required> / '
                form_txt += '한국 서열표<input type="radio" name="diffkr" id="diffkr1" value="true" required>  <br><br>'

                form_txt += '<label for="info0">플레이 수, 팝토모 아이디 표시:   </label>'
                form_txt += '표시 안함<input type="radio" name="info" id="info0" value="false" required> / '
                form_txt += '정보 표시<input type="radio" name="info" id="info1" value="true" checked="checked" required>  <br><br>'

                form_txt += '<label for="labelkr0">곡 표시제목:   </label>'
                form_txt += '일본어 원문<input type="radio" name="labelkr" id="labelkr0" value="false" required> / '
                form_txt += '한국어 곡명(별명)<input type="radio" name="labelkr" id="labelkr1" value="true" checked="checked" required>  <br>'

                form_txt += '<h3>필터 설정</h3>'
                
                form_txt += '필터를 적용할 경우, 설정된 메달/점수/랭크보다 높은 것에 적용됩니다. <br>'
                form_txt += '메달/점수/랭크 필터 중 하나만 적용하는 것을 추천합니다. <br><br>'

                form_txt += '<label for="filter0">필터 방법:   </label>'
                form_txt += '필터 없음<input type="radio" name="filter" id="filter0" value="none" checked="checked" required> / '
                form_txt += '필터 어둡게<input type="radio" name="filter" id="filter1" value="darken" required> / '
                form_txt += '도표에서 제거<input type="radio" name="filter" id="filter2" value="disable" required>  <br><br>'

                form_txt += '<label for="fmedal00">메달 필터: </label>'
                form_txt += '없음<input type="radio" id="fmedal00" name="fmedal" checked="checked" value="0" required> / '
                form_txt += '<img src="/medal/1.png" width="20px"><input type="radio" id="fmedal01" name="fmedal" value="1" required> / '
                form_txt += '<img src="/medal/2.png" width="20px"><input type="radio" id="fmedal02" name="fmedal" value="2" required> / '
                form_txt += '<img src="/medal/3.png" width="20px"><input type="radio" id="fmedal03" name="fmedal" value="3" required> / '
                form_txt += '<img src="/medal/4.png" width="20px"><input type="radio" id="fmedal04" name="fmedal" value="4" required> / '
                form_txt += '<img src="/medal/5.png" width="20px"><input type="radio" id="fmedal05" name="fmedal" value="5" required> / '
                form_txt += '<img src="/medal/6.png" width="20px"><input type="radio" id="fmedal06" name="fmedal" value="6" required> / '
                form_txt += '<img src="/medal/7.png" width="20px"><input type="radio" id="fmedal07" name="fmedal" value="7" required> / '
                form_txt += '<img src="/medal/8.png" width="20px"><input type="radio" id="fmedal08" name="fmedal" value="8" required> / '
                form_txt += '<img src="/medal/9.png" width="20px"><input type="radio" id="fmedal09" name="fmedal" value="9" required> / '
                form_txt += '<img src="/medal/10.png" width="20px"><input type="radio" id="fmedal10" name="fmedal" value="10" required> / '
                form_txt += '<img src="/medal/11.png" width="20px"><input type="radio" id="fmedal11" name="fmedal" value="11" required> / '
                form_txt += '<img src="/medal/12.png" width="20px"><input type="radio" id="fmedal12" name="fmedal" value="12" required>  <br><br>'
                
                form_txt += '<label for="frank0">랭크 필터: </label>'
                form_txt += '없음<input type="radio" id="frank0" name="frank" checked="checked" value="0" required> / '
                form_txt += 'S<input type="radio" id="frank1" name="frank" value="1" required> / '
                form_txt += 'AAA<input type="radio" id="frank2" name="frank" value="2" required> / '
                form_txt += 'AA<input type="radio" id="frank3" name="frank" value="3" required> / '
                form_txt += 'A<input type="radio" id="frank4" name="frank" value="4" required> / '
                form_txt += 'B<input type="radio" id="frank5" name="frank" value="5" required> / '
                form_txt += 'C<input type="radio" id="frank6" name="frank" value="6" required> / '
                form_txt += 'D<input type="radio" id="frank7" name="frank" value="7" required> / '
                form_txt += 'E<input type="radio" id="frank8" name="frank" value="8" required> <br><br> '
                
                form_txt += '<label for="fscore">점수 필터 (0=없음): </label>'
                form_txt += '<input type="number" id="fscore" name="fscore" value="0" min="0" max="100000" required>  <br><br>'

                form_txt += f'<input type="hidden" id="tomoID" name="tomoID" value="{userdata["profile"][1]}">'

                form_txt += '<input type="submit" value="표 출력 (15초 정도 걸립니다)">'
                form_txt += '</form>'
                self.wfile.write(bytes(form_txt, "utf-8"))

            else:
                self.wfile.write(bytes(f"<p>유저 데이터를 정상적으로 불러오지 못했습니다.</p>", "utf-8"))
                # go front button
                self.wfile.write(bytes('<form action="/" method="get">', "utf-8"))
                self.wfile.write(bytes('<input type="submit" value="돌아가기">', "utf-8"))
                self.wfile.write(bytes('</form>', "utf-8"))
                
        elif self.path == "/table":
            form = cgi.FieldStorage(
                fp=self.rfile, 
                headers=self.headers,
                encoding='utf-8',
                environ={'REQUEST_METHOD':'POST',
                         'CONTENT_TYPE':self.headers['Content-Type'],
                         })
            # get datalist using utf-8
            diffkr = True if form.getvalue('diffkr') == "true" else False
            info = True if form.getvalue('info') == "true" else False
            labelkr = True if form.getvalue('labelkr') == "true" else False
            pth = GenerateTable(form.getvalue("tomoID"), int(form.getvalue('level')), int(form.getvalue('row')), form.getvalue('filter'), int(form.getvalue('fmedal')), int(form.getvalue('fscore')), int(form.getvalue('frank')), form.getvalue('tomoID'), diffkr, info, labelkr)
            print("Generated Table at ", pth)
            print(f"tomoID: {form.getvalue('tomoID')}, level: {form.getvalue('level')}, row: {form.getvalue('row')}, filter: {form.getvalue('filter')}, fmedal: {form.getvalue('fmedal')}, fscore: {form.getvalue('fscore')}, frank: {form.getvalue('frank')}, diffkr: {diffkr}, info: {info}, labelkr: {labelkr}")
            self.send_response(200)
            self.send_header("content-type", "text/html; charset=utf-8\r\n")
            self.end_headers()

            self.wfile.write(bytes("<html><head><title>개인 팝픈뮤직 도표</title></head>", "utf-8"))
            # Go to front
            self.wfile.write(bytes('<form action="/" method="get">', "utf-8"))
            self.wfile.write(bytes('<input type="submit" value="처음으로 돌아가기">', "utf-8"))
            self.wfile.write(bytes('</form>', "utf-8"))
            # Go to previous with tomoID
            self.wfile.write(bytes('<form action="/submit" method="post">', "utf-8"))
            self.wfile.write(bytes(f'<input type="hidden" id="datalist" name="datalist" value="{form.getvalue("tomoID")}">', "utf-8"))
            self.wfile.write(bytes('<input type="submit" value="새로운 테이블 생성">', "utf-8"))
            self.wfile.write(bytes('</form>', "utf-8"))
            # show output/5819-4008-9041_L49_C5_kr
            self.wfile.write(bytes("<h1>개인 팝픈뮤직 도표</h1>", "utf-8"))
            self.wfile.write(bytes(f"<img src='/output/{form.getvalue('tomoID')}.png' alt='도표' width='100%'>", "utf-8"))
        else:
            self.send_response(200)
            self.send_header
    
if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    sslctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    sslctx.check_hostname = False
    sslctx.load_cert_chain(certfile='certificate.crt', keyfile="private.key")
    webServer.socket = sslctx.wrap_socket(webServer.socket, server_side=True)
    print("Server started https://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")