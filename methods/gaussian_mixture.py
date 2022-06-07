from sklearn.mixture import GaussianMixture
from methods.model import Model
from zipfile import ZipFile
import numpy as np

class GaussianMixturesModel(Model):
    def __init__(self, model_path: str):

        model_dir =  '/tmp/gm'
        with ZipFile(model_path, 'r') as ref:
            ref.extractall(model_dir)
            
        means = np.load(f'{model_dir}/gm_means.npy')
        covariances = np.load(f'{model_dir}/gm_covariances.npy')
        weights = np.load(f'{model_dir}/gm_weights.npy')
        
        gm = GaussianMixture(n_components = len(means), covariance_type='full')
        gm.precisions_cholesky_ = np.linalg.cholesky(np.linalg.inv(covariances))
        gm.weights_ = weights 
        gm.means_ = means
        gm.covariances_ = covariances 
        self.threshold = np.load(f'{model_dir}/gm_threshold.npy')
        
        self.gm = gm
    
    def predict(self, measurement) -> bool:
        cpu_usage, temperature = measurement
        scored = self.gm.score_samples([[cpu_usage, temperature]])
        
        outliers = scored < self.threshold
        
        # we just pass one sample for scoring so we have only 1 outlier candidate
        return outliers[0]