import React, {Component} from 'react';

class Interfaces extends Component {

    constructor(props) {
        super(props);
        this.state = {
            interfaces_table: {interfaces: []},
            isLoading: false,
        };
    }

    componentDidMount() {
        this.setState({isLoading: true});

        fetch(process.env.REACT_APP_QUOKKA_HOST + '/ui/device?device=devnet-csr-always-on-sandbox&info=interfaces')
            .then(res => res.json())
            .then((data) => {
                this.setState({interfaces_table: data, isLoading: false})
                console.log(this.state.interfaces_table)
            })
            .catch(console.log)
    }

    render() {

        const {interfaces_table, isLoading} = this.state;

        if (isLoading) {
            return <p>Loading ...</p>;
        }
        return (
            <div className="container">
                <div className="col-xs-12">
                    <h2>Interfaces Table</h2>
                    <table width="80%">
                        <tbody>
                        <tr>
                            <th>IP Address</th>
                            <th>MAC Address</th>
                            <th>Interface</th>
                        </tr>
                        {this.state.interfaces_table.interfaces_table.map((interface_entry) => (
                            <tr key={interface_entry.mac}>
                                <td>{interface_entry.ip}</td>
                                <td>{interface_entry.mac}</td>
                                <td>{interface_entry.interface}</td>
                            </tr>
                        ))}
                        </tbody>
                    </table>
                </div>
            </div>
        );
    }
}

export default Interfaces;
