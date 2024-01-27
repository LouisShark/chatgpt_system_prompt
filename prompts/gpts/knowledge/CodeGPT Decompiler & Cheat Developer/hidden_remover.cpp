#include "features/hidden_remover.h"

Hook<Trampoline32> HiddenHook;
tHiddenHook o_hom_update_vars_hidden;
uintptr_t hom_update_vars_code_start = 0;
uintptr_t hom_update_vars_hidden_loc = 0;
int32_t hom_mods_original_value = 0;

void init_unmod_hidden()
{
    if (hom_update_vars_hidden_loc)
    {
        HiddenHook = Hook<Trampoline32>(hom_update_vars_hidden_loc + 0x7, (BYTE *)hk_hom_update_vars_hidden, (BYTE *)&o_hom_update_vars_hidden, 6);
        if (cfg_hidden_remover_enabled)
            HiddenHook.Enable();
    }
}

void unmod_hidden_on_beatmap_load()
{
    if (cfg_hidden_remover_enabled && osu_manager_ptr)
    {
        uintptr_t osu_manager = *(uintptr_t *)(osu_manager_ptr);
        if (osu_manager)
        {
            uintptr_t hit_manager_ptr = *(uintptr_t *)(osu_manager + OSU_MANAGER_HIT_MANAGER_OFFSET);
            uintptr_t mods_ptr = *(uintptr_t *)(hit_manager_ptr + OSU_HIT_MANAGER_MODS_OFFSET);
            *(int32_t *)(mods_ptr + 0x0C) = hom_mods_original_value;
            hom_mods_original_value = 0;
        }
    }
}

void enable_hidden_remover_hooks()
{
    enable_notify_hooks();
    HiddenHook.Enable();
}

void disable_hidden_remover_hooks()
{
    disable_notify_hooks();
    HiddenHook.Disable();
}

__declspec(naked) void hk_hom_update_vars_hidden()
{
    __asm {
        push eax
        push ebx
        push edx
        mov eax, [ecx+OSU_HIT_MANAGER_MODS_OFFSET]
        mov ebx, [eax+0x8]
        mov edx, [eax+0xC]
        mov hom_mods_original_value, edx
        xor edx, ebx
        and edx, -0x9
        xor edx, ebx
        mov [eax+0xC], edx
        pop edx
        pop ebx
        pop eax
        jmp o_hom_update_vars_hidden
    }
}
