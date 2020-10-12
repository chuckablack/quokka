import React, {Component} from 'react';
import Button from '@material-ui/core/Button'
import Grid from "@material-ui/core/Grid";
import 'typeface-roboto'
import CheckCircleIcon from "@material-ui/icons/CheckCircle";
import {green, red} from "@material-ui/core/colors";
import CancelIcon from "@material-ui/icons/Cancel";
import MaterialTable from "material-table";
import Dialog from "@material-ui/core/Dialog";
import DialogTitle from "@material-ui/core/DialogTitle";
import DialogContent from "@material-ui/core/DialogContent";
import DialogActions from "@material-ui/core/DialogActions";
import ReactDiffViewer from 'react-diff-viewer'

const oldCode = `
const a = 10
const b = 10
const c = () => console.log('foo')

if(a > 10) {
  console.log('bar')
}

console.log('done')
`;
const newCode = `
const a = 10
const boo = 10

if(a === 10) {
  console.log('bar')
}
`;
class Devices extends Component {

    constructor(props) {
        super(props);
        this.state = {
            devices: {devices: []},
            dashboard: props.dashboard,
            countdownValue: process.env.REACT_APP_REFRESH_RATE,
            openConfigDiffDialog: false,
            deviceName: '',
            configDiff: {current: {}, old: {}}
        };
    }

    countdown() {
        this.setState({countdownValue: this.state.countdownValue-1})
        if (this.state.countdownValue === 0) {
            this.fetchDevices()
        }
    }

    fetchDevices() {

        let requestUrl = 'http://' + process.env.REACT_APP_QUOKKA_HOST + ':5000/ui/devices'
        fetch(requestUrl)
            .then(res => res.json())
            .then((data) => {
                console.log(data)
                this.setState({devices: data})
                this.setState({countdownValue: process.env.REACT_APP_REFRESH_RATE})
            })
            .catch((e) => {
                console.log(e)
                this.setState({countdownValue: process.env.REACT_APP_REFRESH_RATE})
            });
    }

    fetchDeviceConfigDiff(deviceName) {

        let requestUrl = 'http://' + process.env.REACT_APP_QUOKKA_HOST + ':5000/ui/device/config?device=' + deviceName
        fetch(requestUrl)
            .then(res => res.json())
            .then((data) => {
                console.log(data)
                this.setState({configDiff: data});
            })
            .catch((e) => {
                console.log(e)
            });

    }

    componentDidMount() {
        this.fetchDevices(false)
        this.interval = setInterval(() => this.countdown(), 1000)
    }

    componentWillUnmount() {
        clearInterval(this.interval)
    }

    renderDeviceStatus(deviceName) {
        this.state.dashboard.setState({deviceName: deviceName, show: "devicestatus"})
    }

    renderCapture(ip) {
        this.state.dashboard.setState({ip: ip, protocol: null, port: null, show: "capture"})
    }

    renderConfigDiffDialog(deviceName) {
        this.fetchDeviceConfigDiff(deviceName)
        this.setState({openConfigDiffDialog: true, deviceName: deviceName})
        this.setState({configDiff: {current: {}, old: {}}});
    }

    handleCloseConfigDiffDialog(parent) {
        parent.setState({openConfigDiffDialog: false})
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
                    <h6>Time until refresh: {this.state.countdownValue} seconds</h6>
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
                            customSort: (a, b) => {
                                if( a.availability && !b.availability ) return 1;
                                else if (a.availability === b.availability ) return 0
                                else return -1;
                            }
                        },
                        {   title: 'Name',
                            field: 'name',
                            defaultSort: 'asc',
                            customSort: (a, b) => {
                                if( a.name.toUpperCase() > b.name.toUpperCase() ) return 1;
                                else if( a.name.toUpperCase() < b.name.toUpperCase() ) return -1;
                                else return 0;
                            }
                        },
                        { title: 'Hostname', field: 'hostname', defaultSort: 'asc' },
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
                        },
                        {
                            icon: 'pageview',
                            tooltip: 'Capture packets for device',
                            onClick: (event, rowData) => {
                                this.renderCapture(rowData.ip_address)
                            }
                        },
                        {
                            icon: 'compare',
                            tooltip: 'Configuration Diff',
                            onClick: (event, rowData) => {
                                this.renderConfigDiffDialog(rowData.name)
                            }
                        },

                    ]}
                />
                <Dialog
                    open={this.state.openConfigDiffDialog}
                    maxWidth="lg"
                >
                    <DialogTitle>Config Diff Results: {this.state.deviceName}</DialogTitle>
                    <DialogContent>
                        <ReactDiffViewer
                            leftTitle={this.state.configDiff.old.timestamp}
                            oldValue={this.state.configDiff.old.config}
                            rightTitle={this.state.configDiff.current.timestamp}
                            newValue={this.state.configDiff.current.config}
                            splitView={true}
                        />
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={() => this.handleCloseConfigDiffDialog(this)}>
                            Close
                        </Button>
                    </DialogActions>
                </Dialog>
            </div>
        );
    }
}

export default Devices;
