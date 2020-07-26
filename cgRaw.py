import nuke
import re

def filter_check(filter):

    if len(filter) == 1:
        if filter[0] == '*':
            filter = '(.*)'
        else:
            filter = filter[0]
    else:
        filter = re.compile('|'.join(filter))
    return filter


def selection_filter(node):

    coloraovs = node.channels()
    coloraovs = set([item.split('.')[0] for item in coloraovs if re.search('_col_', item)])

    lightfilter = node.knob('lightfilter').getValue().split(' ')
    componentfilter = node.knob('componentfilter').getValue().split(' ')

    if node.knob('invertlightfilter').getValue() == 0:
        collection = [i for i in coloraovs if re.search(filter_check(lightfilter), i)]
    else:
        collection = [i for i in coloraovs if not re.search(filter_check(lightfilter), i)]

    if node.knob('invertcomponentfilter').getValue() == 0:
        collection = [i for i in collection if re.search(filter_check(componentfilter), i)]
    else:
        collection = [i for i in collection if not re.search(filter_check(componentfilter), i)]

    return collection


def selection_panel(layerset):
    coloraovs = nuke.thisNode().channels()
    coloraovs = set([item.split('.')[0] for item in coloraovs if re.search('_col_', item)])
    if layerset == 'lights':
        coloraovs = set([ i.split('_col_')[0] for i in coloraovs])
    else:
        lightfilter = nuke.thisNode()['lightfilter'].getValue().split(' ')
        if nuke.thisNode().knob('invertlightfilter').getValue() == 0:
            collection = [i for i in coloraovs if re.search(filter_check(lightfilter), i)]
        else:
            collection = [i for i in coloraovs if not re.search(filter_check(lightfilter), i)]
        coloraovs = set([ i.split('_col_')[1] for i in collection])
    p = nuke.Panel('select ' + layerset)
    p.addBooleanCheckBox('all', False)
    for i in coloraovs:
        p.addBooleanCheckBox(i, False)
    if p.show() == 1:
        coloraovs.add('all')
        selection = [i for i in coloraovs if p.value(i)]
        if 'all' in selection:
            selection = '*'
        if layerset == 'lights':
            nuke.thisNode()['lightfilter'].setValue((' ').join(selection))
        else:
            nuke.thisNode()['componentfilter'].setValue((' ').join(selection))


def clone_node(node):

    exclude_list = ['xpos','ypos', 'help', 'useLifetime', 'lifetimeEnd', 'lifetimeStart', 'bookmark', 'dope_sheet', 'postage_stamp_frame', 'hide_input', 'updateUI', 'note_font_color', 'onCreate', 'knobChanged', 'note_font', 'tile_color', 'selected', 'autolabel', 'process_mask', 'label', 'onDestroy', 'indicators', 'maskFrom', 'Mask', 'postage_stamp', 'disable', 'maskChannelMask', 'panel', 'maskFromFlag', 'name', 'cached', 'fringe', 'filter', 'gl_color', 'transform', 'note_font_size']

    orig_selection = nuke.selectedNodes()

    [n.setSelected(False) for n in nuke.selectedNodes()]
    node.setSelected(True)

    nuke.nodeCopy("%clipboard%")
    node.setSelected(False)
    nuke.nodePaste("%clipboard%")
    new_node = nuke.selectedNode()
    for i in node.knobs():
        if i not in exclude_list:

            new_node.knob(i).setExpression('%s.%s' % (node.name(), node.knob(i).name()))

            if isinstance(new_node.knob(i), nuke.AColor_Knob):
                new_node.knob(i).setValue([1,1,1,1])
            elif isinstance(new_node.knob(i), nuke.WH_Knob):
                new_node.knob(i).setValue([1,1])

    xpos = node.xpos()
    ypos = node.ypos()
    new_node.setXpos(xpos)
    new_node.setYpos(ypos + 80)
    new_node.addKnob(nuke.Boolean_Knob('is_copy', 'is Copy', 1))

    [n.setSelected(False) for n in nuke.selectedNodes()]
    [n.setSelected(True) for n in orig_selection]

    return new_node  


def update_insides(node):
    [nuke.delete(n) for n in nuke.allNodes() if n.knob('is_copy')]
    selection = selection_filter(node)
    with node:
        node = nuke.toNode('master')
        init = 1
        for i in selection:
            if init == 1:
                node.knob('channels').setValue(i)
            else:
                new_node = clone_node(node)
                new_node.knob('channels').setValue(i)
                new_node.setInput(0, node)
                new_node.setInput(1, nuke.toNode('mask'))
                node = new_node
            init = 0
        nuke.toNode('develope').setInput(0, new_node)


def update_isolate(node):
    selection = selection_filter(node)
    with node:
        node = nuke.toNode('master')
        expressions = {'expr0' : '.red', 'expr1' : '.green', 'expr2' : '.blue'}
        [node.knob(k).setValue(' + '.join([i + expressions[k] for i in selection])) for k in expressions.keys()]


def create_layer(node):
    light = node['lightname'].getValue()
    lobe = node['componentname'].getValue()
    layer = light + '_col_' + lobe
    nuke.Layer( layer , [ 'red', 'green', 'blue'])
    return layer


def update_addcustom(node):
    layer = create_layer(node)
    with node:
        nuke.toNode('addCustom')['out'].setValue(layer)