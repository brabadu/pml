from collections import namedtuple


PmlNode = namedtuple('PmlNode', ['block', 'sub_nodes'])


def pml_node(block, sub_nodes=None):
    if not sub_nodes:
        sub_nodes = []
    sub_nodes_dict = {}
    for sub_block in sub_nodes:
        sub_nodes_dict.update(sub_block)
    return {
        block.tag_name: PmlNode(
            block=block,
            sub_nodes=sub_nodes_dict
        )
    }
