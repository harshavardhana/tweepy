from setuptools import setup

version = '2.0.0'

setup(
    name='tweepy',
    version=version,
    description='Twitter python API - Fully supported user \'streaming\' and site \'streaming\'',
    author='Harshavardhana',
    author_email='harsha@harshavardhana.net',
    url='https://github.com/harshavardhana/tweepy.git',
    license='MIT',
    platforms=['any'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=['tweepy'],
)
