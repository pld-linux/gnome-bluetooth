Summary:	GNOME Bluetooth Subsystem
Summary(pl.UTF-8):	Podsystem GNOME Bluetooth
Name:		gnome-bluetooth
Version:	0.11.0
Release:	2
License:	GPL
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-bluetooth/0.11/%{name}-%{version}.tar.gz
# Source0-md5:	fdfc2ad1204f08c49c0054ae39f2d42b
Patch0:		%{name}-python.patch
Patch1:		%{name}-gnomeui.patch
Patch2:		%{name}-desktop.patch
Patch3:		%{name}-link.patch
URL:		http://usefulinc.com/software/gnome-bluetooth/
BuildRequires:	GConf2-devel >= 2.14.0
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake >= 1.8
BuildRequires:	gob2 >= 2.0.14
BuildRequires:	gtk+2-devel >= 2.10.0
BuildRequires:	intltool >= 0.18
BuildRequires:	libbtctl-devel >= 0.9.0
BuildRequires:	libgnomeui-devel >= 2.16.0
BuildRequires:	librsvg-devel >= 1:2.16.0
BuildRequires:	libtool
BuildRequires:	openobex-devel >= 1.2
BuildRequires:	pkgconfig
BuildRequires:	python-btctl >= 0.8.0
BuildRequires:	python-pygtk-devel >= 2:2.0
BuildRequires:	sed >= 4.0
Requires:	%{name}-libs = %{version}-%{release}
Requires:	bluez-utils
Requires:	python-btctl >= 0.8.0
Requires:	python-gnome-ui >= 2.16.0
Requires:	python-pygtk-glade >= 2.10.1
%pyrequires_eq	python-libs
Suggests:	gnome-vfs-obexftp
Obsoletes:	python-gnome-bluetooth
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

%description -l pl.UTF-8
GNOME Bluetooth Subsystem (podsystem GNOME Bluetooth) jest tworzony
przez Edda Dumbilla jako prototyp z zamiarem włączenia do projektu
GNOME. Na razie jest we wczesnym stadium rozwoju.

Ten pakiet zawiera serwer Bonobo do sterowania urządzeniami Bluetooth
oraz proste GUI do przeglądania dostępnych urządzeń
(gnome-bluetooth-admin). Dostępny jest serwer OBEX
(gnome-obex-server), pozwalający ściągać pliki wysłane przez Bluetooth
do PC i zapisywać je w katalogu domowym. Program gnome-obex-send
pozwala wysyłać pliki. Jest używany przez moduł gnome-vfs - wystarczy
wpisać bluetooth:/// w Nautilusie i przeciągnąć plik na urządzenie
docelowe.

%package libs
Summary:	GNOME bluetooth subsystem shared libraries
Summary(pl.UTF-8):	Współdzielone biblioteki dla podsystemu GNOME bluetooth
License:	LGPL
Group:		Development/Libraries
Requires:	libbtctl >= 0.8.0
Requires:	libgnomeui >= 2.16.0

%description libs
GNOME bluetooth subsystem shared libraries.

%description libs -l pl.UTF-8
Współdzielone biblioteki dla podsystemu GNOME bluetooth.

%package devel
Summary:	Header files for GNOME bluetooth subsystem
Summary(pl.UTF-8):	Pliki nagłówkowe dla podsystemu GNOME bluetooth
License:	LGPL
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	libbtctl-devel >= 0.8.0
Requires:	libgnomeui-devel >= 2.16.0

%description devel
Header files for GNOME bluetooth subsystem.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla podsystemu GNOME bluetooth.

%package static
Summary:	Static GNOME bluetooth library
Summary(pl.UTF-8):	Statyczna biblioteka GNOME bluetooth
License:	LGPL
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static GNOME bluetooth library.

%description static -l pl.UTF-8
Statyczna biblioteka GNOME bluetooth.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{__intltoolize}
#%%{__glib_gettextize}
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	--enable-static \
	--disable-schemas-install
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/bonobo/lib*.{a,la}
rm -f $RPM_BUILD_ROOT%{py_sitedir}/gnomebt/*.{a,la}

# duplicated with nb
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/no

%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install gnome-obex-server.schemas

%preun
%gconf_schema_uninstall gnome-obex-server.schemas

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.png
%{_sysconfdir}/gconf/schemas/gnome-obex-server.schemas

%dir %{py_sitedir}/gnomebt
%attr(755,root,root) %{py_sitedir}/gnomebt/*.so

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so
%{_libdir}/*.la
%{_includedir}/*
%{_pkgconfigdir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
