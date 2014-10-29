# PML #

This is a demo for PML.

1. clone a repo
1. `pip install -r requirements.txt`
1. `python blockbuild/main.py`

## Structure ##
* blockbuild/main.py is the entry point and has example for launching PML rendering with `render_pml_template`
* blockbuild/blocks.py has blocks and nodes definition
* blockbuild/templates/all.html has templates for blocks

* blockbuild/pml/blocks.py - `@pml_block` definition, with quick&sloppy hack to make it work with Jinja2
* blockbuild/pml/blocks.py - definition for `render_pml_template`