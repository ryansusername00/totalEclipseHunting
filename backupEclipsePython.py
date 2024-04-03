import requests
from datetime import datetime, timedelta

# Starting location for the drive - replace with actual coordinates
starting_latitude = 37.220511654446234
starting_longitude = -76.62429314439137

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


def fetch_weather_forecast(latitude, longitude, time_utc):
    # For demonstration, we're not using the time parameter because the API might not support it directly.
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,cloud_cover,weathercode,precipitation_probability"
    response = requests.get(url)
    return response.json()

def format_weather_forecast(weather_data, time_utc):
    # Simulate fetching the forecast for the specific time (not actually implemented)
    forecast_data = weather_data['hourly']
    temperatures = forecast_data['temperature_2m']
    cloud_cover = forecast_data['cloud_cover']
    precip_probability = forecast_data['precipitation_probability']
    return f"Forecast for {time_utc}: Temperature: {temperatures[0]}°C, Cloud Coverage: {cloud_cover[0]}%, Precipitation Probability: {precip_probability[0]}%"

def generate_google_maps_directions_url(origin, destination):
    origin_str = f"{origin[0]},{origin[1]}"
    destination_str = f"{destination[0]},{destination[1]}"
    return f"https://www.google.com/maps/dir/{origin_str}/{destination_str}"

data = """
16:42	5	30.6S	149	47.6W	6	11.7S	146	38.0W	5	50.2S	148	07.8W	1.043		11	81	159	02m27.5s
16:44	4	20.5S	145	29.6W	5	08.4S	143	00.6W	4	44.0S	144	13.0W	1.044		16	81	166	02m36.8s
16:46	3	21.2S	142	27.6W	4	12.3S	140	15.6W	3	46.4S	141	20.3W	1.045		19	81	171	02m44.2s
16:48	2	27.1S	140	01.8W	3	20.2S	137	59.5W	2	53.3S	138	59.7W	1.046		22	81	174	02m50.6s
16:50	1	36.2S	137	58.5W	2	30.8S	136	02.5W	2	03.3S	136	59.7W	1.047		25	81	178	02m56.3s
16:52	0	47.7S	136	10.6W	1	43.4S	134	19.0W	1	15.4S	135	14.1W	1.048		27	81	181	03m01.6s
16:54	0	01.0S	134	34.2W	0	57.6S	132	45.9W	0	29.1S	133	39.5W	1.048		29	81	183	03m06.4s
16:56	0	44.4N	133	06.9W	0	13.0S	131	21.1W	0	15.9N	132	13.5W	1.049		31	81	186	03m10.9s
16:58	1	28.6N	131	46.8W	0	30.6N	130	03.0W	0	59.7N	130	54.5W	1.05		33	82	188	03m15.2s
17:00	2	11.8N	130	32.7W	1	13.2N	128	50.5W	1	42.7N	129	41.2W	1.05		35	82	190	03m19.3s
17:02	2	54.2N	129	23.6W	1	55.1N	127	42.8W	2	24.8N	128	32.8W	1.05		37	82	192	03m23.1s
17:04	3	35.9N	128	18.8W	2	36.4N	126	39.1W	3	06.3N	127	28.6W	1.051		38	83	193	03m26.8s
17:06	4	17.0N	127	17.7W	3	17.0N	125	39.0W	3	47.2N	126	28.0W	1.051		40	83	194	03m30.3s
17:08	4	57.5N	126	19.9W	3	57.2N	124	42.0W	4	27.5N	125	30.6W	1.052		41	84	196	03m33.7s
17:10	5	37.5N	125	24.9W	4	36.8N	123	47.8W	5	07.3N	124	36.1W	1.052		43	84	197	03m36.9s
17:12	6	17.1N	124	32.5W	5	16.0N	122	56.0W	5	46.7N	123	44.0W	1.052		44	85	198	03m40.0s
17:14	6	56.3N	123	42.4W	5	54.8N	122	06.4W	6	25.6N	122	54.1W	1.053		46	86	199	03m42.9s
17:16	7	35.0N	122	54.2W	6	33.3N	121	18.7W	7	04.3N	122	06.2W	1.053		47	86	199	03m45.8s
17:18	8	13.5N	122	07.9W	7	11.4N	120	32.8W	7	42.5N	121	20.1W	1.053		48	87	200	03m48.5s
17:20	8	51.6N	121	23.2W	7	49.2N	119	48.5W	8	20.5N	120	35.6W	1.053		49	88	201	03m51.1s
17:22	9	29.4N	120	40.0W	8	26.8N	119	05.7W	8	58.2N	119	52.6W	1.054		51	89	201	03m53.6s
17:24	10	07.0N	119	58.1W	9	04.0N	118	24.2W	9	35.6N	119	10.9W	1.054		52	90	202	03m56.0s
17:26	10	44.3N	119	17.5W	9	41.1N	117	43.8W	10	12.7N	118	30.4W	1.054		53	91	202	03m58.4s
17:28	11	21.4N	118	37.9W	10	17.9N	117	04.6W	10	49.7N	117	51.0W	1.054		54	92	202	04m00.6s
17:30	11	58.3N	117	59.4W	10	54.4N	116	26.3W	11	26.4N	117	12.6W	1.055		55	93	202	04m02.7s
17:32	12	34.9N	117	21.7W	11	30.8N	115	49.0W	12	02.9N	116	35.1W	1.055		56	94	203	04m04.8s
17:34	13	11.4N	116	44.9W	12	07.0N	115	12.4W	12	39.3N	115	58.4W	1.055		57	96	203	04m06.7s
17:36	13	47.8N	116	08.8W	12	43.0N	114	36.6W	13	15.4N	115	22.5W	1.055		58	97	203	04m08.6s
17:38	14	23.9N	115	33.4W	13	18.9N	114	01.4W	13	51.4N	114	47.2W	1.055		59	99	203	04m10.3s
17:40	14	59.9N	114	58.5W	13	54.6N	113	26.8W	14	27.3N	114	12.5W	1.055		60	100	203	04m12.0s
17:42	15	35.8N	114	24.3W	14	30.1N	112	52.8W	15	03.0N	113	38.3W	1.056		61	102	203	04m13.6s
17:44	16	11.6N	113	50.4W	15	05.5N	112	19.2W	15	38.6N	113	04.6W	1.056		62	104	202	04m15.1s
17:46	16	47.2N	113	17.0W	15	40.8N	111	46.0W	16	14.0N	112	31.4W	1.056		63	105	202	04m16.5s
17:48	17	22.7N	112	44.0W	16	15.9N	111	13.3W	16	49.3N	111	58.4W	1.056		64	107	202	04m17.9s
17:50	17	58.1N	112	11.3W	16	51.0N	110	40.8W	17	24.5N	111	25.8W	1.056		64	109	202	04m19.1s
17:52	18	33.4N	111	38.8W	17	25.9N	110	08.6W	17	59.6N	110	53.5W	1.056		65	112	202	04m20.3s
17:54	19	08.6N	111	06.5W	18	00.7N	109	36.6W	18	34.7N	110	21.4W	1.056		66	114	202	04m21.4s
17:56	19	43.7N	110	34.4W	18	35.4N	109	04.8W	19	09.6N	109	49.4W	1.056		66	116	201	04m22.4s
17:58	20	18.8N	110	02.5W	19	10.1N	108	33.1W	19	44.4N	109	17.6W	1.056		67	119	201	04m23.4s
18:00	20	53.8N	109	30.6W	19	44.6N	108	01.5W	20	19.2N	108	45.8W	1.056		67	122	201	04m24.2s
18:02	21	28.7N	108	58.7W	20	19.1N	107	29.9W	20	53.8N	108	14.1W	1.056		68	125	200	04m25.0s
18:04	22	03.5N	108	26.8W	20	53.5N	106	58.4W	21	28.5N	107	42.4W	1.056		68	128	200	04m25.7s
18:06	22	38.3N	107	54.9W	21	27.8N	106	26.8W	22	03.0N	107	10.7W	1.056		69	131	200	04m26.3s
18:08	23	13.0N	107	22.8W	22	02.0N	105	55.1W	22	37.5N	106	38.8W	1.057		69	134	199	04m26.8s
18:10	23	47.7N	106	50.7W	22	36.2N	105	23.3W	23	11.9N	106	06.8W	1.057		69	137	199	04m27.2s
18:12	24	22.3N	106	18.3W	23	10.3N	104	51.4W	23	46.3N	105	34.7W	1.057		70	140	199	04m27.6s
18:14	24	56.9N	105	45.7W	23	44.4N	104	19.2W	24	20.6N	105	02.3W	1.057		70	144	198	04m27.9s
18:16	25	31.4N	105	12.9W	24	18.4N	103	46.8W	24	54.8N	104	29.7W	1.057		70	147	198	04m28.1s
18:18	26	05.9N	104	39.8W	24	52.3N	103	14.2W	25	29.1N	103	56.8W	1.057		70	151	197	04m28.2s
18:20	26	40.4N	104	06.3W	25	26.3N	102	41.2W	26	03.3N	103	23.6W	1.057		70	154	197	04m28.2s
18:22	27	14.8N	103	32.4W	26	00.1N	102	07.8W	26	37.4N	102	49.9W	1.057		70	157	197	04m28.1s
18:24	27	49.2N	102	58.0W	26	33.9N	101	34.0W	27	11.5N	102	15.9W	1.056		69	161	196	04m28.0s
18:26	28	23.6N	102	23.2W	27	07.7N	100	59.8W	27	45.6N	101	41.4W	1.056		69	164	196	04m27.7s
18:28	28	57.9N	101	47.8W	27	41.4N	100	25.1W	28	19.6N	101	06.3W	1.056		69	168	195	04m27.4s
18:30	29	32.2N	101	11.9W	28	15.1N	99	49.8W	28	53.6N	100	30.7W	1.056		68	171	195	04m27.0s
18:32	30	06.5N	100	35.3W	28	48.8N	99	13.9W	29	27.6N	099	54.5W	1.056		68	174	194	04m26.5s
18:34	30	40.8N	99	57.9W	29	22.4N	98	37.4W	30	01.5N	099	17.5W	1.056		68	177	194	04m26.0s
18:36	31	15.0N	99	19.9W	29	56.0N	98	00.1W	30	35.4N	098	39.9W	1.056		67	180	193	04m25.3s
18:38	31	49.3N	98	41.0W	30	29.6N	97	22.1W	31	09.3N	098	01.5W	1.056		66	183	193	04m24.5s
18:40	32	23.5N	98	01.3W	31	03.1N	96	43.3W	31	43.2N	097	22.2W	1.056		66	185	192	04m23.7s
18:42	32	57.6N	97	20.6W	31	36.6N	96	03.6W	32	17.0N	096	42.0W	1.056		65	188	192	04m22.7s
18:44	33	31.8N	96	38.8W	32	10.0N	95	23.0W	32	50.8N	096	00.8W	1.056		64	191	191	04m21.7s
18:46	34	05.9N	95	56.0W	32	43.4N	94	41.3W	33	24.6N	095	18.6W	1.056		64	193	191	04m20.6s
18:48	34	40.0N	95	12.1W	33	16.8N	93	58.5W	33	58.3N	094	35.2W	1.056		63	195	190	04m19.4s
18:50	35	14.1N	94	26.9W	33	50.1N	93	14.6W	34	32.0N	093	50.7W	1.055		62	198	189	04m18.0s
18:52	35	48.1N	93	40.3W	34	23.4N	92	29.5W	35	05.6N	093	04.8W	1.055		61	200	189	04m16.6s
18:54	36	22.1N	92	52.3W	34	56.6N	91	43.0W	35	39.2N	092	17.6W	1.055		60	202	188	04m15.1s
18:56	36	56.0N	92	02.8W	35	29.8N	90	55.0W	36	12.8N	091	28.9W	1.055		59	204	188	04m13.5s
18:58	37	29.9N	91	11.6W	36	02.9N	90	05.6W	36	46.3N	090	38.6W	1.055		58	206	187	04m11.8s
19:00	38	03.8N	90	18.7W	36	36.0N	89	14.5W	37	19.7N	089	46.6W	1.055		57	208	186	04m10.0s
19:02	38	37.5N	89	23.9W	37	09.0N	88	21.6W	37	53.1N	088	52.8W	1.054		56	210	186	04m08.1s
19:04	39	11.2N	88	27.0W	37	41.9N	87	26.9W	38	26.3N	087	57.0W	1.054		55	212	185	04m06.1s
19:06	39	44.8N	87	27.9W	38	14.7N	86	30.1W	38	59.5N	086	59.1W	1.054		54	214	184	04m04.0s
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


def parse_data_lines(data):
    """
    Generator to yield the universal standard time and the third set of latitude and longitude coordinates from each line of data.
    Each line of data is expected to have multiple columns separated by tabs, with the 7th/8th columns for latitude and the 9th/10th for longitude.
    """
    lines = data.strip().split("\n")
    for line in lines:
        parts = line.split("\t")
        time_utc = parts[0]
        # Adjust indices to match your data structure: 7th/8th for latitude, 9th/10th for longitude
        latDeg = parts[5]
        latMin = parts[6]
        longDeg = parts[7]
        longMin = parts[8]

        lat = " ".join([latDeg, latMin])   
        lng = " ".join([longDeg, longMin])
        yield time_utc, lat, lng


def main():
    for time_utc, lat, lng in parse_data_lines(data):
        latitude, longitude = parse_latitude(lat), parse_longitude(lng)
        weather_data = fetch_weather_forecast(latitude, longitude, time_utc)
        weather_forecast = format_weather_forecast(weather_data, time_utc)
        print(weather_forecast)

        maps_url = generate_google_maps_directions_url((starting_latitude, starting_longitude), (latitude, longitude))
        print(f"Google Maps URL: {maps_url}\n")

if __name__ == "__main__":
    main()