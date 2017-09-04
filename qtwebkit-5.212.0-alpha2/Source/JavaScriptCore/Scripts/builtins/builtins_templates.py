#!/usr/bin/env python
#
# Copyright (c) 2014, 2015 Apple Inc. All rights reserved.
# Copyright (C) 2015 Canon Inc. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY APPLE INC. AND ITS CONTRIBUTORS ``AS IS''
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL APPLE INC. OR ITS CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGE.

# Builtins generator templates, which can be filled with string.Template.


class BuiltinsGeneratorTemplates:

    LicenseText = (
    """Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY APPLE INC. AND ITS CONTRIBUTORS ``AS IS''
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL APPLE INC. OR ITS CONTRIBUTORS
BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
THE POSSIBILITY OF SUCH DAMAGE.
""")

    DoNotEditWarning = (
    """// DO NOT EDIT THIS FILE. It is automatically generated from JavaScript files for
// builtins by the script: Source/JavaScriptCore/Scripts/generate-js-builtins.py""")

    HeaderIncludeGuardTop = (
    """#ifndef ${headerGuard}
#define ${headerGuard}""")

    HeaderIncludeGuardBottom = (
    """#endif // ${headerGuard}
""")

    NamespaceTop = (
    """namespace ${namespace} {""")

    NamespaceBottom = (
    """} // namespace ${namespace}""")

    CombinedHeaderStaticMacros = (
    """#define DECLARE_BUILTIN_GENERATOR(codeName, functionName, argumentCount) \\
    JSC::FunctionExecutable* codeName##Generator(JSC::VM&);

${macroPrefix}_FOREACH_BUILTIN_CODE(DECLARE_BUILTIN_GENERATOR)
#undef DECLARE_BUILTIN_GENERATOR""")

    SeparateHeaderStaticMacros = (
    """#define DECLARE_BUILTIN_GENERATOR(codeName, functionName, argumentCount) \\
    JSC::FunctionExecutable* codeName##Generator(JSC::VM&);

${macroPrefix}_FOREACH_${objectMacro}_BUILTIN_CODE(DECLARE_BUILTIN_GENERATOR)
#undef DECLARE_BUILTIN_GENERATOR""")

    CombinedJSCImplementationStaticMacros = (
    """
#define DEFINE_BUILTIN_GENERATOR(codeName, functionName, argumentCount) \\
JSC::FunctionExecutable* codeName##Generator(JSC::VM& vm) \\
{\\
    return vm.builtinExecutables()->codeName##Executable()->link(vm, vm.builtinExecutables()->codeName##Source()); \
}
${macroPrefix}_FOREACH_BUILTIN_CODE(DEFINE_BUILTIN_GENERATOR)
#undef DEFINE_BUILTIN_GENERATOR
""")

    SeparateJSCImplementationStaticMacros = (
    """
#define DEFINE_BUILTIN_GENERATOR(codeName, functionName, argumentCount) \\
JSC::FunctionExecutable* codeName##Generator(JSC::VM& vm) \\
{\\
    return vm.builtinExecutables()->codeName##Executable()->link(vm, vm.builtinExecutables()->codeName##Source()); \
}
${macroPrefix}_FOREACH_${objectMacro}_BUILTIN_CODE(DEFINE_BUILTIN_GENERATOR)
#undef DEFINE_BUILTIN_GENERATOR
""")

    CombinedWebCoreImplementationStaticMacros = (
        """
#define DEFINE_BUILTIN_GENERATOR(codeName, functionName, argumentCount) \\
JSC::FunctionExecutable* codeName##Generator(JSC::VM& vm) \\
{\\
    JSVMClientData* clientData = static_cast<JSVMClientData*>(vm.clientData); \\
    return clientData->builtinFunctions().${objectNameLC}Builtins().codeName##Executable()->link(vm, clientData->builtinFunctions().${objectNameLC}Builtins().codeName##Source()); \\
}
${macroPrefix}_FOREACH_BUILTIN_CODE(DEFINE_BUILTIN_GENERATOR)
#undef DEFINE_BUILTIN_GENERATOR
""")

    SeparateWebCoreImplementationStaticMacros = (
        """
#define DEFINE_BUILTIN_GENERATOR(codeName, functionName, argumentCount) \\
JSC::FunctionExecutable* codeName##Generator(JSC::VM& vm) \\
{\\
    JSVMClientData* clientData = static_cast<JSVMClientData*>(vm.clientData); \\
    return clientData->builtinFunctions().${objectNameLC}Builtins().codeName##Executable()->link(vm, clientData->builtinFunctions().${objectNameLC}Builtins().codeName##Source()); \\
}
${macroPrefix}_FOREACH_${objectMacro}_BUILTIN_CODE(DEFINE_BUILTIN_GENERATOR)
#undef DEFINE_BUILTIN_GENERATOR
""")

    SeparateHeaderWrapperBoilerplate = (
    """class ${objectName}BuiltinsWrapper : private JSC::WeakHandleOwner {
public:
    explicit ${objectName}BuiltinsWrapper(JSC::VM* vm)
        : m_vm(*vm)
        ${macroPrefix}_FOREACH_${objectMacro}_BUILTIN_FUNCTION_NAME(INITIALIZE_BUILTIN_NAMES)
#define INITIALIZE_BUILTIN_SOURCE_MEMBERS(name, functionName, length) , m_##name##Source(JSC::makeSource(StringImpl::createFromLiteral(s_##name, length)))
        ${macroPrefix}_FOREACH_${objectMacro}_BUILTIN_CODE(INITIALIZE_BUILTIN_SOURCE_MEMBERS)
#undef INITIALIZE_BUILTIN_SOURCE_MEMBERS
    {
    }

#define EXPOSE_BUILTIN_EXECUTABLES(name, functionName, length) \\
    JSC::UnlinkedFunctionExecutable* name##Executable(); \\
    const JSC::SourceCode& name##Source() const { return m_##name##Source; }
    ${macroPrefix}_FOREACH_${objectMacro}_BUILTIN_CODE(EXPOSE_BUILTIN_EXECUTABLES)
#undef EXPOSE_BUILTIN_EXECUTABLES

    ${macroPrefix}_FOREACH_${objectMacro}_BUILTIN_FUNCTION_NAME(DECLARE_BUILTIN_IDENTIFIER_ACCESSOR)

    void exportNames();

private:
    JSC::VM& m_vm;

    ${macroPrefix}_FOREACH_${objectMacro}_BUILTIN_FUNCTION_NAME(DECLARE_BUILTIN_NAMES)

#define DECLARE_BUILTIN_SOURCE_MEMBERS(name, functionName, length) \\
    JSC::SourceCode m_##name##Source;\\
    JSC::Weak<JSC::UnlinkedFunctionExecutable> m_##name##Executable;
    ${macroPrefix}_FOREACH_${objectMacro}_BUILTIN_CODE(DECLARE_BUILTIN_SOURCE_MEMBERS)
#undef DECLARE_BUILTIN_SOURCE_MEMBERS

};

#define DEFINE_BUILTIN_EXECUTABLES(name, functionName, length) \\
inline JSC::UnlinkedFunctionExecutable* ${objectName}BuiltinsWrapper::name##Executable() \\
{\\
    if (!m_##name##Executable)\\
        m_##name##Executable = JSC::Weak<JSC::UnlinkedFunctionExecutable>(JSC::createBuiltinExecutable(m_vm, m_##name##Source, functionName##PublicName(), s_##name##ConstructAbility), this, &m_##name##Executable);\\
    return m_##name##Executable.get();\\
}
${macroPrefix}_FOREACH_${objectMacro}_BUILTIN_CODE(DEFINE_BUILTIN_EXECUTABLES)
#undef DEFINE_BUILTIN_EXECUTABLES

inline void ${objectName}BuiltinsWrapper::exportNames()
{
#define EXPORT_FUNCTION_NAME(name) m_vm.propertyNames->appendExternalName(name##PublicName(), name##PrivateName());
    ${macroPrefix}_FOREACH_${objectMacro}_BUILTIN_FUNCTION_NAME(EXPORT_FUNCTION_NAME)
#undef EXPORT_FUNCTION_NAME
}""")

    SeparateHeaderInternalFunctionsBoilerplate = (
    """class ${objectName}BuiltinFunctions {
public:
    explicit ${objectName}BuiltinFunctions(JSC::VM& vm) : m_vm(vm) { }

    void init(JSC::JSGlobalObject&);
    void visit(JSC::SlotVisitor&);

public:
    JSC::VM& m_vm;

#define DECLARE_BUILTIN_SOURCE_MEMBERS(functionName) \\
    JSC::WriteBarrier<JSC::JSFunction> m_##functionName##Function;
    ${macroPrefix}_FOREACH_${objectMacro}_BUILTIN_FUNCTION_NAME(DECLARE_BUILTIN_SOURCE_MEMBERS)
#undef DECLARE_BUILTIN_SOURCE_MEMBERS
};

inline void ${objectName}BuiltinFunctions::init(JSC::JSGlobalObject& globalObject)
{
#define EXPORT_FUNCTION(codeName, functionName, length)\\
    m_##functionName##Function.set(m_vm, &globalObject, JSC::JSFunction::createBuiltinFunction(m_vm, codeName##Generator(m_vm), &globalObject));
    ${macroPrefix}_FOREACH_${objectMacro}_BUILTIN_CODE(EXPORT_FUNCTION)
#undef EXPORT_FUNCTION
}

inline void ${objectName}BuiltinFunctions::visit(JSC::SlotVisitor& visitor)
{
#define VISIT_FUNCTION(name) visitor.append(&m_##name##Function);
    ${macroPrefix}_FOREACH_${objectMacro}_BUILTIN_FUNCTION_NAME(VISIT_FUNCTION)
#undef VISIT_FUNCTION
}
""")
