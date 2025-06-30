local wezterm = require 'wezterm'

local config = wezterm.config_builder()

if wezterm.target_triple:find("windows") then
  -- Use PowerShell on Windows
  config.default_prog = { "powershell.exe", "-NoLogo" }
else
  -- Use zsh on macOS or Linux
  config.default_prog = { "zsh" }
end

config.font_size = 12
config.color_scheme = 'GruvboxDarkHard'
config.window_background_opacity = 0.8
config.macos_window_background_blur = 30
config.audible_bell = "Disabled"

return config
