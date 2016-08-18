import ast
import sys

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


service_requires = [
    # FIXME Test Werkzeug 0.9, 0.10, 0.11 as well
    'Werkzeug >= 0.11, < 0.12',
]
install_requires = [
    'setuptools',
    'iso8601',
] + service_requires
tests_require = [
    'pytest >= 2.9.0',
    'import-order',
    'flake8',
]
docs_require = [
    'Sphinx',
]
below35_requires = [
    'typing',
]
if 'bdist_wheel' not in sys.argv and sys.version_info < (3, 5):
    install_requires.extend(below35_requires)


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
        ":python_version<'3.5'": below35_requires,
        'service': service_requires,
        'tests': tests_require,
        'docs': docs_require,
    },
    classifiers=[]
)
