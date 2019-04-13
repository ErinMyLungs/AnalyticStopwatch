import {millisecondConversion, timeStringMillisecondConversion} from "./helperFunctions";

let Button = mui.react.Button;
let Container = mui.react.Container;

class Timer extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            running: false,
            input: false,
            timerLength: 0,
            timerRemaining: 0,
            timerString: '00:00:00:000',
        };
        this.startPauseTimer = this.startPauseTimer.bind(this);
        this.clearTimer = this.clearTimer.bind(this);
        this.setTimer = this.setTimer.bind(this);
    }

    startPauseTimer() {
        let running = !this.state.running;
        this.setState({
            running: running,
        });
        if (running) {
            this.endTime = this.state.timerRemaining === 0 ? Date.now() + this.state.timerLength : Date.now() + this.state.timerRemaining;
            this.timerID = setInterval(
                () => this.tick(), 10);
        }
        if (!running) {
            clearInterval(this.timerID)
        }
    }

    componentDidMount() {
        {/*My default timerLength is 55min so might as well make it easy on me*/
        }
        let startupTime = 3300000;
        let timeObject = millisecondConversion(startupTime);
        this.setState({
            timerLength: startupTime,
            timerString: timeObject.timeString,
        });
    }

    componentWillUnmount() {
        clearInterval(this.timerID)
    }

    clearTimer() {
        clearInterval(this.timerID);
        this.setState({running: false,});
        let timerRemaining = this.state.timerRemaining;
        if (timerRemaining === 0) {
            this.setState({
                timerLength: 0,
                timerString: '00:00:00:000',
                input: true
            })
        } else {
            this.setState({
                timerRemaining: 0,
                timerString: (millisecondConversion(this.state.timerLength).timeString)
            })
        }
    }

    tick() {
        if (this.state.timerRemaining === 0) {
            this.setState({
                timerRemaining: this.state.timerLength
            });
        }
        let timerRemaining = this.endTime - Date.now();

        try {
            this.timeObject = millisecondConversion(timerRemaining);
        }
        catch (rangeError) {
            clearInterval(this.timerID);
            this.setState({
                running: !this.state.running,
                timerString: 'CLEARED!',
                timerRemaining: 0
            });

                return;

            /*TODO: Audio chime in this catch to signify completion of the timer*/
        }
        this.setState({
            timerRemaining: timerRemaining,
            timerString: this.timeObject.timeString,
        });

    }

    inputTime(value) {
        let timerString = this.state.timerString.slice(0, 8);
        this.updateString = timerString.split(":").join('').slice(1) + value;
        this.setState({
            timerString: ([this.updateString.slice(0, 2), this.updateString.slice(2, 4), this.updateString.slice(4), '000'].join(':'))
        })
    }

    setTimer() {
        let timerLength = timeStringMillisecondConversion(this.updateString);
        this.setState({
            timerLength: timerLength,
            timerRemaining: 0,
            input: false
        })

    }


    render() {
        return (
            <div className="mui--text-center">
                <Container justify-content={'center'}>
                    <h2 data-cy="timerStringDisplay"> {this.state.timerString}</h2>
                    {!this.state.input && <Button variant="raised" color="primary" data-cy="startPauseTimerButton"
                                                  onClick={this.startPauseTimer}>{this.state.running ? 'Pause' : 'Start'}</Button>}
                    {this.state.input && <Button variant="raised" color="primary" data-cy="timerInputButtonSet"
                                                 onClick={this.setTimer}>Set</Button>}
                    <Button variant="raised" color="primary" data-cy="clearTimerButton"
                            onClick={this.clearTimer}>Clear</Button>

                    {this.state.input && <div>
                        <Button variant="raised" color="primary" data-cy="timerInputButton1"
                                onClick={() => this.inputTime(1)}>1</Button>
                        <Button variant="raised" color="primary" data-cy="timerInputButton2"
                                onClick={() => this.inputTime(2)}>2</Button>
                        <Button variant="raised" color="primary" data-cy="timerInputButton3"
                                onClick={() => this.inputTime(3)}>3</Button>
                        <Button variant="raised" color="primary" data-cy="timerInputButton4"
                                onClick={() => this.inputTime(4)}>4</Button>
                        <Button variant="raised" color="primary" data-cy="timerInputButton5"
                                onClick={() => this.inputTime(5)}>5</Button>
                        <br/>
                        <Button variant="raised" color="primary" data-cy="timerInputButton6"
                                onClick={() => this.inputTime(6)}>6</Button>
                        <Button variant="raised" color="primary" data-cy="timerInputButton7"
                                onClick={() => this.inputTime(7)}>7</Button>
                        <Button variant="raised" color="primary" data-cy="timerInputButton8"
                                onClick={() => this.inputTime(8)}>8</Button>
                        <Button variant="raised" color="primary" data-cy="timerInputButton9"
                                onClick={() => this.inputTime(9)}>9</Button>
                        <Button variant="raised" color="primary" data-cy="timerInputButton0"
                                onClick={() => this.inputTime(0)}>0</Button>
                        <br/>
                    </div>}
                </Container>
            </div>
        );
    }
}


export default Timer