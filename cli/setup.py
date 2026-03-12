from setuptools import setup, find_packages

setup(
    name="spearmint-cli",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "typer>=0.9.0",
        "rich>=13.0.0",
        "python-dotenv>=1.0.0",
        "requests>=2.31.0",
    ],
    entry_points={
        "console_scripts": [
            "spearmint=spearmint_cli.main:app",
        ],
    },
)
