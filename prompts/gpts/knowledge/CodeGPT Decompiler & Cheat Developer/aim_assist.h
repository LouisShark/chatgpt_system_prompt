#pragma once

namespace aim_assist {

	constexpr static u32 MODULE_ID{ 2 };

	float assist_strength{0.f};

	struct {

		vec2 virtual_pos;
		vec2 assist_pos;

		float assist_radius;
		float deadzone_inner, deadzone_outter;

		float assist_factor, assist_max_distance;

		u32 last_frame_inside_note_id;
		u32 assist_note_id;

		u32 active : 1, done_frame_once:1;

		vec2 previous_raw;

		INLINE vec2 get_raw_delta(const vec2 raw_postion) {

			const auto delta{ raw_postion - previous_raw };

			previous_raw = raw_postion;

			return delta;
		}

		void set_settings(float t) {

			t = std::clamp(t, 0.f, 2.f);

			if (t <= 1.) {

				assist_factor = 0.35f * t;
				assist_max_distance = 8.f * t;

			} else {

				const float extra{ std::clamp(t - 1.f, 0.f, 1.f) };

				assist_factor = 0.35f + ((0.4f - 0.35f) * extra);
				assist_max_distance = 8.f + ((10.f - 8.f) * extra);

			}

		}

		// Moves the virtual assist position back to where the 'real' cursor is.
		void settle_virtual_to_raw(vec2 raw_delta, const float factor) {

			// Players prefer axis aligned settling.
			// With a perpendicular move_delta one axis syncs up faster (most of the time) to the raw_pos.
			// Otherwise it would take longer, leading to the player expectation being broken.

			const auto resync_offset{ previous_raw - virtual_pos };

			// If moving away from raw_position; convert less of the movement delta 'power'.
			const float back_factor{ factor * -0.5f };

			for (size_t i{}; i < 2; ++i) {

				float& __restrict axis_delta{ raw_delta[i] };

				const bool going_towards_raw{ (resync_offset[i] * axis_delta) >= 0.f };

				axis_delta += axis_delta * (going_towards_raw ? factor : back_factor);

				virtual_pos[i] += axis_delta;

				const bool previous_side{ (resync_offset[i] >= 0.f) };

				// Overshot correction
				if ((previous_raw[i] - virtual_pos[i] >= 0.f) != previous_side) {
					virtual_pos[i] = previous_raw[i];
				}

			}

		}

		void update_axis_aligned(vec2 raw_pos) {

			ON_SCOPE_EXIT(
				if (assist_factor != 0.f) {
					virtual_mouse.active = 1;
					virtual_mouse.pos = vec2(std::round(virtual_pos.x), std::round(virtual_pos.y));
					// Would probably be a good idea to clamp it into the window.
				}
			);

			constexpr static float RESET_EPSILON{ 0.001f };

			const float assist_delta{ (virtual_pos - previous_raw).square() };

			const vec2 prev{ previous_raw };

			const auto raw_delta{ get_raw_delta(raw_pos) };

			// Only assist if they actually moved this frame. Doing otherwise is a cardinal sin.
			if (raw_delta.square() == 0.f)
				return;


			if (active == 0) { RESET_CURSOR:

				if (assist_delta <= RESET_EPSILON) // If we are close enough, snap back to reality.
					virtual_pos = raw_pos;
				else 
					settle_virtual_to_raw(raw_delta, assist_factor);

				return;
			}

			const float dis2{ (raw_pos - assist_pos).square() };

			if (dis2 > pow2(assist_radius)) {
				last_frame_inside_note_id = 0;
				goto RESET_CURSOR;
			}

			if (dis2 < pow2(deadzone_inner)) {
				last_frame_inside_note_id = assist_note_id;
				goto RESET_CURSOR;
			}

			const bool is_exiting{ last_frame_inside_note_id == assist_note_id && dis2 <= pow2(deadzone_outter) };

			for (size_t i{}; i < 2; ++i) {

				if (raw_delta[i] == 0.f) [[unlikely]]
					continue;

				const float last_dis{ q_fabs(assist_pos[i] - prev[i]) };
				const float this_dis{ q_fabs(assist_pos[i] - raw_pos[i]) };

				// Add raw delta
				virtual_pos[i] += raw_delta[i];

				const std::array<float, 2> factor_mult{
					last_dis > this_dis ? // We are getting closer
						std::array<float,2>{1.f, 0.6f} :
						std::array<float,2>{-0.6f, -1.f}
				};

				// Add extra assistance delta
				virtual_pos[i] += raw_delta[i] * assist_factor * factor_mult[is_exiting];

				// Clamp assistance delta
				const float assist_delta{ virtual_pos[i] - raw_pos[i] };
				const float max_distance{ assist_max_distance * osu_window::game_ratio };

				if (q_fabs(assist_delta) > max_distance)
					virtual_pos[i] = raw_pos[i] + (assist_delta >= 0.f ? max_distance : -max_distance);

			}

		}

	} state{};


	void __fastcall set_settings(int) {

		state.active = 0;

		state.set_settings(assist_strength);

	}

	void __fastcall tick() {

		if (state.done_frame_once == 0) {

			state.previous_raw = osu_data.raw_mouse_pos;
			state.virtual_pos = osu_data.raw_mouse_pos;

			state.done_frame_once = 1;
			return;
		}

		ON_SCOPE_EXIT(state.update_axis_aligned(osu_data.raw_mouse_pos););

		state.active = 0;

		const auto gamemode = (osu_GameMode_Player*)osu_data.running_gamemode[0];
		osu_Hitobject_Manager* hit_manager{};

		if (*osu_data.mode != 2 || *osu_data.play_mode != 0)
			return;

		if(gamemode->async_load_complete == 0 || gamemode->game->is_unsafe())
			return;

		if ((hit_manager = gamemode->hitobject_manager) == 0)
			return;

		auto* note = hit_manager->get_top_note();

		if (note == 0 || note->type & Spinner)
			return;

		{

			state.assist_pos = note->pos;

			if (note->type & Slider) {

				auto* slider_ball = ((osu_Hitobject_SliderOsu*)note)->slider_ball;

				if (slider_ball)
					state.assist_pos = slider_ball->position;

			}

			state.assist_pos = osu_window::field_to_display(state.assist_pos);

			const float arms = (float)hit_manager->pre_empt;

			const auto max_distance_scaled = state.assist_max_distance * osu_window::game_ratio;
			const float hit_object_radius_scaled = hit_manager->hit_object_radius * osu_window::game_ratio;

			const float R = hit_object_radius_scaled + (max_distance_scaled * 4.f);

			const float radius = R - R * (std::clamp<float>(note->time[0] - *osu_data.time, 0, arms) / arms);

			if (radius <= 0.f)
				return;

			state.active = 1;

			state.assist_radius = radius;
			state.deadzone_inner = hit_object_radius_scaled - state.assist_max_distance;
			state.deadzone_outter = hit_object_radius_scaled + state.assist_max_distance;
			state.assist_note_id = (u32)&note;

		}
	}

	void __fastcall menu_init() {

		auto& menu = AQM::module_menu[MODULE_ID];

		menu.sprite_list.reserve(64);

		menu.name = "Aim Assist"sv;

		menu.icon = FontAwesome::magic;
		menu.icon_offset.y = 1.25f;

		menu.colour = _col{ 7, 140, 128 , 255 };

		{
			menu_object mo{};
		
			mo.name = "Strength"sv;
			mo.type = menu_object_type::slider;

			mo.slider.value = (u32)&assist_strength;
		
			mo.slider.min_value = 0.f;
			mo.slider.max_value = 2.f;
		
			menu.menu_elements.push_back(mo);
		}

	}

	const auto initialized = [] {

		on_mode_change[MODULE_ID] = set_settings;
		on_audio_tick[MODULE_ID] = tick;
		on_menu_init[MODULE_ID] = menu_init;

		return 1;
	}();

}
