%bcond_with doc

Summary: The GNU versions of grep pattern matching utilities
%define _name grep
Name: gnu-%{_name}
Version: 3.11
Release: 0
License: GPLv3+
Source: %{name}-%{version}.tar.bz2
Source1: posync.sh
Source2: af.po
Source3: be.po
Source4: bg.po
Source5: ca.po
Source6: cs.po
Source7: da.po
Source8: de.po
Source9: el.po
Source10: eo.po
Source11: es.po
Source12: et.po
Source13: eu.po
Source14: fi.po
Source15: fr.po
Source16: ga.po
Source17: gl.po
Source18: he.po
Source19: hr.po
Source20: hu.po
Source21: id.po
Source22: it.po
Source23: ja.po
Source24: ka.po
Source25: ko.po
Source26: ky.po
Source27: lt.po
Source28: nb.po
Source29: nl.po
Source30: pa.po
Source31: pl.po
Source32: pt.po
Source33: pt_BR.po
Source34: ro.po
Source35: ru.po
Source36: sk.po
Source37: sl.po
Source38: sr.po
Source39: sv.po
Source40: ta.po
Source41: th.po
Source42: tr.po
Source43: uk.po
Source44: vi.po
Source45: zh_CN.po
Source46: zh_TW.po
Source47: polist.inc
Patch0: grep-3.11-tests-drop.patch
Patch1: grep-3.11-gnulib-tests-drop.patch
URL: http://www.gnu.org/software/grep/
BuildRequires: gettext
BuildRequires: pkgconfig(libpcre2-8)
BuildRequires: rsync
BuildRequires: gperf
%{?with_doc:BuildRequires texinfo}
Obsoletes: %{_name} < 1:2.5.1a+git1
Provides: %{_name} = 1:2.5.1a+git1

%description
The GNU versions of commonly used grep utilities.  Grep searches
through textual input for lines which contain a match to a specified
pattern and then prints the matching lines.  GNU's grep utilities
include grep, egrep and fgrep.

You should install grep on your system, because it is a very useful
utility for searching through text.

%if 0%{?with_doc}
%package doc
Summary:   Documentation for %{name}
Requires:  %{name} = %{version}-%{release}
Obsoletes: %{_name}-docs < 1:2.5.1a+git1
Provides: %{_name}-docs = 1:2.5.1a+git1

%description doc
Man and info pages for %{name}.
%endif

%package locale
Summary: Translations and Locale for package %{name}

%description locale
This package provides translations for package %{name}.

%prep
%autosetup -p1 -n %{name}-%{version}/upstream

# bootstrap po files ourself
for source in %{sources} ; do
    case $source in
        *.po) cp $source po/. ;;
        *) : ;;
    esac
done
ls po/*.po |sed 's|.*/||; s|\.po$||' > po/LINGUAS

%{?!with_doc:sed '/makeinfo/d' -i bootstrap.conf}


%build

# Set tarball-version so the gnu version script picks it up
# to set the application version
echo %{version} > .tarball-version

./bootstrap --no-git \
            --gnulib-srcdir=gnulib \
            --skip-po

%configure \
           CFLAGS="-I%{_includedir}/pcre" \
           CFLAGS="$RPM_OPT_FLAGS"

%make_build po lib src tests gnulib-tests %{?with_doc: doc}

%install
for dir in po lib src %{?with_doc: doc}; do
    %{__make} -C $dir install DESTDIR=%{?buildroot} INSTALL="%{__install} -p"
done

%find_lang %{_name}

%check
for dir in tests gnulib-tests ; do
    %{__make} -C $dir check
done

%files locale -f %{_name}.lang
%defattr(-,root,root,-)

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/*

%if 0%{?with_doc}
%files doc
%defattr(-,root,root)
%{_infodir}/%{_name}.*
%{_mandir}/man1/*%{_name}.*
%endif
