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

#ifndef APP_LOG_H
#define APP_LOG_H

#include "sl_iostream.h"
#include "sl_iostream_handles.h"
#include "app_log_config.h"
#include "sl_status.h"

#define APP_LOG_LEVEL_CRITICAL             0
#define APP_LOG_LEVEL_ERROR                1
#define APP_LOG_LEVEL_WARNING              2
#define APP_LOG_LEVEL_INFO                 3
#define APP_LOG_LEVEL_DEBUG                4

#define APP_LOG_TRACE_FORMAT               "%s:%d :%s: "

#define APP_LOG_COLOR_BLACK           "\033[2;30m"
#define APP_LOG_COLOR_RED             "\033[2;31m"
#define APP_LOG_COLOR_GREEN           "\033[2;32m"
#define APP_LOG_COLOR_YELLOW          "\033[2;33m"
#define APP_LOG_COLOR_BLUE            "\033[2;34m"
#define APP_LOG_COLOR_MAGENTA         "\033[2;35m"
#define APP_LOG_COLOR_CYAN            "\033[2;36m"
#define APP_LOG_COLOR_WHITE           "\033[2;37m"
#define APP_LOG_COLOR_BRIGHT_BLACK    "\033[1;30m"
#define APP_LOG_COLOR_BRIGHT_RED      "\033[1;31m"
#define APP_LOG_COLOR_BRIGHT_GREEN    "\033[1;32m"
#define APP_LOG_COLOR_BRIGHT_YELLOW   "\033[1;33m"
#define APP_LOG_COLOR_BRIGHT_BLUE     "\033[1;34m"
#define APP_LOG_COLOR_BRIGHT_MAGENTA  "\033[1;35m"
#define APP_LOG_COLOR_BRIGHT_CYAN     "\033[1;36m"
#define APP_LOG_COLOR_BRIGHT_WHITE    "\033[1;37m"

#define APP_LOG_BACKGROUND_COLOR_NONE            "\033[0m"
#define APP_LOG_BACKGROUND_COLOR_BLACK           "\033[40m"
#define APP_LOG_BACKGROUND_COLOR_RED             "\033[41m"
#define APP_LOG_BACKGROUND_COLOR_GREEN           "\033[42m"
#define APP_LOG_BACKGROUND_COLOR_YELLOW          "\033[43m"
#define APP_LOG_BACKGROUND_COLOR_BLUE            "\033[44m"
#define APP_LOG_BACKGROUND_COLOR_MAGENTA         "\033[45m"
#define APP_LOG_BACKGROUND_COLOR_CYAN            "\033[46m"
#define APP_LOG_BACKGROUND_COLOR_WHITE           "\033[47m"
#define APP_LOG_BACKGROUND_COLOR_BRIGHT_BLACK    "\033[40,1m"
#define APP_LOG_BACKGROUND_COLOR_BRIGHT_RED      "\033[41,1m"
#define APP_LOG_BACKGROUND_COLOR_BRIGHT_GREEN    "\033[42,1m"
#define APP_LOG_BACKGROUND_COLOR_BRIGHT_YELLOW   "\033[43,1m"
#define APP_LOG_BACKGROUND_COLOR_BRIGHT_BLUE     "\033[44,1m"
#define APP_LOG_BACKGROUND_COLOR_BRIGHT_MAGENTA  "\033[45,1m"
#define APP_LOG_BACKGROUND_COLOR_BRIGHT_CYAN     "\033[46,1m"
#define APP_LOG_BACKGROUND_COLOR_BRIGHT_WHITE    "\033[47,1m"

// -----------------------------------------------------------------------------
// Global variables

extern sl_iostream_t * app_log_iostream;

/***************************************************************************//**
 * Application log init
 ******************************************************************************/
void app_log_init();

/***************************************************************************//**
 * Sets IO Stream
 * @param[in] stream IO stream to set
 * @return SL_STATUS_INVALID_PARAMETER if IO stream instance is not present
 ******************************************************************************/
sl_status_t app_log_iostream_set(sl_iostream_t *stream);

/***************************************************************************//**
 * Get the current IO Stream for logging
 ******************************************************************************/
sl_iostream_t * app_log_iostream_get(void);

/***************************************************************************//**
 * Log status string
 * @param[in] value Status code
 ******************************************************************************/
void app_log_status_string(sl_status_t sc);

// -----------------------------------------------------------------------------
// Logging macro definitions

#if defined(APP_LOG_ENABLE) && APP_LOG_ENABLE
#if defined(APP_LOG_COLOR_ENABLE) && APP_LOG_COLOR_ENABLE
#define app_log_print_color(lev)                          \
  do {                                                    \
    switch (lev) {                                        \
      case APP_LOG_LEVEL_DEBUG:                           \
        sl_iostream_printf(app_log_iostream,              \
                           APP_LOG_LEVEL_DEBUG_COLOR);    \
        break;                                            \
      case APP_LOG_LEVEL_INFO:                            \
        sl_iostream_printf(app_log_iostream,              \
                           APP_LOG_LEVEL_INFO_COLOR);     \
        break;                                            \
      case APP_LOG_LEVEL_WARNING:                         \
        sl_iostream_printf(app_log_iostream,              \
                           APP_LOG_LEVEL_WARNING_COLOR);  \
        break;                                            \
      case APP_LOG_LEVEL_ERROR:                           \
        sl_iostream_printf(app_log_iostream,              \
                           APP_LOG_LEVEL_ERROR_COLOR);    \
        break;                                            \
      case APP_LOG_LEVEL_CRITICAL:                        \
        sl_iostream_printf(app_log_iostream,              \
                           APP_LOG_LEVEL_CRITICAL_COLOR); \
        break;                                            \
    }                                                     \
  } while (0)
#define app_log_print_background(lev)                                \
  do {                                                               \
    switch (lev) {                                                   \
      case APP_LOG_LEVEL_DEBUG:                                      \
        sl_iostream_printf(app_log_iostream,                         \
                           APP_LOG_LEVEL_DEBUG_BACKGROUND_COLOR);    \
        break;                                                       \
      case APP_LOG_LEVEL_INFO:                                       \
        sl_iostream_printf(app_log_iostream,                         \
                           APP_LOG_LEVEL_INFO_BACKGROUND_COLOR);     \
        break;                                                       \
      case APP_LOG_LEVEL_WARNING:                                    \
        sl_iostream_printf(app_log_iostream,                         \
                           APP_LOG_LEVEL_WARNING_BACKGROUND_COLOR);  \
        break;                                                       \
      case APP_LOG_LEVEL_ERROR:                                      \
        sl_iostream_printf(app_log_iostream,                         \
                           APP_LOG_LEVEL_ERROR_BACKGROUND_COLOR);    \
        break;                                                       \
      case APP_LOG_LEVEL_CRITICAL:                                   \
        sl_iostream_printf(app_log_iostream,                         \
                           APP_LOG_LEVEL_CRITICAL_BACKGROUND_COLOR); \
        break;                                                       \
    }                                                                \
  } while (0)
#else // APP_LOG_COLOR_ENABLE
#define app_log_print_color(level)
#define app_log_print_background(level)
#endif // APP_LOG_COLOR_ENABLE
#if defined(APP_LOG_PREFIX_ENABLE) && APP_LOG_PREFIX_ENABLE
#define app_log_print_prefix(lev)                          \
  do {                                                     \
    switch (lev) {                                         \
      case APP_LOG_LEVEL_DEBUG:                            \
        sl_iostream_printf(app_log_iostream,               \
                           "%s ",                          \
                           APP_LOG_LEVEL_DEBUG_PREFIX);    \
        break;                                             \
      case APP_LOG_LEVEL_INFO:                             \
        sl_iostream_printf(app_log_iostream,               \
                           "%s ",                          \
                           APP_LOG_LEVEL_INFO_PREFIX);     \
        break;                                             \
      case APP_LOG_LEVEL_WARNING:                          \
        sl_iostream_printf(app_log_iostream,               \
                           "%s ",                          \
                           APP_LOG_LEVEL_WARNING_PREFIX);  \
        break;                                             \
      case APP_LOG_LEVEL_ERROR:                            \
        sl_iostream_printf(app_log_iostream,               \
                           "%s ",                          \
                           APP_LOG_LEVEL_ERROR_PREFIX);    \
        break;                                             \
      case APP_LOG_LEVEL_CRITICAL:                         \
        sl_iostream_printf(app_log_iostream,               \
                           "%s ",                          \
                           APP_LOG_LEVEL_CRITICAL_PREFIX); \
        break;                                             \
    }                                                      \
  } while (0)
#else // APP_LOG_PREFIX_ENABLE
#define app_log_print_prefix(level)
#endif // APP_LOG_PREFIX_ENABLE
#if defined(APP_LOG_TRACE_ENABLE) && APP_LOG_TRACE_ENABLE
#define app_log(...)                                   \
  do {                                                 \
    app_log_print_background(APP_LOG_LEVEL_DEBUG);     \
    app_log_print_color(APP_LOG_LEVEL_DEBUG);          \
    sl_iostream_printf(app_log_iostream,               \
                       APP_LOG_TRACE_FORMAT,           \
                       __FILE__,                       \
                       __LINE__,                       \
                       __func__);                      \
    sl_iostream_printf(app_log_iostream, __VA_ARGS__); \
  } while (0)
#define app_log_level(level, ...)      \
  do {                                 \
    if (level <= APP_LOG_LEVEL) {      \
      app_log_print_background(level); \
      app_log_print_color(level);      \
      app_log_print_prefix(level);     \
      app_log(__VA_ARGS__);            \
    }                                  \
  } while (0)
#define app_log_status_level(level, sc)                    \
  do {                                                     \
    if (!(sc == SL_STATUS_OK) && level <= APP_LOG_LEVEL) { \
      app_log_print_background(level);                     \
      app_log_print_color(level);                          \
      app_log_print_prefix(level);                         \
      sl_iostream_printf(app_log_iostream,                 \
                         APP_LOG_TRACE_FORMAT,             \
                         __FILE__,                         \
                         __LINE__,                         \
                         __func__);                        \
      sl_iostream_printf(app_log_iostream,                 \
                         "Status: " #sc "= 0x%04x ",       \
                         (int)sc);                         \
      app_log_status_string(sc);                           \
      sl_iostream_printf(app_log_iostream, "\n");          \
    }                                                      \
  } while (0)
#define app_log_status_level_f(level, sc, ...)             \
  do {                                                     \
    if (!(sc == SL_STATUS_OK) && level <= APP_LOG_LEVEL) { \
      app_log_print_background(level);                     \
      app_log_print_color(level);                          \
      app_log_print_prefix(level);                         \
      sl_iostream_printf(app_log_iostream,                 \
                         APP_LOG_TRACE_FORMAT,             \
                         __FILE__,                         \
                         __LINE__,                         \
                         __func__);                        \
      sl_iostream_printf(app_log_iostream,                 \
                         "Status: " #sc "= 0x%04x ",       \
                         (int)sc);                         \
      app_log_status_string(sc);                           \
      sl_iostream_printf(app_log_iostream,                 \
                         __VA_ARGS__);                     \
    }                                                      \
  } while (0)
#else // APP_LOG_TRACE_ENABLE
#define app_log(...)                               \
  do {                                             \
    app_log_print_background(APP_LOG_LEVEL_DEBUG); \
    app_log_print_color(APP_LOG_LEVEL_DEBUG);      \
    sl_iostream_printf(app_log_iostream,           \
                       __VA_ARGS__);               \
  } while (0)
#define app_log_level(level, ...)                        \
  do {                                                   \
    if (level <= APP_LOG_LEVEL) {                        \
      app_log_print_background(level);                   \
      app_log_print_color(level);                        \
      app_log_print_prefix(level);                       \
      sl_iostream_printf(app_log_iostream, __VA_ARGS__); \
    }                                                    \
  } while (0)
#define app_log_status_level(level, sc)                    \
  do {                                                     \
    if (!(sc == SL_STATUS_OK) && level <= APP_LOG_LEVEL) { \
      app_log_print_background(level);                     \
      app_log_print_color(level);                          \
      app_log_print_prefix(level);                         \
      sl_iostream_printf(app_log_iostream,                 \
                         "Status: " #sc "= 0x%04x ",       \
                         (int)sc);                         \
      app_log_status_string(sc);                           \
      sl_iostream_printf(app_log_iostream, "\n");          \
    }                                                      \
  } while (0)
#define app_log_status_level_f(level, sc, ...)             \
  do {                                                     \
    if (!(sc == SL_STATUS_OK) && level <= APP_LOG_LEVEL) { \
      app_log_print_background(level);                     \
      app_log_print_color(level);                          \
      app_log_print_prefix(level);                         \
      sl_iostream_printf(app_log_iostream,                 \
                         "Status: " #sc "= 0x%04x ",       \
                         (int)sc);                         \
      app_log_status_string(sc);                           \
      sl_iostream_printf(app_log_iostream,                 \
                         __VA_ARGS__);                     \
    }                                                      \
  } while (0)
#endif // APP_LOG_TRACE_ENABLE
#define app_log_append(...) do {         \
    sl_iostream_printf(app_log_iostream, \
                       __VA_ARGS__);     \
} while (0)
#define app_log_status(sc)                 \
  app_log_status_level(APP_LOG_LEVEL_INFO, \
                       sc)
#define app_log_status_f(sc, ...)            \
  app_log_status_level_f(APP_LOG_LEVEL_INFO, \
                         sc,                 \
                         __VA_ARGS__)
#else // APP_LOG_ENABLE
#define app_log(...)
#define app_log_level(level, ...)
#define app_log_status(sc) (void)sc
#define app_log_status_f(sc, ...) (void)sc
#define app_log_status_level(level, sc) (void)sc
#define app_log_status_level_f(level, sc, ...) (void)sc
#define app_log_append(...)
#endif // APP_LOG_ENABLE

#define app_log_debug(...)           \
  app_log_level(APP_LOG_LEVEL_DEBUG, \
                __VA_ARGS__)
#define app_log_info(...)           \
  app_log_level(APP_LOG_LEVEL_INFO, \
                __VA_ARGS__)
#define app_log_warning(...)           \
  app_log_level(APP_LOG_LEVEL_WARNING, \
                __VA_ARGS__)
#define app_log_error(...)           \
  app_log_level(APP_LOG_LEVEL_ERROR, \
                __VA_ARGS__)
#define app_log_critical(...)           \
  app_log_level(APP_LOG_LEVEL_CRITICAL, \
                __VA_ARGS__)

#define app_log_status_debug(sc)            \
  app_log_status_level(APP_LOG_LEVEL_DEBUG, \
                       sc)
#define app_log_status_info(sc)            \
  app_log_status_level(APP_LOG_LEVEL_INFO, \
                       sc)
#define app_log_status_warning(sc)            \
  app_log_status_level(APP_LOG_LEVEL_WARNING, \
                       sc)
#define app_log_status_error(sc)            \
  app_log_status_level(APP_LOG_LEVEL_ERROR, \
                       sc)
#define app_log_status_critical(sc)            \
  app_log_status_level(APP_LOG_LEVEL_CRITICAL, \
                       sc)

#define app_log_status_debug_f(sc, ...)       \
  app_log_status_level_f(APP_LOG_LEVEL_DEBUG, \
                         sc,                  \
                         __VA_ARGS__, ...)
#define app_log_status_info_f(sc, ...)       \
  app_log_status_level_f(APP_LOG_LEVEL_INFO, \
                         sc,                 \
                         __VA_ARGS__)
#define app_log_status_warning_f(sc, ...)       \
  app_log_status_level_f(APP_LOG_LEVEL_WARNING, \
                         sc,                    \
                         __VA_ARGS__)
#define app_log_status_error_f(sc, ...)       \
  app_log_status_level_f(APP_LOG_LEVEL_ERROR, \
                         sc,                  \
                         __VA_ARGS__)
#define app_log_status_critical_f(sc, ...)       \
  app_log_status_level_f(APP_LOG_LEVEL_CRITICAL, \
                         sc,                     \
                         __VA_ARGS__)

#endif // APP_LOG_H
