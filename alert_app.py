"""
Aplicație SUPER SIMPLĂ - primește avertizări prin BLUETOOTH SERIAL
Robotul trimite date prin Bluetooth, aplicația le afișează pe web
"""
from flask import Flask, render_template_string, request, jsonify
from datetime import datetime
import threading
import json
import time

app = Flask(__name__)

# Lista de avertizări primite
alerts = []

# Configurare Bluetooth Serial
BLUETOOTH_PORT = None  # Se va detecta automat sau setezi manual (ex: "COM5")
serial_connection = None

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="2">
    <title>🔔 Avertizări Robot</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            margin: 0;
        }
        .header { text-align: center; margin-bottom: 30px; }
        h1 { font-size: 36px; margin: 10px 0; }
        .count { 
            font-size: 60px; 
            font-weight: bold; 
            text-align: center;
            background: rgba(255,255,255,0.2);
            padding: 30px;
            border-radius: 20px;
            margin: 20px 0;
        }
        .alert-box {
            background: white;
            color: #333;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 15px;
            font-size: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
        .alert-time { 
            font-size: 14px; 
            color: #666; 
            margin-top: 10px;
        }
        .emoji { font-size: 40px; }
        .empty {
            text-align: center;
            padding: 60px 20px;
            opacity: 0.7;
            font-size: 18px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 Sistem Avertizări Robot</h1>
        <p>Pagina se actualizează automat</p>
    </div>
    
    <div class="count">
        {{ total }} avertizări
    </div>
    
    <div>
        {% if alerts %}
            {% for alert in alerts %}
            <div class="alert-box">
                <div class="emoji">🚨</div>
                <strong>S-A GĂSIT CEVA!</strong>
                {% if alert.message %}
                <div style="margin-top: 10px;">{{ alert.message }}</div>
                {% endif %}
                <div class="alert-time">⏰ {{ alert.timestamp }}</div>
            </div>
            {% endfor %}
        {% else %}
            <div class="empty">
                🤖 Robotul lucrează...<br>
                <small>Aștept avertizări</small>
            </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(
        HTML_TEMPLATE, 
        alerts=list(reversed(alerts[-10:])),  # Ultimele 10
        total=len(alerts)
    )

@app.route('/alert', methods=['POST', 'GET'])
def receive_alert():
    """Primește avertizare de la robot"""
    try:
        data = request.json if request.is_json else {}
        message = data.get('message', '')
        
        alert = {
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'message': message
        }
        alerts.append(alert)
        
        print(f"🚨 AVERTIZARE PRIMITĂ! Total: {len(alerts)}")
        return jsonify({'status': 'ok', 'total': len(alerts)})
    except:
        return jsonify({'status': 'ok'})

def citeste_bluetooth():
    """Thread separat care citește date de pe portul serial Bluetooth"""
    global serial_connection
    
    try:
        import serial
        import serial.tools.list_ports
        
        # Caută portul SPIKE Prime Bluetooth
        print("\n🔍 Caut robot SPIKE Prime pe Bluetooth...")
        ports = serial.tools.list_ports.comports()
        
        for port in ports:
            # SPIKE Prime apare ca "Standard Serial over Bluetooth"
            if "Bluetooth" in port.description or "SPIKE" in port.description:
                print(f"✅ Găsit: {port.device} - {port.description}")
                BLUETOOTH_PORT_GASIT = port.device
                
                try:
                    serial_connection = serial.Serial(
                        port=BLUETOOTH_PORT_GASIT,
                        baudrate=115200,
                        timeout=1
                    )
                    print(f"🔗 Conectat la {BLUETOOTH_PORT_GASIT}")
                    break
                except Exception as e:
                    print(f"⚠️ Nu pot conecta la {BLUETOOTH_PORT_GASIT}: {e}")
        
        if not serial_connection:
            print("❌ Nu am găsit robot SPIKE pe Bluetooth")
            print("💡 Asigură-te că robotul este:")
            print("   1. Conectat prin Bluetooth la PC")
            print("   2. Programul rulează pe robot")
            return
        
        # Citește continuu de pe serial
        print("📡 Ascult după alerte de la robot...\n")
        while True:
            try:
                if serial_connection.in_waiting > 0:
                    line = serial_connection.readline().decode('utf-8').strip()
                    
                    # Caută linii care încep cu "ALARMA:"
                    if line.startswith("ALARMA:"):
                        try:
                            # Extrage JSON-ul
                            json_str = line.replace("ALARMA:", "")
                            data = json.loads(json_str)
                            
                            tip = data.get('type', 'OBSTACOL')
                            distanta = data.get('distance', 0)
                            
                            mesaj = f"{tip} la {distanta}mm"
                            
                            alert = {
                                'timestamp': datetime.now().strftime('%H:%M:%S'),
                                'message': mesaj
                            }
                            alerts.append(alert)
                            
                            print(f"🚨 ALERTĂ: {mesaj}")
                        except json.JSONDecodeError:
                            print(f"⚠️ Date invalide: {line}")
                    
            except Exception as e:
                print(f"⚠️ Eroare citire serial: {e}")
                time.sleep(1)
                
    except ImportError:
        print("❌ Modulul 'pyserial' nu este instalat!")
        print("💡 Rulează: pip install pyserial")
    except Exception as e:
        print(f"❌ Eroare Bluetooth: {e}")

if __name__ == '__main__':
    import socket
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    
    print("\n" + "="*70)
    print("🔔 SERVER AVERTIZĂRI PORNIT (BLUETOOTH SERIAL)!")
    print("="*70)
    print(f"\n📱 Pe telefon accesează: http://{ip}:5000")
    print(f"💻 Pe PC accesează: http://127.0.0.1:5000")
    print("\n" + "="*70)
    print("\n📡 Robotul trimite prin Bluetooth Serial")
    print("   (nu mai este nevoie de WiFi!)")
    print("="*70 + "\n")
    
    # Pornește thread-ul pentru citire Bluetooth
    bluetooth_thread = threading.Thread(target=citeste_bluetooth, daemon=True)
    bluetooth_thread.start()
    
    # Așteaptă 2 secunde ca thread-ul să se conecteze
    time.sleep(2)
    
    app.run(host='0.0.0.0', port=5000, debug=False)
