/***************************************************************************//**
 * @file 
 * @brief app_init.c
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
#include "sl_sleeptimer.h"
#include "app_init.h"
#include "app_process.h"
#include "app_menu.h"
#include "sl_flex_assert.h"
#include "app_measurement.h"
#include "app_graphics.h"

#if defined(SL_CATALOG_KERNEL_PRESENT)
#include "app_task_init.h"
#endif

// -----------------------------------------------------------------------------
//                              Macros and Typedefs
// -----------------------------------------------------------------------------

// -----------------------------------------------------------------------------
//                          Static Function Declarations
// -----------------------------------------------------------------------------
/// Timer expiration callback for the delay function.
static void init_screen_timer_callback(sl_sleeptimer_timer_handle_t *handle, void *data);

// -----------------------------------------------------------------------------
//                                Global Variables
// -----------------------------------------------------------------------------

// -----------------------------------------------------------------------------
//                                Static Variables
// -----------------------------------------------------------------------------
/// Timer for the delay of the showing init screen
static sl_sleeptimer_timer_handle_t init_screen_timer;

// -----------------------------------------------------------------------------
//                          Public Function Definitions
// -----------------------------------------------------------------------------
/*******************************************************************************
 * The function is used for application initialization.
 *
 * @param None
 * @returns None
 ******************************************************************************/
void app_init(void)
{
  sl_status_t sleep_timer_status = 0;

  graphics_init();
  init_range_test_phys();
  menu_init();

  set_next_state(INFO_SCREEN);
  request_refresh_screen();

  sleep_timer_status = sl_sleeptimer_start_timer(&init_screen_timer,
                                                 sl_sleeptimer_ms_to_tick(3000), init_screen_timer_callback,
                                                 NULL, 0, 0);

  APP_WARNING(sleep_timer_status == 0, "Sleeptimer start failed with code %d",
              sleep_timer_status);

  APP_INFO("Range test\n");
}

/*******************************************************************************
 * The function is used for stopping the timer in the init block.
 *
 * @param None
 * @returns None
 ******************************************************************************/
void end_init_timer(void)
{
  bool is_running = false;
  sl_status_t sleep_timer_status = 0;
  sleep_timer_status = sl_sleeptimer_is_timer_running(&init_screen_timer,
                                                      &is_running);
  APP_WARNING(sleep_timer_status == 0,
              "Sleeptimer state read failed with code %d", sleep_timer_status);
  if (is_running) {
    sleep_timer_status = sl_sleeptimer_stop_timer(&init_screen_timer);
    APP_WARNING(sleep_timer_status == 0,
                "Sleeptimer stop failed with code %d", sleep_timer_status);
  }
}

// -----------------------------------------------------------------------------
//                          Static Function Definitions
// -----------------------------------------------------------------------------
/*******************************************************************************
 * Timer expiration callback for the delay function.
 *
 * @param handle Pointer to handle to timer.
 * @param data Pointer to delay flag.
 ******************************************************************************/
static void init_screen_timer_callback(sl_sleeptimer_timer_handle_t *handle, void *data)
{
  (void)data;  // Unused parameter.
  (void)handle;  // Unused parameter.

  set_next_state(MENU_SCREEN);
  request_refresh_screen();
#if defined(SL_CATALOG_KERNEL_PRESENT)
  RTOS_ERR err;
  OSFlagPost(&proprietary_event_flags, RANGETEST_FLAG, OS_OPT_POST_FLAG_SET, &err);
#endif
}
