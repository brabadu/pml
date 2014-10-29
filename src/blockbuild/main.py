# all the imports
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

# app.config.from_envvar('BLOCKBUILD_SETTINGS', silent=True)

# def connect_db():
#     return sqlite3.connect(app.config['DATABASE'])

from blocks import container_node
from pml.render import render_pml_template

TEMPLATE = """<container>
    <header />
    <sub_a />
    <editor />
</container>""".strip()


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
