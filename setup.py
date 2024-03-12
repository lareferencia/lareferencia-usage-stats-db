import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='LAReferenciaUsageStatsDB',
    author='Lautaro Matas',
    author_email='lmatas@gmail.com',
    description='LA Referencia Usage Stats DB',
    keywords='LA Referencia, Usage Stats, Database',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/lareferencia/lareferencia-usage-stats-db',
    project_urls={
        'Documentation': 'https://github.com/lareferencia/lareferencia-usage-stats-db',
        'Bug Reports':
        'https://github.com/lareferencia/lareferencia-usage-stats-db/issues',
        'Source Code': 'https://github.com/lareferencia/lareferencia-usage-stats-db',
        # 'Funding': '',
        # 'Say Thanks!': '',
    },
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    classifiers=[
        # see https://pypi.org/classifiers/
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    # install_requires=['Pillow'],
    extras_require={
        'dev': ['check-manifest'],
        # 'test': ['coverage'],
    },
    # entry_points={
    #     'console_scripts': [  # This can provide executable scripts
    #         'run=examplepy:main',
    # You can execute `run` in bash to run `main()` in src/examplepy/__init__.py
    #     ],
    # },
)
