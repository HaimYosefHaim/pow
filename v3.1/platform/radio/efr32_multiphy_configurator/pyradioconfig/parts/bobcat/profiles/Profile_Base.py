from pyradioconfig.parts.ocelot.profiles.Profile_Base import Profile_Base_Ocelot
from pyradioconfig.parts.common.profiles.bobcat_regs import build_modem_regs_bobcat
from pyradioconfig.calculator_model_framework.interfaces.iprofile import IProfile

class Profile_Base_Bobcat(Profile_Base_Ocelot):

    def __init__(self):
        super().__init__()
        self._description = "Profile used for most PHYs"
        self._family = "bobcat"

    def buildRegisterOutputs(self, model, profile, family):
        build_modem_regs_bobcat(model, profile, family)

    def build_hidden_profile_inputs(self, model, profile):
        IProfile.make_hidden_input(profile, model.vars.src1_range_available_minimum, "modem",
                                   readable_name="SRC range minimum", value_limit_min=125, value_limit_max=155)
        IProfile.make_hidden_input(profile, model.vars.input_decimation_filter_allow_dec3, "modem",
                                   readable_name="1=Allow input decimation filter decimate by 3 in cost function",
                                   value_limit_min=0, value_limit_max=1)
        IProfile.make_hidden_input(profile, model.vars.input_decimation_filter_allow_dec8, "modem",
                                   readable_name="1=Allow input decimation filter decimate by 8 in cost function",
                                   value_limit_min=0, value_limit_max=1)
        IProfile.make_hidden_input(profile, model.vars.demod_select, 'Advanced', readable_name="Demod Selection")
        IProfile.make_hidden_input(profile, model.vars.adc_clock_mode, "modem",
                                   readable_name="ADC Clock Mode (XO vs VCO)")
        IProfile.make_hidden_input(profile, model.vars.adc_rate_mode, 'Advanced', readable_name="ADC Rate Mode")
        IProfile.make_hidden_input(profile, model.vars.bcr_demod_en, 'Advanced',
                                   readable_name="Force BCR demod calculation", value_limit_min=0, value_limit_max=1)
        IProfile.make_hidden_input(profile, model.vars.synth_settling_mode, 'modem',
                                   readable_name="Synth Settling Mode")

        IProfile.make_hidden_input(profile, model.vars.fast_detect_enable, 'Advanced',
                                   readable_name="Fast preamble detect enable")
        IProfile.make_hidden_input(profile, model.vars.aox_enable, 'modem', readable_name="Enable AoX")
