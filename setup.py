from setuptools import setup, find_packages


with open("README.md") as readme:
    long_description = readme.read()


setup(
    name="netschoolapi",
    version="11.0.6",
    description="Асинхронный API-клиент для «Сетевого города»",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="unneyon",
    author_email="me@unneyon.ru",
    url="https://github.com/unneyon/netschoolapi/",
    packages=find_packages(),
    package_data={"netschoolapi": ["py.typed"]},
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Russian",
        "Topic :: Communications :: Chat",
        "Topic :: Education",
    ],
    license="MIT",
    install_requires=open("requirements.txt").read().strip().split("\n"),
    python_requires=">=3.10",
)