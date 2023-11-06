/***************************************************************************//**
 * @file app_process.h
 * @brief Top level application functions.
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
#ifndef APP_PROCESS_H
#define APP_PROCESS_H

// -----------------------------------------------------------------------------
//                                   Includes
// -----------------------------------------------------------------------------
#include "app_psa_crypto_ecdsa.h"
#include "app_psa_crypto_key.h"
#include <string.h>
#include "nvm3.h"

// -----------------------------------------------------------------------------
//                              Macros and Typedefs
// -----------------------------------------------------------------------------
/// State machine states
typedef enum {
  PSA_CRYPTO_IDLE,
  PSA_CRYPTO_INIT,
  SELECT_KEY_STORAGE,
  SELECT_SECPR1_SIZE,
  SELECT_HASH_ALGO,
  CREATE_KEY,
  SIGN_HASH,
  EXPORT_PUBLIC_KEY,
  IMPORT_PUBLIC_KEY,
  VERIFY_HASH_SIGNATURE,
  DESTROY_KEY,
  IMPORT_PRIVATE_KEY,
  SIGN_HASH_BUILTIN,
  OPEN_BUILTIN_KEY,
  EXPORT_PUBLIC_BUILTIN_KEY,
  VERIFY_HASH_SIGNATURE_BUILTIN,
  CLOSE_BUILTIN_KEY,
  PSA_CRYPTO_EXIT
} state_t;

/// ECDSA process states
typedef enum {
  ECDSA_SIGN_HASH,
  ECDSA_VERIFY_HASH,
  ECDSA_SIGN_KEY_SIGN_HASH,
  ECDSA_SIGN_KEY_VERIFY_HASH,
  ECDSA_COMMAND_KEY_SIGN_HASH,
  ECDSA_COMMAND_KEY_VERIFY_HASH,
  ECDSA_DEVICE_KEY_SIGN_HASH,
  ECDSA_DEVICE_KEY_VERIFY_HASH,
} ecdsa_state_t;

/// Option selection maximum values
#if defined(SEMAILBOX_PRESENT) && (_SILICON_LABS_SECURITY_FEATURE == _SILICON_LABS_SECURITY_FEATURE_VAULT)
#define KEY_STORAGE_MAX         (PERSISTENT_WRAP_KEY + 1)
#else
#if defined(MBEDTLS_PSA_CRYPTO_BUILTIN_KEYS)
#define KEY_STORAGE_MAX         (PERSISTENT_PLAIN_KEY + 1)
#else
#define KEY_STORAGE_MAX         PERSISTENT_PLAIN_KEY
#endif
#endif
#define SECPR1_SIZE_MAX         (3)
#define HASH_ALGO_MAX           (5)

/// Default key usage is none
#define DEFAULT_KEY_USAGE       (0)

/// Persistent key ID
#define PERSISTENT_KEY_ID       PSA_KEY_ID_USER_MIN

// -----------------------------------------------------------------------------
//                                Global Variables
// -----------------------------------------------------------------------------

// -----------------------------------------------------------------------------
//                          Public Function Declarations
// -----------------------------------------------------------------------------

/***************************************************************************//**
 * Application state machine, called infinitely.
 ******************************************************************************/
void app_process_action(void);

#endif  // APP_PROCESS_H
