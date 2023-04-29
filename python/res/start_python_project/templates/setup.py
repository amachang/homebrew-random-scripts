from setuptools import setup, find_packages

setup(
    name="{{ project_name }}",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="Hitoshi Amano",
    author_email="seijro@gmail.com",
    description="TODO",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/amachang/{{ project_name }}",
    classifiers=[],
)
