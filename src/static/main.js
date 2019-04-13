/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = "./static/stopwatchReact.js");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./static/clockComponent.js":
/*!**********************************!*\
  !*** ./static/clockComponent.js ***!
  \**********************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\nclass Clock extends React.Component {\n  constructor(props) {\n    super(props);\n    this.state = {\n      date: new Date()\n    };\n  }\n\n  componentDidMount() {\n    this.timerID = setInterval(() => this.tick(), 1000);\n  }\n\n  componentWillUnmount() {\n    clearInterval(this.timerID);\n  }\n\n  tick() {\n    this.setState({\n      date: new Date()\n    });\n  }\n\n  render() {\n    return React.createElement(\"h2\", null, \" \", this.state.date.toLocaleTimeString(), \" \");\n  }\n\n}\n\n/* harmony default export */ __webpack_exports__[\"default\"] = (Clock);\n//# sourceMappingURL=clockComponent.js.map\n\n//# sourceURL=webpack:///./static/clockComponent.js?");

/***/ }),

/***/ "./static/helperFunctions.js":
/*!***********************************!*\
  !*** ./static/helperFunctions.js ***!
  \***********************************/
/*! exports provided: millisecondConversion, timeStringMillisecondConversion */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"millisecondConversion\", function() { return millisecondConversion; });\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"timeStringMillisecondConversion\", function() { return timeStringMillisecondConversion; });\nfunction millisecondConversion(timeDelta = 0) {\n  {\n    /*Takes milliseconds and converts it into ms, s, m, h in human readable and rounded values along with a string of them stitched together.*/\n  }\n  let timeObject = {};\n\n  if (timeDelta < 0) {\n    throw new RangeError('Negative Time Supplied');\n  }\n\n  timeObject.millisecond = Math.floor(timeDelta % 1000).toString().padStart(3, '0');\n  timeDelta /= 1000;\n  timeObject.seconds = Math.floor(timeDelta % 60).toString().padStart(2, '0');\n  timeDelta /= 60;\n  timeObject.minutes = Math.floor(timeDelta % 60).toString().padStart(2, '0');\n  timeDelta /= 60;\n  timeObject.hours = Math.floor(timeDelta % 24).toString().padStart(2, '0');\n  timeObject.timeString = timeObject.hours + ':' + timeObject.minutes + ':' + timeObject.seconds + ':' + timeObject.millisecond;\n  return timeObject;\n}\nfunction timeStringMillisecondConversion(timeDelta = \"000000\") {\n  /*a quick test*/\n  if (typeof timeDelta !== 'string') {\n    throw new TypeError('timeDelta must be a string! Did you mean to use milliSecondConversion?');\n  }\n\n  if (timeDelta.length !== 6) {\n    throw new RangeError('String must have 6 characters');\n  }\n\n  let hours = Math.floor(parseInt(timeDelta.slice(0, 2)));\n  let min = Math.floor(parseInt(timeDelta.slice(2, 4)));\n  let sec = Math.floor(parseInt(timeDelta.slice(4)));\n  /*Dimensional analysis to convert and sum human readable time-string to milliseconds*/\n\n  let milliseconds = ((hours * 60 + min) * 60 + sec) * 1000;\n  return milliseconds;\n}\n//# sourceMappingURL=helperFunctions.js.map\n\n//# sourceURL=webpack:///./static/helperFunctions.js?");

/***/ }),

/***/ "./static/stopwatchComponent.js":
/*!**************************************!*\
  !*** ./static/stopwatchComponent.js ***!
  \**************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _helperFunctions__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./helperFunctions */ \"./static/helperFunctions.js\");\n\nlet Button = mui.react.Button;\n\nclass Stopwatch extends React.Component {\n  constructor(props) {\n    super(props);\n    this.state = {\n      date: Date.now(),\n      timeDelta: 0,\n      timeDiff: 0,\n      timeString: '00:00:00:000',\n      running: false\n    };\n    this.startPauseWatch = this.startPauseWatch.bind(this);\n    this.clearWatch = this.clearWatch.bind(this);\n  }\n\n  componentWillUnmount() {\n    clearInterval(this.timerID);\n  }\n\n  tick() {\n    let timeDelta = Date.now() - this.state.date;\n    let timeDiff = this.state.timeDiff + timeDelta;\n    let timeObject = Object(_helperFunctions__WEBPACK_IMPORTED_MODULE_0__[\"millisecondConversion\"])(timeDiff);\n    this.setState({\n      timeDelta: timeDelta,\n      timeString: timeObject.timeString\n    });\n  }\n\n  startPauseWatch() {\n    let running = !this.state.running;\n    let counter = this.state.timeDelta + this.state.timeDiff;\n    {\n      /*directly using state gives flipped results from test.\r\n          React will read the prior state, not the flipped one so this side-steps\r\n          the problem by creating a var of the flipped state*/\n    }\n    this.setState({\n      running: running,\n      date: Date.now()\n    });\n\n    if (running !== true) {\n      this.setState({\n        timeDiff: counter\n      });\n      clearInterval(this.timerID);\n    }\n\n    if (running) {\n      this.timerID = setInterval(() => this.tick(), 10);\n    }\n  }\n\n  clearWatch() {\n    this.setState({\n      date: Date.now(),\n      timeDelta: 0,\n      timeDiff: 0,\n      timeString: '00:00:00:000',\n      running: false\n    });\n    clearInterval(this.timerID);\n  }\n\n  render() {\n    return React.createElement(\"div\", null, React.createElement(\"h2\", {\n      \"data-cy\": \"stopwatchTimeString\"\n    }, \" \", this.state.timeString), React.createElement(Button, {\n      variant: \"raised\",\n      color: \"primary\",\n      \"data-cy\": \"startPauseCounterButton\",\n      onClick: this.startPauseWatch\n    }, this.state.running ? 'Pause' : 'Start'), React.createElement(Button, {\n      variant: \"raised\",\n      color: \"primary\",\n      \"data-cy\": \"clearCounterButton\",\n      onClick: this.clearWatch\n    }, \"Clears\"));\n  }\n\n}\n\n/* harmony default export */ __webpack_exports__[\"default\"] = (Stopwatch);\n//# sourceMappingURL=stopwatchComponent.js.map\n\n//# sourceURL=webpack:///./static/stopwatchComponent.js?");

/***/ }),

/***/ "./static/stopwatchReact.js":
/*!**********************************!*\
  !*** ./static/stopwatchReact.js ***!
  \**********************************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _clockComponent__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./clockComponent */ \"./static/clockComponent.js\");\n/* harmony import */ var _stopwatchComponent__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./stopwatchComponent */ \"./static/stopwatchComponent.js\");\n/* harmony import */ var _timerComponent__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./timerComponent */ \"./static/timerComponent.js\");\n\n\n\nlet Button = mui.react.Button;\nlet Container = mui.react.Container;\n\nfunction Toggle(props) {\n  if (props.componentSelection === 'Clock') {\n    return React.createElement(_clockComponent__WEBPACK_IMPORTED_MODULE_0__[\"default\"], null);\n  }\n\n  if (props.componentSelection === 'Stopwatch') {\n    return React.createElement(_stopwatchComponent__WEBPACK_IMPORTED_MODULE_1__[\"default\"], null);\n  }\n\n  if (props.componentSelection === 'Timer') {\n    return React.createElement(_timerComponent__WEBPACK_IMPORTED_MODULE_2__[\"default\"], null);\n  }\n}\n\nclass App extends React.Component {\n  constructor(props) {\n    super(props);\n    this.state = {\n      currentTime: 0,\n      componentSelection: 'Timer'\n    };\n    this.handleClick = this.handleClick.bind(this);\n  }\n\n  handleClick(event) {\n    this.setState({\n      componentSelection: event.target.value\n    });\n  }\n\n  render() {\n    return React.createElement(\"div\", {\n      className: \"mui--text-center\"\n    }, React.createElement(Container, {\n      fluid: true\n    }, React.createElement(Toggle, {\n      componentSelection: this.state.componentSelection\n    }), React.createElement(\"br\", null), this.state.componentSelection !== 'Clock' && React.createElement(Button, {\n      variant: \"raised\",\n      color: \"primary\",\n      value: \"Clock\",\n      \"data-cy\": \"clockToggleButton\",\n      onClick: this.handleClick\n    }, \"Clock\"), this.state.componentSelection !== 'Stopwatch' && React.createElement(Button, {\n      variant: \"raised\",\n      color: \"primary\",\n      value: \"Stopwatch\",\n      \"data-cy\": \"stopwatchToggleButton\",\n      onClick: this.handleClick\n    }, \"Stopwatch\"), this.state.componentSelection !== 'Timer' && React.createElement(Button, {\n      variant: \"raised\",\n      color: \"primary\",\n      value: \"Timer\",\n      \"data-cy\": \"timerToggleButton\",\n      onClick: this.handleClick\n    }, \"Timer\")));\n  }\n\n}\n\nReactDOM.render(React.createElement(App, null), document.getElementById('root'));\n//# sourceMappingURL=stopwatchReact.js.map\n\n//# sourceURL=webpack:///./static/stopwatchReact.js?");

/***/ }),

/***/ "./static/timerComponent.js":
/*!**********************************!*\
  !*** ./static/timerComponent.js ***!
  \**********************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _helperFunctions__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./helperFunctions */ \"./static/helperFunctions.js\");\n\nlet Button = mui.react.Button;\nlet Container = mui.react.Container;\n\nclass Timer extends React.Component {\n  constructor(props) {\n    super(props);\n    this.state = {\n      running: false,\n      input: false,\n      timerLength: 0,\n      timerRemaining: 0,\n      timerString: '00:00:00:000'\n    };\n    this.startPauseTimer = this.startPauseTimer.bind(this);\n    this.clearTimer = this.clearTimer.bind(this);\n    this.setTimer = this.setTimer.bind(this);\n  }\n\n  startPauseTimer() {\n    let running = !this.state.running;\n    this.setState({\n      running: running\n    });\n\n    if (running) {\n      this.endTime = this.state.timerRemaining === 0 ? Date.now() + this.state.timerLength : Date.now() + this.state.timerRemaining;\n      this.timerID = setInterval(() => this.tick(), 10);\n    }\n\n    if (!running) {\n      clearInterval(this.timerID);\n    }\n  }\n\n  componentDidMount() {\n    {\n      /*My default timerLength is 55min so might as well make it easy on me*/\n    }\n    let startupTime = 3300000;\n    let timeObject = Object(_helperFunctions__WEBPACK_IMPORTED_MODULE_0__[\"millisecondConversion\"])(startupTime);\n    this.setState({\n      timerLength: startupTime,\n      timerString: timeObject.timeString\n    });\n  }\n\n  componentWillUnmount() {\n    clearInterval(this.timerID);\n  }\n\n  clearTimer() {\n    clearInterval(this.timerID);\n    this.setState({\n      running: false\n    });\n    let timerRemaining = this.state.timerRemaining;\n\n    if (timerRemaining === 0) {\n      this.setState({\n        timerLength: 0,\n        timerString: '00:00:00:000',\n        input: true\n      });\n    } else {\n      this.setState({\n        timerRemaining: 0,\n        timerString: Object(_helperFunctions__WEBPACK_IMPORTED_MODULE_0__[\"millisecondConversion\"])(this.state.timerLength).timeString\n      });\n    }\n  }\n\n  tick() {\n    if (this.state.timerRemaining === 0) {\n      this.setState({\n        timerRemaining: this.state.timerLength\n      });\n    }\n\n    let timerRemaining = this.endTime - Date.now();\n\n    try {\n      this.timeObject = Object(_helperFunctions__WEBPACK_IMPORTED_MODULE_0__[\"millisecondConversion\"])(timerRemaining);\n    } catch (rangeError) {\n      clearInterval(this.timerID);\n      this.setState({\n        running: !this.state.running,\n        timerString: 'CLEARED!',\n        timerRemaining: 0\n      });\n      return;\n      /*TODO: Audio chime in this catch to signify completion of the timer*/\n    }\n\n    this.setState({\n      timerRemaining: timerRemaining,\n      timerString: this.timeObject.timeString\n    });\n  }\n\n  inputTime(value) {\n    let timerString = this.state.timerString.slice(0, 8);\n    this.updateString = timerString.split(\":\").join('').slice(1) + value;\n    this.setState({\n      timerString: [this.updateString.slice(0, 2), this.updateString.slice(2, 4), this.updateString.slice(4), '000'].join(':')\n    });\n  }\n\n  setTimer() {\n    let timerLength = Object(_helperFunctions__WEBPACK_IMPORTED_MODULE_0__[\"timeStringMillisecondConversion\"])(this.updateString);\n    this.setState({\n      timerLength: timerLength,\n      timerRemaining: 0,\n      input: false\n    });\n  }\n\n  render() {\n    return React.createElement(\"div\", {\n      className: \"mui--text-center\"\n    }, React.createElement(Container, {\n      \"justify-content\": 'center'\n    }, React.createElement(\"h2\", {\n      \"data-cy\": \"timerStringDisplay\"\n    }, \" \", this.state.timerString), !this.state.input && React.createElement(Button, {\n      variant: \"raised\",\n      color: \"primary\",\n      \"data-cy\": \"startPauseTimerButton\",\n      onClick: this.startPauseTimer\n    }, this.state.running ? 'Pause' : 'Start'), this.state.input && React.createElement(Button, {\n      variant: \"raised\",\n      color: \"primary\",\n      \"data-cy\": \"timerInputButtonSet\",\n      onClick: this.setTimer\n    }, \"Set\"), React.createElement(Button, {\n      variant: \"raised\",\n      color: \"primary\",\n      \"data-cy\": \"clearTimerButton\",\n      onClick: this.clearTimer\n    }, \"Clear\"), this.state.input && React.createElement(\"div\", null, React.createElement(Button, {\n      variant: \"raised\",\n      color: \"primary\",\n      \"data-cy\": \"timerInputButton1\",\n      onClick: () => this.inputTime(1)\n    }, \"1\"), React.createElement(Button, {\n      variant: \"raised\",\n      color: \"primary\",\n      \"data-cy\": \"timerInputButton2\",\n      onClick: () => this.inputTime(2)\n    }, \"2\"), React.createElement(Button, {\n      variant: \"raised\",\n      color: \"primary\",\n      \"data-cy\": \"timerInputButton3\",\n      onClick: () => this.inputTime(3)\n    }, \"3\"), React.createElement(Button, {\n      variant: \"raised\",\n      color: \"primary\",\n      \"data-cy\": \"timerInputButton4\",\n      onClick: () => this.inputTime(4)\n    }, \"4\"), React.createElement(Button, {\n      variant: \"raised\",\n      color: \"primary\",\n      \"data-cy\": \"timerInputButton5\",\n      onClick: () => this.inputTime(5)\n    }, \"5\"), React.createElement(\"br\", null), React.createElement(Button, {\n      variant: \"raised\",\n      color: \"primary\",\n      \"data-cy\": \"timerInputButton6\",\n      onClick: () => this.inputTime(6)\n    }, \"6\"), React.createElement(Button, {\n      variant: \"raised\",\n      color: \"primary\",\n      \"data-cy\": \"timerInputButton7\",\n      onClick: () => this.inputTime(7)\n    }, \"7\"), React.createElement(Button, {\n      variant: \"raised\",\n      color: \"primary\",\n      \"data-cy\": \"timerInputButton8\",\n      onClick: () => this.inputTime(8)\n    }, \"8\"), React.createElement(Button, {\n      variant: \"raised\",\n      color: \"primary\",\n      \"data-cy\": \"timerInputButton9\",\n      onClick: () => this.inputTime(9)\n    }, \"9\"), React.createElement(Button, {\n      variant: \"raised\",\n      color: \"primary\",\n      \"data-cy\": \"timerInputButton0\",\n      onClick: () => this.inputTime(0)\n    }, \"0\"), React.createElement(\"br\", null))));\n  }\n\n}\n\n/* harmony default export */ __webpack_exports__[\"default\"] = (Timer);\n//# sourceMappingURL=timerComponent.js.map\n\n//# sourceURL=webpack:///./static/timerComponent.js?");

/***/ })

/******/ });