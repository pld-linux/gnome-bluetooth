Summary:	GNOME Bluetooth Subsystem
Summary(pl):	Podsystem GNOME Bluetooth
Name:		gnome-bluetooth
Version:	0.5.1
Release:	2
License:	GPL
Group:		X11/Applications
Source0:	http://downloads.usefulinc.com/gnome-bluetooth/%{name}-%{version}.tar.gz
# Source0-md5:	60dfef22c0cc075ac1e3d84c249b8ca3
Patch0:		%{name}-python.patch
Patch1:		%{name}-gnomeui.patch
URL:		http://usefulinc.com/software/gnome-bluetooth/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gob2 >= 2.0.8
BuildRequires:	libbtctl-devel >= 0.4
BuildRequires:	libgnomeui-devel
BuildRequires:	libtool
BuildRequires:	nautilus-devel
BuildRequires:	openobex-devel
BuildRequires:	sed >= 4.0
Requires:	bluez-utils
Requires:	python-gnome-ui >= 2.0.0
%pyrequires_eq	python-libs
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

%package devel
Summary:	Header files for GNOME bluetooth subsystem
Summary(pl):	Pliki nag³ówkowe dla podsystemu GNOME bluetooth
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for GNOME bluetooth subsystem.

%description devel -l pl
Pliki nag³ówkowe dla podsystemu GNOME bluetooth.

%package static
Summary:	Static GNOME bluetooth library
Summary(pl):	Statyczna biblioteka GNOME bluetooth
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static GNOME bluetooth library.

%description static -l pl
Statyczna biblioteka GNOME bluetooth.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

sed -i -e 's#$(PYTHON_PREFIX)/lib#$(PYTHON_PREFIX)/%{_lib}#g' python/Makefile.am

%build
glib-gettextize --copy --force
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{py_comp} $RPM_BUILD_ROOT%{py_sitedir}
%{py_ocomp} $RPM_BUILD_ROOT%{py_sitedir}

sed -i 's/manager.py$/manager.pyo/' $RPM_BUILD_ROOT%{_bindir}/gnome-bluetooth-manager

%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/*.so.*
%attr(755,root,root) %{_libdir}/bonobo/*.so
%{_libdir}/bonobo/servers/*
%{_datadir}/%{name}
%{_desktopdir}/*

%dir %{py_sitedir}/gnomebt
%attr(755,root,root) %{py_sitedir}/gnomebt/*.so
%{py_sitedir}/gnomebt/*.pyc
%{py_sitedir}/gnomebt/*.pyo

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so
%{_includedir}/*
%{_pkgconfigdir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
