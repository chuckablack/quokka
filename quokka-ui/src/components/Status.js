import React, {Component} from 'react';

class Status extends Component {

    constructor(props) {
        super(props);
        this.state = {
            status_table: {status: []},
            isLoading: false,
        };
    }

    componentDidMount() {
        this.setState({isLoading: true});

        fetch('http://127.0.0.1:5000/device?device=devnet-csr-always-on-sandbox&info=status')
            .then(res => res.json())
            .then((data) => {
                this.setState({status_table: data, isLoading: false})
                console.log(this.state.status_table)
            })
            .catch(console.log)
    }

    render() {

        const {status_table, isLoading} = this.state;

        if (isLoading) {
            return <p>Loading ...</p>;
        }
        return (
            <div className="container">
                <div className="col-xs-12">
                    <h2>Status Table</h2>
                    <table width="80%">
                        <tbody>
                        <tr>
                            <th>IP Address</th>
                            <th>MAC Address</th>
                            <th>Interface</th>
                        </tr>
                        {this.state.status_table.status.map((status_entry) => (
                            <tr key={status_entry.mac}>
                                <td>{status_entry.ip}</td>
                                <td>{status_entry.mac}</td>
                                <td>{status_entry.interface}</td>
                            </tr>
                        ))}
                        </tbody>
                    </table>
                </div>
            </div>
        );
    }
}

export default Status;
