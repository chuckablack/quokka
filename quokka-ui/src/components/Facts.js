import React, {Component} from 'react';
import Button from '@material-ui/core/Button'
import CircularProgress from "@material-ui/core/CircularProgress";
import Grid from "@material-ui/core/Grid";
import Table from '@material-ui/core/Table'
import TableBody from '@material-ui/core/TableBody'
import TableRow from '@material-ui/core/TableRow'
import TableCell from '@material-ui/core/TableCell'
import 'typeface-roboto'

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
                    <p>Loading {this.props.deviceName}...</p>
                    <CircularProgress />
                </div>
            );
        }
        return (
            <div className="container">
                <Grid container direction="row" justify="space-between" alignItems="center">
                    <h1>Facts</h1>
                    <Button variant="contained" onClick={() => {this.fetchFacts()}}>Refresh Facts</Button>
                </Grid>
                <Table>
                    <TableBody>
                    <TableRow>
                        <TableCell style={{ fontWeight:'bold' }}>FQDN</TableCell>
                        <TableCell>{facts.facts.fqdn}</TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell style={{ fontWeight:'bold' }}>Hostname</TableCell>
                        <TableCell>{facts.facts.hostname}</TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell style={{ fontWeight:'bold' }}>Model</TableCell>
                        <TableCell>{facts.facts.model}</TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell style={{ fontWeight:'bold' }}>OS Version</TableCell>
                        <TableCell>{facts.facts.os_version}</TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell style={{ fontWeight:'bold' }}>Serial</TableCell>
                        <TableCell>{facts.facts.serial_number}</TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell style={{ fontWeight:'bold' }}>Vendor</TableCell>
                        <TableCell>{facts.facts.vendor}</TableCell>
                    </TableRow>
                    </TableBody>
                </Table>
            </div>
        );
    }
}

export default Facts;
