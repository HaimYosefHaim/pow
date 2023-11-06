/***************************************************************************//**
 * @file app_psa_crypto_key.h
 * @brief PSA Crypto key functions.
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
#ifndef APP_PSA_CRYPTO_KEY_H
#define APP_PSA_CRYPTO_KEY_H

// -----------------------------------------------------------------------------
//                                   Includes
// -----------------------------------------------------------------------------
#include "app_psa_crypto_macro.h"

// -----------------------------------------------------------------------------
//                              Macros and Typedefs
// -----------------------------------------------------------------------------
/// Key buffer size = maximum public key size + 1
#define KEY_BUF_SIZE            (133)

/// Location value for wrapped key (PSA_KEY_LOCATION_SLI_SE_OPAQUE)
#define WRAP_KEY_LOCATION       ((psa_key_location_t)0x000001UL)

/// Offset for key creation
#define CREATE_KEY_OFFSET       (0)

/// Offset for key import
#define IMPORT_KEY_OFFSET       (4)

/// Key storage and type
#define VOLATILE_PLAIN_KEY      (0)
#define PERSISTENT_PLAIN_KEY    (1)
#define VOLATILE_WRAP_KEY       (2)
#define PERSISTENT_WRAP_KEY     (3)

// -----------------------------------------------------------------------------
//                                Global Variables
// -----------------------------------------------------------------------------

// -----------------------------------------------------------------------------
//                          Public Function Declarations
// -----------------------------------------------------------------------------

/***************************************************************************//**
 * Get key buffer pointer.
 *
 * @returns Returns pointer to key buffer.
 ******************************************************************************/
uint8_t * get_key_buf_ptr(void);

/***************************************************************************//**
 * Get key length.
 *
 * @returns Returns key length.
 ******************************************************************************/
size_t get_key_len(void);

/***************************************************************************//**
 * Get key identifier.
 *
 * @returns Returns key identifier.
 ******************************************************************************/
psa_key_handle_t get_key_id(void);

/***************************************************************************//**
 * Get key algorithm.
 *
 * @returns Returns key algorithm.
 ******************************************************************************/
psa_algorithm_t get_key_algo(void);

/***************************************************************************//**
 * Set key length.
 *
 * @param length The length of the key.
 ******************************************************************************/
void set_key_len(size_t length);

/***************************************************************************//**
 * Set key identifier.
 *
 * @param id The identifier of the key.
 ******************************************************************************/
void set_key_id(psa_key_handle_t id);

/***************************************************************************//**
 * Initialize the PSA Crypto.
 *
 * @returns Returns PSA error code, @ref crypto_values.h.
 ******************************************************************************/
psa_status_t init_psa_crypto(void);

/***************************************************************************//**
 * Open a built-in key.
 *
 * @param builtin_key_id The built-in key ID to open.
 * @returns Returns PSA error code, @ref crypto_values.h.
 ******************************************************************************/
psa_status_t open_builtin_key(psa_key_id_t builtin_key_id);

/***************************************************************************//**
 * Close a built-in key.
 *
 * @returns Returns PSA error code, @ref crypto_values.h.
 ******************************************************************************/
psa_status_t close_builtin_key(void);

/***************************************************************************//**
 * Generate or import a key.
 *
 * @param storage_type The key storage type.
 * @param type The key type.
 * @param size The key size in bits.
 * @param id The key identifier for persistent key.
 * @param usage The key usage.
 * @param algo The key algorithm.
 * @returns Returns PSA error code, @ref crypto_values.h.
 ******************************************************************************/
psa_status_t create_import_key(uint8_t storage_type,
                               psa_key_type_t type,
                               size_t size,
                               psa_key_id_t id,
                               psa_key_usage_t usage,
                               psa_algorithm_t algo);

/***************************************************************************//**
 * Copy a key.
 *
 * @param id The key identifier for persistent copied key.
 * @param usage The copied key usage.
 * @param algo The copied key algorithm.
 * @returns Returns PSA error code, @ref crypto_values.h.
 ******************************************************************************/
psa_status_t copy_key(psa_key_id_t id,
                      psa_key_usage_t usage,
                      psa_algorithm_t algo);

/***************************************************************************//**
 * Derive a symmetric key.
 *
 * @param storage_type The derived key storage type.
 * @param operation Pointer to key derivation operation object.
 * @param size The derived key size in bits.
 * @param id The key identifier for persistent derived key.
 * @param usage The derived key usage.
 * @param algo The derived key algorithm.
 * @returns Returns PSA error code, @ref crypto_values.h.
 ******************************************************************************/
psa_status_t derive_key(uint8_t storage_type,
                        psa_key_derivation_operation_t *operation,
                        size_t size,
                        psa_key_id_t id,
                        psa_key_usage_t usage,
                        psa_algorithm_t algo);

/***************************************************************************//**
 * Free any auxiliary resources that the object might contain.
 ******************************************************************************/
void reset_key_attr(void);

/***************************************************************************//**
 * Export a key.
 *
 * @returns Returns PSA error code, @ref crypto_values.h.
 ******************************************************************************/
psa_status_t export_key(void);

/***************************************************************************//**
 * Export a public key.
 *
 * @returns Returns PSA error code, @ref crypto_values.h.
 ******************************************************************************/
psa_status_t export_public_key(void);

/***************************************************************************//**
 * Destroy a key.
 *
 * @returns Returns PSA error code, @ref crypto_values.h.
 ******************************************************************************/
psa_status_t destroy_key(void);

#endif  // APP_PSA_CRYPTO_KEY_H
