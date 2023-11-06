# simple_rail_rx validation script for RAIL auto state transition and RAIL_ConfigChannel call
def validate(project):
  flex_channel_config = project.config("ENABLE_RAIL_PROPRIETARY_CHANNEL_CONFIGURATION")
  if flex_channel_config is not None:
    if int(flex_channel_config.value()) != 1:
      project.error(
                "ENABLE_RAIL_PROPRIETARY_CHANNEL_CONFIGURATION config shall be set to True",
                "rail_init_config.h",
                "RAIL_ConfigChannels() needs to be called with a generated RAIL config struct"
            )
