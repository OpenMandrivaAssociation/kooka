# Spec is based on openSUSE spec adopted for ROSA/Mandriva

%define git 20130123

Name:		kooka
Version:	0.61
Release:	0.%{git}.3
License:	LGPLv2+
Group:		Graphical desktop/KDE
Summary:	Scan and OCR suite for KDE
Url:		https://projects.kde.org/kooka
# From git
Source:		%{name}-%{version}.git%{git}.tar.bz2
Source1:	%{name}-lang.tar.bz2
# ROSA's translation update (29.01.2013)
Source2:	%{name}-ru.po
BuildRequires:	kdelibs4-devel
BuildRequires:	pkgconfig(libgphoto2)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(sane-backends)

%description
Kooka is an open source GNU/Linux scan program based on SANE and
KScan library.

Kooka helps you to handle the most important scan parameters, find the
correct image file format to save and manage your scanned images. It
offers support for different OCR modules. Libkscan, a autonomous part
of Kooka, provides a scan service for easy and consistent use to all
KDE applications.

Install ocrad or gocr if you wish to enable optical character recognition
in kooka.

This is the WIP KDE4 port.

%files -f %{name}.lang
%{_kde_applicationsdir}/kooka.desktop
%{_kde_appsdir}/kooka
%{_kde_bindir}/kooka
%{_kde_iconsdir}/hicolor/48x48/apps/kooka.png
%{_kde_services}/scanservice.desktop
%{_kde_docdir}/HTML/en/*

#----------------------------------------------------------------------

%define libkscan_major 3
%define libkscan_libname %mklibname libkscan %{libkscan_major}

%package -n %{libkscan_libname}
Summary:	KScan is a KDE scanner library
Requires:	libkscan_common >= %{version}

%description -n %{libkscan_libname}
KScan is a KDE scanner library.

%files -n %{libkscan_libname}
%{_kde_libdir}/liblibkscan.so.%{libkscan_major}*

#----------------------------------------------------------------------

%package -n libkscan_common
Summary:	Common files (languages etc) for KScan, a KDE scanner library

%description -n libkscan_common
Common files (languages etc) for KScan, a KDE scanner library.

%files -n libkscan_common -f libkscan.lang
%{_kde_appsdir}/libkscan

#----------------------------------------------------------------------

%prep
%setup -q -n %{name}-%{version}.git%{git} -a 1
cat >> CMakeLists.txt << EOF
add_subdirectory( po )
EOF
# Overwrite with ROSA's translation
cp -f %{SOURCE2} po/ru/%{name}.po

%build
%cmake_kde4
%make

%install
%makeinstall_std -C build

rm -f %{buildroot}%{_kde_libdir}/liblibkscan.so

%find_lang kooka %{name}.lang
%find_lang libkscan libkscan.lang

