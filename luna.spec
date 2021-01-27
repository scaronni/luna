# Notes:
# - All the libraries do not have a SONAME defined (readealf -d $so | grep SONAME)
# - All the PCI card drivers require the base client, the rest not
# - The group hsmusers is created here and set on PCI card udev rules

%global hsmusers_group hsmusers
%global	debug_package %{nil}

Name:           luna
Version:        10.3.0
Release:        1%{?dist}
Summary:        Linux Client Software for Thales Luna HSMs
License:        Thales Luna HSM License Agreement
URL:            https://cpl.thalesgroup.com/encryption/hardware-security-modules/general-purpose-hsms

ExclusiveArch:  x86_64

Source0:        %{name}-%{version}.tar.xz
Source1:        %{name}-tarball.sh
Source2:        %{name}-pedserver.service
Source3:        %{name}-pedserver.xml
Source4:        %{name}-pedclient.service

BuildRequires:  javapackages-tools
BuildRequires:  systemd-devel


%description
Linux Client Software for Thales Luna HSM 7.7.0 for Network HSM and PCI-e HSM
release. Includes Client Software, Drivers, Remote PED And Backup HSM.

%package        devel
Summary:        Header files and development libraries for %{name}
Requires:       %{name}%{?_isa} == %{version}-%{release}

%description    devel
This package contains headers and static libraries to develop software that uses
the Luna Client software, including the FM SDK.

%package        java
Summary:        Java components for the Luna Client
Requires:       javapackages-filesystem

%description    java
Luna Java Service Provider C++, JCPROV JNI Library and JSP jMultitoken to test
the performance of the Luna Java Service Provider.

%package        javadoc
Summary:        Javadoc for the Java Luna Client components.
Requires:       javapackages-filesystem

%description    javadoc
Luna Java Service Provider C++, JCPROV JNI Library and JSP jMultitoken to test
the performance of the Luna Java Service Provider.

Contains the following javadoc documentation:
- Luna Java Service Provider Documentation
- Luna JCPROV documentation

%package        pedserver
Summary:        Connect a PED to a remote HSM
Requires:       kmod-lunaped
Requires:       systemd
Requires:       firewalld-filesystem

%description    pedserver
The PED server program that resides on a workstation and mediates between a
locally-connected Remote PED and a distant PEDClient (running at a distant Luna
HSM).

%package        pedclient
Summary:        Accept connections from A remote PED.
Requires:       %{name}%{?_isa} == %{version}-%{release}
Requires:       systemd
Requires:       kmod-k7
Requires:       kmod-g7
#Requires:       kmod-uhd
#Requires:       kmod-vkd

%description    pedclient
The PED Client program - embedded in the case of a Luna appliance, or installed
on a computer with a contained Luna K-card HSM or with a USB-connected Luna G5
(or Backup) HSM - anchors the HSM end of the Remote PED service and initiates
the contact with a PedServer instance, on behalf of its HSM.

%package        samples
Summary:        Luna Client code samples
Requires:       %{name}-devel%{?_isa} == %{version}-%{release}

%description samples
Examples that use the Luna Client Software:
- SafeNet PKCS 11
- ProtectToolkit Functionality
- Luna Java Service Provider
- Luna JCPROV

%prep
%autosetup -n %{name}-%{version}

# Reorganize samples to pick them up later in the files section:
mkdir samples
mv usr/safenet/lunaclient/samples samples/lunaclient
mv usr/safenet/lunafmsdk/samples samples/lunafmsdk
mv usr/safenet/lunaclient/jsp/samples samples/jsp
mv usr/safenet/lunaclient/jcprov/samples samples/jcprov

%build
# Nothing to build

%install
# Binaries
mkdir -p %{buildroot}%{_bindir}
cp -f usr/safenet/lunaclient/bin/* %{buildroot}%{_bindir}/
rm -f %{buildroot}%{_bindir}/openssl.cnf

mkdir -p %{buildroot}%{_sbindir}
cp -f usr/safenet/lunaclient/sbin/* %{buildroot}%{_sbindir}/
mv %{buildroot}%{_bindir}/PedServer %{buildroot}%{_sbindir}/
# Symlink to find the binary
ln -sf PedServer %{buildroot}%{_sbindir}/pedServer

# Headers
mkdir -p %{buildroot}%{_includedir}
cp -fr usr/safenet/lunafmsdk/include/* %{buildroot}%{_includedir}/

# Libraries
mkdir -p %{buildroot}%{_libdir}
cp -f usr/safenet/luna{client,fmsdk}/lib/* \
  usr/safenet/lunaclient/jcprov/lib/*.so \
  usr/safenet/lunaclient/jsp/lib/*.so \
  %{buildroot}%{_libdir}/

# Java
mkdir -p %{buildroot}%{_javadir}/luna
cp -f usr/safenet/lunaclient/{jsp,jcprov}/lib/*.jar %{buildroot}%{_javadir}/luna/
cp -f usr/safenet/lunaclient/jsp/bin/*.{class,jar} %{buildroot}%{_javadir}/luna/

# Configuration files
mkdir -p %{buildroot}%{_sysconfdir}
cp -f etc/*.conf %{buildroot}%{_sysconfdir}/

# Systemd & firewall
install -p -m 644 -D %{SOURCE2} %{buildroot}%{_unitdir}/pedserver.service
install -p -m 644 -D %{SOURCE3} %{buildroot}%{_prefix}/lib/firewalld/services/pedserver.xml
install -p -m 644 -D %{SOURCE4} %{buildroot}%{_unitdir}/pedclient.service

# Javadoc
mkdir -p %{buildroot}%{_javadocdir}/luna
cp -fr usr/safenet/lunaclient/jsp/javadoc %{buildroot}%{_javadocdir}/luna/jsp
cp -fr usr/safenet/lunaclient/jcprov/javadocs %{buildroot}%{_javadocdir}/luna/jcprov

# All the libraries do not have a SONAME defined (readealf -d $so | grep SONAME), so ldconfig does not touch them:
#ln -sf libCryptoki2_64.so %{buildroot}%{_libdir}/libCryptoki2_64.so.%{version}
#ln -sf libCryptoki2_64.so %{buildroot}%{_libdir}/libCryptoki2_64.so.2

# Logging
mkdir -p %{buildroot}/var/log/luna

# Compatibility symlinks
mkdir -p %{buildroot}%{_sysconfdir}/lunaclient
mkdir -p %{buildroot}%{_prefix}/safenet
ln -sf %{_sysconfdir}/lunaclient %{buildroot}%{_prefix}/safenet/lunaclient
ln -sf %{_libdir} %{buildroot}%{_sysconfdir}/lunaclient/lib

%ldconfig_scriptlets

%ldconfig_scriptlets java

%pre
getent group %{hsmusers_group} >/dev/null || groupadd -r %{hsmusers_group}

%post   pedserver
%systemd_post pedserver.service
%firewalld_reload

%preun  pedserver
%systemd_preun pedserver.service

%postun pedserver
%systemd_postun_with_restart pedserver.service
%firewalld_reload

%post   pedclient
%systemd_post pedclient.service

%preun  pedclient
%systemd_preun pedclient.service

%postun pedclient
%systemd_postun_with_restart pedclient.service

%files
%license 008-010068-001_EULA_HSM7_SW_revC.txt
%{_sbindir}/hsmrecover
%{_sbindir}/lunareset
%{_bindir}/ckdemo
%{_bindir}/cmu
%{_bindir}/configurator
%{_bindir}/ctfm
%{_bindir}/fmrecover
%{_bindir}/lunacm
%{_bindir}/lunadiag
%{_bindir}/mkfm
%{_bindir}/multitoken
%exclude %{_bindir}/salogin
%{_bindir}/vtl
%{_libdir}/libCryptoki2_64.so
%{_libdir}/libcklog2.so
%{_libdir}/libethsm.so
%{_libdir}/libshim.so
%exclude %{_libdir}/libSoftToken.so
%config %attr(644,root,%{hsmusers_group}) %{_sysconfdir}/Chrystoki.conf
%{_sysconfdir}/lunaclient
# Compatibility links
%{_prefix}/safenet

%files devel
%{_includedir}/fm
%{_libdir}/libfmsupt.a

%files java
%{_libdir}/libjcprov.so
%{_libdir}/libLunaAPI.so
%{_javadir}/luna

%files javadoc
%license 008-010068-001_EULA_HSM7_SW_revC.pdf
%{_javadocdir}/luna

%files pedserver
%{_prefix}/lib/firewalld/services/pedserver.xml
%{_sbindir}/PedServer
%{_sbindir}/pedServer
%{_unitdir}/pedserver.service
%config %attr(644,root,root) %{_sysconfdir}/pedServer.conf

%files pedclient
%{_bindir}/pedClient
%{_unitdir}/pedclient.service

%files samples
%doc samples

%changelog
* Fri Jan 22 2021 Simone Caronni <negativo17@gmail.com> - 10.3.0-1
- First build based on Luna Client 10.3.
