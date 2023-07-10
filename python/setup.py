from setuptools import setup, find_packages

setup(
    name="random_scripts",
    version="0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "hello_python=random_scripts.hello:main",
            "rename_with_dir=random_scripts.rename_with_dir:main",
            "major_image_res=random_scripts.major_image_res:main",
            "make_app=random_scripts.make_app:main",
        ],
    },
    install_requires=[
        "art~=5.9",
        "jinja2~=3.1.2",
        "keyring~=23.13.1",
        "appdirs~=1.4.4",
        "click~=8.1.3",
        "PyGithub~=1.58.1",
        "virtualenv~=20.23.0",
        "imagesize~=1.4.1",
        "tqdm~=4.65.0",
        "types-tqdm~=4.65.0.1",
    ],
)
