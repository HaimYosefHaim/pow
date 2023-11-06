/***************************************************************************//**
 * @file 
 * @brief app_process.c
 *******************************************************************************
 * # License
 * <b>Copyright 2018 Silicon Laboratories Inc. www.silabs.com</b>
 *******************************************************************************
 *
 * SPDX-License-Identifier: Zlib
 *
 * The licensor of this software is Silicon Laboratories Inc.
 *
 * This software is provided 'as-is', without any express or implied
 * warranty. In no event will the authors be held liable for any damages
 * arising from the use of this software.
 *
 * Permission is granted to anyone to use this software for any purpose,
 * including commercial applications, and to alter it and redistribute it
 * freely, subject to the following restrictions:
 *
 * 1. The origin of this software must not be misrepresented; you must not
 *    claim that you wrote the original software. If you use this software
 *    in a product, an acknowledgment in the product documentation would be
 *    appreciated but is not required.
 * 2. Altered source versions must be plainly marked as such, and must not be
 *    misrepresented as being the original software.
 * 3. This notice may not be removed or altered from any source distribution.
 *
 ******************************************************************************/

// -----------------------------------------------------------------------------
//                                   Includes
// -----------------------------------------------------------------------------
#include "sl_component_catalog.h"
#include "app_init.h"
#include "app_process.h"
#include "app_graphics.h"
#include "app_button.h"
#include "app_graphics.h"
#include "app_measurement.h"
#include "app_menu.h"

#if defined(SL_CATALOG_KERNEL_PRESENT)
#include "app_task_init.h"
#include "app_bluetooth.h"
#endif

// -----------------------------------------------------------------------------
//                              Macros and Typedefs
// -----------------------------------------------------------------------------
///Define to allow detailed RAIL error printout
//#define DEBUG_RAIL_EVENTS
// -----------------------------------------------------------------------------
//                          Static Function Declarations
// -----------------------------------------------------------------------------

// -----------------------------------------------------------------------------
//                                Global Variables
// -----------------------------------------------------------------------------
/// State machine variable to hold the current state
state_t state = INFO_SCREEN;

// -----------------------------------------------------------------------------
//                                Static Variables
// -----------------------------------------------------------------------------
/// As the LCD don't need to be refresh always, use this to set when to refresh
/// the hole LCD display
static bool refresh_screen = false;

// -----------------------------------------------------------------------------
//                          Public Function Definitions
// -----------------------------------------------------------------------------
/*******************************************************************************
 * State set for other part of the application.
 *
 * @param next_state What should be the next state in the state machine
 * @returns None
 ******************************************************************************/
void set_next_state(state_t next_state)
{
  state = next_state;
}

/*******************************************************************************
 * LCD screen needs update.
 *
 * @param None
 * @returns None
 ******************************************************************************/
void request_refresh_screen(void)
{
  refresh_screen = true;
}

/*******************************************************************************
 * The function is used for Application logic.
 * @brief Application state machine, called infinitely
 *
 * @param None
 * @returns None
 ******************************************************************************/
void app_process_action(void)
{
  switch (state) {
    case INFO_SCREEN:
      if (refresh_screen) {
        graphics_draw_init_screen();
        refresh_screen = false;
      }
      if (get_and_clear_button_state(BUTTON_0) || get_and_clear_button_state(BUTTON_1)) {
        end_init_timer();
        set_next_state(MENU_SCREEN);
        refresh_screen = true;
      }
      break;
    case MENU_SCREEN:
      if (get_and_clear_button_state(BUTTON_1)) {
        menu_next_item();
        refresh_screen = true;
      } else if (get_and_clear_button_state(BUTTON_0)) {
        menu_item_action();
        refresh_screen = true;
      }
      if (refresh_screen) {
        if (state == MENU_SCREEN) {
          graphics_draw_menu();
          refresh_screen = false;
        }
      }
      break;
    case START_MEASURMENT:
      range_test_init();
      refresh_screen = false;
      // to prevent other handlers to occupy the radio
      set_all_radio_handlers_to_idle();
      if (range_test_settings.radio_mode == RADIO_MODE_RX) {
        set_next_state(RECEIVE_MEASURMENT);
        receive_setup_radio();
        range_test_reset_values();
        graphics_draw_rx_screen();
      } else if (range_test_settings.radio_mode == RADIO_MODE_TX) {
        set_next_state(SEND_MEASURMENT);
#if defined(SL_CATALOG_KERNEL_PRESENT)
        if (!is_bluetooth_connected()) {
          deactivate_bluetooth();
        }
#endif
        graphics_draw_tx_screen();
      }
#if defined(SL_CATALOG_KERNEL_PRESENT)
      {
        RTOS_ERR err;
        OSFlagPost(&proprietary_event_flags, RANGETEST_FLAG, OS_OPT_POST_FLAG_SET, &err);
      }
#endif
      break;
    case RECEIVE_MEASURMENT:
      refresh_screen = receive_measurment();
      if (refresh_screen) {
        graphics_draw_rx_screen();
#if defined(SL_CATALOG_KERNEL_PRESENT)
        advertise_received_data(range_test_measurement.rssi_latch_value,
                                range_test_measurement.packets_received_counter,
                                range_test_measurement.packets_received_correctly);
#endif
      }

#if defined(SL_CATALOG_KERNEL_PRESENT)
      manage_bluetooth_restart();
#endif

      if (get_and_clear_button_state(BUTTON_1)) {
        stop_recive_measurement();
        set_next_state(MENU_SCREEN);
        refresh_screen = true;
      }
      break;
    case SEND_MEASURMENT:
      if (range_test_measurement.tx_is_running) {
        refresh_screen = send_measurment();
      }
      if (refresh_screen) {
        graphics_draw_tx_screen();
      }
      if (get_and_clear_button_state(BUTTON_1)) {
        set_next_state(MENU_SCREEN);
        refresh_screen = true;
        range_test_measurement.tx_is_running = false;
        set_all_radio_handlers_to_idle();
#if defined(SL_CATALOG_KERNEL_PRESENT)
        if (!is_bluetooth_connected()) {
          activate_bluetooth();
        }
#endif
      } else if (get_and_clear_button_state(BUTTON_0)) {
        range_test_measurement.tx_is_running = !range_test_measurement.tx_is_running;
        range_test_reset_values();
        refresh_screen = true;
#if defined(SL_CATALOG_KERNEL_PRESENT)
        if (range_test_measurement.tx_is_running) {
          if (!is_bluetooth_connected()) {
            deactivate_bluetooth();
          }
        } else {
          if (!is_bluetooth_connected()) {
            activate_bluetooth();
          }
        }
#endif
      }

      break;
    default:
      break;
  }
  print_log();
#if defined(DEBUG_RAIL_EVENTS)
  print_errors_from_rail_handler();
#endif
#if defined(SL_CATALOG_KERNEL_PRESENT)
  send_bluetooth_indications();
#endif
}

// -----------------------------------------------------------------------------
//                          Static Function Definitions
// -----------------------------------------------------------------------------
