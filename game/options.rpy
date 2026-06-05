# game/options.rpy
# Basic Ren'Py project configuration for DemoAVG.

define config.name = "DemoAVG"
define gui.show_name = True

define config.version = "1.0"
define build.name = "DemoAVG"

define config.window_title = "DemoAVG"

define config.has_sound = True
define config.has_music = True
define config.has_voice = False

define config.enter_transition = dissolve
define config.exit_transition = dissolve
define config.intra_transition = dissolve
define config.after_load_transition = None
define config.end_game_transition = None

define config.window = "auto"

define config.save_directory = "DemoAVG-1740000000"

define config.default_fullscreen = False
define config.default_text_cps = 0
define config.default_afm_time = 15

define config.rollback_enabled = True

define config.screen_width = 1280
define config.screen_height = 720
