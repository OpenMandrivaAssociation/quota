Summary:	System administration tools for monitoring users' disk usage
Name:		quota
Version:	3.17
Release:	%mkrel 7
License:	BSD and GPLv2+
Group:		System/Configuration/Other
URL:		http://sourceforge.net/projects/linuxquota/
Source0:	http://prdownloads.sourceforge.net/linuxquota/%{name}-%{version}.tar.gz
Patch0:		quota-3.06-warnquota.patch
Patch1:		quota-3.17-no-stripping.patch
Patch2:		quota-3.06-man-page.patch
Patch3:		quota-3.06-pie.patch
Patch4:		quota-3.13-wrong-ports.patch
Patch5:		quota-3.16-helpoption.patch
Patch6:		quota-3.16-quotaoffhelp.patch
Patch50:	quota-tools-default-conf.patch
BuildRequires:	e2fsprogs-devel
BuildRequires:	gettext
BuildRequires:	tcp_wrappers-devel
Requires:	e2fsprogs
Requires:	initscripts >= 6.38
Requires:	tcp_wrappers
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The quota package contains system administration tools for monitoring and
limiting users' and or groups' disk usage, per filesystem.

Install quota if you want to monitor and/or limit user/group disk usage.

%prep

%setup -q -n quota-tools
%patch0 -p1
%patch1 -p1
%patch2 -p1
%ifnarch ppc ppc64
%patch3 -p1
%endif
%patch4 -p1
%patch5 -p1
%patch6 -p1

%patch50 -p1 -b .default-conf

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
    --enable-rootsbin 

%make

%install
rm -rf %{buildroot}

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

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc Changelog README.ldap-support README.mailserver ldap-scripts
%config(noreplace) %{_sysconfdir}/warnquota.conf
%config(noreplace) %{_sysconfdir}/quotagrpadmins
%config(noreplace) %{_sysconfdir}/quotatab
/sbin/*
%{_bindir}/*
%{_sbindir}/*
%{_includedir}/rpcsvc/*
%{_mandir}/man?/*
