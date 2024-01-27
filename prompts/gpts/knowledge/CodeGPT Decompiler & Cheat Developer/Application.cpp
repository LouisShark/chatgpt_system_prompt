#include "InputHandler.hpp"
#include "Process.hpp"

int main(int argc, char* argv[])
{
	using namespace DLL_Injector;

	InjectionData iData;
	
	// Handle console input.
	if (HandleInput(argc, argv, iData) == -1)
		return -1;

	// Inject DLL.
	return InjectDLL(iData);
}
