import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tsanomaly",
    version="0.0.1",
    author="Willie Wheeler",
    license="MIT",
    description="Time series anomaly detection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls = {
        "GitHub" : "https://github.com/williewheeler/tsanomaly"
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    package_dir={ "" : "src" },
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3",
    install_requires=[
        "matplotlib",
        "numpy",
        "pandas",
    ],
)
