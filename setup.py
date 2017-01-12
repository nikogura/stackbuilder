from setuptools import setup, find_packages

setup(
    name="Stackbuilder",
    version="0.1.0",
    packages=find_packages(),
    package_data={},
    author="Nik Ogura",
    author_email="nik.ogura@gmail.com",
    description="Build framework for creating technology stacks from multiple independant components on Linux",
    license="Apache 2.0",
    keywords="build make stack",
    url="https://github.com/nikogura/stackbuilder",

    install_requires=[
        'python-gnupg',
        'PyYAML',
        'requests',

    ]

)