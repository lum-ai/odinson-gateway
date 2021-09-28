import os
import subprocess
from setuptools import setup

VERSION = "0.1.0"
JAR_FILE_PATH = os.path.join(
    "odinson-entrypoint", "target", "scala-2.12", "odinson-entrypoint.jar"
)

os.chdir("odinson-entrypoint")
subprocess.call("sbt assembly", shell=True)
os.chdir("..")

setup(
    name="odinson",
    packages=["odinson"],
    data_files=[("share/odinson", [JAR_FILE_PATH])],
    version=VERSION,
    install_requires=["py4j==0.10.9.2"],
)
