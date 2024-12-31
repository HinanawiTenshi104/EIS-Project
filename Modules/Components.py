import numpy as np
import schemdraw
import schemdraw.elements as elm

"""
class ComponentExample(ComponentBase):
    VarA1 = 0
    VarA2 = 0
    VarB = 0

    def __init__(self):
        super().__init__()
        self.varmap = {"VarA": 2, "VarB": 1}
        self.displayName = "The Name Shown In the Result Page"
    
    def Impedance(self, w: np.ndarray)->np.ndarray:
        # your implementation here
        # return the impedance under the circular frequency w (w = 2*pi*f)
        # remember to np.conj() the result when you're done
    
    # Optional
    def Derivative(self, w: np.ndarray)->np.ndarray:
        # your implementation here
        # return the derivative of the impedance under the circular frequency w (w = 2*pi*f)
        # remember to np.conj() the result when you're done
    
    def GetBoundType(self, dataInfo: dict) -> dict:
        # your implementation here
        # should have the same key as varmap
        #
        # Example:
        # boundType = {"ValA": (10.4, 10.5), "ValB": (0.114, 0.514)}
        # return content
        
        # dataInfo contains data impedance's:
        # dataInfo["Real Min"], dataInfo["Real Max"], dataInfo["Real Width"]
    
    # Optional
    def UpdateParameters(self, parameters: list[float]):
        # it'll inherit from ComponentBase, but you can rewrite your own(not recommended)
    
    # Optional
    def DerivedQuantities(self) -> dict:
        # your implementation here
        # things you'd like to show in the result page
        #
        # Example:
        # content = {}
        # VarC = VarA * VarB / 10
        # content["VarC_DisplayName"] = VarC
        # return content
    
    # Optional
    def GetDiagram() -> schemdraw.Drawing:
        with schemdraw.Drawing(show=False) as diagram:
            # your diagram here

        return diagram
"""


class ComponentBase:
    varmap = {}
    displayName = ""

    def __init__(self):
        pass

    def UpdateParameters(self, parameters: list[float]):
        totalVarCount = sum(self.varmap.values())
        if totalVarCount != len(parameters):
            raise ValueError(
                f"传入的参数数量与模块{self.__class__.__name__}所定义的数量不一致！"
            )

        index = 0
        for varName, varCount in self.varmap.items():
            if varCount == 1:
                setattr(self, varName, parameters[index])
                index += 1
            elif varCount > 1:
                for i in range(varCount):
                    var = varName + str(i)
                    setattr(self, var, parameters[index])
                    index += 1


class Filling:
    def __init__(self):
        self.varmap = "Ignore"
        self.displayName = "..."

    def GetDiagram() -> schemdraw.Drawing:
        with schemdraw.Drawing(show=False) as diagram:
            diagram += elm.DotDotDot().right()

        return diagram


class StartResistance(ComponentBase):
    RCircuit = 0

    def __init__(self):
        super().__init__()
        self.varmap = {"RCircuit": 1}
        self.displayName = "电路欧姆电阻"

    def Impedance(self, w: np.ndarray) -> np.ndarray:
        return self.RCircuit

    def Derivative(self, w: np.ndarray) -> np.ndarray:
        return 0

    def GetBoundType(self, dataInfo: dict) -> dict:
        realMin = dataInfo["Real Min"]

        RCircuitBound = (0.01 * realMin, 100 * realMin)
        bounds = [RCircuitBound]

        boundTypeDict = {}
        for key, bound in zip(self.varmap.keys(), bounds):
            boundTypeDict[key] = bound

        return boundTypeDict

    def GetDiagram() -> schemdraw.Drawing:
        with schemdraw.Drawing(show=False) as diagram:
            diagram += elm.Resistor().label("Rc").right()

        return diagram


class StartInductor(ComponentBase):
    Rs = 0
    L_Start = 0

    def __init__(self):
        super().__init__()
        self.varmap = {"Rs": 1, "L_Start": 1}
        self.displayName = "启动电感"

    def Impedance(self, w: np.ndarray) -> np.ndarray:
        Rs = self.Rs
        L = w * self.L_Start * 1j
        impedances = 1 / (1 / Rs + 1 / L)

        return np.conj(impedances)

    def Derivative(self, w: np.ndarray) -> np.ndarray:
        # 恰好函数导数的共轭=函数共轭的导数
        denominator = 1 / self.Rs - 1j / (self.L * w)
        denominatorSquared = denominator**2
        derivatives = -1j / (self.L * w**2 * denominatorSquared)

        return np.conj(derivatives)

    def GetBoundType(self, dataInfo: dict) -> dict:
        realMin = dataInfo["Real Min"]
        realWidth = dataInfo["Real Width"]

        RsBound = (0.01 * realMin, 100 * realMin)
        LBound = (1e-50, 1e-5)
        bounds = [RsBound, LBound]

        boundTypeDict = {}
        for key, bound in zip(self.varmap.keys(), bounds):
            boundTypeDict[key] = bound

        return boundTypeDict

    def GetDiagram() -> schemdraw.Drawing:
        with schemdraw.Drawing(show=False) as diagram:
            diagram += elm.Line().length(1.5).right()
            diagram += elm.Line().length(1.5).up()
            diagram += elm.Resistor().label("Rs").right()
            diagram += elm.Line().length(1.5).down()
            diagram.push()
            diagram += elm.Line().length(1.5).down()
            diagram += elm.Inductor2().label("L").left()
            diagram += elm.Line().length(1.5).up()
            diagram.pop()
            diagram += elm.Line().length(1.5).right()

        return diagram


class RingImpedance(ComponentBase):
    R = 0
    C = 0
    beta = 0

    def __init__(self):
        super().__init__()
        self.varmap = {"R": 1, "C": 1, "beta": 1}
        self.displayName = "单容抗弧"

    def Impedance(self, w: np.ndarray) -> np.ndarray:
        R = self.R
        C = self.C
        beta = self.beta

        tau = (R * C * w ** (1 - beta)) / np.cos((np.pi / 2) * (1 - beta))
        impedances = R / (1 + (w * 1j) ** beta * tau)
        return np.conj(impedances)

    def Derivative(self, w: np.ndarray) -> np.ndarray:
        # 恰好函数导数的共轭=函数共轭的导数
        R = self.R
        C = self.C
        beta = self.beta

        alpha = 1 - beta
        term1 = R * C * w**alpha
        term2 = np.cos(np.pi * alpha / 2)
        term3 = term1 / term2
        term4 = C * R * alpha * w * term3 ** (1 / beta - 1)
        term4 = term4 / (beta * term2 * w**beta)
        term5 = (w * term3 ** (1 / beta)) * 1j

        numerator = -(R * beta * (term3 ** (1 / beta) + term4))
        denominator = term5**alpha * (term5**beta + 1) ** 2
        derivatives = (numerator * 1j) / denominator

        return np.conj(derivatives)

    def GetBoundType(self, dataInfo: dict) -> dict:
        realWidth = dataInfo["Real Width"]

        RBound = (1e-50, 1.5 * realWidth)
        CBound = (1e-50, 1.5 * realWidth)
        betaBound = (0.1, 0.98)
        bounds = [RBound, CBound, betaBound]

        boundTypeDict = {}
        for key, bound in zip(self.varmap.keys(), bounds):
            boundTypeDict[key] = bound

        return boundTypeDict

    def DerivedQuantities(self) -> dict:
        derivedQuantities = {}

        tau = self.R * self.C
        derivedQuantities["tau"] = tau

        return derivedQuantities

    def GetDiagram() -> schemdraw.Drawing:
        with schemdraw.Drawing(show=False) as diagram:
            diagram += elm.Line().length(1.5).right()
            diagram += elm.Line().length(1.5).up()
            diagram += elm.Resistor().label(f"R").right()
            diagram += elm.Line().length(1.5).down()
            diagram.push()
            diagram += elm.Line().length(1.5).down()
            diagram += elm.Capacitor().label(f"C").left()
            diagram += elm.Line().length(1.5).up()
            diagram.pop()
            diagram += elm.Line().length(1.5).right()

        return diagram


class NonIdealCapacitor_Series(ComponentBase):
    R_NICS = 0
    C_NICS = 0
    n_NICS = 0

    def __init__(self):
        super().__init__()
        self.varmap = {"R_NICS": 1, "C_NICS": 1, "n_NICS": 1}
        self.displayName = "非理想电容-串联"

    def Impedance(self, w: np.ndarray) -> np.ndarray:
        R = self.R_NICS
        C = self.C_NICS
        n = self.n_NICS

        denominator = C * (w * 1j) ** n
        impedances = R + 1 / denominator
        return np.conj(impedances)

    def GetBoundType(self, dataInfo: dict) -> dict:
        realWidth = dataInfo["Real Width"]

        RBound = (1e-50, 1.5 * realWidth)
        CBound = (1e-50, 1.5 * realWidth)
        nBound = (0.1, 0.98)
        bounds = [RBound, CBound, nBound]

        boundTypeDict = {}
        for key, bound in zip(self.varmap.keys(), bounds):
            boundTypeDict[key] = bound

        return boundTypeDict

    def GetDiagram() -> schemdraw.Drawing:
        with schemdraw.Drawing(show=False) as diagram:
            diagram += elm.Resistor().label(f"R").right()
            diagram += elm.Capacitor().label(f"CPE").right()

        return diagram


class NonIdealCapacitor_Parallel(ComponentBase):
    R_NICP = 0
    C_NICP = 0
    n_NICP = 0

    def __init__(self):
        super().__init__()
        self.varmap = {"R_NICP": 1, "C_NICP": 1, "n_NICP": 1}
        self.displayName = "非理想电容-并联"

    def Impedance(self, w: np.ndarray) -> np.ndarray:
        R = self.R_NICP
        C = self.C_NICP
        n = self.n_NICP

        term1 = C * (w * 1j) ** n
        impedances = 1 / (1 / R + term1)
        return np.conj(impedances)

    def GetBoundType(self, dataInfo: dict) -> dict:
        realWidth = dataInfo["Real Width"]

        RBound = (1e-50, 1.5 * realWidth)
        CBound = (1e-50, 1.5 * realWidth)
        nBound = (0.1, 0.98)
        bounds = [RBound, CBound, nBound]

        boundTypeDict = {}
        for key, bound in zip(self.varmap.keys(), bounds):
            boundTypeDict[key] = bound

        return boundTypeDict

    def GetDiagram() -> schemdraw.Drawing:
        with schemdraw.Drawing(show=False) as diagram:
            diagram += elm.Line().length(1.5).right()
            diagram += elm.Line().length(1.5).up()
            diagram += elm.Resistor().label(f"R").right()
            diagram += elm.Line().length(1.5).down()
            diagram.push()
            diagram += elm.Line().length(1.5).down()
            diagram += elm.Capacitor().label(f"CPE").left()
            diagram += elm.Line().length(1.5).up()
            diagram.pop()
            diagram += elm.Line().length(1.5).right()

        return diagram


class NonIdealStartInductor(ComponentBase):
    R_NISI = 0
    L_NISI = 0
    n_NISI = 0

    def __init__(self):
        super().__init__()
        self.varmap = {"R_NISI": 1, "L_NISI": 1, "n_NISI": 1}
        self.displayName = "非理想启动电感"

    def Impedance(self, w: np.ndarray) -> np.ndarray:
        R = self.R_NISI
        L = self.L_NISI
        n = self.n_NISI

        term1 = (w * 1j) ** n / L
        impedances = 1 / (1 / R + term1)
        return np.conj(impedances)

    def GetBoundType(self, dataInfo: dict) -> dict:
        realWidth = dataInfo["Real Width"]

        RBound = (1e-50, 1.5 * realWidth)
        LBound = (1e-50, 1.5 * realWidth)
        nBound = (-1, 0)
        bounds = [RBound, LBound, nBound]

        boundTypeDict = {}
        for key, bound in zip(self.varmap.keys(), bounds):
            boundTypeDict[key] = bound

        return boundTypeDict

    def GetDiagram() -> schemdraw.Drawing:
        with schemdraw.Drawing(show=False) as diagram:
            diagram += elm.Line().length(1.5).right()
            diagram += elm.Line().length(1.5).up()
            diagram += elm.Resistor().label(f"R").right()
            diagram += elm.Line().length(1.5).down()
            diagram.push()
            diagram += elm.Line().length(1.5).down()
            diagram += elm.Inductor2().label(f"LCPE").left()
            diagram += elm.Line().length(1.5).up()
            diagram.pop()
            diagram += elm.Line().length(1.5).right()

        return diagram


class ChargeTransferComponent(ComponentBase):
    R = 0
    L = 0
    C = 0
    beta = 0

    def __init__(self):
        super().__init__()
        self.varmap = {"R": 1, "L": 1, "C": 1, "beta": 1}
        self.displayName = "电荷转移模块"

    def Impedance(self, w: np.ndarray) -> np.ndarray:
        R = self.R
        L = self.L
        C = self.C
        beta = self.beta

        L = w * L * 1j

        tau = ((R + L) * C * w ** (1 - beta)) / np.cos((np.pi / 2) * (1 - beta))
        impedances = (R + L) / (1 + (w * 1j) ** beta * tau)
        return np.conj(impedances)

    def GetBoundType(self, dataInfo: dict) -> dict:
        realWidth = dataInfo["Real Width"]

        RBound = (1e-50, 1.5 * realWidth)
        LBound = (0, 1e-6)
        CBound = (1e-50, 1.5 * realWidth)
        betaBound = (0.1, 0.99)
        bounds = [RBound, LBound, CBound, betaBound]

        boundTypeDict = {}
        for key, bound in zip(self.varmap.keys(), bounds):
            boundTypeDict[key] = bound

        return boundTypeDict

    def GetDiagram() -> schemdraw.Drawing:
        with schemdraw.Drawing(show=False) as diagram:
            diagram += elm.Line().length(1.5).right()
            diagram += elm.Line().length(1.5).up()
            diagram += elm.Resistor().label(f"R").right()
            diagram += elm.Inductor2().label(f"L").right()
            diagram += elm.Line().length(1.5).down()
            diagram.push()
            diagram += elm.Line().length(1.5).down()
            diagram += elm.Line().length(1.5).left()
            diagram += elm.Capacitor().label(f"C").left()
            diagram += elm.Line().length(1.5).left()
            diagram += elm.Line().length(1.5).up()
            diagram.pop()
            diagram += elm.Line().length(1.5).right()

        return diagram
