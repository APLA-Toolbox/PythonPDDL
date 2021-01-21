import setuptools

with open("requirements.txt") as f:
    required = f.read().splitlines()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="jupyddl",  # Replace with your own username
    version="0.4.1",
    author="Erwin Lejeune",
    author_email="erwinlejeune.pro@gmail.com",
    description="Jupyddl is a PDDL planner built on top of a Julia parser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/apla-toolbox/pythonpddl",
    packages=setuptools.find_packages(),
    install_requires=required,
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "Framework :: Pytest",
    ],
    python_requires=">=3.6",
)
