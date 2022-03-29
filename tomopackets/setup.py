import os
import re
import sys
import platform
import subprocess
from pathlib import Path
import numpy

from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext
from distutils.version import LooseVersion


__version__ = '1.1.0'

class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def run(self):
        try:
            out = subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError("CMake must be installed to build the following extensions: " +
                               ", ".join(e.name for e in self.extensions))

        if platform.system() == "Windows":
            cmake_version = LooseVersion(re.search(r'version\s*([\d.]+)', out.decode()).group(1))
            if cmake_version < '3.1.0':
                raise RuntimeError("CMake >= 3.1.0 is required on Windows")

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        cmake_path=str(Path(sys.exec_prefix) / Path('share/cmake/pybind11'))
        numpy_path=numpy.get_include()
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        print('pha names: ',ext.name,extdir)
        cmake_args = ['-DNUMPY_INCLUDE=' + numpy_path,
              '-DCONDA_CMAKE=' + cmake_path,
              '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + extdir,
              '-DCMAKE_MODULE_NAME=' + ext.name,
              '-DPYTHON_EXECUTABLE=' + sys.executable]
        print(f"calling cmake with {' '.join(cmake_args)}")
        cfg = 'Debug' if self.debug else 'Release'
        build_args = ['--config', cfg]

        if platform.system() == "Windows":
            cmake_args += ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}'.format(cfg.upper(), extdir)]
            if sys.maxsize > 2**32:
                cmake_args += ['-A', 'x64']
            build_args += ['--', '/m']
        else:
            cmake_args += ['-DCMAKE_BUILD_TYPE=' + cfg]
            build_args += ['--', '-j2']

        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        subprocess.check_call(['cmake', ext.sourcedir] + cmake_args, cwd=self.build_temp)
        subprocess.check_call(['cmake', '--build', '.'] + build_args, cwd=self.build_temp)


setup(
    name='tomopackets',
    version=__version__,
    author='Jan-Willem Buurlage',
    author_email='janwillembuurlage@gmail.com',
    url='https://github.com/cicwi/RECAST3D',
    description='ZeroMQ based streaming for RT tomography',
    long_description='',
    ext_modules=[CMakeExtension('py_tomop')],
    cmdclass=dict(build_ext=CMakeBuild),
    packages=find_packages(include=['tomop']),
    zip_safe=False,
)
