"""
Aplicație web SIMPLĂ pentru notificări
Versiune simplificată fără WebSocket - refresh automat
"""
from flask import Flask, render_template_string
from datetime import datetime
import threading
import time

app = Flask(__name__)

# Detectări în memorie
detections = []

HTML_TEMPLATE = '''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="refresh" content="3">
<title>Robot FLL</title>
<style>
body{font-family:Arial,sans-serif;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:white;padding:15px;margin:0}
.header{text-align:center;margin-bottom:20px}
.status{background:rgba(76,175,80,0.8);padding:10px;border-radius:10px;display:inline-block;margin:10px 0}
.stats{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:20px}
.stat-card{background:rgba(255,255,255,0.2);padding:15px;border-radius:10px;text-align:center}
.stat-value{font-size:28px;font-weight:bold}
.stat-label{font-size:11px;opacity:0.8}
.detection{background:white;color:#333;padding:15px;border-radius:10px;margin-bottom:10px}
.detection-type{font-size:18px;font-weight:bold;margin-bottom:5px}
.movila{color:#ff6b6b}
.groapa{color:#4ecdc4}
.details{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:10px}
.detail{background:#f5f5f5;padding:8px;border-radius:5px;text-align:center}
.detail-value{font-size:16px;font-weight:bold;color:#667eea}
.detail-label{font-size:10px;color:#666}
.btn{background:rgba(255,255,255,0.3);color:white;border:2px solid white;padding:12px 20px;border-radius:8px;font-size:14px;font-weight:bold;margin-top:10px;width:100%;max-width:200px}
</style>
</head>
<body>
<div class="header">
<h1>🏺 Robot FLL</h1>
<div class="status">✓ Conectat</div>
<br>
<button class="btn" onclick="if(confirm('Stergi TOATE detectarile?'))fetch('/reset').then(function(){location.reload()})">🔄 RESETARE</button>
</div>
<div class="stats">
<div class="stat-card"><div class="stat-value">{{ total }}</div><div class="stat-label">TOTAL DETECTARI</div></div>
<div class="stat-card"><div class="stat-value">{{ last_time }}</div><div class="stat-label">ULTIMA DETECTARE</div></div>
</div>
<h3 style="text-align:center">📡 Detectari in Timp Real</h3>
{% if detections %}
{% for det in detections %}
<div class="detection">
<div class="detection-type {{ det.type.lower() }}">{{ '🔺' if det.type == 'MOVILA' else '🕳️' }} {{ det.type }}</div>
<small>{{ det.timestamp }}</small>
<div class="details">
<div class="detail"><div class="detail-value">{{ "%.1f"|format(det.variation) }}</div><div class="detail-label">Variatie (cm)</div></div>
<div class="detail"><div class="detail-value">{{ det.confidence }}%</div><div class="detail-label">Incredere</div></div>
<div class="detail"><div class="detail-value">{{ "%.1f"|format(det.distance) }}</div><div class="detail-label">Distanta (cm)</div></div>
</div>
</div>
{% endfor %}
{% else %}
<div style="text-align:center;padding:40px;opacity:0.6">🤖 Robot in asteptare...<br><small>Notificarile vor aparea aici automat</small></div>
{% endif %}
</body>
</html>'''

@app.route('/')
def index():
    last_time = detections[-1]['timestamp'] if detections else '--:--:--'
    return render_template_string(HTML_TEMPLATE, 
                                 detections=list(reversed(detections)), 
                                 total=len(detections),
                                 last_time=last_time)

@app.route('/reset')
def reset():
    """Resetare detectări"""
    detections.clear()
    print("\n🔄 RESETARE! Toate detectările au fost șterse.")
    return '{"status": "ok", "message": "Detectări resetate!"}', 200

def notify_anomaly(anomaly_data):
    """Adaugă detectare"""
    detection = {
        'id': len(detections) + 1,
        'timestamp': datetime.now().strftime('%H:%M:%S'),
        'type': anomaly_data['anomaly_type'],
        'variation': anomaly_data['variation'],
        'confidence': int(anomaly_data['confidence'] * 100),
        'distance': anomaly_data['corrected_distance']
    }
    detections.append(detection)
    print(f"🚨 DETECTARE #{detection['id']}: {detection['type']}")
    return detection

def simulate_robot():
    """Simulare detectări"""
    time.sleep(5)
    test_detections = [
        {'anomaly_type': 'MOVILA', 'variation': -2.8, 'corrected_distance': 12.2, 'confidence': 0.92},
        {'anomaly_type': 'GROAPA', 'variation': 3.5, 'corrected_distance': 18.5, 'confidence': 0.87},
        {'anomaly_type': 'MOVILA', 'variation': -2.1, 'corrected_distance': 12.9, 'confidence': 0.78}
    ]
    for i, det in enumerate(test_detections, 1):
        print(f"\n🤖 Detectare {i}/{len(test_detections)}")
        time.sleep(8)
        notify_anomaly(det)

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🏺 SERVER NOTIFICĂRI MOBILE - VERSIUNE SIMPLIFICATĂ")
    print("="*70)
    print("\n✅ Accesează în browser:")
    print("   • PC: http://127.0.0.1:5000")
    print("   • TELEFON: http://192.168.0.201:5000")
    print("\n📱 IMPORTANT pentru telefon:")
    print("   1. Conectează telefonul la Wi-Fi-ul ACASĂ")
    print("   2. Deschide browser (Chrome/Safari)")
    print("   3. Scrie EXACT în bara de adrese: 192.168.0.201:5000")
    print("   4. Apasă Enter/Go")
    print("\n🔄 Auto-refresh la 3 secunde | Resetare automată la pornire")
    print("="*70 + "\n")
    
    threading.Thread(target=simulate_robot, daemon=True).start()
    app.run(host='0.0.0.0', port=5000, debug=False)
