# -*- coding: utf-8 -*-
from fabric.api import *
import os

project_dir = os.path.dirname(os.path.abspath(__file__))

@task
def setup():
    """Initialize project, load necessary dependencies."""
    with lcd(project_dir):
        local('rm -rf venv')
        local('virtualenv --python=python2.7 --distribute --prompt "ubershopper ~ " venv')
        with prefix('source venv/bin/activate'):
            local('pip install -r ./requirements.txt')
