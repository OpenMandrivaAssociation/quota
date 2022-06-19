%define _disable_lto 1

Summary:	System administration tools for monitoring users' disk usage
Name:		quota
Version:	4.06
Release:	1
License:	BSD and GPLv2+
Group:		System/Configuration/Other
Url:		http://sourceforge.net/projects/linuxquota/
Source0:	http://prdownloads.sourceforge.net/linuxquota/%{name}-%{version}.tar.gz
Source1:	%{name}.rpmlintrc
Source2:	quota_nld.service
Source3:	quota_nld.sysconfig
Patch0:		quota-4.04-warnquota.patch
Patch3:		quota-3.13-wrong-ports.patch
BuildRequires:	gettext
BuildRequires:	openldap-devel
BuildRequires:	tcp_wrappers-devel
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(ext2fs)
BuildRequires:	pkgconfig(libnl-1)
BuildRequires:	pkgconfig(libnl-3.0)
BuildRequires:	pkgconfig(libtirpc)
Requires:	e2fsprogs
Requires:	tcp_wrappers

%description
The quota package contains system administration tools for monitoring and
limiting users' and or groups' disk usage, per filesystem.

Install quota if you want to monitor and/or limit user/group disk usage.

%files -f %{name}.lang
%doc Changelog README.ldap-support README.mailserver
%doc %{_docdir}/quota/quota*
%exclude %{_docdir}/quota/*.c
%exclude %{_docdir}/quota/ldap-scripts
%{_bindir}/*
%exclude %{_bindir}/quota_nld
%exclude %{_bindir}/warnquota
%{_mandir}/man1/*
%{_mandir}/man8/*
%exclude %{_mandir}/man8/quota_nld.8*
%exclude %{_mandir}/man8/warnquota.8*

#----------------------------------------------------------------------------

%package ldap-scripts
Summary:	ldap-scripts for %{name}
Group:		System/Configuration/Other
Requires:	%{name} = %{EVRD}
Conflicts:	%{name} < 4.04-3

%description ldap-scripts
This package contains the ldap scripts for %{name}.

%files ldap-scripts
%{_datadir}/quota/ldap-scripts/*

#----------------------------------------------------------------------------

%package nld
Summary:	quota_nld daemon
Group:		System/Configuration/Other
Conflicts:	quota < 4.01-7

%description nld
Daemon that listens on netlink socket and processes received quota warnings.
Note, that you have to enable the kernel support for sending quota messages
over netlink (in Filesystems->Quota menu). The daemon supports forwarding
warning messages to the system D-Bus (so that desktop manager can display
a dialog) and writing them to the terminal user has last accessed.

%files nld
%config(noreplace) %{_sysconfdir}/sysconfig/quota_nld
%{_unitdir}/quota_nld.service
%attr(0755,root,root) %{_bindir}/quota_nld
%attr(0644,root,root) %{_mandir}/man8/quota_nld.8*

#----------------------------------------------------------------------------

%package warnquota
Summary:	Send e-mail to users over quota
Group:		System/Configuration/Other
Conflicts:	quota < 4.01-7

%description warnquota
Utility that checks disk quota for each local file system and mails a warning
message to those users who have reached their soft limit.  It is typically run
via cron(8).

%files warnquota
%config(noreplace) %{_sysconfdir}/quotagrpadmins
%config(noreplace) %{_sysconfdir}/quotatab
%config(noreplace) %{_sysconfdir}/warnquota.conf
%{_bindir}/warnquota
%{_mandir}/man5/*
%{_mandir}/man8/warnquota.8*

#----------------------------------------------------------------------------

%package devel
Summary:	Development files for %{name}
Group:		Development/Other
Requires:	%{name} = %{EVRD}
Conflicts:	quota < 4.01-6

%description devel
This package contains the development files for %{name}.

%files devel
%doc %{_docdir}/quota/*.c
%dir %{_includedir}/rpcsvc
%{_includedir}/rpcsvc/*
%{_mandir}/man3/*

#----------------------------------------------------------------------------

%prep
%autosetup -p1

#fix typos/mistakes in localized documentation
for pofile in $(find ./po/*.p*)
do
	sed -i 's/editting/editing/' "$pofile"
done

%build
%serverbuild

%configure \
	--enable-ext2direct=yes \
	--enable-ldapmail=yes \
	--enable-netlink=yes \
	--enable-rpcsetquota=yes \
	--enable-strip-binaries=no \
	--enable-rootsbin 
%make_build

%install
install -d %{buildroot}%{_sysconfdir}
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_mandir}/{man1,man2,man3,man8}
install -d %{buildroot}%{_datadir}/%{name}/

%make_install \
             DEF_BIN_MODE=755 \
             DEF_SBIN_MODE=755 \
             DEF_MAN_MODE=644 \
             STRIP=""

install -m644 warnquota.conf -D %{buildroot}%{_sysconfdir}/warnquota.conf

install -p -m644 %{SOURCE1} -D %{buildroot}%{_unitdir}/quota_nld.service
install -p -m644 %{SOURCE2} -D %{buildroot}%{_sysconfdir}/sysconfig/quota_nld

cp -pr ldap-scripts %{buildroot}%{_datadir}/%{name}/

%find_lang %{name}
