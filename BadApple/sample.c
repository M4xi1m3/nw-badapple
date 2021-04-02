#include <extapp_api.h>
#include <stdbool.h>
#include <stdint.h>
#include <string.h>

#include "vdo.h"

void extapp_main() {
    for(unsigned int i = 0; i < vdo_len;) {
        uint8_t frame_type = vdo[i++];
        switch (frame_type) {
            case 3:
                extapp_pushRectUniform(0, 0, LCD_WIDTH, LCD_HEIGHT, 0);
                break;
            case 4:
                extapp_pushRectUniform(0, 0, LCD_WIDTH, LCD_HEIGHT, 0xFFFF);
                break;
            case 0: {
                for (unsigned int j = 0; j < 240; j++) {
                    uint8_t line_type = vdo[i++];
                    switch(line_type) {
                        case 1:
                        case 2: {
                            unsigned int total_len = 0;
                            bool color = line_type == 2;
                            while (total_len < 320) {
                                uint8_t num = vdo[i++];
                                extapp_pushRectUniform(total_len, j, num, 1, color ? 0xFFFF : 0);
                                color = !color;
                                total_len += num;
                            }
                            break;
                        }
                        case 3:
                            extapp_pushRectUniform(0, j, LCD_WIDTH, 1, 0);
                            break;
                        case 4:
                            extapp_pushRectUniform(0, j, LCD_WIDTH, 1, 0xFFFF);
                            break;
                        default:
                            break;
                    }
                }
                break;
            }
            default:
                break;
        }
        uint64_t k = extapp_scanKeyboard();
        if (k & SCANCODE_Home) {
            return;
        }
        extapp_waitForVBlank();
        extapp_waitForVBlank();
    }

    extapp_msleep(1000);
}
