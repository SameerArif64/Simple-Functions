from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements, dependency_links = [], []
    for line in f:
        (dependency_links if line.startswith("git+") else requirements).append(line.strip())

setup(
    name="simple_func",
    version="1.0.0",
    packages=find_packages(),
    install_requires=requirements,
    dependency_links=dependency_links,
    author="Sameer Arif",
    author_email="supersameer64@gmail.com",
    description="A Python utility library for tasks like mouse event handling, dynamic module importing, file operations, and string manipulation.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/SameerArif64/Simple-Functions",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    license="MIT",
)
