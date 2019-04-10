### Expected Behavior ( I think )

I expect MyApp's _semver compatible_ requirements to override additional requirements coming from its build requirements.

### Current Behavior (1.13+)

1. Run the following:
```sh
# Create SharedCOMLib 1.0.1
$ conan create shared_com_lib.py 1.0.1@user/testing
# Create SharedCOMLib 1.0.2
$ conan create shared_com_lib.py 1.0.2@user/testing
# Create SharedGuiLib 0.1
$ conan create shared_gui_lib.py user/testing
# Resolve requirements for MyApp 0.1
$ conan info myapp.py
```
2. And receive the following error:
```
ERROR: Conflict in SharedGuiLib/0.1@user/testing
    Requirement SharedCOMLib/1.0.1@user/testing conflicts with already defined SharedCOMLib/1.0.2@user/testing
    To change it, override it in your base requirements
```

### Old Behavior (1.12.3)

1. Run the following:
```sh
# Create SharedCOMLib 1.0.1
$ conan create shared_com_lib.py 1.0.1@user/testing
# Create SharedCOMLib 1.0.2
$ conan create shared_com_lib.py 1.0.2@user/testing
# Create SharedGuiLib 0.1
$ conan create shared_gui_lib.py user/testing
# Resolve requirements for MyApp 0.1
$ conan info myapp.py
```
2. The requirement provided by the build requirement is overridden as expected:
```
$ ./conan-1.12.3/Scripts/conan info myapp.py
SharedGuiLib/0.1@user/testing requirement SharedCOMLib/1.0.1@user/testing overridden by your conanfile to SharedCOMLib/1.0.2@user/testing
```

### Context

I have three Conan packages in play:

1. MyApp
_The primary Qt Desktop application that I'm trying to build. Not an actual package per se, but it uses Conan to describe its build dependencies._
2. SharedCOMLib
_Multiple COM ([Component Object Model](https://docs.microsoft.com/en-us/windows/desktop/com/component-object-model--com--portal)) dlls implementing various things. Used at runtime by "MyApp"_
3. SharedGuiLib
_Static Qt GUI library offering convenient Widgets / wrappers / utilities, including some that take advantage of classes found in "SharedCOMLib". Used by "MyApp" to avoid re-inventing the wheel on common widgets/dialogs/etc. shared between a variety of tools._

With the following package versions:

#### SharedCOMLib
* Version 1.0.1
* Version 1.0.2

#### SharedGuiLib
* Version 0.1
* Requires `SharedCOMLib/1.0.1`

#### MyApp
* Version 0.1
* Requires `SharedCOMLib/1.0.2`
* Build Requires `SharedGuiLib/0.1`

A build requirement of MyApp (i.e. "SharedCOMLib") has outdated requirements on another shared library (i.e. "SharedCOMLib"). MyApp also has a requirement on the same shared library (i.e. "SharedCOMLib"), albeit with a more up to date version.

Up until Conan 1.13, that has been okay, because Conan overrode the older version of "SharedCOMLib" coming from my MyApp's build requirements with the newer version coming from MyApp's requirements.

I can apply the fix outlined above in https://github.com/conan-io/conan/issues/4753#issuecomment-477611606, and do something like:

```diff
- requires = ("SharedCOMLib/1.0.2@user/testing",)
+def requirements(self):
+        self.requires('SharedCOMLib/1.0.2@user/testing', override=True)
```

But I'm not certain whether the above change is necessary in a 1.13+ world or whether my example illustrates a regression.

As always, thanks to you and all the other maintainers for all your hard work and support maintaining Conan!


### References

* https://github.com/conan-io/conan/issues/4753
* https://github.com/conan-io/conan/issues/4931
