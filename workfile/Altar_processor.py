import csv
import os
import re
import json

def dms2dd(direction, degrees, minutes, seconds):
    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60)
    if direction == 'W' or direction == 'S':
        dd *= -1
    return dd

def dd2dms(deg):
    d = int(deg)
    md = abs(deg - d) * 60
    m = int(md)
    sd = (md - m) * 60
    return [d, m, sd]

def parse_dms(cardinality, dms):
    parts = re.split('[º°\'",.]+', dms)
    coord = dms2dd(cardinality, parts[0], parts[1], parts[2])

    return coord

def process_csv(dir, region):

    # Construct filepath
    dirname = os.path.dirname(__file__)
    filepath = os.path.join(dirname, 'raw files/House Altar Data/{}'.format(dir))

    with open(filepath) as infile:
        
        # Read data into list of lists
        reader = csv.reader(infile)
        data = list(reader)

        # Group two lines at a time
        def pairwise(iterable):
            # "s -> (s0, s1), (s2, s3), (s4, s5), ..."
            a = iter(iterable)
            return zip(a, a)
        
        # Validate headers
        noColumn = data[0][0] == '\ufeffNO.'
        nameColumn = data[0][1] == ' NAMA ALTAR '
        addressColumn = data[0][3] == 'ALAMAT'
        GPSColumn = data[0][9] == 'GPS'
        checkColumn = data[0][14] == 'CHECK'

        if (noColumn or nameColumn or addressColumn or GPSColumn or checkColumn) == False:
            raise ValueError ("Headers in wrong position, aborting.")
        else:
            print("Formating validated")
        
        def pantakError(x):
            raise ValueError("Pantak value neither Y or N, instead: {}".format(x))

        i = 1
        buffer = []
        for x, y in pairwise(data[2:]):
            # Validate temple number for row positioning
            if x[0] != str(i):
                raise ValueError ("Temple number wrong; is {}, should be {}.".format(x[0], i))
            else:
                i = i + 1
            
            latDMS = x[10] + "°" + x[11] + "'" + x[12] + "." + x[13] + "\""
            lonDMS = y[10] + "°" + y[11] + "'" + y[12] + "." + y[13] + "\""
            
            latDD = parse_dms("N", latDMS)
            lonDD = parse_dms("E", lonDMS)

            constructor = {
                "village_id": region.strip() + "-" + x[0],
                "name": x[1].strip(),
                "address_line_1": x[3].strip() + ". " + y[3].strip() + " " + y[4].strip(),
                "address_line_2": y[5].strip() + " " + y[6].strip() + " " + y[7].strip() + " " + y[8].strip(),
                "latlng" : [latDD, lonDD],
                "photo_id": x[15].strip(),
                "Pantak": True if y[15].strip() == "Y" else False if y[15].strip() == "N" else pantakError(y[15])
            }

            buffer.append(constructor)
            print("{} {} added to buffer".format(constructor["village_id"], constructor["name"]))

        print("Processing done, dumping into file")

        dirname = os.path.dirname(__file__)
        filepath = os.path.join(dirname, "{}-altar-processed.json".format(region))
        with open(filepath, "w") as out:
            json.dump(buffer, out)
        print("Done. Data in {}".format(filepath))

process_csv('altar-central.csv', "central")
process_csv('altar-east.csv', "east")
process_csv('altar-north.csv', "north")
process_csv('altar-south.csv', "south")
process_csv('altar-west.csv', "west")