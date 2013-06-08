Name:       qt5-qtwebkit
Summary:    Web content engine library for Qt
Version:    5.0.2
Release:    1%{?dist}
Group:      Qt/Qt
License:    BSD and LGPLv2+
URL:        http://download.qt-project.org/official_releases/qt/5.0/5.0.2/submodules/qtwebkit-opensource-src-5.0.2.tar.gz
Source0:    %{name}-%{version}.tar.bz2
BuildRequires:  qt5-qtcore-devel
BuildRequires:  qt5-qtgui-devel
BuildRequires:  qt5-qtnetwork-devel
BuildRequires:  qt5-qtwidgets-devel
BuildRequires:  qt5-qtprintsupport-devel
#BuildRequires:  qt5-qtlocation-devel
BuildRequires:  qt5-qtmultimedia-devel
BuildRequires:  qt5-qtscript-devel
BuildRequires:  qt5-qtv8-devel
BuildRequires:  pkgconfig(Qt5Qml)
BuildRequires:  pkgconfig(Qt5Quick)
BuildRequires:  qt5-qt3d-devel
#BuildRequires:  qt5-qtsensors-devel
BuildRequires:  qt5-qtxmlpatterns-devel
BuildRequires:  qt5-qmake
BuildRequires:  qt5-qtsql-devel
BuildRequires:  pkgconfig(icu-uc)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  glib2-devel
BuildRequires:  gst-plugins-base-devel
BuildRequires:  gstreamer-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libpng-devel
BuildRequires:  gperf
BuildRequires:  python
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  fdupes
BuildRequires:  ruby

%description
QtWebKit provides a Web browser engine that makes it easy to embed content from
the World Wide Web into your Qt application.


%package uiprocess-launcher
Summary:    Web content engine library for Qt - WebKit2 process launcher
Group:      Qt/Qt

%description uiprocess-launcher
QtWebKit provides a Web browser engine that makes it easy to embed content from
the World Wide Web into your Qt application.

This package contains the UI process launcher for WebKit2 engine


%package -n lib%{_qtmodule_base_name}5
Summary:    Web content engine library for Qt - core runtime files
Group:      Qt/Qt
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description -n lib%{_qtmodule_base_name}5
QtWebKit provides a Web browser engine that makes it easy to embed content from
the World Wide Web into your Qt application.

This package contains the core runtime files needed to launch Qt 5 applications
using QtWebKit library.


%package -n lib%{_qtmodule_base_name}5-devel
Summary:    Web content engine library for Qt - core development files
Group:      Qt/Qt
Requires:   lib%{_qtmodule_base_name}5 = %{version}

%description -n lib%{_qtmodule_base_name}5-devel
QtWebKit provides a Web browser engine that makes it easy to embed content from
the World Wide Web into your Qt application.

This package contains the core development files needed to build Qt 5 applications
using QtWebKit library.


%package -n lib%{_qtmodule_base_name}5-widgets
Summary:    Web content engine library for Qt - GUI runtime files
Group:      Qt/Qt
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description -n lib%{_qtmodule_base_name}5-widgets
QtWebKit provides a Web browser engine that makes it easy to embed content from
the World Wide Web into your Qt application.

This package contains the GUI runtime files needed to launch Qt 5 applications
using QtWebKitWidgets library.


%package -n lib%{_qtmodule_base_name}5-widgets-devel
Summary:    Web content engine library for Qt - GUI development files
Group:      Qt/Qt
Requires:   lib%{_qtmodule_base_name}5-widgets = %{version}

%description -n lib%{_qtmodule_base_name}5-widgets-devel
QtWebKit provides a Web browser engine that makes it easy to embed content from
the World Wide Web into your Qt application.

This package contains the GUI development files needed to build Qt 5 applications
using QtWebKitWidgets library.


%package -n qt5-qtqml-import-webkitplugin
Summary:    Qt WebKit QML plugin
Group:      Qt/Qt

%description -n qt5-qtqml-import-webkitplugin
QtWebKit provides a Web browser engine that makes it easy to embed content from
the World Wide Web into your Qt application.

This package contains the WebKit QML plugin for QtQml.

%package -n qt5-qtqml-import-webkitplugin-experimental
Summary:    Qt WebKit Experimental QML plugin
Group:      Qt/Qt

%description -n qt5-qtqml-import-webkitplugin-experimental
QtWebKit provides a Web browser engine that makes it easy to embed content from
the World Wide Web into your Qt application.

This package contains the WebKit QML Experimental plugin for QtQml.


%prep
%setup -q -n %{name}-%{version}/qtwebkit

# remove .../qt/tests directory which introduces nothing but trouble
rm -rf Source/WebKit/qt/tests/

%build
## From Carsten Munk: create way smaller debuginfo
#export CXXFLAGS="`echo $CXXFLAGS | sed 's/ -g / -gdwarf-4 /g'`"
#export CFLAGS="`echo $CFLAGS | sed 's/ -g / -gdwarf-4 /g'`"
# XXX: Remove debug symbols entirely, we're running out of linker memory!
export CXXFLAGS="`echo $CXXFLAGS | sed 's/ -g / /g'`"
export CFLAGS="`echo $CFLAGS | sed 's/ -g / /g'`"
#
export QMAKEPATH="`pwd`/Tools/qmake"
export QTDIR=/usr/share/qt5
#

qmake -qt=5
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}

%qmake5_install
# Remove .la files
rm -f %{buildroot}/usr/lib/libQt5WebKit.la
rm -f %{buildroot}/usr/lib/libQt5WebKitWidgets.la
# Fix wrong path in pkgconfig files
find %{buildroot}%{_libdir}/pkgconfig -type f -name '*.pc' \
-exec perl -pi -e "s, -L%{_builddir}/?\S+,,g" {} \;
# Fix wrong path in prl files
find %{buildroot}%{_libdir} -type f -name '*.prl' \
-exec sed -i -e "/^QMAKE_PRL_BUILD_DIR/d;s/\(QMAKE_PRL_LIBS =\).*/\1/" {} \;
# Eliminate duplicates
%fdupes %{buildroot}/%{_libdir}
%fdupes %{buildroot}/%{_includedir}







%post -n lib%{_qtmodule_base_name}5 -p /sbin/ldconfig

%postun -n lib%{_qtmodule_base_name}5 -p /sbin/ldconfig

%post -n lib%{_qtmodule_base_name}5-widgets -p /sbin/ldconfig

%postun -n lib%{_qtmodule_base_name}5-widgets -p /sbin/ldconfig







%files uiprocess-launcher
%defattr(-,root,root,-)
%{_libdir}/qt5/libexec/QtWebProcess
%{_libdir}/qt5/libexec/QtWebPluginProcess


%files -n lib%{_qtmodule_base_name}5
%defattr(-,root,root,-)
%{_libdir}/libQt5WebKit.so.*

%files -n lib%{_qtmodule_base_name}5-devel
%defattr(-,root,root,-)
%{_includedir}/qt5/QtWebKit/
%{_libdir}/cmake/Qt5WebKit/
%{_libdir}/libQt5WebKit.prl
%{_libdir}/libQt5WebKit.so
%{_libdir}/pkgconfig/Qt5WebKit.pc
%{_datadir}/qt5/mkspecs/modules/qt_lib_webkit.pri

%files -n lib%{_qtmodule_base_name}5-widgets
%defattr(-,root,root,-)
%{_libdir}/libQt5WebKitWidgets.so.*

%files -n lib%{_qtmodule_base_name}5-widgets-devel
%defattr(-,root,root,-)
%{_includedir}/qt5/QtWebKitWidgets/
%{_libdir}/cmake/Qt5WebKitWidgets/
%{_libdir}/libQt5WebKitWidgets.prl
%{_libdir}/libQt5WebKitWidgets.so
%{_libdir}/pkgconfig/Qt5WebKitWidgets.pc
%{_datadir}/qt5/mkspecs/modules/qt_lib_webkitwidgets.pri

%files -n qt5-qtqml-import-webkitplugin
%defattr(-,root,root,-)
%{_libdir}/qt5/qml/QtWebKit/libqmlwebkitplugin.so
%{_libdir}/qt5/qml/QtWebKit/qmldir

%files -n qt5-qtqml-import-webkitplugin-experimental
%defattr(-,root,root,-)
%{_libdir}/qt5/qml/QtWebKit/experimental/libqmlwebkitexperimentalplugin.so
%{_libdir}/qt5/qml/QtWebKit/experimental/qmldir


#### No changelog section, separate $pkg.changes contains the history

