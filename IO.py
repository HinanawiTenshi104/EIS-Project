# import ast
import os
import shutil

import numpy as np
import send2trash
from lmfit import minimizer

import DataProcessor
import DrawDiagram
import DRT
import Model
import Optimizer

drawProcessedDataInCompareDiagram = False

defaultDataDir = "Datas\\ExperimentDatas"
defaultProcessedDataDir = "Datas\\PreprocessedDatas"
defaultResultDir = "Datas\\Results"
defaultDRTDir = "Datas\\DRTDatas"
defaultDirs = {
    "Data Dir": defaultDataDir,
    "Processed Data Dir": defaultProcessedDataDir,
    "DRT Data Dir": defaultDRTDir,
    "Result Dir": defaultResultDir,
}
dirs = defaultDirs

dataDtype = [("frequency", np.float64), ("impedance", np.complex128)]
DRTDtype = [("tau", np.float64), ("gamma", np.float64)]

supportedDataExts = [".txt"]
dataLineSplitTexts = [" ", ",", "\t", ", "]

resultStandards = ["MSE", "R2", "MSD"]
resultStandardsReverse = [False, True, False]
resultDefaultStandard = "R2"


def ReadData(relativePath: str) -> np.ndarray:
    if not relativePath.endswith(".txt"):
        print(f"文件格式不为.txt:{relativePath}")
        return None

    filePath = os.path.join(dirs["Data Dir"], relativePath)
    data = []
    try:
        with open(filePath, "r", encoding="utf-8") as file:
            for line in file:
                if line[0] == "#":
                    continue

                success = False
                for splitText in dataLineSplitTexts:
                    dataLine = line.split(splitText)

                    if len(dataLine) != 3:
                        continue

                    try:
                        frequency = float(dataLine[0])
                        impedance = complex(float(dataLine[1]), float(dataLine[2]))
                        data.append((frequency, impedance))

                        success = True
                        break
                    except:
                        continue

                if not success:
                    print(f"格式错误：{line.strip()}")

        dataNp = np.array(data, dtype=dataDtype)
        # 阻抗取共轭
        if np.sum(dataNp["impedance"].imag < 0) >= len(dataNp["impedance"]) // 2:
            dataNp["impedance"] = np.conj(dataNp["impedance"])
        # 频率变成从小到大
        sortIndices = np.argsort([data["frequency"] for data in dataNp])
        dataNp = dataNp[sortIndices]

        return dataNp

    except FileNotFoundError:
        print(f"文件未找到：{filePath}")
        return None


def ReadAllDatas(
    dataDir: str = dirs["Data Dir"],
) -> tuple[list[np.ndarray], list[str]]:
    dataNames = os.listdir(dataDir)
    if len(dataNames) == 0:
        raise ValueError(f"No data Found in directory {dataDir}!")

    datas = []
    for fileName in dataNames:
        if not fileName.endswith(".txt"):
            continue

        data = ReadData(fileName)
        datas.append(data)

    for dataName in dataNames:
        dataName = dataName.strip(".txt")

    return datas, dataNames


def WriteData(
    data: np.ndarray,
    dataTitle: str = "data.txt",
    savePath: str = dirs["Processed Data Dir"],
    splitRealAndImag: bool = True,
):
    if not dataTitle.endswith(".txt"):
        dataTitle += ".txt"

    filePath = os.path.join(savePath, dataTitle)
    directory = os.path.dirname(filePath)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(filePath, "w", encoding="UTF-8") as file:
        if splitRealAndImag:
            file.write("Frequency\tReal\tImag\n")
        else:
            file.write("Frequency\tImpedance\n")
        for f, z in np.nditer([data["frequency"], data["impedance"]]):
            z = z.conjugate()
            if splitRealAndImag:
                file.write(f"{f}\t{z.real}\t{z.imag}\n")
            else:
                file.write(f"{f}\t{z}\n")


def WriteDatas(
    datas: list[np.ndarray],
    dataNames: list[str],
    savePath: str = dirs["Processed Data Dir"],
    splitRealAndImag: bool = True,
):
    for data, dataName in zip(datas, dataNames):
        WriteData(data, dataName, savePath, splitRealAndImag)


def WriteResult(
    resultText: str, resultTitle: str = "result.txt", printResult: bool = True
):
    if not resultTitle.endswith(".txt"):
        resultTitle += ".txt"

    filePath = os.path.join(dirs["Result Dir"], resultTitle)
    directory = os.path.dirname(filePath)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(filePath, "w", encoding="UTF-8") as file:
        file.write(resultText)

    if printResult:
        print(f"Results in folder: \\{directory}")


def ReadResult(resultTitle: str) -> tuple[list[float], list[int]]:
    if not resultTitle.endswith(".txt"):
        resultTitle += ".txt"

    filePath = os.path.join(dirs["Result Dir"], resultTitle)
    with open(filePath, "r", encoding="UTF-8") as file:
        for line in file:
            if "RCircuit:" in line:
                RCircuit = float(line.split(": ")[1].strip())
            elif "Rs:" in line:
                Rs = float(line.split(": ")[1].strip())
            elif "L:" in line:
                L = float(line.split(": ")[1].strip())
            elif "Beta:" in line:
                betaStr = line.split(": ")[1].strip().strip("[]").split(", ")
                beta = [float(num) for num in betaStr]
            elif "R:" in line:
                RStr = line.split(": ")[1].strip().strip("[]").split(", ")
                R = [float(num) for num in RStr]
            elif "C:" in line:
                CStr = line.split(": ")[1].strip().strip("[]").split(", ")
                C = [float(num) for num in CStr]
            # elif "Bounds:" in line:
            #   boundsStr = line.split(": ")[1].strip()
            #   boundsPairs = [pair.strip().split() for pair in boundsStr.split(",")]
            #   bounds = [(float(pair[0]), float(pair[1])) for pair in boundsPairs]
            # yeah... kinda lame to give up and use eval(), but it is what it is...(2024.10.15)
            #   bounds = ast.literal_eval(boundsStr)
            # And... turns out I don't even know what to do about these read hyper parameters,
            # it's already optimized after all.
            # So yeah, on top of dirty code its also useless, hooray!
            # (The only reason I left it here will be to just tell the history)
            # (And yes, I AM being extremely sarcastic)

    consts = [RCircuit, Rs, L]
    parameters = consts + beta + R + C
    paraFormat = [len(consts), len(R), len(beta) != 1]
    return parameters, paraFormat  # , bounds


def GenerateResult(
    result: minimizer.MinimizerResult,
    model: Model.Model,
    cost: float,
    hyperParameters: list,
    time: float,
    saveName: str,
    savePath: str,
    saveImgWhenProcessing: bool,
    drawProcessedDataInCompareDiagram: bool,
    ogData: np.ndarray,
    data: np.ndarray,
    DRTData: np.ndarray,
    dataName: str,
    drawOptions: list[bool, bool, bool],
    printResult: bool,
):
    R2 = DataProcessor.R2(ogData, result, model)
    MSD = DataProcessor.MSD(ogData, result, model)
    costsText = f"MSE: {cost}, R2: {R2}, MSD: {MSD}"
    resultText = DataProcessor.GenerateResultText(
        result, model, costsText, hyperParameters, time
    )

    if printResult:
        print(resultText, end="\n\n")

    WriteResult(resultText, os.path.join(savePath, saveName), printResult)

    if saveImgWhenProcessing:
        varmaps = model.circuit.varmaps
        parametersChanged = DataProcessor.ChangeParameterType(varmaps, result.params)
        model.UpdateParameters(parametersChanged)
        modelData = DataProcessor.GetModelData(model, ogData)

        datas = [ogData, modelData, data]
        labels = ["Exp-Data", "Model", "Processed-Data"]

        if drawProcessedDataInCompareDiagram == False:
            datas.pop()
            labels.pop()

        DrawDiagram.DrawCompareDiagram(
            datas=datas,
            labels=labels,
            title=dataName,
            savePath=savePath,
            drawOptions=drawOptions,
            show=False,
            saveImg=True,
        )
        if DRTData is not None:
            DrawDiagram.DrawDRTDiagram(
                DRTData=DRTData,
                label="DRT",
                title=dataName,
                saveName=dataName + "\\DRT.png",
                show=False,
                saveImg=True,
            )


def GenerateBatchResult(
    preProcessorInfo: list,
    totalTime: float,
    dataNames: list[str],
    methods: list[str],
    bestCosts: list[float],
    bestMethods: list[str],
    dataTimes: list[float],
    saveName: str = "batch info.txt",
):
    resultText = "Batch Info:\n\n"
    for dataName, bestCost, bestMethod, dataTime in zip(
        dataNames, bestCosts, bestMethods, dataTimes
    ):
        resultText += f"{dataName}:\n"
        resultText += f"\tBest Method: {bestMethod}\n"
        resultText += f"\tBest Cost(MSE): {bestCost}\n"
        resultText += f"\tTime Usage: {dataTime:.3f} Seconds\n"

    resultText += f"\nTotal Time Usage: {totalTime:.3f} Seconds\n"

    resultText += DataProcessor.GeneratePreProcessorInfo(preProcessorInfo)

    resultText += f"\nOptimizer Infos:\n"
    resultText += f"Used Methods:\n\t{methods}\n"
    resultText += f"Residual Type: {Optimizer.residualType}\n"
    resultText += f"Normalization Mode: {Optimizer.normalizationMode}\n"
    resultText += f"Residual Structure: {Optimizer.residualStuc}\n"
    resultText += f"Residual Function Mode: {Optimizer.residualMode}\n"
    if Optimizer.residualMode == Optimizer.residualModes[3]:
        resultText += f"\tDelta of the Huber Loss: {Optimizer.delta}\n"
    resultText += f"Apply Weight To Residual: {Optimizer.applyWeight}\n"
    if Optimizer.applyWeight:
        resultText += f"Weight Options: {Optimizer.weightOptions}\n"
        resultText += f"dzWeight Options: {Optimizer.dzweightOptions}\n"
        resultText += f"diWeight Options: {Optimizer.diweightOptions}\n"

    WriteResult(resultText, saveName, False)


def ChangeResultsStructure(
    dataNames: list[str], straList: list[str], deleteOriginal: bool = True
):
    dataNames = [dataName.strip(".txt") for dataName in dataNames]
    dataNames = sorted(dataNames, key=len, reverse=True)

    # 遍历result文件夹下的所有子文件夹和文件
    for straFolder in os.listdir(dirs["Result Dir"]):
        if (
            os.path.isdir(os.path.join(dirs["Result Dir"], straFolder))
            and straFolder in straList
        ):
            straPath = os.path.join(dirs["Result Dir"], straFolder)
            # 对每个stra文件夹
            for fileName in os.listdir(straPath):
                # 找到对应的dataName文件
                for dataName in dataNames:
                    if fileName.startswith(dataName):
                        newDataFolder = os.path.join(dirs["Result Dir"], dataName)
                        if not os.path.exists(newDataFolder):
                            os.makedirs(newDataFolder)

                        fileBase, fileExt = os.path.splitext(fileName)
                        if fileExt == ".txt":
                            fileBase = fileBase[len(dataName) :]
                            dstFileName = f"{straFolder}{fileExt}"
                        else:
                            fileBase = fileBase[len(dataName) + 1 :]
                            dstFileName = f"{fileBase}@{straFolder}{fileExt}"

                        srcFilePath = os.path.join(straPath, fileName)
                        dstFilePath = os.path.join(newDataFolder, dstFileName)

                        if deleteOriginal:
                            shutil.move(srcFilePath, dstFilePath)
                        else:
                            shutil.copy2(srcFilePath, dstFilePath)

                        break
            if deleteOriginal:
                os.removedirs(straPath)


def ReadDRTData(DRTDataTitle: str) -> np.ndarray:
    if not DRTDataTitle.endswith(".txt"):
        DRTDataTitle += ".txt"

    filePath = os.path.join(dirs["DRT Data Dir"], DRTDataTitle)
    data = []
    try:
        with open(filePath, "r", encoding="utf-8") as file:
            dataflag = False
            for i, line in enumerate(file):
                if "tau, gamma(tau)" in line:
                    dataflag = True
                    continue
                if not dataflag:
                    continue

                success = False
                for splitText in dataLineSplitTexts:
                    dataLine = line.split(splitText)

                    if len(dataLine) != 2:
                        continue

                    try:
                        tau = float(dataLine[0])
                        gamma = float(dataLine[1])
                        data.append((tau, gamma))

                        success = True
                        break
                    except:
                        continue

                if not success:
                    print(f"第{i}行格式错误：{line}")

        dataNp = np.array(data, dtype=DRTDtype)

        return dataNp

    except FileNotFoundError:
        print(f"文件未找到：{filePath}")
        return None


def runDRT(inputPaths: list[str], outputPaths: list[str], overwrite: bool = True):
    if not overwrite:
        newInputPaths = []
        newOutputPaths = []
        for inputPath, outputPath in zip(inputPaths, outputPaths):
            if os.path.isfile(outputPath):
                continue

            newInputPaths.append(inputPath)
            newOutputPaths.append(outputPath)
        inputPaths = newInputPaths
        outputPaths = newOutputPaths

    for inputPath, outputPath in zip(inputPaths, outputPaths):
        DRT.runDRT(inputPath, outputPath)


def cleanupDirectory(dir: str):
    for fileName in os.listdir(dir):
        if not (fileName.startswith("[") and fileName.endswith("]")):
            filePath = os.path.join(dir, fileName)

            if os.path.isfile(filePath) or os.path.isdir(filePath):
                relPath = os.path.relpath(filePath, os.getcwd())
                print(f"Clean up: {relPath}")

                send2trash.send2trash(filePath)
    print("Clean Up Complete!")
