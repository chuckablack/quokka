import React, {Component} from 'react';
import Button from '@material-ui/core/Button'
import CircularProgress from "@material-ui/core/CircularProgress";

class Counters extends Component {

    constructor(props) {
        super(props);
        this.state = {
            counters: {counters: {}},
            isLoading: false,
        };
    }

    fetchCounters() {
        this.setState({isLoading: true});
        fetch('http://127.0.0.1:5000/device?device=devnet-csr-always-on-sandbox&info=counters')
            .then(res => res.json())
            .then((data) => {
                this.setState({counters: data, isLoading: false})
                console.log(this.state.counters)
            })
            .catch(console.log)
    }
    componentDidMount() {
        this.fetchCounters()
    }

    render() {

        const {counters, isLoading} = this.state;

        if (isLoading) {
            return (
                <div className="container">
                    <h1>Interface Counters Table</h1>
                    <p>Loading ...</p>
                    <CircularProgress />
                </div>
            );
        }
        return (
            <div className="container">
                <h1>Interface Counters Table</h1>
                <Button variant="contained" onClick={() => {this.fetchCounters()}}>Refresh Counters</Button>
                <table width="80%">
                    <tbody>
                    <tr>
                        <th>Interface</th>
                        <th>Rx Octets</th>
                        <th>Tx Octets</th>
                    </tr>
                    {/*const {counters} = counters.counters;*/}
                    {Object.keys(counters.counters).map((key, index) => (
                        <tr key={index}>
                            <td>{key}</td>
                            <td>{counters.counters[key].rx_octets}</td>
                            <td>{counters.counters[key].tx_octets}</td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            </div>
        );
    }
}

export default Counters;
