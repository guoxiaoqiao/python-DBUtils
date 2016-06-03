%if 0%{?fedora} > 12
%global with_python3 1
%else
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

%global mod_name DBUtils

Name:           python-DBUtils
Version:        1.1
Release:        1%{?dist}
Summary:        A fast tunnel proxy that help you get through firewalls

License:        ASL 2.0
URL:            https://github.com/guoxiaoqiao/mysqlclient-python
Source0:        %{mod_name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
# m2crypto is not available for python3
#BuildRequires:  python3-m2crypto
Requires:       python3-mysqlclient
%endif

%description
python-DBUtils

%if 0%{?with_python3}
%package -n python3-%{mod_name}
Summary:        python-DBUtils

%description -n python3-%{mod_name}
python-DBUtils

This package contains the client and server implementation for Shadowsocks in
Python 3.
%endif

%prep
%setup -q -n %{mod_name}-%{version}
# remove shebangs in the module files
#sed -i -e '/^#!\//, 1d' %{mod_name}/*.py %{mod_name}/crypto/*.py
# explicitly remove the included egg
rm -fr %{mod_name}*.egg-info

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3

%build
#%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3

%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
#mv $RPM_BUILD_ROOT%{_bindir}/{,python3-}sslocal
#mv $RPM_BUILD_ROOT%{_bindir}/{,python3-}ssserver
%endif # with_python3
#%{__python2} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT


%check
#%{__python2} setup.py test

%if 0%{?with_python3}
pushd %{py3dir}
#%{__python3} setup.py test
popd
%endif # with_python3

#%files
#%doc README.rst
#%license LICENSE
#%{_bindir}/sslocal
#%{_bindir}/ssserver
#%{python2_sitelib}/%{mod_name}*

%if 0%{?with_python3}
%files -n python3-%{mod_name}
#%doc README.rst
#%license LICENSE
#%{_bindir}/python3-sslocal
#%{_bindir}/python3-ssserver
%{python3_sitelib}/*
%endif

%changelog
* Fri Oct 30 2015 Robin Lee <cheeselee@fedoraproject.org> - 2.8.2-2
- 2.8.2 license changed to ASL 2.0

* Fri Oct 30 2015 Robin Lee <cheeselee@fedoraproject.org> - 2.8.2-1
- Update to 2.8.2

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Nov 16 2014 Robin Lee <cheeselee@fedoraproject.org> - 2.4.3-2
- Build a subpackage for python3

* Sun Nov 16 2014 Robin Lee <cheeselee@fedoraproject.org> - 2.4.3-1
- Update to 2.4.3

* Sat Sep 13 2014 Robin Lee <cheeselee@fedoraproject.org> - 2.2.1-1
- Update to 2.2.1

* Tue Jul 15 2014 Robin Lee <cheeselee@fedoraproject.org> - 2.0.11-1
- Update to 2.0.11, LICENSE included
- Explicitly remove the included egg

* Sat Jul 12 2014 Robin Lee <cheeselee@fedoraproject.org> - 2.0.10-2
- BuildRequires python2-setuptools

* Sat Jul 12 2014 Robin Lee <cheeselee@fedoraproject.org> - 2.0.10-1
- Update to 2.0.10
- Requries and BuildRequires m2crypto

* Sun Jul  6 2014 Robin Lee <cheeselee@fedoraproject.org> - 2.0.8-2
- Explicitly use python2 macros

* Sat Jun 28 2014 Robin Lee <cheeselee@fedoraproject.org> - 2.0.8-1
- Initial package for Fedora
