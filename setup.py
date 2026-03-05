"""Setup configuration for CrystalClearHouse."""

from setuptools import setup, find_packages

setup(
    name="crystalclearhouse",
    version="0.1.0",
    description="An intelligent agent orchestration system",
    author="CrystalClearHouse Team",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        # Add dependencies as needed
    ],
    entry_points={
        "console_scripts": [
            "crystalclearhouse-orchestrator=crystalclearhouse.orchestrator.orchestrator:main",
            "crystalclearhouse-planner=crystalclearhouse.agents.planner:main",
        ],
    },
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "supervisor>=4.2.0",
        ],
    },
)
