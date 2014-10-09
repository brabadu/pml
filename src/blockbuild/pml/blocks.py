from functools import partial
from inspect import getargspec
from inspect import isgeneratorfunction
# from mako.runtime import Context
# from webhelpers.html.builder import literal

from flask import render_template

from .render import StopRendering


class MakoBlock(object):

    def __init__(self, func, template_name, def_name):
        self._func = func
        self._template_name = template_name
        self._def_name = def_name

    def call(self, *args, **kwargs):
        return self._func(*args, **kwargs)

    def render(self, ctx):
        return render_mako_def(self._template_name, self._def_name, **ctx)

    def __call__(self, *args, **kwargs):
        if args and isinstance(args[0], Context):
            args = args[1:]
        return self.render(self.call(*args, **kwargs))


class MakoPmlBlock(MakoBlock):
    def __init__(self, func, template_name, def_name,
                 tag_name=None, wrapper=None):
        super(MakoPmlBlock, self).__init__(func, template_name, def_name)
        self._tag_name = tag_name if tag_name is not None else def_name
        self._wrapper = wrapper

    @property
    def tag_name(self):
        return self._tag_name

    @property
    def wrapper(self):
        return self._wrapper

    @property
    def is_multiple(self):
        return isgeneratorfunction(self._func)

    def __call__(self, *args, **kwargs):
        if args and isinstance(args[0], Context):
            args = args[1:]

        try:
            if self.is_multiple:
                iter_context = self.call(*args, **kwargs)
            else:
                iter_context = [self.call(*args, **kwargs)]
        except StopRendering:
            return u''


        rendered_content = map(self.render, iter_context)

        return literal('').join(rendered_content)

    def partial(self, context):
        func_spec = getargspec(self._func)
        func_kwargs = {
            k: v for k, v in context.iteritems() if k in func_spec.args
        }
        partial_func = partial(self._func, **func_kwargs)
        block = self.__class__(
            partial_func,
            self._template_name,
            self._def_name,
            self._tag_name,
            self._wrapper
        )

        return block

    def __repr__(self):
        return (
            u"<PmlBlock(def_name='{def_name}', tag_name='{tag_name}')>".format(
                def_name=self._def_name,
                tag_name=self._tag_name
            )
        )


class Jinja2Block(object):

    def __init__(self, func, template_name):
        self._func = func
        self._template_name = template_name

    def call(self, *args, **kwargs):
        return self._func(*args, **kwargs)

    def render(self, ctx):
        return render_template(self._template_name, **ctx)

    def __call__(self, *args, **kwargs):
        # if args and isinstance(args[0], Context):
        #     args = args[1:]
        return self.render(self.call(*args, **kwargs))



class Jinja2PmlBlock(Jinja2Block):
    def __init__(self, func, template_name,
                 _tag_name, wrapper=None):
        super(Jinja2PmlBlock, self).__init__(func, template_name)
        self._tag_name = _tag_name
        self._wrapper = wrapper

    @property
    def tag_name(self):
        return self._tag_name

    @property
    def is_multiple(self):
        return isgeneratorfunction(self._func)

    @property
    def wrapper(self):
        return self._wrapper

    def __call__(self, *args, **kwargs):
        # if args and isinstance(args[0], Context):
        #     args = args[1:]

        try:
            if self.is_multiple:
                iter_context = self.call(*args, **kwargs)
            else:
                iter_context = [self.call(*args, **kwargs)]
        except StopRendering:
            return u''


        rendered_content = map(self.render, iter_context)

        return (u'').join(rendered_content)

    def partial(self, context):
        func_spec = getargspec(self._func)
        func_kwargs = {
            k: v for k, v in context.iteritems() if k in func_spec.args
        }
        partial_func = partial(self._func, **func_kwargs)
        block = self.__class__(
            partial_func,
            self._template_name,
            self._tag_name,
            self._wrapper
        )

        return block

    def __repr__(self):
        return (
            u"<PmlBlock(template_name='{template_name}', tag_name='{tag_name}')>".format(
                template_name=self._template_name,
                tag_name=self._tag_name
            )
        )


def pml_block(template_name, tag_name=None):
    def decorator(func):
        return Jinja2PmlBlock(func, template_name, tag_name)

    return decorator
