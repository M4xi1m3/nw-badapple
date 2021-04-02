#include <extapp_api.h>
#include <stdbool.h>
#include <stdint.h>
#include <string.h>

#include "vdo.h"

void extapp_main() {
    for(unsigned int len = 0; len < vdo_len;) {
        uint64_t start = extapp_millis();
        extapp_waitForVBlank();
        uint8_t frame_type = vdo[len++];
        switch (frame_type) {
            case 1:
            case 2: {
                unsigned int i = 0, j = 0, k = 0;
                bool color = frame_type == 2;
                while (i < 320*240) {
                    uint8_t num = vdo[len++];
                    i += num;
                    j += num;
                    if (j >= 320) {
                        extapp_pushRectUniform(j-num, k, (num - (j - 320)), 1, color ? 0xFFFF : 0);
                        k++;
                        if (j-320 != 0) {
                            extapp_pushRectUniform(0, k, (j - 320), 1, color ? 0xFFFF : 0);
                            j = j - 320;
                        } else {
                            j = 0;
                        }
                    } else {
                        extapp_pushRectUniform(j-num, k, num, 1, color ? 0xFFFF : 0);
                    }
                    color = !color;
                }
                break;
            }
            case 3:
                extapp_pushRectUniform(0, 0, LCD_WIDTH, LCD_HEIGHT, 0);
                break;
            case 4:
                extapp_pushRectUniform(0, 0, LCD_WIDTH, LCD_HEIGHT, 0xFFFF);
                break;
            default:
                break;
        }
        while (extapp_millis() - start < (len%3 == 0 ? 66 : 67));
        
        uint64_t k = extapp_scanKeyboard();
        if (k & SCANCODE_Home) {
            return;
        }
    }
}
