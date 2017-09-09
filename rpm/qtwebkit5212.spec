# Conditional building of X11 related things
%bcond_with X11

Name:       qt5-qtwebkit
Summary:    Web content engine library for Qt
Version:    5.212.0
Release:    +git4%{?dist}
Group:      Qt/Qt
License:    BSD and LGPLv2+
URL:        https://code.qt.io/qt/qtwebkit.git
Source0:    %{name}-%{version}-alpha2.tar.xz
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  pkgconfig(Qt5PrintSupport)
#BuildRequires:  qt5-qtlocation-devel
BuildRequires:  pkgconfig(Qt5Script)
BuildRequires:  pkgconfig(Qt5Qml)
BuildRequires:  pkgconfig(Qt5Quick)
BuildRequires:  pkgconfig(Qt53D)
#BuildRequires:  qt5-qtsensors-devel
BuildRequires:  pkgconfig(Qt5XmlPatterns)
BuildRequires:  pkgconfig(Qt5Multimedia)
BuildRequires:  qt5-qmake
BuildRequires:  cmake
BuildRequires:  pkgconfig(Qt5Sql)
BuildRequires:  pkgconfig(icu-uc)
BuildRequires:  pkgconfig(sqlite3)
%if %{with X11}
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xrender)
%endif
# FIXME, it needs checking if other glib modules are used, those need
#        to be added separately!
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  libjpeg-turbo-devel
BuildRequires: 	pkgconfig(gstreamer-1.0)
BuildRequires: 	pkgconfig(gstreamer-base-1.0)
BuildRequires: 	pkgconfig(gstreamer-plugins-base-1.0)
BuildRequires: 	pkgconfig(gstreamer-plugins-bad-1.0)
BuildRequires: 	pkgconfig(gstreamer-audio-1.0)
BuildRequires: 	pkgconfig(gstreamer-video-1.0)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(libxslt)
BuildRequires:  qt5-qtmultimedia-devel
BuildRequires:  qt5-qtmultimedia-plugin-mediaservice-gstcamerabin
BuildRequires:  nemo-qtmultimedia-plugins-gstvideotexturebackend
BuildRequires:  qt5-qtmultimedia-plugin-audio-pulseaudio
BuildRequires:  qt5-qtmultimedia-plugin-audio-alsa
BuildRequires:  qt5-qtmultimedia-plugin-mediaservice-gstmediacapture
BuildRequires:  qt5-qtmultimedia-plugin-mediaservice-gstmediaplayer
BuildRequires:  qt5-qtmultimedia-plugin-mediaservice-gstaudiodecoder
BuildRequires:  qt5-qtmultimedia-plugin-resourcepolicy-resourceqt
BuildRequires:  qt5-qtmultimedia-plugin-playlistformats-m3u
BuildRequires:  gperf
BuildRequires:  python
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  fdupes
BuildRequires:  ruby
BuildRequires:  perl
BuildRequires:  perl-version
BuildRequires:  perl-libs

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


%package -n libqtwebkit5
Summary:    Web content engine library for Qt - core runtime files
Group:      Qt/Qt
Requires:   %{name}-uiprocess-launcher = %{version}
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description -n libqtwebkit5
QtWebKit provides a Web browser engine that makes it easy to embed content from
the World Wide Web into your Qt application.

This package contains the core runtime files needed to launch Qt 5 applications
using QtWebKit library.


%package -n libqtwebkit5-devel
Summary:    Web content engine library for Qt - core development files
Group:      Qt/Qt
Requires:   libqtwebkit5 = %{version}

%description -n libqtwebkit5-devel
QtWebKit provides a Web browser engine that makes it easy to embed content from
the World Wide Web into your Qt application.

This package contains the core development files needed to build Qt 5 applications
using QtWebKit library.


# %package -n libqtwebkit5-widgets
# Summary:    Web content engine library for Qt - GUI runtime files
# Group:      Qt/Qt
# Requires(post): /sbin/ldconfig
# Requires(postun): /sbin/ldconfig

# %description -n libqtwebkit5-widgets
# QtWebKit provides a Web browser engine that makes it easy to embed content from
# the World Wide Web into your Qt application.
# 
# This package contains the GUI runtime files needed to launch Qt 5 applications
# using QtWebKitWidgets library.


# %package -n libqtwebkit5-widgets-devel
# Summary:    Web content engine library for Qt - GUI development files
# Group:      Qt/Qt
# Requires:   libqtwebkit5-widgets = %{version}
# 
# %description -n libqtwebkit5-widgets-devel
# QtWebKit provides a Web browser engine that makes it easy to embed content from
# the World Wide Web into your Qt application.
# 
# This package contains the GUI development files needed to build Qt 5 applications
# using QtWebKitWidgets library.


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
%setup -q -n qtwebkit-%{version}-alpha2

# remove .../qt/tests directory which introduces nothing but trouble
#rm -rf Source/WebKit/qt/tests/

# Avoid "Project ERROR: Missing CMake tests. Either create tests in tests/auto/cmake, or disable cmake config file creation with CONFIG-=create_cmake"
#mkdir -p tests/auto/cmake

# JavaScriptCore bytecode Files generate // In consequence new JavaScriptCore needs GCC 4.9
#cd Source/JavaScriptCore/; python generate-bytecode-files --bytecodes_h llint/Bytecodes.h --init_bytecodes_asm llint/InitBytecodes.asm bytecode/BytecodeList.json

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
touch .git

%ifarch aarch64
%global qtdefines  DEFINES+=ENABLE_JIT=0 DEFINES+=ENABLE_YARR_JIT=0 DEFINES+=ENABLE_ASSEMBLER=0
%else
%global qtdefines  
%endif

#
# Configure to release build, drop tests, mimic Tools/qmake/mkspecs/features/production_build.prf for the whole
# build not just WebCore. We could also drop WebKit1 support aka libqtwebkit5-widgets with WEBKIT_CONFIG-=build_webkit1.
# See also Tools/qmake/mkspecs/features/features.prf.
# qmake -qt=5 CONFIG+=release CONFIG-=debug \
#        %{?qtdefines} \
#        WEBKIT_CONFIG-=build_tests \
#        CONFIG+=no_debug_info \
#        CONFIG-=separate_debug_info \
#        CONFIG-=create_cmake \
#        QMAKE_CFLAGS+=$QMAKE_CFLAGS_RELEASE \
#        QMAKE_CXXFLAGS+=$QMAKE_CXXFLAGS_RELEASE \
#        CONFIG*=use_all_in_one_files \
#        WEBKIT_CONFIG-=ftpdir \
#        WEBKIT_CONFIG-=video \
#        WEBKIT_CONFIG-=web_audio \
#        WEBKIT_CONFIG-=legacy_web_audio \
#        WEBKIT_CONFIG-=use_gstreamer \
#        WEBKIT_CONFIG-=use_gstreamer010 \
#        WEBKIT_CONFIG-=use_qt_multimedia \
#        WEBKIT_CONFIG-=gamepad \
#        WEBKIT_CONFIG-=svg \
#        WEBKIT_CONFIG-=inspector \
#        WEBKIT_CONFIG-=fullscreen_api \
#        WEBKIT_CONFIG-=netscape_plugin_api \
#        WEBKIT_CONFIG-=build_qttestsupport

mkdir -p build-rpm
cd build-rpm
cmake -DPORT=Qt \
       -DCMAKE_BUILD_TYPE=Release \
       -DENABLE_TOOLS=OFF \
       -DCMAKE_C_FLAGS_RELEASE:STRING="-DNDEBUG" \
       -DCMAKE_CXX_FLAGS_RELEASE:STRING="-DNDEBUG" \
       -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
       -DENABLE_WEBKIT2_DEFAULT=ON \
       -DUSE_QT_MULTIMEDIA=ON \
       -DUSE_GSTREAMER=OFF \
       -DUSE_GSTREAMER_GL=OFF \
       -DENABLE_FTL_JIT=OFF \
       -DENABLE_INDEXED_DATABASE=OFF \
       -DENABLE_TEST_SUPPORT=OFF \
       -DENABLE_API_TESTS=OFF \
       -DENABLE_GEOLOCATION=OFF \
       -DENABLE_DEVICE_ORIENTATION=OFF \
       -DENABLE_X11_TARGET=OFF \
       -DENABLE_WEB_AUDIO=OFF \
       -DENABLE_VIDEO=ON \
       -DENABLE_MEDIA_SOURCE=OFF \
       -DUSE_LIBHYPHEN=OFF \
       -DENABLE_INSPECTOR_UI=ON \
       -DENABLE_QT_WEBCHANNEL=OFF \
       -DENABLE_DATABASE_PROCESS=OFF \
       -DENABLE_FTPDIR=OFF ..

make -j6
cd ..

%install
cd build-rpm
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
cd ..
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


%post -n libqtwebkit5 -p /sbin/ldconfig

%postun -n libqtwebkit5 -p /sbin/ldconfig

# %post -n libqtwebkit5-widgets -p /sbin/ldconfig
# 
# %postun -n libqtwebkit5-widgets -p /sbin/ldconfig

%files uiprocess-launcher
%defattr(-,root,root,-)
%{_libdir}/qt5/libexec/QtWebProcess
%{_libdir}/qt5/libexec/QtWebNetworkProcess

%files -n libqtwebkit5
%defattr(-,root,root,-)
%{_libdir}/libQt5WebKit.so.*

%files -n libqtwebkit5-devel
%defattr(-,root,root,-)
%{_includedir}/qt5/QtWebKit/
%{_libdir}/cmake/Qt5WebKit/
%{_libdir}/libQt5WebKit.so
%{_libdir}/pkgconfig/Qt5WebKit.pc
%{_datadir}/qt5/mkspecs/modules/qt_lib_webkit.pri

# %files -n libqtwebkit5-widgets
# %defattr(-,root,root,-)
# %{_libdir}/libQt5WebKitWidgets.so.*
# 
# %files -n libqtwebkit5-widgets-devel
# %defattr(-,root,root,-)
# %{_includedir}/qt5/QtWebKitWidgets/
# %{_libdir}/cmake/Qt5WebKitWidgets/
# %{_libdir}/libQt5WebKitWidgets.so
# %{_libdir}/pkgconfig/Qt5WebKitWidgets.pc
# %{_datadir}/qt5/mkspecs/modules/qt_lib_webkitwidgets.pri

%files -n qt5-qtqml-import-webkitplugin
%defattr(-,root,root,-)
%{_libdir}/qt5/qml/QtWebKit/libqmlwebkitplugin.so
%{_libdir}/qt5/qml/QtWebKit/qmldir
%{_libdir}/qt5/qml/QtWebKit/plugins.qmltypes

%files -n qt5-qtqml-import-webkitplugin-experimental
%defattr(-,root,root,-)
%{_libdir}/qt5/qml/QtWebKit/experimental/libqmlwebkitexperimentalplugin.so
%{_libdir}/qt5/qml/QtWebKit/experimental/qmldir


#### No changelog section, separate $pkg.changes contains the history
 
