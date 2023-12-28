from setuptools import setup

setup(
    # ...
    options={"build_exe": {"include_files": [("images", "images")]}}
)
