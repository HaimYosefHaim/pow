/***************************************************************************//**
 * @file 
 * @brief Macros defined for the wMBus plugin.
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

#ifndef SL_MBEDTLS_CONFIG_H
#define SL_MBEDTLS_CONFIG_H

#if !defined(NO_CRYPTO_ACCELERATION)
/* SiliconLabs plugins with CRYPTO acceleration support. */
#define MBEDTLS_AES_ALT
#endif

/* mbed TLS modules */
#define MBEDTLS_AES_C
#define MBEDTLS_CIPHER_MODE_CBC

/* Save RAM at the expense of ROM */
#define MBEDTLS_AES_ROM_TABLES

#include "mbedtls/check_config.h"

#endif /* SL_MBEDTLS_CONFIG_H */
