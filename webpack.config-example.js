const path = require('path');

module.exports = {
  module: {
    rules: [
      {test: /\.mp3$/,
        loader: 'file-loader'}
    ]
  },
  mode: 'development',
  entry: './static/stopwatchReact.js',

  output: {
    filename: 'main.js',
    path: path.resolve('./static')
  }
};