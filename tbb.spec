# use: major=year, minor=Update version, [micro=date if present]
%define		major	2021
%define		minor	5
%define		micro	0

%ifarch %{armv6}
%define		with_libatomic	1
%endif

Summary:	The Threading Building Blocks library abstracts low-level threading details
Summary(pl.UTF-8):	Threading Building Blocks - biblioteka abstrahująca niskopoziomowe szczegóły obsługi wątków
Name:		tbb
Version:	2021.9.0
Release:	1
License:	Apache v2.0
Group:		Development/Tools
# Source0Download: https://github.com/oneapi-src/oneTBB/releases
Source0:	https://github.com/01org/tbb/archive/v%{version}/oneTBB-%{version}.tar.gz
# Source0-md5:	ba4ecedc4949f673a34b35de738a72fc
Source1:	http://www.threadingbuildingblocks.org/uploads/81/91/Latest%20Open%20Source%20Documentation/Design_Patterns.pdf
# Source1-md5:	46062fef922d39abfd464bc06e02cdd8
Source2:	http://www.threadingbuildingblocks.org/uploads/81/91/Latest%20Open%20Source%20Documentation/Getting_Started.pdf
# Source2-md5:	b8f94104c47f9667e537b98bd940494a
Source3:	http://www.threadingbuildingblocks.org/uploads/81/91/Latest%20Open%20Source%20Documentation/Reference.pdf
# Source3-md5:	1481cbd378f4964691046d0ba570b374
Source4:	http://www.threadingbuildingblocks.org/uploads/81/91/Latest%20Open%20Source%20Documentation/Tutorial.pdf
# Source4-md5:	5bbdd1050c5dac5c1b782a6a98db0c46
URL:		http://www.threadingbuildingblocks.org/
BuildRequires:	cmake >= 3.1
BuildRequires:	hwloc-devel
%{?with_libatomic:BuildRequires:	libatomic-devel}
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 2.007
BuildRequires:	sed >= 4.0
ExclusiveArch:	%{ix86} %{x8664} x32 %{arm} aarch64 ia64 ppc ppc64
# __TBB_machine_cmpswp8 uses gcc's __sync_val_compare_and_swap8 or directly cmpxchg8b asm instruction
ExcludeArch:	i386 i486
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# see src/tbb/CMakeLists.txt /TBB_PC_NAME
%ifarch %{ix86} x32 %{arm} ppc
%define		tbb_pc_name	tbb32
%else
%define		tbb_pc_name	tbb
%endif

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
%setup -q -n oneTBB-%{version}

cp -p %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} .

%build
%cmake -B build \
	%{?with_libatomic:-DTBB_LIB_LINK_LIBS=-latomic} \
	-DTBB_STRICT:BOOL=OFF \
	-DTBB_TEST:BOOL=OFF

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%if "%{tbb_pc_name}" != "tbb"
# for compatibility
ln -sf %{tbb_pc_name}.pc $RPM_BUILD_ROOT%{_pkgconfigdir}/tbb.pc
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md third-party-programs.txt
%attr(755,root,root) %{_libdir}/libtbb.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libtbb.so.12
%attr(755,root,root) %{_libdir}/libtbbbind.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libtbbbind.so.3
%attr(755,root,root) %{_libdir}/libtbbmalloc.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libtbbmalloc.so.2
%attr(755,root,root) %{_libdir}/libtbbmalloc_proxy.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libtbbmalloc_proxy.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtbb.so
%attr(755,root,root) %{_libdir}/libtbbbind.so
%attr(755,root,root) %{_libdir}/libtbbmalloc.so
%attr(755,root,root) %{_libdir}/libtbbmalloc_proxy.so
# likely to be owned by different package?
%dir %{_includedir}/oneapi
%{_includedir}/oneapi/tbb.h
%{_includedir}/oneapi/tbb
%{_includedir}/tbb
%{_pkgconfigdir}/%{tbb_pc_name}.pc
%if "%{tbb_pc_name}" != "tbb"
%{_pkgconfigdir}/tbb.pc
%endif
%{_libdir}/cmake/TBB

%files doc
%defattr(644,root,root,755)
%doc *.pdf
