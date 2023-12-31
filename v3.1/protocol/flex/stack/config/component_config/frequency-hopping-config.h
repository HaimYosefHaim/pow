/***************************************************************************//**
 * @brief Connect Stack Common component configuration header.
 *
 *******************************************************************************
 * # License
 * <b>Copyright 2019 Silicon Laboratories Inc. www.silabs.com</b>
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

// <<< Use Configuration Wizard in Context Menu >>>

// <h>Connect Stack Frequency Hopping configuration

// <o EMBER_FREQUENCY_HOPPING_SEED> Channel Sequence Generation Seed <0-65536>
// <i> Default: 0
// <i> The frequency hopping channel sequence generation seed.
#define EMBER_FREQUENCY_HOPPING_SEED                                   (0)

// <o EMBER_FREQUENCY_HOPPING_START_CHANNEL> Start Channel <0-99>
// <i> Default: 0
// <i> The lowest channel on the frequency hopping list.
#define EMBER_FREQUENCY_HOPPING_START_CHANNEL                          (0)

// <o EMBER_FREQUENCY_HOPPING_END_CHANNEL> End Channel <0-99>
// <i> Default: 9
// <i> The highest channel on the frequency hopping list.
#define EMBER_FREQUENCY_HOPPING_END_CHANNEL                            (9)

// <o EMBER_FREQUENCY_HOPPING_CHANNEL_DURATION_MS> Channel Duration in milliseconds<200-1000>
// <i> Default: 400
// <i> Time in milliseconds spent on each channel when frequency hopping (channel slot duration).
#define EMBER_FREQUENCY_HOPPING_CHANNEL_DURATION_MS                    (400)

// <o EMBER_FREQUENCY_HOPPING_CHANNEL_GUARD_DURATION_MS> Channel Guard Duration in milliseconds<20-100>
// <i> Default: 20
// <i> Portion of a channel slot in milliseconds during which TX is not allowed (both beginning and end of the channel slot).
#define EMBER_FREQUENCY_HOPPING_CHANNEL_GUARD_DURATION_MS              (20)

// <o EMBER_FREQUENCY_HOPPING_SERVER_FREQ_INFO_BROADCAST_PERIOD_S> Server Broadcast Info Period in seconds<5-1000>
// <i> Default: 15
// <i> Server broadcasts info period in seconds.
#define EMBER_FREQUENCY_HOPPING_SERVER_FREQ_INFO_BROADCAST_PERIOD_S    (15)

// <o EMBER_FREQUENCY_HOPPING_SLEEPY_CLIENT_RESYNC_PERIOD_S> Client Resync Period in seconds<3-3600>
// <i> Default: 60
// <i> Time in seconds after which client triggers an active resync procedure with the server (if needed). Because of clock drifting when the MCU enters EM2 low power mode, only apply to sleepy device
#define EMBER_FREQUENCY_HOPPING_SLEEPY_CLIENT_RESYNC_PERIOD_S          (60)

// <o EMBER_FREQUENCY_HOPPING_ALWAYS_ON_CLIENT_SYNC_TIMEOUT_S> Client synchronization timeout in seconds<10-65535>
// <i> Default: 100
// <i> The maximum duration in seconds without receiving frequency hopping information from the server before considering the hopping server lost. Only apply to non sleepy device. 65535 means no timeout.
#define EMBER_FREQUENCY_HOPPING_ALWAYS_ON_CLIENT_SYNC_TIMEOUT_S        (100)

// <o EMBER_FREQUENCY_HOPPING_SERVER_ADVERTISING_ITERATION_COUNT> Server advertisement sequence count <1-25>
// <i> Default: 3
// <i> Number of iteration over all channels during initial advertisement sequence
#define EMBER_FREQUENCY_HOPPING_SERVER_ADVERTISING_ITERATION_COUNT     (3)

// </h>

// <<< end of configuration section >>>
