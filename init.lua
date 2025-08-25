-- Automatically load all lua files in lua/core
local function load_core_config()
  local core_path_glob = vim.fn.stdpath("config") .. "/lua/core/*.lua"
  for _, file_path in ipairs(vim.fn.glob(core_path_glob, true, true)) do
    local module_name = vim.fn.fnamemodify(file_path, ":t"):gsub("%.lua$", "")
    local ok, _ = pcall(require, "core." .. module_name)
    if not ok then
      vim.notify("Error loading core config: " .. module_name, vim.log.levels.ERROR)
    end
  end
end

load_core_config()

require("lazy_bootstrap")
require("lazy_plugins")
