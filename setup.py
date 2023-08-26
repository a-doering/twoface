from pathlib import Path

from setuptools import find_namespace_packages, setup

BASE_DIR = Path(__file__).parent
with open(Path(BASE_DIR, "requirements.txt")) as file:
    required_packages = [ln.strip() for ln in file.readlines()]

dev_packages = ["black==23.7.0", "flake8==6.1.0", "isort==5.12.0", "pytest==7.4.0"]
setup(
    name="twoface",
    version="0.1.0",
    description="",
    author="a-doering",
    author_email="",
    url="",
    python_requires=">=3.11",
    packages=find_namespace_packages(),
    install_requires=[required_packages],
    extras_require={
        "dev": dev_packages,
    },
)
