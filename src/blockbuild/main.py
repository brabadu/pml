# all the imports
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

DEBUG = True
SECRET_KEY = 'development key'
app = Flask(__name__)
app.config.from_object(__name__)

from blocks import container_node
from pml.render import render_pml_template


TEMPLATE = """
<container>
    <header />
    <sub_a />
    <editor />
</container>"""


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST' and request.form.get('template'):
        template = request.form.get('template')
    else:
        template = TEMPLATE

    return render_pml_template(template, 'xml', {
        'page': template
    }, container_node)


if __name__ == '__main__':
    app.run()
