import time

import numpy as np

import DataProcessor
import Debug
import DrawDiagram
import IO
import Model
import Optimizer

# 0. Program parameters
preProcessData = True
processData = True
testAllMethods = True
# 建议还是选False然后自己挑，至少在Cost函数改好之前
saveOnlyBestResult = False
drawProcessedDataInCompareDiagram = False
# Nyquist, Bode, Derivative
drawOptions = [True, True, True]
printResult = False
printProgressBar = True
saveImgWhenProcessing = True

# 0.1 more debug-like options...
drawProcessedData = False
drawDataDerivative = False
drawDataExtremum = False
drawDRTDiagram = True
drawCirCuitDiagram = False
writeData = False
# 是否从straName/dataName 变成dataName/straName的结构
changeResultStructure = True
readResult = False
readResultTitle = "[manual]\\1.7.txt"
drawResults = False

# 1. Hyper Parameters
# 1.1 Model's Hyper Parameters
# 常数个数（不含beta），环的个数，beta是否可变
constCounts = 3
variableBeta = True
ringCounts = 3
paraFormat = [constCounts, variableBeta, ringCounts]

datas = []
dataNames = []
ogDatas = []

preProcessorInfo = []
hyperParameters = []


# 1. Read Experiment Datas
def ReadExperimentDatas():
    global datas, dataNames, ogDatas, preProcessorInfo

    # 1. Read Experiment Datas
    datas, dataNames = IO.ReadAllDatas()
    # 1.1 Filter Datas
    ogDatas = datas

    # Filter, Cutoffer, Interpolater, Smoother, Downsampler
    preProcessorSwitch = [False, False, False, False, False]

    windowSize = 5
    threshold = 1
    dthreshold = 1
    counts = -1
    deleteAboveZero = False
    filterOptions = [windowSize, threshold, dthreshold, counts, deleteAboveZero]

    rejectDistance = 0.2
    cutSection = (0.1, 0.9)
    cutofferOptions = [rejectDistance, cutSection]

    interpMode = "10^x"
    xStart = 0.6
    xEnd = 4.5
    pointCounts = 100
    interpolaterOptions = [interpMode, xStart, xEnd, pointCounts]

    windowLength = 4
    polyOrder = 3
    smootherOptions = [windowLength, polyOrder]

    fuseDistance = 0.01
    downSamplerOptions = [fuseDistance]

    preProcessorInfo = [
        preProcessorSwitch,
        filterOptions,
        cutofferOptions,
        interpolaterOptions,
        smootherOptions,
        downSamplerOptions,
    ]

    if preProcessData:
        datas = DataProcessor.PreProcessDatas(
            datas,
            preProcessorInfo,
        )

        if drawProcessedData:
            DrawDiagram.plt.switch_backend("TkAgg")
            for ogData, data, dataName in zip(ogDatas, datas, dataNames):
                ogZ = ogData["impedance"]
                z = data["impedance"]
                print(f"{dataName}'s length: {len(z)}")

                zs = [ogZ, z]
                labels = ["Original Data", "PreProcessed Data"]
                DrawDiagram.DrawNyquistDigram(
                    dataImpedances=zs,
                    labels=labels,
                    title=dataName,
                )
                # DrawDiagram.DrawBodeDiagram(ogData, data, title=dataName)
            DrawDiagram.plt.switch_backend("Agg")

    if drawDataDerivative:
        DrawDiagram.plt.switch_backend("TkAgg")
        for data, dataName in zip(datas, dataNames):
            d = DataProcessor.GetDataDerivatives(data)
            DrawDiagram.DrawDerivativeDigram([d], title=dataName + "-derivative")
        DrawDiagram.plt.switch_backend("Agg")

    if drawDataExtremum:
        DrawDiagram.plt.switch_backend("TkAgg")
        for data, dataName in zip(datas, dataNames):
            z = data["impedance"]
            dz = DataProcessor.GetDataDerivatives(data)
            di = DataProcessor.GetImpedanceDerivatives(z)
            extremumIndex = DataProcessor.GetExtremumIndex(z.imag)
            dzextremumIndex = DataProcessor.GetExtremumIndex(dz.imag)
            diextremumIndex = DataProcessor.GetExtremumIndex(di)
            DrawDiagram.DrawExtremums(
                z,
                np.concatenate((extremumIndex, dzextremumIndex, diextremumIndex)),
                title=dataName + "-extremum",
            )
        DrawDiagram.plt.switch_backend("Agg")


# 2. Setup Parameters
def SetupParameters():
    global hyperParameters, paraFormat, ringCounts

    # 2. Setup Parameters
    DRTData = IO.ReadDRTData(dataNames[0])
    if drawDRTDiagram:
        DrawDiagram.plt.switch_backend("TkAgg")
        DrawDiagram.DrawDRTDiagram(DRTData, title=dataNames[0])
        DrawDiagram.plt.switch_backend("Agg")

    ringCounts = DataProcessor.GenerateRingCount(DRTData)
    ringCounts = 3
    paraFormat = [
        constCounts,
        ringCounts,
        variableBeta,
    ]
    bounds = DataProcessor.GenerateBounds(paraFormat, datas[0])

    hyperParameters = [bounds] + [Optimizer.methodList[0]]

    if drawCirCuitDiagram:
        DrawDiagram.plt.switch_backend("TkAgg")
        DrawDiagram.DrawCircuitDiagram(
            ringCount=paraFormat[1], title="Equivalent Circuit Diagram"
        )
        DrawDiagram.plt.switch_backend("Agg")


# 3. Data Processing
def DataProcessing():
    global paraFormat

    if processData:
        totalTimeStart = time.time()
        methodList = Optimizer.methodList if testAllMethods else [hyperParameters[1]]
        if printProgressBar:
            totalProgressCounts = len(datas) * len(methodList)
            dataProgressCounts = len(methodList)
            totalProgressCounter = 0
            dataProgressCounter = 0

        bestMethods = []
        bestCosts = []
        dataTimes = []

        for data, dataName, ogData in zip(datas, dataNames, ogDatas):
            dataTimeStart = time.time()
            dataProgressCounter = 0

            bestMethod = ""
            bestResult = None
            bestCost = float("inf")

            # Optimization
            print(f"Optimizing {dataName}...")

            for method in methodList:
                methodTimeStart = time.time()

                if printProgressBar:
                    totalProgressCounter += 1
                    dataProgressCounter += 1

                savePath = method if testAllMethods else ""

                if writeData:
                    IO.WriteData(data, dataName + "-data.txt", savePath)

                # Get Result
                hyperParameters[1] = method
                result = Optimizer.curveFit(paraFormat, hyperParameters, data)

                # Optimized Cost
                optimizedCost = np.mean(np.square(result.residual))

                # Save The Best Result
                if optimizedCost < bestCost:
                    bestMethod = method
                    bestResult = result
                    bestCost = optimizedCost

                # Generate Current Method Results
                methodTimeEnd = time.time()
                methodTime = methodTimeEnd - methodTimeStart

                if not saveOnlyBestResult:
                    IO.GenerateResult(
                        result,
                        paraFormat,
                        optimizedCost,
                        hyperParameters,
                        methodTime,
                        dataName,
                        savePath,
                        saveImgWhenProcessing,
                        ogData,
                        data,
                        dataName,
                        drawOptions,
                        printResult,
                    )

                if printProgressBar:
                    DrawDiagram.DrawProgressBar(
                        dataProgressCounter,
                        dataProgressCounts,
                        prefix=f"当前数据进度:",
                        suffix=f"{method.ljust(max(len(s) for s in methodList)+1)}用时: {methodTime:.3f}秒",
                        length=50,
                    )
                    print()
                    DrawDiagram.DrawProgressBar(
                        totalProgressCounter,
                        totalProgressCounts,
                        prefix="总进度:      ",
                        suffix="完成",
                        length=50,
                    )
            print()

            # Generate Data Results
            dataTimeEnd = time.time()
            dataTime = dataTimeEnd - dataTimeStart

            bestMethods.append(bestMethod)
            bestCosts.append(bestCost)
            dataTimes.append(dataTime)

            if saveOnlyBestResult:
                IO.GenerateResult(
                    bestResult,
                    paraFormat,
                    bestCost,
                    hyperParameters,
                    dataTime,
                    dataName,
                    "",
                    saveImgWhenProcessing,
                    ogData,
                    data,
                    dataName,
                    drawOptions,
                    printResult,
                )

        totalTimeEnd = time.time()
        totalTime = totalTimeEnd - totalTimeStart

        IO.GenerateBatchResult(
            preProcessorInfo,
            totalTime,
            dataNames,
            bestCosts,
            bestMethods,
            dataTimes,
            "batch info",
        )
        print(f"\nTotal Time Usage: {totalTime:.3f} Seconds")

    if changeResultStructure:
        IO.ChangeResultsStructure(dataNames, Optimizer.methodList)

    # 3.2 Read results
    if readResult:
        parameters, paraFormat = IO.ReadResult(readResultTitle)
        model = Model.Model(parameters, paraFormat)

        data = IO.ReadData(readResultTitle)

        modelData = np.copy(data)
        modelData["impedance"] = model.ImpedancesAnalyse(modelData["frequency"])
        IO.WriteData(modelData, splitRealAndImag=True)


# 4. Draw results
def DrawResults():
    # 4. Draw results
    if drawResults:
        if readResult:
            title = readResultTitle
        else:
            title = ""

        # Under Maintenance (aka I'm too lazy to fix)

        """
        DrawDiagram.plt.switch_backend("TkAgg")
        DrawDiagram.DrawCompareDiagram(model, data, title)
        DrawDiagram.plt.switch_backend("Agg")
        """


if __name__ == "__main__":
    # 1. Read Experiment Datas
    ReadExperimentDatas()
    # 2. Setup Parameters
    SetupParameters()
    # 3. Data Processing
    DataProcessing()
    # 4. Draw results
    DrawResults()
    # 5. End of the program
    input("\nPress any key to exit\n")
