# -*- coding: utf-8 -*-
'''
Project:       ~/projects/Pythons/cpp_punctuator/build_distributable
File Name:     setup.py
Author:        Chaos
Email:         life0531@foxmail.com
Date:          2022/08/15
Software:      Vscode
'''

'''
Make Punctuator-Module distributable using Python's setup tool
'''
from distutils.command.build_ext import build_ext
import glob
import os
import platform
import shutil
import sys
import setuptools

def cmake_extension(name, *args, **kwargs) -> setuptools.Extension:
    kwargs["language"] = "c++"
    sources = []
    return setuptools.Extension(name, sources, *args, **kwargs)

class BuildExtension(build_ext):
    def build_extension(self, ext: setuptools.extension.Extension):
        src_dir = os.path.dirname(os.path.abspath(__file__))
        os.makedirs(os.path.join(src_dir, self.build_temp), exist_ok=True)
        os.makedirs(os.path.join(src_dir, self.build_lib), exist_ok=True)

        cmake_args = os.environ.get("PUNCTUATOR_MAKE_ARGS", "-DCMAKE_BUILD_TYPE=Release")
        if "PYTHON_EXECUTABLE" not in cmake_args:
            print(f"Setting PYTHON_EXECUTABLE to {sys.executable}")
            cmake_args += f" -DPYTHON_EXECUTABLE={sys.executable}"

        os.system(f"cmake {cmake_args} -S {src_dir} -B {os.path.join(src_dir, self.build_temp)}")

        build_res = os.system(f"cmake --build {os.path.join(src_dir, self.build_temp)}")
        if build_res != 0:
            raise Exception(
                "\nBuild failed. Please check the error message.\n"
            )

        libs = []
        torch_lib = f"{self.build_temp}/_deps/libtorch-src/lib"
        for ext in ["so", "pyd", 'dylib', 'dll']:
            libs.extend(glob.glob(f"{self.build_temp}/**/punctuator*.{ext}", recursive=True))
            libs.extend(glob.glob(f"{torch_lib}/*c10.{ext}"))
            libs.extend(glob.glob(f"{torch_lib}/*torch_cpu.{ext}"))
            libs.extend(glob.glob(f"{torch_lib}/*torch.{ext}"))
            libs.extend(glob.glob(f"{torch_lib}/*gomp*.{ext}"))

        if platform.system() == "Windows":
            libs.extend(glob.glob(f"{self.build_temp}/**/*.dll", recursive=True))

        for lib in libs:
            print(f"Copying {lib} to {self.build_lib}/")
            shutil.copy(f"{lib}", f"{self.build_lib}/")



package_name = "punctuator"

setuptools.setup(
    name=package_name,
    version="0.1.1",  # 0.1.0 is the pure lib file
    author="Chaos",
    package_dir={
        package_name: "src",
    },
    packages=[package_name],
    ext_modules=[cmake_extension("punctuator")],
    cmdclass={"build_ext": BuildExtension},
    zip_safe=False,
    setup_requires=["tqdm"],
    install_requires=["tqdm"],
    classifiers=[
        "Programming Language :: C++",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.6",
)
