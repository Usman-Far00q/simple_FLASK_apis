import os
import sys
import config.settings  # we are importing setting.py file solely
# because we want sys.modules to be able to rad from it (because sys.modules --> returns the
# names of the Python modules that have already been IMPORTED)

# create settings object corresponding to specified env
APP_ENV = os.environ.get('APP_ENV', 'Dev')

# ge the attr="<APP-ENV>Config" from the
# config/settings.py (which is basically going to be a
# class because of the way we have written the settings.py file)
_current = getattr(sys.modules['config.settings'], '{0}Config'.format(APP_ENV))()

# # copy attributes to the module for convenience
for atr in [f for f in dir(_current) if not '__' in f]:
    # environment can override anything
    val = os.environ.get(atr)
    if val:
        setattr(_current, atr, val)


my_flask_config_obj = _current


def as_dict():
   res = {}
   for atr in [f for f in dir(config) if not '__' in f]:
       val = getattr(config, atr)
       res[atr] = val
   return res
