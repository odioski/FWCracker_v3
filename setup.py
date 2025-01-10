from setuptools import setup, find_packages

setup(
    name="FWCracker",
    version="3.0.0",
    packages=find_packages(),
    install_requires=[
        "pyserial",
        "PyQt6",
    ],
    entry_points={
        "console_scripts": [
            "FWCracker=FWCracker:main",
        ],
    },
    package_data={
        "": ["*.png", "*.qss"],
    },
    include_package_data=True,
    author="Omar Daniels",
    author_email="link92@bookmotives.com",
    description="A firmware cracking tool with a GUI.",
    url="https://github.com/odioski",
)
