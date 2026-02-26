"""
Aplicație MOBILĂ OPTIMIZATĂ pentru telefon
Versiune ultra-simplă pentru acces de pe telefon
"""
from flask import Flask, render_template_string
from datetime import datetime
import threading
import time

app = Flask(__name__)

# Detectări în memorie
detections = []

HTML_MOBILE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta http-equiv="refresh" content="3">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <title>Robot FLL</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            min-height: 100vh;
        }
        .header { 
            text-align: center; 
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid rgba(255,255,255,0.3);
        }
        h1 { 
            font-size: 24px; 
            margin-bottom: 10px;
        }
        .status { 
            background: rgba(76, 175, 80, 0.9); 
            padding: 8px 15px; 
            border-radius: 20px;
            display: inline-block;
            font-size: 14px;
            margin: 5px 0;
        }
        .reset-btn {
            background: rgba(255,87,34,0.9);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 25px;
            font-size: 16px;
            font-weight: bold;
            margin-top: 10px;
            cursor: pointer;
            width: 100%;
            max-width: 300px;
            -webkit-tap-highlight-color: transparent;
        }
        .reset-btn:active {
            background: rgba(255,87,34,1);
            transform: scale(0.98);
        }
        .stats {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-bottom: 20px;
        }
        .stat-card {
            background: rgba(255,255,255,0.25);
            padding: 15px;
            border-radius: 12px;
            text-align: center;
        }
        .stat-value { 
            font-size: 28px; 
            font-weight: bold;
            line-height: 1;
        }
        .stat-label { 
            font-size: 11px; 
            opacity: 0.9;
            margin-top: 5px;
        }
        .section-title {
            text-align: center;
            font-size: 18px;
            margin-bottom: 15px;
            opacity: 0.95;
        }
        .detection {
            background: white;
            color: #333;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        }
        .detection.first {
            border: 3px solid #ff5722;
            animation: glow 1.5s infinite;
        }
        @keyframes glow {
            0%, 100% { box-shadow: 0 2px 8px rgba(255,87,34,0.4); }
            50% { box-shadow: 0 4px 20px rgba(255,87,34,0.8); }
        }
        .detection-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        .detection-type { 
            font-size: 20px; 
            font-weight: bold;
        }
        .movila { color: #ff6b6b; }
        .groapa { color: #4ecdc4; }
        .timestamp {
            font-size: 12px;
            color: #666;
        }
        .details {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 8px;
            margin-top: 10px;
        }
        .detail { 
            background: #f5f5f5; 
            padding: 8px; 
            border-radius: 8px;
            text-align: center;
        }
        .detail-value { 
            font-size: 16px; 
            font-weight: bold; 
            color: #667eea;
        }
        .detail-label { 
            font-size: 10px; 
            color: #666;
            margin-top: 2px;
        }
        .empty-state {
            text-align: center;
            padding: 60px 20px;
            opacity: 0.7;
        }
        .empty-state .icon {
            font-size: 64px;
            margin-bottom: 15px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🏺 Robot FLL</h1>
        <div class="status">✓ Conectat</div>
        <br>
        <button class="reset-btn" onclick="if(confirm('Ștergi toate detectările?')) { fetch('/reset').then(function(){ location.reload(); }); }">
            🔄 RESETARE
        </button>
        <button class="reset-btn" onclick="fetch('/test').then(function(){ setTimeout(function(){ location.reload(); }, 500); });" style="background: rgba(76, 175, 80, 0.9); margin-top: 10px;">
            🧪 TEST DETECTARE
        </button>
    </div>
    
    <div class="stats">
        <div class="stat-card">
            <div class="stat-value">{{ total }}</div>
            <div class="stat-label">TOTAL</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{{ last_time }}</div>
            <div class="stat-label">ULTIMA</div>
        </div>
    </div>
    
    <div class="section-title">📡 Detectări</div>
    
    {% if detections %}
        {% for det in detections %}
        <div class="detection{{ ' first' if loop.index == 1 else '' }}">
            <div class="detection-header">
                <div class="detection-type {{ det.type.lower() }}">
                    {{ '🔺' if det.type == 'MOVILA' else '🕳️' }} {{ det.type }}
                </div>
                <div class="timestamp">{{ det.timestamp }}</div>
            </div>
            <div class="details">
                <div class="detail">
                    <div class="detail-value">{{ "%.1f"|format(det.variation) }}</div>
                    <div class="detail-label">Variație cm</div>
                </div>
                <div class="detail">
                    <div class="detail-value">{{ det.confidence }}%</div>
                    <div class="detail-label">Încredere</div>
                </div>
                <div class="detail">
                    <div class="detail-value">{{ "%.1f"|format(det.distance) }}</div>
                    <div class="detail-label">Distanță cm</div>
                </div>
            </div>
        </div>
        {% endfor %}
    {% else %}
        <div class="empty-state">
            <div class="icon">🤖</div>
            <div>Robot în așteptare...</div>
            <small>Notificările vor apărea automat</small>
        </div>
    {% endif %}
    
    <script>
        // Vibrează la detectări noi
        (function() {
            var count = {{ total }};
            var lastCount = parseInt(sessionStorage.getItem('lc') || '0');
            if (count > lastCount && lastCount > 0 && navigator.vibrate) {
                navigator.vibrate([200, 100, 200]);
            }
            sessionStorage.setItem('lc', count.toString());
        })();
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    """Pagina principală"""
    import socket
    client_ip = socket.gethostbyname(socket.gethostname())
    print(f"📱 Acces la pagină de la IP: {client_ip}")
    last_time = detections[-1]['timestamp'] if detections else '--:--'
    return render_template_string(HTML_MOBILE, 
                                 detections=list(reversed(detections)), 
                                 total=len(detections),
                                 last_time=last_time)

@app.route('/reset')
def reset():
    """Resetare detectări"""
    detections.clear()
    print("\n🔄 RESETARE! Detectările au fost șterse.")
    return '{"status":"ok"}', 200

@app.route('/test')
def test_detection():
    """Generează o detectare de test instant"""
    import random
    test_types = [
        {'anomaly_type': 'MOVILA', 'variation': -2.5, 'corrected_distance': 12.5, 'confidence': 0.90},
        {'anomaly_type': 'GROAPA', 'variation': 3.2, 'corrected_distance': 15.8, 'confidence': 0.85}
    ]
    test_data = random.choice(test_types)
    notify_anomaly(test_data)
    print("\n✅ Detectare de TEST generată manual!")
    return '{"status":"ok", "message":"Detectare de test adaugata!"}', 200

def notify_anomaly(anomaly_data):
    """Adaugă detectare nouă"""
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
    """Simulare detectări de test"""
    time.sleep(5)
    test_data = [
        {'anomaly_type': 'MOVILA', 'variation': -2.8, 'corrected_distance': 12.2, 'confidence': 0.92},
        {'anomaly_type': 'GROAPA', 'variation': 3.5, 'corrected_distance': 18.5, 'confidence': 0.87},
        {'anomaly_type': 'MOVILA', 'variation': -2.1, 'corrected_distance': 12.9, 'confidence': 0.78}
    ]
    for i, det in enumerate(test_data, 1):
        print(f"\n🤖 Detectare {i}/{len(test_data)}")
        time.sleep(10)
        notify_anomaly(det)

if __name__ == '__main__':
    print("\n" + "="*70)
    print("📱 SERVER APLICAȚIE MOBILĂ - OPTIMIZAT PENTRU TELEFON")
    print("="*70)
    print("\n✅ TELEFON - Accesează:")
    print("   http://192.168.0.201:5001")
    print("\n✅ PC - Accesează:")
    print("   http://127.0.0.1:5001")
    print("\n📱 Caracteristici:")
    print("   • Design simplu și rapid pentru telefon")
    print("   • Auto-refresh la 3 secunde")
    print("   • Vibrație la detectări noi")
    print("   • Buton resetare mare pentru deget")
    print("   • Port 5001 (diferit de versiunea PC)")
    print("\n🔄 Lista pornește goală")
    print("="*70 + "\n")
    
    threading.Thread(target=simulate_robot, daemon=True).start()
    app.run(host='0.0.0.0', port=5001, debug=False)
