#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import shutil

class ClapackConan(ConanFile):
    name = "clapack"
    version = "3.2.1"
    license = "Freeware with copyright notice"
    url = "https://github.com/joakimono/conan-clapack"
    homepage = "http://www.netlib.org/clapack/"
    description = "CLAPACK's goal is to provide LAPACK for someone who does not have access to a Fortran compiler"
    settings = "os", "compiler", "build_type", "arch", "os_build", "arch_build"
    generators = "cmake"
    exports = "patch/*"
    source_file = "clapack-3.2.1-CMAKE.tgz"
    source_dir = source_file[:-4]
    
    def source(self):
    
        link = "http://www.netlib.org/clapack/clapack-3.2.1-CMAKE.tgz"
        tools.get(link, sha1="5ea1bcc4314e392bca8b9e5f61d44355cf9f4cc1")
        
        tools.patch(patch_file="patch/MainCMakeLists.patch", base_path=self.source_dir)
        tools.patch(patch_file="patch/SRC_CMakeLists.patch", base_path=self.source_dir)
        tools.patch(patch_file="patch/F2C_CMakeLists.patch", base_path=self.source_dir)
        tools.patch(patch_file="patch/BLAS_CMakeLists.patch", base_path=self.source_dir)
        shutil.move(self.source_dir + "/COPYING", self.source_dir + "/LICENSE")

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder=self.source_dir)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("COPYING", dst="licenses", src=self.source_dir, 
                  ignore_case=True, keep_path=False)

    def package_info(self):
        if self.settings.os == "Windows":
            self.cpp_info.libs = ["libf2c", "blas", "lapack"]
            if(self.settings.build_type) == "Debug":
                for i in range(len(self.cpp_info.libs)):
                    self.cpp_info.libs[i] += 'd'
        else:
            self.cpp_info.libs = ["f2c", "blas", "lapack"]
          
    def configure(self):
        del self.settings.compiler.libcxx