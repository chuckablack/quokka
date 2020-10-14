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
import Backdrop from "@material-ui/core/Backdrop";

class Arp extends Component {

    constructor(props) {
        super(props);
        this.state = {
            deviceName: props.deviceName,
            arp_table: {arp: []},
            isLoading: false,
        };
    }

    fetchArp() {
        const deviceName = this.state.deviceName

        this.setState({isLoading: true});
        fetch(process.env.REACT_APP_QUOKKA_HOST + '/ui/device?device=' + deviceName + '&info=arp')
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

        return (
            <div className="container">
                <Grid container direction="row" justify="space-between" alignItems="center">
                    <h2>ARP Table</h2>
                    {isLoading ?
                        <Backdrop open={true}>
                            <CircularProgress color="inherit" />
                        </Backdrop>
                        : ""}
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
