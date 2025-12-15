from .coordinates import clean_latitude, clean_longitude

def format_and_clean_geolocation(val):
    try:
        # Extracting latitude and longitude from a tuple string
        lat, lon = str(val).strip("()").split(",")
        geo_lat = clean_latitude(round(float(lat), 6))
        geo_lon = clean_longitude(round(float(lon), 6))


        # Removing invalid data
        if geo_lat == None or geo_lon == None: return None
    except Exception as e:
        return None
    return (geo_lat, geo_lon)

def validate_geolocation(row): 
    geo_lat, geo_lon = row["Geolocation"]
    latitude = row["Latitude"]
    longitude = row["Longitude"]

    # Fixing Geolocation values if they differ from column Latitude and Longitude
    if latitude != geo_lat: geo_lat = latitude
    if longitude != geo_lon: geo_lon = longitude

    return (geo_lat, geo_lon)

# Converting tuple to string for Database
def geo_to_string(val):
    lat, lon = val
    return f"{lat},{lon}"