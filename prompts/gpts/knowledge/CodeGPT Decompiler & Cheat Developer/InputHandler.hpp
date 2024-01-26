#pragma once

#include "Process.hpp"

namespace DLL_Injector
{
	enum CONSOLE_PARAMS
	{
		COMMAND            = 0,
		PROCESS_NAME       = 1,
		DLL_FILEPATH_START = 2
	};

	int HandleInput(int argc, char* argv[], InjectionData& data);

} // namespace DLL_Injector
