%{?scl:%scl_package nodejs-supports-color}
%{!?scl:%global pkg_name %{name}}

# This macro is needed at the start for building on EL6
%{?nodejs_find_provides_and_requires}

%global enable_tests 0

%global barename supports-color

Name:               %{?scl_prefix}nodejs-supports-color
Version:            3.1.1
Release:            6%{?dist}
Summary:            Detect whether a terminal supports color
License:            MIT
URL:                https://www.npmjs.org/package/supports-color
Source0:            http://registry.npmjs.org/%{barename}/-/%{barename}-%{version}.tgz
#Source2:            https://raw.githubusercontent.com/sindresorhus/supports-color/master/test.js
Source2:            test.js

BuildArch:          noarch
%if 0%{?fedora} >= 19
ExclusiveArch:      %{nodejs_arches} noarch
%else
ExclusiveArch:      %{ix86} x86_64 %{arm} noarch
%endif

BuildRequires:      %{?scl_prefix}runtime

%if 0%{?enable_tests}
BuildRequires:      %{?scl_prefix}npm(require-uncached)
BuildRequires:      %{?scl_prefix}npm(mocha)
%endif

%description
Detect whether a terminal supports color

%prep
%setup -q -n package
cp %{SOURCE2} .

# Remove bundled node_modules if there are any..
rm -rf node_modules/

#%%nodejs_fixdep --caret

%build
# This causes warnings when running the tests
#%nodejs_symlink_deps --build

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/supports-color
cp -pr browser.js index.js package.json \
    %{buildroot}%{nodejs_sitelib}/supports-color

%nodejs_symlink_deps

%check
%if 0%{?enable_tests}
%nodejs_symlink_deps --check
mocha
%endif

%files
%{!?_licensedir:%global license %doc}
%license license
%doc readme.md
%{nodejs_sitelib}/supports-color/

%changelog
* Mon Jul 03 2017 Zuzana Svetlikova <zsvetlik@redhat.com> - 3.1.1-6
- rh-nodejs8 rebuild

* Tue Feb 16 2016 Zuzana Svetlikova <zsvetlik@redhat.com> - 3.1.1-5
- Use macro in -runtime dependency
- Rebuilt with updated metapackage

* Thu Jan 07 2016 Tomas Hrcka <thrcka@redhat.com> - 3.1.1-2
- Enable scl macros

* Mon Sep 14 2015 Troy Dawson <tdawson@redhat.com> - 3.1.1-1
- Update to 3.1.1 (no longer has a binary)
- Remove tests until all dependencies are built

* Tue Feb 10 2015 Ralph Bean <rbean@redhat.com> - 1.2.0-2
- Include license from github.
- Enable tests.
- Make cli.js into a symlink.
- Comment out nodejs_symlink_deps --build, as per review.

* Tue Dec 02 2014 Ralph Bean <rbean@redhat.com> - 1.2.0-1
- Initial packaging for Fedora.
