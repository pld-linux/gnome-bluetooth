Summary:	GNOME Bluetooth Subsystem
Summary(pl):	Podsystem GNOME Bluetooth
Name:		gnome-bluetooth
Version:	0.4.1
Release:	0.1
License:	GPL
Group:		X11/Applications
Source0:	http://usefulinc.com/software/gnome-bluetooth/releases/%{name}-%{version}.tar.gz
# Source0-md5:	59d83693ee5e10fed0aa7c941b0423d9
URL:		http://usefulinc.com/software/gnome-bluetooth/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gob2 >= 2.0.6
BuildRequires:	libbtctl-devel >= 0.3
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
przez Edda Dumbilla jako prototyp z zamiarem w³±czenia do projektu
GNOME. Na razie jest we wczesnym stadium rozwoju.

Ten pakiet zawiera serwer Bonobo do sterowania urz±dzeniami Bluetooth
oraz proste GUI do przegl±dania dostêpnych urz±dzeñ
(gnome-bluetooth-admin). Dostêpny jest serwer OBEX
(gnome-obex-server), pozwalaj±cy ¶ci±gaæ pliki wys³ane przez Bluetooth
do PC i zapisywaæ je w katalogu domowym. Program gnome-obex-send
pozwala wysy³aæ pliki. Jest u¿ywany przez modu³ gnome-vfs - wystarczy
wpisaæ bluetooth:/// w Nautilusie i przeci±gn±æ plik na urz±dzenie
docelowe.

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
%{_sysconfdir}/gnome-vfs-2.0/modules/*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/gnome-bluetooth-control
%attr(755,root,root) %{_libdir}/gnome-vfs-2.0/modules/libbluetooth.so
%{_libdir}/gnome-vfs-2.0/modules/libbluetooth.la
%{_libdir}/bonobo/servers/*
%{_datadir}/%{name}
%{_datadir}/idl/*
%{_desktopdir}/*
