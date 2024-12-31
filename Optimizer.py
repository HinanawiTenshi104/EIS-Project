import numpy as np
from lmfit import Parameters, minimizer

import DataProcessor
import Model

# from scipy.optimize import curve_fit

defaultRingCount = 3

# 注释掉的要不是需要jac和hess懒得准备，要不是绝对不可能用的（就是你brute）
methodFullList = [
    "leastsq",
    "nelder",
    "lbfgsb",
    "powell",
    "cg",
    # "newton",
    "cobyla",
    "bfgsb",
    "tnc",
    # "trust-ncg",
    # "trust-exact",
    # "trust-krylov",
    # "trust-constr",
    # "dogleg",
    "slsqp",
    "differential_evolution",
    # "brute",
    "basinhopping",
    "ampgo",
    # "shgo", 好像用起来会内存泄漏，怪，反正是垃圾算法
    "dual_annealing",
    # "emcee",
]
# 效果不好的算法
bad = [methodFullList[i] for i in [1, 5, 6]]
# 按算法用时长短分成三类
fast = [methodFullList[i] for i in [0, 2, 3, 7, 8]]
medium = [methodFullList[i] for i in [4, 9, 12]]
slow = [methodFullList[i] for i in [10, 11]]

methodListDict = {"Fast": fast, "Medium": medium, "Slow": slow, "Bad": bad}

methodList = fast  # + medium + slow

# Value就挺好了，而且还快；Derivative信息还是太多噪音了，效果不一定更好
residualTypes = ("Value", "Value + F-Z Derivative", "Value + R-I Derivative")
normalizationModes = ("None", "Min-Max", "Z-Score")
# Complex效果和Real + Imag差不多(感觉是内部就是把Complex变成Real + Imag运算的)；后两个效果太烂了，我都删了
residualStucs = ("Real + Imag", "Complex")  # , "Phase + Mag"), "R + I + P + M")
# 效果都不错，感觉Log-Cosh比较通用一点，不过容易出现NaN
residualModes = ("MSE", "MAE", "Log-Cosh", "Huber")

residualType = residualTypes[0]
normalizationMode = normalizationModes[0]
residualStuc = residualStucs[0]
residualMode = residualModes[2]

if residualMode == residualModes[3]:
    delta = 1.0

applyWeight = False
weightOptions = (4, 1)
dzweightOptions = (4, 0.4)
diweightOptions = (4, 4)


def curveFit(
    hyperParameters: list,
    data: np.ndarray,
    model: Model.Model,
) -> minimizer.MinimizerResult:
    f = data["frequency"]
    z = data["impedance"]
    ydata = np.concatenate((z.real, z.imag))

    circuit = model.circuit
    varmaps = circuit.varmaps

    if normalizationMode == normalizationModes[1]:
        ymax = ydata.max()
        ymin = ydata.min()

        def normalize(y):
            return (y - ymin) / (ymax - ymin)

        ydata = normalize(ydata)

    if normalizationMode == normalizationModes[2]:
        ymean = ydata.mean()
        ystd = ydata.std()

        def normalize(y):
            return (y - ymean) / ystd

        ydata = normalize(ydata)

    dz = DataProcessor.GetDataDerivatives(data)
    di = DataProcessor.GetImpedanceDerivatives(z)

    # Setup Weight
    if applyWeight:
        options = [weightOptions, dzweightOptions, diweightOptions]
        weight, dWeight = DataProcessor.GenerateWeight(data, options)

    bools = f < 1000
    weight = np.ones_like(f)
    weight *= bools * 1
    weight = np.tile(weight, 2)

    def residual(parameters: Parameters):
        parametersChanged = DataProcessor.ChangeParameterType(varmaps, parameters)
        model.UpdateParameters(parametersChanged)

        zStar = model.ImpedancesAnalyse(f)
        ystar = np.concatenate((zStar.real, zStar.imag))
        if normalizationMode != normalizationModes[0]:
            ystar = normalize(ystar)

        # valueDifferences = zStar - z
        residual = ystar - ydata

        """
        if residualStuc == residualStucs[0]:
            residual = valueDifferences
        if residualStuc == residualStucs[1]:
            residual = np.concatenate((valueDifferences.real, valueDifferences.imag))
        if residualStuc == residualStucs[2]:
            phase, mag = DataProcessor.GetPhaseAndMagnitude(valueDifferences)
            residual = np.concatenate((phase, mag))
        """
        if residualType != residualTypes[0]:
            if residualType == residualTypes[1]:
                dzStar = model.ImpedancesDerivativeAnalyse(f)
                derivativeDifferences = dzStar - dz
                if residualStuc == residualStucs[0]:
                    dresidual = np.concatenate(
                        (derivativeDifferences.real, derivativeDifferences.imag)
                    )
            if residualType == residualTypes[2]:
                diStar = DataProcessor.GetImpedanceDerivatives(zStar)
                derivativeDifferences = diStar - di
                dresidual = np.tile(derivativeDifferences, 2)

            """
            if residualStuc == residualStucs[1]:
                dresidual = derivativeDifferences
            if residualStuc == residualStucs[2]:
                dphase, dmag = DataProcessor.GetPhaseAndMagnitude(derivativeDifferences)
                dresidual = np.concatenate((dphase, dmag))
            """
            # 保证导数的residual和值的residual数量级差不多
            dresidual = dresidual / dresidual.mean()
            dresidual = np.mean(residual) * dresidual

            if applyWeight:
                dresidual = dWeight * dresidual

            residual += dresidual

        if residualMode == residualModes[0]:
            residual = residual**2
        if residualMode == residualModes[1]:
            residual = np.abs(residual)
        if residualMode == residualModes[2]:
            residual = np.log(np.cosh(residual))
        if residualMode == residualModes[3]:
            isSmallError = np.abs(residual) <= delta
            squaredLoss = 0.5 * np.square(residual)
            linearLoss = delta * (np.abs(residual) - 0.5 * delta)

            residual = np.where(isSmallError, squaredLoss, linearLoss)

        if applyWeight:
            residual = weight * residual

        residual *= weight

        return residual

    boundType = hyperParameters[0]
    method = hyperParameters[1]

    bounds = DataProcessor.GenerateBounds(varmaps, boundType)

    parameters = DataProcessor.InitParameter(varmaps, bounds)

    result = minimizer.minimize(residual, parameters, method=method)

    return result


"""
def curveFitLegacy(
    paraFormat: list[int, int, bool], hyperParameters: list, data: np.ndarray
):
    xdata = data["frequency"]
    z = data["impedance"]
    ydata = np.concatenate((z.real, z.imag))

    ymini = ydata.min()
    ymaxy = ydata.max()

    def normalize(y):
        return (y - ymini) / (ymaxy - ymini)

    def f(x, RCircuit, Rs, L, beta1, beta2, beta3, R1, R2, R3, C1, C2, C3):
        consts = [RCircuit, Rs, L]
        beta = [beta1, beta2, beta3]
        R = [R1, R2, R3]
        C = [C1, C2, C3]
        parameters = consts + beta + R + C

        model = Model.Model(parameters, paraFormat)
        ymodel = model.ImpedancesAnalyse(x)
        ymodel = np.concatenate((ymodel.real, ymodel.imag))

        return normalize(ymodel)

    bounds = hyperParameters[0]
    mins = tuple(bound[0] for bound in bounds)
    maxs = tuple(bound[1] for bound in bounds)
    newbounds = [mins, maxs]

    popt, _ = curve_fit(f, xdata, normalize(ydata), bounds=newbounds)

    parameters = [float(num) for num in popt]
    model = Model.Model(parameters, paraFormat)
    modelData = DataProcessor.GetModelData(model, data)

    datas = [data, modelData]
    DrawDiagram.plt.switch_backend("TkAgg")
    DrawDiagram.DrawCompareDiagram(datas)
    DrawDiagram.plt.switch_backend("Agg")

    return popt
"""
