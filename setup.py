from distutils.core import setup

setup(
    name='downloader',
    version='0.1.0',
    author='Sgiath',
    author_email='Sgiath@outlook.com',
    url='https://github.com/Sgiath/downloader',
    description='',
    long_description='',
    download_url='',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Home Automation',
        'Topic :: Utilities'
    ],
    platforms=[],
    license='',
    packages=['downloader'],
    package_dir={'downloader': 'downloader'},
    scripts=[],
    install_requires=['Click==6.3'],
    entry_points={
        'console_scripts': [
            'download = downloader.__main__:main'
        ]
    }
)
