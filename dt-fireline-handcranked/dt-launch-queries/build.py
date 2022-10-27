#   -*- coding: utf-8 -*-
from pybuilder.core import use_plugin, init

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.flake8")
use_plugin("python.coverage")
use_plugin("python.distutils")

name = "dt-revenue-persubs"
default_task = "publish"
description = "revenue-persubs is a data pipeline"


@init
def set_properties(project):
    project.set_property("coverage_break_build", False)
    project.set_property("dir_source_main_python", "src/main/python")
    project.set_property("dir_source_unittest_python", "src/test/python")
    project.depends_on_requirements("requirements.txt")
    project.set_property("distutils_entry_points", {'console_scripts': ['run=scripts.runner:run']})
