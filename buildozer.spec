[app]
# (str) Title of your application
title = Agri Advisor

# (str) Package name
package.name = agriadvisor

# (str) Package domain (needed for android packaging)
package.domain = org.agri.advisor

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas,db

# (str) Application versioning
version = 1.0.0

# (list) Application requirements
requirements = python3,kivy,sqlite3

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
permissions = INTERNET

# (int) Target Android API
android.api = 33

# (int) Minimum API supported
android.minapi = 21

# (list) Architectures to build for
android.archs = arm64-v8a

# (bool) Enable Android auto backup feature
android.allow_backup = True

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
