import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="file-utility-al",
    version="0.0.2",
    author="Ujjwal Singh",
    author_email="ujjwalks01@gmail.com",
    description="This project contains utility file to load data to train models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ujjwalks/file_utility_al",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)