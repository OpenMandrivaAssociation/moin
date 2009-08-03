%define	name	moin
%define	version	1.5.7

Summary:	Python clone of WikiWiki
Name:		%{name}
Version:	%{version}
Release:	%mkrel 1
License:	GPL
Group:		Networking/WWW
URL:		http://moinmoin.wikiwikiweb.de/
Source0:	http://dl.sf.net/moin/%{name}-%{version}.tar.gz
Source1:	README.RPM
Source2:	apache2-moin.conf
Patch0:		moin-1.5.6-multiconfig.patch
Patch1:		moin-1.5.6-xml_newline.patch
Patch2:		moin-1.5.7-python-2.6.patch
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
Requires:	apache-conf
Requires:	python
Requires:	python-base
BuildRequires:	python
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
%patch0 -p1 -b .multiconfig
%patch1 -p1 -b .xml_newline
%patch2 -p1

%build
%__python setup.py build 

%install
rm -rf %{buildroot}
%__python setup.py install --root=%{buildroot} --record=INSTALLED_FILES

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

%files -f INSTALLED_FILES
%defattr(-,root,root)
%doc README README.update.urpmi docs/CHANGES* docs/INSTALL.html docs/README.migration
%doc docs/licenses/
%{_bindir}/moin
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf.d/moin.conf
