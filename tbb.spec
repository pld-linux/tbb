%define		major 	4
%define		minor	2
%define		micro	20130725
%define		sourcebasename tbb%{major}%{minor}_%{micro}oss
Summary:	The Threading Building Blocks library abstracts low-level threading details
Summary(pl.UTF-8):	Threading Building Blocks - biblioteka abstrahująca niskopoziomowe szczegóły obsługi wątków
Name:		tbb
Version:	%{major}.%{minor}.%{micro}
Release:	1
License:	GPL v2 with runtime exception
Group:		Development/Tools
Source0:	http://threadingbuildingblocks.org/sites/default/files/software_releases/source/%{sourcebasename}_src.tgz
# Source0-md5:	24342639e8b26771142061a9fedd1465
Source1:	http://www.threadingbuildingblocks.org/uploads/81/91/Latest%20Open%20Source%20Documentation/Design_Patterns.pdf
# Source1-md5:	46062fef922d39abfd464bc06e02cdd8
Source2:	http://www.threadingbuildingblocks.org/uploads/81/91/Latest%20Open%20Source%20Documentation/Getting_Started.pdf
# Source2-md5:	b8f94104c47f9667e537b98bd940494a
Source3:	http://www.threadingbuildingblocks.org/uploads/81/91/Latest%20Open%20Source%20Documentation/Reference.pdf
# Source3-md5:	1481cbd378f4964691046d0ba570b374
Source4:	http://www.threadingbuildingblocks.org/uploads/81/91/Latest%20Open%20Source%20Documentation/Tutorial.pdf
# Source4-md5:	5bbdd1050c5dac5c1b782a6a98db0c46
Source5:	%{name}.pc.in
Source6:	%{name}malloc.pc.in
Source7:	%{name}malloc_proxy.pc.in
Patch1:		%{name}-cxxflags.patch
Patch2:		mfence.patch
URL:		http://www.threadingbuildingblocks.org/
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
# We need "arch" binary:
BuildRequires:	util-linux
ExclusiveArch:	%{ix86} %{x8664} %{arm} ia64 ppc ppc64
# __TBB_machine_cmpswp8 uses gcc's __sync_val_compare_and_swap8 or directly cmpxchg8b asm instruction
ExcludeArch:	i386 i486
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Threading Building Blocks (TBB) is a C++ runtime library that
abstracts the low-level threading details necessary for optimal
multi-core performance. It uses common C++ templates and coding style
to eliminate tedious threading implementation work.

TBB requires fewer lines of code to achieve parallelism than other
threading models. The applications you write are portable across
supported platforms. Since the library is also inherently scalable, no
code maintenance is required as more processor cores become available.

%description -l pl.UTF-8
Threading Building Blocks (TBB) to biblioteka uruchomieniowa C++
abstrahująca niskopoziomowe szczegóły obsługi wątków potrzebne dla
optymalnej wydajności na procesorach wielordzeniowych. Wykorzystuje
szablony C++ w celu wyeliminowania nudnej pracy nad wielowątkowością.

TBB wymaga mniej linii kodu do osiągnięcia równoległości niż inne
modele wątkowania. Aplikacje są przenośne między obsługiwanymi
platformami. Biblioteka jest skalowalna, więc nie jest wymagane
modyfikowanie kodu wraz z dostępnością większej liczby rdzeni
procesor.

%package devel
Summary:	The Threading Building Blocks C++ headers
Summary(pl.UTF-8):	Pliki nagłówkowe C++ bibliotek Threading Building Blocks
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files and shared object symlinks for the Threading Building
Blocks (TBB) C++ libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe i dowiązania symboliczne dla bibliotek C++ Threading
Building Blocks.

%package doc
Summary:	The Threading Building Blocks documentation
Summary(pl.UTF-8):	Dokumentacja bibliotek Threading Building Blocks
Group:		Documentation

%description doc
PDF documentation for the user of the Threading Building Block (TBB)
C++ library.

%description doc -l pl.UTF-8
Dokumentacja w formacie PDF dla użytkowników biblioteki C++ Threading
Building Blocks (TBB).

%prep
%setup -q -n %{sourcebasename}
%patch1 -p1
%patch2 -p1

cp -p %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} .

cp -p %{SOURCE5} %{SOURCE6} %{SOURCE7} .

sed -i -e 's/-march=pentium4//' build/linux.gcc.inc

%build
%{__make} \
	CPLUS="%{__cxx}" \
	CXXFLAGS="%{rpmcxxflags}" \
	tbb_build_prefix=obj

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir},%{_pkgconfigdir}}

cd build/obj_release
for file in tbb tbbmalloc tbbmalloc_proxy; do
	install lib${file}.so.2 $RPM_BUILD_ROOT%{_libdir}/lib${file}.so.2.%{version}
	ln -s lib${file}.so.2.%{version} $RPM_BUILD_ROOT%{_libdir}/lib${file}.so
	ln -s lib${file}.so.2.%{version} $RPM_BUILD_ROOT%{_libdir}/lib${file}.so.2
done
cd -

cd include
find tbb -type f -name '*.h' -exec \
	install -p -D -m 644 {} $RPM_BUILD_ROOT%{_includedir}/{} ';'
cd -

for pc in tbb.pc tbbmalloc.pc tbbmalloc_proxy.pc; do
	in=$pc.in
	# fail if obsolete
	[ ! -f $RPM_BUILD_ROOT%{_pkgconfigdir}/$pc ] || exit 1
	sed -e '
		s,@prefix@,%{_prefix},;
		s,@libdir@,%{_libdir},;
		s,@includedir@,%{_includedir}/tbb,;
		s,@version@,%{version},
	' $in > $RPM_BUILD_ROOT%{_pkgconfigdir}/$pc
done

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES COPYING doc/Release_Notes.txt
%attr(755,root,root) %{_libdir}/libtbb.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtbb.so.2
%attr(755,root,root) %{_libdir}/libtbbmalloc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtbbmalloc.so.2
%attr(755,root,root) %{_libdir}/libtbbmalloc_proxy.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtbbmalloc_proxy.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtbb.so
%attr(755,root,root) %{_libdir}/libtbbmalloc.so
%attr(755,root,root) %{_libdir}/libtbbmalloc_proxy.so
%{_includedir}/tbb
%{_pkgconfigdir}/tbb.pc
%{_pkgconfigdir}/tbbmalloc.pc
%{_pkgconfigdir}/tbbmalloc_proxy.pc

%files doc
%defattr(644,root,root,755)
%doc *.pdf
