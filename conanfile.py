#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import shutil


class ClapackConan(ConanFile):
    name = "clapack"
    version = "3.2.1"
    license = "BSD 3-Clause"
    # BSD-3-Clause-Clear
    url = "https://github.com/sintef-ocean/conan-clapack"
    author = "SINTEF Ocean"
    homepage = "http://www.netlib.org/clapack/"
    description = \
        "CLAPACK's goal is to provide LAPACK for someone who does " \
        "not have access to a Fortran compiler"
    topics = ("clapack", "LAPACK", "Port to C", "Numerical linear algebra")
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "fPIC": [True, False],
    }
    default_options = {
        "fPIC": True,
    }
    generators = ("cmake_paths", "cmake_find_package")
    exports = ["patch/*"]
    source_file = "clapack-{}-CMAKE.tgz".format(version)
    source_subfolder = source_file[:-4]
    build_subfolder = "build_subfolder"

    def source(self):

        link = "http://www.netlib.org/clapack/" + self.source_file
        tools.get(link, sha1="5ea1bcc4314e392bca8b9e5f61d44355cf9f4cc1")

        tools.patch(patch_file="patch/MainCMakeLists.patch",
                    base_path=self.source_subfolder)
        tools.patch(patch_file="patch/SRC_CMakeLists.patch",
                    base_path=self.source_subfolder)
        tools.patch(patch_file="patch/F2C_CMakeLists.patch",
                    base_path=self.source_subfolder)
        tools.patch(patch_file="patch/BLAS_CMakeLists.patch",
                    base_path=self.source_subfolder)
        shutil.move(self.source_subfolder + "/COPYING",
                    self.source_subfolder + "/LICENSE")

    def build(self):
        cmake = CMake(self)
        cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC
        cmake.configure(source_folder=self.source_subfolder,
                        build_folder=self.build_subfolder)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("COPYING", dst="licenses", src=self.source_subfolder,
                  ignore_case=True, keep_path=False)

    def package_info(self):
        self.cpp_info.name = 'CLAPACK'
        if self.settings.compiler == "Visual Studio":
            self.cpp_info.libs = ["libf2c", "blas", "lapack"]
            if self.settings.build_type == "Debug":
                for i in range(len(self.cpp_info.libs)):
                    self.cpp_info.libs[i] += 'd'
        else:
            self.cpp_info.libs = ["lapack", "blas", "f2c"]

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC


    def configure(self):
        del self.settings.compiler.libcxx
