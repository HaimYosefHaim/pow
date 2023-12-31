/***************************************************************************//**
 * @file 
 * @brief sl_flex_ble_protocol_config.h
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

#ifndef SL_FLEX_UTIL_BLE_PROTOCOL_CONFIG_H
#define SL_FLEX_UTIL_BLE_PROTOCOL_CONFIG_H

#include "sl_flex_util_ble_protocol_types.h"

// <<< Use Configuration Wizard in Context Menu >>>

// <h> Bluetooth LE Settings
// <h> BLE: Transition Times
// <o SL_RAIL_UTIL_PROTOCOL_BLE_TIMING_IDLE_TO_RX_US> Transition time (microseconds) from idle to RX
// <0-65535:1>
// <i> Default: 100
#define SL_RAIL_UTIL_PROTOCOL_BLE_TIMING_IDLE_TO_RX_US  100
// <o SL_RAIL_UTIL_PROTOCOL_BLE_TIMING_TX_TO_RX_US> Transition time (microseconds) from TX to RX
// <0-65535:1>
// <i> Default: 150
#define SL_RAIL_UTIL_PROTOCOL_BLE_TIMING_TX_TO_RX_US  150
// <o SL_RAIL_UTIL_PROTOCOL_BLE_TIMING_IDLE_TO_TX_US> Transition time (microseconds) from idle to TX
// <0-65535:1>
// <i> Default: 100
#define SL_RAIL_UTIL_PROTOCOL_BLE_TIMING_IDLE_TO_TX_US  100
// <o SL_RAIL_UTIL_PROTOCOL_BLE_TIMING_RX_TO_TX_US> Transition time (microseconds) from RX to TX
// <0-65535:1>
// <i> Default: 150
#define SL_RAIL_UTIL_PROTOCOL_BLE_TIMING_RX_TO_TX_US  150
// </h>

// <h> BLE: RX Search Timeouts
// <e SL_RAIL_UTIL_PROTOCOL_BLE_TIMING_RX_SEARCH_TIMEOUT_AFTER_IDLE_ENABLE> Enable RX Search timeout after Idle
// <i> Default: 0
#define SL_RAIL_UTIL_PROTOCOL_BLE_TIMING_RX_SEARCH_TIMEOUT_AFTER_IDLE_ENABLE 0
// <o SL_RAIL_UTIL_PROTOCOL_BLE_TIMING_RX_SEARCH_TIMEOUT_AFTER_IDLE_US> Max time (microseconds) radio will search for packet when coming from idle
// <1-65535:1>
// <i> Default: 65535
#define SL_RAIL_UTIL_PROTOCOL_BLE_TIMING_RX_SEARCH_TIMEOUT_AFTER_IDLE_US  65535
// </e>
// <e SL_RAIL_UTIL_PROTOCOL_BLE_TIMING_RX_SEARCH_TIMEOUT_AFTER_TX_ENABLE> Enable RX Search timeout after TX
// <i> Default: 0
#define SL_RAIL_UTIL_PROTOCOL_BLE_TIMING_RX_SEARCH_TIMEOUT_AFTER_TX_ENABLE 0
// <o SL_RAIL_UTIL_PROTOCOL_BLE_TIMING_RX_SEARCH_TIMEOUT_AFTER_TX_US> Max time (microseconds) radio will search for packet when coming from TX
// <1-65535:1>
// <i> Default: 65535
#define SL_RAIL_UTIL_PROTOCOL_BLE_TIMING_RX_SEARCH_TIMEOUT_AFTER_TX_US  65535
// </e>
// </h>
// </h>

#endif // SL_FLEX_UTIL_BLE_PROTOCOL_CONFIG_H
