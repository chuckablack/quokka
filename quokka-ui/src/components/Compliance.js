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

class Compliance extends Component {

    constructor(props) {
        super(props);
        this.state = {
            devices: {devices: []},
            isLoading: false,
            dashboard: props.dashboard,
            countdownValue: process.env.REACT_APP_REFRESH_RATE,
        };
    }

    countdown() {
        this.setState({countdownValue: this.state.countdownValue-1})
        if (this.state.countdownValue <= 0) {
            this.fetchCompliance()
        }
    }

    fetchCompliance() {

        this.setState({isLoading: true});
        let requestUrl = 'http://' + process.env.REACT_APP_QUOKKA_HOST + ':5000/ui/devices'
        fetch(requestUrl)
            .then(res => res.json())
            .then((data) => {
                this.setState({devices: data, isLoading: false})
                console.log(this.state.devices)
                this.setState({countdownValue: process.env.REACT_APP_REFRESH_RATE})
            })
            .catch(console.log)
    }

    componentDidMount() {
        this.fetchCompliance(false)
        this.interval = setInterval(() => this.countdown(), 1000)
    }

    componentWillUnmount() {
        clearInterval(this.interval)
    }

    renderDeviceStatus(deviceName) {
        this.state.dashboard.setState({deviceName: deviceName, show: "devicestatus"})
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
                    <h2>Compliance Table</h2>
                    {isLoading ?
                        <Backdrop open={true}>
                            <CircularProgress color="inherit"/>
                        </Backdrop>
                        : ""}
                    <h6>Time until refresh: {this.state.countdownValue} seconds</h6>
                    <Button variant="contained" onClick={() => {
                        this.fetchCompliance()
                    }}>Refresh Compliance</Button>
                </Grid>
                <MaterialTable
                    title="Device OS and Config Compliance"
                    columns={[
                        {
                            width: null,
                            title: 'Status',
                            render: rowData =>
                                rowData.availability ?
                                    <CheckCircleIcon style={{color: green[500]}}/>
                                    : <CancelIcon style={{color: red[500]}}/>,
                         },
                        { title: 'Name', field: 'name', defaultSort: 'asc' },
                        { title: 'Vendor : OS', render: rowData => rowData.vendor + " : " + rowData.os},
                        { title: 'IP Address', field: 'ip_address' },
                        {
                            title: 'Software Version',
                            headerStyle: {textAlign: 'right'},
                            cellStyle: {textAlign: 'center'},
                            render: rowData =>
                                rowData.os_compliance ?
                                    <CheckCircleIcon style={{color: green[500]}}/>
                                    : <CancelIcon  style={{color: red[500]}}/>
                        },
                        {
                            title: 'Config',
                            headerStyle: {textAlign: 'right'},
                            cellStyle: {textAlign: 'center'},
                            render: rowData =>
                                rowData.config_compliance ?
                                    <CheckCircleIcon style={{color: green[500]}}/>
                                    : <CancelIcon  style={{color: red[500]}}/>
                                    },
                        { title: 'Last Checked', field: 'last_compliance_check' },
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

export default Compliance;
