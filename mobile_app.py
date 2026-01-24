"""
🏺 APLICAȚIE NOTIFICĂRI MOBILE - ROBOT FLL UNEARTH

Aplicație web care rulează pe telefon în browser.
Când robotul detectează o anomalie arheologică, 
primești notificare INSTANT pe telefon!

"""
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
from datetime import datetime
import threading
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fll_unearth_2026'
socketio = SocketIO(app, cors_allowed_origins="*")

# Stocăm detectările în memorie (dispare când oprești aplicația)
detections = []
connected_clients = 0


@app.route('/')
def index():
    """Pagina principală - interfață mobilă"""
    return render_template('mobile.html')


@app.route('/api/status')
def status():
    """Status sistem"""
    return jsonify({
        'status': 'online',
        'total_detections': len(detections),
        'connected_devices': connected_clients,
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/notify', methods=['POST'])
def api_notify():
    """Endpoint pentru robot să trimită notificări"""
    try:
        data = request.get_json()
        detection = notify_anomaly(data)
        return jsonify({'success': True, 'detection': detection}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@socketio.on('connect')
def handle_connect():
    """Când un dispozitiv se conectează"""
    global connected_clients
    connected_clients += 1
    print(f'📱 Dispozitiv conectat! Total: {connected_clients}')
    emit('connection_status', {
        'status': 'connected',
        'message': 'Conectat la robot!'
    })


@socketio.on('disconnect')
def handle_disconnect():
    """Când un dispozitiv se deconectează"""
    global connected_clients
    connected_clients -= 1
    print(f'📱 Dispozitiv deconectat. Total: {connected_clients}')


def notify_anomaly(anomaly_data):
    """
    Trimite notificare pe toate dispozitivele conectate
    Apelează această funcție când robotul detectează ceva!
    """
    detection = {
        'id': len(detections) + 1,
        'timestamp': datetime.now().strftime('%H:%M:%S'),
        'type': anomaly_data['anomaly_type'],
        'variation': anomaly_data['variation'],
        'confidence': int(anomaly_data['confidence'] * 100),
        'distance': anomaly_data['corrected_distance']
    }
    
    detections.append(detection)
    
    # Trimite notificare pe toate telefoanele conectate
    socketio.emit('new_anomaly', detection)
    
    print(f"🚨 DETECTARE #{detection['id']}: {detection['type']} - Trimis pe {connected_clients} dispozitive")
    
    return detection


def simulate_robot():
    """Simulare robot pentru testare - ȘTERGE când conectezi robotul real"""
    time.sleep(5)  # Așteaptă să se conecteze telefoanele
    
    # Simulare detectări
    test_detections = [
        {
            'anomaly_type': 'MOVILA',
            'variation': -2.8,
            'corrected_distance': 12.2,
            'confidence': 0.92
        },
        {
            'anomaly_type': 'GROAPA',
            'variation': 3.5,
            'corrected_distance': 18.5,
            'confidence': 0.87
        },
        {
            'anomaly_type': 'MOVILA',
            'variation': -2.1,
            'corrected_distance': 12.9,
            'confidence': 0.78
        }
    ]
    
    for i, detection in enumerate(test_detections, 1):
        print(f"\n🤖 Robot scanează... (Detectare {i}/{len(test_detections)})")
        time.sleep(8)  # Așteaptă între detectări
        notify_anomaly(detection)


if __name__ == '__main__':
    print("\n" + "="*70)
    print("🏺 SERVER NOTIFICĂRI MOBILE - FLL UNEARTH")
    print("="*70)
    print("\n📱 INSTRUCȚIUNI:")
    print("1. Notează adresa IP afișată mai jos")
    print("2. Pe telefon, deschide browser (Chrome/Safari)")
    print("3. Accesează: http://ADRESA_IP:5000")
    print("4. Lasă aplicația deschisă pe telefon")
    print("5. Când robotul detectează ceva, primești notificare!\n")
    
    # Afișează IP-ul computerului
    import socket
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print(f"🌐 Adresa ta IP: {ip_address}")
    print(f"📱 Pe telefon accesează: http://{ip_address}:5000")
    print("\n" + "="*70 + "\n")
    
    # Pornește simulare robot în background (doar pentru test)
    # COMENTEAZĂ această linie când conectezi robotul real!
    # threading.Thread(target=simulate_robot, daemon=True).start()
    
    # Pornește serverul
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)
