
import setuptools
import os
import re

with open("README.md", "r") as fh:
    long_description = fh.read()

with open(os.path.join(os.path.dirname(__file__), 'awattar', '__init__.py')) as f:
    version = re.search("__version__ = '([^']+)'", f.read()).group(1)

setuptools.setup(
    name="awattar",
    version=version,
    author="Peter Gransdorfer",    
    description="aWATTar Client to analyse the energy market data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Gransi/awattar",
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',        
    ],
    install_requires=['requests', 'datetime', 'python-dateutil'],
    python_requires='>=3.6'
)