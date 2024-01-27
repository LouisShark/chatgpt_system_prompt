#pragma comment(lib, "Winhttp.lib")
#pragma comment(lib, "Opengl32.lib")

#include <d3d9.h>

#include "stdafx.h"

#include "scan.h"
#include "parse.h"
#include "input.h"
#include "ui.h"
#include "hitobject.h"

#define D3DDEV9_LEN 119

typedef IDirect3D9* (WINAPI *Direct3DCreate9T)(UINT SDKVersion);

static bool init = false;

HDC hDc = NULL;
HWND g_hwnd = NULL;
HANDLE g_process = NULL;
HMODULE g_module = NULL;
IDirect3DDevice9 *g_d3d9_device = 0;
void *pDeviceTable[D3DDEV9_LEN];

bool compatibility_mode = false;

static void unload_module()
{
    Sleep(2000);
    VirtualFree(wglSwapBuffersGateway, 0, MEM_RELEASE);
    FreeLibrary(g_module);
}

void unload_dll()
{
    destroy_ui();
    destroy_hooks();
    std::thread(unload_module).detach();
}

static inline void imgui_new_frame()
{
    ImGui_ImplWin32_NewFrame();
    ImGui::NewFrame();

    process_hitobject();

    if (GetAsyncKeyState(VK_F11) & 1)
    {
        cfg_mod_menu_visible = !cfg_mod_menu_visible;
        ImGui::SaveIniSettingsToDisk(ImGui::GetIO().IniFilename);
    }

    draw_debug_log();
    ImGui::GetIO().MouseDrawCursor = ImGui::GetIO().WantCaptureMouse;

    if (!cfg_mod_menu_visible)
    {
        if (!show_debug_log_window)
            ImGui::GetIO().MouseDrawCursor = false;
        goto frame_end;
    }

    update_ui();

frame_end:

    ImGui::EndFrame();
    ImGui::Render();
}

HRESULT __stdcall d3d9_update(IDirect3DDevice9 *pDevice)
{
    if (!init)
    {
        init = true;

        g_process = GetCurrentProcess();
        g_d3d9_device = pDevice;

        init_ui(pDevice);
        CloseHandle(CreateThread(0, 0, (LPTHREAD_START_ROUTINE)init_hooks, 0, 0, 0));
    }

    ImGui_ImplDX9_NewFrame();
    imgui_new_frame();
    ImGui_ImplDX9_RenderDrawData(ImGui::GetDrawData());

    return wglSwapBuffersGateway(pDevice);
}

__declspec(naked) void opengl_update()
{
    if (!init)
    {
        init = true;

        g_process = GetCurrentProcess();

        hDc = wglGetCurrentDC();
        g_hwnd = WindowFromDC(hDc);

#ifdef FR_LOG_TO_CONSOLE
        AllocConsole();
        FILE *f;
        freopen_s(&f, "CONOUT$", "w", stdout);
        freopen_s(&f, "CONOUT$", "w", stderr);
#endif // FR_LOG_TO_CONSOLE

        init_ui();
        CloseHandle(CreateThread(0, 0, (LPTHREAD_START_ROUTINE)init_hooks, 0, 0, 0));
    }

    ImGui_ImplOpenGL3_NewFrame();
    imgui_new_frame();
    ImGui_ImplOpenGL3_RenderDrawData(ImGui::GetDrawData());

    __asm {
        jmp [wglSwapBuffersGateway]
    }
}

static inline BOOL CALLBACK EnumWindowsCallback(HWND handle, LPARAM lParam)
{
    DWORD wndProcId = 0;
    GetWindowThreadProcessId(handle, &wndProcId);

    if (GetCurrentProcessId() != wndProcId)
        return TRUE;

    g_hwnd = handle;
    return FALSE;
}

static inline HWND GetProcessWindow()
{
    EnumWindows(EnumWindowsCallback, NULL);
    return g_hwnd;
}

static inline bool GetD3D9Device(void **pTable, size_t Size)
{
    if (!pTable)
        return false;

    Size *= sizeof(void *);

    HMODULE d3d9 = GetModuleHandleA("d3d9.dll");
    Direct3DCreate9T d3d9_create = (Direct3DCreate9T)GetProcAddress(d3d9, "Direct3DCreate9");
    IDirect3D9 *pD3D = d3d9_create(D3D_SDK_VERSION);

    if (!pD3D)
        return false;

    IDirect3DDevice9 *pDummyDevice = NULL;

    D3DPRESENT_PARAMETERS d3dpp = {};
    d3dpp.Windowed = false;
    d3dpp.SwapEffect = D3DSWAPEFFECT_DISCARD;
    d3dpp.hDeviceWindow = GetProcessWindow();

    HRESULT dummyDeviceCreated = pD3D->CreateDevice(D3DADAPTER_DEFAULT, D3DDEVTYPE_HAL, d3dpp.hDeviceWindow, D3DCREATE_SOFTWARE_VERTEXPROCESSING, &d3dpp, &pDummyDevice);

    if (dummyDeviceCreated != S_OK)
    {
        d3dpp.Windowed = true;
        dummyDeviceCreated = pD3D->CreateDevice(D3DADAPTER_DEFAULT, D3DDEVTYPE_HAL, d3dpp.hDeviceWindow, D3DCREATE_SOFTWARE_VERTEXPROCESSING, &d3dpp, &pDummyDevice);

        if (dummyDeviceCreated != S_OK)
        {
            pD3D->Release();
            return false;
        }
    }

    memcpy(pTable, *reinterpret_cast<void ***>(pDummyDevice), Size);

    pDummyDevice->Release();
    pD3D->Release();
    return true;
}

DWORD WINAPI freedom_main(HMODULE hModule)
{
    g_module = hModule;

    SwapBuffersHook = Hook<Trampoline32>("wglSwapBuffers", "opengl32.dll", (BYTE *)opengl_update, (BYTE *)&wglSwapBuffersGateway, 5);
    SwapBuffersHook.src += 14;
    SwapBuffersHook.Enable();

    // NOTE(Ciremun): one second is enough... right?
    Sleep(1000);

    if (!init)
    {
        // NOTE(Ciremun): Compatibility Mode
        SwapBuffersHook.Disable();
        compatibility_mode = true;
        if (GetD3D9Device((void **)pDeviceTable, D3DDEV9_LEN))
        {
            void *pEndScene = pDeviceTable[42];
            SwapBuffersHook = Hook<Trampoline32>((BYTE *)pEndScene, (BYTE *)d3d9_update, (BYTE *)&wglSwapBuffersGateway, 7);
            SwapBuffersHook.Enable();
        }
    }

    return 0;
}

BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved)
{
    if (ul_reason_for_call == DLL_PROCESS_ATTACH)
        CloseHandle(CreateThread(0, 0, (LPTHREAD_START_ROUTINE)freedom_main, hModule, 0, 0));
    return TRUE;
}
