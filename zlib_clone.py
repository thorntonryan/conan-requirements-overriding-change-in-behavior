from conans import ConanFile

class MyZlibClone(ConanFile):
    name = "MyZlibClone"
    description = "Static library with strong semver ABI guarantees, like zlib"
    settings = "os", "compiler", "build_type", "arch"
