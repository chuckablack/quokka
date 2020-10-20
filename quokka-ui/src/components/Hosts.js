import React, {Component} from 'react';
import Button from '@material-ui/core/Button'
import Grid from "@material-ui/core/Grid";
import 'typeface-roboto'
import CheckCircleIcon from '@material-ui/icons/CheckCircle';
import CancelIcon from '@material-ui/icons/Cancel';
import {green, red} from '@material-ui/core/colors';
import MaterialTable from "material-table";
import AccountTreeTwoToneIcon from '@material-ui/icons/AccountTreeTwoTone'
import Dialog from '@material-ui/core/Dialog'
import DialogTitle from '@material-ui/core/DialogTitle'
import DialogActions from "@material-ui/core/DialogActions";
import DialogContent from "@material-ui/core/DialogContent";
import PolicyOutlinedIcon from '@material-ui/icons/PolicyOutlined'
import PolicyTwoToneIcon from '@material-ui/icons/PolicyTwoTone'

class Hosts extends Component {

    constructor(props) {
        super(props);
        this.state = {
            hosts: {hosts: []},
            dashboard: props.dashboard,
            countdownValue: process.env.REACT_APP_REFRESH_RATE,
            openPortScanDialog: false,
            openExtendedPortScanDialog: false,
            portScanHost: '',
            portScanResults: '',
            extendedPortScanResults: '',
            token: '',
            openTraceRouteDialog: false,
            target: '',
            traceRouteResults: {traceroute_output: ''},
        };
    }

    countdown() {
        this.setState({countdownValue: this.state.countdownValue-1})
        if (this.state.countdownValue === 0) {
            this.fetchHosts()
        }
    }

    fetchHosts() {

        let requestUrl = process.env.REACT_APP_QUOKKA_HOST + '/ui/hosts'
        fetch(requestUrl)
            .then(res => res.json())
            .then((data) => {
                console.log(data)
                this.setState({hosts: data})
                this.setState({countdownValue: process.env.REACT_APP_REFRESH_RATE})
            })
            .catch((e) => {
                console.log(e)
                this.setState({countdownValue: process.env.REACT_APP_REFRESH_RATE})
            });
    }

    fetchPortScan(hostId) {

        this.setState({portScanResults: {result: "scanning ...", open_ports: "scanning ..."}})
        let requestUrl = process.env.REACT_APP_QUOKKA_HOST + '/ui/scan?hostid=' + hostId
        const requestOptions = { method: 'GET'}
        fetch(requestUrl, requestOptions)
            .then(res => res.json())
            .then((data) => {
                this.setState({portScanResults: data})
                console.log(this.state.portScanResults)
            })
            .catch(console.log)
    }

    initiateExtendedPortScan(hostId) {

        this.setState({extendedPortScanResults: {result: "initiating scan ..."}})
        let requestUrl = process.env.REACT_APP_QUOKKA_HOST + '/ui/scan/extended?hostid=' + hostId
        const requestOptions = { method: 'POST'}
        fetch(requestUrl, requestOptions)
            .then(res => res.json())
            .then((data) => {
                this.setState({token: data.token})
                this.fetchExtendedPortScanResults(hostId)
                console.log(this.state.extendedPortScanResults)
            })
            .catch(console.log)
    }

    fetchExtendedPortScanResults( hostId ) {
       this.setState({extendedPortScanResults: {result: "retrieving scan results ..."}})
        let requestUrl = process.env.REACT_APP_QUOKKA_HOST + '/ui/scan/extended?hostid=' + hostId + '&token=' + this.state.token
        const requestOptions = { method: 'GET'}
        fetch(requestUrl, requestOptions)
            .then(res => res.json())
            .then((data) => {
                this.setState({extendedPortScanResults: data})
                console.log(this.state.extendedPortScanResults)
            })
            .catch(console.log)

    }

    initiateTraceRoute( target ) {

        this.setState({traceRouteResults: {result: "initiating trace route ...", traceroute_output: ""}})
        let requestUrl = process.env.REACT_APP_QUOKKA_HOST + '/ui/traceroute?target=' + target
        const requestOptions = { method: 'POST'}
        fetch(requestUrl, requestOptions)
            .then(res => res.json())
            .then((data) => {
                this.setState({token: data.token})
                this.fetchTraceRouteResults(target)
                console.log(this.state.traceRouteResults)
            })
            .catch(console.log)
    }

    fetchTraceRouteResults( target ) {
        this.setState({traceRouteResults: {result: "fetching route results ...", traceroute_output: ""}})
        let requestUrl = process.env.REACT_APP_QUOKKA_HOST + '/ui/traceroute?target=' + target + '&token=' + this.state.token
        const requestOptions = { method: 'GET'}
        fetch(requestUrl, requestOptions)
            .then(res => res.json())
            .then((data) => {
                this.setState({traceRouteResults: data})
                console.log(this.state.traceRouteResults)
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

    handleCloseExtendedPortScanDialog(parent) {
        parent.setState({openExtendedPortScanDialog: false})
    }

    handleCloseTraceRouteDialog(parent) {
        parent.setState({openTraceRouteDialog: false})
    }

    renderPortScanDialog(hostId, ip) {
        this.fetchPortScan(hostId)
        this.setState({openPortScanDialog: true, portScanHost: ip})
    }

    renderExtendedPortScanDialog(hostId, ip) {
        this.initiateExtendedPortScan(hostId)
        this.setState({openExtendedPortScanDialog: true, portScanHost: ip})
    }

    renderTraceRouteDialog(target) {
        this.initiateTraceRoute(target)
        this.setState({openTraceRouteDialog: true, target: target})
    }


    render() {

        const {hosts} = this.state;

        return (
            <div className="container" style={{maxWidth: "100%"}}>
                <link
                    rel="stylesheet"
                    href="https://fonts.googleapis.com/icon?family=Material+Icons"
                />
                <Grid container direction="row" justify="space-between" alignItems="center">
                    <h2>Hosts Table</h2>
                    <h6>Time until refresh: {this.state.countdownValue} seconds</h6>
                    <Button variant="contained" onClick={() => {
                        this.fetchHosts()
                    }}>Refresh Hosts</Button>
                </Grid>
                <MaterialTable
                    title="Discovered Hosts with Availability and Response Time"
                    columns={[
                        {
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
                            customSort: (a, b) => {
                                if( a.name.toUpperCase() > b.name.toUpperCase() ) return 1;
                                else if( a.name.toUpperCase() < b.name.toUpperCase() ) return -1;
                                else return 0;
                            }
                        },
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
                            icon: PolicyOutlinedIcon,
                            tooltip: 'Scan for open ports',
                            onClick: (event, rowData) => {
                                this.renderPortScanDialog(rowData.id, rowData.ip_address)
                            }
                        },
                        {
                            icon: PolicyTwoToneIcon,
                            tooltip: 'Extended Scan for open ports',
                            onClick: (event, rowData) => {
                                this.renderExtendedPortScanDialog(rowData.id, rowData.ip_address)
                            }
                        },
                        {
                            icon: AccountTreeTwoToneIcon,
                            tooltip: 'Trace-route to host',
                            onClick: (event, rowData) => {
                                this.renderTraceRouteDialog(rowData.name)
                            }
                        },
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
                <Dialog
                    open={this.state.openExtendedPortScanDialog}
                    maxWidth="lg"
                >
                    <DialogTitle>Extended Port Scan Results: {this.state.portScanHost}</DialogTitle>
                    <DialogContent>
                        <b>Output from extended scan:</b><br />
                        Result: {this.state.extendedPortScanResults.result}<br />
                        Extended scan results:
                        <pre>
                            {this.state.extendedPortScanResults.scan_output}
                        </pre>
                        <br /><br />
                        <b>NOTE:</b><br />
                        Depending on the host, scanning may take up to a few minutes to complete
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={() => this.handleCloseExtendedPortScanDialog(this)}>
                            Close
                        </Button>
                    </DialogActions>
                </Dialog>
                <Dialog
                    open={this.state.openTraceRouteDialog}
                    maxWidth="lg"
                >
                    <DialogTitle>Trace Route Results: {this.state.target}</DialogTitle>
                    <DialogContent>
                        <b>Output from trace route:</b><br />
                        Result: {this.state.traceRouteResults.result}<br />
                        Trace route results:
                        <img id="traceroute"
                             src={"data:image/png;base64," + this.state.traceRouteResults.traceroute_output}
                             alt="">
                        </img>
                        <br /><br />
                        <b>NOTE:</b><br />
                        Depending on the target, trace route may take up to a few minutes to complete
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={() => this.handleCloseTraceRouteDialog(this)}>
                            Close
                        </Button>
                    </DialogActions>
                </Dialog>
            </div>
        );
    }
}

export default Hosts;
