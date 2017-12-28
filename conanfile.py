from conans import ConanFile, tools
import os

class SwigConan(ConanFile):
    name = "swig"
    version = "3.0.12"
    license = "https://github.com/swig/swig/raw/master/LICENSE"
    url = "https://github.com/ulricheck/conan-swig"
    description = "SWIG is a software development tool that connects programs written in C and C++ with a variety of high-level programming languages. http://www.swig.org"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"


    def build(self):
        if self.settings.os == "Windows":
            source_file = "swigwin-%s" % self.version
            tools.get("https://downloads.sourceforge.net/project/swig/swigwin/%s/%s.zip" % (source_file, source_file))
            os.rename(source_file, "source")
        else:
            raise ValueError("Swig Build dependency only support on Windows = please install swig on other systems using your package manager")


    def package(self):
        if self.settings.os == "Windows":
            self.copy("swig.exe", dst=".", src="source")
            self.copy("*", dst="Lib", src="source/Lib")
        else:
            raise ValueError("Swig Build dependency only support on Windows = please install swig on other systems using your package manager")

    def package_info(self):
        swig_home = os.path.join(self.package_folder)
        self.output.info("Creating SWIG_HOME environment variable with : {0}".format(swig_home))
        self.env_info.SWIG_HOME = swig_home
        self.output.info("Appending PATH environment variable with : {0}".format(swig_home))
        self.env_info.path.append(swig_home)
