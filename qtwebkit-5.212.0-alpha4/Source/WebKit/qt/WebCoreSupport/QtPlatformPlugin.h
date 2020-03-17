/*
 * Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies)
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Library General Public
 * License as published by the Free Software Foundation; either
 * version 2 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Library General Public License for more details.
 *
 * You should have received a copy of the GNU Library General Public License
 * along with this library; see the file COPYING.LIB.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
 * Boston, MA 02110-1301, USA.
 *
 */

#ifndef QtPlatformPlugin_h
#define QtPlatformPlugin_h

#include "qwebkitplatformplugin.h"
#include <QPluginLoader>

class QWebSelectMethod;
class QWebNotificationPresenter;
class QWebHapticFeedbackPlayer;
class QWebSelectData;
class QWebTouchModifier;
#if ENABLE(VIDEO) && USE(QT_MULTIMEDIA)
class QWebFullScreenVideoHandler;
#endif
class QWebSpellChecker;

namespace WebCore {

class QtPlatformPlugin {
public:
    QtPlatformPlugin()
        : m_loaded(false)
        , m_plugin(0)
    {
    }

    ~QtPlatformPlugin();

    std::unique_ptr<QWebSelectMethod> createSelectInputMethod();
    std::unique_ptr<QWebNotificationPresenter> createNotificationPresenter();
    std::unique_ptr<QWebHapticFeedbackPlayer> createHapticFeedbackPlayer();
    std::unique_ptr<QWebTouchModifier> createTouchModifier();
#if ENABLE(VIDEO) && USE(QT_MULTIMEDIA)
    std::unique_ptr<QWebFullScreenVideoHandler> createFullScreenVideoHandler();
#endif
    std::unique_ptr<QWebSpellChecker> createSpellChecker();

    QWebKitPlatformPlugin* plugin();

private:
    bool m_loaded;
    QWebKitPlatformPlugin* m_plugin;
    QPluginLoader m_loader;
    bool load();
    bool load(const QString& file);
    bool loadStaticallyLinkedPlugin();
    template<typename T> std::unique_ptr<T> createExtension(QWebKitPlatformPlugin::Extension);
};

}

#endif // QtPlatformPlugin_h
