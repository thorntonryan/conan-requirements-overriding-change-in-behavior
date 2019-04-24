from conans import ConanFile

class MyAppConan(ConanFile):
    name = "MyApp"
    version = "0.1"
    settings = "os", "compiler", "build_type", "arch"

    requires = (
            "MyBoostClone/1.70.0@user/testing",
            "MyZlibClone/1.2.11@user/testing",
            "SharedStaticLib/0.1@user/testing",
    )
