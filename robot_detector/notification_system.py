"""
Sistem de notificare pentru arheologi
"""
import time
from datetime import datetime
from typing import List, Dict
import json


class AlertMessage:
    """Mesaj de alertă pentru detectarea artefactelor"""
    
    def __init__(self, artifact_data: dict, robot_name: str):
        self.timestamp = datetime.now()
        self.robot_name = robot_name
        self.artifact_data = artifact_data
        self.alert_id = f"ALERT-{int(time.time() * 1000)}"
    
    def format_message(self) -> str:
        """Formatează mesajul de alertă"""
        return f"""
╔══════════════════════════════════════════════════════════════╗
║              🚨 ALERTĂ ARTEFACT DETECTAT 🚨                  ║
╠══════════════════════════════════════════════════════════════╣
║ ID Alertă:    {self.alert_id:<45} ║
║ Robot:        {self.robot_name:<45} ║
║ Timestamp:    {self.timestamp.strftime('%Y-%m-%d %H:%M:%S'):<45} ║
║                                                              ║
║ DETALII ARTEFACT:                                            ║
║ ├─ Tip:        {self.artifact_data['type']:<43} ║
║ ├─ Distanță:   {self.artifact_data['distance']:<8} m                              ║
║ ├─ Poziție:    X={self.artifact_data['position'][0]:<6}, Y={self.artifact_data['position'][1]:<6}                   ║
║ └─ Confidence: {self.artifact_data['confidence'] * 100:<5}%                                      ║
╚══════════════════════════════════════════════════════════════╝
"""
    
    def to_dict(self) -> dict:
        """Convertește mesajul în dicționar"""
        return {
            'alert_id': self.alert_id,
            'robot_name': self.robot_name,
            'timestamp': self.timestamp.isoformat(),
            'artifact': self.artifact_data
        }


class NotificationSystem:
    """Sistem de notificare pentru arheologi"""
    
    def __init__(self):
        self.archaeologists: List[str] = []
        self.alert_history: List[AlertMessage] = []
        self.log_file = "c:\\Users\\Alexa\\Desktop\\Java\\robot_detector\\detections.log"
    
    def register_archaeologist(self, name: str):
        """Înregistrează un arheolog în sistem"""
        self.archaeologists.append(name)
        print(f"✅ Arheolog înregistrat: {name}")
    
    def send_alert(self, alert: AlertMessage):
        """Trimite alertă către toți arheologii înregistrați"""
        self.alert_history.append(alert)
        
        # Afișare alertă în consolă
        print(alert.format_message())
        
        # Notificare arheologi
        print("📧 Trimitere notificări către arheologi:")
        for archaeologist in self.archaeologists:
            print(f"   → {archaeologist}: Notificare trimisă")
        
        # Salvare în log
        self._save_to_log(alert)
        
        print(f"💾 Alertă salvată în jurnal: {self.log_file}")
        print()
    
    def _save_to_log(self, alert: AlertMessage):
        """Salvează alerta în fișierul de log"""
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(f"{alert.timestamp.isoformat()} | {alert.alert_id} | "
                       f"{alert.robot_name} | {alert.artifact_data['type']} | "
                       f"Poziție: {alert.artifact_data['position']} | "
                       f"Confidence: {alert.artifact_data['confidence']}\n")
        except Exception as e:
            print(f"⚠️ Eroare la salvarea în log: {e}")
    
    def get_alert_count(self) -> int:
        """Returnează numărul total de alerte trimise"""
        return len(self.alert_history)
    
    def get_last_alerts(self, count: int = 5) -> List[AlertMessage]:
        """Returnează ultimele alerte"""
        return self.alert_history[-count:]
    
    def export_alerts_json(self, filename: str = "alerts_export.json"):
        """Exportă toate alertele în format JSON"""
        full_path = f"c:\\Users\\Alexa\\Desktop\\Java\\robot_detector\\{filename}"
        try:
            data = [alert.to_dict() for alert in self.alert_history]
            with open(full_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"📁 Alerte exportate în: {full_path}")
        except Exception as e:
            print(f"⚠️ Eroare la export: {e}")
