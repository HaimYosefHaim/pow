/***************************************************************************//**
 * @file
 * @brief Application logging interface
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

#ifndef SL_APP_LOG_H
#define SL_APP_LOG_H

#include "app_log.h"

#warning "sl_app_log is deprecated and marked for removal in a later release. Please use app_log instead."

#define sl_app_log(...) app_log(__VA_ARGS__)

#endif // SL_APP_LOG_H
