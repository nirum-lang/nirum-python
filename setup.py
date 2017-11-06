import ast
import re
import sys

from setuptools import find_packages, setup, __version__ as setuptools_version


def readme(name='README.rst'):
    try:
        with open(name) as f:
            rst = f.read()
        return re.sub(
            r'(^|\n).. include::\s*([^\n]+)($|\n)',
            lambda m: m.group(1) + (readme(m.group(2)) or '') + m.group(3),
            rst
        )
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


setup_requires = []
service_requires = [
    # FIXME Test Werkzeug 0.9, 0.10, 0.11 as well
    'Werkzeug >= 0.11, < 1.0',
]
install_requires = [
    'six', 'iso8601',
] + service_requires
tests_require = [
    'pytest >= 3.1.2, < 4.0.0',
    'pytest-flake8 >= 0.9.1, < 1.0.0',
    'flake8-import-order >= 0.12, < 1.0',
    'flake8-import-order-spoqa >= 1.0.1, < 2.0.0',
]
docs_require = [
    'Sphinx',
]
extras_require = {
    'service': service_requires,
    'tests': tests_require,
    'docs': docs_require,
}
below35_requires = [
    'typing',
]
below34_requires = [
    'enum34',
]


if 'bdist_wheel' not in sys.argv and sys.version_info < (3, 5):
    install_requires.extend(below35_requires)


if tuple(map(int, setuptools_version.split('.'))) < (17, 1):
    setup_requires = ['setuptools >= 17.1']
    extras_require.update({":python_version=='3.4'": below35_requires})
    extras_require.update({":python_version=='2.7'": below35_requires})
    extras_require.update({":python_version=='2.7'": below34_requires})
else:
    extras_require.update({":python_version<'3.5'": below35_requires})
    extras_require.update({":python_version<'3.4'": below34_requires})


setup(
    name='nirum',
    version=get_version(),
    description='The Nirum runtime library for Python',
    long_description=readme(),
    url='https://github.com/spoqa/nirum-python',
    bugtrack_url='https://github.com/spoqa/nirum/issues',
    author='Kang Hyojun',
    author_email='iam.kanghyojun' '@' 'gmail.com',
    license='MIT license',
    packages=find_packages(exclude=['tests']),
    install_requires=install_requires,
    setup_requires=setup_requires,
    extras_require=extras_require,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Object Brokering',
    ]
)
