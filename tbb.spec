# use: major=year, minor=Update version, [micro=date if present]
%define		major	2021
%define		minor	4
%define		micro	0
Summary:	The Threading Building Blocks library abstracts low-level threading details
Summary(pl.UTF-8):	Threading Building Blocks - biblioteka abstrahująca niskopoziomowe szczegóły obsługi wątków
Name:		tbb
Version:	%{major}.%{minor}.%{micro}
Release:	1
License:	Apache v2.0
Group:		Development/Tools
# Source0Download: https://github.com/oneapi-src/oneTBB/releases
Source0:	https://github.com/01org/tbb/archive/v%{version}/oneTBB-%{version}.tar.gz
# Source0-md5:	fa317f16003e31e33a57ae7d888403e4
Source1:	http://www.threadingbuildingblocks.org/uploads/81/91/Latest%20Open%20Source%20Documentation/Design_Patterns.pdf
# Source1-md5:	3fd5805aa4439b2c46072c9673300a4a
Source2:	http://www.threadingbuildingblocks.org/uploads/81/91/Latest%20Open%20Source%20Documentation/Getting_Started.pdf
# Source2-md5:	993aca18f0717f3ca3b36a7e4d0e0124
Source3:	http://www.threadingbuildingblocks.org/uploads/81/91/Latest%20Open%20Source%20Documentation/Reference.pdf
# Source3-md5:	c646c043d65a45b460eeb03b0a8ef0fb
Source4:	http://www.threadingbuildingblocks.org/uploads/81/91/Latest%20Open%20Source%20Documentation/Tutorial.pdf
# Source4-md5:	5c712f3a977525d5f23286decb3b1e16
URL:		http://www.threadingbuildingblocks.org/
BuildRequires:	cmake >= 3.1
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	sed >= 4.0
# We need "arch" binary:
BuildRequires:	util-linux
ExclusiveArch:	%{ix86} %{x8664} x32 %{arm} aarch64 ia64 ppc ppc64
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
%setup -q -n oneTBB-%{version}

cp -p %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} .

%build
%cmake -B build \
	-DTBB_STRICT:BOOL=OFF \
	-DTBB_TEST:BOOL=OFF

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md third-party-programs.txt
%attr(755,root,root) %{_libdir}/libtbb.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libtbb.so.12
%attr(755,root,root) %{_libdir}/libtbbmalloc.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libtbbmalloc.so.2
%attr(755,root,root) %{_libdir}/libtbbmalloc_proxy.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libtbbmalloc_proxy.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtbb.so
%attr(755,root,root) %{_libdir}/libtbbmalloc.so
%attr(755,root,root) %{_libdir}/libtbbmalloc_proxy.so
# likely to be owned by different package?
%dir %{_includedir}/oneapi
%{_includedir}/oneapi/tbb.h
%{_includedir}/oneapi/tbb
%{_includedir}/tbb
%{_pkgconfigdir}/tbb.pc
%{_libdir}/cmake/TBB

%files doc
%defattr(644,root,root,755)
%doc *.pdf
