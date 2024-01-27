#include "Process.hpp"

#include <iostream>
#include <Windows.h>
#include <TlHelp32.h>

DWORD DLL_Injector::GetProcessID(const char* procName)
{
	HANDLE snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
	if (snapshot == INVALID_HANDLE_VALUE)
		return 0;

	PROCESSENTRY32 procEntry;
	procEntry.dwSize = sizeof(PROCESSENTRY32);

	DWORD pid = 0;
	bool result = Process32First(snapshot, &procEntry);

	while (result)
	{
		size_t i;
		char currentProcName[MAX_PATH];
		wcstombs_s(&i, currentProcName, MAX_PATH, procEntry.szExeFile, MAX_PATH - 1);

		if (strcmp(procName, currentProcName) == 0)
		{
			pid = procEntry.th32ProcessID;
			break;
		}

		result = Process32Next(snapshot, &procEntry);
	}

	CloseHandle(snapshot);
	return pid;
}

int DLL_Injector::InjectDLL(InjectionData& data)
{
	FARPROC LoadLibraryAProc = GetProcAddress(
		GetModuleHandle(TEXT("kernel32.dll")),
		"LoadLibraryA"
	);

	if (LoadLibraryAProc == NULL)
	{
		std::cout
			<< "ERROR: Couldn't get LoadLibraryA address. "
			<< "GetLastError() returned " << GetLastError() << "." << std::endl;

		return -1;
	}

	HANDLE procHandle = OpenProcess(
		PROCESS_ALL_ACCESS,
		FALSE,
		data.procID
	);

	if (procHandle == NULL)
	{
		std::cout
			<< "ERROR: OpenProcess() failed. "
			<< "GetLastError() returned " << GetLastError() << ". "
			<< "Is the process running as administrator? Consider executing this command as administrator."
			<< std::endl;

		return -1;
	}

	// Check if the process is a 64 bit application.
	IsWow64Process(procHandle, &data.isX64);

	LPVOID remoteBuff = VirtualAllocEx(procHandle, NULL, data.dllPath.length(), MEM_COMMIT, PAGE_READWRITE);
	if (remoteBuff == NULL)
	{
		std::cout
			<< "ERROR: VirtualAllocEx() failed. "
			<< "GetLastError() returned " << GetLastError() << "." << std::endl;

		CloseHandle(procHandle);
		return -1;
	}

	if (!WriteProcessMemory(procHandle, remoteBuff, data.dllPath.c_str(), data.dllPath.length(), NULL))
	{
		std::cout
			<< "ERROR: WriteProcessMemory() failed. "
			<< "GetLastError() returned " << GetLastError() << "." << std::endl;

		VirtualFreeEx(procHandle, remoteBuff, 0, MEM_RELEASE);
		CloseHandle(procHandle);
		return -1;
	}

	HANDLE thread = CreateRemoteThread(procHandle, NULL, NULL, (LPTHREAD_START_ROUTINE)LoadLibraryAProc, remoteBuff, NULL, NULL);
	if (!thread)
	{
		std::cout
			<< "ERROR: CreateRemoteThread() failed. "
			<< "GetLastError() returned " << GetLastError() << "." << std::endl;

		VirtualFreeEx(procHandle, remoteBuff, 0, MEM_RELEASE);
		CloseHandle(procHandle);
		return -1;
	}

	WaitForSingleObject(thread, INFINITE);
	CloseHandle(thread);

	VirtualFreeEx(procHandle, remoteBuff, 0, MEM_RELEASE);
	CloseHandle(procHandle);

	std::cout << "DLL succesfully injected." << std::endl;

	return 0;
}
