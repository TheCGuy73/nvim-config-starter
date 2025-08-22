local M = {}

-- Helper function for recursive loading of plugin definitions (from 'effective')
local function recursive_load_plugins_from_dir(base_path, relative_path, plugins_table)
  local full_path = base_path .. "/" .. relative_path
  local files = vim.fn.readdir(full_path)

  if not files then return end

  for _, file in ipairs(files) do
    local current_path = full_path .. "/" .. file
    local file_stat = vim.loop.fs_stat(current_path)

    if file_stat and file_stat.type == "directory" then
      recursive_load_plugins_from_dir(base_path, relative_path .. "/" .. file, plugins_table)
    elseif file:match("%.lua$") then
      local module_name = "user.packages." .. relative_path:gsub("/", ".") .. "." .. file:gsub("%.lua$", "")
      local ok, loaded_plugins = pcall(require, module_name)
      if ok and type(loaded_plugins) == "table" then
        for _, plugin in ipairs(loaded_plugins) do
          table.insert(plugins_table, plugin)
        end
      end
    end
  end
end

-- Helper function for recursive loading of configuration files
local function recursive_load_configs_from_dir(base_path, relative_path)
  local full_path = base_path .. "/" .. relative_path
  local files = vim.fn.readdir(full_path)

  if not files then
    return
  end

  for _, file in ipairs(files) do
    local current_path = full_path .. "/" .. file
    local file_stat = vim.loop.fs_stat(current_path)

    if file_stat and file_stat.type == "directory" then
      recursive_load_configs_from_dir(base_path, relative_path .. "/" .. file)
    elseif file:match("%.lua$") then
      local module_name = "user.packages." .. relative_path:gsub("/", ".") .. "." .. file:gsub("%.lua$", "")
      local ok, _ = pcall(require, module_name)
      if not ok then
        vim.notify("Error loading " .. module_name, vim.log.levels.ERROR)
      end
    end
  end
end



-- This function loads plugin definitions from 'effective'
function M.load_plugins()
  local plugins = {}
  local base_path = vim.fn.stdpath("config") .. "/lua/user/packages"
  recursive_load_plugins_from_dir(base_path, "effective", plugins)
  return plugins
end

-- This function loads editor configurations from 'editor'
function M.load_editor_configs()
  local base_path = vim.fn.stdpath("config") .. "/lua/user/packages"
  recursive_load_configs_from_dir(base_path, "editor")
end

return M