const HtmlWebpackPlugin = require('html-webpack-plugin');

// import type IForkTsCheckerWebpackPlugin from 'fork-ts-checker-webpack-plugin';
// eslint-disable-next-line @typescript-eslint/no-var-requires
// const ForkTsCheckerWebpackPlugin: typeof IForkTsCheckerWebpackPlugin = require('fork-ts-checker-webpack-plugin');

// const path = require('path');
const TsconfigPathsPlugin = require('tsconfig-paths-webpack-plugin');

export const plugins = [
  new HtmlWebpackPlugin({
    template: './src/index.html'
  }),
  new TsconfigPathsPlugin({
    configFile: './tsconfig.json',
  })
];