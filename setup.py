from setuptools import setup, find_packages

setup(
	name='annotate-variants',
	version='0.0.1',
    author="Vinay Pinnaka",
    author_email="",
    description="A tool to annotate variants",
    package_dir={'':"src"},
    packages=find_packages("src"),
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'annotate-variants=annotatevariants.annotate_variants:main',
        ]
    },
)
