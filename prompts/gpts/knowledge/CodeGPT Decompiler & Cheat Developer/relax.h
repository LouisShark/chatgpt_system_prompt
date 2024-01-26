#pragma once

#include "config.h"

extern float od_window;
extern float od_window_left_offset;
extern float od_window_right_offset;
extern float od_check_ms;

extern float jumping_window_offset;

extern int wait_hitobjects_min;
extern int wait_hitobjects_max;

extern bool debug_relax;

void relax_on_beatmap_load();
void update_relax(Circle &circle, const int32_t audio_time);
