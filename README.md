# Raspberry PI Anomaly detector

### What is required

- Python3 (packages: numpy, sklearn, pandas)
- All the requirements can be found inside `requirements.txt`

## How it works

- all implemented models get loaded into memory
- a measurement gets recorded: current CPU percentage usage and CPU temperature (method works only for raspberry pi).
- the measurement gets passed to each model to check for potential anomaly
- the anomaly results get saved to `$ANOMALIES_OUTPUT/fan_anomaly.prom` prometheus compatible file
  as a series of `gauge` measurements as follows `node_fan_anomaly{model="here goes model name"} 1/0` where `1/0` is either
  `1` for an anomaly and `0` for a normal measurement

### Hot to fetch data for training

The anomaly detection needs enought temperature and CPU correlation data to train the models properly. The easiest way to collect data is to use **Prometheus** and **Node Exporter** on Raspberry PI, as these tools collect all necessary data.
For fetching data from Prometheus use prepared script:

```
python data_loader/fetch_data.py --url <PROMETHEUS_URL> --range <RANGE_IN_HOURS> --source <PROMETHEUS_DATA_SOURCE>
```

For generating data with different CPU usage, using `data_loader/raspberry_loadgen.py` script is recommended.

### How to generate model

To run the script that generates Gaussian Mixture model just use:

```sh
python models_generation/gaussian_mixture.py
```

### How to run

To run the script just use

```sh
python main.py
```

_NOTE_
The script can take 2 environmental variables:

- `MODELS_PATH` - path pointing to pre-trained models (defaults to `./models`)
- `ANOMALIES_OUTPUT` - output directory where the `fan_anomaly.prom` file will get saved (defaults to `./textfiles`)

### Currently implemented models

- Gaussian Mixtures

### Grafana dashboard

Besides `fan_anomaly.prom` file that gets generated on each script execution one can utilize the
`grafana_anomalies_dashboard.json` to visualize the anomalies for each model in a time series fashion.

The `fan_anomaly.prom` can be used by `node exporter` tool as a textfile source. Make sure
that you correctly set up the necessary paths.

#### Example dashboard

![Grafana dashboard](/media/grafana_dashboard.png)

---

## Video demo:

### Overheating anomaly detection

### Restoring to normal work params
