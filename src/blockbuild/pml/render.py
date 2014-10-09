# coding=utf-8
from inspect import ismodule
from inspect import getmembers
from itertools import imap

# from webhelpers.html import literal

literal = lambda x: x

from . import formats


class StopRendering(StopIteration):
    pass


def _render_pml(
        root_node,
        context,
        pml_nodes,
        pml_mediate_nodes=None,
):
    pml_mediate_nodes = pml_mediate_nodes or {}

    node_name, attributes, sub_nodes = root_node

    pml_node = pml_nodes.get(node_name)

    if pml_node:
        pml_sub_nodes = pml_node.sub_nodes

        if len(sub_nodes) == 0 and len(pml_sub_nodes) > 0:
            raise ValueError(
                'Template node "{node}" has no children defined'.format(node=node_name)
            )
    else:
        pml_node = pml_mediate_nodes.get(node_name)
        pml_sub_nodes = pml_nodes

    if pml_node is None:
        raise ValueError(
            'PML node "{node}" is not found!'.format(node=node_name)
        )

    block = pml_node.block

    partial_block = block.partial(context)
    try:
        block_context = partial_block.call(**attributes)
    except StopRendering:
        return u''

    current_block_content = []
    iter_context = block_context if block.is_multiple else [block_context]
    for current_context in iter_context:
        render_context = {}
        render_context.update(context)
        render_context.update(current_context)
        rendered_block_content = imap(
            lambda child: _render_pml(
                child,
                render_context,
                pml_sub_nodes,
                pml_mediate_nodes,
            ),
            sub_nodes
        )
        render_context.update(
            tag_content=literal('').join(
                rendered_block_content
            ).strip(),
            tag_node=root_node
        )
        current_block_content.append(partial_block.render(render_context))

    if partial_block.wrapper is not None:
        wrapper_context = {}
        wrapper_context.update(context)
        wrapper_context.update(
            partial_block.wrapper.partial(context).call()
        )
        wrapper_context.update(
            tag_content=literal('').join(
                current_block_content
            )
        )
        result = partial_block.wrapper.render(wrapper_context)
    else:
        result = literal('').join(current_block_content)

    return result


_formats_processors = dict(getmembers(formats, ismodule))


def render_pml_template(pml_template, pml_format, context, pml_nodes,
                        pml_mediate_nodes=None, max_blocks_nesting_level=50):
    format = _formats_processors.get(pml_format)
    pml_tree = format.loads(pml_template, max_blocks_nesting_level)
    return _render_pml(pml_tree, context, pml_nodes, pml_mediate_nodes)


def dump_pml_template(root_node, pml_format):
    format = _formats_processors.get(pml_format)
    return format.dumps(root_node)
