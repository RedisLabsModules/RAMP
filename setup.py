#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name="ramp-packer",
    description="Packs for Redis modules into a distributable format",
    long_description=open("README.md").read().strip(),
    long_description_content_type="text/markdown",
    keywords=["Redis", "key-value store", "database"],
    license="BSD-2-Clause",
    version="2.4.0-dev1+redispy35",
    packages=find_packages(
        include=[
            "RAMP"
        ]
    ),
    url="https://github.com/RedisLabsModules/RLTest",
    project_urls={
        "Documentation": "https://github.com/RedisLabsModules/RLTest",
        "Changes": "https://github.com/RedisLabsModules/RLTest/releases",
        "Code": "https://github.com/RedisLabsModules/RLTest",
        "Issue tracker": "https://github.com/RedisLabsModules/RLTest/issues",
    },
    author="Redis Inc.",
    author_email="oss@redis.com",
    python_requires=">=3.6",
    install_requires=[
        "distro ~= 1.5.0",
        "redis ~= 3.5.3",
        "PyYAML ~= 5.3.1",
        "click ~= 8.0.0",
        "semantic-version ~= 2.8.5",
        "typing ~= 3.5.0"
    ],
    classifiers=[
        'Topic :: Database',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: BSD License',
        'Development Status :: 5 - Production/Stable'
    ],
    extras_require={
    },
    entry_points='''
        [console_scripts]
        ramp=RAMP.ramp:ramp
    ''',
)
