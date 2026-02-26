# Instrucțiuni pentru AI: Proiect Robot SPIKE Prime

## Context Proiect
Acest proiect constă într-un robot LEGO SPIKE Prime care detectează obstacole și comunică prin Bluetooth Serial cu o aplicație Flask web.

## Arhitectură Sistem

### 1. Robot SPIKE Prime (SPIKE/spike.py)
- **Hardware**: LEGO SPIKE Prime Hub OS 1.8.149
- **Limbaj**: MicroPython cu API modern `runloop`
- **Porturi**:
  - Port C: Distance Sensor (UltrasonicSensor)
  - Port A: Motor stânga (237°)
  - Port E: Motor dreapta (181°)

### 2. Aplicație Web (robot_detector/alert_app.py)
- **Framework**: Flask (Python 3.14.2)
- **Comunicare**: Bluetooth Serial prin `pyserial`
- **Port**: 5000 (http://127.0.0.1:5000)

## Restricții Critice MicroPython

### ❌ NU FOLOSI NICIODATĂ:
```python
# F-strings
message = f"Distanta: {dist}mm"  # ❌ NU MERGE

# time module
import time
time.sleep(1)  # ❌ NU MERGE

# urequests (WiFi/HTTP)
import urequests
urequests.post(url, json=data)  # ❌ NU MERGE
```

### ✅ FOLOSEȘTE ÎNTOTDEAUNA:
```python
# String formatting
message = "Distanta: {}mm".format(dist)  # ✅ CORECT

# Sleep cu runloop
await runloop.sleep_ms(1000)  # ✅ CORECT

# Comunicare prin print (serial)
print("ALARMA:{" + '"type":"' + tip + '"}')  # ✅ CORECT
```

## API Runloop (Modern SPIKE Prime)

### Structură Obligatorie:
```python
import runloop
from hub import light_matrix, sound, port, button
import motor_pair
import distance_sensor

async def main():
    # Tot codul TREBUIE să fie async
    motor_pair.pair(motor_pair.PAIR_1, port.E, port.A)
    await runloop.sleep_ms(1000)

# Pornire program
runloop.run(main())
```

### Funcții Cheie:
- `runloop.sleep_ms(ms)` - Delay async
- `runloop.until(lambda: condition)` - Așteaptă condiție
- `motor_pair.move(PAIR_1, steering, velocity=speed)` - Mișcare
- `distance_sensor.distance(port.C)` - Citire senzor (returnează mm sau -1)

## Configurare Motor Pair

### Pentru Mers ÎNAINTE (IMPORTANT!):
```python
# Ordinea inversată - altfel merge ÎNAPOI!
motor_pair.pair(motor_pair.PAIR_1, MOTOR_DREAPTA, MOTOR_STANGA)
motor_pair.move(motor_pair.PAIR_1, 0, velocity=30)  # steering=0 = drept
```

### Steering:
- `0` = DREPT înainte
- `-100 la -1` = Cotește stânga
- `1 la 100` = Cotește dreapta

## Comunicare Bluetooth Serial

### Pe Robot (spike.py):
```python
# Trimite date JSON formatate ca string
print("ALARMA:{" + '"type":"PIATRA","distance":' + str(45) + "}")
```

### Pe PC (alert_app.py):
```python
# Citește serial și parsează JSON
if line.startswith("ALARMA:"):
    json_str = line.replace("ALARMA:", "")
    data = json.loads(json_str)
```

## Workflow Dezvoltare

### 1. Editare Cod Robot:
- Editează `c:\Users\dimit\OneDrive\Desktop\app\SPIKE\spike.py`
- Respectă restricțiile MicroPython

### 2. Upload pe Robot:
- Deschide SPIKE App Desktop (NU versiunea web!)
- Conectează robot prin USB/Bluetooth
- Butonul **"Upload to Hub"** (NU "Play"!)
- "Play" rulează pe PC și dă erori ImportError

### 3. Rulare Aplicație:
```powershell
cd c:\Users\dimit\OneDrive\Desktop\app\robot_detector
.venv\Scripts\activate
python alert_app.py
```

### 4. Test Robot:
- Conectează robot prin Bluetooth la PC (Windows Settings)
- Pornește aplicația (pasul 3)
- Apasă butonul STÂNGA pe robot pentru start
- Deschide browser: http://127.0.0.1:5000

## Probleme Comune

### "ImportError: no module named 'spike'"
- **Cauză**: Codul rulează pe PC în loc de robot
- **Fix**: Folosește "Upload to Hub" în SPIKE App Desktop

### "Robot merge ÎNAPOI în loc de ÎNAINTE"
- **Cauză**: Ordinea motor_pair.pair() greșită
- **Fix**: `motor_pair.pair(PAIR_1, MOTOR_DREAPTA, MOTOR_STANGA)` (inversează!)

### "Nu primesc alerte în aplicație"
- **Verifică**: Robot conectat Bluetooth în Windows Settings?
- **Verifică**: Aplicația găsește portul COM? (mesaj în terminal)
- **Verifică**: Robotul printează "ALARMA:..." în consolă?

### "False positive - detectează obstacol când nu e nimic"
- **Cauză**: Prag prea mare sau senzor prea sensibil
- **Fix**: Scade `PRAG_OBSTACOL` sau verifică calibrarea senzorului

## Structură Fișiere

```
app/
├── SPIKE/
│   └── spike.py              # Cod robot (runloop async)
└── robot_detector/
    ├── alert_app.py          # Server Flask + Bluetooth Serial
    ├── templates/
    │   └── mobile.html       # UI web (auto-generated)
    ├── requirements.txt
    └── README.md
```

## Comenzi Utile

### Python Environment:
```powershell
# Activare venv
.venv\Scripts\activate

# Instalare dependințe
pip install -r requirements.txt

# Instalare pyserial (Bluetooth)
pip install pyserial
```

### Git:
```powershell
git status
git add .
git commit -m "mesaj"
git push
```

## Note Importante

1. **Întotdeauna testează pe robot** - emularea pe PC NU funcționează
2. **Bluetooth trebuie conectat** - Windows Settings → Devices → Bluetooth
3. **SPIKE App Desktop only** - versiunea web nu poate uploada cod Python
4. **Async/await peste tot** - API-ul runloop e complet asincron
5. **String formatting cu .format()** - f-strings nu există în MicroPython
