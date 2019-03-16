from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [
    Extension("mymodule1",  ["mymodule1.py"]),
    Extension("mymodule2",  ["mymodule2.py"]),

#   ... all your modules that need be compiled ...

]

setup(
    name = 'My Program Name',
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules
)
