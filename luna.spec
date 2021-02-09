# Notes:
# - All the libraries do not have a SONAME defined (readealf -d $so | grep SONAME)
# - All the PCI card drivers require the base client, the rest not
# - The group hsmusers is created here and set on PCI card udev rules

# Todo:
# - snmp package
# - cloud-plugin-linux64-x86 ?
# - safenet-softtoken_client ?
# - rbs/rbs_processor2 package

%global hsmusers_group hsmusers
%global	debug_package %{nil}

Name:           luna
Epoch:          1
Version:        10.3.0
Release:        5%{?dist}
Summary:        Linux Client Software for Thales Luna HSMs
License:        Thales Luna HSM License Agreement
URL:            https://cpl.thalesgroup.com/encryption/hardware-security-modules/general-purpose-hsms

ExclusiveArch:  x86_64

Source0:        %{name}-%{version}.tar.xz
Source1:        %{name}-tarball.sh
Source2:        %{name}-pedserver.service
Source3:        %{name}-pedserver.xml
Source4:        %{name}-pedclient.service

Patch0:         %{name}-config-paths.patch

BuildRequires:  firewalld-filesystem
BuildRequires:  javapackages-tools
BuildRequires:  systemd-devel

Provides:       ckdemo == %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      ckdemo < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       cklog == %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      cklog < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       configurator == %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      configurator < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       FM_TOOLS_PCI_CLIENT == %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      FM_TOOLS_PCI_CLIENT < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       FM_TOOLS_SA_CLIENT == %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      FM_TOOLS_SA_CLIENT < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       hsmrecover == %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      hsmrecover < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       libcryptoki == %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      libcryptoki < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       libshim == %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      libshim < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       lunacm == %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      lunacm < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       lunacmu == %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      lunacmu < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       lunadiag == %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      lunadiag < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       lunareset == %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      lunareset < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       multitoken == %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      multitoken < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       salogin == %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      salogin < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       vtl == %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      vtl < %{?epoch:%{epoch}:}%{version}-%{release}

%description
Linux Client Software for Thales Luna HSM 7.7.0 for Network HSM and PCI-e HSM
release. Includes Client Software, Drivers, Remote PED And Backup HSM.

%package        devel
Summary:        Header files and development libraries for %{name}
Requires:       %{name}%{?_isa} == %{version}-%{release}
Provides:       FMSDK == %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      FMSDK < %{?epoch:%{epoch}:}%{version}-%{release}

%description    devel
This package contains headers and static libraries to develop software that uses
the Luna Client software, including the FM SDK.

%package        java
Summary:        Java components for the Luna Client
Requires:       javapackages-filesystem
Provides:       lunajcprovapi == %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      lunajcprovapi < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       lunajcprovjava == %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      lunajcprovjava < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       lunajmt == %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      lunajmt < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       lunajspapi == %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      lunajspapi < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       lunajspjava == %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      lunajspjava < %{?epoch:%{epoch}:}%{version}-%{release}

%description    java
Luna Java Service Provider C++, JCPROV JNI Library and JSP jMultitoken to test
the performance of the Luna Java Service Provider.

%package        javadoc
Summary:        Javadoc for the Java Luna Client components.
BuildArch:      noarch
Requires:       javapackages-filesystem
Provides:       lunajcprovdocs == %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      lunajcprovdocs < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       lunajspdocs == %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      lunajspdocs < %{?epoch:%{epoch}:}%{version}-%{release}

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
Provides:       PedServer == %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      PedServer < %{?epoch:%{epoch}:}%{version}-%{release}

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
Provides:       pedClient == %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      pedClient < %{?epoch:%{epoch}:}%{version}-%{release}

%description    pedclient
The PED Client program - embedded in the case of a Luna appliance, or installed
on a computer with a contained Luna K-card HSM or with a USB-connected Luna G5
(or Backup) HSM - anchors the HSM end of the Remote PED service and initiates
the contact with a PedServer instance, on behalf of its HSM.

%package        samples
Summary:        Luna Client code samples
BuildArch:      noarch
Requires:       %{name}-devel%{?_isa} == %{version}-%{release}
Provides:       ckSample == %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      ckSample < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       lunajcprovsamples == %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      lunajcprovsamples < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       lunajspsamples == %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      lunajspsamples < %{?epoch:%{epoch}:}%{version}-%{release}

%description samples
Examples that use the Luna Client Software:
- SafeNet PKCS 11
- ProtectToolkit Functionality
- Luna Java Service Provider
- Luna JCPROV

%prep
%autosetup -p1 -n %{name}-%{version}

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
mv %{buildroot}%{_bindir}/openssl.cnf %{buildroot}%{_sysconfdir}/

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
mkdir -p %{buildroot}%{_var}/log/luna

# Compatibility symlinks
mkdir -p %{buildroot}%{_sysconfdir}/lunaclient
mkdir -p %{buildroot}%{_prefix}/safenet
ln -sf %{_sysconfdir}/lunaclient %{buildroot}%{_prefix}/safenet/lunaclient
ln -sf %{_libdir} %{buildroot}%{_sysconfdir}/lunaclient/lib
ln -sf %{_bindir} %{buildroot}%{_sysconfdir}/lunaclient/bin

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
%{_var}/log/luna

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
%config %attr(644,root,root) %{_sysconfdir}/openssl.cnf

%files pedclient
%{_bindir}/pedClient
%{_unitdir}/pedclient.service

%files samples
%doc samples

%changelog
* Fri Feb 12 2021 Simone Caronni <negativo17@gmail.com> - 1:10.3.0-5
- Update configuration files.

* Fri Feb 12 2021 Simone Caronni <negativo17@gmail.com> - 1:10.3.0-4
- Make sure firewalld_reload macro is expanded at buildtime.

* Fri Feb 12 2021 Simone Caronni <negativo17@gmail.com> - 1:10.3.0-3
- Fix systemd units.

* Tue Feb 09 2021 Simone Caronni <negativo17@gmail.com> - 1:10.3.0-2
- Add obsolete/provides.

* Fri Jan 22 2021 Simone Caronni <negativo17@gmail.com> - 10.3.0-1
- First build based on Luna Client 10.3.
