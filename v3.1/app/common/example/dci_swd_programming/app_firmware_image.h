/***************************************************************************//**
 * @file app_firmware_image.h
 * @brief The firmware image data.
 *******************************************************************************
 * # License
 * <b>Copyright 2020 Silicon Laboratories Inc. www.silabs.com</b>
 *******************************************************************************
 *
 * The licensor of this software is Silicon Laboratories Inc. Your use of this
 * software is governed by the terms of Silicon Labs Master Software License
 * Agreement (MSLA) available at
 * www.silabs.com/about-us/legal/master-software-license-agreement. This
 * software is distributed to you in Source Code format and is governed by the
 * sections of the MSLA applicable to Source Code.
 *
 ******************************************************************************/
#ifndef APP_FIRMWARE_IMAGE_H
#define APP_FIRMWARE_IMAGE_H

// -----------------------------------------------------------------------------
//                                   Includes
// -----------------------------------------------------------------------------
#include <stdint.h>
#include <inttypes.h>
#include "em_common.h"

// -----------------------------------------------------------------------------
//                              Macros and Typedefs
// -----------------------------------------------------------------------------
/// Application firmware image start address
#define APP_START_ADDR          (0x00000000UL)

/// SE firmware image start address
#define SE_START_ADDR           (0x00040000UL)

/// Delay in micro seconds after upgrading SE firmware
#define SE_UPGRADE_DELAY        (2500000)

/// Delay in micro seconds after soft reset to erase or program user data
#define USER_DATA_DELAY         (1000000)

// -----------------------------------------------------------------------------
//                                Global Variables
// -----------------------------------------------------------------------------

// -----------------------------------------------------------------------------
//                          Public Function Declarations
// -----------------------------------------------------------------------------
/***************************************************************************//**
 * Get start address of the EFR32xG21 HSE firmware image.
 *
 * @returns Returns start address of the EFR32xG21 HSE firmware image.
 ******************************************************************************/
const uint8_t * get_xg21_hse_addr(void);

/***************************************************************************//**
 * Get size of the EFR32xG21 HSE firmware image.
 *
 * @returns Returns size of the EFR32xG21 HSE firmware image.
 ******************************************************************************/
uint32_t get_xg21_hse_size(void);

/***************************************************************************//**
 * Get start address of the EFR32xG22 VSE firmware image.
 *
 * @returns Returns start address of the EFR32xG22 VSE firmware image.
 ******************************************************************************/
const uint8_t * get_xg22_vse_addr(void);

/***************************************************************************//**
 * Get size of the EFR32xG22 VSE firmware image.
 *
 * @returns Returns size of the EFR32xG22 VSE firmware image.
 ******************************************************************************/
uint32_t get_xg22_vse_size(void);

/***************************************************************************//**
 * Get start address of the EFR32xG21 application firmware image.
 *
 * @returns Returns start address of the EFR32xG21 application firmware image.
 ******************************************************************************/
const uint8_t * get_xg21_app_addr(void);

/***************************************************************************//**
 * Get size of the EFR32xG21 application firmware image.
 *
 * @returns Returns size of the EFR32xG21 application firmware image.
 ******************************************************************************/
uint32_t get_xg21_app_size(void);

/***************************************************************************//**
 * Get start address of the EFR32xG22 application firmware image.
 *
 * @returns Returns start address of the EFR32xG22 application firmware image.
 ******************************************************************************/
const uint8_t * get_xg22_app_addr(void);

/***************************************************************************//**
 * Get size of the EFR32xG22 application firmware image.
 *
 * @returns Returns size of the EFR32xG22 application firmware image.
 ******************************************************************************/
uint32_t get_xg22_add_size(void);

/***************************************************************************//**
 * Get start address of the EFR32xG21 signed firmware image.
 *
 * @returns Returns start address of the EFR32xG21 signed firmware image.
 ******************************************************************************/
const uint8_t * get_xg21_signed_addr(void);

/***************************************************************************//**
 * Get size of the EFR32xG21 signed firmware image.
 *
 * @returns Returns size of the EFR32xG21 signed firmware image.
 ******************************************************************************/
uint32_t get_xg21_signed_size(void);

/***************************************************************************//**
 * Get start address of the EFR32xG22 signed firmware image.
 *
 * @returns Returns start address of the EFR32xG22 signed firmware image.
 ******************************************************************************/
const uint8_t * get_xg22_signed_addr(void);

/***************************************************************************//**
 * Get size of the EFR32xG22 signed firmware image.
 *
 * @returns Returns size of the EFR32xG22 signed firmware image.
 ******************************************************************************/
uint32_t get_xg22_signed_size(void);

/***************************************************************************//**
 * Get start address of EFR32xG21 application firmware image to erase user data.
 *
 * @returns Returns start address of the application firmware image.
 ******************************************************************************/
const uint8_t * get_xg21_userdata_erase_app_addr(void);

/***************************************************************************//**
 * Get size of of EFR32xG21 application firmware image to erase user data.
 *
 * @returns Returns size of the application firmware image.
 ******************************************************************************/
uint32_t get_xg21_userdata_erase_app_size(void);

/***************************************************************************//**
 * Get start address of EFR32xG21 application firmware image to write user data.
 *
 * @returns Returns start address of the application firmware image.
 ******************************************************************************/
const uint8_t * get_xg21_userdata_write_app_addr(void);

/***************************************************************************//**
 * Get size of EFR32xG21 application firmware image to write user data.
 *
 * @returns Returns size of the application firmware image.
 ******************************************************************************/
uint32_t get_xg21_userdata_write_app_size(void);

/***************************************************************************//**
 * Get start address of EFR32xG21 application firmware image to upgrade HSE.
 *
 * @returns Returns start address of the application firmware image.
 ******************************************************************************/
const uint8_t * get_xg21_hse_upgrade_app_addr(void);

/***************************************************************************//**
 * Get size of EFR32xG21 application firmware image to upgrade HSE.
 *
 * @returns Returns size of the application firmware image.
 ******************************************************************************/
uint32_t get_xg21_hse_upgrade_app_size(void);

/***************************************************************************//**
 * Get start address of EFR32xG22 application firmware image to upgrade VSE.
 *
 * @returns Returns start address of the application firmware image.
 ******************************************************************************/
const uint8_t * get_xg22_vse_upgrade_app_addr(void);

/***************************************************************************//**
 * Get size of EFR32xG22 application firmware image to upgrade VSE.
 *
 * @returns Returns size of the application firmware image.
 ******************************************************************************/
uint32_t get_xg22_vse_upgrade_app_size(void);

/***************************************************************************//**
 * Get start address of the user data.
 *
 * @returns Returns start address of the user data.
 ******************************************************************************/
const uint32_t * get_userdata_addr(void);

/***************************************************************************//**
 * Get size of the user data.
 *
 * @returns Returns size of the user data.
 ******************************************************************************/
uint32_t get_userdata_size(void);

#endif  // APP_FIRMWARE_IMAGE_H
