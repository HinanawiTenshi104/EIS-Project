# well, plt.close(fig) is not working with my current multithreading...
# so if you want to use plt.show(), switch backend before you do so,
# and promise to switch back to "Agg" when you're done, or...
# i won't like you anymore :(
# https://stackoverflow.com/questions/50742269/matplotlib-threading-closing-a-specific-figure-instance
# https://stackoverflow.com/questions/3285193/how-to-change-matplotlib-backends
import os
import tempfile

import matplotlib.axes as axes
import matplotlib.pyplot as plt
import numpy as np
import schemdraw
import schemdraw.elements as elm

import DataProcessor
import IO

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]  # 设置默认字体为微软雅黑
plt.rcParams["axes.unicode_minus"] = False  # 解决保存图像时负号'-'显示为方块的问题
plt.switch_backend("Agg")

diagramTypes = ["Nyquist", "Bode", "Derivative", "DRT"]


# schemdraw document: https://schemdraw.readthedocs.io/en/stable/index.html
def DrawCircuitDiagram(ringCount: int, title: str = ""):
    def addRing(diagram: schemdraw.Drawing, index: int):
        diagram += elm.Line().length(1.5).up()
        diagram += elm.Resistor().label(f"R{index}").right()
        diagram += elm.Line().length(1.5).down()
        diagram.push()
        diagram += elm.Line().length(1.5).down()
        diagram += elm.Capacitor().label(f"C{index}").left()
        diagram += elm.Line().length(1.5).up()
        diagram.pop()
        diagram += elm.Line().right()

    with schemdraw.Drawing(show=False) as diagram:
        diagram += elm.Line().right()
        diagram += elm.Line().length(1.5).up()
        diagram += elm.Resistor().label("Rs").right()
        diagram += elm.Line().length(1.5).down()
        diagram.push()
        diagram += elm.Line().length(1.5).down()
        diagram += elm.Inductor2().label("L").left()
        diagram += elm.Line().length(1.5).up()
        diagram.pop()
        diagram += elm.Line().right()
        for i in range(0, ringCount):
            addRing(diagram, i + 1)

    plt.ion()
    diagram.draw(canvas="matplotlib")
    plt.title(title)
    plt.pause(0.5)
    plt.ioff()


def NyquistDiagram(ax: axes.Axes, data: np.ndarray, title: str, label: str):
    real = np.real(data)
    imag = np.imag(data)

    ax.scatter(real, imag, label=label)
    ax.legend()
    ax.set_title(title)
    ax.set_xlabel("Re")
    ax.set_ylabel("Im")


def BodeDiagram(
    axPhase: axes.Axes, axMag: axes.Axes, data: np.ndarray, title: str, label: str
):
    fs = data["frequency"]
    zs = data["impedance"]
    phase, mag = DataProcessor.GetPhaseAndMagnitude(zs)

    fs = np.log10(fs)
    phase = np.rad2deg(phase)
    mag = np.log10(mag)

    axPhase.scatter(fs, phase, label=label + "-Phase")
    axPhase.legend()
    axPhase.set_title(title)
    axPhase.set_xlabel("log10(f)")
    axPhase.set_ylabel("phase")

    axMag.scatter(fs, mag, label=label + "-Magnitude")
    axMag.legend()
    axMag.set_xlabel("log10(f)")
    axMag.set_ylabel("log10(Magnitude)")


def DrawNyquistDigram(
    dataImpedances: list[np.ndarray],
    labels: list[str] = ["Exp-Data"],
    title: str = "Nyquist",
    saveName: str = "file",
    temp: bool = False,
    show: bool = True,
    saveImg: bool = False,
    block: bool = True,
):
    fig, ax = plt.subplots()
    savePath = os.path.join(IO.dirs["Result Dir"], saveName)
    directory = os.path.dirname(savePath)
    if not os.path.exists(directory):
        os.makedirs(directory)

    for dataImpedance, label in zip(dataImpedances, labels):
        NyquistDiagram(ax, dataImpedance, title, label)

    if temp:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            fig.savefig(tmpfile.name)
            plt.close(fig)
        return tmpfile.name

    if saveImg:
        fig.savefig(savePath)
    if show:
        plt.show(block=block)

    plt.close(fig)


def DrawBodeDiagram(
    datas: list[np.ndarray],
    labels: list[str] = ["Exp-Data"],
    title: str = "Bode",
    saveName: str = "file",
    temp: bool = False,
    show: bool = True,
    saveImg: bool = False,
    block: bool = True,
):
    fig, [axPhase, axMag] = plt.subplots(nrows=2, sharex="col")
    savePath = os.path.join(IO.dirs["Result Dir"], saveName)
    directory = os.path.dirname(savePath)
    if not os.path.exists(directory):
        os.makedirs(directory)

    for data, label in zip(datas, labels):
        BodeDiagram(axPhase, axMag, data, title, label)

    if temp:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            fig.savefig(tmpfile.name)
            plt.close(fig)
        return tmpfile.name

    if saveImg:
        fig.savefig(savePath)
    if show:
        plt.show(block=block)

    plt.close(fig)


def DrawDerivativeDigram(
    dataDerivatives: list[np.ndarray],
    labels: list[str] = ["Exp-Data"],
    title: str = "Derivative",
    saveName: str = "file",
    temp: bool = False,
    show: bool = True,
    saveImg: bool = False,
    block: bool = True,
):
    fig, ax = plt.subplots()
    savePath = os.path.join(IO.dirs["Result Dir"], saveName)
    directory = os.path.dirname(savePath)
    if not os.path.exists(directory):
        os.makedirs(directory)

    for dataDerivative, label in zip(dataDerivatives, labels):
        NyquistDiagram(ax, dataDerivative, title, label)

    if temp:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            fig.savefig(tmpfile.name)
            plt.close(fig)
        return tmpfile.name

    if saveImg:
        fig.savefig(savePath)
    if show:
        plt.show(block=block)

    plt.close(fig)


def DrawCompareDiagram(
    datas: list[np.ndarray],
    labels: list[str] = ["Exp-Data", "Model"],
    title: str = "Results",
    savePath: str = "",
    drawOptions: list[bool] = [True, False, False],
    show: bool = True,
    saveImg: bool = False,
    block: bool = True,
):
    title = title.strip(".txt")
    drawNyquist, drawBode, drawDerivative = drawOptions

    zs = []
    for data in datas:
        zs.append(data["impedance"])

    if drawDerivative:
        dzs = []
        for data in datas:
            dzs.append(DataProcessor.GetDataDerivatives(data))

    if drawNyquist:
        saveName = os.path.join(savePath, title + "-Nyquist.png")
        DrawNyquistDigram(
            zs,
            labels=labels,
            title=title,
            saveName=saveName,
            temp=False,
            show=show,
            saveImg=saveImg,
            block=block,
        )
    if drawBode:
        saveName = os.path.join(savePath, title + "-Bode.png")
        DrawBodeDiagram(
            datas,
            labels=labels,
            title=title,
            saveName=saveName,
            temp=False,
            show=show,
            saveImg=saveImg,
            block=block,
        )
    if drawDerivative:
        saveName = os.path.join(savePath, title + "-Derivative.png")
        DrawDerivativeDigram(
            dzs,
            labels=labels,
            title=title,
            saveName=saveName,
            temp=False,
            show=show,
            saveImg=saveImg,
            block=block,
        )


def DrawExtremums(
    z: np.ndarray,
    extremumIndex: np.ndarray,
    dataLabel: str = "Exp-Data",
    modelLabel: str = "Extremum",
    title: str = "Extremums",
):
    extremums = z[extremumIndex]
    impedances = [z, extremums]
    labels = [dataLabel, modelLabel]
    DrawNyquistDigram(impedances, labels=labels, title=title)


# DRTData: ["tau", "gamma"]
def DrawDRTDiagram(
    DRTData: np.ndarray,
    label: str = "DRT",
    title: str = "DRT Result",
    saveName: str = "file",
    temp: bool = False,
    show: bool = True,
    saveImg: bool = False,
    block: bool = True,
):
    fig, ax = plt.subplots()
    savePath = os.path.join(IO.dirs["Result Dir"], saveName)
    directory = os.path.dirname(savePath)
    if not os.path.exists(directory):
        os.makedirs(directory)

    x = np.log10(DRTData["tau"])
    y = DRTData["gamma"]

    ax.scatter(x, y, label=label)
    ax.legend()
    ax.set_title(title)
    ax.set_xlabel("log10(τ)")
    ax.set_ylabel("γ")

    if temp:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            fig.savefig(tmpfile.name)
            plt.close(fig)
        return tmpfile.name

    if saveImg:
        fig.savefig(savePath)
    if show:
        plt.show(block=block)

    plt.close(fig)
