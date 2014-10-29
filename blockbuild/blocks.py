from random import choice

from pml.blocks import pml_block
from pml.nodes import pml_node


@pml_block('all.html', 'container')
def container():
    return {}


@pml_block('all.html', 'content')
def content():
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


@pml_block('all.html', 'kittens')
def kittens(num=5):
    for i in xrange(int(num)):
        yield {
            'x':  choice(range(2, 5)) * 100,
            'y':  choice(range(2, 5)) * 100,
        }


container_node = pml_node(container, [
    pml_node(header),
    pml_node(content),
    pml_node(editor),
    pml_node(kittens),
])
