export function millisecondConversion(timeDelta = 0) {
    {/*Takes milliseconds and converts it into ms, s, m, h in human readable and rounded values along with a string of them stitched together.*/
    }
    let timeObject = {};
    if (timeDelta < 0) {
        throw new RangeError('Negative Time Supplied');

    }
    timeObject.millisecond = Math.floor(timeDelta % 1000).toString().padStart(3, '0');
    timeDelta /= 1000;
    timeObject.seconds = Math.floor(timeDelta % 60).toString().padStart(2, '0');
    timeDelta /= 60;
    timeObject.minutes = Math.floor(timeDelta % 60).toString().padStart(2, '0');
    timeDelta /= 60;
    timeObject.hours = Math.floor(timeDelta % 24).toString().padStart(2, '0');
    timeObject.timeString = timeObject.hours + ':' + timeObject.minutes + ':' + timeObject.seconds + ':' + timeObject.millisecond;
    return timeObject;
}

export function timeStringMillisecondConversion(timeDelta = "000000") {
    /*a quick test*/
    if (typeof timeDelta !== 'string') {
        throw new TypeError('timeDelta must be a string! Did you mean to use milliSecondConversion?');
    }
    if (timeDelta.length !== 6) {
        throw new RangeError('String must have 6 characters')
    }
    let hours = Math.floor(parseInt(timeDelta.slice(0, 2)));
    let min = Math.floor(parseInt(timeDelta.slice(2, 4)));
    let sec = Math.floor(parseInt(timeDelta.slice(4)));
    /*Dimensional analysis to convert and sum human readable time-string to milliseconds*/
    let milliseconds = (((((hours * 60) + min) * 60) + sec) * 1000);
    return milliseconds
}
