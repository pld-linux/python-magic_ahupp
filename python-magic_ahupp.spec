# NOTE: original package name is python-magic, but it would conflict with
# python*-magic packages built from file.spec.
# Also, we rename magic.py to magic_ahupp.py to avoid import name conflict.
#
# Conditional build:
%bcond_with	tests	# unit tests (broken, magic._pyc_ file is missing in sources)
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	File type identification using libmagic
Summary(pl.UTF-8):	Identyfikacja typu pliku przy użyciu libmagic
Name:		python-magic_ahupp
Version:	0.4.15
Release:	4
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/python-magic/
Source0:	https://files.pythonhosted.org/packages/source/p/python-magic/python-magic-%{version}.tar.gz
# Source0-md5:	e384c95a47218f66c6501cd6dd45ff59
URL:		http://github.com/ahupp/python-magic
%if %{with tests}
BuildRequires:	libmagic
%endif
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	libmagic
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This module uses ctypes to access the libmagic file type
identification library. It makes use of the local magic database and
supports both textual and MIME-type output.

%description -l pl.UTF-8
Ten moduł wykorzystuje ctypes do dostępu do biblioteki identyfikacji
typów plików libmagic. Wykorzystuje lokalną bazę danych wartości
magicznych i obsługuje wyjście zarówno w postaci tekstu, jak i typów
MIME.

%package -n python3-magic_ahupp
Summary:	File type identification using libmagic
Summary(pl.UTF-8):	Identyfikacja typu pliku przy użyciu libmagic
Group:		Libraries/Python
Requires:	libmagic
Requires:	python3-modules >= 1:3.6

%description -n python3-magic_ahupp
This module uses ctypes to access the libmagic file type
identification library. It makes use of the local magic database and
supports both textual and MIME-type output.

%description -n python3-magic_ahupp -l pl.UTF-8
Ten moduł wykorzystuje ctypes do dostępu do biblioteki identyfikacji
typów plików libmagic. Wykorzystuje lokalną bazę danych wartości
magicznych i obsługuje wyjście zarówno w postaci tekstu, jak i typów
MIME.

%prep
%setup -q -n python-magic-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
LC_ALL=C.UTF-8 %{__python} -m unittest discover -s test
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
LC_ALL=C.UTF-8 %{__python3} -m unittest discover -s test
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%{__rm} $RPM_BUILD_ROOT%{py_sitescriptdir}/magic.py[co]
%{__mv} $RPM_BUILD_ROOT%{py_sitescriptdir}/{magic,magic_ahupp}.py
%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_postclean
%endif

%if %{with python3}
%py3_install

%{__rm} $RPM_BUILD_ROOT%{py3_sitescriptdir}/__pycache__/*.py[co]
%{__mv} $RPM_BUILD_ROOT%{py3_sitescriptdir}/{magic,magic_ahupp}.py
%py3_comp $RPM_BUILD_ROOT%{py3_sitescriptdir}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitescriptdir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc LICENSE
%{py_sitescriptdir}/magic_ahupp.py[co]
%{py_sitescriptdir}/python_magic-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-magic_ahupp
%defattr(644,root,root,755)
%doc LICENSE
%{py3_sitescriptdir}/magic_ahupp.py
%{py3_sitescriptdir}/__pycache__/magic_ahupp.cpython-*.py[co]
%{py3_sitescriptdir}/python_magic-%{version}-py*.egg-info
%endif
