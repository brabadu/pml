# -*- coding: utf-8 -*-

from uaprom.lib.pml import pml_block


_template = "/admin/vertical/dangerous_html.mako"


@pml_block(_template, "dangerous_html")
def dangerous_html(text):
    return {"text": text}
