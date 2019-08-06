from conans import ConanFile, CMake, tools
import os


class SimpleWebSocketServerConan(ConanFile):
    name = "Simple-WebSocket-Server"
    version = "a4d0d064-git"
    source_sha256 = ""
    description = "A very simple, fast, multithreaded, platform independent WebSocket (WS) and WebSocket Secure (WSS) server and client library."
    # topics can get used for searches, GitHub topics, Bintray tags etc. Add here keywords about the library
    topics = ("conan", "Simple-WebSocket-Server", "socket")
    url = "https://github.com/bincrafters/conan-Simple-WebSocket-Server"
    homepage = "https://gitlab.com/eidheim/Simple-WebSocket-Server"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "MIT"  # Indicates license type of the packaged library; please use SPDX Identifiers https://spdx.org/licenses/
    no_copy_source = True

    requires = (
        "OpenSSL/1.1.1c@conan/stable",
    )
    options = {
        "use_asio_standalone": [True, False],
    }
    default_options = {
        "use_asio_standalone": True,
    }
    # Packages the license for the conanfile.py
    exports = ["LICENSE.md"]

    # Custom attributes for Bincrafters recipe conventions
    _source_subfolder = "source_subfolder"

    def requirements(self):
        if self.options.use_asio_standalone:
            self.default_options["asio:standalone"] = True
            self.requires("asio/1.13.0@bincrafters/stable")
        else:
            self.requires("boost_asio/1.69.0@bincrafters/stable")

    def source(self):
        if self.version.endswith("-git"):
            git = tools.Git(folder=self._source_subfolder)
            git.clone("https://gitlab.com/eidheim/Simple-WebSocket-Server.git", "master")
            git.checkout(self.version.split('-')[0])
        else:
            tools.get(f"https://gitlab.com/eidheim/Simple-WebSocket-Server/-/archive/v{self.version}/Simple-WebSocket-Server-v{self.version}.tar.gz",
                      sha256=self.source_sha256)
            extracted_dir = self.name + "-v" + self.version

            # Rename to "source_subfolder" is a convention to simplify later steps
            os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["USE_STANDALONE_ASIO"] = True
        cmake.configure(source_folder=self._source_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()
        # If the CMakeLists.txt has a proper install method, the steps below may be redundant
        # If so, you can just remove the lines below
        self.copy(pattern="*.hpp", dst="include", src=self._source_subfolder)

    def package_id(self):
        self.info.header_only()
