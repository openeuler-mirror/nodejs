%bcond_with bootstrap
%global baserelease 7
%{?!_pkgdocdir:%global _pkgdocdir %{_docdir}/%{name}-%{version}}
%global nodejs_epoch 1
%global nodejs_major 10
%global nodejs_minor 21
%global nodejs_patch 0
%global nodejs_abi %{nodejs_major}.%{nodejs_minor}
%global nodejs_soversion 64
%global nodejs_version %{nodejs_major}.%{nodejs_minor}.%{nodejs_patch}
%global nodejs_release %{baserelease}
%global nodejs_datadir %{_datarootdir}/nodejs
%global v8_epoch 1
%global v8_major 6
%global v8_minor 8
%global v8_build 275
%global v8_patch 32
%global v8_abi %{v8_major}.%{v8_minor}
%global v8_version %{v8_major}.%{v8_minor}.%{v8_build}.%{v8_patch}
%global v8_release %{nodejs_epoch}.%{nodejs_major}.%{nodejs_minor}.%{nodejs_patch}.%{nodejs_release}
%global c_ares_major 1
%global c_ares_minor 15
%global c_ares_patch 0
%global c_ares_version %{c_ares_major}.%{c_ares_minor}.%{c_ares_patch}
%global http_parser_major 2
%global http_parser_minor 9
%global http_parser_patch 3
%global http_parser_version %{http_parser_major}.%{http_parser_minor}.%{http_parser_patch}
%global libuv_major 1
%global libuv_minor 34
%global libuv_patch 2
%global libuv_version %{libuv_major}.%{libuv_minor}.%{libuv_patch}
%global nghttp2_major 1
%global nghttp2_minor 41
%global nghttp2_patch 0
%global nghttp2_version %{nghttp2_major}.%{nghttp2_minor}.%{nghttp2_patch}
%global icu_major 64
%global icu_minor 2
%global icu_version %{icu_major}.%{icu_minor}
%global icudatadir %{nodejs_datadir}/icudata
%{!?little_endian: %global little_endian %(%{__python3} -c "import sys;print (0 if sys.byteorder=='big' else 1)")}
%global punycode_major 2
%global punycode_minor 1
%global punycode_patch 0
%global punycode_version %{punycode_major}.%{punycode_minor}.%{punycode_patch}
%global npm_epoch 1
%global npm_major 6
%global npm_minor 14
%global npm_patch 4
%global npm_version %{npm_major}.%{npm_minor}.%{npm_patch}
%global npm_release %{nodejs_epoch}.%{nodejs_major}.%{nodejs_minor}.%{nodejs_patch}.%{nodejs_release}
%global brotli_major 1
%global brotli_minor 0
%global brotli_patch 7
%global brotli_version %{brotli_major}.%{brotli_minor}.%{brotli_patch}

Name: nodejs
Epoch: %{nodejs_epoch}
Version: %{nodejs_version}
Release: %{nodejs_release}
Summary: JavaScript runtime
License: MIT and ASL 2.0 and ISC and BSD
Group: Development/Languages
URL: http://nodejs.org/

Source0: https://nodejs.org/dist/v%{version}/node-v%{version}.tar.gz
Source1: npmrc
Source2: btest402.js
Source3: https://github.com/unicode-org/icu/releases/download/release-%{icu_major}-%{icu_minor}/icu4c-%{icu_major}_%{icu_minor}-src.tgz
Source7: nodejs_native.attr

Patch1: 0001-Disable-running-gyp-on-shared-deps.patch
Patch2: 0002-Install-both-binaries-and-use-libdir.patch
Patch3: 0003-build-auto-load-ICU-data-from-with-icu-default-data-.patch
Patch4: 0004-src-avoid-OOB-read-in-URL-parser.patch
Patch5: CVE-2020-8252.patch
Patch6: CVE-2020-8265.patch
Patch7: CVE-2020-8287.patch
Patch8: CVE-2021-22883.patch
Patch9: CVE-2021-22884.patch
Patch10: CVE-2021-22918.patch

BuildRequires: python2-devel python3-devel zlib-devel gcc >= 6.3.0
BuildRequires: gcc-c++ >= 6.3.0 nodejs-packaging chrpath libatomic

%if %{with bootstrap}
Provides: bundled(http-parser) = %{http_parser_version}
Provides: bundled(libuv) = %{libuv_version}
Provides: bundled(nghttp2) = %{nghttp2_version}
%else
BuildRequires: systemtap-sdt-devel
BuildRequires: libuv-devel >= 1:%{libuv_version}
Requires: libuv >= 1:%{libuv_version}
BuildRequires: libnghttp2-devel >= %{nghttp2_version}
Requires: libnghttp2 >= %{nghttp2_version}
BuildRequires: http-parser-devel >= %{http_parser_version}
Requires: http-parser >= %{http_parser_version}
%endif

BuildRequires: openssl-devel
Requires: ca-certificates
Requires: nodejs-libs%{?_isa} = %{nodejs_epoch}:%{version}-%{release}
Recommends: nodejs-full-i18n%{?_isa} = %{nodejs_epoch}:%{version}-%{release}
Provides: nodejs(abi) = %{nodejs_abi}
Provides: nodejs(abi%{nodejs_major}) = %{nodejs_abi}
Provides: nodejs(v8-abi) = %{v8_abi}
Provides: nodejs(v8-abi%{v8_major}) = %{v8_abi}
Provides: nodejs(engine) = %{nodejs_version}
Conflicts: node <= 0.3.2-12
Provides: nodejs-punycode = %{punycode_version}
Provides: npm(punycode) = %{punycode_version}
Provides: bundled(c-ares) = %{c_ares_version}
Provides: bundled(v8) = %{v8_version}
Provides: bundled(icu) = %{icu_version}
Requires: (nodejs-packaging if rpm-build)
Recommends: npm >= %{npm_epoch}:%{npm_version}-%{npm_release}%{?dist}
Provides: bundled(brotli) = %{brotli_version}
Provides: %{name}-help = %{nodejs_epoch}:%{nodejs_version}-%{nodejs_release}%{?dist}
Obsoletes: %{name}-help < %{nodejs_epoch}:%{nodejs_version}-%{nodejs_release}%{?dist}

%description
Node.js is a platform built on Chrome's JavaScript runtime
for easily building fast, scalable network applications.
Node.js uses an event-driven, non-blocking I/O model that
makes it lightweight and efficient, perfect for data-intensive
real-time applications that run across distributed devices.

%package devel
Summary: JavaScript runtime - development headers
Group: Development/Languages
Requires: %{name}%{?_isa} = %{epoch}:%{nodejs_version}-%{nodejs_release}%{?dist}
Requires: openssl-devel%{?_isa}
Requires: zlib-devel%{?_isa}
Requires: brotli-devel%{?_isa}
Requires: nodejs-packaging

%if %{with bootstrap}
%else
Requires: http-parser-devel%{?_isa}
Requires: libuv-devel%{?_isa}
%endif

%description devel
Development headers for the Node.js JavaScript runtime.

%package libs
Summary: Node.js and v8 libraries

%if 0%{?__isa_bits} == 64
Provides: libv8.so.%{v8_major}()(64bit)
Provides: libv8_libbase.so.%{v8_major}()(64bit)
Provides: libv8_libplatform.so.%{v8_major}()(64bit)
%else
Provides: libv8.so.%{v8_major}
Provides: libv8_libbase.so.%{v8_major}
Provides: libv8_libplatform.so.%{v8_major}
%endif

Provides: v8 = %{v8_epoch}:%{v8_version}-%{nodejs_release}%{?dist}
Provides: v8%{?_isa} = %{v8_epoch}:%{v8_version}-%{nodejs_release}%{?dist}
Obsoletes: v8 < 1:6.7.17-10

%description libs
Libraries to support Node.js and provide stable v8 interfaces.

%package full-i18n
Summary: Non-English locale data for Node.js
Requires: %{name}%{?_isa} = %{nodejs_epoch}:%{nodejs_version}-%{nodejs_release}%{?dist}

%description full-i18n
Optional data files to provide full-icu support for Node.js. Remove this
package to save space if non-English locales are not needed.

%package -n v8-devel
Summary: v8 - development headers
Epoch: %{v8_epoch}
Version: %{v8_version}
Release: %{v8_release}%{?dist}
Requires: %{name}-devel%{?_isa} = %{nodejs_epoch}:%{nodejs_version}-%{nodejs_release}%{?dist}

%description -n v8-devel
Development headers for the v8 runtime.

%package -n npm
Summary: Node.js Package Manager
Epoch: %{npm_epoch}
Version: %{npm_version}
Release: %{npm_release}%{?dist}

Obsoletes: npm < 0:3.5.4-6
Provides: npm = %{npm_epoch}:%{npm_version}
Requires: nodejs = %{nodejs_epoch}:%{nodejs_version}-%{nodejs_release}%{?dist}
Recommends: nodejs-docs = %{nodejs_epoch}:%{nodejs_version}-%{nodejs_release}%{?dist}
Provides: npm(npm) = %{npm_version}

%description -n npm
npm is a package manager for node.js. You can use it to install and publish
your node programs. It manages dependencies and does other cool stuff.

%package docs
Summary: Node.js API documentation
Group: Documentation
BuildArch: noarch

Provides: %{name}-help = %{nodejs_epoch}:%{nodejs_version}-%{nodejs_release}%{?dist}
Obsoletes: %{name}-help < %{nodejs_epoch}:%{nodejs_version}-%{nodejs_release}%{?dist}
Conflicts: %{name} > %{nodejs_epoch}:%{nodejs_version}-%{nodejs_release}%{?dist}
Conflicts: %{name} < %{nodejs_epoch}:%{nodejs_version}-%{nodejs_release}%{?dist}

%description docs
The API documentation for the Node.js JavaScript runtime.

%prep
%autosetup -p1 -n node-v%{nodejs_version}
rm -rf deps/zlib
rm -rf deps/openssl
pathfix.py -i %{__python2} -pn $(find -type f ! -name "*.js")
find . -type f -exec sed -i "s~/usr\/bin\/env python~/usr/bin/python2~" {} \;
find . -type f -exec sed -i "s~/usr\/bin\/python\W~/usr/bin/python2~" {} \;
sed -i "s~python~python2~" $(find . -type f | grep "gyp$")
sed -i "s~usr\/bin\/python2~usr\/bin\/python3~" ./deps/v8/tools/gen-inlining-tests.py
sed -i "s~usr\/bin\/python.*$~usr\/bin\/python2~" ./deps/v8/tools/mb/mb_unittest.py
find . -type f -exec sed -i "s~python -c~python2 -c~" {} \;
sed -i "s~which('python')~which('python2')~" configure

%build
%define _lto_cflags %{nil}

%ifarch s390 s390x %{arm} %ix86
%global optflags %(echo %{optflags} | sed 's/-g /-g1 /')
%endif

export CC='%{__cc}'
export CXX='%{__cxx}'
export CFLAGS='%{optflags} \
               -D_LARGEFILE_SOURCE \
               -D_FILE_OFFSET_BITS=64 \
               -DZLIB_CONST \
               -fno-delete-null-pointer-checks'
export CXXFLAGS='%{optflags} \
                 -D_LARGEFILE_SOURCE \
                 -D_FILE_OFFSET_BITS=64 \
                 -DZLIB_CONST \
                 -fno-delete-null-pointer-checks'

export CFLAGS="$(echo ${CFLAGS} | tr '\n\\' '  ')"
export CXXFLAGS="$(echo ${CXXFLAGS} | tr '\n\\' '  ')"
export LDFLAGS="%{build_ldflags}"

%if %{with bootstrap}
./configure --prefix=%{_prefix} \
           --shared \
           --libdir=%{_lib} \
           --shared-openssl \
           --shared-zlib \
           --without-dtrace \
           --with-intl=small-icu \
           --debug-nghttp2 \
           --openssl-use-def-ca-store
%else
./configure --prefix=%{_prefix} \
           --shared \
           --libdir=%{_lib} \
           --shared-openssl \
           --shared-zlib \
           --shared-libuv \
           --shared-http-parser \
           --shared-nghttp2 \
           --with-dtrace \
           --with-intl=small-icu \
           --with-icu-default-data-dir=%{icudatadir} \
           --debug-nghttp2 \
           --openssl-use-def-ca-store
%endif

make BUILDTYPE=Release %{?_smp_mflags}
pushd deps/
tar xfz %SOURCE3
pushd icu/source
mkdir -p converted
%if 0%{?little_endian}
install -Dpm0644 data/in/icudt%{icu_major}l.dat converted/
%else
mkdir -p data/out/tmp
%configure
%make_build
icu_root=$(pwd)
LD_LIBRARY_PATH=./lib ./bin/icupkg -tb data/in/icudt%{icu_major}l.dat \
                                       converted/icudt%{icu_major}b.dat
%endif

popd # icu/source
popd # deps

%install
rm -rf %{buildroot}
./tools/install.py install %{buildroot} %{_prefix}
chmod 0755 %{buildroot}/%{_bindir}/node
chrpath --delete %{buildroot}%{_bindir}/node
ln -s libnode.so.%{nodejs_soversion} %{buildroot}%{_libdir}/libnode.so
for header in %{buildroot}%{_includedir}/node/libplatform %{buildroot}%{_includedir}/node/v8*.h; do
    header=$(basename ${header})
    ln -s %{_includedir}/node/${header} %{buildroot}%{_includedir}/${header}
done
for soname in libv8 libv8_libbase libv8_libplatform; do
    ln -s libnode.so.%{nodejs_soversion} %{buildroot}%{_libdir}/${soname}.so
    ln -s libnode.so.%{nodejs_soversion} %{buildroot}%{_libdir}/${soname}.so.%{v8_major}
done
mkdir -p %{buildroot}%{_prefix}/lib/node_modules
install -Dpm0644 %{SOURCE7} %{buildroot}%{_rpmconfigdir}/fileattrs/nodejs_native.attr
cat << EOF > %{buildroot}%{_rpmconfigdir}/nodejs_native.req
#!/bin/sh
echo 'nodejs(abi%{nodejs_major}) >= %nodejs_abi'
echo 'nodejs(v8-abi%{v8_major}) >= %v8_abi'
EOF
chmod 0755 %{buildroot}%{_rpmconfigdir}/nodejs_native.req
mkdir -p %{buildroot}%{_pkgdocdir}/html
cp -pr doc/* %{buildroot}%{_pkgdocdir}/html
rm -f %{buildroot}%{_pkgdocdir}/html/nodejs.1
mkdir -p %{buildroot}%{_datadir}/node
cp -p common.gypi %{buildroot}%{_datadir}/node
mv %{buildroot}/%{_datadir}/doc/node/gdbinit %{buildroot}/%{_pkgdocdir}/gdbinit
mkdir -p %{buildroot}%{_mandir} \
         %{buildroot}%{_pkgdocdir}/npm

cp -pr deps/npm/man/* %{buildroot}%{_mandir}/
rm -rf %{buildroot}%{_prefix}/lib/node_modules/npm/man
ln -sf %{_mandir}  %{buildroot}%{_prefix}/lib/node_modules/npm/man
cp -pr deps/npm/docs %{buildroot}%{_pkgdocdir}/npm/
rm -rf %{buildroot}%{_prefix}/lib/node_modules/npm/docs
ln -sf %{_pkgdocdir}/npm %{buildroot}%{_prefix}/lib/node_modules/npm/docs
rm -f %{buildroot}/%{_defaultdocdir}/node/lldb_commands.py \
      %{buildroot}/%{_defaultdocdir}/node/lldbinit
find %{buildroot}%{_prefix}/lib/node_modules/npm \
    -not -path "%{buildroot}%{_prefix}/lib/node_modules/npm/bin/*" \
    -executable -type f \
    -exec chmod -x {} \;
chmod 0755 %{buildroot}%{_prefix}/lib/node_modules/npm/node_modules/npm-lifecycle/node-gyp-bin/node-gyp
chmod 0755 %{buildroot}%{_prefix}/lib/node_modules/npm/node_modules/node-gyp/bin/node-gyp.js
mkdir -p %{buildroot}%{_sysconfdir}
cp %{SOURCE1} %{buildroot}%{_sysconfdir}/npmrc
mkdir -p %{buildroot}%{_prefix}/etc
ln -s %{_sysconfdir}/npmrc %{buildroot}%{_prefix}/etc/npmrc
install -Dpm0644 -t %{buildroot}%{icudatadir} deps/icu/source/converted/*

%check
LD_LIBRARY_PATH=%{buildroot}%{_libdir} %{buildroot}/%{_bindir}/node -e "require('assert').equal(process.versions.node, '%{nodejs_version}')"
LD_LIBRARY_PATH=%{buildroot}%{_libdir} %{buildroot}/%{_bindir}/node -e "require('assert').equal(process.versions.v8.replace(/-node\.\d+$/, ''), '%{v8_version}')"
LD_LIBRARY_PATH=%{buildroot}%{_libdir} %{buildroot}/%{_bindir}/node -e "require('assert').equal(process.versions.ares.replace(/-DEV$/, ''), '%{c_ares_version}')"

LD_LIBRARY_PATH=%{buildroot}%{_libdir} %{buildroot}/%{_bindir}/node -e "require(\"assert\").equal(require(\"punycode\").version, '%{punycode_version}')"

NODE_PATH=%{buildroot}%{_prefix}/lib/node_modules:%{buildroot}%{_prefix}/lib/node_modules/npm/node_modules LD_LIBRARY_PATH=%{buildroot}%{_libdir} %{buildroot}/%{_bindir}/node -e "require(\"assert\").equal(require(\"npm\").version, '%{npm_version}')"

NODE_PATH=%{buildroot}%{_prefix}/lib/node_modules:%{buildroot}%{_prefix}/lib/node_modules/npm/node_modules LD_LIBRARY_PATH=%{buildroot}%{_libdir} %{buildroot}/%{_bindir}/node --icu-data-dir=%{buildroot}%{icudatadir} %{SOURCE2}

%pretrans -n npm -p <lua>
-- Replace the npm man directory with a symlink
-- Drop this scriptlet when F31 is EOL
path = "%{_prefix}/lib/node_modules/npm/man"
st = posix.stat(path)
if st and st.type == "directory" then
  status = os.rename(path, path .. ".rpmmoved")
  if not status then
    suffix = 0
    while not status do
      suffix = suffix + 1
      status = os.rename(path .. ".rpmmoved", path .. ".rpmmoved." .. suffix)
    end
    os.rename(path, path .. ".rpmmoved")
  end
end

%pretrans -n v8-devel -p <lua>
-- Replace the v8 libplatform include directory with a symlink
-- Drop this scriptlet when F30 is EOL
path = "%{_includedir}/libplatform"
st = posix.stat(path)
if st and st.type == "directory" then
  status = os.rename(path, path .. ".rpmmoved")
  if not status then
    suffix = 0
    while not status do
      suffix = suffix + 1
      status = os.rename(path .. ".rpmmoved", path .. ".rpmmoved." .. suffix)
    end
    os.rename(path, path .. ".rpmmoved")
  end
end

%files
%{_bindir}/node
%dir %{_prefix}/lib/node_modules
%dir %{_datadir}/node
%dir %{_datadir}/systemtap
%dir %{_datadir}/systemtap/tapset
%{_datadir}/systemtap/tapset/node.stp

%if %{with bootstrap}
%else
%dir %{_usr}/lib/dtrace
%{_usr}/lib/dtrace/node.d
%endif

%{_rpmconfigdir}/fileattrs/nodejs_native.attr
%{_rpmconfigdir}/nodejs_native.req
%doc AUTHORS CHANGELOG.md COLLABORATOR_GUIDE.md GOVERNANCE.md README.md
%doc %{_mandir}/man1/node.1*

%files devel
%{_includedir}/node
%{_libdir}/libnode.so
%{_datadir}/node/common.gypi
%{_pkgdocdir}/gdbinit

%files full-i18n
%dir %{icudatadir}
%{icudatadir}/icudt%{icu_major}*.dat

%files libs
%license LICENSE
%{_libdir}/libnode.so.%{nodejs_soversion}
%{_libdir}/libv8.so.%{v8_major}
%{_libdir}/libv8_libbase.so.%{v8_major}
%{_libdir}/libv8_libplatform.so.%{v8_major}
%dir %{nodejs_datadir}/

%files -n v8-devel
%{_includedir}/libplatform
%{_includedir}/v8*.h
%{_libdir}/libv8.so
%{_libdir}/libv8_libbase.so
%{_libdir}/libv8_libplatform.so
%ghost %{_includedir}/libplatform.rpmmoved

%files -n npm
%{_bindir}/npm
%{_bindir}/npx
%{_prefix}/lib/node_modules/npm
%config(noreplace) %{_sysconfdir}/npmrc
%{_prefix}/etc/npmrc
%ghost %{_sysconfdir}/npmignore
%doc %{_mandir}/man1/npm*.1*
%doc %{_mandir}/man1/npx.1*
%doc %{_mandir}/man5/folders.5*
%doc %{_mandir}/man5/install.5*
%doc %{_mandir}/man5/npmrc.5*
%doc %{_mandir}/man5/package-json.5*
%doc %{_mandir}/man5/package-lock-json.5*
%doc %{_mandir}/man5/package-locks.5*
%doc %{_mandir}/man5/shrinkwrap-json.5*
%doc %{_mandir}/man7/config.7*
%doc %{_mandir}/man7/developers.7*
%doc %{_mandir}/man7/disputes.7*
%doc %{_mandir}/man7/orgs.7*
%doc %{_mandir}/man7/registry.7*
%doc %{_mandir}/man7/removal.7*
%doc %{_mandir}/man7/scope.7*
%doc %{_mandir}/man7/scripts.7*
%doc %{_mandir}/man7/semver.7*

%files docs
%dir %{_pkgdocdir}
%{_pkgdocdir}/html
%{_pkgdocdir}/npm/docs


%changelog
* Tue Jul 20 2021 zhouwenpei <zhouwenpei1@huawei.com> 1:10.21.0-7
- fix CVE-2021-22918

* Mon Mar 15 2021 xinghe <xinghe1@huawei.com> 1:10.21.0-6
- fix CVE-2021-22883 CVE-2021-22884

* Fri Feb 5 2021 xinghe <xinghe1@huawei.com> 1:10.21.0-5
- fix CVE-2020-8265 CVE-2020-8287

* Tue Dec 6 2020 wangxiao <wangxiao65@huawei.com> 1:10.21.0-4
- fix CVE-2020-8252

* Sat Nov 28 2020 wutao <wutao61@huawei.com> 1:10.21.0-3
- fix conflicts between help and docs packages

* Wed Nov 04 2020 gaozhekang <gaozhekang@huawei.com> - 1:10.21.0-2
- avoid OOB read in URL parser

* Wed Oct 14 2020 Jeffery.Gao <gaojianxing@huawei.com> - 1:10.21.0-1
- Update to 10.21.0

* Thu Aug 20 2020 wutao <wutao61@huawei.com> - 1:10.11.0-3
- fix dist miss problem

* Fri Mar 20 2020 shijian <shijian16@huawei.com> - 1:10.11.0-2
- Fix CVE-2018-12122 CVE-2019-5737

* Fri Mar  6 2020 openEuler Buildteam <buildteam@openeuler.org> - 1:10.11.0-1
- Package init
