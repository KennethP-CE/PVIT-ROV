import math

#platform data
platforms = {
    "Hibernia":  {"lat": 46.7504, "lon": -48.7819, "depth": 78.0},
    "Hebron":    {"lat": 46.5440, "lon": -48.4980, "depth": 93.0},
    "Sea Rose":  {"lat": 46.7895, "lon": -48.1417, "depth": 107.0},
    "Terra Nova": {"lat": 46.4000, "lon": -48.4000, "depth": 91.0},
}

def dms_to_dd(dms_str):
    d, m, s = map(float, dms_str.split())
    return d + (m / 60) + (s / 3600)

def calculate_threats():
    # example inputs: 47 58 0 | 48 50 0 | Keel: 78 | Heading: 180
    inpLat = input("Enter Iceberg Latitude (D M S): ")
    inpLong = input("Enter Iceberg Longitude (D M S): ")
    ice_keel = float(input("Input Keel Depth (m): "))
    ice_heading = float(input("Input Iceberg Heading (degrees): "))

    ice_lat = dms_to_dd(inpLat)
    ice_lon = -dms_to_dd(inpLong) # west is negative

    print(f"\n--- 2026 MATE ROV Assessment ---")

    for name, data in platforms.items():
        # Eearth is nautical miles
        R_nm = 3440.1 
        
        # 1. distance and bearing from start
        lat1, lon1 = math.radians(ice_lat), math.radians(ice_lon)
        lat2, lon2 = math.radians(data["lat"]), math.radians(data["lon"])
        
        d = math.acos(math.sin(lat1)*math.sin(lat2) + math.cos(lat1)*math.cos(lat2)*math.cos(lon2-lon1))
        dist_to_start = d * R_nm
        
        y = math.sin(lon2-lon1) * math.cos(lat2)
        x = math.cos(lat1)*math.sin(lat2) - math.sin(lat1)*math.cos(lat2)*math.cos(lon2-lon1)
        bearing_to_plt = (math.degrees(math.atan2(y, x)) + 360) % 360

        # how close will the iceberg get
        angle_diff = math.radians(ice_heading - bearing_to_plt)
        xtd = math.asin(math.sin(dist_to_start/R_nm) * math.sin(angle_diff)) * R_nm
        closest_dist = abs(xtd)

        # intersection
        is_ahead = math.cos(angle_diff) > 0
        
        # 110%
        is_grounded = ice_keel >= (data["depth"] * 1.1)

        #printing
        if is_grounded:
            p_threat = "GREEN (Iceberg will ground)"
        elif not is_ahead or closest_dist > 10:
            p_threat = "GREEN"
        elif closest_dist < 5:
            p_threat = "RED"
        else:
            p_threat = "YELLOW"

        # subsea assets
        if is_grounded:
            s_threat = "GREEN (Iceberg will ground)"
        elif not is_ahead or closest_dist > 25:
            s_threat = "GREEN (Does not intersect)"
        else:
            ratio = ice_keel / data["depth"]
            if 0.9 <= ratio < 1.1:
                s_threat = "RED"
            elif 0.7 <= ratio < 0.9:
                s_threat = "YELLOW"
            else:
                s_threat = "GREEN"

        print(f"{name}:")
        print(f"  Closest Pass: {closest_dist:.2f} nm")
        print(f"  Platform: {p_threat}")
        print(f"  Subsea:   {s_threat}")

calculate_threats()