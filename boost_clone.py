from conans import ConanFile

class MyBoostClone(ConanFile):
    name = "MyBoostClone"
    description = "Header only library, like Boost"
    settings = "os", "compiler", "build_type", "arch"
    options = {"header_only": [True,False]}
    default_options = "header_only=True"
