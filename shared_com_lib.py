from conans import ConanFile


class SharedCOMLibConan(ConanFile):
    name = "SharedCOMLib"
    settings = "os", "compiler", "build_type", "arch"
