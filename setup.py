from setuptools import setup, find_packages

setup(
    name="movie_selector",
    version="1.0.0",
    packages=find_packages(),
    install_requires=["colorama"],
    entry_points={
        'console_scripts': [
            'movie-selector=movie_selector.main:main',
        ],
    },
    author="Patrick McGuire",
    author_email="mcguirepr89@gmail.com",
    description="A CLI tool for random movie selection",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
