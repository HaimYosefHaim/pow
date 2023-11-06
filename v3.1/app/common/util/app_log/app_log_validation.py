

ComponentDictionary =  {'SL_IOSTREAM_TYPE_SWO': 'iostream_swo', 
                        'SL_IOSTREAM_TYPE_RTT': 'iostream_rtt', 
                        'SL_IOSTREAM_TYPE_UART': 'iostream_usart', 
                        'SL_IOSTREAM_TYPE_VUART': 'iostream_vuart', 
                    }

def check_type(project, stream_type):
    if stream_type in ComponentDictionary:
        component_name = ComponentDictionary[stream_type]
        if component_name is not None:
            c = project.is_selected(component_name)
            return c
    return False

def get_types(project):
    types  = []
    for stream_type in ComponentDictionary:
        component_name = ComponentDictionary[stream_type]
        if component_name is not None:
            c = project.is_selected(component_name)
            if c:
                types.append(stream_type)
    return types

def check_type_instance(project, stream_type):
    if stream_type in ComponentDictionary:
        component_name = ComponentDictionary[stream_type]
        if component_name is not None:
            if project.is_selected(component_name):
                c = project.component(component_name)
                return c.is_instantiable()
    return False

def get_names(project, stream_type):
    if stream_type in ComponentDictionary:
        component_name = ComponentDictionary[stream_type]
        if component_name is not None:
            if project.is_selected(component_name):
                c = project.component(component_name)
                return c.instances()
    return []

def check_name(project, stream_type, stream_name):
    if stream_name in get_names(project, stream_type):
        return True
    return False

# app_log validation script for checking IO stream validity.
def validate(project):
  override_enabled = project.config("APP_LOG_OVERRIDE_DEFAULT_STREAM")
  if override_enabled is not None:
    if int(override_enabled.value()) == 1:
      stream_type = project.config("APP_LOG_STREAM_TYPE")
      if stream_type is not None:
          valid_type = check_type(project, stream_type.value())
          type_has_instance = check_type_instance(project, stream_type.value());
          valid_name = False
          stream_name = project.config("APP_LOG_STREAM_INSTANCE")
          
          if stream_name is not None:
            stream_name_tr = stream_name.value().replace("\"", "")
            valid_name = check_name(project, stream_type.value(), stream_name_tr)
          component_name = project.component(ComponentDictionary[stream_type.value()]).label()
          if not valid_type:
            types = get_types(project)
            project.error(
                        "IO Stream is not found by type",
                        project.target_for_defines('APP_LOG_STREAM_TYPE'),
                        "Type " +  stream_type.value().replace("SL_IOSTREAM_TYPE_"," ") + " is not present. " 
                            + "Add the '" + component_name + "' ("+ ComponentDictionary[stream_type.value()] + ") component to the project "
                            + "or choose a type from installed ones: [" 
                            + (', '.join(map(str, types) ).replace("SL_IOSTREAM_TYPE_"," ") )  + " ] ",
                         project.quickfix(types)
                    )
          elif type_has_instance and not valid_name:
            names = get_names(project,stream_type.value())
            project.error(
                        "IO Stream is not found by instance name",
                        project.target_for_defines('APP_LOG_STREAM_INSTANCE'),
                        "Instance is not present with type='"+ stream_type.value().replace("SL_IOSTREAM_TYPE_"," ") + "' and name='" 
                            +  stream_name_tr + "'. " 
                            + "Add '" + stream_name_tr + "' instance of '" + component_name + "' component or "
                            + "choose from available instances: [ " + (', '.join(map(str, names) ) ) +" ]",
                        project.quickfix(names)
                        )
            
            