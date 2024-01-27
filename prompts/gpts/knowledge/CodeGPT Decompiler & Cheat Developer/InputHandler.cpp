#include "InputHandler.hpp"

#include <iostream>
#include <fstream>

int DLL_Injector::HandleInput(int argc, char* argv[], InjectionData& data)
{
	if (argc < 3)
	{
		std::cout
			<< "ERROR: Insufficient number of arguments.\n"
			<< "USAGE: " << argv[COMMAND] << " [process name] [dll path]\n"
			<< "EXAMPLE: " << argv[COMMAND] << " Notepad.exe C:/DLLs/Example.dll" << std::endl;

		return -1;
	}

	// Get process name and ID.
	data.procName = argv[PROCESS_NAME];
	data.procID = DLL_Injector::GetProcessID(data.procName.c_str());

	if (!data.procID)
	{
		std::cout
			<< "ERROR: Couldn't find \"" << data.procName << "\" process. "
			<< "Make sure that the process is running and that the entered name is correct. "
			<< "Process names are case sensitive." << std::endl;

		return -1;
	}

	// Get DLL filepath.
	data.dllPath = "";
	for (int i = DLL_FILEPATH_START; i < argc; i++)
	{
		if (i != DLL_FILEPATH_START)
			data.dllPath += " ";

		data.dllPath += argv[i];
	}

	// Check if the file exists.
	std::ifstream file(data.dllPath);
	if (!file.good())
	{
		std::cout
			<< "ERROR: Couldn't find the DLL file at \"" << data.dllPath << "\". "
			<< "Make sure you've entered the correct path." << std::endl;

		return -1;
	}

	return 0;
}
