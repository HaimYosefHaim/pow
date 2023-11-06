/***************************************************************************//**
 * @file 
 * @brief app_cli.c
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
#include <string.h>
#include PLATFORM_HEADER
#include "em_chip.h"
#include "stack/include/ember.h"
#include "hal/hal.h"
#include "sl_cli.h"
#include "sl_flex_assert.h"
#include "app_process.h"
#include "sl_light_switch.h"

// -----------------------------------------------------------------------------
//                              Macros and Typedefs
// -----------------------------------------------------------------------------
#define ENABLED  "enabled"
#define DISABLED "disabled"

// -----------------------------------------------------------------------------
//                          Static Function Declarations
// -----------------------------------------------------------------------------
// Connect Tx options
static EmberMessageOptions tx_options = EMBER_OPTIONS_NONE;
// -----------------------------------------------------------------------------
//                                Global Variables
// -----------------------------------------------------------------------------
///This structure contains all the flags used in the state machine
extern light_application_flags_t state_machine_flags;

// -----------------------------------------------------------------------------
//                                Static Variables
// -----------------------------------------------------------------------------

// -----------------------------------------------------------------------------
//                          Public Function Definitions
// -----------------------------------------------------------------------------

//-----------------------------------------------------------------------------

/******************************************************************************
 * CLI - Form a local network
 *****************************************************************************/
void cli_form(sl_cli_command_arg_t *arguments)
{
  (void) arguments;
  state_machine_flags.form_network_request = true;
}

/******************************************************************************
 * CLI - leave command
 *****************************************************************************/
void cli_leave(sl_cli_command_arg_t *arguments)
{
  (void) arguments;
  emberResetNetworkState();
  state_machine_flags.leave_request = true;
}

/******************************************************************************
 * CLI - reset command
 *****************************************************************************/
void cli_reset(sl_cli_command_arg_t *arguments)
{
  (void) arguments;
  halReboot();
}

/******************************************************************************
 * CLI - info command
 * It lists the main attributes of the current state of the node
 *****************************************************************************/
void cli_info(sl_cli_command_arg_t *arguments)
{
  (void) arguments;
  char* is_ack = ((tx_options & EMBER_OPTIONS_ACK_REQUESTED) ? ENABLED : DISABLED);
  char* is_security = ((tx_options & EMBER_OPTIONS_SECURITY_ENABLED) ? ENABLED : DISABLED);
  char* is_high_prio = ((tx_options & EMBER_OPTIONS_HIGH_PRIORITY) ? ENABLED : DISABLED);

  APP_INFO("Info:\n");
  APP_INFO("         MCU Id: 0x%llX\n", SYSTEM_GetUnique());
  APP_INFO("  Network state: 0x%02X\n", emberNetworkState());
  APP_INFO("      Node type: 0x%02X\n", emberGetNodeType());
  APP_INFO("        Node id: 0x%04X\n", emberGetNodeId());
  APP_INFO("         Pan id: 0x%04X\n", emberGetPanId());
  APP_INFO("        Channel: %d\n", (uint16_t)emberGetRadioChannel());
  APP_INFO("          Power: %d\n", (int16_t)emberGetRadioPower());
  APP_INFO("     TX options: MAC acks %s, security %s, priority %s\n", is_ack, is_security, is_high_prio);
}

/******************************************************************************
 * CLI - set PAN ID
 *****************************************************************************/
void cli_set_pan_id(sl_cli_command_arg_t *arguments)
{
  uint16_t pan_id = sl_cli_get_argument_uint16(arguments, 0);
  sl_set_pan_id(pan_id);
}

/******************************************************************************
 * CLI - set the communication channel
 *****************************************************************************/
void cli_set_channel(sl_cli_command_arg_t *arguments)
{
  uint16_t channel = sl_cli_get_argument_uint16(arguments, 0);
  sl_set_channel(channel);
}
