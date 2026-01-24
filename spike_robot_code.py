"""
Cod pentru SPIKE Prime - Detectare anomalii și notificări mobile
Copiază acest cod în SPIKE™ Prime App

SETUP:
- Senzor distanță pe portul A
- Motoare pe porturi B și C
- Robotul și PC-ul pe același Wi-Fi
"""

from spike import PrimeHub, DistanceSensor, MotorPair
from math import cos, radians
import urequests
import json
import time

hub = PrimeHub()
distance_sensor = DistanceSensor('A')  # Senzorul pe portul A
motors = MotorPair('B', 'C')  # Motoarele pe B și C

baseline = 15.0  # Distanța medie pe teren plat (cm)
SERVER_IP = "192.168.100.5"  # IP-ul PC-ului (vezi în terminal)
SERVER_PORT = 5000

# Funcție pentru a trimite notificare
def send_notification(anomaly_data):
    try:
        url = f"http://{SERVER_IP}:{SERVER_PORT}/api/notify"
        headers = {'Content-Type': 'application/json'}
        response = urequests.post(url, json=anomaly_data, headers=headers)
        print("✓ Notificare trimisă!")
        response.close()
        return True
    except Exception as e:
        print("✗ Eroare notificare:", e)
        return False

print("🤖 Robot SPIKE Prime pornit!")
print(f"📡 Conectare la: {SERVER_IP}:{SERVER_PORT}")
hub.speaker.beep(60, 0.1)

# Buclă principală de detectare
while True:
    try:
        # Citește senzori
        measured_distance = distance_sensor.get_distance_cm()
        
        if measured_distance is None:
            print("⚠️ Senzor distanță nu răspunde")
            time.sleep(0.5)
            continue
        
        tilt_angle = hub.motion_sensor.get_pitch_angle()
        
        # Compensare înclinare: h = d × cos(θ)
        corrected_distance = measured_distance * cos(radians(abs(tilt_angle)))
        variation = corrected_distance - baseline
        
        print(f"📏 Distanță: {corrected_distance:.1f}cm | Variație: {variation:+.1f}cm")
        
        # Detectare anomalie (prag ±2 cm)
        if abs(variation) > 2.0:
            anomaly_type = 'MOVILA' if variation < 0 else 'GROAPA'
            confidence = min(abs(variation) / 5.0, 1.0)
            
            print(f"🚨 ANOMALIE DETECTATĂ: {anomaly_type}")
            
            # Oprește robotul
            motors.stop()
            
            # Trimite notificare pe telefon
            notification_data = {
                'anomaly_type': anomaly_type,
                'variation': round(variation, 2),
                'corrected_distance': round(corrected_distance, 2),
                'confidence': round(confidence, 2)
            }
            
            if send_notification(notification_data):
                # Feedback vizual și sonor
                hub.light_matrix.write(anomaly_type[0])  # M sau G
                hub.speaker.beep(80, 0.2)
                time.sleep(0.1)
                hub.speaker.beep(60, 0.2)
            
            # Pauză după detectare
            time.sleep(3)
            hub.light_matrix.off()
        
        # Continuă mișcarea
        motors.start(30)  # Viteza 30%
        time.sleep(0.2)
        
    except KeyboardInterrupt:
        print("\n🛑 Oprire robot...")
        motors.stop()
        hub.light_matrix.off()
        break
    except Exception as e:
        print(f"⚠️ Eroare: {e}")
        motors.stop()
        time.sleep(1)

print("👋 Program terminat!")
