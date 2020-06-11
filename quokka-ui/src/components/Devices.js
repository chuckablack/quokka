import React, {Component} from 'react';
import Button from '@material-ui/core/Button'
import CircularProgress from "@material-ui/core/CircularProgress";
import Grid from "@material-ui/core/Grid";
import 'typeface-roboto'
import Backdrop from "@material-ui/core/Backdrop";
import CheckCircleIcon from "@material-ui/icons/CheckCircle";
import {green, red} from "@material-ui/core/colors";
import CancelIcon from "@material-ui/icons/Cancel";
import MaterialTable from "material-table";

class Devices extends Component {

    constructor(props) {
        super(props);
        this.state = {
            devices: {devices: []},
            isLoading: false,
            dashboard: props.dashboard,
        };
    }

    fetchDevices() {

        this.setState({isLoading: true});
        let requestUrl = 'http://127.0.0.1:5000/devices'
        fetch(requestUrl)
            .then(res => res.json())
            .then((data) => {
                this.setState({devices: data, isLoading: false})
                console.log(this.state.devices)
            })
            .catch(console.log)
    }

    componentDidMount() {
        this.fetchDevices(false)
        this.interval = setInterval(() => this.fetchDevices(), 300000)
    }

    componentWillUnmount() {
        clearInterval(this.interval)
    }

    renderDashboardFacts(deviceName) {
        this.state.dashboard.setState({deviceName: deviceName, show: "facts"})
    }

    render() {

        const {devices, isLoading} = this.state;

        return (
            <div className="container" style={{maxWidth: "100%"}}>
                <link
                    rel="stylesheet"
                    href="https://fonts.googleapis.com/icon?family=Material+Icons"
                />
                <Grid container direction="row" justify="space-between" alignItems="center">
                    <h2>Devices Table</h2>
                    {isLoading ?
                        <Backdrop open={true}>
                            <CircularProgress color="inherit"/>
                        </Backdrop>
                        : ""}
                    <Button variant="contained" onClick={() => {
                        this.fetchDevices()
                    }}>Refresh Devices</Button>
                </Grid>
                <MaterialTable
                    title="Device Status"
                    columns={[
                        {
                            width: null,
                            title: 'Status',
                            render: rowData =>
                                rowData.availability ?
                                    <CheckCircleIcon style={{color: green[500]}}/>
                                    : <CancelIcon style={{color: red[500]}}/>,
                        },
                        { title: 'Name', field: 'name' },
                        { title: 'Vendor:OS', render: rowData => rowData.vendor + ":" + rowData.os},
                        { title: 'IP Address', field: 'ip_address' },
                        { title: 'CPU%', field: 'cpu' },
                        { title: 'Memory%', field: 'memory' },
                        { title: 'Rsp Time (msec)', field: 'response_time' },
                        { title: 'Last Checked', field: 'last_heard' },
                    ]}
                    data={ devices.devices }
                    options={{
                        sorting: true,
                        padding: "dense",
                        pageSize: 10,
                    }}
                    actions={[
                        {
                            icon: 'dns',
                            tooltip: 'Display Device Facts',
                            onClick: (event, rowData) => {
                                this.renderDashboardFacts(rowData.name)
                            }
                        }
                    ]}
                    // actions={[{
                    //     onClick: (event, rowData) => {this.renderDashboardFacts(rowData.name)}
                    // }]}
                />
                {/*<Table size="small">*/}
                {/*    <TableHead>*/}
                {/*        <TableRow>*/}
                {/*            <TableCell align="center">Status</TableCell>*/}
                {/*            <TableCell>Name</TableCell>*/}
                {/*            <TableCell>Vendor : OS</TableCell>*/}
                {/*            <TableCell>IP Address</TableCell>*/}
                {/*            <TableCell>CPU%</TableCell>*/}
                {/*            <TableCell>Memory%</TableCell>*/}
                {/*            <TableCell align="center">Rsp Time (msec)</TableCell>*/}
                {/*            <TableCell>Last Heard</TableCell>*/}
                {/*        </TableRow>*/}
                {/*    </TableHead>*/}
                {/*    <TableBody>*/}
                {/*        {devices.devices.map((device) => (*/}
                {/*            <TableRow key={device.name}>*/}
                {/*                <TableCell align="center">{device.availability ?*/}
                {/*                    <CheckCircleIcon style={{color: green[500]}}/>*/}
                {/*                    : <CancelIcon  style={{color: red[500]}}/>*/}
                {/*                }</TableCell>*/}
                {/*                <TableCell onClick={() => this.renderDashboardFacts(device.name)}*/}
                {/*                           style={{cursor: 'pointer'}}>{device.name}</TableCell>*/}
                {/*                <TableCell>{device.vendor} : {device.os}</TableCell>*/}
                {/*                <TableCell>{device.ip_address}</TableCell>*/}
                {/*                <TableCell align="center">{device.cpu}</TableCell>*/}
                {/*                <TableCell align="center">{device.memory}</TableCell>*/}
                {/*                <TableCell align="center">{device.response_time}</TableCell>*/}
                {/*                <TableCell>{device.last_heard}</TableCell>*/}
                {/*            </TableRow>*/}
                {/*        ))}*/}
                {/*    </TableBody>*/}
                {/*</Table>*/}
            </div>
        );
    }
}

export default Devices;
