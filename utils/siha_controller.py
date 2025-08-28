import time
import math
from pymavlink import mavutil
import numpy as np

class SIHAController:
    def __init__(self):
        """
        SIHA Controller sınıfı - Pure pymavlink implementation
        
        Args:
            connection_string: ArduPilot bağlantı adresi
        """
        self.dev = False
        
        
        self.connection_string = None
        self.mavlink_connection = None
        self.vehicle_armed = False
        self.current_mode = "UNKNOWN"
        self.target_system = 1
        self.target_component = 1
        
        # Telemetry data
        self.current_location = {'lat': 0, 'lon': 0, 'alt': 0}
        self.current_attitude = {'roll': 0, 'pitch': 0, 'yaw': 0}
        self.current_velocity = {'vx': 0, 'vy': 0, 'vz': 0}
        self.battery_info = {'voltage': 0, 'current': 0, 'remaining': 0}
        self.gps_info = {'fix_type': 0, 'satellites': 0}

    def connect_to_vehicle(self, connection_string, baudrate):
        """Uçağa bağlan"""
        try:
            print(f"Uçağa bağlanılıyor: {connection_string} | {baudrate}")
            self.mavlink_connection = mavutil.mavlink_connection(connection_string, baud=baudrate)

            # Heartbeat bekle
            print("Heartbeat bekleniyor...")
            if not self.dev:
                self.mavlink_connection.wait_heartbeat()
            
            # System ve component ID'leri al
            self.target_system = self.mavlink_connection.target_system
            self.target_component = self.mavlink_connection.target_component
            
            print("Bağlantı başarılı!")
            self.print_vehicle_info()
            
            # Telemetri akışını başlat
            self.request_data_stream()
            
            return True
            
        except Exception as e:
            print(f"Bağlantı hatası: {e}")
            return False
    
    def request_data_stream(self):
        """Telemetri akışını başlat"""
        try:
            # Position data
            self.mavlink_connection.mav.request_data_stream_send(
                self.target_system, self.target_component,
                mavutil.mavlink.MAV_DATA_STREAM_POSITION, 4, 1)
            
            # Attitude data
            self.mavlink_connection.mav.request_data_stream_send(
                self.target_system, self.target_component,
                mavutil.mavlink.MAV_DATA_STREAM_EXTRA1, 4, 1)
                
            # System status
            self.mavlink_connection.mav.request_data_stream_send(
                self.target_system, self.target_component,
                mavutil.mavlink.MAV_DATA_STREAM_EXTENDED_STATUS, 2, 1)
                
        except Exception as e:
            print(f"Data stream request hatası: {e}")
    
    def update_telemetry(self):
        """Telemetri verilerini güncelle"""
        # Check if we have an active connection
        if self.mavlink_connection is None:
            return  # Silently return if no connection

        try:
            msg = self.mavlink_connection.recv_match(type=['GLOBAL_POSITION_INT', 'ATTITUDE',
                                                          'VFR_HUD', 'SYS_STATUS', 'GPS_RAW_INT',
                                                          'HEARTBEAT'], blocking=False)
            if msg:
                msg_type = msg.get_type()
                
                if msg_type == 'GLOBAL_POSITION_INT':
                    self.current_location = {
                        'lat': msg.lat / 1e7,
                        'lon': msg.lon / 1e7,
                        'alt': msg.relative_alt / 1000.0
                    }
                    
                elif msg_type == 'ATTITUDE':
                    self.current_attitude = {
                        'roll': math.degrees(msg.roll),
                        'pitch': math.degrees(msg.pitch),
                        'yaw':  math.degrees(msg.yaw)
                    }
                    
                elif msg_type == 'VFR_HUD':
                    self.current_velocity = {
                        'groundspeed': msg.groundspeed,
                        'airspeed': msg.airspeed,
                        'heading': msg.heading
                    }
                    
                elif msg_type == 'SYS_STATUS':
                    present = msg.onboard_control_sensors_present
                    enabled = msg.onboard_control_sensors_enabled
                    health = msg.onboard_control_sensors_health
                    voltage = msg.voltage_battery / 1000.0   # mV → V
                    current = msg.current_battery / 100.0
                    remaining = msg.battery_remaining
                    
                    self.battery_info = {
                        'voltage': voltage,
                        'current': current,
                        'remaining': remaining
                    }
                    
                elif msg_type == 'GPS_RAW_INT':
                    self.gps_info = {
                        'lat': msg.lat / 1e7,
                        'lon': msg.lon / 1e7,
                        'alt': msg.alt / 1000.0,
                        'fix_type': msg.fix_type,
                        'satellites': msg.satellites_visible
                    }
                    
                elif msg_type == 'HEARTBEAT':
                    armed = bool(msg.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED)
                    mode = mavutil.mode_string_v10(msg)
                    self.current_mode = mode
                    self.vehicle_armed = bool(msg.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED)
                    
        except Exception as e:
            print(f"Telemetri güncelleme hatası: {e}")
    
    def return_telemetry_var(self):
        data = {
            'current_location': self.current_location,
            'current_attitude': self.current_attitude,
            'current_velocity': self.current_velocity,
            'battery_info': self.battery_info,
            'gps_info': self.gps_info,
            'vehicle_armed': self.vehicle_armed,
            'mode': self.current_mode
        }
        return data

    def print_vehicle_info(self):
        """Uçak bilgilerini yazdır"""
        if self.mavlink_connection:
            print("=" * 50)
            print("UÇAK BİLGİLERİ")
            print("=" * 50)
            print(f"Bağlantı: {self.connection_string}")
            print(f"System ID: {self.target_system}")
            print(f"Component ID: {self.target_component}")
            print(f"MAVLink bağlantısı: Aktif")
            print(f"Mod: {self.current_mode}")
            print(f"Armed: {self.vehicle_armed}")
            print("=" * 50)
        else:
            print("Bağlantı yok!")
    
    def wait_for_arm(self):
        """Arm durumunu bekle"""
        print("Uçağın arm olmasını bekleniyor...")
        while not self.vehicle_armed:
            self.update_telemetry()
            time.sleep(1)
            print(".", end="", flush=True)
        print("\nUçak armed!")
    
    def set_mode(self, mode_name):
        """Uçuş modunu değiştir"""
        try:
            if not self.mavlink_connection:
                print("Bağlantı yok!")
                return False
            
            # ArduPilot modları
            mode_mapping = {
                'MANUAL': 0,
                'CIRCLE': 1,
                'STABILIZE': 2,
                'TRAINING': 3,
                'ACRO': 4,
                'FLY_BY_WIRE_A': 5,
                'FLY_BY_WIRE_B': 6,
                'CRUISE': 7,
                'AUTOTUNE': 8,
                'AUTO': 10,
                'RTL': 11,
                'LOITER': 12,
                'TAKEOFF': 13,
                'AVOID_ADSB': 14,
                'GUIDED': 15,
                'INITIALISING': 16,
                'QSTABILIZE': 17,
                'QHOVER': 18,
                'QLOITER': 19,
                'QLAND': 20,
                'QRTL': 21,
                'QAUTOTUNE': 22,
                'QACRO': 23,
                'THERMAL': 24,
                'LAND': 25
            }
            
            if mode_name not in mode_mapping:
                print(f"Geçersiz mod: {mode_name}")
                return False
            
            mode_id = mode_mapping[mode_name]
            
            # Mod değişim komutu gönder
            self.mavlink_connection.mav.set_mode_send(
                self.target_system,
                mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
                mode_id
            )
            
            print(f"Mod değiştirme komutu gönderildi: {mode_name}")
            self.current_mode = mode_name
            return True
            
        except Exception as e:
            print(f"Mod değiştirme hatası: {e}")
            return False
    
    def arm_vehicle(self):
        """Uçağı arm et"""
        print("Uçak arm ediliyor...")
        
        if not self.mavlink_connection:
            print("Bağlantı yok!")
            return False
        
        # Arm komutu gönder
        self.mavlink_connection.mav.command_long_send(
            self.target_system, self.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0, 1, 0, 0, 0, 0, 0, 0
        )
        
        # Arm durumunu bekle
        start_time = time.time()
        while not self.vehicle_armed and (time.time() - start_time) < 10:
            self.update_telemetry()
            time.sleep(0.5)
        
        if self.vehicle_armed:
            print("Uçak başarıyla arm edildi!")
            return True
        else:
            print("Arm işlemi başarısız!")
            return False
    
    def disarm_vehicle(self):
        """Uçağı disarm et"""
        print("Uçak disarm ediliyor...")
        
        if not self.mavlink_connection:
            print("Bağlantı yok!")
            return False
        
        # Disarm komutu gönder
        self.mavlink_connection.mav.command_long_send(
            self.target_system, self.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0, 0, 0, 0, 0, 0, 0, 0
        )
        
        # Disarm durumunu bekle
        start_time = time.time()
        while self.vehicle_armed and (time.time() - start_time) < 10:
            self.update_telemetry()
            time.sleep(0.5)
        
        if not self.vehicle_armed:
            print("Uçak başarıyla disarm edildi!")
            return True
        else:
            print("Disarm işlemi başarısız!")
            return False
    
    def takeoff(self, target_altitude):
        """Kalkış yap"""
        print(f"Kalkış yapılıyor, hedef irtifa: {target_altitude}m")
        
        # GUIDED moda geç
        self.set_mode("GUIDED")
        
        # Arm et
        if not self.arm_vehicle():
            return False
        
        # Takeoff komutu gönder
        self.mavlink_connection.mav.command_long_send(
            self.target_system, self.target_component,
            mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
            0, 0, 0, 0, 0, 0, 0, target_altitude
        )
        
        # Hedef irtifaya ulaşana kadar bekle
        print("Hedef irtifaya çıkılıyor...")
        while True:
            self.update_telemetry()
            current_altitude = self.current_location['alt']
            print(f"Mevcut irtifa: {current_altitude:.1f}m")
            
            if current_altitude >= target_altitude * 0.95:
                print("Hedef irtifaya ulaşıldı!")
                break
            
            time.sleep(1)
        
        return True
    
    def goto_position(self, lat, lon, alt):
        """Belirtilen koordinatlara git"""
        print(f"Hedefe gidiliyor: {lat:.6f}, {lon:.6f}, {alt}m")
        
        if not self.mavlink_connection:
            print("Bağlantı yok!")
            return False
        
        # GUIDED moda geç
        self.set_mode("GUIDED")
        
        # Waypoint komutu gönder
        self.mavlink_connection.mav.set_position_target_global_int_send(
            0,  # time_boot_ms
            self.target_system, self.target_component,
            mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,
            0b0000111111111000,  # type_mask
            int(lat * 1e7), int(lon * 1e7), alt,
            0, 0, 0,  # velocity
            0, 0, 0,  # acceleration
            0, 0  # yaw, yaw_rate
        )
        
        # Hedefe ulaşana kadar bekle
        while True:
            self.update_telemetry()
            current_location = self.current_location
            distance = self.get_distance_metres(
                current_location['lat'], current_location['lon'], lat, lon
            )
            
            print(f"Hedefe mesafe: {distance:.1f}m")
            
            if distance < 5:  # 5 metre içinde
                print("Hedefe ulaşıldı!")
                break
            
            time.sleep(1)
        
        return True
    
    def get_distance_metres(self, lat1, lon1, lat2, lon2):
        """İki nokta arasındaki mesafeyi hesapla (metre)"""
        dlat = lat2 - lat1
        dlong = lon2 - lon1
        
        # Yaklaşık hesaplama
        distance = math.sqrt((dlat * dlat) + (dlong * dlong)) * 1.113195e5
        return distance
    
    def land_vehicle(self):
        """Uçağı indir"""
        print("İniş yapılıyor...")
        
        if not self.mavlink_connection:
            print("Bağlantı yok!")
            return False
        
        # LAND moda geç
        self.set_mode("LAND")
        
        # İnişi bekle
        while self.vehicle_armed:
            self.update_telemetry()
            altitude = self.current_location['alt']
            print(f"İniş irtifası: {altitude:.1f}m")
            time.sleep(1)
        
        print("İniş tamamlandı!")
        return True
    
    def emergency_land(self):
        """Acil iniş"""
        print("ACİL İNİŞ!")
        
        if not self.mavlink_connection:
            print("Bağlantı yok!")
            return False
        
        # Acil iniş komutu
        self.mavlink_connection.mav.command_long_send(
            self.target_system, self.target_component,
            mavutil.mavlink.MAV_CMD_NAV_LAND,
            0, 0, 0, 0, 0, 0, 0, 0
        )
        
        self.set_mode("LAND")
    
    def close_connection(self):
        """Bağlantıyı kapat"""
        if self.mavlink_connection:
            self.mavlink_connection.close()
            print("Bağlantı kapatıldı.")

# Test fonksiyonu
def main():
    """Ana fonksiyon - Test uçuşu"""
    
    # SIHA Controller oluştur
    siha = SIHAController()
    
    try:
        # Uçağa bağlan
        if not siha.connect_to_vehicle():
            return
        
        # Kalkış yap
        siha.takeoff(50)  # 50 metre irtifa
        
        # Test waypoint'leri
        waypoints = [
            (37.4419, -122.1430, 50),  # Örnek koordinatlar
            (37.4429, -122.1440, 50),
            (37.4439, -122.1450, 50),
        ]
        
        # Waypoint'leri takip et
        for wp in waypoints:
            siha.goto_position(wp[0], wp[1], wp[2])
            time.sleep(5)  # Waypoint'te bekle
        
        # İniş yap
        siha.land_vehicle()
        
    except KeyboardInterrupt:
        print("\nProgram durduruldu!")
        siha.emergency_land()
    
    except Exception as e:
        print(f"Hata: {e}")
        siha.emergency_land()
    
    finally:
        siha.close_connection()

if __name__ == "__main__":
    main()
