import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pythonpddl-guilyx",  # Replace with your own username
    version="0.2.0",
    author="Erwin Lejeune",
    author_email="erwinlejeune.pro@gmail.com",
    description="PythonPDDL is a PDDL planner built on top of a Julia parser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/apla-toolbox/pythonpddl",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: Ubuntu, MacOS",
    ],
    python_requires=">=3.6",
)
