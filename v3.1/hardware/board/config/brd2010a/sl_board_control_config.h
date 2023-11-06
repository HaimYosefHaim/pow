#ifndef SL_BOARD_CONTROL_CONFIG_H
#define SL_BOARD_CONTROL_CONFIG_H

// <<< Use Configuration Wizard in Context Menu >>>

// <q SL_BOARD_ENABLE_VCOM> Enable Virtual COM UART
// <i> Default: 0
#define SL_BOARD_ENABLE_VCOM                    0

// <q SL_BOARD_ENABLE_DISPLAY> Enable Display
// <i> Default: 0
#define SL_BOARD_ENABLE_DISPLAY                 0

// <<< end of configuration section >>>

// <<< sl:start pin_tool >>>

// <gpio> SL_BOARD_ENABLE_VCOM
// $[GPIO_SL_BOARD_ENABLE_VCOM]
#define SL_BOARD_ENABLE_VCOM_PORT               gpioPortA
#define SL_BOARD_ENABLE_VCOM_PIN                8
// [GPIO_SL_BOARD_ENABLE_VCOM]$

// <gpio> SL_BOARD_ENABLE_DISPLAY
// $[GPIO_SL_BOARD_ENABLE_DISPLAY]
#define SL_BOARD_ENABLE_DISPLAY_PORT            gpioPortA
#define SL_BOARD_ENABLE_DISPLAY_PIN             10
// [GPIO_SL_BOARD_ENABLE_DISPLAY]$

// <gpio> SL_BOARD_SELECT_DISPLAY
// $[GPIO_SL_BOARD_SELECT_DISPLAY]
#define SL_BOARD_SELECT_DISPLAY_PORT            gpioPortA
#define SL_BOARD_SELECT_DISPLAY_PIN             8
// [GPIO_SL_BOARD_SELECT_DISPLAY]$

// <<< sl:end pin_tool >>>

#endif // SL_BOARD_CONTROL_CONFIG_H
