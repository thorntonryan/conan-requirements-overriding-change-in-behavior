import os


def run(cmd):
    ret = os.system(cmd)
    if ret != 0:
        raise Exception(cmd)

run("conan create zlib_clone.py 1.2.8@user/testing")
run("conan create zlib_clone.py 1.2.11@user/testing")
run("conan create boost_clone.py 1.67.0@user/testing")
run("conan create boost_clone.py 1.70.0@user/testing")
run("conan create shared_lib.py user/testing")
run("conan info myapp.py")
