from setuptools import setup, find_packages

setup(
    name='finops',
    version='0.1.1',
    description='Financial tools for the rest of us.',
    author='Alireza Nilgaran',
    author_email='alireza.nilgaran@gmail.com',
    url='https://github.com/nixuri/FinOps',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'pandas',
    ],
)