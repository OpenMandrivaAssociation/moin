%define	name	moin
%define	version	1.9.3

Summary:	Python clone of WikiWiki
Name:		%{name}
Version:	%{version}
Release:	%mkrel 1
License:	GPLv2
Group:		Networking/WWW
URL:		http://moinmo.in/
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
