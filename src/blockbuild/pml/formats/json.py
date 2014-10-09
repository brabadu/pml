import simplejson as json


def _loads_pml_from_json_tree(node, max_blocks_nesting_level):
    if max_blocks_nesting_level == 0:
        raise ValueError("Nesting pml_node level too deep!")

    name, attributes, nodes = node

    sub_nodes = [
        _loads_pml_from_json_tree(sub_node, max_blocks_nesting_level - 1)
        for sub_node in nodes
    ]

    return name, attributes, sub_nodes


def loads(pml_template, max_blocks_nesting_level):
    json_tree = json.loads(pml_template)
    return _loads_pml_from_json_tree(json_tree, max_blocks_nesting_level)


def dumps():
    raise NotImplementedError
