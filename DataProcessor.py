import types

import numpy as np
from lmfit import Parameters, fit_report, minimizer
from scipy.interpolate import CubicSpline
from scipy.signal import find_peaks, savgol_filter
from scipy.spatial import KDTree

import IO
import Model
import Optimizer

ExtremumMinimumDistance = 10
DRTExtremumMinimumDistance = 10
DRTExtremumRelativePeakThreshold = 0.1


def R2(
    ogData: np.ndarray,
    result: minimizer.MinimizerResult,
    model: Model.Model,
) -> float:
    varmaps = model.circuit.varmaps
    parametersChanged = ChangeParameterType(varmaps, result.params)
    model.UpdateParameters(parametersChanged)
    modelData = GetModelData(model, ogData)

    zData = ogData["impedance"]
    zModel = modelData["impedance"]
    yData = np.concatenate((zData.real, zData.imag))
    yModel = np.concatenate((zModel.real, zModel.imag))

    yDataAverage = np.average(yData)

    SSTot = np.sum(np.square(yData - yDataAverage))
    SSRes = np.sum(np.square(yData - yModel))

    R2 = 1 - SSRes / SSTot

    return R2


def MSD(
    ogData: np.ndarray,
    result: minimizer.MinimizerResult,
    model: Model.Model,
) -> float:
    varmaps = model.circuit.varmaps
    parametersChanged = ChangeParameterType(varmaps, result.params)
    model.UpdateParameters(parametersChanged)
    modelData = GetModelData(model, ogData)

    zData = ogData["impedance"]
    zModel = modelData["impedance"]

    msd = GetMinSquaredDistancesToDataCurve(zModel, zData)
    return msd


def GenerateRingCount(DRTData: np.ndarray):
    y = DRTData["gamma"]
    peaks, _ = find_peaks(y, distance=DRTExtremumMinimumDistance)

    maxPeakValue = max(y[peaks])

    ringCount = 0
    for peak in peaks:
        if y[peak] < maxPeakValue * DRTExtremumRelativePeakThreshold:
            continue

        ringCount += 1

    return ringCount


def GenerateDataInfo(data: np.ndarray) -> dict:
    dataInfo = {}
    impedance = data["impedance"]

    realMin = min(impedance.real)
    realMax = max(impedance.real)
    realWidth = realMax - realMin

    dataInfo["Real Min"] = realMin
    dataInfo["Real Max"] = realMax
    dataInfo["Real Width"] = realWidth

    return dataInfo


def GenerateBounds(varmaps: list[dict], boundType: dict) -> list[(float, float)]:
    bounds = []

    for varmap in varmaps:
        for varname, count in varmap.items():
            if varname in boundType:
                for _ in range(count):
                    bounds.append(boundType[varname])
            else:
                raise ValueError(f"{varname} not in BoundType!")

    return bounds


def ChangeParameterType(varmaps: list[dict], parameters: Parameters) -> list[float]:
    parametersChanged = []

    parametersValue = parameters.valuesdict()

    varCounts = {}
    for varmap in varmaps:
        for varname, count in varmap.items():
            for _ in range(count):
                if varname not in varCounts:
                    varCounts[varname] = 1
                else:
                    varCounts[varname] += 1

                index = varCounts[varname]
                varParaName = f"{varname}{index}"
                parametersChanged.append(parametersValue[varParaName])

    return parametersChanged


def InitParameter(
    varmaps: list[dict],
    bounds: list[(float, float)],
) -> Parameters:
    parameters = Parameters()

    varCounts = {}
    boundIndex = 0
    for varmap in varmaps:
        for varname, count in varmap.items():
            for _ in range(count):
                if varname not in varCounts:
                    varCounts[varname] = 1
                else:
                    varCounts[varname] += 1

                minValue, maxValue = bounds[boundIndex]
                value = (minValue + maxValue) / 2

                varIndex = varCounts[varname]
                varParaName = f"{varname}{varIndex}"
                parameters.add(varParaName, value=value, min=minValue, max=maxValue)
                boundIndex += 1

    return parameters


def GetPhaseAndMagnitude(impedance: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    phase = np.angle(impedance)
    mag = np.abs(impedance)

    return phase, mag


def GetDataDerivatives(data: np.ndarray) -> np.ndarray:
    f = data["frequency"]
    z = data["impedance"]

    derivatives = np.gradient(z) / np.gradient(f)

    return derivatives


def GetImpedanceDerivatives(z: np.ndarray) -> np.ndarray:
    zReal = z.real
    zImag = z.imag

    derivatives = np.gradient(zImag) / np.gradient(zReal)

    return derivatives


def GetMinSquaredDistancesToDataCurve(
    modelImp: np.ndarray, interpDataImp: np.ndarray
) -> float:
    distances = np.square(modelImp.real - interpDataImp.real) + np.square(
        modelImp.imag - interpDataImp.imag
    )

    return min(distances)


def GetModelData(model: Model.Model, data: np.ndarray) -> np.ndarray:
    modelData = np.copy(data)
    modelData["impedance"] = model.ImpedancesAnalyse(data["frequency"])

    return modelData


def GetExtremumIndex(y: np.ndarray) -> np.ndarray:
    peaks, _ = find_peaks(y, distance=ExtremumMinimumDistance)
    valleys, _ = find_peaks(-y, distance=ExtremumMinimumDistance)

    extremums = np.concatenate((peaks, valleys))

    # Remove Close Extremums
    extremums.sort()
    # Skip The First And The Last Extremums, cause it tends to be random noise
    # extremums = extremums[1:-1]

    extremumsList = [extremums[0]]
    for i in range(1, len(extremums)):
        if extremums[i] - extremumsList[-1] > ExtremumMinimumDistance:
            extremumsList.append(extremums[i])
    extremums = np.array(extremumsList)

    return extremums


def AddWeightsAroundIndexes(
    weight: np.ndarray, indexes: np.ndarray, options: list[int, float]
):
    radius, addWeight = options
    for index in indexes:
        left = max(index - radius, 0)
        right = min(index + radius, len(weight))
        for i in range(left, right):
            weight[i] += addWeight


def GenerateWeight(
    data: np.ndarray, options: list[tuple, tuple, tuple]
) -> tuple[np.ndarray, np.ndarray]:
    weightOptions, dzweightOptions, diweightOptions = options
    f = data["frequency"]
    z = data["impedance"]
    dz = GetDataDerivatives(data)
    di = GetImpedanceDerivatives(z)

    extremumIndex = GetExtremumIndex(z.imag)
    dzextremumIndex = GetExtremumIndex(dz.imag)
    diextremumIndex = GetExtremumIndex(di)

    weight = np.ones_like(f)
    AddWeightsAroundIndexes(weight, extremumIndex, weightOptions)
    if Optimizer.residualStuc != Optimizer.residualStucs[1]:
        weight = np.tile(weight, 2)

    if Optimizer.residualType != Optimizer.residualTypes[0]:
        dzWeight = np.full(len(f), 0.1)
        diWeight = np.full(len(f), 1)
        AddWeightsAroundIndexes(dzWeight, dzextremumIndex, dzweightOptions)
        AddWeightsAroundIndexes(diWeight, diextremumIndex, diweightOptions)
        if Optimizer.residualStuc != Optimizer.residualStucs[1]:
            dzWeight = np.tile(dzWeight, 2)
            diWeight = np.tile(diWeight, 2)

        dWeight = dzWeight + diWeight

    return weight, dWeight


def FilterData(data: np.ndarray, filterOptions: list) -> np.ndarray:
    windowSize, threshold, dthreshold, counts, deleteAboveZero = filterOptions

    centerIndex = windowSize // 2
    # 删掉虚部大于0的数据
    if deleteAboveZero:
        mask = data["impedance"].imag > 0
        # filteredData = data[~mask]
        filteredData = data[mask]
    else:
        filteredData = np.copy(data)

    filterDataLength = 0
    while (filterDataLength != filteredData.shape[0]) and (counts != 0):
        filterDataLength = filteredData.shape[0]
        mask = np.ones(filterDataLength, dtype=bool)

        for i in range(filterDataLength):
            if i <= centerIndex:
                window = filteredData[:windowSize]
            elif i >= filterDataLength - centerIndex:
                window = filteredData[-windowSize:]
            else:
                window = filteredData[i - centerIndex : i + centerIndex + 1]

            zs = window["impedance"]
            dzs = GetDataDerivatives(window)
            z = zs[centerIndex]
            dz = dzs[centerIndex]

            # 去中心
            zs = np.delete(zs, centerIndex)
            dzs = np.delete(dzs, centerIndex)

            mean = np.mean(zs)
            dmean = np.mean(dzs)
            std = np.std(zs)
            dstd = np.std(dzs)
            zScore = (z - mean) / std
            dzScore = (dz - dmean) / dstd

            if (zScore > threshold) or (dzScore > dthreshold):
                mask[i] = False

        filteredData = filteredData[mask]
        counts -= 1

    return filteredData


def SmoothData(data: np.ndarray, smootherOptions: list) -> np.ndarray:
    windowLength, polyOrder = smootherOptions

    z = data["impedance"]
    zReal = z.real
    zImag = z.imag

    zRealSmoothed = savgol_filter(zReal, windowLength, polyOrder)
    zImagSmoothed = savgol_filter(zImag, windowLength, polyOrder)

    zSmoothed = zRealSmoothed + 1j * zImagSmoothed
    smoothedData = np.copy(data)
    smoothedData["impedance"] = zSmoothed

    return smoothedData


def DownSampleData(data: np.ndarray, downSampleOptions: list) -> np.ndarray:
    fuseDistance = downSampleOptions[0]

    fs = data["frequency"]
    zs = data["impedance"]
    dataLen = data.shape[0]

    zPoints = np.array([[z.real, z.imag] for z in zs])

    tree = KDTree(zPoints)

    downSampledData = []
    processed = np.zeros(dataLen, dtype=bool)
    for i in range(dataLen):
        if not processed[i]:
            neighbors = tree.query_ball_point(zPoints[i], fuseDistance)

            if len(neighbors) > 1:
                centerZ = np.mean(zs[neighbors])
                centerF = np.mean(fs[neighbors])
                downSampledData.append((centerF, centerZ))

                processed[neighbors] = True
            else:
                downSampledData.append((fs[i], zs[i]))

    downSampledData = np.array(downSampledData, dtype=IO.dataDtype)

    return downSampledData


def CutoffData(data: np.ndarray, cutoffOptions: list):
    rejectDistance, cutSection = cutoffOptions

    fs = data["frequency"]
    zs = data["impedance"]
    dataLen = data.shape[0]

    zPoints = np.array([[z.real, z.imag] for z in zs])

    tree = KDTree(zPoints)

    cutoffData = []
    for i in range(dataLen):
        neighbors = tree.query_ball_point(zPoints[i], rejectDistance)

        if len(neighbors) > 1:
            cutoffData.append((fs[i], zs[i]))
        else:
            break

    cutoffData = np.array(cutoffData, dtype=IO.dataDtype)

    leftBound = int(len(cutoffData) * cutSection[0])
    rightBound = int(len(cutoffData) * cutSection[1])
    cutoffData = cutoffData[leftBound:rightBound]

    return cutoffData


def GenerateDataInterpolation(data: np.ndarray) -> CubicSpline:
    f = data["frequency"]
    z = data["impedance"]

    dataInterpolationReal = CubicSpline(f, z.real)
    dataInterpolationImag = CubicSpline(f, z.imag)

    return [dataInterpolationReal, dataInterpolationImag]


def InterpolatedData(data: np.ndarray, interpolaterOptions: list) -> np.ndarray:
    interpMode, xStart, xEnd, pointCounts = interpolaterOptions

    if interpMode == "10^x":
        interpFrequency = np.power(10, np.linspace(xStart, xEnd, pointCounts))

    realFunc, imagFunc = GenerateDataInterpolation(data)
    z = realFunc(interpFrequency) + 1j * imagFunc(interpFrequency)

    interpolatedData = np.array(list(zip(interpFrequency, z)), dtype=IO.dataDtype)

    return interpolatedData


def PreProcessDatas(
    datas: list[np.ndarray],
    preProcessorInfo: list,
) -> list[np.ndarray]:
    (
        preProcessorSwitch,
        filterOptions,
        cutofferOptions,
        interpolaterOptions,
        smootherOptions,
        downSamplerOptions,
    ) = preProcessorInfo
    filterData, cutoffData, interpolateData, smoothData, downSampleData = (
        preProcessorSwitch
    )

    processedDatas = []
    for data in datas:
        processedData = np.copy(data)

        if filterData:
            processedData = FilterData(processedData, filterOptions)
        if cutoffData:
            processedData = CutoffData(processedData, cutofferOptions)
        if interpolateData:
            processedData = InterpolatedData(processedData, interpolaterOptions)
        if smoothData:
            processedData = SmoothData(processedData, smootherOptions)
        if downSampleData:
            processedData = DownSampleData(processedData, downSamplerOptions)

        processedDatas.append(processedData)

    return processedDatas


def GenerateResultText(
    result: minimizer.MinimizerResult,
    model: Model.Model,
    costsText: str,
    hyperParameters: list,
    time: float,
) -> str:
    circuit = model.circuit
    varmaps = circuit.varmaps
    parameters = ChangeParameterType(varmaps, result.params)
    model.UpdateParameters(parameters)

    resultText = ""
    resultText += f"优化结果:\n"
    resultText += f"使用的电路: {circuit.displayName}\n"

    for i, (component, componentName) in enumerate(
        zip(circuit.components, circuit.componentDisplayNames)
    ):
        # Paras
        resultText += f"组件 {i+1}: {componentName}\n"
        for varName in component.varmap.keys():
            val = getattr(component, varName)
            resultText += f"\t{varName}: {val:.8f}\n"

        # Derived Quantities
        if hasattr(component, "DerivedQuantities") and isinstance(
            component, types.MethodType
        ):
            resultText += "\t导出量:\n"
            derivedQuantities = component.DerivedQuantities()
            for varName, val in derivedQuantities.items():
                resultText += f"\t{varName}: {val:.8f}\n"

    # Hyper Parameters
    boundType = hyperParameters[0]
    displayBoundType = {}
    for key, val in boundType.items():
        minVal, maxVal = val
        minVal = float(minVal)
        maxVal = float(maxVal)
        displayBoundType[key] = (minVal, maxVal)

    # Output
    resultText += f"\n优化后代价: {costsText}\n"
    resultText += f"\n超参数:\n"
    resultText += f"参数取值范围: {displayBoundType}\n"
    resultText += f"\n用时: {time:.3f}秒\n"
    resultText += f"\n\n详细的分析报告:\n"
    resultText += fit_report(result)

    return resultText


def GeneratePreProcessorInfo(preProcessorInfo: list):
    (
        preProcessorSwitch,
        filterOptions,
        cutofferOptions,
        interpolaterOptions,
        smootherOptions,
        downSamplerOptions,
    ) = preProcessorInfo
    resultText = f"\nPre Processor Info:\n"

    filterData, cutoffData, interpolateData, smoothData, downSampleData = (
        preProcessorSwitch
    )
    resultText += f"Pre Processor Switch:\n"
    resultText += f"\tFilter: {filterData}\n"
    resultText += f"\tCutoffer: {cutoffData}\n"
    resultText += f"\tInterpolater: {interpolateData}\n"
    resultText += f"\tSmoother: {smoothData}\n"
    resultText += f"\tDownSampler: {downSampleData}\n"

    if filterData:
        resultText += f"Filter Options: {filterOptions}\n"
    if cutoffData:
        resultText += f"Cutoffer Options: {cutofferOptions}\n"
    if interpolateData:
        resultText += f"Interpolater Options: {interpolaterOptions}\n"
    if smoothData:
        resultText += f"Smoother Options: {smootherOptions}\n"
    if downSampleData:
        resultText += f"DownSampler Options: {downSamplerOptions}\n"

    return resultText
