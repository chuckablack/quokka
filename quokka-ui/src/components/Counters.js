import React, {Component} from 'react';
import Button from '@material-ui/core/Button'
import CircularProgress from "@material-ui/core/CircularProgress";
import Grid from "@material-ui/core/Grid";
import Table from '@material-ui/core/Table'
import TableBody from '@material-ui/core/TableBody'
import TableRow from '@material-ui/core/TableRow'
import TableCell from '@material-ui/core/TableCell'
import TableHead from '@material-ui/core/TableHead'
import Backdrop from '@material-ui/core/Backdrop'
import 'typeface-roboto'

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

        // if (isLoading) {
        //     return (
        //         <div style={{textAlign: "center"}} className="container">
        //             <h1>Counters Table</h1>
        //             <p>Loading ...</p>
        //             <CircularProgress/>
        //         </div>
        //     );
        // }

        return (
            <div className="container">
                <Grid container direction="row" justify="space-between" alignItems="center">
                    <h1>Counters Table</h1>
                    {isLoading ?
                        <Backdrop open={true}>
                            <CircularProgress color="inherit" />
                        </Backdrop>
                        : ""}
                    <Button variant="contained" onClick={() => {
                        this.fetchCounters()
                    }}>Refresh Counters</Button>
                </Grid>
                <Grid item  xs={12}>
                    <Table size="small">
                        <TableHead>
                            <TableRow>
                                <TableCell>Interface</TableCell>
                                <TableCell>Rx Octets</TableCell>
                                <TableCell>Tx Octets</TableCell>
                                <TableCell>Rx Packets</TableCell>
                                <TableCell>Tx Packets</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {Object.keys(counters.counters).map((key, index) => (
                                <TableRow key={index}>
                                    <TableCell>{key}</TableCell>
                                    <TableCell>{counters.counters[key].rx_octets}</TableCell>
                                    <TableCell>{counters.counters[key].tx_octets}</TableCell>
                                    <TableCell>{counters.counters[key].rx_unicast_packets}</TableCell>
                                    <TableCell>{counters.counters[key].tx_unicast_packets}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </Grid>
            </div>
        );
    }
}

export default Counters;
