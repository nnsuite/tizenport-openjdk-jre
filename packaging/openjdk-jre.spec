%define debug_package %{nil}

Name:		openjdk-jre
Version:	1.8.0.222
Release:	0
Summary:	OpenJDK 8 JRE Repackaging Official Downloads
License:        Apache-1.1 AND Apache-2.0 AND GPL-1.0-or-later AND GPL-2.0-only AND GPL-2.0-with-classpath-exception AND LGPL-2.0-only AND MPL-1.0 AND MPL-1.1 AND SUSE-Public-Domain AND W3C
Group:          Development/Languages/Java
Url:            http://openjdk.java.net/

Source0:	openjdk-jre-%{version}.tar.gz

Source2000:	openjdk-jre.manifest

ExclusiveArch:	aarch64 x86_64 %ix86 armv7l

%description
The full openjdk 8 downloaded at
https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html
This is RPM package of the downloaded tar.gz.
Fetched deb files and extracted data.tar.xz from
https://packages.debian.org/sid/openjdk-8-jdk-headless

Do NOT install this into deployed images.

%prep
%setup -q
cp %{SOURCE2000} .

%build

# Nothing to do. They are prebuilt binaries.

%install


# armv7l / armel
%ifarch armv7l
%define archivepath %{_builddir}/%{name}-%{version}/openjdk-8-jre-headless_8u222-b10-1/armel/data.tar
%define keyword armel
%endif

# aarch64 / arm64
%ifarch aarch64
%define archivepath %{_builddir}/%{name}-%{version}/openjdk-8-jre-headless_8u222-b10-1/arm64/data.tar
%define keyword arm64
%endif

# x86_64 / amd64
%ifarch x86_64
%define archivepath %{_builddir}/%{name}-%{version}/openjdk-8-jre-headless_8u222-b10-1/amd64/data.tar
%define keyword amd64
%endif

# ix86 / i386
%ifarch %ix86
%define archivepath %{_builddir}/%{name}-%{version}/openjdk-8-jre-headless_8u222-b10-1/i386/data.tar
%define keyword i386
%endif

pushd %{buildroot}
xz -d %{archivepath}.xz
tar -xf %{archivepath}
pushd usr
# remove doc
rm -rf share
pushd lib
rm -rf debug
popd
popd

mkdir -p %{buildroot}%{_libdir}
pushd %{buildroot}%{_libdir}
ln -sf /usr/lib/jvm/java-8-openjdk-%{keyword}/jre/lib/%{keyword}/jli/libjli.so libjli.so
popd

popd

%files
%manifest openjdk-jre.manifest
%defattr(-,root,root,-)
/usr/lib/jvm
/etc/java-8-openjdk
%exclude /usr/lib/jvm/java-8-openjdk-*/jre/lib/*/jli

%post -p /usr/sbin/ldconfig
%postun -p /usr/sbin/ldconfig

%package libjli
Summary:	Provide libjli only for openjdk-jdk
%description libjli
Provides libjli only
%files libjli
%manifest openjdk-jre.manifest
/usr/lib/jvm/java-8-openjdk-*/jre/lib/*/jli
%{_libdir}/libjli.so

%post libjli
/usr/sbin/ldconfig
%postun libjli
/usr/sbin/ldconfig
