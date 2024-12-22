import requests
from datetime import datetime


def get_response(stationCode="5100002"):
    return requests.get(f'https://kalkulatorkolejowy.pl/bilkom/api/nextdeparture/extended/{stationCode}').json()[0]


def get_data(response):
    departure_time = response['timestamp']
    reload_time = departure_time + int(response['delay']*60)
    departure_time_object = datetime.fromtimestamp(int(departure_time))
    departure_time = departure_time_object.strftime("%H:%M")
    return {
        'train_code': response['trainCode'],
        'track_and_platform': find_valid_track_and_platform(response),
        'arrival_station': response['arrivalStation'],
        'delay': response['delay'],
        'departure_time': departure_time,
        'reload_time': reload_time,
        'intermediate_stations': get_intermediate_stations(response),
        'this_station': response['currentStation'],
        'amenities': response['amenities'],
        'train_name': get_train_name(response),
    }


def get_intermediate_stations(response):
    via = response['via']
    intermediate_stations = []

    for station in via:
        if station['thisStation'] == False and station['beforeThis'] == False:
            intermediate_stations.append(station['station'])

    return intermediate_stations


def get_train_name(response):
    # the train name is has four CAPITAL LETTERS at its start and is not the word UWAGA
    amenities = response['amenities']
    for amenity in amenities:
        if amenity[0].isupper() and amenity[1].isupper() and amenity[2].isupper() and amenity[3].isupper() and amenity [0:4] != "UWAG":
            amenity = amenity.split(":")
            return f"{amenity[0]}"
    return ""


def find_valid_track_and_platform(response):
    track = response["track"]
    platform = response["platform"]
    if track == "podroz" and platform == '<a class="btn btn-primary" href="':
        return ""
    return f"{platform}/{track}"


def main():
    parameters = get_data(get_response("5100002"))
    print(f"{parameters['this_station']} | {parameters['track_and_platform']}")
    print(f"{parameters["train_code"]} {parameters["train_name"]} - {parameters["arrival_station"]}")
    print(f"{parameters["departure_time"]} (+{parameters["delay"]})")
    for station in parameters['intermediate_stations']:
        print(f"> {station}", end=" ")
    print()


if __name__ == "__main__":
    main()