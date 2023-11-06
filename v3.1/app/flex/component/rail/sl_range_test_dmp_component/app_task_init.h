/***************************************************************************//**
 * @file 
 * @brief app_task_init.h
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
#ifndef APP_TASK_INIT_H
#define APP_TASK_INIT_H

// -----------------------------------------------------------------------------
//                                   Includes
// -----------------------------------------------------------------------------
#include "os.h"

// -----------------------------------------------------------------------------
//                              Macros and Typedefs
// -----------------------------------------------------------------------------
#define RANGETEST_FLAG  ((OS_FLAGS)0x01)

// -----------------------------------------------------------------------------
//                                Global Variables
// -----------------------------------------------------------------------------
/* OS Event Flag Group */
extern OS_FLAG_GRP  proprietary_event_flags;

// -----------------------------------------------------------------------------
//                          Public Function Declarations
// -----------------------------------------------------------------------------
/*******************************************************************************
 * The function is used for application initialization.
 *
 * @param None
 * @returns None
 ******************************************************************************/
void app_task_init(void);

#endif  // APP_TASK_INIT_H
