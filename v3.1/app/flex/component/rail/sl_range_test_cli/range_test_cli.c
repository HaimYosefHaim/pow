/***************************************************************************//**
 * @file 
 * @brief range_test_cli.c
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
#include <stdlib.h>
#include <stddef.h>
#include "sl_cli.h"
#include "sl_flex_assert.h"
#include "app_measurement.h"
#include "app_menu.h"
#include "app_process.h"
#include "em_common.h"

#if defined(SL_CATALOG_KERNEL_PRESENT)
#include "app_task_init.h"
#include "app_bluetooth.h"
#include "gatt_db.h"
#endif

// -----------------------------------------------------------------------------
//                              Macros and Typedefs
// -----------------------------------------------------------------------------

// -----------------------------------------------------------------------------
//                          Static Function Declarations
// -----------------------------------------------------------------------------
/*******************************************************************************
 * Apply changes that were made, update lcd and allow program to run in DMP
 ******************************************************************************/
static void apply_changes(void);
// -----------------------------------------------------------------------------
//                                Global Variables
// -----------------------------------------------------------------------------

// -----------------------------------------------------------------------------
//                                Static Variables
// -----------------------------------------------------------------------------

// -----------------------------------------------------------------------------
//                          Public Function Definitions
// -----------------------------------------------------------------------------
/*******************************************************************************
 * @brief  This function is defined in app_measurement_standard.c
 *         If that file is not present then it is an only custom phy range test
 ******************************************************************************/
void print_standard_name(char *print_buffer);

/*******************************************************************************
 * Checks if selected standard phy is supported before setting it
 * @param index
 ******************************************************************************/
SL_WEAK bool std_phy_is_supported(uint8_t index)
{
  (void)index;
  return false;
}

/*******************************************************************************
 * Checks id selected phy is standard before setting it
 * @param index: selected phy index
 ******************************************************************************/
SL_WEAK bool is_phy_standard(uint8_t index)
{
  (void)index;
  return false;
}

/*******************************************************************************
 * CLI - list_phys: List available phys
 ******************************************************************************/
void cli_list_phys(sl_cli_command_arg_t *arguments)
{
  // Eliminate compiler warning
  (void) arguments;
  uint8_t phy_list[256] = { 0 };
  uint8_t phy_list_length = 0;
  phy_list_generation(phy_list, &phy_list_length);
  phy_list[phy_list_length - 1] = 0;
  APP_INFO("Available phys:   %s\n", phy_list);
}

/*******************************************************************************
 * CLI - get_mode: Get current radio mode of the device
 ******************************************************************************/
void cli_get_mode(sl_cli_command_arg_t *arguments)
{
  // Eliminate compiler warning
  (void) arguments;
  APP_INFO("Mode:             %s\n", range_test_settings.radio_mode == RADIO_MODE_RX ? "RX" : "TX");
}

/*******************************************************************************
 * CLI - set_mode: Set current radio mode of the device
 ******************************************************************************/
void cli_set_mode(sl_cli_command_arg_t *arguments)
{
  uint8_t radio_mode = sl_cli_get_argument_uint8(arguments, 0);
  if (radio_mode < 2) {
    range_test_settings.radio_mode = (radio_modes_t)radio_mode;
    APP_INFO("Mode:             %s\n", range_test_settings.radio_mode == RADIO_MODE_RX ? "RX" : "TX");
    apply_changes();
#if defined(SL_CATALOG_KERNEL_PRESENT)
    add_bluetooth_indication(gattdb_radioMode);
#endif
  } else {
    APP_INFO("Please use 0 for RX and 1 for TX mode\n");
  }
}

/*******************************************************************************
 * CLI - get_phy: Get current radio phy of the device
 ******************************************************************************/
void cli_get_phy(sl_cli_command_arg_t *arguments)
{
  // Eliminate compiler warning
  (void) arguments;
  char phy_name[13u];
  if (!is_current_phy_standard()) {
    sprintf(phy_name, "custom_%u", (range_test_settings.current_phy));
  } else {
    print_standard_name(phy_name);
  }
  APP_INFO("PHY:              %d:%s\n", range_test_settings.current_phy, phy_name);
}

/*******************************************************************************
 * CLI - set_phy: Set current radio phy of the device
 ******************************************************************************/
void cli_set_phy(sl_cli_command_arg_t *arguments)
{
  // Eliminate compiler warning
  bool new_phy_applied = false;
  uint8_t phy = sl_cli_get_argument_uint8(arguments, 0);
  if (phy < number_of_phys) {
    if (!is_phy_standard(phy)) {
      range_test_settings.current_phy = phy;
      new_phy_applied = true;
    } else {
      if (std_phy_is_supported(phy)) {
        range_test_settings.current_phy = phy;
        new_phy_applied = true;
      } else {
        APP_INFO("This phy is not supported! Please use list_phys to see which phys are supported\n");
      }
    }
  } else {
    APP_INFO("Out of range! Please use list_phys to see phys\n");
  }

  if (new_phy_applied) {
    apply_new_phy(true);
    apply_changes();
  #if defined(SL_CATALOG_KERNEL_PRESENT)
    add_bluetooth_indication(gattdb_phy);
  #endif
    cli_get_phy(arguments);
  }
}

/*******************************************************************************
 * CLI - get_power: Get current tx power of the device
 ******************************************************************************/
void cli_get_power(sl_cli_command_arg_t *arguments)
{
  // Eliminate compiler warning
  (void) arguments;
  uint32_t base_frequency = 0;
  uint32_t channel_spacing = 0;
  int16_t power = 0;
  get_rail_config_data(&base_frequency, &channel_spacing, &power);
  int16_t tx_power = range_test_settings.tx_power;
  APP_INFO("Power:            %+i.%d/%+i.%ddBm\n",
           (tx_power / 10),
           (((tx_power > 0) ? (tx_power) : (-tx_power)) % 10),
           (power / 10),
           (((power > 0) ? (power) : (-power)) % 10));
}

/*******************************************************************************
 * CLI - set_power: Set current tx power of the device
 ******************************************************************************/
void cli_set_power(sl_cli_command_arg_t *arguments)
{
  int16_t power = sl_cli_get_argument_int16(arguments, 0);
  if ((get_min_tx_power_deci_dbm() <= power) && (power <= get_max_tx_power_deci_dbm())) {
    range_test_settings.tx_power = power;
    update_tx_power();
    apply_changes();
    cli_get_power(arguments);
#if defined(SL_CATALOG_KERNEL_PRESENT)
    add_bluetooth_indication(gattdb_txPower);
#endif
  } else {
    APP_INFO("Out of range! Correct range is %d - %d\n", get_min_tx_power_deci_dbm(), get_max_tx_power_deci_dbm());
  }
}

/*******************************************************************************
 * CLI - get_fequency: Get current frequency of the device
 ******************************************************************************/
void cli_get_fequency(sl_cli_command_arg_t *arguments)
{
  // Eliminate compiler warning
  (void) arguments;
  char freq_string[11u];
  uint32_t base_frequency = 0;
  uint32_t channel_spacing = 0;
  int16_t power = 0;
  get_rail_config_data(&base_frequency, &channel_spacing, &power);

  if (base_frequency % 1000000u) {
    sprintf(freq_string,
            "%u.%02uMHz",
            (uint16_t) (base_frequency / 1000000u),
            (uint16_t) ((base_frequency % 1000000u) / 10000u));
  } else {
    sprintf(freq_string,
            "%uMHz",
            (uint16_t) (base_frequency / 1000000u));
  }

  APP_INFO("Frequency:        %s\n", freq_string);
}

/*******************************************************************************
 * CLI - get_channel_number: Get current channel number of the device
 ******************************************************************************/
void cli_get_channel_number(sl_cli_command_arg_t *arguments)
{
  // Eliminate compiler warning
  (void) arguments;
  APP_INFO("Channel number:   %d\n", range_test_settings.channel);
}

/*******************************************************************************
 * CLI - set_channel_number: Set current channel number of the device
 ******************************************************************************/
void cli_set_channel_number(sl_cli_command_arg_t *arguments)
{
  uint16_t channel = sl_cli_get_argument_uint16(arguments, 0);
  uint16_t start = 0;
  uint16_t end = 0;
  get_rail_channel_range(&start, &end);
  if (start <= channel && channel <= end) {
    range_test_settings.channel = channel;
    apply_changes();
    cli_get_channel_number(arguments);
#if defined(SL_CATALOG_KERNEL_PRESENT)
    add_bluetooth_indication(gattdb_channel);
#endif
  } else {
    APP_INFO("Out of range! Correct range is %d - %d\n", start, end);
  }
}

/*******************************************************************************
 * CLI - get_payload_length: Get current payload length of the device
 ******************************************************************************/
void cli_get_payload_length(sl_cli_command_arg_t *arguments)
{
  // Eliminate compiler warning
  (void) arguments;
  APP_INFO("Payload length:   %d\n", range_test_settings.payload_length);
}

/*******************************************************************************
 * CLI - set_payload_length: Set current payload length of the device
 ******************************************************************************/
void cli_set_payload_length(sl_cli_command_arg_t *arguments)
{
  uint8_t payload_length = sl_cli_get_argument_uint8(arguments, 0);
  uint8_t min = 0;
  uint8_t max = 0;
  get_rail_payload_range(&min, &max);
  if (min <= payload_length && payload_length <= max) {
    range_test_settings.payload_length = payload_length;
    apply_changes();
    cli_get_payload_length(arguments);
#if defined(SL_CATALOG_KERNEL_PRESENT)
    add_bluetooth_indication(gattdb_payload);
#endif
  } else {
    APP_INFO("Out of range! Correct range is %d - %d\n", min, max);
  }
}

/*******************************************************************************
 * CLI - get_packet_count: Get current packet count of the device
 ******************************************************************************/
void cli_get_packet_count(sl_cli_command_arg_t *arguments)
{
  // Eliminate compiler warning
  (void) arguments;
  if (range_test_settings.packets_repeat_number != 0xFFFF) {
    APP_INFO("Packet Count:     %d\n", range_test_settings.packets_repeat_number);
  } else {
    APP_INFO("Packet Count:     Repeat\n");
  }
}

/*******************************************************************************
 * CLI - set_packet_count: Set current packet count of the device
 ******************************************************************************/
void cli_set_packet_count(sl_cli_command_arg_t *arguments)
{
  static uint16_t pktsNum[8u] =
  { 500u, 1000u, 2500u, 5000u, 10000u, 25000u, 50000u, 0xFFFF };
  uint8_t packets_repeat_number = sl_cli_get_argument_uint8(arguments, 0);
  if (packets_repeat_number < 8) {
    range_test_settings.packets_repeat_number = pktsNum[packets_repeat_number];
    apply_changes();
    cli_get_packet_count(arguments);
#if defined(SL_CATALOG_KERNEL_PRESENT)
    add_bluetooth_indication(gattdb_pktsReq);
#endif
  } else {
    APP_INFO("Out of range! Correct range is 0 - 7\n");
  }
}

/*******************************************************************************
 * CLI - get_remote_id: Get current remote id of the device
 ******************************************************************************/
void cli_get_remote_id(sl_cli_command_arg_t *arguments)
{
  // Eliminate compiler warning
  (void) arguments;
  APP_INFO("Remote ID:        %d\n", range_test_settings.destination_id);
}

/*******************************************************************************
 * CLI - set_remote_id: Set current remote id of the device
 ******************************************************************************/
void cli_set_remote_id(sl_cli_command_arg_t *arguments)
{
  uint8_t remote_id = sl_cli_get_argument_uint8(arguments, 0);
  if (remote_id > 32) {
    APP_INFO("Out of range! Correct range is 0 - 32\n");
  } else {
    range_test_settings.destination_id = remote_id;
    apply_changes();
    cli_get_remote_id(arguments);
#if defined(SL_CATALOG_KERNEL_PRESENT)
    add_bluetooth_indication(gattdb_destID);
#endif
  }
}

/*******************************************************************************
 * CLI - get_self_id: Get current self id of the device
 ******************************************************************************/
void cli_get_self_id(sl_cli_command_arg_t *arguments)
{
  // Eliminate compiler warning
  (void) arguments;
  APP_INFO("Self ID:          %d\n", range_test_settings.source_id);
}

/*******************************************************************************
 * CLI - set_self_id: Set current self id of the device
 ******************************************************************************/
void cli_set_self_id(sl_cli_command_arg_t *arguments)
{
  uint8_t self_id = sl_cli_get_argument_uint8(arguments, 0);
  if (self_id > 32) {
    APP_INFO("Out of range! Correct range is 0 - 32\n");
  } else {
    range_test_settings.source_id = self_id;
    apply_changes();
    cli_get_self_id(arguments);
#if defined(SL_CATALOG_KERNEL_PRESENT)
    add_bluetooth_indication(gattdb_srcID);
#endif
  }
}

/*******************************************************************************
 * CLI - get_ma_window_size: Get current MA window size of the device
 ******************************************************************************/
void cli_get_ma_window_size(sl_cli_command_arg_t *arguments)
{
  // Eliminate compiler warning
  (void) arguments;
  APP_INFO("MA Window size:   %d\n", range_test_settings.moving_average_window_size);
}

/*******************************************************************************
 * CLI - set_ma_window_size: Set current MA window size of the device
 ******************************************************************************/
void cli_set_ma_window_size(sl_cli_command_arg_t *arguments)
{
  uint8_t set_ma_window_size = sl_cli_get_argument_uint8(arguments, 0);
  if ( set_ma_window_size == 32
       || set_ma_window_size == 64
       || set_ma_window_size == 128) {
    range_test_settings.moving_average_window_size = set_ma_window_size;
    apply_changes();
    cli_get_ma_window_size(arguments);
    #if defined(SL_CATALOG_KERNEL_PRESENT)
    add_bluetooth_indication(gattdb_maSize);
    #endif
  } else {
    APP_INFO("Not correct value! Please use 32, 64 or 128!\n");
  }
}

/*******************************************************************************
 * CLI - get_usart_log_enable: Get current uart log settings of the device
 ******************************************************************************/
void cli_get_usart_log_enable(sl_cli_command_arg_t *arguments)
{
  // Eliminate compiler warning
  (void) arguments;
  APP_INFO("UART log enabled: %s\n", (range_test_settings.usart_log_enable) ? ("Yes") : ("No"));
}

/*******************************************************************************
 * CLI - set_usart_log_enable: Set current uart log settings of the device
 ******************************************************************************/
void cli_set_usart_log_enable(sl_cli_command_arg_t *arguments)
{
  uint8_t usart_log_enable = sl_cli_get_argument_uint8(arguments, 0);
  if (usart_log_enable < 2) {
    range_test_settings.usart_log_enable = usart_log_enable;
    apply_changes();
    cli_get_usart_log_enable(arguments);
#if defined(SL_CATALOG_KERNEL_PRESENT)
    add_bluetooth_indication(gattdb_log);
#endif
  } else {
    APP_INFO("Out of range! Correct range is 0 - 1\n");
  }
}

/*******************************************************************************
 * CLI - start_measurement: Start the measurement
 ******************************************************************************/
void cli_start_measurement(sl_cli_command_arg_t *arguments)
{
  (void) arguments;
  if (range_test_settings.radio_mode == RADIO_MODE_RX) {
  } else {
    range_test_measurement.tx_is_running = true;
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
  set_next_state(START_MEASURMENT);
  apply_changes();
#if defined(SL_CATALOG_KERNEL_PRESENT)
  add_bluetooth_indication(gattdb_isRunning);
#endif
}

#if defined(SL_CATALOG_KERNEL_PRESENT)
/*******************************************************************************
 * CLI - is_ble_connected: Checks connection status of BLE
 ******************************************************************************/
void cli_is_ble_connected(sl_cli_command_arg_t *arguments)
{
  (void) arguments;
  APP_INFO("BLE is connected: %s\n", (is_bluetooth_connected()) ? ("Yes") : ("No"));
}
#endif

/*******************************************************************************
 * CLI - stop_measurement: Stops the running measurement
 ******************************************************************************/
void cli_stop_measurement(sl_cli_command_arg_t *arguments)
{
  (void) arguments;
  if (range_test_settings.radio_mode == RADIO_MODE_RX) {
    stop_recive_measurement();
  } else {
    range_test_measurement.tx_is_running = false;
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
  set_all_radio_handlers_to_idle();
  set_next_state(MENU_SCREEN);
  apply_changes();
#if defined(SL_CATALOG_KERNEL_PRESENT)
  add_bluetooth_indication(gattdb_isRunning);
#endif
}

/*******************************************************************************
 * CLI - info: Get current configurations of the device
 ******************************************************************************/
void cli_info(sl_cli_command_arg_t *arguments)
{
  // Eliminate compiler warning
//  (void) arguments;
  APP_INFO("Configurations:\n");
  cli_get_mode(arguments);
  cli_get_phy(arguments);
  cli_get_power(arguments);
  cli_get_fequency(arguments);
  cli_get_channel_number(arguments);
  cli_get_payload_length(arguments);
  cli_get_packet_count(arguments);
  cli_get_remote_id(arguments);
  cli_get_self_id(arguments);
  cli_get_ma_window_size(arguments);
  cli_get_usart_log_enable(arguments);
  APP_INFO("\n");
  cli_list_phys(arguments);
#if defined(SL_CATALOG_KERNEL_PRESENT)
  APP_INFO("\n");
  cli_is_ble_connected(arguments);
#endif
}

// -----------------------------------------------------------------------------
//                          Static Function Definitions
// -----------------------------------------------------------------------------
/*******************************************************************************
 * Apply changes that were made, update lcd and allow program to run in DMP
 ******************************************************************************/
void apply_changes(void)
{
  request_refresh_screen();
#if defined(SL_CATALOG_KERNEL_PRESENT)
  RTOS_ERR err;
  OSFlagPost(&proprietary_event_flags, RANGETEST_FLAG,
             OS_OPT_POST_FLAG_SET, &err);
#endif
}
