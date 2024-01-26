#pragma once

#include <stdint.h>

#include "pattern.h"

constexpr auto parse_beatmap_func_sig       { pattern::build<"55 8B EC 57 56 53 81 EC 58 01 00 00 8B F1 8D BD B8 FE FF FF B9 4E 00 00 00 33 C0 F3 AB 8B CE 89 8D B0 FE FF FF"> };
constexpr auto current_scene_func_sig       { pattern::build<"55 8B EC 57 56 53 50 8B D9 83 3D"> };
constexpr auto beatmap_onload_func_sig      { pattern::build<"55 8B EC 57 56 53 83 EC 44 8B F1 B9"> };
constexpr auto selected_song_func_sig       { pattern::build<"55 8B EC 83 E4 F8 57 56 83 EC 38 83 3D"> };
constexpr auto audio_time_func_sig          { pattern::build<"55 8B EC 83 E4 F8 57 56 83 EC 38 83 3D"> };
constexpr auto osu_manager_func_sig         { pattern::build<"55 8B EC 57 56 53 83 EC 14 80 3D"> };
constexpr auto binding_manager_func_sig     { pattern::build<"55 8B EC 57 56 83 EC 58 8B F1 8D 7D A0"> };
constexpr auto selected_replay_func_sig     { pattern::build<"55 8B EC 57 56 53 81 EC A0 00 00 00 8B F1 8D BD 68 FF FF FF B9 22 00 00 00 33 C0 F3 AB 8B CE 8B F1 8D 7D E0"> };
constexpr auto window_manager_func_sig      { pattern::build<"57 56 53 83 EC 6C 8B F1 8D 7D A8 B9 12 00 00 00 33 C0 F3 AB 8B CE 89 4D 94"> };
constexpr auto update_timing_func_sig       { pattern::build<"55 8B EC 83 E4 F8 57 56 83 EC 18 8B F9 8B 0D"> };
constexpr auto check_timewarp_func_sig      { pattern::build<"55 8B EC 57 56 53 81 EC B0 01 00 00 8B F1 8D BD 50 FE FF FF B9 68 00 00 00 33 C0"> };
constexpr auto osu_client_id_func_sig       { pattern::build<"8B F1 8D 7D C4 B9 0C 00 00 00 33 C0 F3 AB 8B CE 89 4D C0 8B 15"> };
constexpr auto username_func_sig            { pattern::build<"55 8B EC 57 56 53 83 EC 08 33 C0 89 45 EC 89 45 F0 8B F2 8B CE 8B 01 8B 40 30"> };
constexpr auto update_flashlight_func_sig   { pattern::build<"55 8B EC 56 83 EC 14 8B F1 8B 56 5C"> };
constexpr auto check_flashlight_func_sig    { pattern::build<"55 8B EC 57 56 53 83 EC 18 8B F9 80"> };
constexpr auto hom_update_vars_func_sig     { pattern::build<"55 8B EC 57 56 53 83 EC . 8B F1 8B DA 8B 7E . 85 FF 75 . 8D 65 . 5B 5E 5F 5D C2 08 00 8B CF BA"> };

constexpr auto approach_rate_sig            { pattern::build<"8B 85 B0 FE FF FF D9 58 2C"> };
constexpr auto approach_rate_sig_2          { pattern::build<"8B 85 B0 FE FF FF D9 40 38 D9 58 2C"> };
constexpr auto circle_size_sig              { pattern::build<"8B 85 B0 FE FF FF D9 58 30"> };
constexpr auto overall_difficulty_sig       { pattern::build<"8B 85 B0 FE FF FF D9 58 38"> };
constexpr auto beatmap_onload_sig           { pattern::build<"0F 94 C2"> };
constexpr auto current_scene_sig            { pattern::build<"A1....A3....A1....A3"> };
constexpr auto selected_song_sig            { pattern::build<"D9 EE DD 5C 24 10 83 3D"> };
constexpr auto audio_time_sig               { pattern::build<"F7 DA 3B C2"> };
constexpr auto osu_manager_sig              { pattern::build<"85 C9"> };
constexpr auto binding_manager_sig          { pattern::build<"8D 45 D8 50 8B 0D"> };
constexpr auto selected_replay_sig          { pattern::build<"8B 46 38 83 78 30 00"> };
constexpr auto osu_username_sig             { pattern::build<"8B 01 8B 40 28 FF 50 18 8B 15"> };
constexpr auto window_manager_sig           { pattern::build<"83 C2 04 8B 0D"> };
constexpr auto score_multiplier_sig         { pattern::build<"8B F1 D9 E8 83 FA 04 0F 83"> };
constexpr auto update_timing_sig            { pattern::build<"D9 C0 DD 05"> };
constexpr auto update_timing_sig_2          { pattern::build<"DE E9 DD 1D"> };
constexpr auto check_timewarp_sig           { pattern::build<"D9 E8 DE F1 DE C9"> };
constexpr auto hom_update_vars_hidden_sig   { pattern::build<"DD 1C 24 8B CE 8B 01 8B 40 . FF 50 . DD 5E . 8B 7E ."> };
