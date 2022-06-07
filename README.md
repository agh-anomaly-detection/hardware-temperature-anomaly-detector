# Raspberry PI Anomaly detector

## What is required
- Python3 (packages: numpy, sklearn, pandas)
- All the requirements can be found inside `requirements.txt`
    
# How it works
- all implemented models get loaded into memory
- a measurement gets recorded: current CPU percentage usage and CPU temperature (method works only for raspberry pi).
- the measurement gets passed to each model to check for potential anomaly
- the anomaly results get saved to `$ANOMALIES_OUTPUT/fan_anomaly.prom` prometheus compatible file
  as a series of `gauge` measurements as follows `node_fan_anomaly{model="here goes model name"} 1/0` where `1/0` is either
  `1` for an anomaly and `0` for a normal measurement
    
## How to run
To run the script just use
`python3 main.py`

*NOTE*
The script can take 2 environmental variables:
- `MODELS_PATH` - path pointing to pre-trained models (defaults to `./models`)
- `ANOMALIES_OUTPUT` - output directory where the `fan_anomaly.prom` file will get saved (defaults to `./textfiles`)
    
## Currently implemented models
- Gaussian Mixtures
    
## Grafana dashboard
Besides `fan_anomaly.prom` file that gets generated on each script execution one can utilize the
`grafana_anomalies_dashboard.json` to visualize the anomalies for each model in a time series fashion.

The `fan_anomaly.prom` can be used by `node exporter` tool as a textfile source. Make sure
that you correctly set up the necessary paths.

