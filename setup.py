from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='finops',
    version='0.1.2',
    description='Financial tools for the rest of us.',
    author='Alireza Nilgaran',
    author_email='alireza.nilgaran@gmail.com',
    url='https://github.com/nixuri/FinOps',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='BSD (3-clause)',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'pandas',
        'requests',
        'beautifulsoup4',
        'datetime',
    ],
)