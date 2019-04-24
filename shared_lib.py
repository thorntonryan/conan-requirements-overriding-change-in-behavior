from conans import ConanFile

class SharedStaticLibConan(ConanFile):
    name = "SharedStaticLib"
    version = "0.1"
    description = "Shared library that does not expose its private dependencies through its public API."
    settings = "os", "compiler", "build_type", "arch"
    default_options = "boost:header_only=True", "zlib:shared=False"

    requires = (
        # Not exposed through public headers of this library
        ("MyZlibClone/1.2.8@user/testing","private"),
        ("MyBoostClone/1.67.0@user/testing", "private"),
    )

    def package_id(self):
        # Header only library, defined in object files of this shared library
        # Must use full_version_mode in order to avoid violating One Definition Rule
        # if consumers happen to use a different version of boost
        self.info.requires["MyBoostClone"].full_version_mode()

        # static library that makes strong semver compatibility guarentees in its ABI
        # Semver compatible with 1.x
        # Semver incompatible with 2.x
        self.info.requires["MyZlibClone"].semver_mode()
