from setuptools import setup

setup(
    name='tron_explorer',
    version='1.0.0',
    packages=['tron_explorer', 'tron_explorer.test'],
    url='',
    python_requires='>3.8',
    license='MIT',
    author='Amirali Omidvar',
    author_email='amirali.omidvar80@gmail.com',
    description='A Python Wrapper for tronscan.org REST API',
    include_package_data=False
)
