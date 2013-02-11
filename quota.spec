Summary:	System administration tools for monitoring users' disk usage
Name:		quota
Version:	4.01
Release:	1
License:	BSD and GPLv2+
Group:		System/Configuration/Other
URL:		http://sourceforge.net/projects/linuxquota/
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
BuildRequires:	pkgconfig(ext2fs)
BuildRequires:	gettext
BuildRequires:	tcp_wrappers-devel
BuildRequires:	pkgconfig(libtirpc)
BuildRequires:	pkgconfig(libnl-3.0)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	openldap-devel
Requires:	e2fsprogs
Requires:	initscripts >= 6.38
Requires:	tcp_wrappers

%description
The quota package contains system administration tools for monitoring and
limiting users' and or groups' disk usage, per filesystem.

Install quota if you want to monitor and/or limit user/group disk usage.

%prep
%setup -q -n quota-tools
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
    --enable-strip-binaries=no
make
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
%{_includedir}/rpcsvc/*
%{_mandir}/man?/*


%changelog
* Sun Feb 10 2013 Per Øyvind Karlsen <peroyvind@mandriva.org> 3.17-11
- sync patches from fedora
- cosmetics
- add buildrequires on pkgconfig(libtirpc)

* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 3.17-7mdv2011.0
+ Revision: 669393
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 3.17-6mdv2011.0
+ Revision: 607266
- rebuild

* Mon Mar 15 2010 Oden Eriksson <oeriksson@mandriva.com> 3.17-4mdv2010.1
+ Revision: 520206
- rebuilt for 2010.1

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 3.17-3mdv2010.0
+ Revision: 426841
- rebuild

* Wed Feb 04 2009 Guillaume Rousse <guillomovitch@mandriva.org> 3.17-2mdv2009.1
+ Revision: 337607
- new release
- sync patch set with fedora
- keep bash completion in its own package
- rediff patch 1 (stripping)
- drop partches 5, 7 and 10, merged upstream

* Mon Dec 22 2008 Oden Eriksson <oeriksson@mandriva.com> 3.16-4mdv2009.1
+ Revision: 317559
- sync with quota-3.16-8.fc11.src.rpm

* Thu Sep 11 2008 Oden Eriksson <oeriksson@mandriva.com> 3.16-3mdv2009.0
+ Revision: 283788
- sync with quota-3.16-4.fc10.src.rpm

* Thu Aug 07 2008 Thierry Vignaud <tv@mandriva.org> 3.16-2mdv2009.0
+ Revision: 265615
- rebuild early 2009.0 package (before pixel changes)

* Tue Apr 15 2008 Guillaume Rousse <guillomovitch@mandriva.org> 3.16-1mdv2009.0
+ Revision: 194365
- new version
  drop patch 5 (merged upstream)
  drop patch 1 (makefile arg is enough)

* Thu Mar 06 2008 Oden Eriksson <oeriksson@mandriva.com> 3.15-1mdv2008.1
+ Revision: 180933
- sync with fc9

* Tue Jan 15 2008 Thierry Vignaud <tv@mandriva.org> 3.14-3mdv2008.1
+ Revision: 152810
- remove useless kernel require
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot


* Sun Jan 14 2007 Guillaume Rousse <guillomovitch@mandriva.org> 3.14-2mdv2007.0
+ Revision: 108839
- spec cleanup
- drop unused patches
- add bash completion

* Mon Dec 11 2006 Emmanuel Andry <eandry@mandriva.org> 3.14-1mdv2007.1
+ Revision: 94583
- New version 3.14
  bunzip patches
  drop patch 2
- Import quota

* Thu Jan 05 2006 Stefan van der Eijk <stefan@eijk.nu> 3.13-2mdk
- rebuild

* Wed Aug 10 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 3.13-1mdk
- 3.13
- fix summary-ended-with-dot
- %%mkrel

* Thu Nov 11 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 3.12-1mdk
- 3.12
- sync with fedora

* Sun Aug 08 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 3.10-1mdk
- 3.10
- synced with fedora
- misc spec file fixes

