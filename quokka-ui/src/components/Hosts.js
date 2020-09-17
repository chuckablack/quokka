import React, {Component} from 'react';
import Button from '@material-ui/core/Button'
import CircularProgress from "@material-ui/core/CircularProgress";
import Grid from "@material-ui/core/Grid";
import 'typeface-roboto'
import Backdrop from "@material-ui/core/Backdrop";
import CheckCircleIcon from '@material-ui/icons/CheckCircle';
import CancelIcon from '@material-ui/icons/Cancel';
import {green, red} from '@material-ui/core/colors';
import MaterialTable from "material-table";
import Dialog from '@material-ui/core/Dialog'
import DialogTitle from '@material-ui/core/DialogTitle'
import DialogActions from "@material-ui/core/DialogActions";
import DialogContent from "@material-ui/core/DialogContent";

class Hosts extends Component {

    constructor(props) {
        super(props);
        this.state = {
            hosts: {hosts: []},
            isLoading: false,
            dashboard: props.dashboard,
            countdownValue: process.env.REACT_APP_REFRESH_RATE,
            openPortScanDialog: false,
            portScanHost: '',
            portScanResults: "[22, 23, 80, 443]",
        };
    }

    countdown() {
        this.setState({countdownValue: this.state.countdownValue-1})
        if (this.state.countdownValue <= 0) {
            this.fetchHosts()
        }
    }

    fetchHosts() {

        this.setState({isLoading: true});
        let requestUrl = 'http://' + process.env.REACT_APP_QUOKKA_HOST + ':5000/ui/hosts'
        fetch(requestUrl)
            .then(res => res.json())
            .then((data) => {
                this.setState({hosts: data, isLoading: false})
                console.log(this.state.hosts)
                this.setState({countdownValue: process.env.REACT_APP_REFRESH_RATE})
            })
            .catch(console.log)
    }

    fetchPortScan(hostId) {

        this.setState({isLoading: true});
        this.setState({portScanResults: {result: "scanning ...", open_ports: "scanning ..."}})
        let requestUrl = 'http://' + process.env.REACT_APP_QUOKKA_HOST + ':5000/ui/scan?hostid=' + hostId
        const requestOptions = { method: 'GET'}
        fetch(requestUrl, requestOptions)
            .then(res => res.json())
            .then((data) => {
                this.setState({portScanResults: data, isLoading: false})
                console.log(this.state.portScanResults)
            })
            .catch(console.log)
    }

    componentDidMount() {
        this.fetchHosts()
        this.interval = setInterval(() => this.countdown(), 1000)
    }

    componentWillUnmount() {
        clearInterval(this.interval)
    }

    renderHostTS(hostId) {
        this.state.dashboard.setState({hostId: hostId, show: "hoststatus"})
    }

    renderCapture(ip) {
        this.state.dashboard.setState({ip: ip, protocol: null, port: null, show: "capture"})
    }

    handleClosePortScanDialog(parent) {
        parent.setState({openPortScanDialog: false})
    }

    renderPortScanDialog(hostId, ip) {
        this.fetchPortScan(hostId)
        this.setState({openPortScanDialog: true, portScanHost: ip})
    }


    render() {

        const {hosts, isLoading} = this.state;

        return (
            <div className="container" style={{maxWidth: "100%"}}>
                <link
                    rel="stylesheet"
                    href="https://fonts.googleapis.com/icon?family=Material+Icons"
                />
                <Grid container direction="row" justify="space-between" alignItems="center">
                    <h2>Hosts Table</h2>
                    {isLoading ?
                        <Backdrop open={true}>
                            <CircularProgress color="inherit" />
                        </Backdrop>
                        : ""}
                    <h6>Time until refresh: {this.state.countdownValue} seconds</h6>
                    <Button variant="contained" onClick={() => {
                        this.fetchHosts()
                    }}>Refresh Hosts</Button>
                </Grid>
                <MaterialTable
                    isLoading={this.state.isLoading}
                    title="Discovered Hosts with Availability and Response Time"
                    columns={[
                        {
                            title: 'Status',
                            render: rowData =>
                                rowData.availability ?
                                    <CheckCircleIcon style={{color: green[500]}}/>
                                    : <CancelIcon style={{color: red[500]}}/>,
                        },
                        { title: 'Name', field: 'name' },
                        { title: 'IP Address', field: 'ip_address', defaultSort: 'asc' },
                        { title: 'MAC Address', field: 'mac_address' },
                        { title: 'Rsp Time', field: 'response_time' },
                        { title: 'Last Heard', field: 'last_heard' },
                    ]}
                    data={ hosts.hosts }
                    options={{
                        sorting: true,
                        padding: "dense",
                        pageSize: 10,
                    }}
                    actions={[
                        {
                            icon: 'poll',
                            tooltip: 'Display Time-Series for Host',
                            onClick: (event, rowData) => {
                                this.renderHostTS(rowData.id)
                            }
                        },
                        {
                            icon: 'pageview',
                            tooltip: 'Capture packets for host',
                            onClick: (event, rowData) => {
                                this.renderCapture(rowData.ip_address)
                            }
                        },
                        {
                            icon: 'policy',
                            tooltip: 'Scan for open ports',
                            onClick: (event, rowData) => {
                                this.renderPortScanDialog(rowData.id, rowData.ip_address)
                            }
                        }

                    ]}

                />
                <Dialog
                    open={this.state.openPortScanDialog}
                >
                    <DialogTitle>Port Scan Results: {this.state.portScanHost}</DialogTitle>
                    <DialogContent>
                        <b>Open TCP Ports for connections:</b><br />
                        Result: {this.state.portScanResults.result}<br />
                        Open Ports: {this.state.portScanResults.open_ports}
                        <br /><br />
                        <b>NOTE:</b><br />
                        Depending on the host, scanning may take up to a few minutes to complete
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={() => this.handleClosePortScanDialog(this)}>
                            Close
                        </Button>
                    </DialogActions>
                </Dialog>
            </div>
        );
    }
}

export default Hosts;
