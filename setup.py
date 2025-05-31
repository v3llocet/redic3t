from setuptools import setup, find_packages

setup(
    name="redic3t",
    version="0.1.0",
    description="Passive reconnaissance tool using Wayback Machine archives",
    author="v3llocet",
    author_email="v3ll0cet@proton.me",
    packages=find_packages(),
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "redic3t=redic3t.main:main",
        ],
    },
    include_package_data=True,
)
