/***************************************************************************//**
 * @file 
 * @brief Set of APIs for the sl_connect_sdk_ota_bootloader_test_common component.
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
#include PLATFORM_HEADER
#include "stack/include/ember.h"
#include "hal/hal.h"
#include "sl_flex_assert.h"
#include "sl_connect_sdk_ota_bootloader_test_common.h"
#include "sl_connect_sdk_btl-interface.h"
#include "sl_cli.h"

// -----------------------------------------------------------------------------
//                                Global Variables
// -----------------------------------------------------------------------------
/// The image tag the client shall accept.
uint8_t ota_bootloader_test_image_tag = DEFAULT_IMAGE_TAG;
/// Default behavior to OTA resume counter reset.
bool ota_resume_start_counter_reset = DEFAULT_COUNTER_RESET;

// -----------------------------------------------------------------------------
//                          Public Function Definitions
// -----------------------------------------------------------------------------

/**************************************************************************//**
 * Brief description of my_public_function().
 *****************************************************************************/
void cli_bootloader_get_version(sl_cli_command_arg_t *arguments)
{
  (void) arguments;
  uint16_t bl_version;

  emberAfPluginBootloaderInterfaceGetVersion(&bl_version);

  APP_INFO("bootloader version: %d\n", bl_version);
}

/**************************************************************************//**
 * Brief description of my_public_function().
 *****************************************************************************/
void cli_bootloader_init(sl_cli_command_arg_t *arguments)
{
  (void) arguments;

  if (emberAfPluginBootloaderInterfaceInit()) {
    APP_INFO("bootloader init succeeded!\n");
  } else {
    APP_INFO("bootloader init failed! wrong chip?\n");
  }
}

/**************************************************************************//**
 * Brief description of my_public_function().
 *****************************************************************************/
void cli_bootloader_sleep(sl_cli_command_arg_t *arguments)
{
  (void) arguments;

  emberAfPluginBootloaderInterfaceSleep();
  APP_INFO("sleep bootloader and flash part\n");
}

void cli_bootloader_flash_erase(sl_cli_command_arg_t *arguments)
{
  (void) arguments;

  APP_INFO("flash erase started\n");
  emberAfPluginBootloaderInterfaceChipErase();
  ota_resume_start_counter_reset = true;
}

/**************************************************************************//**
 * Brief description of my_public_function().
 *****************************************************************************/
void cli_bootloader_validate_image(sl_cli_command_arg_t *arguments)
{
  (void) arguments;

  if (!emberAfPluginBootloaderInterfaceValidateImage()) {
    APP_INFO("Image is invalid!\n");
  } else {
    APP_INFO("Image is valid!\n");
  }
}

/**************************************************************************//**
 * Brief description of my_public_function().
 *****************************************************************************/
void cli_bootloader_flash_erase_slot(sl_cli_command_arg_t *arguments)
{
  uint32_t slot = sl_cli_get_argument_uint32(arguments, 0);

  APP_INFO("flash erasing slot %lu started\n", slot);

  if ( emberAfPluginBootloaderInterfaceChipEraseSlot(slot) ) {
    APP_INFO("flash erase successful!\n");
  } else {
    APP_INFO("flash erase failed!\n");
  }
}

/**************************************************************************//**
 * Brief description of my_public_function().
 *****************************************************************************/
void cli_bootloader_flash_image(sl_cli_command_arg_t *arguments)
{
  (void) arguments;
  bootloader_flash_image();
}

/**************************************************************************//**
 * Brief description of my_public_function().
 *****************************************************************************/
void cli_bootloader_flash_read(sl_cli_command_arg_t *arguments)
{
  uint32_t address = sl_cli_get_argument_uint32(arguments, 0);
  uint8_t length = sl_cli_get_argument_uint8(arguments, 1);
  uint8_t buff[255];
  uint8_t i;

  if (emberAfPluginBootloaderInterfaceRead(address, length, buff)) {
    APP_INFO("flash read succeeded!\n");
    APP_INFO("address: %lu, length: %d, data:\n", address, length);
    for (i = 0; i < length; i++) {
      APP_INFO("0x%x ", buff[i]);
    }
    APP_INFO("\n");
  } else {
    APP_INFO("flash read failed!\n");
  }
}

/**************************************************************************//**
 * Brief description of my_public_function().
 *****************************************************************************/
void cli_bootloader_flash_write(sl_cli_command_arg_t *arguments)
{
  uint32_t address = sl_cli_get_argument_uint32(arguments, 0);
  size_t length;

  uint8_t *data_buff = sl_cli_get_argument_hex(arguments, 1, &length);

  if (emberAfPluginBootloaderInterfaceWrite(address, length, data_buff)) {
    APP_INFO("flash write succeeded!\n");
  } else {
    APP_INFO("flash write failed!\n");
  }
}

/**************************************************************************//**
 * Brief description of my_public_function().
 *****************************************************************************/
void cli_bootloader_set_tag(sl_cli_command_arg_t *arguments)
{
  uint8_t new_image_tag = 0;
  new_image_tag = sl_cli_get_argument_uint8(arguments, 0);
  if (new_image_tag != ota_bootloader_test_image_tag) {
    ota_bootloader_test_image_tag = new_image_tag;
    ota_resume_start_counter_reset = true;
  }
  APP_INFO("image tag set\n");
}

// -----------------------------------------------------------------------------
//                          Public Function Definitions
// -----------------------------------------------------------------------------
/**************************************************************************//**
 * This function initiates a bootload.
 *****************************************************************************/
void bootloader_flash_image(void)
{
  if (!emberAfPluginBootloaderInterfaceIsBootloaderInitialized()) {
    if (!emberAfPluginBootloaderInterfaceInit()) {
      APP_INFO("bootloader init failed\n");
      return;
    }
  }

  emberAfPluginBootloaderInterfaceBootload();

  // If we get here bootload process failed.
  APP_INFO("bootload failed!\n");
}
