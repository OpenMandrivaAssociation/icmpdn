Summary:	ICMP host name utilities
Name:		icmpdn
Version:	0.4
Release:	%mkrel 5
License:	GPL
Group:		System/Servers
URL:		http://www.dolda2000.com/~fredrik/icmp-dn/
Source0:	http://www.dolda2000.com/~fredrik/icmp-dn/%{name}-%{version}.tar.bz2
Source1:	icmpdnd.init.bz2
Source2:	icmpdnd.sysconfig.bz2
Requires(post): rpm-helper
Requires(preun): rpm-helper
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
libtoolize --copy --force; aclocal -I autotools; autoconf; automake

%configure2_5x \
    --libdir=/%{_lib} \
    --sbindir=/sbin \
    --bindir=/bin \
    
%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

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
%if %mdkversion < 200900
/sbin/ldconfig
%endif

%preun
%_preun_service icmpdnd

%if %mdkversion < 200900
%postun -p /sbin/ldconfig
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

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

