#
# todo:
# - add python subpackage
# - fix static and devel subpackages
#
Summary:	GNOME Bluetooth Subsystem
Summary(pl):	Podsystem GNOME Bluetooth
Name:		gnome-bluetooth
Version:	0.5.1
Release:	0.1
License:	GPL
Group:		X11/Applications
Source0:	http://downloads.usefulinc.com/gnome-bluetooth/%{name}-%{version}.tar.gz
# Source0-md5:	60dfef22c0cc075ac1e3d84c249b8ca3
Patch0:		%{name}-python.patch
URL:		http://usefulinc.com/software/gnome-bluetooth/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gob2 >= 2.0.8
BuildRequires:	libbtctl-devel >= 0.4
BuildRequires:	libgnomeui-devel
BuildRequires:	libtool
BuildRequires:	nautilus-devel
BuildRequires:	openobex-devel
Requires:	bluez-utils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The GNOME Bluetooth Subsystem is being developed as a prototype by Edd
Dumbill, with the intention of being submitted to the GNOME desktop
project. The software is in its early stages right now.

This package contains a Bonobo server to control Bluetooth devices,
and a simple GUI to explore which devices are available
(gnome-bluetooth-admin). An OBEX server is available,
gnome-obex-server. This will receive files sent via Bluetooth to your
PC, and save them in your home directory. The program gnome-obex-send
enables you to send files. It is used by the gnome-vfs module - go to
bluetooth:/// in Nautilus and drag and drop a file onto a destination
device.

%description -l pl
GNOME Bluetooth Subsystem (podsystem GNOME Bluetooth) jest tworzony
przez Edda Dumbilla jako prototyp z zamiarem w��czenia do projektu
GNOME. Na razie jest we wczesnym stadium rozwoju.

Ten pakiet zawiera serwer Bonobo do sterowania urz�dzeniami Bluetooth
oraz proste GUI do przegl�dania dost�pnych urz�dze�
(gnome-bluetooth-admin). Dost�pny jest serwer OBEX
(gnome-obex-server), pozwalaj�cy �ci�ga� pliki wys�ane przez Bluetooth
do PC i zapisywa� je w katalogu domowym. Program gnome-obex-send
pozwala wysy�a� pliki. Jest u�ywany przez modu� gnome-vfs - wystarczy
wpisa� bluetooth:/// w Nautilusie i przeci�gn�� plik na urz�dzenie
docelowe.

%package devel
Summary:	Header files for gnome bluetooth subsystem
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for gnome bluetooth subsystem.

%package static
Summary:	Static gnome bluetooth library
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static gnome bluetooth library.

%prep
%setup -q

%build
rm -f missing
glib-gettextize --copy --force
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/*.so.*
%attr(755,root,root) %{_libdir}/bonobo/*.so
%{_libdir}/bonobo/servers/*
%{_datadir}/%{name}
%{_desktopdir}/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so
%{_includedir}/*
%{_pkgconfigdir}/*

%files static
%defattr(644,root,root,755)
#%{_libdir}/*.a
