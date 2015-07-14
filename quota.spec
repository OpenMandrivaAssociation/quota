%bcond_with	uclibc

Summary:	System administration tools for monitoring users' disk usage
Name:		quota
Version:	4.01
Release:	12
License:	BSD and GPLv2+
Group:		System/Configuration/Other
Url:		http://sourceforge.net/projects/linuxquota/
Source0:	http://prdownloads.sourceforge.net/linuxquota/%{name}-%{version}.tar.gz
Source1:	%{name}.rpmlintrc
Source2:	quota_nld.service
Source3:	quota_nld.sysconfig
Patch0:		quota-4.01-warnquota.patch
Patch1:		quota-3.06-man-page.patch
Patch2:		quota-3.06-pie.patch
Patch3:		quota-3.13-wrong-ports.patch
# Submitted to upstream, SF#3571486
Patch4:		quota-4.01-Make-group-warning-message-more-official.patch
# In upstream after 4.01, SF#3571589
Patch5:		quota-4.01-define_charset_in_mail.patch
# In upstream after 4.01, SF#3602786, bug #846296
Patch6:		quota-4.01-Do-not-fiddle-with-quota-files-on-XFS-and-GFS.patch
# In upstream after 4.01, SF#3602777
Patch7:		quota-4.01-quotacheck-Make-sure-d-provides-at-least-as-much-inf.patch
# In upstream after 4.01, SF#3607034
Patch8:		quota-4.01-Add-quotasync-1-manual-page.patch
# In upstream after 4.01, SF#3607034
Patch9:		quota-4.01-Complete-quotasync-usage.patch
# In upstream after 4.01, SF#3607034
Patch10:	quota-4.01-Correct-quotasync-exit-code.patch
# In upstream after 4.01, SF#3607038
Patch11:	quota-4.01-Fix-various-usage-mistakes.patch
# In upstream after 4.01, SF#3600120
Patch12:	quota-4.01-Recognize-units-at-block-limits-by-setquota.patch
# In upstream after 4.01, SF#3600120
Patch13:	quota-4.01-Recognize-block-limit-units-on-setquota-standard-inp.patch
# In upstream after 4.01, SF#3600120
Patch14:	quota-4.01-Recognize-units-at-block-limits-by-edquota.patch
# In upstream after 4.01, SF#3600120
Patch15:	quota-4.01-Recognize-units-at-inode-limits-by-setquota.patch
# In upstream after 4.01, SF#3600120
Patch16:	quota-4.01-Recognize-units-at-inode-limits-by-edquota.patch
# In upstream after 4.01
Patch17:	quota-4.01-Close-FILE-handles-on-error.patch
# In upstream after 4.01
Patch18:	quota-4.01-Remove-installation-of-manpages-into-section-2.patch
# In upstream after 4.01, <https://sourceforge.net/p/linuxquota/patches/39/>
Patch19:	quota-4.01-Add-quotagrpadmins-5-manual-page.patch
# In upstream after 4.01, <https://sourceforge.net/p/linuxquota/patches/39/>
Patch20:	quota-4.01-Add-quotatab-5-manual-page.patch
# In upstream after 4.01, <https://sourceforge.net/p/linuxquota/patches/39/>
Patch21:	quota-4.01-Add-warnquota.conf-5-manual-page.patch
# In upstream after 4.01, <https://sourceforge.net/p/linuxquota/patches/39/>
Patch22:	quota-4.01-Improve-rcp.rquota-8-manual-page.patch
# In upstream after 4.01, <https://sourceforge.net/p/linuxquota/bugs/115/>,
# bug #1072769
Patch23:	quota-4.01-Prevent-from-grace-period-overflow-in-RPC-transport.patch

Patch111:	quota-4.01-libtirpc.patch
BuildRequires:	gettext
BuildRequires:	openldap-devel
BuildRequires:	tcp_wrappers-devel
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(ext2fs)
BuildRequires:	pkgconfig(libnl-1)
BuildRequires:	pkgconfig(libnl-3.0)
BuildRequires:	pkgconfig(libtirpc)
%if %{with uclibc}
BuildRequires:	uClibc-devel 
%endif
Requires:	e2fsprogs
Requires:	initscripts
Requires:	tcp_wrappers

%description
The quota package contains system administration tools for monitoring and
limiting users' and or groups' disk usage, per filesystem.

Install quota if you want to monitor and/or limit user/group disk usage.

%files -f %{name}.lang
%doc Changelog README.ldap-support README.mailserver ldap-scripts
/sbin/*
%{_bindir}/*
%{_sbindir}/*
%exclude %{_sbindir}/quota_nld
%exclude %{_sbindir}/warnquota
%{_mandir}/man1/*
%{_mandir}/man8/*
%exclude %{_mandir}/man8/quota_nld.8*
%exclude %{_mandir}/man8/warnquota.8*

#----------------------------------------------------------------------------

%if %{with uclibc}
%package -n uclibc-%{name}
Summary:	uClibc build of quota tools
Group:		System/Configuration/Other

%description -n uclibc-%{name}
The quota package contains system administration tools for monitoring and
limiting users' and or groups' disk usage, per filesystem.

Install quota if you want to monitor and/or limit user/group disk usage.

%files -n uclibc-%{name}
%{uclibc_root}/sbin/*
%{uclibc_root}%{_bindir}/*
%{uclibc_root}%{_sbindir}/*
%endif

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
%attr(0755,root,root) %{_sbindir}/quota_nld
%attr(0644,root,root) %{_mandir}/man8/quota_nld.8*
%doc Changelog

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
%{_sbindir}/warnquota
%{_mandir}/man5/*
%{_mandir}/man8/warnquota.8*
%doc Changelog README.ldap-support README.mailserver

#----------------------------------------------------------------------------

%package devel
Summary:	Development files for %{name}
Group:		Development/Other
Requires:	%{name} = %{EVRD}
Conflicts:	quota < 4.01-6

%description devel
This package contains the development files for %{name}.

%files devel
%dir %{_includedir}/rpcsvc
%{_includedir}/rpcsvc/*
%{_mandir}/man3/*

#----------------------------------------------------------------------------

%prep
%setup -qn quota-tools
%patch0 -p1
%patch1 -p1
%ifnarch ppc ppc64
%patch2 -p1
%endif
%patch3 -p1
%patch4 -p1 -b .group_warning
%patch5 -p1 -b .charset_in_mail
%patch6 -p1 -b .gfs_files
%patch7 -p1 -b .quotackeck_debug
%patch8 -p1 -b .quotasync_manual
%patch9 -p1 -b .quotasync_usage
%patch10 -p1 -b .quotasync_exit
%patch11 -p1 -b .usage
%patch12 -p1 -b .setquota_block_units
%patch13 -p1 -b .setquota_block_units_stdin
%patch14 -p1 -b .edquota_block_units
%patch15 -p1 -b .setquota_inode_units
%patch16 -p1 -b .edquota_inode_units
%patch17 -p1 -b .close_file_handles
%patch18 -p1 -b .remove_man2
%patch19 -p1 -b .doc_quotagrpadmins
%patch20 -p1 -b .doc_quotatab
%patch21 -p1 -b .doc_warnquota
%patch22 -p1 -b .doc_rquota
%patch23 -p1 -b .rpc_time

%patch111 -p1 -b .tirpc~

#fix typos/mistakes in localized documentation
for pofile in $(find ./po/*.p*)
do
   sed -i 's/editting/editing/' "$pofile"
done

%if %{with uclibc}
mkdir -p .uclibc
cp -a * .uclibc
%endif

%build
%serverbuild

%if %{with uclibc}
mkdir -p .uclibc
pushd .uclibc
%uclibc_configure \
	--enable-ext2direct=yes \
	--enable-ldapmail=no \
	--enable-netlink=no \
	--enable-rootsbin=yes \
	--enable-rpcsetquota=yes \
	--enable-strip-binaries=no \
	--enable-rootsbin 
%make CC="%{uclibc_cc}" RPCLIB=""
popd
%endif

%configure \
	--enable-ext2direct=yes \
	--enable-ldapmail=yes \
	--enable-netlink=yes \
	--enable-rootsbin=yes \
	--enable-rpcsetquota=yes \
	--enable-strip-binaries=no \
	--enable-rootsbin 
%make

%install
install -d %{buildroot}/sbin
install -d %{buildroot}%{_sysconfdir}
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_mandir}/{man1,man2,man3,man8}

%if %{with uclibc}
make -C .uclibc install ROOTDIR=%{buildroot} \
             DEF_BIN_MODE=755 \
             DEF_SBIN_MODE=755 \
             DEF_MAN_MODE=644 \
             STRIP=""
mv %{buildroot}/sbin %{buildroot}%{uclibc_root}
rm -r %{buildroot}%{uclibc_root}%{_includedir}
rm -rf %{buildroot}%{uclibc_root}%{_localedir}
%endif

make install ROOTDIR=%{buildroot} \
             DEF_BIN_MODE=755 \
             DEF_SBIN_MODE=755 \
             DEF_MAN_MODE=644 \
             STRIP=""

install -m644 warnquota.conf -D %{buildroot}%{_sysconfdir}/warnquota.conf

install -p -m644 %{SOURCE1} -D %{buildroot}%{_unitdir}/quota_nld.service
install -p -m644 %{SOURCE2} -D %{buildroot}%{_sysconfdir}/sysconfig/quota_nld

%find_lang %{name}

