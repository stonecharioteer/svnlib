from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="svnlib",
    version="0.1.1a",
    author="Vinay Keerthi",
    author_email="ktvkvinaykeerthi@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    url="https://vinay87.github.io/svnlib",
    license="MIT",
    tests_require=["pytest"],
    
    project_urls={
        "Documentation": "https://vinay87.github.io/svnlib", # Replace with readthedocs.
        "Source Code": "https://github.com/vinay87/svnlib",
        "Bug Tracker": "https://github.com/vinay87/svnlib/issues"
        },

    classifiers=(
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Topic :: Software Development :: Version Control",
        "Intended Audience :: Developers"
    )
)
