# all the imports
import sqlite3
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

from blockbuild.blocks import container_node
from blockbuild.pml.render import render_pml_template

@app.route('/')
def main():
	template = """
	<container>
		<header />
		<sub_a />
	</container>
	"""
	return render_pml_template(template, 'xml', {}, container_node)


if __name__ == '__main__':
    app.run()
