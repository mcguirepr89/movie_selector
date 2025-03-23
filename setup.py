from setuptools import setup, find_packages

setup(
    name="movie_selector",
    version="1.0.3",
    packages=find_packages(),
    install_requires=["colorama"],
    entry_points={
        'console_scripts': [
            'movie-selector=movie_selector.main:main',
        ],
    },
    author="Patrick McGuire",
    description="A CLI tool for random movie selection",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mcguirepr89/movie_selector",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
