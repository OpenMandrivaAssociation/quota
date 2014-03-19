Summary:	System administration tools for monitoring users' disk usage
Name:		quota
Version:	4.01
Release:	6
License:	BSD and GPLv2+
Group:		System/Configuration/Other
Url:		http://sourceforge.net/projects/linuxquota/
Source0:	http://prdownloads.sourceforge.net/linuxquota/%{name}-%{version}.tar.gz
Patch0:		quota-4.01-warnquota.patch
Patch2:		quota-3.06-man-page.patch
Patch3:		quota-3.06-pie.patch
Patch4:		quota-3.13-wrong-ports.patch
# Submitted to upstream, SF#3571486
Patch7:		quota-4.01-Make-group-warning-message-more-official.patch
# In upstream after 4.01, SF#3571589
Patch8:		quota-4.01-define_charset_in_mail.patch
# In upstream after 4.01, SF#3602786, bug #846296
Patch9:		quota-4.01-Do-not-fiddle-with-quota-files-on-XFS-and-GFS.patch
# In upstream after 4.01, SF#3602777
Patch10:	quota-4.01-quotacheck-Make-sure-d-provides-at-least-as-much-inf.patch
Patch11:	quota-4.01-libtirpc.patch
BuildRequires:	gettext
BuildRequires:	openldap-devel
BuildRequires:	tcp_wrappers-devel
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(ext2fs)
BuildRequires:	pkgconfig(libnl-1)
BuildRequires:	pkgconfig(libtirpc)
Requires:	e2fsprogs
Requires:	initscripts >= 6.38
Requires:	tcp_wrappers

%description
The quota package contains system administration tools for monitoring and
limiting users' and or groups' disk usage, per filesystem.

Install quota if you want to monitor and/or limit user/group disk usage.

%package devel
Summary:	Development files for %{name}
Group:		Development/Other
Requires:	%{name} = %{version}-%{release}
Conflicts:	%{name} < 4.01-6

%description devel
This package contains the development files for %{name}.

%prep
%setup -qn quota-tools
%patch0 -p1
%patch2 -p1
%ifnarch ppc ppc64
%patch3 -p1
%endif
%patch4 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1 -b .tirpc~

#fix typos/mistakes in localized documentation
for pofile in $(find ./po/*.p*)
do
   sed -i 's/editting/editing/' "$pofile"
done

%build
%serverbuild

%configure2_5x \
	--enable-ldapmail=try \
	--with-ext2direct=no \
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

make install ROOTDIR=%{buildroot} \
             DEF_BIN_MODE=755 \
             DEF_SBIN_MODE=755 \
             DEF_MAN_MODE=644 \
             STRIP=""

install -m0644 warnquota.conf %{buildroot}%{_sysconfdir}

# we don't support XFS yet
rm -f %{buildroot}%{_sbindir}/quot
rm -f %{buildroot}%{_sbindir}/xqmstats
rm -f %{buildroot}%{_mandir}/man8/quot.*
rm -f %{buildroot}%{_mandir}/man8/xqmstats.*

%find_lang %{name}

%files -f %{name}.lang
%doc Changelog README.ldap-support README.mailserver ldap-scripts
%config(noreplace) %{_sysconfdir}/warnquota.conf
%config(noreplace) %{_sysconfdir}/quotagrpadmins
%config(noreplace) %{_sysconfdir}/quotatab
/sbin/*
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/man1/*
%{_mandir}/man8/*

%files devel
%dir %{_includedir}/rpcsvc
%{_includedir}/rpcsvc/*
%{_mandir}/man3/*

