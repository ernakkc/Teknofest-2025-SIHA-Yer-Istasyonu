import math
from pymavlink import mavutil

class GetInfo:
    def __init__(self, mavlink_connection, updater_func):
        self.mavlink_connection = mavlink_connection
        self.updater_func = updater_func

        mavlink_connection.mav.request_data_stream_send(mavlink_connection.target_system, mavlink_connection.target_component, mavutil.mavlink.MAV_DATA_STREAM_POSITION, 4, 1)
        mavlink_connection.mav.request_data_stream_send(mavlink_connection.target_system, mavlink_connection.target_component, mavutil.mavlink.MAV_DATA_STREAM_EXTRA1, 4, 1)
        mavlink_connection.mav.request_data_stream_send(mavlink_connection.target_system, mavlink_connection.target_component, mavutil.mavlink.MAV_DATA_STREAM_EXTENDED_STATUS, 2, 1)


        while not self.mavlink_connection.is_connected():
            msg = mavlink_connection.recv_match(
                type=['GLOBAL_POSITION_INT', 'ATTITUDE', 'VFR_HUD', 'SYS_STATUS', 'GPS_RAW_INT', 'HEARTBEAT'],
                blocking=False,
                timeout=1
            )

            if msg:
                if msg.get_type() == 'GLOBAL_POSITION_INT':
                    lat = msg.lat / 1e7        # derece
                    lon = msg.lon / 1e7        # derece
                    alt = msg.alt / 1000.0     # metre
                    print(f"[GLOBAL_POSITION_INT] Latitude: {lat:.6f}°, Longitude: {lon:.6f}°, Altitude: {alt:.2f} m")

                if msg.get_type() == 'ATTITUDE':
                    roll = math.degrees(msg.roll)   # rad → derece
                    pitch = math.degrees(msg.pitch)
                    yaw = math.degrees(msg.yaw)
                    print(f"[ATTITUDE] Roll: {roll:.2f}°, Pitch: {pitch:.2f}°, Yaw: {yaw:.2f}°")

                if msg.get_type() == 'VFR_HUD':
                    airspeed = msg.airspeed        # m/s
                    groundspeed = msg.groundspeed  # m/s
                    heading = msg.heading          # derece
                    print(f"[VFR_HUD] Airspeed: {airspeed:.2f} m/s, Groundspeed: {groundspeed:.2f} m/s, Heading: {heading}°")

                if msg.get_type() == 'SYS_STATUS':
                    present = msg.onboard_control_sensors_present
                    enabled = msg.onboard_control_sensors_enabled
                    health = msg.onboard_control_sensors_health
                    voltage = msg.voltage_battery / 1000.0   # mV → V
                    current = msg.current_battery / 100.0    # cA → A
                    print(f"[SYS_STATUS] Sensors Present: {present}, Enabled: {enabled}, Health: {health}, Battery: {voltage:.2f} V, Current: {current:.2f} A")

                if msg.get_type() == 'GPS_RAW_INT':
                    gps_lat = msg.lat / 1e7       # derece
                    gps_lon = msg.lon / 1e7       # derece
                    gps_alt = msg.alt / 1000.0    # metre
                    fix_type = msg.fix_type
                    satellites = msg.satellites_visible
                    print(f"[GPS_RAW_INT] Latitude: {gps_lat:.6f}°, Longitude: {gps_lon:.6f}°, Altitude: {gps_alt:.2f} m, Fix Type: {fix_type}, Satellites: {satellites}")

                if msg.get_type() == 'HEARTBEAT':
                    armed = bool(msg.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED)
                    mode = mavutil.mode_string_v10(msg)
                    print(f"[HEARTBEAT] Armed: {armed}, Mode: {mode}")

                data = {
                    'current_location': {'lat': lat, 'lon': lon, 'alt': alt},
                    'current_attitude': {'roll': roll, 'pitch': pitch, 'yaw': yaw},
                    'current_velocity': {'vx': airspeed, 'vy': groundspeed, 'vz': heading},
                    'battery_info': {'voltage': voltage, 'current': current, 'remaining': None},
                    'gps_info': {'fix_type': fix_type, 'satellites': satellites},
                    'vehicle_armed': armed,
                    'mode': mode
                }

                self.updater_func(data)