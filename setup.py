import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
setup(
   name="gmg",
   version="0.0.3",
   description="Middleware for talking to your Green Mountain Grill",
   long_description=README,
   long_description_content_type="text/markdown",
   author="Christopher McKay",
   author_email="mckaycr@gmail.com",
   license="MIT",
   packages=["gmg"],
   zip_safe=False
)