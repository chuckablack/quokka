import React, {Component} from 'react';

class Arp extends Component {

    constructor(props) {
        super(props);
        this.state = {
            arp_table: {arp: []},
            isLoading: false,
        };
    }

    fetchArp() {
        this.setState({isLoading: true});
        fetch('http://127.0.0.1:5000/device?device=devnet-csr-always-on-sandbox&info=arp')
            .then(res => res.json())
            .then((data) => {
                this.setState({arp_table: data, isLoading: false})
                console.log(this.state.arp_table)
            })
            .catch(console.log)
    }

    componentDidMount() {
        this.fetchArp()
    }

    render() {

        const {arp_table, isLoading} = this.state;

        if (isLoading) {
            return (
                <div className="container">
                    <h1>ARP Table</h1>
                    <p>Loading ...</p>
                </div>
            );
        }
        return (
            <div className="container">
                <h1>ARP Table</h1>
                <button onClick={() => {this.fetchArp()}}>Refresh Arp Information</button>
                <table width="80%">
                    <tbody>
                    <tr>
                        <th>IP Address</th>
                        <th>MAC Address</th>
                        <th>Interface</th>
                    </tr>
                    {arp_table.arp.map((arp_entry) => (
                        <tr key={arp_entry.mac}>
                            <td>{arp_entry.ip}</td>
                            <td>{arp_entry.mac}</td>
                            <td>{arp_entry.interface}</td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            </div>
        );
    }
}

export default Arp;
