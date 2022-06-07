import time
import csv
import requests
import argparse

all_data = {}
temp_data = {}


def info_for_key(key: str):
    if key not in all_data or len(all_data[key]) == 0:
        return (None, None, 0)
    first = max(el[0] for el in all_data[key])
    last = min(el[0] for el in all_data[key])
    count = len(all_data[key])
    return first, last, count


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate CPU load')
    parser.add_argument('--url', type=str, default='http://10.6.0.5:12101',
                        help='Prometheus URL')
    parser.add_argument(
        '--source', type=str, default='node_exporter:9100', help='Name of Prometheus source')
    parser.add_argument('--range', type=int, default=72,
                        help='Number of hours to include [h]')
    args = parser.parse_args()

    PROMETHEUS_URL = args.url
    PROMETHEUS_SOURCE_NAME = args.source
    HOURS = args.range

    QUERY = f"100-rate(node_cpu_seconds_total{{mode='idle',instance='{PROMETHEUS_SOURCE_NAME}'}}[10s])*100"
    QUERY_TEMP = f'node_hwmon_temp_celsius{{instance="{PROMETHEUS_SOURCE_NAME}",job="node"}}'
    STEP = 10
    SINGLE_RANGE = 60 * 60 * 1
    TIMES = HOURS

    now = int(time.time())
    for i in reversed(range(TIMES)):
        start = now - SINGLE_RANGE*(i+1)
        end = now - SINGLE_RANGE*i
        res = requests.get(f'{PROMETHEUS_URL}/api/v1/query_range',  params={'query': QUERY,
                                                                            'start': start, 'end': end, 'step': STEP})
        res2 = requests.get(f'{PROMETHEUS_URL}/api/v1/query_range',  params={'query': QUERY_TEMP,
                                                                             'start': start, 'end': end, 'step': STEP})
        results = res.json()['data']['result']
        results_temp = res2.json()['data']['result']
        for result in results:
            key = str(result['metric']['cpu'])
            if not key in all_data:
                all_data[key] = []
            all_data[key].extend(result['values'])
        for result in results_temp:
            key = str(result['metric']['sensor'])
            if not key in temp_data:
                temp_data[key] = []
            temp_data[key].extend(result['values'])

    print(len(all_data['0']))
    print(info_for_key('0'))

    with open('cpu_measures.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['cpu', 'timestamp', 'usage'])
        for key in all_data:
            for el in all_data[key]:
                writer.writerow([key, *el])
    with open('temp_measures.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['sensor', 'timestamp', 'temperature'])
        for key in temp_data:
            for el in temp_data[key]:
                writer.writerow([key, *el])
