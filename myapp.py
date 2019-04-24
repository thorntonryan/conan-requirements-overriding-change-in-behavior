from conans import ConanFile

class MyAppConan(ConanFile):
    name = "MyApp"
    version = "0.1"
    settings = "os", "compiler", "build_type", "arch"

    requires = ("SharedCOMLib/1.0.2@user/testing", "SharedGuiLib/0.1@user/testing")
