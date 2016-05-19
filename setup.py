import ast

from setuptools import find_packages, setup


def readme():
    try:
        with open('README.rst') as f:
            return f.read()
    except (IOError, OSError):
        return


def get_version():
    filename = 'nirum/__init__.py'
    version = None
    with open(filename, 'r') as f:
        tree = ast.parse(f.read(), filename)
        for node in tree.body:
            if (isinstance(node, ast.Assign) and
                    node.targets[0].id == '__version_info__'):
                version = ast.literal_eval(node.value)
        return '.'.join([str(x) for x in version])


install_requires = [
    'setuptools',
]
tests_require = [
    'pytest >= 2.9.0',
    'import-order',
    'flake8',
]
docs_require = [
    'Sphinx',
]


setup(
    name='nirum',
    version=get_version(),
    description='',
    long_description=readme(),
    url='https://github.com/spoqa/nirum-python',
    author='Kang Hyojun',
    author_email='iam.kanghyojun' '@' 'gmail.com',
    license='MIT license',
    packages=find_packages(exclude=['tests']),
    install_requires=install_requires,
    extras_require={
        'tests': tests_require,
        'docs': docs_require,
    },
    classifiers=[]
)
