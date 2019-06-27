Summary: The GNU versions of grep pattern matching utilities
Name: grep
Version: 2.5.1a
Epoch: 1
Release: 63
License: GPLv2+
Group: Applications/Text
Source: ftp://ftp.gnu.org/pub/gnu/grep/grep-%{version}.tar.bz2
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
Provides: gnu-grep
BuildRequires: pcre-devel >= 3.9-10, texinfo, gettext

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
Obsoletes: %{name}-docs

%description doc
Man and info pages for %{name}.

%prep
%setup -q
%patch0 -p1 -b .fgrep
%patch1 -p1 -b .bracket
%patch2 -p1 -b .i18n
%patch3 -p1 -b .oi
%patch4 -p1 -b .manpage
%patch5 -p1 -b .color
%patch6 -p1 -b .icolor
%patch7 -p1 -b .skip
%patch10 -p1 -b .egf-speedup
%patch11 -p1 -b .dfa-optional
%patch12 -p1 -b .tests
%patch13 -p1 -b .w
%patch14 -p1 -b .P
%patch15 -p1 -b .mem-exhausted
%patch16 -p1 -b .empty-pattern
%patch17 -p1 -b .pcrewrap
%patch18 -p1 -b .utf8
%patch19 -p1

chmod a+x tests/fmbtest.sh
chmod a+x tests/pcrewrap.sh

%build
[ ! -e configure ] && ./autogen.sh
%configure --without-included-regex CPPFLAGS="-I%{_includedir}/pcre"
make %{?_smp_mflags}

%install
rm -rf ${RPM_BUILD_ROOT}
make %{?_smp_mflags} DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

# Use symlinks for egrep and fgrep
ln -sf grep $RPM_BUILD_ROOT%{_bindir}/egrep
ln -sf grep $RPM_BUILD_ROOT%{_bindir}/fgrep

%find_lang %name
%check
make check

%clean
rm -rf ${RPM_BUILD_ROOT}

%lang_package

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/*

%files doc
%defattr(-,root,root)
%{_infodir}/%{name}.*
%{_mandir}/man1/*%{name}.*
