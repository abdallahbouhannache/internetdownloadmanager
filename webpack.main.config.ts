import type { Configuration } from "webpack";

const path = require('path');

// import path from "path"
import "webpack-dev-server";

import { rules } from "./webpack.rules";

const mainConfig: Configuration = {
  /**
   * This is the main entry point for your application, it's the first file
   * that runs in the main process.
   */
  entry: "./src/Render/index.ts",
  devtool: "source-map",
  // Put your normal webpack config below here
  module: {
    rules,
  },
  resolve: {
    extensions: [".js", ".ts", ".jsx", ".tsx", ".css", ".scss", ".sass"],
    alias: {
      "@src": path.resolve(__dirname, "./src/*"),
    },
    // alias: {
    //   '@src': path.resolve(__dirname, './src/'),
    // },
  },

  // output: {
  //   path: __dirname + '/src',
  //   filename: 'electron.js'
  // }

  // "port": 3001,
  //     "loggerPort": 9001,
};

export default mainConfig;
