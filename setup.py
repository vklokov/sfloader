from setuptools import setup

setup(
    name="sfloader",
    url="https://github.com/vklokov/sfloader",
    author="Vladimir Klokov",
    author_email="klokov.dev@gmail.com",
    packages=['sfloader'],
    install_requires=["requests-2.28.1"],
    version="0.1",
    license="MIT",
    description="Salesforce bulk loader",
)