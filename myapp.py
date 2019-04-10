from conans import ConanFile

class MyAppConan(ConanFile):
    name = "MyApp"
    version = "0.1"
    license = "<Put the package license here>"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of MyApp here>"
    topics = ("<Put some tag here>", "<here>", "<and here>")
    settings = "os", "compiler", "build_type", "arch"

    requires = ("SharedCOMLib/1.0.2@user/testing",)
    build_requires = requires + ("SharedGuiLib/0.1@user/testing",)
