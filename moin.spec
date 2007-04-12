%define name    moin
%define version 1.1
%define release %mkrel 3

Summary:	MoinMoin is a WikiWikiWeb clone.
Name:		%name
Version:	%version
Release:	%release
License:	GPL
Group:		Networking/WWW
URL:		http://moin.sourceforge.net/
Source0:	%{name}-%{version}.tar.bz2
Source1:	README.RPM
Source2:	apache2-moin.conf
Source3:	MonthCalendar.py
Source4:	MonthCalendar.css
Source9:	moin_changePage.py
Source11:	IncludePages.py
Source12:	SearchInPagesAndSort.py
Patch1:		moin_config.py.mydefaults.patch
Patch2:		moin.cgi.nowarnings.patch
Patch3:		moinmoin.css.addMonthCalendar.patch
Patch4:		PageEditor.py.alwaysSendEMail.patch
Patch5:		de.py.subjectEncoding.patch
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	python >= 2.2
BuildRequires:	python-devel >= 2.2
#Requires:	python-gdchart

%description
MoinMoin is a WikiWikiWeb clone. A WikiWikiWeb is a collaborative hypertext
environment, with an emphasis on easy access to and modification of
information.

MoinMoin is written in Python and allows you to easily set up your own Wiki,
only requiring a Web server and a Python installation.

This package allows you to run several MoinMoin Wiki instances on one machine.
If you need only one or if you want a template for your Wikis, see the
%{name}-apache2 package.


%package apache2
Summary:	Installs a MoinMoin WikiWikiWeb at http://localhost/wiki/.
Group:		Networking/WWW
Requires:	%name = %version
Requires:	apache2
Requires:	%_bindir/moin-changePage
Obsoletes:	moin-www

%description apache2
This package installs an up and running MoinMoin WikiWikiWeb reachable at
http://localhost/wiki/. It runs behind Apache 2.0, so make sure Apache is
running.


%package apache2-unsafe
Summary:	Additional Macros and Actions for local MoinMoin Wiki
Group:		Networking/WWW
Requires:	%{name}-apache2 = %version

%description apache2-unsafe
This package installs some additional Macros and Actions. Those are not
suited for public installations, either because they can be exploited or
were not yet widely tested. Those include:
 - HTML macro: allows you to use plain HTML code in a wiki page
 - IncludePages macro: incude several pages in one
 - SearchInPagesAndSort macro: search for text and sort results


%prep
%setup -q
cp %SOURCE1 README.RPM
cp %SOURCE3 MoinMoin/macro/MonthCalendar.py
cp %SOURCE4 wiki/htdocs/css/monthcalendar.css
cp %SOURCE9 MoinMoin/scripts/moin_changePage.py
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p0
%patch5 -p0


%build
CFLAGS="%{optflags}" python setup.py build


%install
rm -rf %buildroot
python setup.py install --root="%{buildroot}"

rm %{buildroot}/%_bindir/BasicAuthTransport
rm %{buildroot}/%_bindir/getsystempages
pushd %{buildroot}/%_bindir && rename "" "moin-" get* ; rename "wiki" "moin-" wiki* ; popd

%define mywiki %{_var}/www/moin
install -d %{buildroot}/%{mywiki}
cp -ra %{buildroot}/%{_datadir}/moin/data      %{buildroot}/%{mywiki}/data
cp -a  %{buildroot}/%{_datadir}/moin/cgi-bin/* %{buildroot}/%{mywiki}
rm -f %{buildroot}/%{mywiki}/data/intermap.txt
touch %{buildroot}/%{mywiki}/data/intermap.txt

install -d %{buildroot}/%{_sysconfdir}/httpd/conf.d
cp %SOURCE2 %{buildroot}/%{_sysconfdir}/httpd/conf.d/moin.conf

# unsafe macros
cp %SOURCE11 %SOURCE12 %{buildroot}/%{mywiki}/data/plugin/macro
cp contributions/plugin/macro/HTML.py %{buildroot}/%{mywiki}/data/plugin/macro

%clean
rm -rf %buildroot


%post apache2
%{_initrddir}/httpd reload
echo "updating wiki system pages..."
# process .rpmnew files
cd %{mywiki}/data/text
[ -e *.rpmnew ] && for newfile in *.rpmnew ; do
    file=`echo $newfile | sed 's/.rpmnew$//'`
    echo " - processing page $file (new version)"
    su - apache -c "%_bindir/moin-changePage --base=%{mywiki} \
        --action=edit --page=\"$file\" \
        --content-file=\"%{mywiki}/data/text/$newfile\" \
        --user=\"System\" --comment=\"system upgrade\""
    [ $? -eq 0 ] && rm -f $newfile
done
# process .rpmsave files
[ -e *.rpmsave ] && for delfile in *.rpmsave ; do
    file=`echo $delfile | sed 's/.rpmsave$//'`
    echo " - processing page $file (deleted)"
    su - apache -c "%_bindir/moin-changePage --base=%{mywiki} \
        --action=delete --page=\"$file\" \
        --user=\"System\" --comment=\"system upgrade\""
    [ $? -eq 0 ] && rm -f $delfile
done
# also clear any bad rc value
echo "update done."

%postun apache2
%{_initrddir}/httpd reload


%files
%defattr(0755,root,root,0755)
%{_bindir}/*
%defattr(0644,root,root,0755)
%doc CHANGES COPYING INSTALL.html README README.RPM TODO
%py_puresitedir/MoinMoin
%py_puresitedir/*.egg-info
%{_datadir}/moin


%files apache2
%defattr(0755,root,root,0755)
%{mywiki}/moin.cgi

%defattr(0664,apache,apache,0775)
%dir %{mywiki}
%dir %{mywiki}/data
%dir %{mywiki}/data/backup
%dir %{mywiki}/data/cache
%dir %{mywiki}/data/pages
%dir %{mywiki}/data/user
%config(noreplace) %{mywiki}/data/text

%defattr(0644,root,root,0755)
%dir %{mywiki}/data/plugin
%config(noreplace) %{mywiki}/moin_config.py
%config(noreplace) %{mywiki}/data/intermap.txt
%config(noreplace) %{_sysconfdir}/httpd/conf.d/moin.conf

%defattr(0664,root,apache,0775) 
%dir %{mywiki}/data/plugin/macro
%dir %{mywiki}/data/plugin/action


%files apache2-unsafe
%defattr(0644,root,root,0755)
%{mywiki}/data/plugin/macro/*.py
# %{mywiki}/data/plugin/action/*.py


