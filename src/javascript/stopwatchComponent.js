import {millisecondConversion} from "./helperFunctions";

let Button = mui.react.Button;

class Stopwatch extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            date: Date.now(),
            timeDelta: 0,
            timeDiff: 0,
            timeString: '00:00:00:000',
            running: false,
        };
        this.startPauseWatch = this.startPauseWatch.bind(this);
        this.clearWatch = this.clearWatch.bind(this);
    }


    componentWillUnmount() {
        clearInterval(this.timerID);
    }

    tick() {
        let timeDelta = (Date.now() - this.state.date);
        let timeDiff = (this.state.timeDiff + timeDelta);
        let timeObject = millisecondConversion(timeDiff);
        this.setState({
            timeDelta: timeDelta,
            timeString: timeObject.timeString,
        });
    }

    startPauseWatch() {
        let running = !this.state.running;
        let counter = this.state.timeDelta + this.state.timeDiff;
        {/*directly using state gives flipped results from test.
             React will read the prior state, not the flipped one so this side-steps
             the problem by creating a var of the flipped state*/
        }
        this.setState({
            running: running,
            date: Date.now(),
        });
        if (running !== true) {
            this.setState({
                timeDiff: counter,
            });
            clearInterval(this.timerID)
        }
        if (running) {
            this.timerID = setInterval(
                () => this.tick(),
                10);
        }
    }

    clearWatch() {
        this.setState({
            date: Date.now(),
            timeDelta: 0,
            timeDiff: 0,
            timeString: '00:00:00:000',
            running: false,
        });
        clearInterval(this.timerID)
    }


    render() {
        return (
            <div>
                <h2 data-cy="stopwatchTimeString"> {this.state.timeString}</h2>
                <Button variant="raised" color="primary" data-cy="startPauseCounterButton"
                        onClick={this.startPauseWatch}>{this.state.running ? 'Pause' : 'Start'}</Button>
                <Button variant="raised" color="primary" data-cy="clearCounterButton"
                        onClick={this.clearWatch}>Clears</Button>
            </div>
        );
    }
}

export default Stopwatch