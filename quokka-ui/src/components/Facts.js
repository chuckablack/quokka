import React, {Component} from 'react';

class Facts extends Component {

    constructor(props) {
        super(props);
        this.state = {
            facts: {facts: {}},
            isLoading: false,
        };
    }

    fetchFacts() {
        this.setState({isLoading: true});
        fetch('http://127.0.0.1:5000/device?device=devnet-csr-always-on-sandbox&info=facts')
            .then(res => res.json())
            .then((data) => {
                this.setState({facts: data, isLoading: false})
                console.log(this.state.facts)
            })
            .catch(console.log)
    }

    componentDidMount() {
        this.fetchFacts()
    }

    render() {

        const {facts, isLoading} = this.state;

        if (isLoading) {
            return (
                <div className="container">
                    <h1>Facts Table</h1>
                    <p>Loading ...</p>
                </div>
            );
        }
        return (
            <div className="container">
                <h1>Facts</h1>
                <button onClick={() => {this.fetchFacts()}}>Refresh Facts</button>
                <table width="80%" cellPadding='2'>
                    <tbody>
                    <tr>
                        <td style={{ fontWeight:'bold' }}>FQDN</td>
                        <td>key={facts.facts.fqdn}</td>
                    </tr>
                    <tr>
                        <td style={{ fontWeight:'bold' }}>Hostname</td>
                        <td>{facts.facts.hostname}</td>
                    </tr>
                    <tr>
                        <td style={{ fontWeight:'bold' }}>Model</td>
                        <td>{facts.facts.model}</td>
                    </tr>
                    <tr>
                        <td style={{ fontWeight:'bold' }}>OS Version</td>
                        <td>{facts.facts.os_version}</td>
                    </tr>
                    <tr>
                        <td style={{ fontWeight:'bold' }}>Serial</td>
                        <td>{facts.facts.serial_number}</td>
                    </tr>
                    <tr>
                        <td style={{ fontWeight:'bold' }}>Vendor</td>
                        <td>{facts.facts.vendor}</td>
                    </tr>
                    </tbody>
                </table>
            </div>
        );
    }
}

export default Facts;
