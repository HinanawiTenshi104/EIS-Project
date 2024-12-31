import importlib.util
import types

import numpy as np

# Load Components.py
print("---Loading Components---")
Components_py_Path = "Modules/Components.py"

spec = importlib.util.spec_from_file_location("Components", Components_py_Path)
ComponentModule = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ComponentModule)

# Filling Components Dict
circuitPrototypeComponents = {}
allAttributes = dir(ComponentModule)
componentNames = [attr for attr in allAttributes if not attr.startswith("__")]
componentNames.remove("ComponentBase")

for componentName in componentNames:
    ref = getattr(ComponentModule, componentName)
    if isinstance(ref, type):
        circuitPrototypeComponents[componentName] = ref()
    else:
        print(f"Model Settings: The ref of {componentName} is not a type")


class Circuit:
    displayName = ""
    componentNames = []
    structure = []

    components = []
    componentDisplayNames = []
    varmaps = []

    def __init__(self, circuitInfo: dict = None):
        if circuitInfo == None:
            circuitInfo = {
                "Display Name": "New Circuit",
                "Component Names": [],
                "Structure": [],
            }

        self.displayName = circuitInfo["Display Name"]
        self.componentNames = circuitInfo["Component Names"]
        self.structure = circuitInfo["Structure"]

        self.updateComponentInfos()

    def __populateComponents(self):
        self.components = []
        for componentName in self.componentNames:
            componentRef = getattr(ComponentModule, componentName)
            if componentRef is not None and isinstance(componentRef, type):
                self.components.append(componentRef())
            else:
                raise ValueError(f"Class {componentName} not found or is not a type")

    def __populateVarMaps(self):
        self.varmaps = []
        for component in self.components:
            if hasattr(component, "varmap"):
                varmap = component.varmap
                if isinstance(varmap, dict):
                    self.varmaps.append(varmap)
                    continue

                if isinstance(varmap, str) and varmap == "Ignore":
                    continue

            raise ValueError(
                f"Component {component.__class__.__name__}'s varmap not found or is invaild"
            )

    def __populateComponentDisplayNames(self):
        self.componentDisplayNames = []
        for component in self.components:
            if hasattr(component, "displayName") and isinstance(
                component.displayName, str
            ):
                self.componentDisplayNames.append(component.displayName)
            else:
                print(
                    f"Component {component.__class__.__name__}'s displayName not found or is not a str, use its class name instead"
                )
                self.componentDisplayNames.append(component.__class__.__name__)

    def updateComponentInfos(self):
        self.__populateComponents()
        self.__populateComponentDisplayNames()
        self.__populateVarMaps()

    def GetBoundTypes(self, dataInfo: dict) -> dict:
        boundTypes = {}
        for component in self.components:
            if hasattr(component, "GetBoundType") and isinstance(
                component.GetBoundType, types.MethodType
            ):
                boundType = component.GetBoundType(dataInfo)
                for key, val in boundType.items():
                    boundTypes[key] = val
            else:
                raise ValueError(
                    f"Component {component.__class__.__name__}'s GetBoundType not found or is not a MethodType"
                )

        return boundTypes

    def UpdateParameters(self, parameters: list[float]):
        varCounts = []
        for varmap in self.varmaps:
            varCounts.append(sum(varmap.values()))

        totalVarCount = sum(varCounts)
        if totalVarCount != len(parameters):
            raise ValueError(
                f"给定的参数数量与电路模型{self.__class__.__name__}所定义的数量不一致！"
            )

        paras = []
        index = 0
        for count in varCounts:
            paras.append(parameters[index : index + count])
            index += count

        for component, para in zip(self.components, paras):
            if hasattr(component, "UpdateParameters") and isinstance(
                component.UpdateParameters, types.MethodType
            ):
                component.UpdateParameters(para)
            else:
                raise ValueError(
                    f"Component {component.__class__.__name__}'s UpdateParameters not found or is not a MethodType"
                )

    def ImpedancesAnalyse(self, f: np.ndarray) -> np.ndarray:
        w = 2 * np.pi * f

        impedance = 0 + 0j
        start = 0
        for cut in self.structure:
            circuitSection = self.components[start:cut]
            length = len(circuitSection)
            if length == 0:
                raise ValueError(f"电路切片有问题！结构:{self.structure}")

            # Just Series
            elif length == 1:
                component = circuitSection[0]
                if hasattr(component, "Impedance"):
                    impedance += component.Impedance(w)
                else:
                    raise ValueError(
                        f"模块{component.__class__.__name__}没有Impedance方法!"
                    )

            # Has Parallel Part
            elif length > 1:
                admittance = 0 + 0j
                for component in circuitSection:
                    if hasattr(component, "Impedance"):
                        admittance += 1 / component.Impedance(w)
                    else:
                        raise ValueError(
                            f"模块{component.__class__.__name__}没有Impedance方法!"
                        )

                impedance += 1 / admittance

            start = cut

        return impedance

    def ImpedancesDerivativeAnalyse(self, f: np.ndarray) -> np.ndarray:
        pass
