#include <furi.h>
#include <furi_hal.h>

#include <gui/gui.h>
#include <input/input.h>

#include "helloflipper_icons.h"

typedef struct {
    uint8_t x, y;
} ImagePosition;

static ImagePosition image_position = {.x = 0, .y = 0};
static ImagePosition pixel_position = {.x = 0, .y = 0};
static bool pixel_visible = false;
static uint32_t last_blink_time = 0;

// Screen is 128x64 px
static void app_draw_callback(Canvas* canvas, void* ctx) {
    UNUSED(ctx);

    canvas_clear(canvas);
    canvas_draw_icon(canvas, image_position.x % 128, image_position.y % 64, &I_airplane);
    if (pixel_visible) {
        canvas_draw_line(canvas, pixel_position.x % 128, pixel_position.y % 64, pixel_position.x % 128, pixel_position.y % 64);
    }
}

static void app_input_callback(InputEvent* input_event, void* ctx) {
    furi_assert(ctx);

    FuriMessageQueue* event_queue = ctx;
    furi_message_queue_put(event_queue, input_event, FuriWaitForever);
}

int32_t helloflipper_main(void* p) {
    UNUSED(p);
    FuriMessageQueue* event_queue = furi_message_queue_alloc(8, sizeof(InputEvent));

    ViewPort* view_port = view_port_alloc();
    view_port_draw_callback_set(view_port, app_draw_callback, view_port);
    view_port_input_callback_set(view_port, app_input_callback, event_queue);

    Gui* gui = furi_record_open(RECORD_GUI);
    gui_add_view_port(gui, view_port, GuiLayerFullscreen);

    InputEvent event;

    bool running = true;
    while(running) {
        if(furi_message_queue_get(event_queue, &event, 100) == FuriStatusOk) {
            if((event.type == InputTypePress) || (event.type == InputTypeRepeat)) {
                switch(event.key) {
                case InputKeyLeft:
                    image_position.x -= 2;
                    break;
                case InputKeyRight:
                    image_position.x += 2;
                    break;
                case InputKeyUp:
                    image_position.y -= 2;
                    break;
                case InputKeyDown:
                    image_position.y += 2;
                    break;
                case InputKeyOk:
                    pixel_visible = true;
                    pixel_position.x = image_position.x + 16;
                    pixel_position.y = image_position.y + 16;
                    last_blink_time = xTaskGetTickCount();
                    break;
                default:
                    running = false;
                    break;
                }
            }
        }

        if (pixel_visible) {
            uint32_t current_time = xTaskGetTickCount();
            if (current_time - last_blink_time >= 500) {
                pixel_visible = !pixel_visible;
                last_blink_time = current_time;
            }
            pixel_position.x += 1;
        }

        view_port_update(view_port);
    }

    view_port_enabled_set(view_port, false);
    gui_remove_view_port(gui, view_port);
    view_port_free(view_port);
    furi_message_queue_free(event_queue);

    furi_record_close(RECORD_GUI);

    return 0;
}
