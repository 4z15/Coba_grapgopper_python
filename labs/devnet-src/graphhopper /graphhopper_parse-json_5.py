import requests
import urllib.parse

route_url = "https://graphhopper.com/api/1/route?"
# loc1 = "Washington, D.C."
# loc2 = "Baltimore, Maryland"
key = "98c46221-f462-4e85-b387-196632cdba54"  ### Replace with your API key


def geocoding (location, key):
    while location == "":
        location = input("enter the location again:")
    geocode_url = "https://graphhopper.com/api/1/geocode?" 
    url = geocode_url + urllib.parse.urlencode({"q":location, "limit": "1", "key":key})

    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code
    print("Geocoding API URL for " + location + ":\n" + url)
    if json_status == 200 and len(json_data["hits"]) !=0:
        json_data = requests.get(url).json()
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]
        
        if "country" in json_data["hits"][0]:
            country = json_data["hits"][0]["country"]
        else:
            country=""
        
        if "state" in json_data["hits"][0]:
            state = json_data["hits"][0]["state"]
        else:
            state=""
        
        if len(state) !=0 and len(country) !=0:
            new_loc = name + ", " + state + ", " + country
        elif len(state) !=0:
            new_loc = name + ", " + country
        else:
            new_loc = name
        
        print("Geocoding API URL for " + new_loc + " (Location Type: " + value + ")\n" + url)

    else:
        lat="null"
        lng="null"
        new_loc = location
        if json_status !=200:
            print("Geocode API status : " + str(json_status) + "\nError mesage : " + json_data["message"])
    return json_status,lat,lng,new_loc

# orig = geocoding(loc1, key)
# print(orig)
# dest = geocoding(loc2, key)
# print(dest)
while True:
    print("\n+++++++++++++++++++++++++++++++++++++++++++++")
    print("Vehicle profiles available on Graphhopper:")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    print("car, bike, foot")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    profile=["car", "bike", "foot"]
    vehicle = input("Enter a vehicle profile from the list above: ")
    if vehicle == "quit" or vehicle == "q":
        break
    elif vehicle in profile:
        vehicle = vehicle
    else: 
        vehicle = "car"
        print("No valid vehicle profile was entered. Using the car profile.")

    loc1 = input("Starting Location: ")
    if loc1 == "quit" or loc1 == "q":
        break
    orig = geocoding(loc1,key)
    loc2 = input("Destination: ")
    if loc2 == "quit" or loc2 == "q":
        break
    dst = geocoding(loc2,key)
    print("==============================================")
    if orig[0] == 200 and dst [0] == 200:
        op="&point="+str(orig[1])+"%2C"+str(orig[2])
        dp="&point="+str(dst[1])+"%2C"+str(dst[2])
        paths_url = route_url + urllib.parse.urlencode({"key":key}) + op + dp
        paths_status = requests.get(paths_url).status_code
        paths_data = requests.get(paths_url).json()
        print("Routing API Status: " + str(paths_status) + "\nRouting API URL:\n" + paths_url)
    print("==============================================")
    print("Directions from " + orig[3] + " to " + dst[3] + " by " + vehicle)
    print("==============================================")
    if paths_status == 200:
        miles = (paths_data["paths"][0]["distance"])/1000/1.61
        km = (paths_data["paths"][0]["distance"])/1000
        sec = int(paths_data["paths"][0]["time"]/1000%60)
        min = int(paths_data["paths"][0]["time"]/1000/60%60)
        hr = int(paths_data["paths"][0]["time"]/1000/60/60)

        print("Distance Traveled: " + str(paths_data["paths"][0]["distance"]) + " m")
        print("Trip Duration: {0:02d}:{1:02d}:{2:02d}".format(hr, min, sec))
        print("=================================================")
        for each in range(len(paths_data["paths"][0]["instructions"])):
            path = paths_data["paths"][0]["instructions"][each]["text"]
            distance = paths_data["paths"][0]["instructions"][each]["distance"]
            print("{0} ( {1:.1f} km / {2:.1f} miles )".format(path, distance/1000, distance/1000/1.61))
        print("=============================================")
    else:
        print("Error message: " + paths_data["message"])
        print("*************************************************")



