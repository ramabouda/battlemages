const path = require('path')

const HtmlWebpackPlugin = require('html-webpack-plugin')

// import systematic default webpack settings
const webpackDefaults = require('systematic').webpack_get_defaults(__dirname)
const config = require('systematic/js/config')


// [name] will be interpolated by webpack
webpackDefaults.output.filename = '[name]/bundle.[hash].js'

// One entry point per page
webpackDefaults.entry = {
  game: path.join(__dirname, config.build.src_dir, 'pages/game'),
  login: path.join(__dirname, config.build.src_dir, 'pages/login'),
}

webpackDefaults.plugins.push(new HtmlWebpackPlugin({
  filename: 'game/index.html',
  template: 'battlemages/pages/defaultIndex.html',
  chunks: ['game'],
}))
webpackDefaults.plugins.push(new HtmlWebpackPlugin({
  filename: 'login/index.html',
  template: 'battlemages/pages/defaultIndex.html',
  chunks: ['login'],
}))


module.exports = webpackDefaults
