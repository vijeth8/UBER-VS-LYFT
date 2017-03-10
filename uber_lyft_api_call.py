import requests
import os
import yaml
import boto3
import json
import time
from pprint import pprint

locations = {"galvanize": (37.787613,-122.3988267),
"ggpark": (37.7694208,-122.4884025),
"ggbridge": (37.8090796,-122.4760557),
"sutro baths":(37.7804369,-122.5158822),
"pier 39":(37.808673,-122.4120097),
"twin peaks":(37.7532508,-122.460038),
"airport":(37.6213129,-122.3811441),
"usf" : (37.7766466,-122.4528717),
"glen park" : (37.7330628,-122.4360081),
"sf zoo" : (37.7329743,-122.5050294),
"dolores park" :(37.7596168,-122.4290925),
"AT_T" :(37.7785951,-122.3914585),
"castro": (37.762635,-122.4374087),
"lombart": (37.802139,-122.4209287),
"u_sq":(37.787933,-122.4096868),
"china town":(37.7940865,-122.4115089),
"baker beach":(37.793005,-122.4902552),
"painted ladies":(37.7762593,-122.4349467),
"embarcadero":(37.7968423,-122.4079158),
"tenderloin":(37.7839293,-122.4218072),
"financial district" : (37.796062,-122.4056417),
"ghirardeli_sq" : (37.7975198,-122.4254257),
"outer_sunset" : (37.753550, -122.495344),
"ucsf" : (37.752057,-122.478607),
"stonestown" : (37.7302017,-122.4770621),
"design district" :(37.7689238,-122.4039097),
"forest hill" : (37.7480526,-122.4690046),
"mission bart" : (37.7500642,-122.4261985),
"dogpatch" : (37.757224,-122.3983142),
"mt_davidson" : (37.739037,-122.4583808),
"cal acad science": (37.7685138,-122.463402)
}

rides = {"galvanize": "pier 39",
"ggpark": "ggbridge",
"ggbridge": "sutro baths",
"sutro baths": "ggbridge",
"pier 39": "galvanize",
"twin peaks": "sf zoo",
"airport": "sf zoo",
"usf" : "sf zoo",
"glen park" : "airport",
"sf zoo" : "airport",
"dolores park" : "galvanize",
"AT_T": "tenderloin",
"castro": "galvanize",
"lombart": "ggpark",
"u_sq": "airport",
"china town": "lombart",
"baker beach": "sf zoo",
"painted ladies": "castro",
"embarcadero": "sutro baths",
"tenderloin": "galvanize",
"financial district" : "tenderloin",
"ghirardeli_sq" : "pier 39",
"outer_sunset" : "sf zoo",
"ucsf" : "twin peaks",
"stonestown" : "AT_T",
"design district" : "lombart",
"forest hill" : "dolores park",
"mission bart" : "china town",
"dogpatch" : "ghirardeli_sq",
"mt_davidson" : "ucsf",
"cal acad science": "galvanize"

}


def get_lyft(start,end):
	""" INPUT : Starting loation and ending location
	PROCESS: Makes a request to the UBER API to get the ride information
	OUTPUT : Json with the ride's information """

	url = "https://api.lyft.com/v1/cost"

	l_token = credentials["lyft_token"]

	headers = {"Authorization": "bearer " + l_token}

	start_lat,start_lng = locations[start]

	end_lat, end_lng = locations[end]

	parameters={"start_lat": start_lat, "start_lng": start_lng, "end_lat": end_lat, "end_lng": end_lng}

	lyft_ride_info = requests.get(url, params=parameters, headers=headers).json()

	return lyft_ride_info


def get_uber(start,end):
	""" INPUT : Starting loation and ending location
	PROCESS: Makes a request to the UBER API to get the ride information
	OUTPUT : Json with the ride's information """


	url = "https://api.uber.com/v1/estimates/price?"

	start_lat,start_lng = locations[start]

	end_lat, end_lng = locations[end]

	lat_long = "start_latitude={}&start_longitude={}&end_latitude={}&end_longitude={}"\
	.format(start_lat, start_lng, end_lat, end_lng)

	u_token = credentials["uber_token"]

	uber_ride_info = requests.get(url + lat_long + u_token).json()["prices"]

	return uber_ride_info


def connection():
	""" Connects to kinesis firehose, which internall
	connects to two different s3 bickets. One for uber and one for lyft
	and dumps the raw data from the api calls"""

	client = boto3.client('firehose', region_name="us-east-1")

	uber_json = {}
	lyft_json = {}

	for start,end in rides.items():
		uber_json[start] = {}
		lyft_json[start] = {}

		uber_json[start][end] = get_uber(start,end)
		lyft_json[start][end] = get_lyft(start,end)
		uber_json[start]["time"] = int(round(time.time()/60))
		lyft_json[start]["time"] = int(round(time.time()/60))

	response = client.put_record(
    DeliveryStreamName='uber_stream',
    Record={'Data': json.dumps(uber_json) + "\n"})

	response = client.put_record(
    DeliveryStreamName='lyft_stream',
    Record={'Data': json.dumps(lyft_json) + "\n"})


if __name__ == "__main__":

	credentials = yaml.load(open(os.path.expanduser('taxi.yaml')))

	connection()



