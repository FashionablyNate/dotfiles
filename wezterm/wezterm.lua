local wezterm = require 'wezterm'

local config = wezterm.config_builder()

config.font_size = 12
config.color_scheme = 'Gruvbox (Goph)'
config.window_background_opacity = 0.8
config.macos_window_background_blur = 30
config.audible_bell = "Disabled"

return config
