import types

import numpy as np


class Model:
    circuit = None

    def __init__(self, circuit):
        self.circuit = circuit

    def ImpedancesAnalyse(self, f: np.ndarray) -> np.ndarray:
        impedance = 0 + 0j
        if hasattr(self.circuit, "ImpedancesAnalyse") and isinstance(
            self.circuit.ImpedancesAnalyse, types.MethodType
        ):
            impedance = self.circuit.ImpedancesAnalyse(f)
        else:
            raise ValueError(
                f"电路模型{self.circuit.__class__.__name__}没有ImpedancesAnalyse方法!"
            )

        return impedance

    def ImpedancesDerivativeAnalyse(self, f: np.ndarray) -> np.ndarray:
        derivative = 0 + 0j
        if hasattr(self.circuit, "ImpedancesDerivativeAnalyse") and isinstance(
            self.circuit.ImpedancesDerivativeAnalyse, types.MethodType
        ):
            derivative = self.circuit.ImpedancesDerivativeAnalyse(f)
        else:
            raise ValueError(
                f"电路模型{self.circuit.__class__.__name__}没有ImpedancesDerivativeAnalyse方法!"
            )

        return derivative

    def GetBoundTypes(self, dataInfo: dict) -> dict:
        boundTypes = {}
        if hasattr(self.circuit, "GetBoundTypes") and isinstance(
            self.circuit.GetBoundTypes, types.MethodType
        ):
            boundTypes = self.circuit.GetBoundTypes(dataInfo)
        else:
            raise ValueError(
                f"电路模型{self.circuit.__class__.__name__}没有GetBoundTypes方法!"
            )

        return boundTypes

    def UpdateParameters(self, parameters: list[float]):
        if hasattr(self.circuit, "UpdateParameters") and isinstance(
            self.circuit.UpdateParameters, types.MethodType
        ):
            self.circuit.UpdateParameters(parameters)
        else:
            raise ValueError(
                f"电路模型{self.circuit.__class__.__name__}没有UpdateParameters方法!"
            )
