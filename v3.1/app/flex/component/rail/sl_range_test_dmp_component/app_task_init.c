/***************************************************************************//**
 * @file 
 * @brief app_task_init.c
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
#include "sl_sleeptimer.h"
#include "app_init.h"
#include "app_task_init.h"
#include "app_process.h"
#include "app_menu.h"
#include "sl_flex_assert.h"
#include "app_measurement.h"
#include "app_graphics.h"

// -----------------------------------------------------------------------------
//                              Macros and Typedefs
// -----------------------------------------------------------------------------
// Proprietary Application task
#define PROPRIETARY_APP_TASK_PRIO         6u
#define PROPRIETARY_APP_TASK_STACK_SIZE   (1024 / sizeof(CPU_STK))

// -----------------------------------------------------------------------------
//                          Static Function Declarations
// -----------------------------------------------------------------------------
static void proprietary_app_task(void *p_arg);

// -----------------------------------------------------------------------------
//                                Global Variables
// -----------------------------------------------------------------------------
OS_FLAG_GRP  proprietary_event_flags;

// -----------------------------------------------------------------------------
//                                Static Variables
// -----------------------------------------------------------------------------
static CPU_STK proprietary_app_task_stack[PROPRIETARY_APP_TASK_STACK_SIZE];
static OS_TCB  proprietary_app_task_TCB;

// -----------------------------------------------------------------------------
//                          Public Function Definitions
// -----------------------------------------------------------------------------
/*******************************************************************************
 * The function is used for application initialization.
 *
 * @param None
 * @returns None
 ******************************************************************************/
void app_task_init(void)
{
  RTOS_ERR err;

  // Create the Proprietary Application task
  OSTaskCreate(&proprietary_app_task_TCB,
               "Proprietary App Task",
               proprietary_app_task,
               0u,
               PROPRIETARY_APP_TASK_PRIO,
               &proprietary_app_task_stack[0u],
               (PROPRIETARY_APP_TASK_STACK_SIZE / 10u),
               PROPRIETARY_APP_TASK_STACK_SIZE,
               0u,
               0u,
               0u,
               (OS_OPT_TASK_STK_CHK | OS_OPT_TASK_STK_CLR),
               &err);

  // Initialize the flag group for the proprietary task
  OSFlagCreate(&proprietary_event_flags, "Prop. flags", (OS_FLAGS) 0, &err);
}

static void proprietary_app_task(void *p_arg)
{
  PP_UNUSED_PARAM(p_arg);
  RTOS_ERR err;

  app_init();

  while (DEF_TRUE) {
    app_process_action();
    OSFlagPend(&proprietary_event_flags,
               RANGETEST_FLAG,
               (OS_TICK) 0,
               OS_OPT_PEND_BLOCKING       \
               + OS_OPT_PEND_FLAG_SET_ANY \
               + OS_OPT_PEND_FLAG_CONSUME,
               NULL,
               &err);
  }
}
