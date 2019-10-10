const {
  override,
  overrideDevServer
} = require("customize-cra");

module.exports = {
  webpack: override(
    (config) => {
      config.optimization = config.optimization || {};
      config.optimization.splitChunks = {
         cacheGroups: {
            default: false
         }
      };
      config.optimization.runtimeChunk = false;

      config.output = config.output || {};
      config.output.filename = 'bundle.js';

      return config;
    }
  ),
  devServer: overrideDevServer(
    (config) => {
      config.proxy = {
        '/auth': {
          target: 'http://localhost:5000'
        },
        '/api': {
          target: 'http://localhost:5000',
          changeOrigin: true
        }
      };

      config.contentBase = __dirname + '/../server/src/static';

      return config;
    }
  )
};
