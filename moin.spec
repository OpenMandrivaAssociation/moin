%define	name	moin
%define	version	1.5.6
%define	release	%mkrel 1

Summary:	MoinMoin is a Python clone of WikiWiki
Name:		%name
Version:	%version
Release:	%release
License:	GPL
Group:		Networking/WWW
URL:		http://moinmoin.wikiwikiweb.de/
Source0:	http://dl.sf.net/moin/%{name}-%{version}.tar.gz
Source1:	README.update.urpmi
Source2:	apache2-moin.conf.bz2
Patch0:		moin-1.5.6-multiconfig.patch.bz2
Patch1:		moin-1.5.6-xml_newline.patch.bz2
Patch2:		moin-1.5.6-moin.cgi.patch.bz2
Patch3:		moin-1.5.6-wikiconfig.patch.bz2
BuildArch:	noarch
Requires:	python
Requires:	python-base
BuildRequires:	dos2unix
BuildRequires:	python
BuildRequires:	python-devel

%description
A WikiWikiWeb is a collaborative hypertext environment, with an emphasis on
easy access to and modification of information. MoinMoin is a Python
WikiClone that allows you to easily set up your own wiki, only requiring a
Web server and a Python installation.

%package apache2
Summary:	Installs a MoinMoin WikiWikiWeb at http://localhost/wiki/
Group:		Networking/WWW
Requires:	%name = %version
Requires:	apache2
Obsoletes:	moin-www
Provides:	moin-www

%description apache2
This package installs an up and running MoinMoin WikiWikiWeb reachable at
http://localhost/wiki/. It runs behind Apache 2.0, so make sure Apache is
running.

%prep
%setup -q
%patch0 -p1 -b .multiconfig
# This is required, as patch gets confused by the ^Ms otherwise
dos2unix MoinMoin/formatter/xml_docbook.py
%patch1 -p1 -b .xml_newline
%patch2 -p1 -b .moin_cgi
%patch3 -p1 -b .wikiconfig

%build
python setup.py build 

%install
rm -rf %buildroot
python setup.py install --root="%{buildroot}"

%define mywiki %{_var}/www/moin
install -d %{buildroot}%{mywiki}
install -d %{buildroot}%{mywiki}/cgi-bin
cp -R %{buildroot}%{_datadir}/moin/data %{buildroot}%{mywiki}/data
cp -R %{buildroot}%{_datadir}/moin/underlay %{buildroot}%{mywiki}/underlay
cp %{buildroot}%{_datadir}/moin/config/wikiconfig.py %{buildroot}%{mywiki}
cp -a  %{buildroot}%{_datadir}/moin/server/moin.cgi %{buildroot}%{mywiki}/cgi-bin

rm -f %{buildroot}%{mywiki}/data/intermap.txt
touch %{buildroot}%{mywiki}/data/intermap.txt

cp %SOURCE1 README.update.urpmi

install -d %{buildroot}%{_sysconfdir}/httpd/conf.d
cp %SOURCE2 %{buildroot}%{_sysconfdir}/httpd/conf.d/moin.conf

%clean
rm -rf %buildroot

%post apache2
%{_initrddir}/httpd reload

%postun apache2
%{_initrddir}/httpd reload

%files
%defattr(-,root,root,0755)
%doc README README.update.urpmi docs/CHANGES* docs/INSTALL.html docs/README.migration
%doc docs/licenses/
%{_bindir}/moin
%py_puresitedir/MoinMoin/
%py_puresitedir/moin-%{version}-py?.?.egg-info
%{_datadir}/moin/
# just to make rpmlint happier:
%defattr(0755,root,root)
%py_puresitedir/MoinMoin/i18n/check_i18n.py
%py_puresitedir/MoinMoin/i18n/mail_i18n-maintainers.py
%py_puresitedir/MoinMoin/i18n/po2wiki.py
%py_puresitedir/MoinMoin/i18n/prepend.py
%py_puresitedir/MoinMoin/i18n/recode.py
%py_puresitedir/MoinMoin/i18n/wiki2po.py
%py_puresitedir/MoinMoin/script/moin.py
%py_puresitedir/MoinMoin/script/old/migration/12_to_13_mig01.py
%py_puresitedir/MoinMoin/script/old/migration/12_to_13_mig02.py
%py_puresitedir/MoinMoin/script/old/migration/12_to_13_mig03.py
%py_puresitedir/MoinMoin/script/old/migration/12_to_13_mig04.py
%py_puresitedir/MoinMoin/script/old/migration/12_to_13_mig05.py
%py_puresitedir/MoinMoin/script/old/migration/12_to_13_mig06.py
%py_puresitedir/MoinMoin/script/old/migration/12_to_13_mig07.py
%py_puresitedir/MoinMoin/script/old/migration/12_to_13_mig08.py
%py_puresitedir/MoinMoin/script/old/migration/12_to_13_mig09.py
%py_puresitedir/MoinMoin/script/old/migration/12_to_13_mig10.py
%py_puresitedir/MoinMoin/script/old/migration/12_to_13_mig11.py
%py_puresitedir/MoinMoin/script/old/migration/152_to_1050300.py
%py_puresitedir/MoinMoin/script/old/print_stats.py
%py_puresitedir/MoinMoin/script/old/repair_language.py
%py_puresitedir/MoinMoin/script/old/xmlrpc-tools/getmasterpages2.py
%py_puresitedir/MoinMoin/script/old/xmlrpc-tools/getsystempages.py
%py_puresitedir/MoinMoin/script/old/xmlrpc-tools/getsystempages2.py
%py_puresitedir/MoinMoin/script/old/xmlrpc-tools/HelloWorld.py
%py_puresitedir/MoinMoin/script/old/xmlrpc-tools/putPageTest.py
%py_puresitedir/MoinMoin/script/old/xmlrpc-tools/UpdateGroupTest.py
%py_puresitedir/MoinMoin/script/old/xmlrpc-tools/WhoAmI.py
%py_puresitedir/MoinMoin/script/old/xmlrpc-tools/wikibackup.py
%py_puresitedir/MoinMoin/script/old/xmlrpc-tools/wikirestore.py
%py_puresitedir/MoinMoin/support/difflib.py
%py_puresitedir/MoinMoin/util/antispam.py
%py_puresitedir/MoinMoin/version.py
%{_datadir}/moin/htdocs/applets/FCKeditor/editor/dialog/fck_spellerpages/spellerpages/server-scripts/spellchecker.pl
%{_datadir}/moin/htdocs/applets/FCKeditor/editor/filemanager/browser/default/connectors/perl/connector.cgi
%{_datadir}/moin/htdocs/applets/FCKeditor/editor/filemanager/browser/default/connectors/py/connector.py
%{_datadir}/moin/htdocs/applets/FCKeditor/_samples/perl/sampleposteddata.cgi
%{_datadir}/moin/htdocs/applets/FCKeditor/_samples/perl/sample01.cgi
%{_datadir}/moin/htdocs/applets/FCKeditor/_samples/perl/sample02.cgi
%{_datadir}/moin/htdocs/applets/FCKeditor/_samples/perl/sample03.cgi
%{_datadir}/moin/htdocs/applets/FCKeditor/_samples/perl/sample04.cgi
%{_datadir}/moin/htdocs/applets/FCKeditor/_samples/py/sampleposteddata.py
%{_datadir}/moin/htdocs/applets/FCKeditor/_samples/py/sample01.py
%{_datadir}/moin/underlay/pages/HelpOnInstalling(2f)ApacheOnLinuxFtp/attachments/explore.py
%{_datadir}/moin/underlay/pages/HelpOnInstalling(2f)BasicInstallation/attachments/pythontest.cgi
%{_datadir}/moin/underlay/pages/HelpOnInstalling(2f)TroubleShooting/attachments/is_python_here.sh
%{_datadir}/moin/underlay/pages/HelpOnInstalling(2f)WikiInstanceCreation/attachments/createinstance.sh
%attr(0644,root,root) %{_datadir}/moin/underlay/pages/SystemPagesSetup/attachments/*.zip

%files apache2
%defattr(0660,apache,apache,0770) 
%{mywiki}
%attr(0550,apache,apache) %{mywiki}/cgi-bin/moin.cgi
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf.d/moin.conf
%attr(0644,root,root) %config(noreplace) %{mywiki}/wikiconfig.py
%attr(0644,root,root) %config(noreplace) %{mywiki}/data/intermap.txt
%defattr(-,root,apache,-)
%{mywiki}/data/plugin
