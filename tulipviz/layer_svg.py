from lxml import etree as ET

def is_white_group(group, ns):
    rects = group.xpath('.//svg:rect', namespaces={'svg': ns})
    for rect in rects:
        fill = rect.attrib.get('fill', '').lower()
        if '255,255,255' in fill or fill in ('#ffffff', 'white'):
            return True
    return False

def is_magenta_group(group, ns):
    rects = group.xpath('.//svg:rect', namespaces={'svg': ns})
    for rect in rects:
        fill = rect.attrib.get('fill', '').lower()
        if '255,192,255' in fill:
            return True
    return False

def is_relevant_group(group, ns):
    return is_white_group(group, ns) or is_magenta_group(group, ns)

def push_white_groups_to_end(svg_path, output_path=None):
    parser = ET.XMLParser(remove_blank_text=True)
    tree = ET.parse(svg_path, parser)
    root = tree.getroot()
    ns = root.nsmap.get(None, 'http://www.w3.org/2000/svg')

    all_groups = root.xpath('.//svg:g', namespaces={'svg': ns})

    white_groups = []
    non_white_groups = []

    for group in all_groups:
        parent = group.getparent()
        if parent is None:
            continue
        if is_relevant_group(group, ns):
            white_groups.append((group, parent))
        else:
            non_white_groups.append((group, parent))

    # Remove and re-append white groups to the end of their parent
    for group, parent in white_groups:
        parent.remove(group)
        parent.append(group)

    # Save the modified SVG
    if output_path:
        tree.write(output_path, encoding='UTF-8', xml_declaration=True, pretty_print=True)
        return output_path
    else:
        return ET.tostring(tree, encoding='unicode', pretty_print=True)
