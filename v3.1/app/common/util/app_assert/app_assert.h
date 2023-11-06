/***************************************************************************//**
 * @file
 * @brief Application assert interface
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

#ifndef APP_ASSERT_H
#define APP_ASSERT_H

#ifdef SL_COMPONENT_CATALOG_PRESENT
#include "sl_component_catalog.h"
#endif // SL_COMPONENT_CATALOG_PRESENT
#include "app_assert_config.h"
#include "sl_status.h"
#ifdef SL_CATALOG_APP_LOG_PRESENT
#include "app_log.h"
#endif

#if defined(APP_ASSERT_ENABLE) && APP_ASSERT_ENABLE
#if defined(SL_CATALOG_APP_LOG_PRESENT) && APP_ASSERT_LOG_ENABLE

#define app_assert_s(expr)                             \
  do {                                                 \
    if (!(expr)) {                                     \
      app_log_level(APP_LOG_LEVEL_CRITICAL,            \
                    "Assertion '" #expr "' failed\n"); \
      while (1) ;                                      \
    }                                                  \
  } while (0)

#define app_assert_status(sc)                        \
  do {                                               \
    if (!(sc == SL_STATUS_OK)) {                     \
      app_log_status_level_f(APP_LOG_LEVEL_CRITICAL, \
                             sc,                     \
                             "Assertion failed");    \
      while (1) ;                                    \
    }                                                \
  } while (0)
#define app_assert_status_f(sc, ...)                            \
  do {                                                          \
    if (!(sc == SL_STATUS_OK)) {                                \
      app_log_status_level_f(APP_LOG_LEVEL_CRITICAL,            \
                             sc,                                \
                             "Assertion failed: " __VA_ARGS__); \
      while (1) ;                                               \
    }                                                           \
  } while (0)
#define app_assert(expr, ...)                                      \
  do {                                                             \
    if (!(expr)) {                                                 \
      app_log_level(APP_LOG_LEVEL_CRITICAL,                        \
                    "Assertion '" #expr "' failed: " __VA_ARGS__); \
      while (1) ;                                                  \
    }                                                              \
  } while (0)
#else // defined(SL_CATALOG_APP_LOG_PRESENT) && APP_ASSERT_LOG_ENABLE
#define app_assert_printless(expr) \
  do {                             \
    if (!(expr)) {                 \
      while (1) ;                  \
    }                              \
  } while (0)
#define app_assert(expr, ...) \
  app_assert_printless(expr)
#define app_assert_s(expr) \
  app_assert_printless(expr)
#define app_assert_status(sc) \
  app_assert_printless(sc == SL_STATUS_OK)
#define app_assert_status_f(sc, ...) \
  app_assert_printless(sc == SL_STATUS_OK)
#endif // defined(SL_CATALOG_APP_LOG_PRESENT) && APP_ASSERT_LOG_ENABLE
#else // APP_ASSERT_ENABLE
#define app_assert(expr, ...)
#define app_assert_s(expr)
#define app_assert_status(sc) (void)sc
#define app_assert_status_f(sc, ...) (void)sc
#endif // APP_ASSERT_ENABLE

#endif // APP_ASSERT_H
