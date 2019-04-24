### Expected Behavior ( I think )

I would expect Conan's "private" requirements to participate in transitive requirement resolution in order to avoid violations of the [One Definition Rule].

### Current Behavior (1.14.4)

1. Run the following:
```sh
# install conan 1.14.4 in venv and build examples
$ ./conan-1.14.4/Scripts/python build.py
```
2. And receive the following error:
```
MyBoostClone/1.67.0@user/testing
    ID: 55fff3b995daa8cc67f1adbb986bef56b7284edd
    BuildID: None
    Remote: None
    Recipe: Cache
    Binary: Skip
    Binary remote: None
    Creation date: 2019-04-23 16:59:00
    Required by:
        SharedStaticLib/0.1@user/testing
MyBoostClone/1.70.0@user/testing
    ID: 55fff3b995daa8cc67f1adbb986bef56b7284edd
    BuildID: None
    Remote: None
    Recipe: Cache
    Binary: Cache
    Binary remote: None
    Creation date: 2019-04-23 16:59:02
    Required by:
        myapp.py (MyApp/0.1@None/None)
MyZlibClone/1.2.8@user/testing
    ID: 479e5c321685f6e20cbbf93c38ae334c54ade580
    BuildID: None
    Remote: None
    Recipe: Cache
    Binary: Skip
    Binary remote: None
    Creation date: 2019-04-23 16:58:57
    Required by:
        SharedStaticLib/0.1@user/testing
MyZlibClone/1.2.11@user/testing
    ID: 479e5c321685f6e20cbbf93c38ae334c54ade580
    BuildID: None
    Remote: None
    Recipe: Cache
    Binary: Cache
    Binary remote: None
    Creation date: 2019-04-23 16:58:59
    Required by:
        myapp.py (MyApp/0.1@None/None)
SharedStaticLib/0.1@user/testing
    ID: 120398e629c94b86476bf86eea4690f10dacfc1a
    BuildID: None
    Remote: None
    Recipe: Cache
    Binary: Cache
    Binary remote: None
    Creation date: 2019-04-23 16:59:04
    Required by:
        myapp.py (MyApp/0.1@None/None)
    Requires:
        MyZlibClone/1.2.8@user/testing
        MyBoostClone/1.67.0@user/testing
myapp.py (MyApp/0.1@None/None)
    ID: 2036575750b15d9f9e530734a22e3980aae91a98
    BuildID: None
    Requires:
        MyBoostClone/1.70.0@user/testing
        MyZlibClone/1.2.11@user/testing
        SharedStaticLib/0.1@user/testing
```

3. Note that MyApp contains two different versions of the same header only library (`MyBoostClone/1.70.0` and `MyBoostClone/1.67.0`)
  and also two different versions of the same static library (`MyZlibClone/1.2.11` and `MyZlibClone/1.2.8`),
  which I believe may result in violations of the [One Definition Rule].

4. I would expect the following:
    * Conan to override `MyZlibClone/1.2.8`, because `MyZlibClone/1.2.11` is semver compatible and use only one version of `MyZlibClone`
    * Conan to reject the use of `SharedStaticLib/0.1`, because it is `full_version_mode` incompatible with MyApp's requirement of `MyBoostClone/1.70.0`. 

### Context

This example attempts to illustrate a real world package my team maintains.

SharedStaticLib represents a collection of helpful utilities used by a variety
of tools. SharedStaticLib is careful to minimize its public API footprint and keeps
any heavy weight dependencies out of its public headers / API.

Use of libraries like Boost or zlib are seen as "implementation details" of the SharedStaticLib
and otherwise hidden from consuming apps.

Other tools, like MyApp, consume SharedStaticLib and may also have some of these same
dependencies (e.g. Boost or zlib) for their own reasons.

This example shows that using "private" requirements in a shared library
may result in violations of the [One Definition Rule] (ODR).

The easiest one to see is Boost, where this example shows 
that both Boost 1.70.0 and Boost 1.67.0 can end up in the same binary.

Conan is not honoring the full_version_mode requirement of Boost by the SharedStaticLib.

Likewise, with zlib, the consuming app has selected a higher, semver compatible
version of zlib, but Conan is not factoring this into its decision to use 
the cached SharedStaticLib, which has an older version embedded inside it,
which would similarly result in ODR violations because the static lib
is using 1.2.8 and the consuming app 1.2.11 yet both are found in the consuming app.

Similarly, if the consuming app used a higher semver incompatible version of zlib,
like 2.0.0, I would expect Conan to reject the use of `SharedStaticLib/0.1` as incompatible.


### References

* https://github.com/conan-io/conan/issues/4753
* https://github.com/conan-io/conan/issues/4931
* https://github.com/conan-io/conan/pull/4987

[One Definition Rule]: https://en.wikipedia.org/wiki/One_Definition_Rule
