import React, {Component} from 'react';
import Button from '@material-ui/core/Button'
import CircularProgress from "@material-ui/core/CircularProgress";
import Grid from "@material-ui/core/Grid";
import Table from '@material-ui/core/Table'
import TableBody from '@material-ui/core/TableBody'
import TableRow from '@material-ui/core/TableRow'
import TableCell from '@material-ui/core/TableCell'
import TableHead from '@material-ui/core/TableHead'
import 'typeface-roboto'

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
                    <CircularProgress/>
                </div>
            );
        }
        return (
            <div className="container">
                <Grid container direction="row" justify="space-between" alignItems="center">
                    <h1>ARP Table</h1>
                    <Button variant="contained" onClick={() => {
                        this.fetchArp()
                    }}>Refresh Arp</Button>
                </Grid>
                <Table size="small">
                    <TableHead>
                        <TableRow>
                            <TableCell>IP Address</TableCell>
                            <TableCell>MAC Address</TableCell>
                            <TableCell>Interface</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {arp_table.arp.map((arp_entry) => (
                            <TableRow key={arp_entry.mac}>
                                <TableCell>{arp_entry.ip}</TableCell>
                                <TableCell>{arp_entry.mac}</TableCell>
                                <TableCell>{arp_entry.interface}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </div>
        );
    }
}

export default Arp;
