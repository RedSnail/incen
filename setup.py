import InnerCensor
from setuptools import setup, find_packages


def parse_requirements(requirements):
    with open(requirements, "r") as req_file:
        return [line.strip('\n') for line in req_file if line.strip('\n')
                and not line.startswith('#')]


requires = parse_requirements("requirements.txt")
scripts = ["InnerCensor/bin/run_censor.py"]

with open('README.md') as f:
    long_description = f.read()

setup(
    name="incen",
    packages=find_packages(),
    version=InnerCensor.__version__,
    description="A Telegram client for convenient compromising cleansing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Oleg Demianchenko",
    author_email="oleg.demianchenko@gmail.com",
    license="MIT",
    platforms="OS Independent",
    url="https://github.com/RedSnail/incen",
    scripts=scripts,
    entry_points={
          'console_scripts': ['incen=InnerCensor.bin.run_censor:main']
      },
    python_requires='>=3.4',
    include_package_data=True,
    install_requires=requires
)

