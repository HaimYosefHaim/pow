/***************************************************************************//**
 * @file
 * @brief Top level application functions
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
#include "tensorflow_lite_micro_microspeech.h"
#include "tensorflow/lite/micro/examples/micro_speech/main_functions.h"
#include "sl_board_control.h"

/***************************************************************************//**
 * Initialize application.
 ******************************************************************************/
void tensorflow_lite_micro_microspeech_init(void)
{
  sl_board_enable_sensor(SL_BOARD_SENSOR_MICROPHONE);
  setup();
}

/***************************************************************************//**
 * Ticking function.
 ******************************************************************************/
void tensorflow_lite_micro_microspeech_process_action(void)
{
  loop();
}
