from setuptools import setup, find_packages

setup(
    name="quantum_spectral_weaving",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "torch>=1.9.0",
        "numpy>=1.19.2",
        "scipy>=1.7.0",
        "git+https://github.com/NeoVertex1/ComplexTensor.git",
    ],
    author="prometheusWaluigi",
    author_email="quantum@weaving.fr.fr",
    description="fr fr this package implements quantum spectral weaving for the riemann hypothesis NO CAP",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/prometheusWaluigi/ideaFilaments",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Physics",
    ],
)