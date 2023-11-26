import sys
import csv
import os
import shutil
import pyproj

def sk42ToWgs84(x, y):
    transformer = pyproj.Transformer.from_crs(4284, 4326)
    lon, lat = transformer.transform(x, y)
    return lon, lat
    
if len(sys.argv) < 2:
    print("Usage: python converter.py <csv_file_name>")
    exit()

csv_file_name = sys.argv[1] #get csv file name as first argument 

#read csv file and get data
csv_file = open(csv_file_name, 'r')
csv_reader = csv.reader(csv_file, delimiter=';')
for row in csv_reader:
    # skip first row
    if csv_reader.line_num == 1:
        continue

    # get data from row
    name = row[0]
    description = row[2]
    coords = row[3]

    coords = coords.split(' ')
    coords[0] = coords[0].replace('-', '.')
    coords[1] = coords[1].replace('-', '.')
    x = float(coords[0])
    y = float(coords[1])

    lon, lat = sk42ToWgs84(x, y)

    sql = "INSERT INTO Data (name, description, lat, lon) VALUES ('%s', '%s', '%s', '%s');" % (name, description, lat, lon)

    sql_file = open('data.sql', 'a')
    sql_file.write(sql + '\n')
    sql_file.close()

