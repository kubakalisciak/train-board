import train_api as train
import weather_api as weather
import datetime as dt
import time


def reload_train_api(station_code):
    train_data = train.get_data(train.get_response(station_code))
    print_train_data(train_data)
    while True:
        try:
            time.sleep(60)
            time_now = dt.datetime.now()
            epoch_now = time_now.timestamp()
            if epoch_now - 60 > int(train_data['reload_time']):
                print_train_data(train.get_data(train.get_response(station_code)))
            else: pass
        except KeyboardInterrupt:
            break


def print_train_data(train_data):
    print(f"{train_data['train_code']} {train_data['train_name']} - {train_data['arrival_station']}")
    print(f"{train_data['departure_time']} (+{train_data['delay']})")
    for station in train_data['intermediate_stations']:
        print(f"> {station}", end=" ")
    print()


print(reload_train_api('5100002'))