import sys
import json
import folium
from zmq import NULL

invalid_input = True

if invalid_input == True:
    def convert(input):
        coordinate = []
        coord = input.split()
        coord = [item.replace(',', '') for item in coord]
        global invalid_input
        if len(coord) < 6:
            coordinate = latLong(coord)
        if len(coord) == 8:
            coordinate = DMS(coord)
        if len(coord) == 6:
            coordinate = DDM(coord)
        invalid_input = True
        return coordinate

def latLong(coord):
    output = []
    string_lat = ""
    string_lon = ""
    global invalid_input
    if len(coord) == 4 or len(coord) == 3:
        if coord[0].isdigit():
            print("Unable to process")
            invalid_input = False
            return
        if coord[0].isalpha():
            print("Unable to process")
            invalid_input = False
            return
        if invalid_input == True:
            if coord[1] == 'N'or'S'or'n'or's' or coord[3] == 'W'or'w'or'E'or'e' or coord[2] == 'W'or'w'or'E'or'e':
                lat = float(coord[0])
                try:
                    lon = float(coord[2])
                except ValueError:
                    lon = float(coord[1])

            if lon < 0 and lon > -181.000000:
                formatted_lon = "{:.6f}".format(lon)
                formatted_lon = float(formatted_lon)
                output.append(formatted_lon)
                string_lon = str(formatted_lon)+" W"
            if lon > 0 and lon < 181.000000:
                formatted_lon = "{:.6f}".format(lon)
                formatted_lon = float(formatted_lon)
                output.append(formatted_lon)
                string_lon = str(formatted_lon)+" E"
            if lat < 0 and lat > -91.000000:
                formatted_lat = "{:.6f}".format(lat)
                formatted_lat = float(formatted_lat)
                output.append(formatted_lat)
                string_lat = str(formatted_lat)+" S, "
            if lat > 0 and lat < 91.000000:
                formatted_lat = "{:.6f}".format(lat)
                formatted_lat = float(formatted_lat)
                output.append(formatted_lat)
                string_lat = str(formatted_lat)+" N, "
            print(string_lat+string_lon)
            return output
    if invalid_input == True:
        if len(coord) == 2:
            try:
                lat = float(coord[0].strip(','))
                lon = float(coord[1])
            except ValueError:
                    print("unable to process")
                    invalid_input = False
                    return
            if lat >= 90.000 and lat <= 180.000:
                temp = lat
                lat = lon
                lon = temp
            if lat <= -90.000 and lat >= -180.000:
                temp = lat
                lat = lon
                lon = temp
            if lon < 0 and lon > -181.000000:
                formatted_lon = "{:.6f}".format(lon)
                formatted_lon = float(formatted_lon)
                output.append(formatted_lon)
                string_lon = str(formatted_lon)+" W"
            if lon > 0 and lon < 181.000000:
                formatted_lon = "{:.6f}".format(lon)
                formatted_lon = float(formatted_lon)
                output.append(formatted_lon)
                string_lon = str(formatted_lon)+" E"
            if lat < 0 and lat > -91.000000:
                formatted_lat = "{:.6f}".format(lat)
                formatted_lat = float(formatted_lat)
                output.append(formatted_lat)
                string_lat = str(formatted_lat)+" S, "
            if lat > 0 and lat < 91.000000:
                formatted_lat = "{:.6f}".format(lat)
                formatted_lat = float(formatted_lat)
                output.append(formatted_lat)
                string_lat = str(formatted_lat)+" N, "
            print(string_lat+string_lon)
            return output


def DMS(coord):
    output = []
    string_lon = ""
    string_lat = ""
    global invalid_input
    try:
        lat_degree = float(coord[0].replace('?', '').replace('D', '').replace('d', ''))
        lat_min = float(coord[1].replace("'",'').replace('M', '').replace('m', ''))
        lat_sec = float(coord[2].replace('"', '').replace('S','').replace('s',''))
        lat_direction = coord[3]
        lon_degree = float(coord[4].replace('?','').replace('D','').replace('d',''))
        lon_min = float(coord[5].replace("'",'').replace('M','').replace('m',''))
        lon_sec = float(coord[6].replace('"','').replace('S','').replace('s',''))
        lon_direction = coord[7]
    except ValueError:
        print("Unable to process")
        invalid_input = False
    if invalid_input == True:
        if lon_degree > -1 and lon_degree < 181 and lon_min > 0 and lon_min < 60 and lon_sec > -1 and lon_sec < 60:
            degree_format = lon_degree + (lon_min/60) + (lon_sec/3600)
            degree_format = "{:.6f}".format(degree_format)
            degree_format = float(degree_format)
            if lon_direction == "W":
                degree_format = -degree_format
            output.append(degree_format)
            if degree_format > -1:
                string_lon = str(degree_format)+" E"
            if degree_format < 0:
                string_lon = str(degree_format)+" W"
        if lat_degree > -1 and lat_degree < 91 and lat_min > 0 and lat_min < 60 and lat_sec > -1 and lat_min < 60:
            degree_format = lat_degree + (lat_min/60) + (lat_sec/3600)
            degree_format = "{:.6f}".format(degree_format)
            degree_format = float(degree_format)
            if lat_direction == "S":
                degree_format = -degree_format
            output.append(degree_format)
            if degree_format > -1:
                string_lat = str(degree_format)+" N, "
            if degree_format < 0:
                string_lat = str(degree_format)+" S, "
        print(string_lat+string_lon)
        return output

def DDM(coord):
    output = []
    global invalid_input
    try:
        lat_degree = float(coord[0].strip('?'))
        lat_decmin = float(coord[1].strip("'"))

        lon_degree = float(coord[3].strip('?'))
        lon_decmin = float(coord[4].strip("'"))
    except ValueError:
        print("Unable to process")
        invalid_input = False
    if invalid_input == True:
        if lon_degree > -1 and lon_degree < 181 and lon_decmin > 0 and lon_decmin < 60:
            degree_format = lon_degree + (lon_decmin/60)
            degree_format = "{:.6f}".format(degree_format)
            degree_format = float(degree_format)
            output.append(degree_format)
        if lat_degree > -1 and lat_degree < 91 and lat_decmin > 0 and lat_decmin < 60:
            degree_format = lat_degree + (lat_decmin/60)
            degree_format = "{:.6f}".format(degree_format)
            degree_format = float(degree_format)
            output.append(degree_format)
        return output


features = []
for line in sys.stdin:
    flag = False
    line.strip()
    coordinate = convert(line)
    if coordinate != None:
        feature = {
            "type": "Feature",
            "properties": {},
            "geometry": {
            "coordinates": coordinate,
            "type": "Point"
            }
        }
        features.append(feature)

geojson = {
    "type": "FeatureCollection",
    "features": features
}

with open('output.geojson', 'w') as f:
    json.dump(geojson, f)

geojson_data = open('output.geojson', 'r').read()


