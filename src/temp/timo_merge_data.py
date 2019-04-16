import pandas as pd

airport_data = '/data/timo/Atlanta_departure_flights_2.csv'
weather_data = '/data/timo/atlanta_weather_2.csv'

airport_df = pd.read_csv(airport_data)
weather_df = pd.read_csv(weather_data)

airport_df.drop(['Unnamed: 0', 'YEAR', 'FL_DATE', 'COMBINED', 'OP_UNIQUE_CARRIER', 'ORIGIN_AIRPORT_ID', 'ORIGIN_AIRPORT_SEQ_ID', 'ORIGIN', 'ORIGIN_CITY_NAME', 'ORIGIN_STATE_NM', 'DEST_AIRPORT_ID', 'DEST_AIRPORT_SEQ_ID', 'DEST', 'DEST_CITY_NAME', 'DEST_STATE_NM', 'CRS_DEP_TIME', 'DEP_TIME', 'DEP_DELAY_NEW', 'DEP_DEL15', 'WHEELS_OFF', 'WHEELS_OFF.1', 'WHEELS_ON', 'WHEELS_ON.1', 'TAXI_IN', 'CRS_ARR_TIME', 'CRS_ARR_TIME.1', 'ARR_TIME', 'ARR_TIME.1', 'ARR_DELAY', 'ARR_DELAY_NEW', 'ARR_DEL15', 'DIVERTED', 'CRS_ELAPSED_TIME', 'ACTUAL_ELAPSED_TIME', 'AIR_TIME', 'FLIGHTS', 'CARRIER_DELAY', 'WEATHER_DELAY', 'NAS_DELAY', 'SECURITY_DELAY', 'LATE_AIRCRAFT_DELAY'], axis=1, inplace=True)

weather_df.drop(['Unnamed: 0', 'STATION', 'DATE', 'TIME', 'COMBINED', 'LATITUDE', 'LONGITUDE', 'ELEVATION', 'NAME'], axis=1, inplace=True)

airport_df.sort_values(by='EPOCH_TIME_STAMP', inplace=True)
weather_df.sort_values(by='EPOCH_TIME_STAMP', inplace=True)

merge_df = pd.DataFrame()

for air_index, air_row in airport_df.iterrows():
    depart_time = air_row['EPOCH_TIME_STAMP']
    lowest_dif_time = 1514848740
    lowest_dif_row = 0
    print('index', air_index)

    for wea_index, wea_row in weather_df.iterrows():
        weather_time = wea_row['EPOCH_TIME_STAMP']

        dif_time = abs(depart_time - weather_time)
        if lowest_dif_time >= dif_time:
            lowest_dif_time = dif_time
            lowest_dif_row = wea_row
        else:
            break

    lowest_dif_row.rename({'EPOCH_TIME_STAMP': 'EPOCH_TIME_STAMP_WEATHER'})
    merge_row = pd.concat([air_row, lowest_dif_row], axis=0)

    merge_df = merge_df.append(pd.DataFrame(merge_row).transpose())

merge_df.to_csv('/data/timo/atlanta_merge_data.csv')