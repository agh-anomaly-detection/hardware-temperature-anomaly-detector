import numpy as np
import pandas as pd
from sklearn.mixture import GaussianMixture
from zipfile import ZipFile
import os


MODELS_PATH = os.getenv("MODELS_PATH", "./models")


if __name__ == "__main__":
    print("Training Gaussian Mixture model...")
    # TODO replace with local file
    df = pd.read_csv('https://raw.githubusercontent.com/def-au1t/AGH_8_AI-Project/master/out_rpi_fan_25_steps1_baseline.csv')
    df.sort_values(by=['timestamp'], inplace=True)
    df_out = pd.DataFrame(columns=['usage', 'temperature'])
    df_out['usage'] = df['usage']
    df_out['temperature'] = df['temperature']


    gm = GaussianMixture(n_components=1, covariance_type='full').fit(df_out)
    scores = gm.score_samples(df_out)
    thresh = np.min(scores)


    print(f'Gaussian Mixture model trained. Anomaly threshold: {thresh}')

    print("Saving model to file...")
    np.save('gm_weights', gm.weights_, allow_pickle=False)
    np.save('gm_means', gm.means_, allow_pickle=False)
    np.save('gm_covariances', gm.covariances_, allow_pickle=False)
    np.save('gm_threshold', thresh, allow_pickle=False)
    file = ZipFile(f'{MODELS_PATH}/gm.zip', 'w')
    file.write('gm_covariances.npy')
    file.write('gm_means.npy')
    file.write('gm_threshold.npy')
    file.write('gm_weights.npy')
    file.close()
    os.remove('gm_weights.npy')
    os.remove('gm_means.npy')
    os.remove('gm_covariances.npy')
    os.remove('gm_threshold.npy')

    print("Model saved!")