Summary: The GNU versions of grep pattern matching utilities
%define _name grep
Name: gnu-%{_name}
Version: 2.5.1a+git1
Release: 0
License: GPLv2+
Group: Applications/Text
Source: grep-2.5.1a.tar.bz2
Patch0: grep-2.5.1-fgrep.patch
Patch1: grep-2.5.1-bracket.patch
Patch2: grep-2.5-i18n.patch
Patch3: grep-2.5.1-oi.patch
Patch4: grep-2.5.1-manpage.patch
Patch5: grep-2.5.1-color.patch
Patch6: grep-2.5.1-icolor.patch
Patch7: grep-skip.patch
Patch10: grep-2.5.1-egf-speedup.patch
Patch11: grep-2.5.1-dfa-optional.patch
Patch12: grep-2.5.1-tests.patch
Patch13: grep-2.5.1-w.patch
Patch14: grep-P.patch
Patch15: grep-mem-exhausted.patch
Patch16: grep-empty-pattern.patch
Patch17: grep-2.5.1a-pcrewrap.patch
Patch18: grep-2.5.1a-utf8.patch
Patch19: grep-aarch64.patch
URL: http://www.gnu.org/software/grep/
BuildRequires: pcre-devel >= 3.9-10, gettext
Obsoletes: %{_name} < 1:2.5.1a+git1
Provides: %{_name} = 1:2.5.1a+git1

%description
The GNU versions of commonly used grep utilities.  Grep searches
through textual input for lines which contain a match to a specified
pattern and then prints the matching lines.  GNU's grep utilities
include grep, egrep and fgrep.

You should install grep on your system, because it is a very useful
utility for searching through text.

%package doc
Summary:   Documentation for %{name}
Group:     Documentation
Requires:  %{name} = %{version}-%{release}
Obsoletes: %{_name}-docs < 1:2.5.1a+git1
Provides: %{_name}-docs = 1:2.5.1a+git1

%description doc
Man and info pages for %{name}.

%package locale
Summary: Translations and Locale for package %{name}

%description locale
This package provides translations for package %{name}.

%prep
%autosetup -p1 -n grep-2.5.1a

chmod a+x tests/fmbtest.sh
chmod a+x tests/pcrewrap.sh

%build
[ ! -e configure ] && ./autogen.sh
%configure --without-included-regex CPPFLAGS="-I%{_includedir}/pcre"
make %{?_smp_mflags}

%install
rm -rf ${RPM_BUILD_ROOT}
make %{?_smp_mflags} DESTDIR=$RPM_BUILD_ROOT install
mkdir -p $RPM_BUILD_ROOT/bin
mv -f $RPM_BUILD_ROOT%{_bindir}/* $RPM_BUILD_ROOT/bin
rm -rf $RPM_BUILD_ROOT%{_bindir}
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

# Use symlinks for egrep and fgrep
ln -sf grep $RPM_BUILD_ROOT/bin/egrep
ln -sf grep $RPM_BUILD_ROOT/bin/fgrep

%find_lang %{_name}
%check
make check

%clean
rm -rf ${RPM_BUILD_ROOT}

%files locale -f %{_name}.lang
%defattr(-,root,root,-)

%files
%defattr(-,root,root)
%license COPYING
/bin/*

%files doc
%defattr(-,root,root)
%{_infodir}/%{_name}.*
%{_mandir}/man1/*%{_name}.*
