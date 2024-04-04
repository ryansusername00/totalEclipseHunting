import requests
import webbrowser
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

# Starting location for the drive - replace with actual coordinates
starting_latitude = 37.220511654446234
starting_longitude = -76.62429314439137

# Filter out any locations where cloud coverage is greater than this value
cloud_coverage_filter = 10 

# Date of eclipse
date_str = "2024-04-08"

def parse_latitude(lat):
    """Parses a latitude string with format 'degrees minutes direction' into a floating-point number in decimal degrees."""
    parts = lat.split()  # Split by whitespace to separate degrees, minutes, and direction
    degrees = float(parts[0])
    minutes = float(parts[1][:-1])  # Remove the direction ('S' or 'N') and convert to float
    direction = parts[1][-1]  # Get the direction

    # Convert to decimal degrees
    decimal_degrees = degrees + minutes / 60

    # If the direction is south, make the result negative
    if direction == 'S':
        decimal_degrees *= -1

    return decimal_degrees

def parse_longitude(lng):
    """Parses a longitude string with format 'degrees minutes direction' into a floating-point number in decimal degrees."""
    parts = lng.split()  # Split by whitespace to separate degrees, minutes, and direction
    degrees = float(parts[0])
    minutes = float(parts[1][:-1])  # Remove the direction ('E' or 'W') and convert to float
    direction = parts[1][-1]  # Get the direction

    # Convert to decimal degrees
    decimal_degrees = degrees + minutes / 60

    # If the direction is west, make the result negative
    if direction == 'W':
        decimal_degrees *= -1

    return decimal_degrees


def fetch_weather_forecast(latitude, longitude):
    # For demonstration, we're not using the time parameter because the API might not support it directly.
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,cloud_cover,weathercode,precipitation_probability"
    response = requests.get(url)
    return response.json()

class WeatherForecast:
    def __init__(self, forecast_time_str, temperature, cloud_coverage, precipitation_probability):
        self.forecast_time_str = forecast_time_str
        self.temperature = temperature
        self.cloud_coverage = cloud_coverage
        self.precipitation_probability = precipitation_probability

    def __repr__(self):
        # Parse the string to a datetime object assuming it's in UTC
        utc_time_obj = datetime.strptime(self.forecast_time_str, "%Y-%m-%dT%H:%M").replace(tzinfo=timezone.utc)
        # Convert UTC datetime to local time
        # might need to install tzdata ('pip install tzdata')
        local_time_obj = utc_time_obj.astimezone(ZoneInfo("America/New_York"))
        # Format it to 'YYYY-MM-DD HH:MM AM/PM' format
        formatted_time_str = local_time_obj.strftime("%Y-%m-%d %I:%M %p %Z")
        return (f"WeatherForecast(time='{formatted_time_str}', temperature={self.temperature}, "
                f"cloud_coverage={self.cloud_coverage}, precipitation_probability={self.precipitation_probability})")


def find_nearest_forecast_index(forecast_data, event_datetime):
    """Find the index of the forecast nearest to the specified event datetime."""
    forecast_times = forecast_data['time']
    # Convert forecast times to datetime objects
    forecast_datetimes = [datetime.strptime(time, "%Y-%m-%dT%H:%M").replace(tzinfo=event_datetime.tzinfo) for time in forecast_times]
    
    # Ensure event_datetime is within the range of forecast times
    if not (forecast_datetimes[0] <= event_datetime <= forecast_datetimes[-1]):
        raise ValueError(f"Event datetime {event_datetime} is out of the forecast data range.")
    
    # Find the index of the forecast time closest to the event datetime
    closest_index = min(range(len(forecast_datetimes)), key=lambda i: abs(forecast_datetimes[i] - event_datetime))
    
    return closest_index

def create_event_datetime(time_str):
    """Creates a UTC datetime object from date and time strings."""
    combined_str = f"{date_str}T{time_str}"
    event_datetime = datetime.strptime(combined_str, "%Y-%m-%dT%H:%M").replace(tzinfo=timezone.utc)
    return event_datetime

def parse_weather_response(weather_data, time_str):
    forecast_data = weather_data['hourly']
    # Convert totality event time to datetime
    event_datetime = create_event_datetime(time_str)
     # Find the index of the nearest forecast time
    i = find_nearest_forecast_index(weather_data['hourly'], event_datetime)

    # Extract the weather data for the closest time
    forecast_time_str = forecast_data['time'][i]  # response looks like '2024-04-03T01:00' or '2024-04-03T09:00
    temperature = forecast_data['temperature_2m'][i]
    cloud_coverage = forecast_data['cloud_cover'][i]
    precipitation_probability = forecast_data['precipitation_probability'][i]

    # Create a WeatherForecast object with the weather information
    forecast = WeatherForecast(forecast_time_str, temperature, cloud_coverage, precipitation_probability)
    return forecast

def generate_google_maps_directions_url(origin, destination):
    origin_str = f"{origin[0]},{origin[1]}"
    destination_str = f"{destination[0]},{destination[1]}"
    return f"https://www.google.com/maps/dir/{origin_str}/{destination_str}"

# Total Solar Eclipse of 2024 Apr 08
# https://eclipse.gsfc.nasa.gov/SEpath/SEpath2001/SE2024Apr08Tpath.html
data = """
19:08	40	18.2N	86	26.5W	38	47.4N	85	31.1W	39	32.6N	085	58.9W	1.054		53	216	183	04m01.7s
19:10	40	51.6N	85	22.6W	39	19.9N	84	29.8W	40	05.6N	084	56.3W	1.054		52	217	183	03m59.4s
19:12	41	24.8N	84	15.9W	39	52.4N	83	26.0W	40	38.4N	083	51.1W	1.053		51	219	182	03m56.9s
19:14	41	57.8N	83	06.3W	40	24.7N	82	19.4W	41	11.0N	082	43.0W	1.053		50	221	181	03m54.4s
19:16	42	30.6N	81	53.4W	40	56.8N	81	09.9W	41	43.5N	081	31.9W	1.053		48	223	180	03m51.7s
19:18	43	03.2N	80	37.0W	41	28.7N	79	57.1W	42	15.8N	080	17.4W	1.052		47	224	179	03m48.9s
19:20	43	35.6N	79	16.9W	42	00.4N	78	40.9W	42	47.8N	078	59.2W	1.052		46	226	179	03m45.9s
19:22	44	07.6N	77	52.5W	42	31.8N	77	20.8W	43	19.5N	077	37.0W	1.052		44	228	178	03m42.8s
19:24	44	39.3N	76	23.6W	43	02.9N	75	56.5W	43	50.9N	076	10.5W	1.052		43	230	177	03m39.6s
19:26	45	10.6N	74	49.6W	43	33.7N	74	27.6W	44	21.9N	074	39.1W	1.051		41	232	176	03m36.3s
19:28	45	41.4N	73	10.0W	44	04.0N	72	53.5W	44	52.4N	073	02.4W	1.051		40	234	175	03m32.8s
19:30	46	11.6N	71	24.2W	44	33.8N	71	13.8W	45	22.4N	071	19.7W	1.05		38	236	173	03m29.1s
19:32	46	41.1N	69	31.3W	45	03.0N	69	27.7W	45	51.8N	069	30.3W	1.05		37	238	172	03m25.2s
19:34	47	09.8N	67	30.4W	45	31.6N	67	34.4W	46	20.5N	067	33.4W	1.05		35	240	171	03m21.2s
19:36	47	37.5N	65	20.4W	45	59.3N	65	32.8W	46	48.2N	065	27.8W	1.049		33	242	170	03m17.0s
19:38	48	04.0N	62	59.9W	46	26.0N	63	21.8W	47	14.8N	063	12.1W	1.049		31	244	168	03m12.5s
19:40	48	29.1N	60	26.8W	46	51.5N	60	59.6W	47	40.1N	060	44.7W	1.048		29	247	167	03m07.7s
19:42	48	52.2N	57	38.5W	47	15.4N	58	24.0W	48	03.7N	058	03.1W	1.047		27	249	165	03m02.7s
19:44	49	13.0N	54	31.6W	47	37.4N	55	32.1W	48	25.1N	055	03.9W	1.047		25	252	163	02m57.2s
19:46	49	30.6N	51	00.3W	47	56.9N	52	19.4W	48	43.7N	051	42.4W	1.046		22	255	161	02m51.3s
19:48	49	43.5N	46	55.5W	48	12.7N	48	38.8W	48	58.2N	047	50.4W	1.045		20	259	159	02m44.8s
19:50	49	49.3N	41	59.5W	48	23.3N	44	17.7W	49	06.6N	043	13.1W	1.044		16	263	156	02m37.3s
19:52	49	41.3N	35	27.0W	48	24.7N	38	48.5W	49	03.9N	037	15.7W	1.043		12	268	153	02m28.2s
"""

# startIndex = 1 for northern limit
# startIndex = 5 for southern limit
# startIndex = 9 for central line
def parse_data_lines(data, startIndex = 5):
    """
    Generator to yield the universal standard time and the third set of latitude and longitude coordinates from each line of data.
    Each line of data is expected to have multiple columns separated by tabs. Using the Central Line coordinates.
    """
    lines = data.strip().split("\n")
    for line in lines:
        parts = line.split("\t")
        time_utc = parts[0]
        # Using central line coordinates
      
        # startIndex = 5 for 5/6/7/8 for southern limit
        # startIndex = 9 for 9/10/11/12 for central line
        startIndex = 5
        latDeg =  parts[startIndex]
        latMin =  parts[startIndex + 1]
        longDeg = parts[startIndex + 2]
        longMin = parts[startIndex + 3]

        lat = " ".join([latDeg, latMin])   
        lng = " ".join([longDeg, longMin])
        yield time_utc, lat, lng


def open_directions_if_clear(forecast, coords):
    # Opens Google Maps directions in a web browser if the cloud coverage for coordinate is less than specified filter
    if forecast.cloud_coverage < cloud_coverage_filter:
        directions_url = generate_google_maps_directions_url((starting_latitude, starting_longitude), coords)
        print(f"Google Maps URL: {directions_url}\n")
        webbrowser.open_new_tab(directions_url)

def main():
    southernPoints = parse_data_lines(data, 5)
    centerPoints = parse_data_lines(data, 9)
    combinedData = zip(southernPoints, centerPoints)
    
    for (time_utc_s, lat_s, lng_s), (_, lat_c, lng_c) in combinedData:
        # Process southern point
        latitude_s, longitude_s = parse_latitude(lat_s), parse_longitude(lng_s)
        weather_response_s = fetch_weather_forecast(latitude_s, longitude_s)
        weather_forecast_s = parse_weather_response(weather_response_s, time_utc_s)
        print(f"Southern Point Forecast for ({latitude_s}, {longitude_s}): {weather_forecast_s}")
        open_directions_if_clear(weather_forecast_s, (latitude_s, longitude_s))

        # Process center point
        latitude_c, longitude_c = parse_latitude(lat_c), parse_longitude(lng_c)
        weather_response_c = fetch_weather_forecast(latitude_c, longitude_c)
        weather_forecast_c = parse_weather_response(weather_response_c, time_utc_s)
        print(f"Center Point Forecast for ({latitude_c}, {longitude_c}): {weather_forecast_c}")
        open_directions_if_clear(weather_forecast_c, (latitude_c, longitude_c))

if __name__ == "__main__":
    main()
    
    
    
    
    
# removed these from data set to start somewhere more reasonable
# 18:32	30	06.5N	100	35.3W	28	48.8N	99	13.9W	29	27.6N	099	54.5W	1.056		68	174	194	04m26.5s
# 18:34	30	40.8N	99	57.9W	29	22.4N	98	37.4W	30	01.5N	099	17.5W	1.056		68	177	194	04m26.0s
# 18:36	31	15.0N	99	19.9W	29	56.0N	98	00.1W	30	35.4N	098	39.9W	1.056		67	180	193	04m25.3s
# 18:38	31	49.3N	98	41.0W	30	29.6N	97	22.1W	31	09.3N	098	01.5W	1.056		66	183	193	04m24.5s
# 18:40	32	23.5N	98	01.3W	31	03.1N	96	43.3W	31	43.2N	097	22.2W	1.056		66	185	192	04m23.7s
# 18:42	32	57.6N	97	20.6W	31	36.6N	96	03.6W	32	17.0N	096	42.0W	1.056		65	188	192	04m22.7s
# 18:44	33	31.8N	96	38.8W	32	10.0N	95	23.0W	32	50.8N	096	00.8W	1.056		64	191	191	04m21.7s
# 18:46	34	05.9N	95	56.0W	32	43.4N	94	41.3W	33	24.6N	095	18.6W	1.056		64	193	191	04m20.6s
# 18:48	34	40.0N	95	12.1W	33	16.8N	93	58.5W	33	58.3N	094	35.2W	1.056		63	195	190	04m19.4s
# 18:50	35	14.1N	94	26.9W	33	50.1N	93	14.6W	34	32.0N	093	50.7W	1.055		62	198	189	04m18.0s
# 18:52	35	48.1N	93	40.3W	34	23.4N	92	29.5W	35	05.6N	093	04.8W	1.055		61	200	189	04m16.6s
# 18:54	36	22.1N	92	52.3W	34	56.6N	91	43.0W	35	39.2N	092	17.6W	1.055		60	202	188	04m15.1s
# 18:56	36	56.0N	92	02.8W	35	29.8N	90	55.0W	36	12.8N	091	28.9W	1.055		59	204	188	04m13.5s
# 18:58	37	29.9N	91	11.6W	36	02.9N	90	05.6W	36	46.3N	090	38.6W	1.055		58	206	187	04m11.8s
# 19:00	38	03.8N	90	18.7W	36	36.0N	89	14.5W	37	19.7N	089	46.6W	1.055		57	208	186	04m10.0s
# 19:02	38	37.5N	89	23.9W	37	09.0N	88	21.6W	37	53.1N	088	52.8W	1.054		56	210	186	04m08.1s
# 19:04	39	11.2N	88	27.0W	37	41.9N	87	26.9W	38	26.3N	087	57.0W	1.054		55	212	185	04m06.1s
# 19:06	39	44.8N	87	27.9W	38	14.7N	86	30.1W	38	59.5N	086	59.1W	1.054		54	214	184	04m04.0s