from setuptools import find_packages, setup

install_requires = [
    'requests==2.25.1'
]

version = "1.0.0"

setup(
    name='gocd-api-python-client',
    packages=find_packages(),
    version=version,
    description='Python API Client for GoCD Server',
    author='Borja Refoyo Ruiz',
    url='https://github.com/Squallium/python-util-microservice',
    install_requires=install_requires,
)
