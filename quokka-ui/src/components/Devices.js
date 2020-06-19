import React, {Component} from 'react';
import Button from '@material-ui/core/Button'
import Grid from "@material-ui/core/Grid";
import 'typeface-roboto'
import CheckCircleIcon from "@material-ui/icons/CheckCircle";
import {green, red} from "@material-ui/core/colors";
import CancelIcon from "@material-ui/icons/Cancel";
import MaterialTable from "material-table";

class Devices extends Component {

    constructor(props) {
        super(props);
        this.state = {
            devices: {devices: []},
            dashboard: props.dashboard,
        };
    }

    fetchDevices() {

        let requestUrl = 'http://127.0.0.1:5000/devices'
        fetch(requestUrl)
            .then(res => res.json())
            .then((data) => {
                this.setState({devices: data})
                console.log(this.state.devices)
            })
            .catch(console.log)
    }

    componentDidMount() {
        this.fetchDevices(false)
        this.interval = setInterval(() => this.fetchDevices(), 60000)
    }

    componentWillUnmount() {
        clearInterval(this.interval)
    }

    renderDeviceStatus(deviceName) {
        this.state.dashboard.setState({deviceName: deviceName, show: "devicestatus"})
    }

    render() {

        const {devices} = this.state;

        return (
            <div className="container" style={{maxWidth: "100%"}}>
                <link
                    rel="stylesheet"
                    href="https://fonts.googleapis.com/icon?family=Material+Icons"
                />
                <Grid container direction="row" justify="space-between" alignItems="center">
                    <h2>Devices Table</h2>
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
                        { title: 'Rsp Time', render: rowData => (rowData.response_time)/1000 },
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
                            tooltip: 'Display Device Status',
                            onClick: (event, rowData) => {
                                this.renderDeviceStatus(rowData.name)
                            }
                        }
                    ]}
                />
            </div>
        );
    }
}

export default Devices;
