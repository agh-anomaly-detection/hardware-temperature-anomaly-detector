from typing import List
import os
import psutil
from methods.gaussian_mixture import GaussianMixturesModel


MODELS_PATH = os.getenv("MODELS_PATH", "./models")
ANOMALIES_OUTPUT = os.getenv("ANOMALIES_OUTPUT", "./textfiles")

def fetch_measurement() -> tuple[float, float]:
    """
    Reads the current CPU usage and CPU temperature
    and returns them as a tuple.
    """

    cpu_usage = psutil.cpu_percent()
    
    try:
        temperature = float(os.popen('cat /sys/class/thermal/thermal_zone0/temp').readline().replace("\n", "")) / 1000
    except Exception:
        # This is for testing on non-raspberry environments...
        temperature = 50.0
        pass


    return (cpu_usage, temperature)

def save_predictions(path: str, predictions: List[tuple[str, bool]]):
    lines = ["# TYPE node_fan_anomaly gauge\n"]
    
    for model_name, prediction in predictions:
        lines.append(f"node_fan_anomaly{{model=\"{model_name}\"}} {1 if prediction else 0}\n")
    with open(path, "w") as fd:
        fd.writelines(lines)
         

if __name__ == "__main__":
    print("Initializing models...")
    models =  {
        "gaussian_mixtures": GaussianMixturesModel(model_path=f"{MODELS_PATH}/gm.zip"),
    }
    print("Models initialized!")

    measurement = fetch_measurement()
    print(f"Recording CPU load and temperature, load: {measurement[0]}%, temperature: {measurement[1]}C")
    predictions = []

    print("Predicting an anomaly...")
    for model_name, model in models.items():
        predictions.append((model_name, model.predict(measurement)))
        
    # NOTE: choose appropriate directory of the `fan_anomaly.prom` so that
    # node exporter can use that
    print("Saving predictions to file...")
    save_predictions(f"{ANOMALIES_OUTPUT}/fan_anomaly.prom", predictions)
