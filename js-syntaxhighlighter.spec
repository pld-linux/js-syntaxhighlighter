%bcond_with	test	# install test.html
Summary:	JavaScript syntax highlighter
Summary(pl.UTF-8):	Podświetlacz składni napisany w JavaScript
Name:		js-syntaxhighlighter
Version:	2.1.364
Release:	1
License:	LGPL v3
Group:		Applications/WWW
# Use distfile or sth, cause DF does not like question mark in URL.
# http://alexgorbatchev.com/downloads/grab.php?name=sh
Source0:	http://execve.pl/PLD/%{name}-%{version}.zip
# Source0-md5:	839d77b07b80e56965ebcfaf2a1186be
URL:		http://alexgorbatchev.com/wiki/SyntaxHighlighter
BuildRequires:	unzip
Requires:	webapps
Requires:	webserver(alias)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		syntaxhighlighter
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
A fully functional self-contained code syntax highlighter developed in
JavaScript.

%description -l pl.UTF-8
W pełni funkcjonalny podświetlacz składni napisany w języku JavaScipt.

%prep
%setup -qc

# Apache1 conf
cat > apache.conf <<'EOF'
Alias /js/syntaxhighlighter %{_appdir}
<Directory %{_appdir}>
	Allow from all
</Directory>
EOF

# lighttpd conf
cat > lighttpd.conf <<'EOF'
alias.url += (
    "/js/syntaxhighlighter" => "%{_appdir}",
)
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_appdir}
cp -a %{?with_test:test.html} scripts styles $RPM_BUILD_ROOT%{_appdir}

install -d $RPM_BUILD_ROOT%{_sysconfdir}
cp -a apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -a apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
cp -a lighttpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%files
%defattr(644,root,root,755)
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%{_appdir}
