/***************************************************************************//**
 * @file app_swd_task.h
 * @brief SWD interface task functions.
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
#ifndef APP_SWD_TASK_H
#define APP_SWD_TASK_H

// -----------------------------------------------------------------------------
//                                   Includes
// -----------------------------------------------------------------------------
#include <stdio.h>
#include "sl_udelay.h"
#include "app_dci_swd.h"
#include "app_prog_error.h"

// -----------------------------------------------------------------------------
//                              Macros and Typedefs
// -----------------------------------------------------------------------------
/// Device family of EFR32xG22
#define XG22_FAMILY     (0x00160000UL)

/// CMU_CLKEN1_SET address of EFR32xG22
#define CLKEN1_SET_ADDR (0x40009068UL)

/// MSC bit of CMU_CLKEN1_SET
#define CLKEN1_SET_MSC  (0x00020000UL)

/// Delay in micro seconds for flash erase
#define ERASE_DELAY     (12000)

/// Timeout count for flash erase
#define ERASE_LOOPCNT   (400)

/// Skip polling flash write ready, 1 to skip
#define SKIP_POLLING    1

/// Delay in micro seconds after flash write
#define WRITE_DELAY     (11)

/// TAR wrap mask for Cortex-M33
#define TAR_WRAP_1K     (0x3FF)

/// User data address
#define USER_DATA_ADDR  (0x0FE00000UL)

// -----------------------------------------------------------------------------
//                                Global Variables
// -----------------------------------------------------------------------------

// -----------------------------------------------------------------------------
//                          Public Function Declarations
// -----------------------------------------------------------------------------
/***************************************************************************//**
 * Retrieve the device information from the DI page of the target.
 *
 * @param name Pointer to buffer to store device name.
 * @param uid Pointer to buffer to store the unique ID.
 ******************************************************************************/
void get_device_info(char *name, uint64_t *uid);

/***************************************************************************//**
 * Verifies the user data is cleared or against the internal memory.
 *
 * @param ptr Pointer to user data address, NULL for blank check.
 ******************************************************************************/
void verify_user_data(uint32_t *ptr);

/***************************************************************************//**
 * Erase the flash and verify that the flash is cleared.
 *
 * @param userdata True to erase user data, false to erase main flash.
 * @returns Returns the number of clock cycles to erase the flash.
 *
 * @note To save time, only the first word on every page of main flash is
 *       checked but this could be modified to check every word.
 ******************************************************************************/
uint32_t erase_flash(bool userdata);

/***************************************************************************//**
 * Uses direct writes to MSC registers in order to program the flash.
 *
 * @param start_addr Start address to program (must in multiple of page size).
 * @param size Firmware image size in bytes.
 * @param ptr Pointer to firmware image address.
 * @returns Returns the number of clock cycles to program the flash.
 ******************************************************************************/
uint32_t prog_flash(uint32_t start_addr, uint32_t size, uint32_t *ptr);

#endif  // APP_SWD_TASK_H
