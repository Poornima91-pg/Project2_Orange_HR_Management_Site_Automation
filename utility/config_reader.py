from configparser import ConfigParser

# Create a ConfigParser instance to read the configuration file
config = ConfigParser()

# Read the 'config.ini' file from the current project directory
config.read("config.ini")

def get_config(section, key):
    """
     Fetches a specific configuration value from the config.ini file.

     Example:
         get_config('browser_name', 'browser')
         'chrome'
     """

    # Return the specific value from the given section and key
    return config[section][key]
