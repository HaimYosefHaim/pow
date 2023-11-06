/***************************************************************************//**
 * @file
 * @brief Application log source file
 *******************************************************************************
 * # License
 * <b>Copyright 2021 Silicon Laboratories Inc. www.silabs.com</b>
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

#include "em_common.h"
#include "sl_status.h"
#include "app_log.h"
#include "sl_iostream.h"
#include "sl_iostream_handles.h"
#include "string.h"

// -----------------------------------------------------------------------------
// Global variables
sl_iostream_t * app_log_iostream = NULL;

// -----------------------------------------------------------------------------
// Public functions

/***************************************************************************//**
 * Sets IO Stream
 ******************************************************************************/
sl_status_t app_log_iostream_set(sl_iostream_t *stream)
{
  sl_status_t ret = SL_STATUS_INVALID_PARAMETER;
  for (uint32_t i = 0; i < sl_iostream_instances_count; i++) {
    if (sl_iostream_instances_info[i]->handle == stream) {
      app_log_iostream = stream;
      ret = SL_STATUS_OK;
      break;
    }
  }
  return ret;
}

/***************************************************************************//**
 * Get the current IO Stream for logging
 ******************************************************************************/
sl_iostream_t * app_log_iostream_get(void)
{
  return app_log_iostream;
}

/******************************************************************************
* Log status string
******************************************************************************/
void app_log_status_string(sl_status_t sc)
{
  sl_iostream_printf(app_log_iostream, "(");
  sl_iostream_t * default_stream_cfgd = sl_iostream_get_default();
  sl_iostream_set_default(app_log_iostream);
  sl_status_print(sc);
  sl_iostream_set_default(default_stream_cfgd);
  sl_iostream_printf(app_log_iostream, ") ");
}

/******************************************************************************
* Application log init
******************************************************************************/
void app_log_init()
{
#if defined(APP_LOG_OVERRIDE_DEFAULT_STREAM) && APP_LOG_OVERRIDE_DEFAULT_STREAM == 1
  char *name = APP_LOG_STREAM_INSTANCE;
  sl_iostream_type_t type = APP_LOG_STREAM_TYPE;

  sl_iostream_t * iostream = NULL;
  sl_iostream_t * iostream_type = NULL;

  for (uint32_t i = 0; i < sl_iostream_instances_count; i++) {
    if (sl_iostream_instances_info[i]->type == type) {
      if (strcmp(sl_iostream_instances_info[i]->name, name) == 0) {
        iostream = sl_iostream_instances_info[i]->handle;
        break;
      }
      if (iostream_type == NULL) {
        iostream_type = sl_iostream_instances_info[i]->handle;
      }
    }
  }

  if (iostream == NULL) {
    // The stream is not found by name
    if (iostream_type != NULL) {
      // Stream found by type
      iostream = iostream_type;
    } else {
      // Not found stream, set to default
      iostream = sl_iostream_get_default();
    }
  }

  app_log_iostream = iostream;
#else  // APP_LOG_OVERRIDE_DEFAULT_STREAM
  app_log_iostream = sl_iostream_get_default();
#endif // APP_LOG_OVERRIDE_DEFAULT_STREAM
}

/******************************************************************************
* Weak implementation of status print
******************************************************************************/
SL_WEAK void sl_status_print(sl_status_t status)
{
  (void) status;
}
