/*
 * Copyright (C) 2007 Apple Inc.  All rights reserved.
 * Copyright (C) 2008 Nokia Corporation and/or its subsidiary(-ies)
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 * 1.  Redistributions of source code must retain the above copyright
 *     notice, this list of conditions and the following disclaimer. 
 * 2.  Redistributions in binary form must reproduce the above copyright
 *     notice, this list of conditions and the following disclaimer in the
 *     documentation and/or other materials provided with the distribution. 
 * 3.  Neither the name of Apple Computer, Inc. ("Apple") nor the names of
 *     its contributors may be used to endorse or promote products derived
 *     from this software without specific prior written permission. 
 *
 * THIS SOFTWARE IS PROVIDED BY APPLE AND ITS CONTRIBUTORS "AS IS" AND ANY
 * EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL APPLE OR ITS CONTRIBUTORS BE LIABLE FOR ANY
 * DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
 * ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
 * THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

#ifndef InspectorClientQt_h
#define InspectorClientQt_h

#include "InspectorClient.h"
#include <inspector/InspectorFrontendChannel.h>
#include "InspectorFrontendClientLocal.h"

#include <QObject>
#include <QString>
#include <wtf/Forward.h>

class QWebPageAdapter;
class QWebPage;
class QWebView;

namespace WebCore {
class InspectorFrontendClientQt;
class InspectorServerRequestHandlerQt;
class Page;

class InspectorClientQt : public InspectorClient, public Inspector::FrontendChannel {
public:
    explicit InspectorClientQt(QWebPageAdapter*);

    void inspectedPageDestroyed() override;

    Inspector::FrontendChannel* openLocalFrontend(InspectorController*) override;
    void bringFrontendToFront() override;

    void highlight() override;
    void hideHighlight() override;

    ConnectionType connectionType() const override;
    bool sendMessageToFrontend(const String&) override;

    void releaseFrontendPage();

    void attachAndReplaceRemoteFrontend(InspectorServerRequestHandlerQt *channel);
    void detachRemoteFrontend();

    void closeFrontendWindow();

private:
    QWebPageAdapter* m_inspectedWebPage;
    QWebPageAdapter* m_frontendWebPage;
    std::unique_ptr<InspectorFrontendClientQt> m_frontendClient;
    bool m_remoteInspector;
    InspectorServerRequestHandlerQt* m_remoteFrontEndChannel;

    friend class InspectorServerRequestHandlerQt;
};

class InspectorFrontendClientQt : public InspectorFrontendClientLocal {
public:
    InspectorFrontendClientQt(QWebPageAdapter* inspectedWebPage, InspectorController* inspectedPageController,
        std::unique_ptr<QObject> inspectorView, WebCore::Page* inspectorPage, InspectorClientQt*);
    ~InspectorFrontendClientQt() override;

    void frontendLoaded() override;

    String localizedStringsURL() override;

    void bringToFront() override;
    void closeWindow() override;

    void attachWindow(DockSide) override;
    void detachWindow() override;

    void setAttachedWindowHeight(unsigned) override;
    void setAttachedWindowWidth(unsigned) override;

    void inspectedURLChanged(const String& newURL) override;

    void inspectorClientDestroyed();

private:
    void updateWindowTitle();
    void destroyInspectorView(bool notifyInspectorController);
    QWebPageAdapter* m_inspectedWebPage;
    std::unique_ptr<QObject> m_inspectorView;
    QString m_inspectedURL;
    bool m_destroyingInspectorView;
    InspectorClientQt* m_inspectorClient;
};
}

#endif
