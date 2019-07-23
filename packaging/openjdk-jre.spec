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
%define keyword2 arm
%endif

# aarch64 / arm64
%ifarch aarch64
%define archivepath %{_builddir}/%{name}-%{version}/openjdk-8-jre-headless_8u222-b10-1/arm64/data.tar
%define keyword arm64
%define keyword2 aarch64
%endif

# x86_64 / amd64
%ifarch x86_64
%define archivepath %{_builddir}/%{name}-%{version}/openjdk-8-jre-headless_8u222-b10-1/amd64/data.tar
%define keyword amd64
%define keyword2 amd64
%endif

# ix86 / i386
%ifarch %ix86
%define archivepath %{_builddir}/%{name}-%{version}/openjdk-8-jre-headless_8u222-b10-1/i386/data.tar
%define keyword i386
%define keyword2 i386
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
ln -sf /usr/lib/jvm/java-8-openjdk-%{keyword}/jre/lib/%{keyword2}/jli/libjli.so libjli.so
ln -sf /usr/lib/jvm/java-8-openjdk-%{keyword}/jre/lib/%{keyword2}/server/libjvm.so libjvm.so
ln -sf /usr/lib/jvm/java-8-openjdk-%{keyword}/jre/lib/%{keyword2}/libverify.so libverify.so
ln -sf /usr/lib/jvm/java-8-openjdk-%{keyword}/jre/lib/%{keyword2}/libjava.so libjava.so
popd

popd

%files
%manifest openjdk-jre.manifest
%defattr(-,root,root,-)
/usr/lib/jvm
/etc/java-8-openjdk
%exclude /usr/lib/jvm/java-8-openjdk-%{keyword}/jre/lib/%{keyword2}/jli
%exclude /usr/lib/jvm/java-8-openjdk-%{keyword}/jre/lib/%{keyword2}/server/libjvm.so
%exclude /usr/lib/jvm/java-8-openjdk-%{keyword}/jre/lib/%{keyword2}/libverify.so
%exclude /usr/lib/jvm/java-8-openjdk-%{keyword}/jre/lib/%{keyword2}/libjava.so

# extra
%exclude /usr/lib/jvm/java-8-openjdk-%{keyword}/jre/lib/%{keyword2}/libjawt.so
%exclude /usr/lib/jvm/java-8-openjdk-%{keyword}/jre/lib/%{keyword2}/libawt_xawt.so
%exclude /usr/lib/jvm/java-8-openjdk-%{keyword}/jre/lib/%{keyword2}/libj2pcsc.so
%exclude /usr/lib/jvm/java-8-openjdk-%{keyword}/jre/lib/%{keyword2}/libjavajpeg.so
%exclude /usr/lib/jvm/java-8-openjdk-%{keyword}/jre/lib/%{keyword2}/libfontmanager.so
%exclude /usr/lib/jvm/java-8-openjdk-%{keyword}/jre/lib/%{keyword2}/libjavalcms.so
#extra libc6 2.28
%exclude /usr/lib/jvm/java-8-openjdk-%{keyword}/jre/lib/%{keyword2}/libsctp.so
%exclude /usr/lib/jvm/java-8-openjdk-%{keyword}/jre/lib/%{keyword2}/libnio.so


%post -p /usr/sbin/ldconfig
%postun -p /usr/sbin/ldconfig

%package essentials
Summary:	Provide libjli only for openjdk-jdk
%description essentials
Provides libjli only
%files essentials
%manifest openjdk-jre.manifest
/usr/lib/jvm/java-8-openjdk-*/jre/lib/*/jli
/usr/lib/jvm/java-8-openjdk-%{keyword}/jre/lib/%{keyword2}/server/libjvm.so
/usr/lib/jvm/java-8-openjdk-%{keyword}/jre/lib/%{keyword2}/libverify.so
/usr/lib/jvm/java-8-openjdk-%{keyword}/jre/lib/%{keyword2}/libjava.so
%{_libdir}/*

%post essentials
/usr/sbin/ldconfig
%postun essentials
/usr/sbin/ldconfig

%package extra
Summary:	Extra JRE files that may break Tizen
%description extra
Do not install
%files extra
/usr/lib/jvm/java-8-openjdk-%{keyword}/jre/lib/%{keyword2}/libjawt.so
/usr/lib/jvm/java-8-openjdk-%{keyword}/jre/lib/%{keyword2}/libawt_xawt.so
/usr/lib/jvm/java-8-openjdk-%{keyword}/jre/lib/%{keyword2}/libj2pcsc.so
/usr/lib/jvm/java-8-openjdk-%{keyword}/jre/lib/%{keyword2}/libjavajpeg.so
/usr/lib/jvm/java-8-openjdk-%{keyword}/jre/lib/%{keyword2}/libfontmanager.so
/usr/lib/jvm/java-8-openjdk-%{keyword}/jre/lib/%{keyword2}/libjavalcms.so
/usr/lib/jvm/java-8-openjdk-%{keyword}/jre/lib/%{keyword2}/libsctp.so
/usr/lib/jvm/java-8-openjdk-%{keyword}/jre/lib/%{keyword2}/libnio.so
