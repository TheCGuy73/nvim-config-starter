local user_plugins = require("user.packages.loader")
require("lazy").setup(user_plugins.load_plugins(), {
  -- your lazy.nvim config goes here
  -- for example, enable auto-install and auto-clean
  install = { colorscheme = { "catppuccin" } },
  checker = { enabled = true }, -- automatically check for plugin updates
  performance = {
    rtp = {
      -- disable some rtp plugins
      disabled_plugins = {
        "gzip",
        "netrwPlugin",
        "tarPlugin",
        "tohtml",
        "tutor",
        "zipPlugin",
      },
    },
  },
    
})