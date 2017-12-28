from conans import ConanFile, CMake, tools
import os

class SwigConan(ConanFile):
    name = "swig"
    version = "3.0.12"
    license = "https://github.com/swig/swig/raw/master/LICENSE"
    url = "https://github.com/ulricheck/conan-swig"
    description = "SWIG is a software development tool that connects programs written in C and C++ with a variety of high-level programming languages. http://www.swig.org"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        if self.settings.os == "Windows":
            # swig will only be built if not on windows
            pass
        else:
            source_file = "swig-rel-%s" % self.version
            tools.get("https://github.com/swig/swig/archive/rel-%s.zip" % self.version)
            os.rename(source_file, "source")


    def build(self):
        if self.settings.os == "Windows":
            source_file = "swigwin-%s" % self.version
            tools.get("https://downloads.sourceforge.net/project/swig/swigwin/%s/%s.zip" % (source_file, source_file))
            os.rename(source_file, "source")
        else:
            from conans import AutoToolsBuildEnvironment
            env_build = AutoToolsBuildEnvironment(self)
            
            with tools.environment_append(env_build.vars):
                self.run("cd source && sh autogen.sh")
                self.run("cd source && ./configure --prefix=%s/install" % self.install_folder)
                self.run("cd source && make && make install")


    def package(self):
        self.copy("*", dst="bin", src="install/bin")
        self.copy("*", dst="share", src="install/share")

    def package_info(self):
        swig_home = os.path.join(self.package_folder)
        self.output.info("Creating SWIG_HOME environment variable with : {0}".format(swig_home))
        self.env_info.SWIG_HOME = swig_home

        bin_path = os.path.join(swig_home, "bin")
        self.output.info("Appending PATH environment variable with : {0}".format(bin_path))
        self.env_info.path.append(bin_path)
