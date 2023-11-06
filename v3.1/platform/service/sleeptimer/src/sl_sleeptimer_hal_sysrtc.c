/***************************************************************************//**
 * @file
 * @brief SLEEPTIMER hardware abstraction implementation for SYSRTC.
 *******************************************************************************
 * # License
 * <b>Copyright 2018 Silicon Laboratories Inc. www.silabs.com</b>
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

#include "peripheral_sysrtc.h"
#include "sl_sleeptimer.h"
#include "sli_sleeptimer_hal.h"
#include "em_core.h"
#include "em_cmu.h"

#if SL_SLEEPTIMER_PERIPHERAL == SL_SLEEPTIMER_PERIPHERAL_SYSRTC

// Minimum difference between current count value and what the comparator of the timer can be set to.
#define SLEEPTIMER_COMPARE_MIN_DIFF  2

#define SLEEPTIMER_TMR_WIDTH (_SYSRTC_CNT_MASK)

static bool cc_disabled = true;

__STATIC_INLINE uint32_t get_time_diff(uint32_t a,
                                       uint32_t b);

/******************************************************************************
 * Initializes SYSRTC sleep timer.
 *****************************************************************************/
void sleeptimer_hal_init_timer(void)
{
  sl_sysrtc_config_t sysrtc_config = SYSRTC_CONFIG_DEFAULT;
  sl_sysrtc_group_config_t group_config = SYSRTC_GROUP_CONFIG_DEFAULT;

  CMU_ClockEnable(cmuClock_SYSRTC, true);

#if (SL_SLEEPTIMER_DEBUGRUN == 1)
  sysrtc_config.enable_debug_run = true;
#endif

  sl_sysrtc_init(&sysrtc_config);

  group_config.compare_channel0_enable = false;
  sl_sysrtc_init_group(0u, &group_config);

  sl_sysrtc_disable_group_interrupts(0u, _SYSRTC_GRP0_IEN_MASK);
  sl_sysrtc_clear_group_interrupts(0u, _SYSRTC_GRP0_IF_MASK);
  sl_sysrtc_enable();
  sl_sysrtc_set_counter(0u);

  NVIC_ClearPendingIRQ(SYSRTC_APP_IRQn);
  NVIC_EnableIRQ(SYSRTC_APP_IRQn);
}

/******************************************************************************
 * Gets SYSRTC counter value.
 *****************************************************************************/
uint32_t sleeptimer_hal_get_counter(void)
{
  return sl_sysrtc_get_counter();
}

/******************************************************************************
 * Gets SYSRTC compare value.
 *****************************************************************************/
uint32_t sleeptimer_hal_get_compare(void)
{
  return sl_sysrtc_get_group_compare_channel_value(0u, 0u);
}

/******************************************************************************
 * Sets SYSRTC compare value.
 *****************************************************************************/
void sleeptimer_hal_set_compare(uint32_t value)
{
  uint32_t counter = sleeptimer_hal_get_counter();
  uint32_t compare = sleeptimer_hal_get_compare();
  uint32_t compare_value = value;
  if (((sl_sysrtc_get_group_interrupts(0u) & SYSRTC_GRP0_IEN_CMP0) != 0)
      || get_time_diff(compare, counter) > SLEEPTIMER_COMPARE_MIN_DIFF
      || compare == counter) {
    // Add margin if necessary
    if (get_time_diff(compare_value, counter) < SLEEPTIMER_COMPARE_MIN_DIFF) {
      compare_value = counter + SLEEPTIMER_COMPARE_MIN_DIFF;
    }
    compare_value %= SLEEPTIMER_TMR_WIDTH;

    sl_sysrtc_set_group_compare_channel_value(0u, 0u, compare_value);
    sleeptimer_hal_enable_int(SLEEPTIMER_EVENT_COMP);
  }

  if (cc_disabled) {
    SYSRTC0->GRP0_CTRL |= SYSRTC_GRP0_CTRL_CMP0EN;
    cc_disabled = false;
  }
}

/******************************************************************************
 * Enables SYSRTC interrupts.
 *****************************************************************************/
void sleeptimer_hal_enable_int(uint8_t local_flag)
{
  uint32_t sysrtc_ien = 0u;

  if (local_flag & SLEEPTIMER_EVENT_OF) {
    sysrtc_ien |= SYSRTC_GRP0_IEN_OVF;
  }

  if (local_flag & SLEEPTIMER_EVENT_COMP) {
    sysrtc_ien |= SYSRTC_GRP0_IEN_CMP0;
  }

  sl_sysrtc_enable_group_interrupts(0u, sysrtc_ien);
}

/******************************************************************************
 * Disables SYSRTC interrupts.
 *****************************************************************************/
void sleeptimer_hal_disable_int(uint8_t local_flag)
{
  uint32_t sysrtc_int_dis = 0u;

  if (local_flag & SLEEPTIMER_EVENT_OF) {
    sysrtc_int_dis |= SYSRTC_GRP0_IEN_OVF;
  }

  if (local_flag & SLEEPTIMER_EVENT_COMP) {
    sysrtc_int_dis |= SYSRTC_GRP0_IEN_CMP0;

    cc_disabled = true;
    SYSRTC0->GRP0_CTRL &= ~_SYSRTC_GRP0_CTRL_CMP0EN_MASK;
  }

  sl_sysrtc_disable_group_interrupts(0u, sysrtc_int_dis);
}

/******************************************************************************
 * Gets status of specified interrupt.
 *
 * Note: This function must be called with interrupts disabled.
 *****************************************************************************/
bool sli_sleeptimer_hal_is_int_status_set(uint8_t local_flag)
{
  bool int_is_set = false;
  uint32_t irq_flag = sl_sysrtc_get_group_interrupts(0u);

  switch (local_flag) {
    case SLEEPTIMER_EVENT_COMP:
      int_is_set = ((irq_flag & SYSRTC_GRP0_IF_CMP0) == SYSRTC_GRP0_IF_CMP0);
      break;

    case SLEEPTIMER_EVENT_OF:
      int_is_set = ((irq_flag & SYSRTC_GRP0_IF_OVF) == SYSRTC_GRP0_IF_OVF);
      break;

    default:
      break;
  }

  return int_is_set;
}

/*******************************************************************************
 * SYSRTC interrupt handler.
 ******************************************************************************/
void SYSRTC_APP_IRQHandler(void)
{
  CORE_DECLARE_IRQ_STATE;
  uint8_t local_flag = 0;
  uint32_t irq_flag;

  CORE_ENTER_ATOMIC();
  irq_flag = sl_sysrtc_get_group_interrupts(0u);

  if (irq_flag & SYSRTC_GRP0_IF_OVF) {
    local_flag |= SLEEPTIMER_EVENT_OF;
  }

  if (irq_flag & SYSRTC_GRP0_IF_CMP0) {
    local_flag |= SLEEPTIMER_EVENT_COMP;
  }
  sl_sysrtc_clear_group_interrupts(0u, irq_flag & (SYSRTC_GRP0_IF_OVF | SYSRTC_GRP0_IF_CMP0));

  process_timer_irq(local_flag);

  CORE_EXIT_ATOMIC();
}

/*******************************************************************************
 * Gets SYSRTC timer frequency.
 ******************************************************************************/
uint32_t sleeptimer_hal_get_timer_frequency(void)
{
  return (CMU_ClockFreqGet(cmuClock_SYSRTC));
}

/*******************************************************************************
 * Computes difference between two times taking into account timer wrap-around.
 *
 * @param a Time.
 * @param b Time to substract from a.
 *
 * @return Time difference.
 ******************************************************************************/
__STATIC_INLINE uint32_t get_time_diff(uint32_t a,
                                       uint32_t b)
{
  return (a - b);
}

#endif
