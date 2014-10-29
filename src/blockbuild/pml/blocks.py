from functools import partial
from inspect import getargspec
from inspect import isgeneratorfunction

from flask import render_template
from flask import current_app
from jinja2.runtime import Context

from .render import StopRendering


class Jinja2PmlBlock(object):
    def __init__(self, func, template_name, block_name,
                 _tag_name, wrapper=None):
        self._func = func
        self._template_name = template_name
        self._block_name = block_name
        self._tag_name = _tag_name or block_name
        self._wrapper = wrapper

        self._func_spec = getargspec(func)

    def call(self, *args, **kwargs):
        return self._func(*args, **kwargs)

    def render(self, ctx):
        env = current_app.jinja_env
        jinja_ctx = Context(env, ctx, self._block_name, {})
        return ''.join(env.get_template(self._template_name)
                          .blocks[self._block_name](jinja_ctx))

    @property
    def tag_name(self):
        return self._tag_name

    @property
    def is_multiple(self):
        return isgeneratorfunction(self._func)

    def __call__(self, *args, **kwargs):
        try:
            if self.is_multiple:
                iter_context = self.call(*args, **kwargs)
            else:
                iter_context = [self.call(*args, **kwargs)]
        except StopRendering:
            return u''

        rendered_content = map(self.render, iter_context)

        return (u'').join(rendered_content)

    def wanted_context(self, context):
        return {
            k: context[k] for k in self._func_spec.args if k in context
        }

    def __repr__(self):
        return (
            u"<PmlBlock(template_name='{template_name}', tag_name='{tag_name}')>".format(
                template_name=self._template_name,
                tag_name=self._tag_name
            )
        )


def pml_block(template_name, block_name, tag_name=None):
    def decorator(func):
        return Jinja2PmlBlock(func, template_name, block_name, tag_name)

    return decorator
