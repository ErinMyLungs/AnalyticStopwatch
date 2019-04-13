import Clock from "./clockComponent";
import Stopwatch from "./stopwatchComponent"
import Timer from "./timerComponent";

let Button = mui.react.Button;
let Container = mui.react.Container;


function Toggle(props) {
    if (props.componentSelection === 'Clock') {
        return <Clock/>;
    }

    if (props.componentSelection === 'Stopwatch') {
        return <Stopwatch/>;
    }

    if (props.componentSelection === 'Timer') {
        return <Timer/>;
    }
}

class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            currentTime: 0,
            componentSelection: 'Timer',
        };
        this.handleClick = this.handleClick.bind(this);
    }

    handleClick(event) {
        this.setState({
            componentSelection: event.target.value,
        });
    }

    render() {

        return (
            <div className="mui--text-center">
                <Container fluid={true}>
                    <Toggle componentSelection={this.state.componentSelection}/>
                    <br/>

                    {
                        this.state.componentSelection !== 'Clock' &&
                        <Button variant="raised" color="primary" value='Clock' data-cy="clockToggleButton"
                                onClick={this.handleClick}>Clock</Button>
                    }
                    {
                        this.state.componentSelection !== 'Stopwatch' &&
                        <Button variant="raised" color="primary" value='Stopwatch' data-cy="stopwatchToggleButton"
                                onClick={this.handleClick}>Stopwatch</Button>
                    }
                    {
                        this.state.componentSelection !== 'Timer' &&
                        <Button variant="raised" color="primary" value='Timer' data-cy="timerToggleButton"
                                onClick={this.handleClick}>Timer</Button>
                    }
                </Container>
            </div>
        )
    }

}

ReactDOM.render(<App/>, document.getElementById('root'));