#
# Conditional build:
%bcond_without	python2	# CPython 2.x support
%bcond_without	python3	# CPython 3.x support
#
Summary:	CPython bindings generator for C++ libraries
Summary(pl.UTF-8):	Generator wiązań CPythona dla bibliotek C++
Name:		shiboken
Version:	1.2.4
Release:	2
License:	LGPL v2.1+ (libraries), GPL v2 (tools)
Group:		Development/Tools
#Source0Download: https://github.com/pyside/Shiboken/releases
Source0:	https://github.com/pyside/Shiboken/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	c284197d06ad25d78009ff55f18dd512
Patch0:		%{name}-python.patch
Patch1:		build.patch
Patch2:		python3.patch
URL:		https://github.com/pyside/Shiboken
BuildRequires:	QtCore-devel >= 4.5.0
BuildRequires:	QtXml-devel >= 4.5.0
BuildRequires:	QtXmlPatterns-devel >= 4.5.0
BuildRequires:	cmake >= 2.6
BuildRequires:	libstdc++-devel
BuildRequires:	libxml2-devel >= 1:2.6.32
BuildRequires:	libxslt-devel >= 1.1.19
BuildRequires:	python-devel >= 1:2.6
BuildRequires:	sphinx-pdg
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

%package python2
Summary:	Shiboken Python 2.x support files
Summary(pl.UTF-8):	Shiboken - pliki do obsługi Pythona 2.x
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	python-devel >= 1:%{py_ver}
Requires:	python-shiboken = %{version}-%{release}

%description python2
Shiboken Python 2.x support files.

%description python2 -l pl.UTF-8
Shiboken - pliki do obsługi Pythona 2.x.

%package -n python-shiboken
Summary:	Shiboken runtime library for Python 2.x
Summary(pl.UTF-8):	Biblioteka uruchomieniowa shiboken dla Pythona 2.x
Group:		Libraries/Python
Requires:	python-libs
Obsoletes:	shiboken-libs

%description -n python-shiboken
Shiboken runtime library for Python 2.x.

%description -n python-shiboken -l pl.UTF-8
Biblioteka uruchomieniowa shiboken dla Pythona 2.x.

%package python3
Summary:	Shiboken Python 3.x support files
Summary(pl.UTF-8):	Shiboken - pliki do obsługi Pythona 3.x
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	python3-devel >= 1:%{py_ver}
Requires:	python3-shiboken = %{version}-%{release}

%description python3
Shiboken Python 3.x support files.

%description python3 -l pl.UTF-8
Shiboken - pliki do obsługi Pythona 3.x.

%package -n python3-shiboken
Summary:	Shiboken runtime library for Python 3.x
Summary(pl.UTF-8):	Biblioteka uruchomieniowa shiboken dla Pythona 3.x
Group:		Libraries/Python
Requires:	python3-libs
Obsoletes:	shiboken-libs

%description -n python3-shiboken
Shiboken runtime library for Python 3.x.

%description -n python3-shiboken -l pl.UTF-8
Biblioteka uruchomieniowa shiboken dla Pythona 3.x.

%prep
%setup -q -n Shiboken-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%if %{with python2}
install -d build-py2
cd build-py2
%cmake ..
%{__make}
cd ..
%endif

%if %{with python3}
install -d build-py3
cd build-py3
%cmake .. \
	-DUSE_PYTHON3=TRUE
%{__make}
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python3}
%{__make} -C build-py3 install \
	DESTDIR=$RPM_BUILD_ROOT
# content depends on python version
%{__mv} $RPM_BUILD_ROOT%{_pkgconfigdir}/shiboken{,3}.pc
%endif

%if %{with python2}
%{__make} -C build-py2 install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n python-shiboken -p /sbin/ldconfig
%postun	-n python-shiboken -p /sbin/ldconfig

%post	-n python3-shiboken -p /sbin/ldconfig
%postun	-n python3-shiboken -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS
%attr(755,root,root) %{_bindir}/shiboken
%{_includedir}/shiboken
%dir %{_libdir}/cmake/Shiboken-%{version}
%{_libdir}/cmake/Shiboken-%{version}/ShibokenConfig.cmake
%{_libdir}/cmake/Shiboken-%{version}/ShibokenConfigVersion.cmake
%{_mandir}/man1/shiboken.1*

%if %{with python2}
%files python2
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libshiboken-python%{py_ver}.so
%{_pkgconfigdir}/shiboken.pc
%{_libdir}/cmake/Shiboken-%{version}/ShibokenConfig-python%{py_ver}.cmake

%files -n python-shiboken
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libshiboken-python%{py_ver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libshiboken-python%{py_ver}.so.1.2
%attr(755,root,root) %{py_sitedir}/shiboken.so
%endif

%if %{with python3}
%files python3
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libshiboken.cpython-3*.so
%{_pkgconfigdir}/shiboken3.pc
%{_libdir}/cmake/Shiboken-%{version}/ShibokenConfig.cpython-3*.cmake

%files -n python3-shiboken
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libshiboken.cpython-3*.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libshiboken.cpython-3*.so.1.2
%attr(755,root,root) %{py3_sitedir}/shiboken.so
%endif
