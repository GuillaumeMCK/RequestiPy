from glob import glob

from setuptools import setup, Extension

module = Extension(
    'http_client',
    sources=glob('sources/*.c'),
    include_dirs=['includes'],
    libraries=['curl'],
)

setup(
    name='http_client',
    version='1.0',
    description='A simple HTTP client in Python using libcurl',
    ext_modules=[module],
)
