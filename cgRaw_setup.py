import nuke

def setup_cgRaw_ui():
    if nuke.GUI:
        toolbar = nuke.menu("Nodes")
        cgRaw_menu = toolbar.addMenu("cgRaw", "cgRaw_icon.png")
        cgRaw_menu.addCommand("cgGrade", 'nuke.createNode("cgGrade")')
        cgRaw_menu.addCommand("cgHueShift", 'nuke.createNode("cgHueShift")')
        cgRaw_menu.addCommand("cgBlur", 'nuke.createNode("cgBlur")')
        cgRaw_menu.addCommand("cgIsolate", 'nuke.createNode("cgIsolate")')
        cgRaw_menu.addCommand("cgErrorCheck", 'nuke.createNode("cgErrorCheck")')
        cgRaw_menu.addCommand("cgAddCustom", 'nuke.createNode("cgAddCustom")')