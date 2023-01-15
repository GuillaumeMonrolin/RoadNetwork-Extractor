from xml.dom import minidom


def generate_canva(svg_file, file_to_export):
    dom = minidom.parse(svg_file)

    dom = clean_geometries(dom)
    dom = resize_canva(dom)
    dom = add_border(dom)
    dom = add_city_name(dom)

    with open(file_to_export, 'w') as file:
        file.write(dom.toprettyxml())


def resize_canva(dom):
    dom.getElementsByTagName("svg")[0].setAttribute("width", "8.379cm")
    dom.getElementsByTagName("svg")[0].setAttribute("height", "10.043cm")
    dom.getElementsByTagName("svg")[0].setAttribute("viewBox", "0 0 576 691")

    return dom


def add_border(dom):
    for elem in dom.getElementsByTagName("g"):
        if elem.getAttribute("id") == "figure_1":
            rect = dom.createElement("rect")
            rect.setAttribute("x", "0")
            rect.setAttribute("y", "0")
            rect.setAttribute("width", "576")
            rect.setAttribute("height", "691")
            rect.setAttribute("style", "fill:rgb(255,255,255);stroke-width:3;stroke:rgb(255,0,0)")
            elem.insertBefore(rect, elem.childNodes[0])
    return dom


def add_city_name(dom):
    title = dom.createElement("text")
    title.setAttribute("x", "288")
    title.setAttribute("y", "660")
    title.setAttribute("font-size", "80")
    title.setAttribute("font-family", "Verdana")
    title.setAttribute("font-weight", "normal")
    title.setAttribute("letter-spacing", "0")
    title.setAttribute("text-anchor", "middle")
    title.setAttribute("fill", "white")
    title.setAttribute("stroke", "blue")
    title.appendChild(dom.createTextNode("Grenoble"))

    dom.getElementsByTagName("g")[0].appendChild(title)

    return dom


def clean_geometries(dom):
    for elem in dom.getElementsByTagName("g"):
        if "PatchCollection_" in elem.getAttribute("id"):
            for path in elem.getElementsByTagName("path"):
                path.setAttribute("style", "fill: #FFFFFF; stroke:blue;")
    return dom
