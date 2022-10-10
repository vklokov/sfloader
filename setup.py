from setuptools import setup

setup(
    name="sfloader",
    url="https://github.com/vklokov/sfloader",
    author="Vladimir Klokov",
    author_email="klokov.dev@gmail.com",
    packages=["sfloader"],
    install_requires=['requests >= 2.20; python_version >= "3.6"'],
    python_requires=">=3.6",
    version="0.1",
    license="MIT",
    description="Salesforce bulk loader",
)
