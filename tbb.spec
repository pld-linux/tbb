%define		sourcebasename tbb%{major}%{minor}_%{releasedate}oss
%define		major 	2
%define		minor	2
%define		releasedate 20090809
%define		rel		1
Summary:	The Threading Building Blocks library abstracts low-level threading details
Name:		tbb
Version:	%{major}.%{minor}
Release:	0.%{releasedate}%{rel}
License:	GPL v2 with exceptions
Group:		Development/Tools
URL:		http://www.threadingbuildingblocks.org/
Source0:	http://threadingbuildingblocks.org/uploads/77/142/%{major}.%{minor}/%{sourcebasename}_src.tgz
# Source0-md5:	c621053887c7ee86932da43e2deb3bff
Source1:	http://www.threadingbuildingblocks.org/uploads/81/91/Latest%20Open%20Source%20Documentation/Design_Patterns.pdf
# Source1-md5:	46062fef922d39abfd464bc06e02cdd8
Source2:	http://www.threadingbuildingblocks.org/uploads/81/91/Latest%20Open%20Source%20Documentation/Getting_Started.pdf
# Source2-md5:	b8f94104c47f9667e537b98bd940494a
Source3:	http://www.threadingbuildingblocks.org/uploads/81/91/Latest%20Open%20Source%20Documentation/Reference.pdf
# Source3-md5:	1481cbd378f4964691046d0ba570b374
Source4:	http://www.threadingbuildingblocks.org/uploads/81/91/Latest%20Open%20Source%20Documentation/Tutorial.pdf
# Source4-md5:	5bbdd1050c5dac5c1b782a6a98db0c46
Patch1:		%{name}-cxxflags.patch
BuildRequires:	libstdc++-devel
BuildRequires:	net-tools
# We need "arch" and "hostname" binaries:
BuildRequires:	util-linux
ExclusiveArch:	%{ix86} %{x8664} ia64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Threading Building Blocks (TBB) is a C++ runtime library that
abstracts the low-level threading details necessary for optimal
multi-core performance. It uses common C++ templates and coding style
to eliminate tedious threading implementation work.

TBB requires fewer lines of code to achieve parallelism than other
threading models. The applications you write are portable across
platforms. Since the library is also inherently scalable, no code
maintenance is required as more processor cores become available.

%package devel
Summary:	The Threading Building Blocks C++ headers and shared development libraries
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files and shared object symlinks for the Threading Building
Blocks (TBB) C++ libraries.

%package doc
Summary:	The Threading Building Blocks documentation
Group:		Documentation

%description doc
PDF documentation for the user of the Threading Building Block (TBB)
C++ library.

%prep
%setup -q -n %{sourcebasename}
%patch1 -p1

cp -p %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} .

%build
%{__make} \
	CXX="%{__cxx}" \
	CXXFLAGS="%{rpmcxxflags}" \
	tbb_build_prefix=obj

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}}

cd build/obj_release
for file in libtbb{,malloc}; do
	install $file.so.2 $RPM_BUILD_ROOT%{_libdir}/$file.so.2.%{version}
	ln -s $file.so.2.%{version} $RPM_BUILD_ROOT%{_libdir}/$file.so
	ln -s $file.so.2.%{version} $RPM_BUILD_ROOT%{_libdir}/$file.so.2
done
cd -

cd include
find tbb -type f -name '*.h' -exec \
	install -p -D -m 644 {} $RPM_BUILD_ROOT%{_includedir}/{} ';'

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING
%doc doc/Release_Notes.txt
%attr(755,root,root) %{_libdir}/libtbb.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtbb.so.2
%attr(755,root,root) %{_libdir}/libtbbmalloc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtbbmalloc.so.2

%files devel
%defattr(644,root,root,755)
%{_includedir}/tbb
%{_libdir}/libtbb.so
%{_libdir}/libtbbmalloc.so

%files doc
%defattr(644,root,root,755)
%doc *.pdf
