"""
Aplicație principală pentru controlul robotului și detectarea artefactelor
"""
import time
import threading
from robot import Robot
from notification_system import NotificationSystem, AlertMessage


class ArtifactDetectorApp:
    """Aplicație de detectare a artefactelor în timp real"""
    
    def __init__(self):
        self.robot = Robot(name="ArcheoBot-X1")
        self.notification_system = NotificationSystem()
        self.is_running = False
        self.scan_interval = 1.0  # secundă între scanări
        self.monitoring_thread = None
    
    def setup(self):
        """Configurează aplicația"""
        print("=" * 70)
        print("  SISTEM DE DETECTARE ARTEFACTE - INIȚIALIZARE")
        print("=" * 70)
        print()
        
        # Înregistrare arheologi
        print("📋 Înregistrare arheologi în sistem:")
        self.notification_system.register_archaeologist("Dr. Elena Popescu")
        self.notification_system.register_archaeologist("Prof. Mihai Ionescu")
        self.notification_system.register_archaeologist("Dr. Ana Dumitrescu")
        print()
    
    def start_monitoring(self):
        """Pornește monitorizarea în timp real"""
        self.is_running = True
        self.robot.start()
        
        print("🚀 START MONITORIZARE ÎN TIMP REAL")
        print(f"⏱️  Interval scanare: {self.scan_interval}s")
        print("=" * 70)
        print()
        
        # Pornire thread de monitorizare
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()
    
    def _monitoring_loop(self):
        """Bucla principală de monitorizare"""
        while self.is_running:
            try:
                # Deplasare robot
                self.robot.move()
                position = self.robot.get_position()
                
                print(f"📍 Poziție robot: X={position[0]}, Y={position[1]} | "
                      f"Artefacte găsite: {self.robot.artifacts_found}", end='\r')
                
                # Detectare obiecte
                artifact_data = self.robot.detect_objects()
                
                # Verificare dacă s-a detectat un artefact
                if artifact_data:
                    self._handle_detection(artifact_data)
                
                # Așteptare până la următoarea scanare
                time.sleep(self.scan_interval)
                
            except Exception as e:
                print(f"\n⚠️ Eroare în bucla de monitorizare: {e}")
    
    def _handle_detection(self, artifact_data: dict):
        """Gestionează detectarea unui artefact"""
        print()  # Linie nouă pentru a afișa alerta clar
        
        # Incrementare contor
        self.robot.artifacts_found += 1
        
        # Creare mesaj de alertă
        alert = AlertMessage(artifact_data, self.robot.name)
        
        # Trimitere notificare
        self.notification_system.send_alert(alert)
    
    def stop_monitoring(self):
        """Oprește monitorizarea"""
        self.is_running = False
        self.robot.stop()
        
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=2.0)
        
        print("\n")
        print("=" * 70)
        print("⏹️  MONITORIZARE OPRITĂ")
        print("=" * 70)
        self._print_summary()
    
    def _print_summary(self):
        """Afișează sumar final"""
        print()
        print("📊 SUMAR SESIUNE:")
        print(f"   • Total artefacte detectate: {self.robot.artifacts_found}")
        print(f"   • Total alerte trimise: {self.notification_system.get_alert_count()}")
        print(f"   • Arheologi notificați: {len(self.notification_system.archaeologists)}")
        print()
        
        # Export date
        if self.notification_system.get_alert_count() > 0:
            self.notification_system.export_alerts_json()
    
    def run(self, duration: int = 30):
        """
        Rulează aplicația pentru o durată specificată
        
        Args:
            duration: Durata în secunde (default: 30)
        """
        self.setup()
        self.start_monitoring()
        
        try:
            print(f"⏳ Aplicația va rula {duration} secunde...")
            print("   Apăsați Ctrl+C pentru a opri mai devreme")
            print()
            time.sleep(duration)
        except KeyboardInterrupt:
            print("\n\n⚠️  Oprire solicitată de utilizator...")
        finally:
            self.stop_monitoring()


def main():
    """Funcție principală"""
    app = ArtifactDetectorApp()
    
    # Rulează aplicația pentru 30 secunde
    # Modificați durata după preferință
    app.run(duration=30)


if __name__ == "__main__":
    main()
