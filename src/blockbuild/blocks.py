from pml.blocks import pml_block
from pml.nodes import pml_node


@pml_block('all.html', 'container')
def container():
    return {}


@pml_block('all.html', 'sub_a')
def sub_a():
    return {
        'body': 'very body'
    }


@pml_block('all.html', 'header')
def header():
    return {
        'text': 'Wow. Such header'
    }


@pml_block('all.html', 'editor')
def editor(page):
    return {
        'page': page
    }


container_node = pml_node(container, [
    pml_node(header),
    pml_node(sub_a),
    pml_node(editor),
])
