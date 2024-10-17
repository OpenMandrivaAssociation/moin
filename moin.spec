%define	name	moin
%define	version	1.9.3

Summary:	Python clone of WikiWiki
Name:		%{name}
Version:	%{version}
Release:	3
License:	GPLv2
Group:		Networking/WWW
URL:		https://moinmo.in/
Source0:	http://static.moinmo.in/files/%{name}-%{version}.tar.gz
Source1:	README.RPM
Source2:	apache2-moin.conf
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
Requires:	apache-conf
Requires:	python
BuildRequires:	python-devel
Obsoletes:	moin-apache2 <= 1.1
Obsoletes:	moin-apache2-unsafe <= 1.1

%description
A WikiWikiWeb is a collaborative hypertext environment, with an emphasis on
easy access to and modification of information. MoinMoin is a Python
WikiClone that allows you to easily set up your own wiki, only requiring a
Web server and a Python installation.

%prep
%setup -q

%build
%__python setup.py build 

%install
rm -rf %{buildroot}
%__python setup.py install --root=%{buildroot}

cp %SOURCE1 README.update.urpmi

install -d %{buildroot}%{_sysconfdir}/httpd/conf.d
cp %SOURCE2 %{buildroot}%{_sysconfdir}/httpd/conf.d/moin.conf

# ensure "templates" are readable
chmod a+r -R %{buildroot}%{_datadir}

%clean
rm -rf %{buildroot}

%post
%{_initrddir}/httpd reload

%postun
%{_initrddir}/httpd reload

%files 
%defattr(-,root,root)
%doc README README.update.urpmi docs/CHANGES* docs/INSTALL.html docs/README.migration
%doc docs/licenses/
%{_bindir}/moin
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf.d/moin.conf
%_datadir/%name/
%py_puresitedir/jabberbot
%py_puresitedir/MoinMoin
%py_puresitedir/*.egg-info


%changelog
* Fri Nov 19 2010 Funda Wang <fwang@mandriva.org> 1.9.3-2mdv2011.0
+ Revision: 598859
- rebuild

* Fri Aug 06 2010 Michael Scherer <misc@mandriva.org> 1.9.3-1mdv2011.0
+ Revision: 566512
- fix file list
- clean requires and BuildRequires
- fix License
- update to 1.9.3

* Sat Jan 23 2010 Frederik Himpe <fhimpe@mandriva.org> 1.9.1-1mdv2010.1
+ Revision: 495331
- Update to new version 1.9.1
- Remove old patches which are not necessary anymore
  (xml_newline and python 2.6)
- Remove multiconfig patch and use default configuration

* Tue Aug 04 2009 Paulo Andrade <pcpa@mandriva.com.br> 1.5.7-1mdv2010.0
+ Revision: 408630
- Update to version 1.5.7.
  Rebuild with python 2.6.

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - rebuild
    - rebuild
    - fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake
    - kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Funda Wang <fwang@mandriva.org>
    - New upstream version 1.5.6


* Fri Dec 15 2006 Nicolas Lécureuil <neoclust@mandriva.org> 1.1-3mdv2007.0
+ Revision: 97500
- Fix file list
- Rebuild against new python
- Import moin

* Sat Dec 04 2004 Michael Scherer <misc@mandrake.org> 1.1-2mdk
- Rebuild for new python

* Sun Jan 11 2004 Michael Reinsch <mr@uue.org> 1.1-1mdk
- release 1.1, rediffed patches
- cleanup in /usr/bin: all moin utils are called moin-* now
- added apache2-unsafe package which brings some additional macros
- handle .rpmnew/.rpmsave files in wiki

* Sun Jan 11 2004 Marcel Pol <mpol@mandrake.org> 1.1-0.cvs20030824.4mdk
- own dir (distlint)

