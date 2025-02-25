from setuptools import setup, find_packages

# handle that unicode error EXPEDITIOUSLY
try:
    with open("README.md", encoding="utf-8") as f:
        long_description = f.read()
except Exception:
    long_description = "quantum spectral weaving fr fr this readme be BUGGED"

setup(
    name="quantum_spectral_weaving",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "torch>=1.9.0",
        "numpy>=1.19.2",
        "scipy>=1.7.0",
        # that complextensor shit prolly doesn't exist lmao
        # we'll mock it later
    ],
    author="prometheusWaluigi",
    author_email="quantum@weaving.fr.fr",
    description="fr fr this package implements quantum spectral weaving for the riemann hypothesis NO CAP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/prometheusWaluigi/ideaFilaments",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Physics",
    ],
)
