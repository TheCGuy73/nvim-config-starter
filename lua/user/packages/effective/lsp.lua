return {
  {
    "neovim/nvim-lspconfig",
    dependencies = {
      "williamboman/mason.nvim",
      "williamboman/mason-lspconfig.nvim",
      "nvim-treesitter/nvim-treesitter",
    },
    config = function()
      -- Setup mason
      require("mason").setup()
      require("mason-lspconfig").setup({
        ensure_installed = { "nimls", "clangd", "serve_d" },
      })

      -- Setup lspconfig
      local lspconfig = require("lspconfig")
      lspconfig.nimls.setup({})
      lspconfig.clangd.setup({})
      lspconfig.serve_d.setup({})

      -- Setup treesitter
      require("nvim-treesitter.configs").setup({
        ensure_installed = { "nim", "c", "cpp", "d" },
        highlight = { enable = true },
      })
    end,
  },
}