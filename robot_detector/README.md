# 📱 APLICAȚIE NOTIFICĂRI MOBILE - ROBOT FLL UNEARTH

Aplicație simplă care trimite notificări instant pe telefon când robotul detectează anomalii arheologice.

---

## 📋 CE FACE APLICAȚIA?

Când robotul SPIKE Prime detectează o anomalie pe teren (movilă sau groapă care poate indica un sit arheologic):
- ✅ Trimite notificare INSTANT pe telefon
- ✅ Afișează detalii: tip anomalie, variație, încredere
- ✅ Vibrație și sunet de alertă
- ✅ Poți conecta multiple telefoane simultan

**Tehnologie:** Python Flask + WebSocket (comunicare în timp real)

---

## 🚀 INSTALARE ȘI RULARE

### 1. Instalează bibliotecile
```bash
pip install flask flask-socketio python-socketio
```

### 2. Pornește serverul
```bash
cd robot_detector
python mobile_app.py
```

Va afișa ceva de genul:
```
🌐 Adresa ta IP: 192.168.1.100
📱 Pe telefon accesează: http://192.168.1.100:5000
```

### 3. Conectează telefonul
- Pe telefon, conectează-te la **același Wi-Fi** ca PC-ul
- Deschide **browser** (Chrome/Safari)
- Accesează adresa afișată: `http://192.168.1.100:5000`
- **GATA!** Vei primi notificări automat!

---

## 🤖 CONECTARE ROBOT SPIKE PRIME

### Pas 1: Dezactivează simularea

În fișierul `mobile_app.py`, **comentează linia 114:**
```python
# threading.Thread(target=simulate_robot, daemon=True).start()
```

### Pas 2: Trimite notificări din codul robotului

Când robotul detectează o anomalie, apelează funcția `notify_anomaly()`:

```python
from mobile_app import notify_anomaly

# În codul robotului, când detectezi anomalie:
notify_anomaly({
    'anomaly_type': 'MOVILA',        # sau 'GROAPA'
    'variation': -2.8,                # Variația față de baseline (cm)
    'corrected_distance': 12.2,       # Distanța corectată (cm)
    'confidence': 0.92                # Încredere (0-1)
})
```

### Pas 3: Exemplu cod robot complet

```python
from spike import PrimeHub, DistanceSensor
from math import cos, radians
import sys
sys.path.append('C:/Users/Alexa/Desktop/Java/robot_detector')
from mobile_app import notify_anomaly

hub = PrimeHub()
distance_sensor = DistanceSensor('A')
baseline = 15.0  # Distanța medie pe teren plat (cm)

while True:
    # Citește senzori
    measured_distance = distance_sensor.get_distance_cm()
    tilt_angle = hub.motion_sensor.get_pitch_angle()
    
    # Compensare tilt: h = d × cos(θ)
    corrected_distance = measured_distance * cos(radians(abs(tilt_angle)))
    
    # Calculează variația
    variation = corrected_distance - baseline
    
    # Detectare anomalie (prag ±2 cm)
    if abs(variation) > 2.0:
        anomaly_type = 'MOVILA' if variation < 0 else 'GROAPA'
        confidence = min(abs(variation) / 5.0, 1.0)  # Încredere bazată pe variație
        
        # TRIMITE NOTIFICARE PE TELEFON!
        notify_anomaly({
            'anomaly_type': anomaly_type,
            'variation': variation,
            'corrected_distance': corrected_distance,
            'confidence': confidence
        })
        
        # Oprește robot pentru verificare
        motors.stop()
        time.sleep(3)
```

---

## 📱 CE VEI VEDEA PE TELEFON

Când robotul detectează ceva:

1. **Notificare roșie** în colțul din dreapta sus:
   ```
   🚨 MOVILA DETECTAT!
   ```

2. **Card cu detalii:**
   - 🔺/🕳️ Tip: MOVILA sau GROAPA
   - 📊 Variație: -2.8 cm (față de teren plat)
   - 🎯 Încredere: 92%
   - 📏 Distanță corectată: 12.2 cm

3. **Vibrație telefon** (dacă browser suportă)

4. **Statistici actualizate:**
   - Total detectări
   - Ora ultimei detectări

---

## 🔧 STRUCTURA APLICAȚIEI

```
robot_detector/
├── mobile_app.py          ← Server Python (rulează pe PC)
├── templates/
│   └── mobile.html        ← Interfață web (se deschide pe telefon)
├── requirements.txt       ← Biblioteci necesare
└── README.md             ← Acest fișier
```

---

## ⚠️ IMPORTANT

### Pentru ca telefonul să se conecteze:
- ✅ PC și telefon pe **același Wi-Fi**
- ✅ Notează **IP-ul** afișat de server
- ✅ Permite Python prin **firewall Windows**

### Pentru demo fără robot:
- Lasă linia 114 necomentată - va simula detectări automat
- Perfect pentru testare și prezentare FLL!

---

## 💡 AVANTAJE

| Altă metodă | Aplicația noastră |
|-------------|-------------------|
| Telegram (complică) | Browser simplu |
| Email (întârziere) | Instant (<100ms) |
| SMS (costă) | Gratis (Wi-Fi) |
| JSON files (static) | Live updates |

---

## 🏆 PENTRU PREZENTARE FLL

**Mesaj cheie:**
> "Datorită aplicației noastre, arheologii sunt informați INSTANT 
> când robotul găsește o anomalie arheologică - pot monitoriza 
> de la distanță prin telefon, în timp real!"

**Demo:** Pornește serverul → Conectează telefonul → Arată notificările live!

---

## ❓ PROBLEME FRECVENTE

**Q: Telefonul nu se conectează?**
- Verifică că sunt pe același Wi-Fi
- Rulează Python ca Administrator
- Verifică firewall-ul Windows

**Q: Notificările nu apar?**
- Reîmprospătează pagina pe telefon
- Verifică consolă PC - arată "Dispozitiv conectat!"

**Q: Cum opresc simularea?**
- Comentează linia 114 în `mobile_app.py`

---

**Aplicație simplă, directă și eficientă! 🎉**

