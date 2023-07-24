const path = require('path');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");


module.exports = {
  mode: 'development',
  entry: './feed/static/feed/main.js',
  output: {
    path: path.resolve(__dirname, 'feed/static/feed'),
    filename: 'bundle.js',
  },
  plugins: [
  new MiniCssExtractPlugin({
    filename: 'styles.css',
  })],
  module: {
  rules: [
    {
      test: /\.(?:js|mjs|cjs)$/,
      exclude: /node_modules/,
      use: {
        loader: 'babel-loader',
        options: {
          presets: [
            ['@babel/preset-env', { targets: "defaults" }]
          ]
        }
      }
    },
    {
      test: /\.css$/i,
      use: [MiniCssExtractPlugin.loader, "css-loader"],
    },
  ]
},
};
