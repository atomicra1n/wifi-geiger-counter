import network
import socket
import json
import time

wlan = None
srv = None
geiger_mod = None
hv_mod = None

def connect(ssid, pwd):
    global wlan
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, pwd)
    
    for i in range(10):
        if wlan.isconnected():
            print("connected:", wlan.ifconfig()[0])
            return True
        time.sleep(1)
    
    print("wifi failed")
    return False

def start(geiger, hv, port=80):
    global srv, geiger_mod, hv_mod
    geiger_mod = geiger
    hv_mod = hv
    srv = socket.socket()
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(('0.0.0.0', port))
    srv.listen(1)
    srv.setblocking(False)

def check():
    if not srv:
        return
    try:
        cl, addr = srv.accept()
        req = cl.recv(1024).decode()
        
        if '/api/data' in req:
            data = {
                'cpm': geiger_mod.get_cpm(),
                'usvh': round(geiger_mod.get_usvh(), 4),
                'total': geiger_mod.pulse_count,
                'hv': round(hv_mod.get_voltage(), 0)
            }
            cl.send('HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n')
            cl.send(json.dumps(data))
        else:
            cl.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n')
            cl.send(PAGE)
        cl.close()
    except:
        pass
# got ai help writing the page
PAGE = """<!DOCTYPE html>
<html><head><title>Geiger Counter</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{font-family:sans-serif;max-width:500px;margin:auto;padding:20px;background:#111;color:#eee}
.box{background:#222;border-radius:8px;padding:15px;margin:10px 0}
.big{font-size:2em;color:#0f0}
</style></head><body>
<h2>Geiger Counter</h2>
<div class="box"><small>CPM</small><div class="big" id="cpm">--</div></div>
<div class="box"><small>Dose</small><div class="big" id="dose">--</div><small>uSv/h</small></div>
<div class="box"><small>HV</small><div id="hv">--</div> V</div>
<div class="box"><small>Total counts</small><div id="total">--</div></div>
<script>
setInterval(function(){
fetch('/api/data').then(function(r){return r.json()}).then(function(d){
document.getElementById('cpm').textContent=d.cpm;
document.getElementById('dose').textContent=d.usvh;
document.getElementById('hv').textContent=d.hv;
document.getElementById('total').textContent=d.total;
})},2000);
</script></body></html>"""