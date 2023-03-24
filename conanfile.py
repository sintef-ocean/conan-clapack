from os.path import join
from conan import ConanFile
from conan.tools.files import get, copy
from conan.tools.files import apply_conandata_patches, export_conandata_patches
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout

required_conan_version = ">=1.53.0"


class ClapackConan(ConanFile):
    name = "clapack"
    version = "3.2.1"
    license = "BSD 3-Clause"
    url = "https://github.com/sintef-ocean/conan-clapack"
    author = "SINTEF Ocean"
    homepage = "http://www.netlib.org/clapack/"
    description = \
        "CLAPACK's goal is to provide LAPACK for someone who does " \
        "not have access to a Fortran compiler"
    topics = ("LAPACK", "Port to C", "Numerical linear algebra")
    settings = "os", "compiler", "build_type", "arch"
    package_type = "static-library"
    options = {
        "fPIC": [True, False],
    }
    default_options = {
        "fPIC": True,
    }

    def export_sources(self):
        export_conandata_patches(self)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        self.settings.rm_safe("compiler.libcxx")
        self.settings.rm_safe("compiler.cppstd")

    def layout(self):
        cmake_layout(self, src_folder="src")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):
        apply_conandata_patches(self)
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

        copy(self, "COPYING", self.source_folder,
             join(self.package_folder, "licenses"))

    def package_info(self):
        self.cpp_info.set_property("cmake_find_mode", "both")
        self.cpp_info.set_property("cmake_file_name", "CLAPACK")
        self.cpp_info.set_property("cmake_target_name", "CLAPACK::CLAPACK")
        if self.settings.compiler == "msvc":
            self.cpp_info.libs = ["libf2c", "blas", "lapack"]
            if self.settings.build_type == "Debug":
                for i in range(len(self.cpp_info.libs)):
                    self.cpp_info.libs[i] += 'd'
        else:
            self.cpp_info.libs = ["lapack", "blas", "f2c"]
