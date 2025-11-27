from setuptools import setup, find_packages

setup(
    name="health_track",
    version="1.0.0",
    packages=find_packages(exclude=["tests", "scripts"]),
    install_requires=[
        "python-dotenv",  # se ainda estiver usando
    ],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "healthtrack=app:main",
        ],
    },
)
