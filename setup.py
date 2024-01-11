from setuptools import setup
from setuptools.command.build_py import build_py
import lzma
import os


class compress_data(build_py):

    _data = [('conway_polynomials', 'CPimport.txt')]

    def compress(self):
        """ Compress data files into build directory"""
        for pkg, filename in self._data:
            src = os.path.join(self.build_lib, pkg, filename)
            dst = os.path.join(self.build_lib, pkg, filename + '.xz')
            print(f"compressing {src} -> {dst}")
            with open(src, "rb") as s:
                with lzma.open(dst, "w") as d:
                    d.write(s.read())
            os.remove(src)

    def run(self):
        build_py.run(self)
        self.compress()


cmdclass = {'build_py': compress_data}

setup(cmdclass=cmdclass)
