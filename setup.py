from os import listdir

import setuptools


def read_text(file_name: str) -> str:
    with open(file_name, "r") as f:
        return f.read()


setuptools.setup(
    name="micropython_typesheds",
    version="7.3.18",
    url="https://github.com/hlovatt/PyBoardTypeshed",
    license="MIT License",  # Can only have one line `license`; setuptools bug.
    author="Howard C Lovatt",
    author_email="howard.lovatt@gmail.com",
    description="Typesheds (a.k.a.: interface stubs, `pyi` files, and type hints) for MicroPython.",
    long_description=read_text("README.md"),
    long_description_content_type="text/markdown",
    py_modules=["micropython-typesheds"],
    platforms=["any"],
    python_requires=">=3.8",
    classifiers=[  # These must have a space either side of `::`, despite PyPI website giving them without!
        "Intended Audience :: Developers",
        "Programming Language :: Python :: Implementation :: MicroPython",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
