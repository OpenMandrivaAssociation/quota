%define name	quota
%define version	3.14

Summary:	System administration tools for monitoring users' disk usage
Name:		%{name}
Version:	%{version}
Release:	%mkrel 3
URL:		http://sourceforge.net/projects/linuxquota/
License:	BSD
Group:		System/Configuration/Other
Source0:	http://prdownloads.sourceforge.net/linuxquota/%{name}-%{version}.tar.bz2
Source1:	%{name}.bash-completion
Patch0:		quota-tools-man-pages-path.patch
Patch1:		quota-tools-no-stripping.patch
Patch3:		quota-tools-default-conf.patch
Patch5:		quota-3.06-pie.patch
BuildRequires:	e2fsprogs-devel
BuildRequires:	gettext
Requires:	initscripts >= 6.38
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The quota package contains system administration tools for monitoring
and limiting users' and or groups' disk usage, per filesystem.

Install quota if you want to monitor and/or limit user/group disk
usage.

%prep
%setup -q -n quota-tools
%patch0 -p1 -b .man-pages
%patch1 -p1 -b .no-stripping
%patch3 -p1 -b .default-conf
%ifnarch ppc ppc64
%patch5 -p1 -b .pie
%endif

%build
%configure --with-ext2direct=no --enable-rootsbin
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
             DEF_MAN_MODE=644

install -m 644 warnquota.conf %{buildroot}%{_sysconfdir}

%find_lang %{name}

# bash completion
install -d -m 755 %{buildroot}%{_sysconfdir}/bash_completion.d
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/bash_completion.d/%{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%{_sysconfdir}/bash_completion.d/%{name}
%config(noreplace) %{_sysconfdir}/warnquota.conf
%config(noreplace) %{_sysconfdir}/quotagrpadmins
%config(noreplace) %{_sysconfdir}/quotatab
/sbin/*
%{_bindir}/*
%{_sbindir}/*
%{_includedir}/rpcsvc/*
%{_mandir}/man?/*


