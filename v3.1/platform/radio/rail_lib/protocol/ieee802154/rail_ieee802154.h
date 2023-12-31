/***************************************************************************//**
 * @file
 * @brief The IEEE 802.15.4 specific header file for the RAIL library.
 *******************************************************************************
 * # License
 * <b>Copyright 2020 Silicon Laboratories Inc. www.silabs.com</b>
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

#ifndef __RAIL_IEEE802154_H__
#define __RAIL_IEEE802154_H__

#include "rail_types.h"

#ifdef __cplusplus
extern "C" {
#endif

/// @addtogroup IEEE802_15_4 IEEE 802.15.4
/// @ingroup Protocol_Specific
/// @brief IEEE 802.15.4 configuration routines
///
/// The functions in this group configure RAIL IEEE 802.15.4 hardware
/// acceleration which includes IEEE 802.15.4 format filtering, address
/// filtering, ACKing, and filtering based on the frame type.
///
/// To configure IEEE 802.15.4 functionality, the application must first set up
/// a RAIL instance with RAIL_Init() and other setup functions.
/// Instead of RAIL_ConfigChannels(), however, an
/// application may use RAIL_IEEE802154_Config2p4GHzRadio() to set up the
/// official IEEE 2.4 GHz 802.15.4 PHY. This configuration is shown below.
///
/// 802.15.4 defines its macAckWaitDuration from the end of the transmitted
/// packet to complete reception of the ACK. RAIL's ackTimeout only covers
/// sync word detection of the ACK. Therefore, subtract the ACK's
/// PHY header and payload time to get RAIL's ackTimeout setting.
/// For 2.4 GHz OQPSK, macAckWaitDuration is specified as 54 symbols;
/// subtracting 2-symbol PHY header and 10-symbol payload yields a RAIL
/// ackTimeout of 42 symbols or 672 microseconds at 16 microseconds/symbol.
///
/// @code{.c}
/// static RAIL_Handle_t railHandle = NULL; // Initialized somewhere else.
///
/// static const RAIL_IEEE802154_Config_t rail154Config = {
///   .addresses = NULL,
///   .ackConfig = {
///     .enable = true,     // Turn on auto ACK for IEEE 802.15.4.
///     .ackTimeout = 672,  // See note above: 54-12 sym * 16 us/sym = 672 us.
///     .rxTransitions = {
///       .success = RAIL_RF_STATE_RX,  // Return to RX after ACK processing
///       .error = RAIL_RF_STATE_RX,    // Ignored
///     },
///     .txTransitions = {
///       .success = RAIL_RF_STATE_RX,  // Return to RX after ACK processing
///       .error = RAIL_RF_STATE_RX,    // Ignored
///     },
///   },
///   .timings = {
///     .idleToRx = 100,
///     .idleToTx = 100,
///     .rxToTx = 192,    // 12 symbols * 16 us/symbol = 192 us
///     .txToRx = 192,    // 12 symbols * 16 us/symbol = 192 us
///     .rxSearchTimeout = 0, // Not used
///     .txToRxSearchTimeout = 0, // Not used
///   },
///   .framesMask = RAIL_IEEE802154_ACCEPT_STANDARD_FRAMES,
///   .promiscuousMode = false,  // Enable format and address filtering.
///   .isPanCoordinator = false,
///   .defaultFramePendingInOutgoingAcks = false,
/// };
///
/// void config154(void)
/// {
///   // Configure the radio and channels for 2.4 GHz IEEE 802.15.4.
///   RAIL_IEEE802154_Config2p4GHzRadio(railHandle);
///   // Initialize the IEEE 802.15.4 configuration using the static configuration above.
///   RAIL_IEEE802154_Init(railHandle, &rail154Config);
/// }
/// @endcode
///
/// To configure address filtering, call
/// RAIL_IEEE802154_SetAddresses() with a structure containing all addresses or
/// call the individual RAIL_IEEE802154_SetPanId(),
/// RAIL_IEEE802154_SetShortAddress(), and RAIL_IEEE802154_SetLongAddress()
/// APIs. RAIL supports \ref RAIL_IEEE802154_MAX_ADDRESSES number of address
/// pairs to receive packets from multiple IEEE
/// 802.15.4 networks at the same time. Broadcast addresses are supported by
/// default without any additional configuration so they do not consume one of
/// these slots. If the application does not require all address pairs, be sure
/// to set unused ones to the proper disabled value for each type. These can
/// be found in the \ref RAIL_IEEE802154_AddrConfig_t documentation. Below is
/// an example of setting filtering for one set of addresses.
///
/// @code{.c}
/// // PanID OTA value of 0x34 0x12.
/// // Short Address OTA byte order of 0x78 0x56.
/// // Long address with OTA byte order of 0x11 0x22 0x33 0x44 0x55 0x66 0x77 0x88.
///
/// // Set up all addresses simultaneously.
/// RAIL_Status_t setup1(void)
/// {
///   RAIL_IEEE802154_AddrConfig_t nodeAddress = {
///     { 0x1234, 0xFFFF, 0xFFFF },
///     { 0x5678, 0xFFFF, 0xFFFF },
///     { { 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88 },
///       { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 },
///       { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 } }
///   };
///   return RAIL_IEEE802154_SetAddresses(railHandle, &nodeAddress);
/// }
///
/// // Alternatively, the addresses can be set up individually as follows:
/// RAIL_Status_t setup2(void)
/// {
///   RAIL_Status_t status;
///   const uint8_t longAddress[] = { 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88 };
///
///   status = RAIL_IEEE802154_SetPanId(railHandle, 0x1234, 0);
///   if (status != RAIL_STATUS_NO_ERROR) {
///     return status
///   }
///   status = RAIL_IEEE802154_SetShortAddress(railHandle, 0x5678, 0);
///   if (status != RAIL_STATUS_NO_ERROR) {
///     return status
///   }
///   status = RAIL_IEEE802154_SetLongAddress(railHandle, longAddress, 0);
///   if (status != RAIL_STATUS_NO_ERROR) {
///     return status
///   }
///
///   return RAIL_STATUS_NO_ERROR;
/// }
/// @endcode
///
/// Address filtering will be enabled except when in promiscuous mode which can
/// be set with RAIL_IEEE802154_SetPromiscuousMode(). The addresses may be
/// changed at runtime. However, if you are receiving a packet while
/// reconfiguring the address filters, you may get undesired behavior so it's
/// safest to do this while not in receive.
///
/// Auto ACK is controlled by the ackConfig and timings fields passed to
/// RAIL_IEEE802154_Init(). After initialization they may be controlled
/// using the normal \ref Auto_Ack and \ref State_Transitions APIs. When in IEEE
/// 802.15.4 mode, the ACK will generally have a 5 byte length, its Frame Type
/// will be ACK, its Frame Version 0 (2003), and its Frame Pending bit will be
/// false unless the \ref RAIL_EVENT_IEEE802154_DATA_REQUEST_COMMAND event is
/// triggered in which case it will default to the
/// \ref RAIL_IEEE802154_Config_t::defaultFramePendingInOutgoingAcks setting.
/// If the default Frame Pending setting is incorrect,
/// the app must call \ref RAIL_IEEE802154_ToggleFramePending
/// (formerly \ref RAIL_IEEE802154_SetFramePending) while handling the
/// \ref RAIL_EVENT_IEEE802154_DATA_REQUEST_COMMAND event.
///
/// This event must be turned on by the user and will fire whenever a data
/// request is being received so that the stack can determine whether there
/// is pending data. Be aware that if the default Frame Pending bit needs to
/// be changed it must be done quickly otherwise the ACK may already
/// have been transmitted with the default setting. Check the return code of
/// RAIL_IEEE802154_ToggleFramePending() to be sure that the bit was changed
/// in time.
///
/// Transmit and receive operations are done using the standard RAIL APIs in
/// IEEE 802.15.4 mode. To send packets using the correct CSMA configuration
/// there is a \ref RAIL_CSMA_CONFIG_802_15_4_2003_2p4_GHz_OQPSK_CSMA define
/// that can initialize the csmaConfig structure passed to \ref
/// RAIL_StartCcaCsmaTx().
/// @{

/**
 * @enum RAIL_IEEE802154_AddressLength_t
 * @brief Different lengths that an 802.15.4 address can have
 */
RAIL_ENUM(RAIL_IEEE802154_AddressLength_t) {
  RAIL_IEEE802154_ShortAddress = 2, /**< 2 byte short address. */
  RAIL_IEEE802154_LongAddress = 3, /**< 8 byte extended address. */
};

#ifndef DOXYGEN_SHOULD_SKIP_THIS
// Self-referencing defines minimize compiler complaints when using RAIL_ENUM
#define RAIL_IEEE802154_ShortAddress ((RAIL_IEEE802154_AddressLength_t) RAIL_IEEE802154_ShortAddress)
#define RAIL_IEEE802154_LongAddress  ((RAIL_IEEE802154_AddressLength_t) RAIL_IEEE802154_LongAddress)
#endif//DOXYGEN_SHOULD_SKIP_THIS

/**
 * @struct RAIL_IEEE802154_Address_t
 * @brief Representation of 802.15.4 address
 * This structure is only used for received source address information
 * needed to perform Frame Pending lookup.
 */
typedef struct RAIL_IEEE802154_Address{
  /** Convenient storage for different address types. */
  union {
    uint16_t shortAddress; /**< Present for 2 byte addresses. */
    uint8_t longAddress[8]; /**< Present for 8 byte addresses. */
  };
  /**
   * Enumeration of the received address length.
   */
  RAIL_IEEE802154_AddressLength_t length;
  /**
   * A bitmask representing which address filter(s) this packet has passed.
   * It is undefined on platforms lacking \ref RAIL_SUPPORTS_ADDR_FILTER_MASK.
   */
  RAIL_AddrFilterMask_t filterMask;
} RAIL_IEEE802154_Address_t;

/** The maximum number of allowed addresses of each type. */
#define RAIL_IEEE802154_MAX_ADDRESSES (3U)

/**
 * @struct RAIL_IEEE802154_AddrConfig_t
 * @brief A configuration structure for IEEE 802.15.4 Address Filtering. The
 * broadcast addresses are handled separately and do not need to be specified
 * here. Any address to be ignored should be set with all bits high.
 *
 * This structure allows configuration of multi-PAN functionality by specifying
 * multiple PAN IDs and short addresses. A packet will be received if it matches
 * an address and its corresponding PAN ID. Long address 0 and short address 0
 * match against PAN ID 0, etc. The broadcast PAN ID and address will work with
 * any address or PAN ID, respectively.
 */
typedef struct RAIL_IEEE802154_AddrConfig{
  /**
   * PAN IDs for destination filtering. All must be specified.
   * To disable a PAN ID, set it to the broadcast value, 0xFFFF.
   */
  uint16_t panId[RAIL_IEEE802154_MAX_ADDRESSES];
  /**
   * A short network addresses for destination filtering. All must be specified.
   * To disable a short address, set it to the broadcast value, 0xFFFF.
   */
  uint16_t shortAddr[RAIL_IEEE802154_MAX_ADDRESSES];
  /**
   * A 64-bit address for destination filtering. All must be specified.
   * This field is parsed in over-the-air (OTA) byte order. To disable a long
   * address, set it to the reserved value of 0x00 00 00 00 00 00 00 00.
   */
  uint8_t longAddr[RAIL_IEEE802154_MAX_ADDRESSES][8];
} RAIL_IEEE802154_AddrConfig_t;

/**
 * @struct RAIL_IEEE802154_Config_t
 * @brief A configuration structure for IEEE 802.15.4 in RAIL.
 */
typedef struct RAIL_IEEE802154_Config {
  /**
   * Configure the RAIL Address Filter to allow the given destination
   * addresses. If this pointer is NULL, defer destination address configuration.
   * If a member of addresses is NULL, defer configuration of just that member.
   * This can be overridden via RAIL_IEEE802154_SetAddresses(), or the
   * individual members can be changed via RAIL_IEEE802154_SetPanId(),
   * RAIL_IEEE802154_SetShortAddress(), and RAIL_IEEE802154_SetLongAddress().
   */
  const RAIL_IEEE802154_AddrConfig_t *addresses;
  /**
   * Define the ACKing configuration for the IEEE 802.15.4 implementation.
   */
  RAIL_AutoAckConfig_t ackConfig;
  /**
   * Define state timings for the IEEE 802.15.4 implementation.
   */
  RAIL_StateTiming_t timings;
  /**
   * Set which 802.15.4 frame types will be received, of Beacon, Data, ACK, and
   * Command. This setting can be overridden via RAIL_IEEE802154_AcceptFrames().
   */
  uint8_t framesMask;
  /**
   * Enable promiscuous mode during configuration. This can be overridden via
   * RAIL_IEEE802154_SetPromiscuousMode() afterwards.
   */
  bool promiscuousMode;
  /**
   * Set whether the device is a PAN Coordinator during configuration. This can
   * be overridden via RAIL_IEEE802154_SetPanCoordinator() afterwards.
   */
  bool isPanCoordinator;
  /**
   * The default value for the Frame Pending bit in outgoing ACKs for packets
   * that triggered the \ref RAIL_EVENT_IEEE802154_DATA_REQUEST_COMMAND event.
   * Such an ACK's Frame Pending bit can be inverted if necessary during the
   * handling of that event by calling \ref RAIL_IEEE802154_ToggleFramePending
   * (formerly \ref RAIL_IEEE802154_SetFramePending).
   */
  bool defaultFramePendingInOutgoingAcks;
} RAIL_IEEE802154_Config_t;

/**
 * Initialize RAIL for IEEE802.15.4 features.
 *
 * @param[in] railHandle A handle of RAIL instance.
 * @param[in] config An IEEE802154 configuration structure.
 * @return A status code indicating success of the function call.
 *
 * This function calls the following RAIL functions to configure the radio for
 * IEEE802.15.4 features.
 *
 * Initializes the following:
 *   - Enables IEEE802154 hardware acceleration
 *   - Configures RAIL Auto ACK functionality
 *   - Configures RAIL Address Filter for 802.15.4 address filtering
 *
 * It saves having to call the following functions individually:
 * - RAIL_ConfigAutoAck()
 * - RAIL_SetRxTransitions()
 * - RAIL_SetTxTransitions()
 * - RAIL_WriteAutoAckFifo()
 * - RAIL_SetStateTiming()
 * - RAIL_ConfigAddressFilter()
 * - RAIL_EnableAddressFilter()
 */
RAIL_Status_t RAIL_IEEE802154_Init(RAIL_Handle_t railHandle,
                                   const RAIL_IEEE802154_Config_t *config);

/**
 * Configure the radio for 2.4 GHz 802.15.4 operation.
 *
 * @param[in] railHandle A handle of RAIL instance.
 * @return A status code indicating success of the function call.
 *
 * This initializes the radio for 2.4 GHz operation. It takes the place of
 * calling \ref RAIL_ConfigChannels. After this call,
 * channels 11-26 will be available, giving the frequencies of those channels
 * on channel page 0, as defined by IEEE 802.15.4-2011 section 8.1.2.2.
 */
RAIL_Status_t RAIL_IEEE802154_Config2p4GHzRadio(RAIL_Handle_t railHandle);

/**
 * Configure the radio for 2.4 GHz 802.15.4 operation with antenna diversity.
 *
 * @param[in] railHandle A handle of RAIL instance.
 * @return A status code indicating success of the function call.
 *
 * This initializes the radio for 2.4 GHz operation, but with a configuration
 * that supports antenna diversity. It takes the place of
 * calling \ref RAIL_ConfigChannels. After this call,
 * channels 11-26 will be available, giving the frequencies of those channels
 * on channel page 0, as defined by IEEE 802.15.4-2011 section 8.1.2.2.
 */
RAIL_Status_t RAIL_IEEE802154_Config2p4GHzRadioAntDiv(RAIL_Handle_t railHandle);

/**
 * Configure the radio for 2.4 GHz 802.15.4 operation with antenna diversity
 * optimized for radio coexistence.
 *
 * @param[in] railHandle A handle of RAIL instance.
 * @return A status code indicating success of the function call.
 *
 * This initializes the radio for 2.4 GHz operation, but with a configuration
 * that supports antenna diversity optimized for radio coexistence. It takes
 * the place of calling \ref RAIL_ConfigChannels. After this call,
 * channels 11-26 will be available, giving the frequencies of those channels
 * on channel page 0, as defined by IEEE 802.15.4-2011 section 8.1.2.2.
 */
RAIL_Status_t RAIL_IEEE802154_Config2p4GHzRadioAntDivCoex(RAIL_Handle_t railHandle);

/**
 * Configure the radio for 2.4 GHz 802.15.4 operation optimized for radio coexistence.
 *
 * @param[in] railHandle A handle of RAIL instance.
 * @return A status code indicating success of the function call.
 *
 * This initializes the radio for 2.4 GHz operation, but with a configuration
 * that supports radio coexistence. It takes the place of
 * calling \ref RAIL_ConfigChannels. After this call,
 * channels 11-26 will be available, giving the frequencies of those channels
 * on channel page 0, as defined by IEEE 802.15.4-2011 section 8.1.2.2.
 */
RAIL_Status_t RAIL_IEEE802154_Config2p4GHzRadioCoex(RAIL_Handle_t railHandle);

/**
 * Configure the radio for 2.4 GHz 802.15.4 operation with a front end module.
 *
 * @param[in] railHandle A handle of RAIL instance.
 * @return A status code indicating success of the function call.
 *
 * This initializes the radio for 2.4 GHz operation, but with a configuration
 * that supports a front end module. It takes the place of
 * calling \ref RAIL_ConfigChannels. After this call,
 * channels 11-26 will be available, giving the frequencies of those channels
 * on channel page 0, as defined by IEEE 802.15.4-2011 section 8.1.2.2.
 */
RAIL_Status_t RAIL_IEEE802154_Config2p4GHzRadioFem(RAIL_Handle_t railHandle);

/**
 * Configure the radio for 2.4 GHz 802.15.4 operation with antenna diversity
 * optimized for a front end module.
 *
 * @param[in] railHandle A handle of RAIL instance.
 * @return A status code indicating success of the function call.
 *
 * This initializes the radio for 2.4 GHz operation, but with a configuration
 * that supports antenna diversity and a front end module. It takes the place of
 * calling \ref RAIL_ConfigChannels. After this call,
 * channels 11-26 will be available, giving the frequencies of those channels
 * on channel page 0, as defined by IEEE 802.15.4-2011 section 8.1.2.2.
 */
RAIL_Status_t RAIL_IEEE802154_Config2p4GHzRadioAntDivFem(RAIL_Handle_t railHandle);

/**
 * Configure the radio for 2.4 GHz 802.15.4 operation optimized for radio coexistence
 * and a front end module.
 *
 * @param[in] railHandle A handle of RAIL instance.
 * @return A status code indicating success of the function call.
 *
 * This initializes the radio for 2.4 GHz operation, but with a configuration
 * that supports radio coexistence and a front end module. It takes the place of
 * calling \ref RAIL_ConfigChannels. After this call,
 * channels 11-26 will be available, giving the frequencies of those channels
 * on channel page 0, as defined by IEEE 802.15.4-2011 section 8.1.2.2.
 */
RAIL_Status_t RAIL_IEEE802154_Config2p4GHzRadioCoexFem(RAIL_Handle_t railHandle);

/**
 * Configure the radio for 2.4 GHz 802.15.4 operation with antenna diversity
 * optimized for radio coexistence and a front end module.
 *
 * @param[in] railHandle A handle of RAIL instance.
 * @return A status code indicating success of the function call.
 *
 * This initializes the radio for 2.4 GHz operation, but with a configuration
 * that supports antenna diversity, radio coexistence and a front end module.
 * It takes the place of calling \ref RAIL_ConfigChannels.
 * After this call, channels 11-26 will be available, giving the frequencies of
 * those channels on channel page 0, as defined by IEEE 802.15.4-2011 section 8.1.2.2.
 */
RAIL_Status_t RAIL_IEEE802154_Config2p4GHzRadioAntDivCoexFem(RAIL_Handle_t railHandle);

/**
 * Configure the radio for SubGHz GB868 863 MHz 802.15.4 operation.
 *
 * @param[in] railHandle A handle of RAIL instance.
 * @return A status code indicating success of the function call.
 *
 * This initializes the radio for SubGHz GB868 863 MHz operation. It takes the
 * place of calling \ref RAIL_ConfigChannels.
 * After this call, GB868 channels in the 863 MHz band (channel pages 28, 29,
 * and 30 -- logical channels 0x80..0x9A, 0xA0..0xA8, 0xC0..0xDA, respectively)
 * will be available, as defined by Rev 22 of the Zigbee Specification, 2017
 * document 05-3474-22, section D.10.2.1.3.2.
 */
RAIL_Status_t RAIL_IEEE802154_ConfigGB863MHzRadio(RAIL_Handle_t railHandle);

/**
 * Configure the radio for SubGHz GB868 915 MHz 802.15.4 operation.
 *
 * @param[in] railHandle A handle of RAIL instance.
 * @return A status code indicating success of the function call.
 *
 * This initializes the radio for SubGHz GB868 915 MHz operation. It takes the
 * place of calling \ref RAIL_ConfigChannels.
 * After this call, GB868 channels in the 915 MHz band (channel page 31 --
 * logical channels 0xE0..0xFA) will be available, as defined by Rev 22 of
 * the Zigbee Specification, 2017 document 05-3474-22, section D.10.2.1.3.2.
 */
RAIL_Status_t RAIL_IEEE802154_ConfigGB915MHzRadio(RAIL_Handle_t railHandle);

/**
 * De-initialize IEEE802.15.4 hardware acceleration.
 *
 * @param[in] railHandle A handle of RAIL instance.
 * @return A status code indicating success of the function call.
 *
 * Disables and resets all IEE802.15.4 hardware acceleration features. This
 * function should only be called when the radio is IDLE. This calls the
 * following:
 * - RAIL_SetStateTiming(), to reset all timings to 100 us
 * - RAIL_EnableAddressFilter(false)
 * - RAIL_ResetAddressFilter()
 */
RAIL_Status_t RAIL_IEEE802154_Deinit(RAIL_Handle_t railHandle);

/**
 * Return whether IEEE802.15.4 hardware acceleration is currently enabled.
 *
 * @param[in] railHandle A handle of RAIL instance.
 * @return True if IEEE802.15.4 hardware acceleration was enabled to start with
 * and false otherwise.
 */
bool RAIL_IEEE802154_IsEnabled(RAIL_Handle_t railHandle);

/**
 * @enum RAIL_IEEE802154_PtiRadioConfig_t
 * @brief 802.15.4 PTI radio configuration mode
 */
RAIL_ENUM(RAIL_IEEE802154_PtiRadioConfig_t) {
  /**
   * 2.4Ghz 802.15.4 radio configuration.
   */
  RAIL_IEEE802154_PTI_RADIO_CONFIG_2P4GHZ = 0x0,
  /**
   * 2.4Ghz 802.15.4 radio configuration
   * with RX antenna diversity support.
   */
  RAIL_IEEE802154_PTI_RADIO_CONFIG_2P4GHZ_ANTDIV = 0x1,
  /**
   * 2.4Ghz 802.15.4 radio configuration
   * optimized for radio coexistence.
   */
  RAIL_IEEE802154_PTI_RADIO_CONFIG_2P4GHZ_COEX = 0x2,
  /**
   * 2.4Ghz 802.15.4 radio configuration with
   * RX antenna diversity support optimized for radio coexistence.
   */
  RAIL_IEEE802154_PTI_RADIO_CONFIG_2P4GHZ_ANTDIV_COEX = 0x3,
  /**
   * 863MHz GB868 802.15.4 radio configuration.
   */
  RAIL_IEEE802154_PTI_RADIO_CONFIG_863MHZ_GB868 = 0x85,
  /**
   * 915MHz GB868 802.15.4 radio configuration.
   */
  RAIL_IEEE802154_PTI_RADIO_CONFIG_915MHZ_GB868 = 0x86
};

#ifndef DOXYGEN_SHOULD_SKIP_THIS
// Self-referencing defines minimize compiler complaints when using RAIL_ENUM
#define RAIL_IEEE802154_PTI_RADIO_CONFIG_2P4GHZ ((RAIL_IEEE802154_PtiRadioConfig_t) RAIL_IEEE802154_PTI_RADIO_CONFIG_2P4GHZ)
#define RAIL_IEEE802154_PTI_RADIO_CONFIG_2P4GHZ_ANTDIV  ((RAIL_IEEE802154_PtiRadioConfig_t) RAIL_IEEE802154_PTI_RADIO_CONFIG_2P4GHZ_ANTDIV)
#define RAIL_IEEE802154_PTI_RADIO_CONFIG_2P4GHZ_COEX ((RAIL_IEEE802154_PtiRadioConfig_t) RAIL_IEEE802154_PTI_RADIO_CONFIG_2P4GHZ_COEX)
#define RAIL_IEEE802154_PTI_RADIO_CONFIG_2P4GHZ_ANTDIV_COEX  ((RAIL_IEEE802154_PtiRadioConfig_t) RAIL_IEEE802154_PTI_RADIO_CONFIG_2P4GHZ_ANTDIV_COEX)
#define RAIL_IEEE802154_PTI_RADIO_CONFIG_863MHZ_GB868 ((RAIL_IEEE802154_PtiRadioConfig_t) RAIL_IEEE802154_PTI_RADIO_CONFIG_863MHZ_GB868)
#define RAIL_IEEE802154_PTI_RADIO_CONFIG_915MHZ_GB868  ((RAIL_IEEE802154_PtiRadioConfig_t) RAIL_IEEE802154_PTI_RADIO_CONFIG_915MHZ_GB868)
#endif//DOXYGEN_SHOULD_SKIP_THIS

/**
 * Return IEEE802.15.4 PTI radio config.
 *
 * @param[in] railHandle A handle of RAIL instance.
 * @return PTI(Packet Trace Information) radio config.
 */
RAIL_IEEE802154_PtiRadioConfig_t RAIL_IEEE802154_GetPtiRadioConfig(RAIL_Handle_t railHandle);

/**
 * Configure the RAIL Address Filter for 802.15.4 filtering.
 *
 * @param[in] railHandle A handle of RAIL instance.
 * @param[in] addresses The address information that should be used.
 * @return A status code indicating success of the function call. If this returns
 * an error, the 802.15.4 address filter is in an undefined state.
 *
 * Set up the 802.15.4 address filter to accept messages to the given
 * addresses. This will return false if any of the addresses failed to be set.
 * If NULL is passed in for addresses, all addresses will be set to their
 * reset value.
 */
RAIL_Status_t RAIL_IEEE802154_SetAddresses(RAIL_Handle_t railHandle,
                                           const RAIL_IEEE802154_AddrConfig_t *addresses);

/**
 * Set a PAN ID for 802.15.4 address filtering.
 *
 * @param[in] railHandle A handle of RAIL instance.
 * @param[in] panId The 16-bit PAN ID information.
 * This will be matched against the destination PAN ID of incoming messages.
 * The PAN ID is sent little endian over the air, meaning panId[7:0] is first in
 * the payload followed by panId[15:8]. Set to 0xFFFF to disable for this index.
 * @param[in] index Indicates which PAN ID to set. Must be below
 * RAIL_IEEE802154_MAX_ADDRESSES.
 * @return A status code indicating success of the function call.
 *
 * Set up the 802.15.4 address filter to accept messages to the given PAN ID.
 */
RAIL_Status_t RAIL_IEEE802154_SetPanId(RAIL_Handle_t railHandle,
                                       uint16_t panId,
                                       uint8_t index);

/**
 * Set a short address for 802.15.4 address filtering.
 *
 * @param[in] railHandle A handle of RAIL instance
 * @param[in] shortAddr 16 bit short address value. This will be matched against the
 * destination short address of incoming messages. The short address is sent
 * little endian over the air meaning shortAddr[7:0] is first in the payload
 * followed by shortAddr[15:8]. Set to 0xFFFF to disable for this index.
 * @param[in] index Which short address to set. Must be below
 * RAIL_IEEE802154_MAX_ADDRESSES.
 * @return A status code indicating success of the function call.
 *
 * Set up the 802.15.4 address filter to accept messages to the given short
 * address.
 */
RAIL_Status_t RAIL_IEEE802154_SetShortAddress(RAIL_Handle_t railHandle,
                                              uint16_t shortAddr,
                                              uint8_t index);

/**
 * Set a long address for 802.15.4 address filtering.
 *
 * @param[in] railHandle A handle of RAIL instance.
 * @param[in] longAddr A pointer to an 8-byte array containing the long address
 * information. The long address must be in over-the-air byte order. This will
 * be matched against the destination long address of incoming messages. Set to
 * 0x00 00 00 00 00 00 00 00 to disable for this index.
 * @param[in] index Indicates which long address to set. Must be below
 * RAIL_IEEE802154_MAX_ADDRESSES.
 * @return A status code indicating success of the function call.
 *
 * Set up the 802.15.4 address filter to accept messages to the given long
 * address.
 */
RAIL_Status_t RAIL_IEEE802154_SetLongAddress(RAIL_Handle_t railHandle,
                                             const uint8_t *longAddr,
                                             uint8_t index);

/**
 * Set whether the current node is a PAN coordinator.
 *
 * @param[in] railHandle A handle of RAIL instance.
 * @param[in] isPanCoordinator True if this device is a PAN coordinator.
 * @return A status code indicating success of the function call.
 *
 * If the device is a PAN Coordinator, it will accept data and command
 * frames with no destination address. This function will fail if 802.15.4
 * hardware acceleration is not currently enabled. This setting may be changed
 * at any time when 802.15.4 hardware acceleration is enabled.
 */
RAIL_Status_t RAIL_IEEE802154_SetPanCoordinator(RAIL_Handle_t railHandle,
                                                bool isPanCoordinator);

/**
 * Set whether to enable 802.15.4 promiscuous mode.
 *
 * @param[in] railHandle A handle of RAIL instance.
 * @param[in] enable True if all frames and addresses should be accepted.
 * @return A status code indicating success of the function call.
 *
 * If promiscuous mode is enabled, no frame or address filtering steps
 * will be performed other than checking the CRC. This function will fail if
 * 802.15.4 hardware acceleration is not currently enabled. This setting may be
 * changed at any time when 802.15.4 hardware acceleration is enabled.
 */
RAIL_Status_t RAIL_IEEE802154_SetPromiscuousMode(RAIL_Handle_t railHandle,
                                                 bool enable);

/**
 * @enum RAIL_IEEE802154_EOptions_t
 * @brief 802.15.4E-2012 options, in reality a bitmask.
 */
RAIL_ENUM_GENERIC(RAIL_IEEE802154_EOptions_t, uint32_t) {
  /** Shift position of \ref RAIL_IEEE802154_E_OPTION_GB868 bit. */
  RAIL_IEEE802154_E_OPTION_GB868_SHIFT = 0,
  RAIL_IEEE802154_E_OPTION_ENH_ACK_SHIFT,
  RAIL_IEEE802154_E_OPTION_IMPLICIT_BROADCAST_SHIFT,
};

/** A value representing no options enabled. */
#define RAIL_IEEE802154_E_OPTIONS_NONE 0UL
/** All options disabled by default . */
#define RAIL_IEEE802154_E_OPTIONS_DEFAULT RAIL_IEEE802154_E_OPTIONS_NONE

/**
 * An option to enable/disable 802.15.4E-2012 features needed for GB868.
 * When not promiscuous, RAIL normally accepts only 802.15.4 MAC frames
 * whose MAC header Frame Version is 0 (802.15.4-2003) or 1 (802.15.4-2006),
 * filtering out higher Frame Version packets (as \ref
 * RAIL_RX_PACKET_ABORT_FORMAT).
 * Enabling this feature additionally allows Frame Version 2 (802.15.4E-2012 /
 * 802.15.4-2015) packets to be accepted and passed to the application.
 *
 * @note If 802.15.4 MAC-level encryption is used with Frame Version 2
 *   frames, RAIL_IEEE802154_EnableEarlyFramePending() should also be
 *   called otherwise data polls may not be recognized to trigger \ref
 *   RAIL_EVENT_IEEE802154_DATA_REQUEST_COMMAND events.
 *
 * @note Enabling this feature also automatically enables \ref
 *   RAIL_IEEE802154_E_OPTION_ENH_ACK on platforms that support
 *   that feature.
 *
 * @note This feature does not automatically enable receiving Multipurpose
 *   frames; that can be enabled via RAIL_IEEE802154_AcceptFrames()'s
 *   \ref RAIL_IEEE802154_ACCEPT_MULTIPURPOSE_FRAMES.
 */
#define RAIL_IEEE802154_E_OPTION_GB868 (1UL << RAIL_IEEE802154_E_OPTION_GB868_SHIFT)

/**
 * An option to enable/disable 802.15.4E-2012 features needed for Enhanced ACKs.
 * This option requires that \ref RAIL_IEEE802154_E_OPTION_GB868 also be
 * enabled, and is enabled automatically on platforms that support this
 * feature. It exists as a separate flag to allow runtime detection of whether
 * the platform supports this feature or not.
 *
 * When enabled, only an Enhanced ACK is expected in response to a transmitted
 * ACK-requesting 802.15.4E Frame Version 2 frame, and when such a frame is
 * received, the application is expected to generate the Enhanced ACK
 * while processing \ref RAIL_EVENT_IEEE802154_DATA_REQUEST_COMMAND and
 * call \ref RAIL_IEEE802154_WriteEnhAck() in time for that Enhanced ACK to
 * be sent. For this to work properly, the application should enable both
 * \ref RAIL_IEEE802154_EnableEarlyFramePending() and
 * \ref RAIL_IEEE802154_EnableDataFramePending(), and use
 * \ref RAIL_GetRxIncomingPacketInfo() to determine whether an Enhanced ACK
 * is needed along the contents of that ACK packet.
 *
 * On 802.15.4E GB868 platforms that lack this support, legacy Immediate ACKs
 * are sent/expected for received/transmitted ACK-requesting 802.15.4E Frame
 * Version 2 frames; calls to \ref RAIL_IEEE802154_WriteEnhAck() have no
 * effect. Attempting to use this feature via \ref
 * RAIL_IEEE802154_ConfigEOptions() returns an error.
 */
#define RAIL_IEEE802154_E_OPTION_ENH_ACK (1UL << RAIL_IEEE802154_E_OPTION_ENH_ACK_SHIFT)

/**
 * An option to enable/disable 802.15.4E-2012 macImplicitBroadcast feature.
 *
 * When enabled, received Frame Version 2 frames without a destination
 * PAN ID or destination address are treated as though they are addressed
 * to the broadcast PAN ID and broadcast short address. When disabled, such
 * frames are filtered unless the device is the PAN coordinator and
 * appropriate source addressing information exists in the packet
 */
#define RAIL_IEEE802154_E_OPTION_IMPLICIT_BROADCAST (1UL << RAIL_IEEE802154_E_OPTION_IMPLICIT_BROADCAST_SHIFT)

/** A value representing all possible options. */
#define RAIL_IEEE802154_E_OPTIONS_ALL 0xFFFFFFFFUL

/**
 * Configure certain 802.15.4E-2012 / 802.15.4-2015 Frame Version 2 features.
 *
 * @param[in] railHandle A handle of RAIL instance.
 * @param[in] mask A bitmask containing which options should be modified.
 * @param[in] options A bitmask containing desired options settings.
 *   Bit positions for each option are found in the \ref
 *   RAIL_IEEE802154_EOptions_t.
 * @return A status code indicating success of the function call.
 *
 * This function will fail if 802.15.4 hardware acceleration is not
 * currently enabled or the platform does not support the feature(s).
 * These settings may be changed at any time when 802.15.4 hardware
 * acceleration is enabled.
 */
RAIL_Status_t RAIL_IEEE802154_ConfigEOptions(RAIL_Handle_t railHandle,
                                             RAIL_IEEE802154_EOptions_t mask,
                                             RAIL_IEEE802154_EOptions_t options);

/**
 * @enum RAIL_IEEE802154_GOptions_t
 * @brief 802.15.4G-2012 options, in reality a bitmask.
 */
RAIL_ENUM_GENERIC(RAIL_IEEE802154_GOptions_t, uint32_t) {
  /** Shift position of \ref RAIL_IEEE802154_G_OPTION_GB868 bit. */
  RAIL_IEEE802154_G_OPTION_GB868_SHIFT = 0,
};

/** A value representing no options enabled. */
#define RAIL_IEEE802154_G_OPTIONS_NONE 0UL
/** All options disabled by default . */
#define RAIL_IEEE802154_G_OPTIONS_DEFAULT RAIL_IEEE802154_G_OPTIONS_NONE

/**
 * An option to enable/disable 802.15.4G-2012 features needed for GB868.
 * Normally RAIL supports 802.15.4-2003 and -2006 radio configurations
 * that have the single-byte PHY header allowing frames up to 128 bytes
 * in size. This feature must be enabled for 802.15.4G-2012 or
 * 802.15.4-2015 SUN PHY radio configurations with the two-byte
 * bit-reversed-length PHY header format.
 *
 * While GB868 only supports whitened non-FEC non-mode-switch frames
 * up to 129 bytes including 2-byte CRC, this option also enables:
 * - On platforms where \ref RAIL_FEAT_IEEE802154_G_4BYTE_CRC_SUPPORTED
 *   is true: automatic per-packet 2/4-byte Frame Check Sequence (FCS)
 *   reception and transmission based on the FCS Type bit in the
 *   received/transmitted PHY header. This includes ACK reception
 *   and automatically-generated ACKs reflect the CRC size of the
 *   incoming frame being acknowledged (i.e., their MAC payload will be
 *   increased to 7 bytes when sending 4-byte FCS).
 *   On other platforms, only the 2-byte FCS is supported.
 * - On platforms where \ref RAIL_FEAT_IEEE802154_G_UNWHITENED_RX_SUPPORTED
 *   and/or \ref RAIL_FEAT_IEEE802154_G_UNWHITENED_TX_SUPPORTED are true:
 *   automatic per-packet whitened/unwhitened reception and transmission,
 *   respectively, based on the Data Whitening bit in the received/transmitted
 *   PHY header. This includes ACK reception and automatically-generated ACKs
 *   which reflect the whitening of the incoming frame being acknowledged.
 *   On other platforms, only whitened frames are supported.
 * - Support for frames up to 2049 bytes per the radio configuration's
 *   maximum packet length setting.
 *
 * @note Sending/receiving whitened frames assumes the radio configuration
 *   has established an appropriate 802.15.4-compliant whitening algorithm.
 *   RAIL does not itself override the radio configuration's whitening
 *   settings other than to enable/disable it per-packet based on the
 *   packet's PHY header Data Whitening flag.
 */
#define RAIL_IEEE802154_G_OPTION_GB868 (1UL << RAIL_IEEE802154_G_OPTION_GB868_SHIFT)

/** A value representing all possible options. */
#define RAIL_IEEE802154_G_OPTIONS_ALL 0xFFFFFFFFUL

/**
 * Configure certain 802.15.4G-2012 / 802.15.4-2015 SUN PHY features
 * (only for radio configurations designed accordingly).
 *
 * @param[in] railHandle A handle of RAIL instance.
 * @param[in] mask A bitmask containing which options should be modified.
 * @param[in] options A bitmask containing desired options settings.
 *   Bit positions for each option are found in the \ref
 *   RAIL_IEEE802154_GOptions_t.
 * @return A status code indicating success of the function call.
 *
 * This function will fail if 802.15.4 hardware acceleration is not
 * currently enabled, the platform does not support the feature(s),
 * the radio configuration is not appropriate, or the radio is not idle.
 */
RAIL_Status_t RAIL_IEEE802154_ConfigGOptions(RAIL_Handle_t railHandle,
                                             RAIL_IEEE802154_GOptions_t mask,
                                             RAIL_IEEE802154_GOptions_t options);

/// When receiving packets, accept 802.15.4 BEACON frame types.
#define RAIL_IEEE802154_ACCEPT_BEACON_FRAMES       (0x01)
/// When receiving packets, accept 802.15.4 DATA frame types.
#define RAIL_IEEE802154_ACCEPT_DATA_FRAMES         (0x02)
/// When receiving packets, accept 802.15.4 ACK frame types.
/// @note Expected ACK frame types will still be accepted regardless
///   of this setting when waiting for an ACK after a transmit that
///   used \ref RAIL_TX_OPTION_WAIT_FOR_ACK and auto-ACK is enabled.
#define RAIL_IEEE802154_ACCEPT_ACK_FRAMES          (0x04)
/// When receiving packets, accept 802.15.4 COMMAND frame types.
#define RAIL_IEEE802154_ACCEPT_COMMAND_FRAMES      (0x08)
// Reserved for possible future use:               (0x10)
/// When receiving packets, accept 802.15.4-2015 Multipurpose frame types.
/// (Not supported on EFR32XG1.)
#define RAIL_IEEE802154_ACCEPT_MULTIPURPOSE_FRAMES (0x20)

/// In standard operation, accept BEACON, DATA and COMMAND frames.
/// Don't receive ACK frames unless waiting for ACK (i.e., only
/// receive expected ACKs).
#define RAIL_IEEE802154_ACCEPT_STANDARD_FRAMES (RAIL_IEEE802154_ACCEPT_BEACON_FRAMES \
                                                | RAIL_IEEE802154_ACCEPT_DATA_FRAMES \
                                                | RAIL_IEEE802154_ACCEPT_COMMAND_FRAMES)

/**
 * Set which 802.15.4 frame types to accept.
 *
 * @param[in] railHandle A handle of RAIL instance.
 * @param[in] framesMask A mask containing which 802.15.4 frame types to receive.
 * @return A status code indicating success of the function call.
 *
 * This function will fail if 802.15.4 hardware acceleration is not currently
 * enabled or framesMask requests an unsupported frame type.
 * This setting may be changed at any time when 802.15.4 hardware
 * acceleration is enabled. Only Beacon, Data, ACK, Command, and Multipurpose
 * (except on EFR32XG1) frames may be received.
 * The RAIL_IEEE802154_ACCEPT_XXX_FRAMES defines may be combined to create a
 * bitmask to pass into this function.
 *
 * \ref RAIL_IEEE802154_ACCEPT_ACK_FRAMES behaves slightly different than the
 * other defines. If \ref RAIL_IEEE802154_ACCEPT_ACK_FRAMES is set, the radio
 * will accept an ACK frame during normal packet reception, but only a
 * truly expected ACK will have its \ref RAIL_RxPacketDetails_t::isAck true.
 * If \ref RAIL_IEEE802154_ACCEPT_ACK_FRAMES is not set, ACK frames will be
 * filtered unless they're expected when the radio is waiting for an ACK.
 */
RAIL_Status_t RAIL_IEEE802154_AcceptFrames(RAIL_Handle_t railHandle,
                                           uint8_t framesMask);

/**
 * Enable early Frame Pending lookup event notification
 * (RAIL_EVENT_IEEE802154_DATA_REQUEST_COMMAND).
 *
 * @param[in] railHandle A handle of RAIL instance.
 * @param[in] enable True to enable, false to disable.
 * @return A status code indicating success of the function call.
 *
 * Normally RAIL_EVENT_IEEE802154_DATA_REQUEST_COMMAND is triggered after
 * receiving the entire MAC header for a MAC command and the MAC
 * command byte indicating the packet is a data request. Enabling this
 * feature causes this event to be triggered earlier, right after receiving
 * the source address information in the MAC header, allowing for more time
 * to perform the lookup and call \ref RAIL_IEEE802154_ToggleFramePending()
 * to update the Frame Pending bit in the outgoing ACK for the incoming frame.
 * This feature is also necessary for handling 802.15.4 MAC-encrypted
 * frames where the MAC Command byte is encrypted (MAC Frame Version 2) --
 * see \ref RAIL_IEEE802154_ConfigEOptions().
 *
 * This function will fail if 802.15.4 hardware acceleration is not
 * currently enabled, or on platforms that do not support this feature.
 * This setting may be changed at any time when 802.15.4 hardware
 * acceleration is enabled.
 */
RAIL_Status_t RAIL_IEEE802154_EnableEarlyFramePending(RAIL_Handle_t railHandle,
                                                      bool enable);

/**
 * Enable Frame Pending lookup event notification
 * (RAIL_EVENT_IEEE802154_DATA_REQUEST_COMMAND) for MAC Data frames.
 *
 * @param[in] railHandle A handle of RAIL instance.
 * @param[in] enable True to enable, false to disable.
 * @return A status code indicating success of the function call.
 *
 * Normally RAIL_EVENT_IEEE802154_DATA_REQUEST_COMMAND is triggered only
 * for MAC command frames whose MAC command byte indicates the packet is
 * a data request. Enabling this feature causes this event to also be
 * triggered for MAC data frames right after receiving the source
 * address information in the MAC header -- necessary to support the
 * Thread Basil-Hayden Enhanced Frame Pending feature.
 *
 * This function will fail if 802.15.4 hardware acceleration is not
 * currently enabled. This setting may be changed at any time when
 * 802.15.4 hardware acceleration is enabled.
 */
RAIL_Status_t RAIL_IEEE802154_EnableDataFramePending(RAIL_Handle_t railHandle,
                                                     bool enable);

/**
 * Alternate naming for function \ref RAIL_IEEE802154_SetFramePending
 * to depict it is used for changing the default setting specified by
 * \ref RAIL_IEEE802154_Config_t::defaultFramePendingInOutgoingAcks in
 * an outgoing ACK.
 */
 #define RAIL_IEEE802154_ToggleFramePending RAIL_IEEE802154_SetFramePending

/**
 * Change the Frame Pending bit on the outgoing legacy Immediate ACK from
 * the default specified by
 * \ref RAIL_IEEE802154_Config_t::defaultFramePendingInOutgoingAcks.
 * @param[in] railHandle A handle of RAIL instance
 * @return A status code indicating success of the function call.
 *
 * This function must only be called while processing the \ref
 * RAIL_EVENT_IEEE802154_DATA_REQUEST_COMMAND if the ACK
 * for this packet should go out with its Frame Pending bit set differently
 * than what was specified by
 * \ref RAIL_IEEE802154_Config_t::defaultFramePendingInOutgoingAcks.
 *
 * It's intended only for use with 802.15.4 legacy Immediate ACKs and
 * not 802.15.4E Enhanced ACKs.
 * This will return \ref RAIL_STATUS_INVALID_STATE if it is too late to
 * modify the outgoing Immediate ACK.

 * @note This function is used to set the Frame Pending bit but its meaning
 * depends on the value of
 * \ref RAIL_IEEE802154_Config_t::defaultFramePendingInOutgoingAcks
 * while transmitting ACK.
 * If \ref RAIL_IEEE802154_Config_t::defaultFramePendingInOutgoingAcks
 * is not set, then Frame Pending bit is set in outgoing ACK.
 * Whereas, if \ref RAIL_IEEE802154_Config_t::defaultFramePendingInOutgoingAcks
 * is set, then Frame Pending bit is cleared in outgoing ACK.
 *
 * Therefore, this function is to be called if the frame is pending when
 * \ref RAIL_IEEE802154_Config_t::defaultFramePendingInOutgoingAcks
 * is not set or if there is no frame pending when
 * \ref RAIL_IEEE802154_Config_t::defaultFramePendingInOutgoingAcks
 * is set.
 */
RAIL_Status_t RAIL_IEEE802154_SetFramePending(RAIL_Handle_t railHandle);

/**
 * Get the source address of the incoming data request.
 *
 * @param[in] railHandle A RAIL instance handle.
 * @param[out] pAddress A pointer to \ref RAIL_IEEE802154_Address_t structure
 *   to populate with source address information.
 * @return A status code indicating success of the function call.
 *
 * This function must only be called when handling the \ref
 * RAIL_EVENT_IEEE802154_DATA_REQUEST_COMMAND event. This will return
 * \ref RAIL_STATUS_INVALID_STATE if the address information is stale
 * (i.e., it is too late to affect the outgoing ACK).
 */
RAIL_Status_t RAIL_IEEE802154_GetAddress(RAIL_Handle_t railHandle,
                                         RAIL_IEEE802154_Address_t *pAddress);

/**
 * Write the AutoACK FIFO for the next outgoing 802.15.4E Enhanced ACK.
 *
 * @param[in] railHandle A handle of RAIL instance.
 * @param[in] ackData Pointer to ACK data to transmit
 * @param[in] ackDataLen Length of ACK data, in bytes
 * @return A status code indicating success of the function call.
 *
 * This function sets the AutoACK data to use in acknowledging the frame
 * being received. It must only be called while processing the \ref
 * RAIL_EVENT_IEEE802154_DATA_REQUEST_COMMAND, and is intended for use
 * when packet information from \ref RAIL_GetRxIncomingPacketInfo()
 * indicates an 802.15.4E Enhanced ACK must be sent instead of a legacy
 * Immediate ACK. \ref RAIL_IEEE802154_ToggleFramePending() should not be
 * called for an Enhanced ACK; instead the Enhanced ACK's Frame Control
 * Field should have the Frame Pending bit set appropriately in its ackData.
 * This will return \ref RAIL_STATUS_INVALID_STATE if it is too late to
 * write the outgoing ACK -- a situation that will likely trigger
 * a \ref RAIL_EVENT_TXACK_UNDERFLOW event. When successful, the Enhanced
 * ackData will only be sent once. Subsequent packets needing an Enhanced
 * ACK will each need to call this function to write their ACK information.
 */
RAIL_Status_t RAIL_IEEE802154_WriteEnhAck(RAIL_Handle_t railHandle,
                                          const uint8_t *ackData,
                                          uint8_t ackDataLen);

/**
 * Convert RSSI into 802.15.4 Link Quality Indication (LQI) metric
 * compatible with the Silicon Labs Zigbee stack.
 *
 * @param[in] origLqi The original LQI, for example from
 *   \ref RAIL_RxPacketDetails_t::lqi.
 *   This parameter is not currently used but may be used in the future.
 * @param[in] rssiDbm The RSSI in dBm, for example from
 *   \ref RAIL_RxPacketDetails_t::rssi.
 * @return An LQI value (range 0..255 but not all intermediate values are
 *   possible) based on the rssiDbm and the chip's RSSI sensitivity range.
 *
 * This function is compatible with \ref RAIL_ConvertLqiCallback_t and
 * is suitable to pass to \ref RAIL_ConvertLqi().
 */
uint8_t RAIL_IEEE802154_ConvertRssiToLqi(uint8_t origLqi, int8_t rssiDbm);

/**
 * Convert RSSI into 802.15.4 Energy Detection (ED) metric
 * compatible with the Silicon Labs Zigbee stack.
 *
 * @param[in] rssiDbm The RSSI in dBm, for example from
 *   \ref RAIL_RxPacketDetails_t::rssi.
 * @return An Energy Detect value (range 0..255 but not all intermediate
 *   values are possible) based on the rssiDbm and the chip's RSSI
 *   sensitivity range.
 */
uint8_t RAIL_IEEE802154_ConvertRssiToEd(int8_t rssiDbm);

/** @} */ // end of IEEE802.15.4

#ifdef __cplusplus
}
#endif

#endif // __RAIL_IEEE802154_H__
