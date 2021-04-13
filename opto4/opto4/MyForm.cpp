#include "MyForm.h"

using namespace opto4;

[STAThreadAttribute]
int main(array<System::String^>^ args) {
	// Enabling Windows XP visual effects before any controls are created
	Application::EnableVisualStyles();
	Application::SetCompatibleTextRenderingDefault(false);

	// Create the main windows and run it 
	Application::Run(gcnew MyForm());
	return 0;
}