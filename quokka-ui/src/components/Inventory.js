import React, {Component} from 'react';
import Button from '@material-ui/core/Button'
import CircularProgress from "@material-ui/core/CircularProgress";
import Grid from "@material-ui/core/Grid";
import Table from '@material-ui/core/Table'
import TableBody from '@material-ui/core/TableBody'
import TableRow from '@material-ui/core/TableRow'
import TableCell from '@material-ui/core/TableCell'
import 'typeface-roboto'
import Backdrop from "@material-ui/core/Backdrop";
import TableHead from "@material-ui/core/TableHead";

class Inventory extends Component {

    constructor(props) {
        super(props);
        this.state = {
            devices: {inventory: []},
            isLoading: false,
        };
    }

    fetchInventory(getLive) {
        const deviceName = this.state.deviceName

        this.setState({isLoading: true});
        let requestUrl = 'http://127.0.0.1:5000/inventory'
        fetch(requestUrl)
            .then(res => res.json())
            .then((data) => {
                this.setState({devices: data, isLoading: false})
                console.log(this.state.devices)
            })
            .catch(console.log)
    }

    componentDidMount() {
        this.fetchInventory(false)
    }

    render() {

        const {devices, isLoading} = this.state;

        return (
            <div className="container">
                <Grid container direction="row" justify="space-between" alignItems="center">
                    <h1>Device Inventory Table</h1>
                    {isLoading ?
                        <Backdrop open={true}>
                            <CircularProgress color="inherit" />
                        </Backdrop>
                        : ""}
                    <Button variant="contained" onClick={() => {
                        this.fetchInventory()
                    }}>Refresh Inventory</Button>
                </Grid>
                <Table size="small">
                    <TableHead>
                        <TableRow>
                            <TableCell>Name</TableCell>
                            <TableCell>Vendor</TableCell>
                            <TableCell>OS</TableCell>
                            <TableCell>IP Address</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {devices.inventory.map((device) => (
                            <TableRow key={device.name}>
                                <TableCell>{device.name}</TableCell>
                                <TableCell>{device.vendor}</TableCell>
                                <TableCell>{device.os}</TableCell>
                                <TableCell>{device.ip_address}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </div>
        );
    }
}

export default Inventory;
