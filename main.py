from js import document
from pyodide.ffi import create_proxy

canvas = document.getElementById("canvas")
ctx = canvas.getContext("2d")
mode_select = document.getElementById("mode")
color_picker = document.getElementById("color")

start = {"x": 0, "y": 0, "drawing": False}

def get_mouse_pos(evt):
    rect = canvas.getBoundingClientRect()
    return {
        "x": evt.clientX - rect.left,
        "y": evt.clientY - rect.top
    }

def mousedown(evt):
    pos = get_mouse_pos(evt)
    start["x"] = pos["x"]
    start["y"] = pos["y"]
    start["drawing"] = True

    if mode_select.value == "dot":
        ctx.fillStyle = color_picker.value
        ctx.fillRect(pos["x"], pos["y"], 2, 2)

def mousemove(evt):
    if not start["drawing"]:
        return
    pos = get_mouse_pos(evt)
    ctx.strokeStyle = color_picker.value

    if mode_select.value == "freedraw":
        ctx.beginPath()
        ctx.moveTo(start["x"], start["y"])
        ctx.lineTo(pos["x"], pos["y"])
        ctx.stroke()
        start["x"], start["y"] = pos["x"], pos["y"]

def mouseup(evt):
    if not start["drawing"]:
        return
    pos = get_mouse_pos(evt)
    ctx.strokeStyle = color_picker.value
    ctx.fillStyle = color_picker.value
    ctx.beginPath()

    if mode_select.value == "line":
        ctx.moveTo(start["x"], start["y"])
        ctx.lineTo(pos["x"], pos["y"])
        ctx.stroke()
    elif mode_select.value == "rect":
        width = pos["x"] - start["x"]
        height = pos["y"] - start["y"]
        ctx.strokeRect(start["x"], start["y"], width, height)
    elif mode_select.value == "circle":
        radius = ((pos["x"] - start["x"]) ** 2 + (pos["y"] - start["y"]) ** 2) ** 0.5
        ctx.arc(start["x"], start["y"], radius, 0, 2 * 3.1416)
        ctx.stroke()
    elif mode_select.value == "ellipse":
        radiusX = abs(pos["x"] - start["x"]) / 2
        radiusY = abs(pos["y"] - start["y"]) / 2
        centerX = (start["x"] + pos["x"]) / 2
        centerY = (start["y"] + pos["y"]) / 2
        ctx.ellipse(centerX, centerY, radiusX, radiusY, 0, 0, 2 * 3.1416)
        ctx.stroke()

    ctx.closePath()
    start["drawing"] = False

canvas.addEventListener("mousedown", create_proxy(mousedown))
canvas.addEventListener("mousemove", create_proxy(mousemove))
canvas.addEventListener("mouseup", create_proxy(mouseup))
