Summary:	ICMP host name utilities
Name:		icmpdn
Version:	0.4
Release:	1
License:	GPL
Group:		System/Servers
URL:		http://www.dolda2000.com/~fredrik/icmp-dn/
Source0:	http://www.dolda2000.com/~fredrik/icmp-dn/%{name}-%{version}.tar.bz2
Source1:	icmpdnd.init.bz2
Source2:	icmpdnd.sysconfig.bz2
Requires(post): rpm-helper
Requires(preun): rpm-helper

%description
Since the Linux kernel does not support the ICMP host name
facilities as described in RFC 1788, I wrote a simple
implementation in user-space. It comprises three parts: 

 o icmpdnd - The ICMP Domain Name daemon, which listens to ICMP
   domain name requests and replies to them.
 o idnlookup - A user utility to query a host for its host name
   over ICMP. Like ping and all other utilities that use ICMP, it
   needs to be installed SUID root.
 o libnss_icmp.so.2 - A glibc NSS module, which uses idnlookup to
   perform queries for the gethostbyaddr function.


The NSS module caches all requests (including failures) and honors
the TTL value sent by the responding host. It uses a configuration
file called /etc/nss-icmp.conf, which controls different aspects
of its operation:

%prep

%setup -q -n %{name}-%{version}

mkdir -p Mandriva
bzcat %{SOURCE1} > Mandriva/icmpdnd.init
bzcat %{SOURCE2} > Mandriva/icmpdnd.sysconfig

%build
rm -f configure
export CPPFLAGS="-D_GNU_SOURCE"
libtoolize --copy --force; aclocal -I autotools; autoconf; automake

%configure2_5x \
    --libdir=/%{_lib} \
    --sbindir=/sbin \
    --bindir=/bin \
    
%make

%install

%makeinstall_std

install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_sysconfdir}/sysconfig

install -m0755 Mandriva/icmpdnd.init %{buildroot}%{_initrddir}/icmpdnd
install -m0644 Mandriva/icmpdnd.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/icmpdnd

# cleanup
rm -rf %{buildroot}%{_sysconfdir}/init.d
rm -f %{buildroot}/%{_lib}/libnss_icmp.la

%post
%_post_service icmpdnd
/sbin/ldconfig

%preun
%_preun_service icmpdnd
/sbin/ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog README
%attr(0755,root,root) %{_initrddir}/icmpdnd
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/icmpdnd
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/nss-icmp.conf
%attr(0755,root,root) /%{_lib}/libnss_icmp.so*
%attr(0755,root,root) /sbin/icmpdnd
%attr(4755,root,root) /bin/idnlookup
%{_mandir}/man*/*



%changelog
* Wed Jan 02 2008 Olivier Blin <oblin@mandriva.com> 0.4-1mdv2008.1
+ Revision: 140756
- restore BuildRoot

  + Thierry Vignaud <tvignaud@mandriva.com>
    - kill re-definition of %%buildroot on Pixel's request


* Fri Jul 14 2006 Oden Eriksson <oeriksson@mandriva.com> 0.4-1mdv2007.0
- 0.4

* Mon Jun 27 2005 Oden Eriksson <oeriksson@mandriva.com> 0.3-1mdk
- 0.3 (Minor feature enhancements)

* Mon May 23 2005 Oden Eriksson <oeriksson@mandriva.com> 0.1-1mdk
- icmp-dn/icmpdn
- use the official tar ball
- no more sub packages

* Sun May 22 2005 Oden Eriksson <oeriksson@mandriva.com> 0.1-1mdk
- initial Mandriva package

