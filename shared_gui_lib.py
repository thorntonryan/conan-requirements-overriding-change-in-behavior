from conans import ConanFile

class SharedGuiLibConan(ConanFile):
    name = "SharedGuiLib"
    version = "0.1"
    settings = "os", "compiler", "build_type", "arch"

    requires = (
        "SharedCOMLib/1.0.1@user/testing"
    )
