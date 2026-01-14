"""
Modul pentru controlul robotului cu senzor de detecție a obiectelor
"""
import time
import random
from typing import Tuple, Optional


class Sensor:
    """Senzor de detecție a obiectelor"""
    
    def __init__(self, detection_range: float = 10.0, sensitivity: float = 0.8):
        self.detection_range = detection_range
        self.sensitivity = sensitivity
        self.is_active = False
    
    def activate(self):
        """Activează senzorul"""
        self.is_active = True
        print("🔵 Senzor activat")
    
    def deactivate(self):
        """Dezactivează senzorul"""
        self.is_active = False
        print("🔴 Senzor dezactivat")
    
    def scan(self, position: Tuple[float, float]) -> Optional[dict]:
        """
        Scanează mediul pentru detectarea obiectelor
        Returns: Dicționar cu datele obiectului detectat sau None
        """
        if not self.is_active:
            return None
        
        # Simulare detectie - șansă de 15% de a detecta un obiect
        if random.random() < 0.15:
            distance = random.uniform(0.5, self.detection_range)
            artifact_type = random.choice([
                "ceramică antică", 
                "monedă romană", 
                "fragment de vas",
                "bijuterie",
                "sculptură mică",
                "inscripție"
            ])
            
            return {
                'type': artifact_type,
                'distance': round(distance, 2),
                'position': position,
                'confidence': round(random.uniform(0.7, 1.0), 2),
                'timestamp': time.time()
            }
        
        return None


class Robot:
    """Robot de explorare cu senzor de detecție"""
    
    def __init__(self, name: str = "Explorer-01"):
        self.name = name
        self.position = (0.0, 0.0)
        self.sensor = Sensor()
        self.is_moving = False
        self.artifacts_found = 0
    
    def start(self):
        """Pornește robotul"""
        print(f"🤖 Robot {self.name} pornit")
        self.sensor.activate()
        self.is_moving = True
    
    def stop(self):
        """Oprește robotul"""
        print(f"🤖 Robot {self.name} oprit")
        self.sensor.deactivate()
        self.is_moving = False
    
    def move(self):
        """Deplasează robotul în mediu"""
        if self.is_moving:
            # Simulare mișcare
            dx = random.uniform(-0.5, 0.5)
            dy = random.uniform(-0.5, 0.5)
            self.position = (
                round(self.position[0] + dx, 2),
                round(self.position[1] + dy, 2)
            )
    
    def get_position(self) -> Tuple[float, float]:
        """Returnează poziția curentă"""
        return self.position
    
    def detect_objects(self) -> Optional[dict]:
        """Detectează obiecte în mediu"""
        return self.sensor.scan(self.position)
    
    def increment_artifacts(self):
        """Incrementează contorul de artefacte găsite"""
        self.artifacts_found += 1
