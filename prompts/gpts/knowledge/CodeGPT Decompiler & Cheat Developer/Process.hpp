#pragma once

#include <string>
#include <Windows.h>

namespace DLL_Injector
{
	struct InjectionData
	{
		DWORD procID;
		std::string procName;
		BOOL isX64;

		std::string dllPath;
	};

	DWORD GetProcessID(const char* procName);
	int InjectDLL(InjectionData& data);

} // namespace DLL_Injector
