/***************************************************************************//**
 * @file app_process.c
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

// -----------------------------------------------------------------------------
//                                   Includes
// -----------------------------------------------------------------------------
#include "app_process.h"

// -----------------------------------------------------------------------------
//                              Macros and Typedefs
// -----------------------------------------------------------------------------

// -----------------------------------------------------------------------------
//                          Static Function Declarations
// -----------------------------------------------------------------------------
/***************************************************************************//**
 * Print SE status.
 ******************************************************************************/
static void print_se_status(void);

/***************************************************************************//**
 * Print OTP configuration.
 ******************************************************************************/
static void print_otp_conf(void);

/***************************************************************************//**
 * Print core clock cycle and time.
 ******************************************************************************/
static void print_cycle_time(void);

/***************************************************************************//**
 * Program an application firmware image to main flash.
 ******************************************************************************/
static void prog_main_flash_app(void);

/***************************************************************************//**
 * Program a SE firmware image to main flash.
 ******************************************************************************/
static void prog_main_flash_se(void);

/***************************************************************************//**
 * Program an application firmware image to upgrade SE firmware.
 ******************************************************************************/
static void prog_main_flash_se_app(void);

/***************************************************************************//**
 * Program a signed application firmware image to main flash.
 ******************************************************************************/
static void prog_main_flash_signed(void);

/***************************************************************************//**
 * Erase the user data.
 ******************************************************************************/
static void erase_user_data(void);

/***************************************************************************//**
 * Program the user data.
 ******************************************************************************/
static void prog_user_data(void);

/***************************************************************************//**
 * Print buffer data in ASCII hex.

 * @param buf Pointer to the binary buffer.
 * @param len Number of bytes to print.
 ******************************************************************************/
static void print_buf(uint8_t *buf, size_t len);

// -----------------------------------------------------------------------------
//                                Global Variables
// -----------------------------------------------------------------------------

// -----------------------------------------------------------------------------
//                                Static Variables
// -----------------------------------------------------------------------------
/// Push button 0 status
static bool pb0_press;

/// Push button 1 status
static bool pb1_press;

/// State machine state variable
static state_t app_state = APP_ENTRY;

/// String for example
static uint8_t example_string[] = "Series 2 DCI and SWD Programmer Examples";

/// Interface selection
static uint8_t interface_select;

static const char *interface_string[] = {
  "DEBUG CHALLENGE INTERFACE (DCI)",
  "SERIAL WIRE DEBUG (SWD) INTERFACE"
};

/// Task selection for DCI
static uint8_t dci_task_select;

static const char *dci_task_string[] = {
  "GET SE STATUS",
  "READ SE OTP CONFIGURATION",
  "READ SERIAL NUMBER",
  "READ PUBLIC SIGN KEY",
  "READ PUBLIC COMMAND KEY",
  "ENABLE SECURE DEBUG",
  "DISABLE SECURE DEBUG",
  "LOCK DEVICE",
  "ERASE DEVICE (UNLOCK)",
  "RECOVER SECURE BOOT FAILURE DEVICE",
  "UPGRADE SE FIRMWARE THROUGH DCI",
  "INITIALIZE AES-128 KEY (EFR32xG21)",
  "INITIALIZE PUBLIC SIGN KEY",
  "INITIALIZE PUBLIC COMMAND KEY",
  "INITIALIZE HSE OTP (EFR32xG21A)",
  "INITIALIZE HSE OTP (EFR32xG21B)",
  "INITIALIZE VSE OTP (EFR32xG22)",
  "DISABLE DEVICE ERASE"
};

/// Task selection for SWD interface
static uint8_t swd_task_select;

static const char *swd_task_string[] = {
  "ERASE MAIN FLASH",
  "PROGRAM MAIN FLASH",
  "ERASE USER DATA",
  "PROGRAM USER DATA",
  "UPGRADE SE FIRMWARE THROUGH APPLICATION FIRMWARE"
};

/// Strings for tamper sources
static const char *tamper_source[TAMPER_SIGNAL_NUM] = {
  NULL,
  "Filter counter         : ",
  "SE watchdog            : ",
  NULL,
  "SE RAM CRC             : ",
  "SE hard fault          : ",
  NULL,
  "SE software assertion  : ",
  NULL,
  "User secure boot       : ",
  "Mailbox authorization  : ",
  "DCI authorization      : ",
  "Flash integrity        : ",
  NULL,
  "Self test              : ",
  "TRNG monitor           : ",
  "PRS0                   : ",
  "PRS1                   : ",
  "PRS2                   : ",
  "PRS3                   : ",
  "PRS4                   : ",
  "PRS5                   : ",
  "PRS6                   : ",
  "PRS7                   : ",
  "Decouple BOD           : ",
  "Temperature sensor     : ",
  "Voltage glitch falling : ",
  "Voltage glitch rising  : ",
  "Secure lock            : ",
  "SE debug               : ",
  "Digital glitch         : ",
  "SE ICACHE              : "
};

/// Device unique ID
static uint64_t unique_id;

/// Buffer for device part number
static char device_name[DEV_NAME_SIZE];

/// Buffer for DCI command and response
static uint32_t cmd_resp_buf[CMD_RESP_SIZE];

// -----------------------------------------------------------------------------
//                          Public Function Definitions
// -----------------------------------------------------------------------------

/***************************************************************************//**
 * Application state machine, called infinitely.
 ******************************************************************************/
void app_process_action(void)
{
  switch (app_state) {
    case APP_ENTRY:
      printf("\n%s - Core running at %" PRIu32 " kHz.", example_string,
             CMU_ClockFreqGet(cmuClock_CORE) / 1000);
      printf("\n  . Current interface selection is %s.\n",
             interface_string[interface_select]);
      printf("  + Press PB0 to select an interface (DCI/SWD), "
             "press PB1 to select the task of the selected interface.\n");
      app_state = SELECT_INTERFACE;
      break;

    case SELECT_INTERFACE:
      if (pb0_press) {
        pb0_press = false;
        interface_select++;
        if (interface_select == INTERFACE_NUM) {
          interface_select = 0;
          printf("\n");
        }
        printf("  + Current interface selection is %s.\n",
               interface_string[interface_select]);
      }
      if (pb1_press) {
        pb1_press = false;
        if (interface_select == DCI_SELECT) {
          printf("\n  . Current DCI task is %s.\n",
                 dci_task_string[dci_task_select]);
          printf("  + Press PB0 to select a DCI task, "
                 "press PB1 to run the selected DCI task.\n");
          app_state = SELECT_DCI_TASK;
        } else {
          printf("\n  . Current SWD task is %s.\n",
                 swd_task_string[swd_task_select]);
          printf("  + Press PB0 to select a SWD task, "
                 "press PB1 to run the selected SWD task.\n");
          app_state = SELECT_SWD_TASK;
        }
      }
      break;

    case SELECT_DCI_TASK:
      if (pb0_press) {
        pb0_press = false;
        dci_task_select++;
        if (dci_task_select == DCI_TASK_NUM) {
          dci_task_select = 0;
          printf("\n");
        }
        printf("  + Current DCI task is %s.\n",
               dci_task_string[dci_task_select]);
      }
      if (pb1_press) {
        pb1_press = false;
        if (dci_task_select > CONFIRM_COMMAND) {
          if (dci_task_select > ONE_TIME_COMMAND) {
            printf("  + Warning: This is a ONE-TIME command and the operation "
                   "is IRREVERSIBLE!\n");
          }
          printf("  + Press PB0 to confirm or press PB1 to abort.\n");
          app_state = CONFIRM_SELECTION;
        } else {
          // Set up DCI command buffer
          app_state += (dci_task_select + 1);
          cmd_resp_buf[0] = app_state;
          set_dci_command(cmd_resp_buf);
        }
      }
      break;

    case GET_SE_STATUS:
      printf("\n  . Read target device SE status... ");
      TRY
      connect_to_dci();
      write_dci_command(cmd_resp_buf);
      read_dci_response(cmd_resp_buf);
      print_se_status();
      app_state = APP_ENTRY;
      CATCH
        app_state = APP_ERROR;
      ENDTRY
      break;

    case READ_USER_CONFIG:
      printf("\n  . Read target device user (SE OTP) configuration... ");
      TRY
      connect_to_dci();
      write_dci_command(cmd_resp_buf);
      read_dci_response(cmd_resp_buf);
      print_otp_conf();
      app_state = APP_ENTRY;
      CATCH
        app_state = APP_ERROR;
      ENDTRY
      break;

    case READ_SERIAL_NUMBER:
      printf("\n  . Read target device serial number... ");
      TRY
      connect_to_dci();
      write_dci_command(cmd_resp_buf);
      read_dci_response(cmd_resp_buf);
      printf("OK\n  + The serial number (%d bytes): ", SERIAL_NUM_SIZE);
      print_buf((uint8_t *)&cmd_resp_buf[1], SERIAL_NUM_SIZE);
      app_state = APP_ENTRY;
      CATCH
        app_state = APP_ERROR;
      ENDTRY
      break;

    case READ_PUB_SIGN_KEY:
      printf("\n  . Read target device public sign key... ");
      TRY
      connect_to_dci();
      write_dci_command(cmd_resp_buf);
      read_dci_response(cmd_resp_buf);
      printf("OK\n  + The public sign key (%d bytes): ", PUB_KEY_SIZE);
      print_buf((uint8_t *)&cmd_resp_buf[1], PUB_KEY_SIZE >> 1);
      printf("                                    ");
      print_buf((uint8_t *)&cmd_resp_buf[9], PUB_KEY_SIZE >> 1);
      app_state = APP_ENTRY;
      CATCH
        app_state = APP_ERROR;
      ENDTRY
      break;

    case READ_PUB_CMD_KEY:
      printf("\n  . Read target device public command key... ");
      TRY
      connect_to_dci();
      write_dci_command(cmd_resp_buf);
      read_dci_response(cmd_resp_buf);
      printf("OK\n  + The public command key (%d bytes): ", PUB_KEY_SIZE);
      print_buf((uint8_t *)&cmd_resp_buf[1], PUB_KEY_SIZE >> 1);
      printf("                                       ");
      print_buf((uint8_t *)&cmd_resp_buf[9], PUB_KEY_SIZE >> 1);
      app_state = APP_ENTRY;
      CATCH
        app_state = APP_ERROR;
      ENDTRY
      break;

    case ENABLE_SECURE_DEBUG:
      printf("\n  . Enable secure debug of target device... ");
      TRY
      connect_to_dci();
      write_dci_command(cmd_resp_buf);
      read_dci_response(cmd_resp_buf);
      printf("OK\n");
      app_state = GET_SE_STATUS;
      cmd_resp_buf[0] = app_state;
      set_dci_command(cmd_resp_buf);
      CATCH
        app_state = APP_ERROR;
      ENDTRY
      break;

    case DISABLE_SECURE_DEBUG:
      printf("\n  . Disable secure debug of target device... ");
      TRY
      connect_to_dci();
      write_dci_command(cmd_resp_buf);
      read_dci_response(cmd_resp_buf);
      printf("OK\n");
      app_state = GET_SE_STATUS;
      cmd_resp_buf[0] = app_state;
      set_dci_command(cmd_resp_buf);
      CATCH
        app_state = APP_ERROR;
      ENDTRY
      break;

    case LOCK_DEVICE:
      printf("\n  . Lock target device... ");
      TRY
      connect_to_dci();
      write_dci_command(cmd_resp_buf);
      read_dci_response(cmd_resp_buf);
      printf("OK\n");
      app_state = GET_SE_STATUS;
      cmd_resp_buf[0] = app_state;
      set_dci_command(cmd_resp_buf);
      CATCH
        app_state = APP_ERROR;
      ENDTRY
      break;

    case ERASE_DEVICE:
      printf("\n  . Erase (unlock) target device... ");
      TRY
      connect_to_dci();
      write_dci_command(cmd_resp_buf);
      read_dci_response(cmd_resp_buf);
      printf("OK\n");
      // Reset to recover the debug interface (EFR32xG21)
      hard_reset_target();
      app_state = GET_SE_STATUS;
      cmd_resp_buf[0] = app_state;
      set_dci_command(cmd_resp_buf);
      CATCH
        app_state = APP_ERROR;
      ENDTRY
      break;

    case RECOVER_DEVICE:
      printf("\n  . Issue a device erase through DCI.\n");
      printf("  + Erase target device... ");
      TRY
      connect_to_dci();
      write_dci_command(cmd_resp_buf);
      read_dci_response(cmd_resp_buf);
      printf("OK\n");
      app_state = INIT_SW_DP;
      CATCH
        app_state = APP_ERROR;
      ENDTRY
      break;

    case PROG_SE_FIRMWARE:
      printf("\n  . Program a SE firmware image to target device.\n");
      app_state = INIT_SW_DP;
      break;

    case CHECK_SE_FIRMWARE:
      printf("\n  . Validate SE firmware image in target device... ");
      TRY
      connect_to_dci();
      write_dci_command(cmd_resp_buf);
      read_dci_response(cmd_resp_buf);
      printf("OK\n");
      app_state = APPLY_SE_FIRMWARE;
      cmd_resp_buf[0] = app_state;
      set_dci_command(cmd_resp_buf);
      CATCH
        app_state = APP_ERROR;
      ENDTRY
      break;

    case APPLY_SE_FIRMWARE:
      printf("\n  . Upgrade SE firmware image, delay few seconds "
             "to check SE status... ");
      TRY
      connect_to_dci();
      write_dci_command(cmd_resp_buf);
      // Cannot read response since the target system is restarted
      sl_udelay_wait(SE_UPGRADE_DELAY);
      printf("Done\n");
      app_state = GET_SE_STATUS;
      cmd_resp_buf[0] = app_state;
      set_dci_command(cmd_resp_buf);
      CATCH
        app_state = APP_ERROR;
      ENDTRY
      break;

    case INIT_AES_KEY_XG21:
      printf("\n  . Initialize AES-128 key of target device... ");
      TRY
      connect_to_dci();
      write_dci_command(cmd_resp_buf);
      read_dci_response(cmd_resp_buf);
      printf("OK\n");
      app_state = APP_ENTRY;
      CATCH
        app_state = APP_ERROR;
      ENDTRY
      break;

    case INIT_PUB_SIGN_KEY:
      printf("\n  . Initialize public sign key of target device... ");
      TRY
      connect_to_dci();
      write_dci_command(cmd_resp_buf);
      read_dci_response(cmd_resp_buf);
      printf("OK\n");
      app_state = READ_PUB_SIGN_KEY;
      cmd_resp_buf[0] = app_state;
      set_dci_command(cmd_resp_buf);
      CATCH
        app_state = APP_ERROR;
      ENDTRY
      break;

    case INIT_PUB_CMD_KEY:
      printf("\n  . Initialize public command key of target device... ");
      TRY
      connect_to_dci();
      write_dci_command(cmd_resp_buf);
      read_dci_response(cmd_resp_buf);
      printf("OK\n");
      app_state = READ_PUB_CMD_KEY;
      cmd_resp_buf[0] = app_state;
      set_dci_command(cmd_resp_buf);
      CATCH
        app_state = APP_ERROR;
      ENDTRY
      break;

    case INIT_HSE_OTP_XG21A:
      printf("\n  . Initialize HSE OTP of EFR32xG21A device... ");
      app_state = INIT_OTP_COMMON;
      break;

    case INIT_HSE_OTP_XG21B:
      printf("\n  . Initialize HSE OTP of EFR32xG21B device... ");
      app_state = INIT_OTP_COMMON;
      break;

    case INIT_VSE_OTP_XG22:
      printf("\n  . Initialize VSE OTP of EFR32xG22 device... ");
      app_state = INIT_OTP_COMMON;
      break;

    case INIT_OTP_COMMON:
      TRY
      connect_to_dci();
      write_dci_command(cmd_resp_buf);
      read_dci_response(cmd_resp_buf);
      printf("OK\n");
      // Reset to activate the new OTP settings
      hard_reset_target();
      app_state = READ_USER_CONFIG;
      cmd_resp_buf[0] = app_state;
      set_dci_command(cmd_resp_buf);
      CATCH
        app_state = APP_ERROR;
      ENDTRY
      break;

    case DISABLE_DEVICE_ERASE:
      printf("\n  . Disable device erase of target device... ");
      TRY
      connect_to_dci();
      write_dci_command(cmd_resp_buf);
      read_dci_response(cmd_resp_buf);
      printf("OK\n");
      app_state = GET_SE_STATUS;
      cmd_resp_buf[0] = app_state;
      set_dci_command(cmd_resp_buf);
      CATCH
        app_state = APP_ERROR;
      ENDTRY
      break;

    case CONFIRM_SELECTION:
      if (pb0_press) {
        pb0_press = false;
        if (interface_select == DCI_SELECT) {
          // Set up DCI command buffer
          app_state = SELECT_DCI_TASK;
          app_state += (dci_task_select + 1);
          cmd_resp_buf[0] = app_state;
          set_dci_command(cmd_resp_buf);
        } else {
          printf("\n  . Connect to target device through SWD interface.\n");
          app_state = INIT_SW_DP;
        }
      }
      if (pb1_press) {
        pb1_press = false;
        app_state = APP_ENTRY;
      }
      break;

    case SELECT_SWD_TASK:
      if (pb0_press) {
        pb0_press = false;
        swd_task_select++;
        if (swd_task_select == SWD_TASK_NUM) {
          swd_task_select = 0;
          printf("\n");
        }
        printf("  + Current SWD task is %s.\n",
               swd_task_string[swd_task_select]);
      }
      if (pb1_press) {
        pb1_press = false;
        printf("  + Press PB0 to confirm or press PB1 to abort.\n");
        app_state = CONFIRM_SELECTION;
      }
      break;

    case INIT_SW_DP:
      printf("  + Initialize DP... ");
      TRY
      printf("OK - IDCODE = 0x%.8lX\n", init_dp());
      app_state = GET_AP_ID;
      CATCH
        app_state = APP_ERROR;
      ENDTRY
      break;

    case GET_AP_ID:
      printf("  + Read AP... ");
      TRY
      printf("OK - IDR = 0x%.8lX\n", read_ap_id());
      app_state = HALT_TARGET;
      CATCH
        app_state = APP_ERROR;
      ENDTRY
      break;

    case HALT_TARGET:
      printf("  + Set up AHB-AP and halt target... ");
      TRY
      init_ahb_ap();
      halt_target();
      printf("OK\n");
      app_state = GET_DEVICE_INFO;
      CATCH
        app_state = APP_ERROR;
      ENDTRY
      break;

    case GET_DEVICE_INFO:
      printf("  + Get device information... ");
      TRY
      get_device_info(device_name, &unique_id);
      printf("OK - Target device is %s and unique ID is 0x%.8lX%.8lX\n",
             device_name, (uint32_t)(unique_id >> 32), (uint32_t)unique_id);
      if (interface_select == DCI_SELECT) {
        if (dci_task_select == RECOVER_SELECT) {
          // Recover device
          app_state = PROG_MAIN_FLASH_SIGNED;
        } else {
          // SE firmware upgrade
          app_state = PROG_MAIN_FLASH_SE;
        }
      } else {
        app_state = SELECT_SWD_TASK;
        app_state += (swd_task_select + 1);
      }
      CATCH
        app_state = APP_ERROR;
      ENDTRY
      break;

    case ERASE_MAIN_FLASH:
      printf("\n  . Erase main flash of target device... ");
      TRY
        cmd_resp_buf[0] = erase_flash(false);
      print_cycle_time();
      app_state = APP_ENTRY;
      CATCH
        app_state = APP_ERROR;
      ENDTRY
      break;

    case PROG_MAIN_FLASH_APP:
      printf("\n  . Program an application firmware image to target device.\n");
      TRY
      prog_main_flash_app();
      printf("  + Issue a soft reset to run the application firmware... ");
      soft_reset_target();
      printf("OK\n");
      app_state = APP_ENTRY;
      CATCH
        app_state = APP_ERROR;
      ENDTRY
      break;

    case PROG_MAIN_FLASH_SE:
      TRY
      prog_main_flash_se();
      if (interface_select == DCI_SELECT) {
        // Upgrade SE firmware through DCI
        app_state = CHECK_SE_FIRMWARE;
      } else {
        // Upgrade SE firmware through application
        printf("  + Issue a pin reset to run the application to upgrade the "
               "SE firmware.\n");
        printf("  + Delay few seconds to check SE status... ");
        hard_reset_target();
        sl_udelay_wait(SE_UPGRADE_DELAY);
        printf("Done\n");
        app_state = GET_SE_STATUS;
      }
      cmd_resp_buf[0] = app_state;
      set_dci_command(cmd_resp_buf);
      CATCH
        app_state = APP_ERROR;
      ENDTRY
      break;

    case PROG_MAIN_FLASH_SE_APP:
      // Program application should run first since it may erase the whole flash
      printf("\n  . Program an application firmware image to target device "
             "to upgrade the SE firmware.\n");
      TRY
      prog_main_flash_se_app();
      printf("\n  . Program a SE firmware image to target device.\n");
      app_state = PROG_MAIN_FLASH_SE;
      CATCH
        app_state = APP_ERROR;
      ENDTRY
      break;

    case PROG_MAIN_FLASH_SIGNED:
      printf("\n  . Program a correctly-signed image to recover device.\n");
      TRY
      prog_main_flash_signed();
      // Reset to recover the debug interface (EFR32xG21)
      hard_reset_target();
      app_state = GET_SE_STATUS;
      cmd_resp_buf[0] = app_state;
      set_dci_command(cmd_resp_buf);
      CATCH
        app_state = APP_ERROR;
      ENDTRY
      break;

    case ERASE_USER_DATA:
      TRY
      erase_user_data();
      app_state = APP_ENTRY;
      CATCH
        app_state = APP_ERROR;
      ENDTRY
      break;

    case PROG_USER_DATA:
      TRY
      prog_user_data();
      app_state = APP_ENTRY;
      CATCH
        app_state = APP_ERROR;
      ENDTRY
      break;

    case APP_ERROR:
      printf("Failed - %s\n", get_error_string(error_code));
      printf("  + Press PB0 to issue a pin reset to the target, press PB1 to "
             "skip.\n");
      app_state = APP_EXIT;
      break;

    case APP_EXIT:
      if (pb0_press) {
        pb0_press = false;
        printf("  + Issue a pin reset to the target.\n");
        hard_reset_target();
        app_state = APP_ENTRY;
      }
      if (pb1_press) {
        pb1_press = false;
        app_state = APP_ENTRY;
      }
      break;

    default:
      break;
  }
}

/***************************************************************************//**
 * Button callback, called if any button is pressed or released.
 ******************************************************************************/
void sl_button_on_change(const sl_button_t *handle)
{
  // Check if any button was pressed
  if (sl_button_get_state(handle) == SL_SIMPLE_BUTTON_PRESSED) {
    if (&sl_button_btn0 == handle) {
      pb0_press = true;
    }
    if (&sl_button_btn1 == handle) {
      pb1_press = true;
    }
  }
}

// -----------------------------------------------------------------------------
//                          Static Function Definitions
// -----------------------------------------------------------------------------
/***************************************************************************//**
 * Print SE status.
 ******************************************************************************/
static void print_se_status(void)
{
  uint32_t index;
  uint32_t boot_status;
  bool boot_error = false;

  // Check response from EFR32xG21 or EFR32xG22
  if (cmd_resp_buf[0] == RESP_WITH_TAMPER) {
    index = 5;
  } else {
    index = 1;
  }

  // Save boot status
  boot_status = cmd_resp_buf[index++];

  // Boot status error code is available if SE firmware >= V1.2.0
  cmd_resp_buf[index] &= SE_VER_MASK;
  if (cmd_resp_buf[index] >= SE_BOOT_ERR_VER) {
    boot_error = true;
  }
  printf("OK\n");
  printf("  + SE firmware version  : %08lX\n",
         cmd_resp_buf[index++]);

  if (cmd_resp_buf[index] != NO_MCU_VER) {
    printf("  + MCU firmware version : %08lX\n",
           cmd_resp_buf[index]);
  } else {
    printf("  + MCU firmware version : NA\n");
  }

  index++;
  printf("  + Debug lock           : ");
  if (cmd_resp_buf[index] & DEBUG_LOCK_MASK) {
    printf("Enabled\n");
  } else {
    printf("Disabled\n");
  }

  printf("  + Debug lock state     : ");
  if (cmd_resp_buf[index] & DEBUG_LOCK_STATE_MASK) {
    printf("True\n");
  } else {
    printf("False\n");
  }

  printf("  + Device Erase         : ");
  if (cmd_resp_buf[index] & DEVICE_ERASE_MASK) {
    printf("Enabled\n");
  } else {
    printf("Disabled\n");
  }

  printf("  + Secure debug         : ");
  if (cmd_resp_buf[index] & SECURE_DEBUG_MASK) {
    printf("Enabled\n");
  } else {
    printf("Disabled\n");
  }

  index++;
  printf("  + Secure boot          : ");
  if (cmd_resp_buf[index] == SECURE_BOOT_NOT_CONF) {
    printf("Disabled and SE OTP is not configured\n");
  } else {
    if (cmd_resp_buf[index] & SECURE_BOOT_MASK) {
      printf("Enabled\n");
    } else {
      printf("Disabled\n");
    }
  }

  // Get boot status error code
  if (boot_error) {
    boot_status = ((boot_status & ERROR_CODE_MASK) >> ERROR_CODE_SHIFT) + DCI_RESPONSE_OK;
    printf("  + Boot status          : %s\n",
           get_error_string(boot_status));
  } else {
    if ((boot_status & BOOT_STATUS_MASK) != BOOT_MAIN_LOOP) {
      printf("  + Boot status          : Failed\n");
    } else {
      printf("  + Boot status          : OK\n");
    }
  }
}

/***************************************************************************//**
 * Print OTP configuration.
 ******************************************************************************/
static void print_otp_conf(void)
{
  uint32_t i;
  uint32_t j;
  uint32_t k;

  printf("OK\n");
  printf("  + Secure boot                    : ");
  if (cmd_resp_buf[1] & SECURE_BOOT_ENABLE_MASK) {
    printf("Enabled\n");
  } else {
    printf("Disabled\n");
  }

  printf("  + Secure boot verify certificate : ");
  if (cmd_resp_buf[1] & SECURE_BOOT_CERT_MASK) {
    printf("Enabled\n");
  } else {
    printf("Disabled\n");
  }

  printf("  + Secure boot anti-rollback      : ");
  if (cmd_resp_buf[1] & ANTI_ROLLBACK_MASK) {
    printf("Enabled\n");
  } else {
    printf("Disabled\n");
  }

  printf("  + Secure boot page lock narrow   : ");
  if (cmd_resp_buf[1] & PAGE_LOCK_NARROW_MASK) {
    printf("Enabled\n");
  } else {
    printf("Disabled\n");
  }

  printf("  + Secure boot page lock full     : ");
  if (cmd_resp_buf[1] & PAGE_LOCK_FULL_MASK) {
    printf("Enabled\n");
  } else {
    printf("Disabled\n");
  }

  // Tamper configuration for secure vault device
  if (cmd_resp_buf[0] == RESP_TAMPER_CONF) {
    printf("  + Tamper source level (valid on Secure Vault device)\n");
    for (i = 0, j = 0, k = 2; i < TAMPER_SIGNAL_NUM; i++, j += 4) {
      if (j == 32) {
        j = 0;
        k++;
      }
      cmd_resp_buf[8] = (cmd_resp_buf[k] >> j) & 0x0f;
      if (tamper_source[i] != NULL) {
        printf("    %s %lu\n", tamper_source[i], cmd_resp_buf[8]);
      }
    }

    printf("  + Reset period for the tamper filter counter: ~32 ms x %u\n",
           1 << (cmd_resp_buf[6] & COUNTER_PERIOD_MASK));
    printf("  + Activation threshold for the tamper filter: %d\n",
           256 / (1 << ((cmd_resp_buf[6] & COUNTER_THRESHOLD_MASK) >> COUNTER_THRESHOLD_SHIFT)));
    if (cmd_resp_buf[6] & GLITCH_DETECTOR_MASK) {
      printf("  + Digital glitch detector always on: Enabled\n");
    } else {
      printf("  + Digital glitch detector always on: Disabled\n");
    }
    printf("  + Tamper reset threshold: %lu\n", cmd_resp_buf[6] >> TAMPER_RESET_SHIFT);
  }
}

/***************************************************************************//**
 * Print core clock cycle and time.
 ******************************************************************************/
static void print_cycle_time(void)
{
  // Core clock cycle in cmd_resp_buf[0]
  if (cmd_resp_buf[0] < 1000000) {
    printf("OK (cycles: %" PRIu32 " time: %" PRIu32 " us)\n",
           cmd_resp_buf[0],
           (cmd_resp_buf[0] * 10) / (CMU_ClockFreqGet(cmuClock_CORE) / 100000));
  } else {
    printf("OK (cycles: %" PRIu32 " time: %" PRIu32 " ms)\n",
           cmd_resp_buf[0],
           cmd_resp_buf[0] / (CMU_ClockFreqGet(cmuClock_CORE) / 1000));
  }
}

/***************************************************************************//**
 * Program an application firmware image to main flash.
 ******************************************************************************/
static void prog_main_flash_app(void)
{
  switch (device_name[DEVICE_INDEX]) {
    case DEVICE_XG21:
      printf("  + EFR32xG21 application firmware image size is %lu bytes "
             "and start address is 0x%08lX.\n", get_xg21_app_size(),
             APP_START_ADDR);
      printf("  + Erase-Program-Verify the EFR32xG21 main flash for "
             "application firmware image... ");
      cmd_resp_buf[0] = prog_flash(APP_START_ADDR,
                                   get_xg21_app_size(),
                                   (uint32_t *)get_xg21_app_addr());
      print_cycle_time();
      break;

    case DEVICE_XG22:
      printf("\n  . EFR32xG22 application firmware image size is %lu bytes "
             "and start address is 0x%08lX.\n", get_xg22_add_size(),
             APP_START_ADDR);
      printf("  + Erase-Program-Verify the EFR32xG22 main flash for "
             "application firmware image... ");
      cmd_resp_buf[0] = prog_flash(APP_START_ADDR,
                                   get_xg22_add_size(),
                                   (uint32_t *)get_xg22_app_addr());
      print_cycle_time();
      break;

    default:
      RAISE(SWD_ERROR_UNKNOWN_DEVICE);
      break;
  }
}

/***************************************************************************//**
 * Program a SE firmware image to main flash.
 ******************************************************************************/
static void prog_main_flash_se(void)
{
  switch (device_name[DEVICE_INDEX]) {
    case DEVICE_XG21:
      printf("  + EFR32xG21 HSE firmware image version: %08lX\n",
             *((uint32_t *)get_xg21_hse_addr() + 3));
      printf("  + EFR32xG21 HSE firmware image size is %lu bytes and start "
             "address is 0x%08lX.\n", get_xg21_hse_size(), SE_START_ADDR);
      printf("  + Erase-Program-Verify the EFR32xG21 main flash for HSE "
             "firmware image... ");
      cmd_resp_buf[0] = prog_flash(SE_START_ADDR,
                                   get_xg21_hse_size(),
                                   (uint32_t *)get_xg21_hse_addr());
      print_cycle_time();
      break;

    case DEVICE_XG22:
      printf("  + EFR32xG22 VSE image version: %08lX\n",
             *((uint32_t *)get_xg22_vse_addr() + 3));
      printf("  + EFR32xG22 VSE firmware image size is %lu bytes and start "
             "address is 0x%08lX.\n", get_xg22_vse_size(), SE_START_ADDR);
      printf("  + Erase-Program-Verify the EFR32xG22 main flash for VSE "
             "firmware image... ");
      cmd_resp_buf[0] = prog_flash(SE_START_ADDR,
                                   get_xg22_vse_size(),
                                   (uint32_t *)get_xg22_vse_addr());
      print_cycle_time();
      break;

    default:
      RAISE(SWD_ERROR_UNKNOWN_DEVICE);
      break;
  }
}

/***************************************************************************//**
 * Program an application firmware image to upgrade SE firmware.
 ******************************************************************************/
static void prog_main_flash_se_app(void)
{
  switch (device_name[DEVICE_INDEX]) {
    case DEVICE_XG21:
      printf("  + EFR32xG21 HSE upgrade application firmware image size is "
             "%lu bytes and start address is 0x%08lX.\n",
             get_xg21_hse_upgrade_app_size(), APP_START_ADDR);
      printf("  + Erase-Program-Verify the EFR32xG21 main flash for "
             "application to upgrade \n");
      printf("    HSE firmware... ");
      cmd_resp_buf[0] = prog_flash(APP_START_ADDR,
                                   get_xg21_hse_upgrade_app_size(),
                                   (uint32_t *)get_xg21_hse_upgrade_app_addr());
      print_cycle_time();
      break;

    case DEVICE_XG22:
      printf("  + EFR32xG22 VSE upgrade application firmware image size is "
             "%lu bytes and start address is 0x%08lX.\n",
             get_xg22_vse_upgrade_app_size(), APP_START_ADDR);
      printf("  + Erase-Program-Verify the EFR32xG21 main flash for "
             "application to upgrade \n");
      printf("    VSE firmware... ");
      cmd_resp_buf[0] = prog_flash(APP_START_ADDR,
                                   get_xg22_vse_upgrade_app_size(),
                                   (uint32_t *)get_xg22_vse_upgrade_app_addr());
      print_cycle_time();
      break;

    default:
      RAISE(SWD_ERROR_UNKNOWN_DEVICE);
      break;
  }
}

/***************************************************************************//**
 * Program a signed application firmware image to main flash.
 ******************************************************************************/
static void prog_main_flash_signed(void)
{
  switch (device_name[DEVICE_INDEX]) {
    case DEVICE_XG21:
      printf("  + EFR32xG21 signed firmware image size is %lu bytes "
             "and start address is 0x%08lX.\n",
             get_xg21_signed_size(),
             APP_START_ADDR);
      printf("  + Erase-Program-Verify the EFR32xG21 main flash for "
             "signed firmware image... ");
      cmd_resp_buf[0] = prog_flash(APP_START_ADDR,
                                   get_xg21_signed_size(),
                                   (uint32_t *)get_xg21_signed_addr());
      print_cycle_time();
      break;

    case DEVICE_XG22:
      printf("  + EFR32xG22 signed firmware image size is %lu bytes "
             "and start address is 0x%08lX.\n",
             get_xg22_signed_size(),
             APP_START_ADDR);
      printf("  + Erase-Program-Verify the EFR32xG22 main flash for "
             "signed firmware image... ");
      cmd_resp_buf[0] = prog_flash(APP_START_ADDR,
                                   get_xg22_signed_size(),
                                   (uint32_t *)get_xg22_signed_addr());
      print_cycle_time();
      break;

    default:
      RAISE(SWD_ERROR_UNKNOWN_DEVICE);
      break;
  }
}

/***************************************************************************//**
 * Erase the user data.
 ******************************************************************************/
static void erase_user_data(void)
{
  switch (device_name[DEVICE_INDEX]) {
    case DEVICE_XG21:
      printf("\n  . Erase EFR32xG21 user data through application "
             "firmware.\n");
      printf("  + EFR32xG21 application firmware image size is %lu bytes "
             "and start address is 0x%08lX.\n",
             get_xg21_userdata_erase_app_size(),
             APP_START_ADDR);
      printf("  + Erase-Program-Verify the EFR32xG21 main flash for "
             "application firmware image... ");
      cmd_resp_buf[0] = prog_flash(APP_START_ADDR,
                                   get_xg21_userdata_erase_app_size(),
                                   (uint32_t *)get_xg21_userdata_erase_app_addr());
      print_cycle_time();
      printf("  + Issue a soft reset to run the application firmware to erase "
             "the EFR32xG21 user data... ");
      soft_reset_target();
      sl_udelay_wait(USER_DATA_DELAY);
      verify_user_data(NULL);
      printf("OK\n");
      break;

    case DEVICE_XG22:
      printf("\n  . Erase EFR32xG22 user data... ");
      cmd_resp_buf[0] = erase_flash(true);
      print_cycle_time();
      break;

    default:
      RAISE(SWD_ERROR_UNKNOWN_DEVICE);
      break;
  }
}

/***************************************************************************//**
 * Program the user data.
 ******************************************************************************/
static void prog_user_data(void)
{
  switch (device_name[DEVICE_INDEX]) {
    case DEVICE_XG21:
      printf("\n  . Program EFR32xG21 user data through application "
             "firmware.\n");
      printf("  + EFR32xG21 application firmware image size is %lu bytes "
             "and start address is 0x%08lX.\n",
             get_xg21_userdata_write_app_size(),
             APP_START_ADDR);
      printf("  + Erase-Program-Verify the EFR32xG21 main flash for "
             "application firmware image... ");
      cmd_resp_buf[0] = prog_flash(APP_START_ADDR,
                                   get_xg21_userdata_write_app_size(),
                                   (uint32_t *)get_xg21_userdata_write_app_addr());
      print_cycle_time();
      printf("  + Issue a soft reset to run the application firmware to "
             "program the EFR32xG21 user data... ");
      soft_reset_target();
      sl_udelay_wait(USER_DATA_DELAY);
      verify_user_data((uint32_t *)get_userdata_addr());
      printf("OK\n");
      break;

    case DEVICE_XG22:
      printf("\n  . Program EFR32xG22 user data.\n");
      printf("  + User data size is %lu bytes and start address is 0x%08lX.\n",
             get_userdata_size(), USER_DATA_ADDR);
      printf("  + Erase-Program-Verify the EFR32xG22 user data... ");
      cmd_resp_buf[0] = prog_flash(USER_DATA_ADDR,
                                   get_userdata_size(),
                                   (uint32_t *)get_userdata_addr());
      print_cycle_time();
      break;

    default:
      RAISE(SWD_ERROR_UNKNOWN_DEVICE);
      break;
  }
}

/***************************************************************************//**
 * Print buffer data in ASCII hex.
 ******************************************************************************/
static void print_buf(uint8_t *buf, size_t len)
{
  uint32_t i;
  uint8_t hex_array[16] = "0123456789ABCDEF";

  for (i = 0; i < len; i++) {
    printf("%c", hex_array[(buf[i] >> 4) & 0x0f]);
    printf("%c", hex_array[buf[i] & 0x0f]);
  }
  printf("\n");
}
