# 🤖 Sistem de Detectare Artefacte cu Robot

Aplicație Python pentru controlul unui robot echipat cu senzor de detecție a obiectelor, care monitorizează continuu mediul și trimite alerte în timp real către arheologi atunci când detectează artefacte.

## 📋 Caracteristici

- ✅ **Monitorizare în timp real** - Scanare continuă a mediului
- ✅ **Detectare automată** - Identificare evenimente de detectie
- ✅ **Sistem de alertare** - Generare și transmitere mesaje către arheologi
- ✅ **Logging complet** - Salvare toate detectările în fișier log
- ✅ **Export date** - Export alertelor în format JSON
- ✅ **Multi-threading** - Procesare asincronă pentru performanță optimă

## 🏗️ Structura Proiectului

```
robot_detector/
├── robot.py                   # Clasele Robot și Sensor
├── notification_system.py     # Sistem de alertare și notificări
├── detector_app.py           # Aplicația principală
├── README.md                 # Documentație
├── detections.log            # Jurnal detectări (generat automat)
└── alerts_export.json        # Export alertelor (generat automat)
```

## 🚀 Cum se folosește

### Instalare

Nu sunt necesare dependențe externe. Aplicația folosește doar librării standard Python.

### Rulare

```bash
python detector_app.py
```

### Oprire

- Aplicația se oprește automat după 30 secunde
- Sau apăsați `Ctrl+C` pentru oprire manuală

## 🎯 Funcționalități Detaliate

### 1. Robot și Senzor

- **Robot**: Se deplasează autonom în mediu
- **Senzor**: Scanează continuu pentru detectarea obiectelor
- **Poziționare**: Urmărire poziție în coordonate (X, Y)

### 2. Detectare Artefacte

Când senzorul detectează un artefact, aplicația capturează:
- Tipul artefactului (ceramică, monedă, vas, etc.)
- Distanța față de robot
- Poziția exactă
- Nivel de încredere (confidence)
- Timestamp-ul detectării

### 3. Sistem de Notificare

- **Înregistrare arheologi**: Sistem de management al destinatarilor
- **Alerte în timp real**: Notificare imediată la detectare
- **Format vizual**: Mesaje formatate pentru ușurință în citire
- **Persistență**: Salvare automată în fișier log

### 4. Raportare

- Sumar sesiune la final
- Export date în JSON
- Statistici detectări

## 📊 Exemplu Output

```
╔══════════════════════════════════════════════════════════════╗
║              🚨 ALERTĂ ARTEFACT DETECTAT 🚨                  ║
╠══════════════════════════════════════════════════════════════╣
║ ID Alertă:    ALERT-1737676800000                           ║
║ Robot:        ArcheoBot-X1                                   ║
║ Timestamp:    2026-01-14 15:30:00                           ║
║                                                              ║
║ DETALII ARTEFACT:                                            ║
║ ├─ Tip:        monedă romană                                ║
║ ├─ Distanță:   3.45 m                                       ║
║ ├─ Poziție:    X=2.34, Y=-1.56                             ║
║ └─ Confidence: 92.0%                                        ║
╚══════════════════════════════════════════════════════════════╝
```

## ⚙️ Configurare

Pentru a modifica parametrii aplicației, editați fișierul `detector_app.py`:

```python
# Durata rulare (secunde)
app.run(duration=30)

# Interval scanare (secunde)
self.scan_interval = 1.0
```

## 📁 Fișiere Generate

### detections.log
Jurnal text cu toate detectările:
```
2026-01-14T15:30:00 | ALERT-123456 | ArcheoBot-X1 | monedă romană | Poziție: (2.34, -1.56) | Confidence: 0.92
```

### alerts_export.json
Export structurat JSON:
```json
[
  {
    "alert_id": "ALERT-123456",
    "robot_name": "ArcheoBot-X1",
    "timestamp": "2026-01-14T15:30:00",
    "artifact": {
      "type": "monedă romană",
      "distance": 3.45,
      "position": [2.34, -1.56],
      "confidence": 0.92
    }
  }
]
```

## 🔧 Extinderi Posibile

1. **Integrare hardware real** - Conectare la senzori fizici
2. **Notificări email/SMS** - Trimitere alerte prin email sau SMS
3. **Interfață grafică** - Vizualizare harta și poziții în timp real
4. **Bază de date** - Stocare date în PostgreSQL/MySQL
5. **API REST** - Expunere date prin API pentru integrare
6. **Machine Learning** - Clasificare automată tipuri artefacte

## 📝 Licență

Proiect educațional - Utilizare liberă
