%{?!_pkgdocdir:%global _pkgdocdir %{_docdir}/%{name}-%{version}}

%global nodejs_epoch 1
%global nodejs_major 10
%global nodejs_minor 11
%global nodejs_patch 0
%global nodejs_abi %{nodejs_major}.%{nodejs_minor}
%global nodejs_version %{nodejs_major}.%{nodejs_minor}.%{nodejs_patch}
%global nodejs_release 5

%global v8_major 6
%global v8_minor 8
%global v8_build 275
%global v8_patch 32
%global v8_abi %{v8_major}.%{v8_minor}
%global v8_version %{v8_major}.%{v8_minor}.%{v8_build}.%{v8_patch}

%global c_ares_version 1.14.0
%global libuv_version 1.23.0
%global nghttp2_version 1.33.0
%global icu_version 62.1
%global punycode_version 2.1.0

%global npm_epoch 1
%global npm_version 6.4.1
%global npm_release 1.10.11.0.1

Name: nodejs
Epoch: %{nodejs_epoch}
Version: %{nodejs_version}
Release: %{nodejs_release}
Summary: JavaScript runtime
License: MIT and ASL 2.0 and ISC and BSD
URL: http://nodejs.org/

Source0: node-v%{nodejs_version}-stripped.tar.gz
Source1: nodejs_native.attr
Source2: nodejs_native.req

Patch0001: Disable-running-gyp-on-shared-deps.patch
Patch0002: Suppress-NPM-message-to-run-global-update.patch
#https://github.com/nodejs/node/commit/ee618a7ab239c98d945c723a4e225bc409151736
Patch0003: CVE-2018-12122.patch
#https://github.com/nodejs/node/commit/1a7302bd48
Patch0004: CVE-2019-5737.patch 
Patch0005: CVE-2018-12121.patch
Patch0006: CVE-2018-12123.patch
Patch0007: src-avoid-OOB-read-in-URL-parser.patch

BuildRequires: gcc gcc-c++ openssl-devel
BuildRequires: http-parser-devel
BuildRequires: libuv-devel >= 1:%{libuv_version}
BuildRequires: libnghttp2-devel >= %{nghttp2_version}
BuildRequires: python2-devel python3-devel zlib-devel

Requires: ca-certificates http-parser >= 2.7.0
Requires: libuv >= 1:1.20.2 libnghttp2 >= %{nghttp2_version}
Requires: npm = %{npm_epoch}:%{npm_version}-%{npm_release}

Provides: nodejs(engine) = %{nodejs_version}
Provides: bundled(v8) = %{v8_version}
Provides: bundled(icu) = %{icu_version}
Provides: nodejs(abi) = %{nodejs_abi}
Provides: nodejs-punycode = %{punycode_version}
Provides: nodejs(v8-abi%{v8_major}) = %{v8_abi}
Provides: npm(punycode) = %{punycode_version}
Provides: bundled(c-ares) = %{c_ares_version}
Provides: nodejs(abi%{nodejs_major}) = %{nodejs_abi}
Provides: nodejs(v8-abi) = %{v8_abi}
Conflicts: node <= 0.3.2-12

%description
Node.js is an open-source, cross-platform, JavaScript runtime environment,
it executes JavaScript code outside of a browser.

%package devel
Summary: JavaScript runtime - development headers
Requires: %{name} = %{epoch}:%{nodejs_version}-%{nodejs_release}%{?dist}
Requires: openssl-devel zlib-devel
Requires: libuv-devel http-parser-devel
Requires: nodejs-packaging

%description devel
Development headers for the Nodejs.

%package -n npm
Summary: Node.js Package Manager
Epoch: %{npm_epoch}
Version: %{npm_version}
Release: %{npm_release}

Provides: npm = %{npm_epoch}:%{npm_version}
Provides: npm(npm) = %{npm_version}
Obsoletes: npm < 0:3.5.4-6

%description -n npm
npm is a package manager for node.js.

%package help
Summary: Nodejs documentation
BuildArch: noarch

%description help
The manual documentation for Nodejs.

%prep
%autosetup -n node-v%{nodejs_version} -p1

pathfix.py -i %{__python2} -pn $(find -type f)
find . -type f -exec sed -i "s~/usr\/bin\/env python~/usr/bin/python2~" {} \;
find . -type f -exec sed -i "s~/usr\/bin\/python\W~/usr/bin/python2~" {} \;
sed -i "s~python~python2~" $(find . -type f | grep "gyp$")
sed -i "s~usr\/bin\/python2~usr\/bin\/python3~" ./deps/v8/tools/gen-inlining-tests.py
sed -i "s~usr\/bin\/python.*$~usr\/bin\/python2~" ./deps/v8/tools/mb/mb_unittest.py
find . -type f -exec sed -i "s~python -c~python2 -c~" {} \;
sed -i "s~which('python')~which('python2')~" configure

%build

export CFLAGS='%{optflags} -g \
               -D_LARGEFILE_SOURCE \
               -D_FILE_OFFSET_BITS=64 \
               -DZLIB_CONST \
               -fno-delete-null-pointer-checks'
export CXXFLAGS='%{optflags} -g \
                 -D_LARGEFILE_SOURCE \
                 -D_FILE_OFFSET_BITS=64 \
                 -DZLIB_CONST \
                 -fno-delete-null-pointer-checks'

export CFLAGS="$(echo ${CFLAGS} | tr '\n\\' '  ')"
export CXXFLAGS="$(echo ${CXXFLAGS} | tr '\n\\' '  ')"
export LDFLAGS="%{build_ldflags}"

./configure --prefix=%{_prefix} \
           --shared-openssl \
           --shared-zlib \
           --shared-libuv \
           --shared-http-parser \
           --shared-nghttp2 \
           --with-dtrace \
           --with-intl=small-icu \
           --debug-nghttp2 \
           --openssl-use-def-ca-store

make BUILDTYPE=Release %{?_smp_mflags}

%install
rm -rf %{buildroot}
./tools/install.py install %{buildroot} %{_prefix}
chmod 0755 %{buildroot}/%{_bindir}/node
mkdir -p %{buildroot}%{_prefix}/lib/node_modules
install -Dpm0644 %{SOURCE1} %{buildroot}%{_rpmconfigdir}/fileattrs/nodejs_native.attr
install -Dpm0644 %{SOURCE2} %{buildroot}%{_rpmconfigdir}/nodejs_native.req
chmod 0755 %{buildroot}%{_rpmconfigdir}/nodejs_native.req
mkdir -p %{buildroot}%{_pkgdocdir}/html
cp -pr doc/* %{buildroot}%{_pkgdocdir}/html
rm -f %{buildroot}%{_pkgdocdir}/html/nodejs.1
mkdir -p %{buildroot}%{_datadir}/node
cp -p common.gypi %{buildroot}%{_datadir}/node
mv %{buildroot}/%{_datadir}/doc/node/gdbinit %{buildroot}/%{_pkgdocdir}/gdbinit
mkdir -p %{buildroot}%{_mandir} %{buildroot}%{_pkgdocdir}/npm
cp -pr deps/npm/man/* %{buildroot}%{_mandir}/
rm -rf %{buildroot}%{_prefix}/lib/node_modules/npm/man
ln -sf %{_mandir}  %{buildroot}%{_prefix}/lib/node_modules/npm/man
cp -pr deps/npm/html deps/npm/doc %{buildroot}%{_pkgdocdir}/npm/
rm -rf %{buildroot}%{_prefix}/lib/node_modules/npm/html
rm -rf %{buildroot}%{_prefix}/lib/node_modules/npm/doc
ln -sf %{_pkgdocdir} %{buildroot}%{_prefix}/lib/node_modules/npm/html
ln -sf %{_pkgdocdir}/npm/html %{buildroot}%{_prefix}/lib/node_modules/npm/doc
rm -f %{buildroot}/%{_defaultdocdir}/node/lldb_commands.py
rm -f %{buildroot}/%{_defaultdocdir}/node/lldbinit

find %{buildroot}%{_prefix}/lib/node_modules/npm \
    -not -path "%{buildroot}%{_prefix}/lib/node_modules/npm/bin/*" \
    -executable -type f \
    -exec chmod -x {} \;

%check
%{buildroot}/%{_bindir}/node -e "require('assert').equal(process.versions.node, '%{nodejs_version}')"
%{buildroot}/%{_bindir}/node -e "require('assert').equal(process.versions.v8.replace(/-node\.\d+$/, ''), '%{v8_version}')"
%{buildroot}/%{_bindir}/node -e "require('assert').equal(process.versions.ares.replace(/-DEV$/, ''), '%{c_ares_version}')"
%{buildroot}/%{_bindir}/node -e "require(\"assert\").equal(require(\"punycode\").version, '%{punycode_version}')"
NODE_PATH=%{buildroot}%{_prefix}/lib/node_modules:%{buildroot}%{_prefix}/lib/node_modules/npm/node_modules %{buildroot}/%{_bindir}/node -e "require(\"assert\").equal(require(\"npm\").version, '%{npm_version}')"

%files
%{_bindir}/node
%dir %{_prefix}/lib/node_modules
%dir %{_datadir}/node
%dir %{_usr}/lib/dtrace
%{_usr}/lib/dtrace/node.d
%dir %{_datadir}/systemtap/tapset
%{_datadir}/systemtap/tapset/node.stp
%{_rpmconfigdir}/fileattrs/nodejs_native.attr
%{_rpmconfigdir}/nodejs_native.req
%license LICENSE
%doc AUTHORS CHANGELOG.md COLLABORATOR_GUIDE.md GOVERNANCE.md README.md

%files devel
%{_includedir}/node
%{_datadir}/node/common.gypi
%{_pkgdocdir}/gdbinit

%files -n npm
%{_bindir}/npm
%{_bindir}/npx
%{_prefix}/lib/node_modules/npm
%ghost %{_sysconfdir}/npmrc
%ghost %{_sysconfdir}/npmignore
%doc %{_mandir}/man*/npm*
%doc %{_mandir}/man*/npx*
%doc %{_mandir}/man5/package.json.5*
%doc %{_mandir}/man5/package-lock.json.5*
%doc %{_mandir}/man7/removing-npm.7*
%doc %{_mandir}/man7/semver.7*

%files help
%dir %{_pkgdocdir}
%{_pkgdocdir}/html
%{_pkgdocdir}/npm/html
%{_pkgdocdir}/npm/doc
%doc %{_mandir}/man1/node.1*

%changelog
* Wed Nov 04 2020 gaozhekang <gaozhekang@huawei.com> - 1:10.11.0-5
- avoid OOB read in URL parser

* Sun Sep 20 2020 zhangtao <zhangtao221@huawei.com> - 1:10.11.0-4
- Fix CVE-2018-12121 CVE-2018-12123

* Thu Aug 20 2020 wutao <wutao61@huawei.com> - 1:10.11.0-3
- fix dist miss problem

* Fri Mar 20 2020 shijian <shijian16@huawei.com> - 1:10.11.0-2
- Fix CVE-2018-12122 CVE-2019-5737

* Fri Mar  6 2020 openEuler Buildteam <buildteam@openeuler.org> - 1:10.11.0-1
- Package init
