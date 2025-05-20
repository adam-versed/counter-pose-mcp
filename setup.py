from setuptools import setup, find_packages

setup(
    name="counter-pose-mcp",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "pydantic>=1.8.2",
        "jsonrpcserver>=5.0.0",
        "websockets>=10.0",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "counter-pose-server=mcp_server.main:main",
        ],
    },
)
