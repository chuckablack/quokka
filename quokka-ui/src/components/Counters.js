import React, {Component} from 'react';

class Counters extends Component {

    constructor(props) {
        super(props);
        this.state = {
            counters: {counters: {}},
            isLoading: false,
        };
    }

    fetchCounters() {
        fetch('http://127.0.0.1:5000/device?device=devnet-csr-always-on-sandbox&info=counters')
            .then(res => res.json())
            .then((data) => {
                this.setState({counters: data, isLoading: false})
                console.log(this.state.counters)
            })
            .catch(console.log)
    }
    componentDidMount() {
        this.setState({isLoading: true});
        this.fetchCounters()
    }

    render() {

        const {counters, isLoading} = this.state;

        if (isLoading) {
            return <p>Loading ...</p>;
        }
        return (
            <div className="container">
                <h1>Interface Counters Table</h1>
                <button onClick={() => {this.fetchCounters()}}>Refresh Counters</button>
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
