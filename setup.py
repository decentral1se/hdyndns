from setuptools import find_packages, setup

with open('README.md', 'r') as handle:
    long_description = handle.read()

setup(
    name='hdyndns',
    version='0.0.5',
    url='',
    license='GPLv3',
    author='Luke M.',
    author_email='lukewm@riseup.net',
    description=(
        'A GNU/Linux Python 3.5+ Dynamic DNS client '
        'for your homebrew server.'
    ),
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[],
    entry_points={
        'console_scripts': [
            'hdyndns = hdyndns.cli:cli_entrypoint',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Environment :: Console',
        'Intended Audience :: Developers',
    ]
)
