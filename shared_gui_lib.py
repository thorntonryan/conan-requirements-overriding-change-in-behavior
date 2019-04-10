from conans import ConanFile

class SharedGuiLibConan(ConanFile):
    name = "SharedGuiLib"
    version = "0.1"
    license = "<Put the package license here>"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of SharedGuiLib here>"
    topics = ("<Put some tag here>", "<here>", "<and here>")
    settings = "os", "compiler", "build_type", "arch"

    requires = (
        "SharedCOMLib/1.0.1@user/testing"
    )
