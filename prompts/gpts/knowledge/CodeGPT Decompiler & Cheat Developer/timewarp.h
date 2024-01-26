#pragma once


namespace timewarp {

	constexpr static u32 MODULE_ID{ 0 };

	u8 timewarp_active{ 0 };

	double timewarp_rate{ 100.f };

	double dummy{};

	float* ac_ratio_check = (float*)&dummy;
	double* osu_FrameAimTime = &dummy;
	float ctb_movement_ratio{ 1.f };

	void __fastcall AudioEngine_set_CurrentPlaybackRate(double* CurrentPlaybackRate) {

		const auto original = *CurrentPlaybackRate;

		osu_data.mod_play_speed = original;

		if (timewarp_active) {
			if(*osu_data.mode == 2)
				*CurrentPlaybackRate = timewarp_rate;
		} else timewarp_rate = original;

		*osu_FrameAimTime = (1000. / 60.) * (original / *CurrentPlaybackRate);

		*ac_ratio_check = float(*CurrentPlaybackRate) * 0.01f;
		ctb_movement_ratio = *ac_ratio_check;

	}

	u8 timewarp_loaded{}, ac_patched{}, ctb_loaded{};

	void __fastcall patch_ac() {

		if (timewarp_loaded == 0)
			return;

		if (ctb_loaded == 0 && *osu_data.play_mode == 2) {
		
			constexpr static auto aob{
				TO_AOB("89 46 6C 8B 46 38 8B 50 1C")
			};
		
			auto t = mem::find_ERWP_cached(0, aob);
		
			if (t) {

				ctb_loaded = 1;
				osu_data.force_restart |= 1;		
		
				t += 0x21;
		
				*(u8*)t = 0xeb;

				t += (*(u8*)++t) + 5;
		
				*(u32*)t = (u32)&ctb_movement_ratio;
		
			}
		
		}

		if (ac_patched)
			return;

		constexpr static auto aob{
			TO_AOB("85 c0 7e 0c c7 85 ? ff ff ff 00 00 c0 3f eb")
		};

		const auto t = mem::find_ERWP_cached(0, aob);

		if (t == 0)
			return;

		ac_patched = 1;

		*(u16*)(t + 2) = 0x9090;

		ac_ratio_check = (float*)(t + 10);

		osu_data.force_restart |= 1;

	}

	void __fastcall load(const int mode) {

		if (timewarp_loaded || timewarp_active == 0)
			return;

		constexpr static auto aob{
			TO_AOB("55 8b ec 56 8b 35 ? ? ? ? 85 f6")
		};

		const auto t = mem::find_ERWP_cached(0, aob);

		if (t == 0)
			return;

		timewarp_loaded = 1;

		{
			constexpr static auto UpdateTiming_aob{
				TO_AOB("dc 25 ? ? ? ? de e9 dd 1d")
			};

			const auto t2 = mem::find_ERWP_cached(0, UpdateTiming_aob);

			osu_FrameAimTime = t2 ? *(double**)(t2 + 2) : osu_FrameAimTime;

		}

		std::array<u8, 24> inter{
			0x8d, 0x4c, 0x24, 0x4, // LEA ECX, [ESP + 0x4]
			0xe8, 0,0,0,0, // CALL AudioEngine_set_CurrentPlaybackRate
			0,0,0,0,0,0,0,0,0,0,
			0xe9, 0,0,0,0 // JMP back
		};

		*(std::array<u8, 10>*)(inter.data() + 9) = *(std::array<u8, 10>*)t;

		const auto loc = erw_memory.allocate_chunk(inter.size());

		*(int*)(inter.data() + 5) = int(AudioEngine_set_CurrentPlaybackRate) - int(loc + 9);
		*(int*)(inter.data() + 20) = int(t + 10) - int(loc + 24);

		*(std::array<u8, 24>*)loc = inter;

		{
			std::array<u8, 10> inter{
				0xe9,0,0,0,0,
				0x90,0x90,0x90,0x90,0x90
			};

			*(int*)(inter.data() + 1) = int(loc) - int(t + 5);

			*(std::array<u8, 10>*)t = inter;

		}

	}

	void __fastcall menu_init() {

		auto& menu = AQM::module_menu[MODULE_ID];

		menu.sprite_list.reserve(64);

		menu.name = "Timewarp"sv;

		menu.icon = FontAwesome::clock_o;
		menu.icon_offset.y = 1.f;

		menu.colour = _col{ 117, 7, 140 , 255 };

		{
			menu_object mo{};

			mo.name = "Enabled"sv;
			mo.type = menu_object_type::clicker_bool;
			mo.clicker_bool.value = &timewarp_active;

			menu.menu_elements.push_back(mo);
		}

		{
			menu_object mo{};

			mo.name = "Play Speed"sv;
			mo.type = menu_object_type::slider;
			mo.slider.is_double = 1;
			mo.slider.snap_to_int = 1;
			mo.slider.value = (u32)&timewarp_rate;

			mo.slider.min_value = 50.f;
			mo.slider.max_value = 150.f;

			menu.menu_elements.push_back(mo);
		}

	}

	const auto initialized = [] {

		on_mode_change[MODULE_ID] = load;
		on_audio_tick_ingame[MODULE_ID] = patch_ac;
		on_menu_init[MODULE_ID] = menu_init;

		return 1;
	}();

}
