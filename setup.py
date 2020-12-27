"""
jlab_enhanced_launcher setup
"""
import json
import os

import setuptools
from jupyter_packaging import (
    create_cmdclass, install_npm, ensure_targets,
    combine_commands, skip_if_exists
)
from packaging.version import parse

HERE = os.path.abspath(os.path.dirname(__file__))

# The name of the project
name="jlab_enhanced_launcher"

# Get our version
with open(os.path.join(HERE, 'package.json')) as f:
    version = str(parse(json.load(f)['version']))

lab_path = os.path.join(HERE, name, "labextension")

# Representative files that should exist after a successful build
jstargets = [
    os.path.join(lab_path, "package.json"),
]

package_data_spec = {
    name.replace("_", "-"): [
        "*"
    ]
}

labext_name = "@jlab-enhanced/launcher"

data_files_spec = [
    ("share/jupyter/labextensions/%s" % labext_name, lab_path, "**"),
    ("share/jupyter/labextensions/%s" % labext_name, HERE, "install.json"),
]

cmdclass = create_cmdclass("jsdeps",
    package_data_spec=package_data_spec,
    data_files_spec=data_files_spec
)

js_command = combine_commands(
    install_npm(HERE, build_cmd="build:prod", npm=["jlpm"]),
    ensure_targets(jstargets),
)

is_repo = os.path.exists(os.path.join(HERE, ".git"))
if is_repo:
    cmdclass["jsdeps"] = js_command
else:
    cmdclass["jsdeps"] = skip_if_exists(jstargets, js_command)

with open("README.md", "r") as fh:
    long_description = fh.read()

setup_args = dict(
    name=name.replace("_", "-"),
    version=version,
    url="https://github.com/fcollonval/jlab-enhanced-launcher.git",
    author="Frederic COLLONVAL",
    description="A enhanced launcher for JupyterLab",
    long_description= long_description,
    long_description_content_type="text/markdown",
    cmdclass= cmdclass,
    packages=setuptools.find_packages(),
    install_requires=[
        "jupyterlab>=3.0.0rc13,==3.*",
        "packaging"
    ],
    zip_safe=False,
    include_package_data=True,
    python_requires=">=3.6",
    license="BSD-3-Clause",
    platforms="Linux, Mac OS X, Windows",
    keywords=["Jupyter", "JupyterLab", "JupyterLab3"],
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Framework :: Jupyter",
    ],
)


if __name__ == "__main__":
    setuptools.setup(**setup_args)
