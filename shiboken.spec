# TODO: python2/python3 builds
Summary:	CPython bindings generator for C++ libraries
Summary(pl.UTF-8):	Generator wiązań CPythona dla bibliotek C++
Name:		shiboken
Version:	1.1.2
Release:	2
License:	LGPL v2.1+ (libraries), GPL v2 (tools)
Group:		Development/Tools
#Source0Download: http://qt-project.org/wiki/category:LanguageBindings::PySide::Downloads
Source0:	http://qt-project.org/uploads/pyside/%{name}-%{version}.tar.bz2
# Source0-md5:	0a37b5011b3a7276bf4584317412a4b6
URL:		http://qt-project.org/PySide/
BuildRequires:	QtCore-devel >= 4.5.0
BuildRequires:	QtXml-devel >= 4.5.0
BuildRequires:	QtXmlPatterns-devel >= 4.5.0
BuildRequires:	cmake >= 2.6
BuildRequires:	libstdc++-devel
BuildRequires:	libxml2-devel >= 1:2.6.32
BuildRequires:	libxslt-devel >= 1.1.19
BuildRequires:	python-devel >= 1:2.6
BuildRequires:	sphinx-pdg
Requires:	%{name}-libs = %{version}-%{release}
Requires:	QtCore >= 4.5.0
Requires:	QtXml >= 4.5.0
Requires:	QtXmlPatterns >= 4.5.0
Requires:	libxml2 >= 1:2.6.32
Requires:	libxslt >= 1.1.19
Requires:	python
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
shiboken is a CPython bindings generator for C++ libraries.

%description -l pl.UTF-8
shiboken to generator wiązań CPythona dla bibliotek C++.

%package libs
Summary:	Shiboken runtime library
Summary(pl.UTF-8):	Biblioteka uruchomieniowa shiboken
Group:		Libraries
Requires:	python-libs

%description libs
Shiboken runtime library.

%description libs -l pl.UTF-8
Biblioteka uruchomieniowa shiboken.

%prep
%setup -q

%build
mkdir build
cd build
%cmake ..

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog
%attr(755,root,root) %{_bindir}/shiboken
%attr(755,root,root) %{_libdir}/libshiboken-python%{py_ver}.so
%{_includedir}/shiboken
%{_pkgconfigdir}/shiboken.pc
%{_libdir}/cmake/Shiboken-%{version}
%{_mandir}/man1/shiboken.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libshiboken-python%{py_ver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libshiboken-python%{py_ver}.so.1.1
%attr(755,root,root) %{py_sitedir}/shiboken.so
