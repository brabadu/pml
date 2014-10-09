from pml.blocks import pml_block
from pml.nodes import pml_node


@pml_block('container.html', 'container')
def container():
    return {}


@pml_block('sub_a.html', 'sub_a')
def sub_a():
    return {
        'body': 'very body'
    }

@pml_block('header.html', 'header')
def header():
    return {
        'text': 'Wow. Such header'
    }


container_node = pml_node(container, [
    pml_node(header),
    pml_node(sub_a),
])
