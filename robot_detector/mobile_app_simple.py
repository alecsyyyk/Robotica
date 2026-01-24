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

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="2">
    <title>🏺 Robot FLL</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            margin: 0;
        }
        .header { text-align: center; margin-bottom: 30px; }
        .status { 
            background: rgba(76, 175, 80, 0.8); 
            padding: 10px; 
            border-radius: 10px;
            display: inline-block;
        }
        .stats {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: rgba(255,255,255,0.2);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
        }
        .stat-value { font-size: 32px; font-weight: bold; }
        .stat-label { font-size: 12px; opacity: 0.8; }
        .detection {
            background: white;
            color: #333;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 15px;
        }
        .detection-type { font-size: 20px; font-weight: bold; }
        .movila { color: #ff6b6b; }
        .groapa { color: #4ecdc4; }
        .details {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin-top: 10px;
        }
        .detail { 
            background: #f5f5f5; 
            padding: 10px; 
            border-radius: 8px;
            text-align: center;
        }
        .detail-value { font-size: 18px; font-weight: bold; color: #667eea; }
        .detail-label { font-size: 11px; color: #666; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🏺 Robot FLL UNearthed</h1>
        <div class="status">✓ Conectat (Auto-refresh)</div>
    </div>
    
    <div class="stats">
        <div class="stat-card">
            <div class="stat-value">{{ total }}</div>
            <div class="stat-label">TOTAL DETECTĂRI</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{{ last_time }}</div>
            <div class="stat-label">ULTIMA DETECTARE</div>
        </div>
    </div>
    
    <div>
        <h3 style="text-align: center;">📡 Detectări în Timp Real</h3>
        {% if detections %}
            {% for det in detections %}
            <div class="detection">
                <div class="detection-type {{ det.type.lower() }}">
                    {{ '🔺' if det.type == 'MOVILA' else '🕳️' }} {{ det.type }}
                </div>
                <small>{{ det.timestamp }}</small>
                <div class="details">
                    <div class="detail">
                        <div class="detail-value">{{ "%.1f"|format(det.variation) }}</div>
                        <div class="detail-label">Variație (cm)</div>
                    </div>
                    <div class="detail">
                        <div class="detail-value">{{ det.confidence }}%</div>
                        <div class="detail-label">Încredere</div>
                    </div>
                    <div class="detail">
                        <div class="detail-value">{{ "%.1f"|format(det.distance) }}</div>
                        <div class="detail-label">Distanță (cm)</div>
                    </div>
                </div>
            </div>
            {% endfor %}
        {% else %}
            <div style="text-align: center; padding: 40px; opacity: 0.6;">
                🤖 Robot în așteptare...<br>
                <small>Notificările vor apărea aici automat</small>
            </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    last_time = detections[-1]['timestamp'] if detections else '--:--:--'
    return render_template_string(HTML_TEMPLATE, 
                                 detections=list(reversed(detections)), 
                                 total=len(detections),
                                 last_time=last_time)

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
    print("   • http://127.0.0.1:5000 (PC)")
    print("   • http://192.168.0.201:5000 (telefon)")
    print("\n📱 Pagina se reîmprospătează automat la 2 secunde!")
    print("="*70 + "\n")
    
    threading.Thread(target=simulate_robot, daemon=True).start()
    app.run(host='0.0.0.0', port=5000, debug=False)
