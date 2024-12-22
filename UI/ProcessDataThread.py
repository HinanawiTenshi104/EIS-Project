import time

import numpy as np
from PyQt6.QtCore import QThread, pyqtSignal

import IO
import Optimizer


class ProcessDataThread(QThread):
    # Booleans
    saveOnlyBestResult = False
    drawOptions = [True, True, False]
    printResult = False
    saveImgWhenProcessing = True
    drawProcessedDataInCompareDiagram = False
    changeResultStructure = True

    # Parameters
    datas = []
    dataNames = []
    ogDatas = []
    DRTDatas = []
    boundTypes = []
    models = []

    preprocessorInfo = []
    methodList = []

    hyperParameters = [None, None]

    # Signals
    progressBarUpdateSignal = pyqtSignal(list)
    currentDataNameUpdateSignal = pyqtSignal(str)
    currentMethodNameUpdateSignal = pyqtSignal(str)
    finishedProcessingSignal = pyqtSignal()

    def run(self):
        totalTimeStart = time.time()
        self.methodList = self.hyperParameters[1]

        totalProgressCounts = len(self.datas) * len(self.methodList)
        dataProgressCounts = len(self.methodList)
        totalProgressCounter = 0
        dataProgressCounter = 0

        bestMethods = []
        bestCosts = []
        dataTimes = []

        for data, dataName, ogData, DRTData, boundType, model in zip(
            self.datas,
            self.dataNames,
            self.ogDatas,
            self.DRTDatas,
            self.boundTypes,
            self.models,
        ):
            self.currentDataNameUpdateSignal.emit(dataName)

            dataTimeStart = time.time()
            dataProgressCounter = 0

            bestMethod = ""
            bestResult = None
            bestCost = float("inf")

            # Optimization
            print(f"\nOptimizing {dataName}...")

            self.hyperParameters[0] = boundType

            for method in self.methodList:
                self.currentMethodNameUpdateSignal.emit(method)

                methodTimeStart = time.time()

                totalProgressCounter += 1
                dataProgressCounter += 1

                savePath = method

                # Get Result
                self.hyperParameters[1] = method
                result = Optimizer.curveFit(self.hyperParameters, data, model)

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

                if not self.saveOnlyBestResult:
                    IO.GenerateResult(
                        result,
                        model,
                        optimizedCost,
                        self.hyperParameters,
                        methodTime,
                        dataName,
                        savePath,
                        self.saveImgWhenProcessing,
                        self.drawProcessedDataInCompareDiagram,
                        ogData,
                        data,
                        DRTData,
                        dataName,
                        self.drawOptions,
                        self.printResult,
                    )

                dataProgress = int(dataProgressCounter / dataProgressCounts * 100)
                totalProgress = int(totalProgressCounter / totalProgressCounts * 100)
                self.progressBarUpdateSignal.emit([dataProgress, totalProgress])

            # Generate Data Results
            dataTimeEnd = time.time()
            dataTime = dataTimeEnd - dataTimeStart
            print(f"Data Time Usage: {dataTime:.3f} Seconds")

            bestMethods.append(bestMethod)
            bestCosts.append(bestCost)
            dataTimes.append(dataTime)

            if self.saveOnlyBestResult:
                IO.GenerateResult(
                    bestResult,
                    model,
                    bestCost,
                    self.hyperParameters,
                    dataTime,
                    dataName,
                    "",
                    self.saveImgWhenProcessing,
                    self.drawProcessedDataInCompareDiagram,
                    ogData,
                    data,
                    DRTData,
                    dataName,
                    self.drawOptions,
                    self.printResult,
                )

        totalTimeEnd = time.time()
        totalTime = totalTimeEnd - totalTimeStart

        IO.GenerateBatchResult(
            self.preprocessorInfo,
            totalTime,
            self.dataNames,
            self.methodList,
            bestCosts,
            bestMethods,
            dataTimes,
            "batch info",
        )
        print(f"\nTotal Time Usage: {totalTime:.3f} Seconds")

        if self.changeResultStructure:
            IO.ChangeResultsStructure(self.dataNames, self.methodList)

        self.finishedProcessingSignal.emit()
