from lxml.etree import tostring, _Comment
from lxml.html import Element, fromstring

literal = lambda x: x


def _loads_pml_from_xml_tree(node, max_blocks_nesting_level):
    if max_blocks_nesting_level == 0:
        raise ValueError("Nesting pml_node level too deep!")

    if isinstance(node, _Comment):
        return ['comment', {'text': literal(unicode(node.text))}, []]

    if node.tag == "dangerous_html":
        content = ''.join([tostring(child) for child in node.iterdescendants()])
        return [node.tag, {'text': literal(unicode(content))}, []]

    sub_nodes = []
    for sub_node in node.iterchildren():
        sub_nodes.append(
            _loads_pml_from_xml_tree(
                sub_node,
                max_blocks_nesting_level - 1
            )
        )

    return node.tag, node.attrib, sub_nodes


def loads(pml_template, max_blocks_nesting_level):
    return _loads_pml_from_xml_tree(
        fromstring(pml_template),
        max_blocks_nesting_level
    )


def _dumps_xml_from_pml_nodes(root_node):
    node_name, attributes, sub_nodes = root_node

    element = Element(node_name, **attributes)

    for sub_node in sub_nodes:
        element.append(_dumps_xml_from_pml_nodes(sub_node))

    return element


def dumps(root_node):
    return tostring(
        _dumps_xml_from_pml_nodes(root_node),
        method="xml"
    )
