import setuptools

with open("README.md", "r", encoding="UTF-8") as fh:
    long_description = fh.read()

requirements = [
    'pandas'
]
    
setuptools.setup(
    name="GERpronouncing",
    version="0.0.1",
    author="Joe Breuer",
    author_email="joe.breuer@gmx.de",
    description="A pronounciation lexicon for German with some useful functions to handle it",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JBreuerPY/GERpronouncing",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: German",
        "Topic :: Artistic Software",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
    ],
    include_package_data=True,
    package_data={'': ['data/*.zip']},
    python_requires='>=3.6',
)