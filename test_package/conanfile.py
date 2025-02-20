from os import path
from conan import ConanFile
from conan.tools.build import can_run
from conan.tools.cmake import cmake_layout, CMake


class ClapackTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps", "CMakeToolchain", "VirtualRunEnv"
    test_type = "explicit"

    def requirements(self):
        self.requires(self.tested_reference_str)

    def layout(self):
        cmake_layout(self)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        if can_run(self):
            bin_path = path.join(self.cpp.build.bindirs[0], "example")
            self.run(bin_path, env="conanrun")
