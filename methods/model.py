from abc import ABC, abstractmethod

class Model(ABC):
    @abstractmethod
    def __init__(self, model_path: str) -> None:
        pass
    
    @abstractmethod
    def predict(self, measurement: tuple[float, float]) -> bool:
        pass