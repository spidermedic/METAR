#!/usr/bin/env python3

import requests
import time
import sys
from my_token import *

def main(argv):

    # Parse the args
    if len(argv) == 1:
        print("\nUsage: [-d] ICAO Code(s)")
        print("-d option is for a decoded output. Default output is standard METAR")
        print("The program requires one or more ICAO codes separated by spaces.\n")
        exit(1)

    if len(argv) == 2:
        if argv[1] == "-d":
            print("\nNo ICAO airport codes were provided.\n")
            exit(1)
        if len(argv[1]) != 4:
            print(f'\n{argv[1]} is not a valid ICAO airport code')
            exit(1)

    # Set the decode flag and set the first airport code to the second arg
    if argv[1] == "-d":
        decode = True
        arg_start = 2

    # Otherwise the airport code is the first arg and the output will be a raw METAR
    else:
        decode = False
        arg_start = 1

    # Now go get the current METAR for each of the ICAO codes provided.
    for item in range(arg_start, len(argv)):
        icao_code = argv[item].upper()
        if decode:
            decode_metar(get_metar(icao_code))
        else:
            print(f'\n{get_metar(icao_code)["raw"]}')

    # Line feed after the last entry, then GTFO.
    print("")
    exit(0)


def get_metar(icao_code):
    """ Retrieve the METAR for the specified airport and return json data"""

    # MY_TOKEN is required for the AVWX api and can be obtained from https://account.avwx.rest/
    # The token is set in my_token.py or can just be appended to the end of the string after &token=
    url = "https://avwx.rest/api/metar/" + icao_code + "?format=json&onfail=cache&token=" + MY_TOKEN

    # Make the web request
    try:
        r = requests.get(url)
    except:
        print(f'\nUnable to fetch data, check ICAO code and make sure you have a valid token. HTTP:{str(r.status_code)}')
        exit(1)

    return(r.json())


def decode_metar(json_data):
    """ Formats and displays the information in a more user-friendly format"""

    # Airport ICAO code
    station = json_data["station"]

    # Time the report was posted sliced from the raw data
    t = json_data['raw'][7:11]
 
    # Format the time so it looks nicer   
    metar_time = format_time(t)

    # Get the wind direction, speed, and gusts
    wind_direction = json_data["wind_direction"]["value"]
    wind_speed = str(json_data['wind_speed']['value']) + " kts"

    if json_data["wind_gust"]:
        wind_gust = " with gusts to " + str(json_data["wind_gust"]['value'])
    else:
        wind_gust = ""

    #Visibility in statute miles and current flight rules
    visibility = json_data['visibility']['value']
    flight_rules = json_data["flight_rules"]

    # Parse the cloud cover list
    sky = ""
    if json_data['clouds']:
        for item in json_data['clouds']:
            sky += item['repr'] + " "
    else:
        sky = "Clear"

    # Convert the yemp and dew point to F
    temp_c = json_data["temperature"]['value']
    temp_f = float(temp_c) * 9/5 + 32
 
    dew_c = json_data["dewpoint"]['value']
    dew_f = float(dew_c) * 9/5 + 32

    # Barometric pressure
    altimeter = json_data["altimeter"]['value']

    # Print it all pretty    
    print('\n')
    print(f'{station}        {metar_time}')
    print(f'Wind        {str(wind_direction)} @ {str(wind_speed)}{str(wind_gust)}')
    print(f'Visibility  {str(visibility)} sm ({flight_rules})')
    print(f'Sky         {sky}')
    print(f'Temp        {str(temp_f)}  ({temp_c}c)')
    print(f'Dew Point   {str(dew_f)}  ({dew_c}c)')
    print(f'Pressure    {str(altimeter)}')

    return

def format_time(t_gmt):
    """ Formats converts t_gmt to local time and formats it for readability"""

    h = t_gmt[:2]
    m = t_gmt[2:]

    if int(h) <= 5:
        h2 = int(h) +24
    else:
        h2 = int(h)

    h_local = h2 - (5 - time.localtime().tm_isdst)

    # older version of formatted_time: formatted_time = "{:02d}:{} ({}:{} gmt)".format(h_local, m, h, m)
    formatted_time = f"{h_local}:{m} ({h}:{m} utc)"

    return (formatted_time)


if __name__ == "__main__":
    main(sys.argv)