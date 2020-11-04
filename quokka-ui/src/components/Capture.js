import React, {Component} from 'react';
import Button from '@material-ui/core/Button'
import CircularProgress from "@material-ui/core/CircularProgress";
import Grid from "@material-ui/core/Grid";
import 'typeface-roboto'
import Backdrop from "@material-ui/core/Backdrop";
import MaterialTable from "material-table";
import Paper from '@material-ui/core/Paper'

class Capture extends Component {

    constructor(props) {
        super(props);
        this.state = {
            packets: {packets: []},
            isLoading: false,
            dashboard: props.dashboard,
            ip: props.ip,
            protocol: props.protocol,
            port: props.port,
            countdownValue: process.env.REACT_APP_REFRESH_RATE,
        };
    }

    countdown() {
        this.setState({countdownValue: this.state.countdownValue-1})
        if (this.state.countdownValue === 0) {
            this.fetchPackets()
        }
    }

    fetchPackets() {

        const {ip, protocol, port} = this.state;

        this.setState({isLoading: true});
        let requestUrl = process.env.REACT_APP_QUOKKA_HOST + '/ui/capture?num_packets=1000';
        if( ip ) { requestUrl += '&ip=' + ip }
        if( protocol ) { requestUrl += '&protocol=' + protocol }
        if( port ) { requestUrl += '&port=' + port }
        fetch(requestUrl)
            .then(res => res.json())
            .then((data) => {
                console.log(data)
                this.setState({packets: data, isLoading: false})
                this.setState({countdownValue: process.env.REACT_APP_REFRESH_RATE})
            })
            .catch(console.log)
    }

    startCapture() {

        const {ip, protocol, port} = this.state;

        // this.setState({isLoading: true});
        let requestUrl = process.env.REACT_APP_QUOKKA_HOST + '/ui/capture?num_packets=10';
        if( ip ) { requestUrl += '&ip=' + ip }
        if( protocol ) { requestUrl += '&protocol=' + protocol }
        if( port ) { requestUrl += '&port=' + port }
        const requestOptions = { method: 'POST'}
        fetch(requestUrl, requestOptions)
            .catch(console.log)
    }

    componentDidMount() {
        this.fetchPackets()
        this.interval = setInterval(() => this.countdown(), 1000)
    }

    componentWillUnmount() {
        clearInterval(this.interval)
    }

    renderServices(dashboard) {
        dashboard.setState({show: "services"})
    }
    renderHosts(dashboard) {
        dashboard.setState({show: "hosts"})
    }
    renderDevices(dashboard) {
        dashboard.setState({show: "devices"})
    }
    renderWorkers(dashboard) {
        dashboard.setState({show: "workers"})
    }

    render() {

        const {packets, isLoading} = this.state;

        return (
            <Grid container direction="column">
                <Grid container direction="row" style={{paddingTop: '10px'}}>
                    <Grid item style={{width: '15%', paddingLeft: '10px'}}>
                        IP address:<br /><Paper elevation={3} /><b>{this.state.ip}</b>
                        <br /><br />
                        Protocol:<br /><b>{this.state.protocol}</b>
                        <br /><br />
                        Port:<br /><b>{this.state.port}</b>
                        <br /><br />  <br /><br />
                        <Button variant="contained" style={{width: '100%'}} onClick={() => this.startCapture()}>Start capture</Button>
                        <br /><br />
                        <Button variant="contained" style={{width: '100%'}} onClick={() => this.renderDevices(this.state.dashboard)}>Return to Devices</Button>
                        <Button variant="contained" style={{width: '100%'}} onClick={() => this.renderHosts(this.state.dashboard)}>Return to Hosts</Button>
                        <Button variant="contained" style={{width: '100%'}} onClick={() => this.renderServices(this.state.dashboard)}>Return to Services</Button>
                        <Button variant="contained" style={{width: '100%'}} onClick={() => this.renderWorkers(this.state.dashboard)}>Return to Workers</Button>
                    </Grid>

                    <Grid item style={{width: '85%', paddingRight: '10px'}}>
                        <div className="container" style={{maxWidth: "100%"}}>
                            <link
                                rel="stylesheet"
                                href="https://fonts.googleapis.com/icon?family=Material+Icons"
                            />
                            <Grid container direction="row" justify="space-between" alignItems="center">
                                <h2>Packets Table</h2>
                                {isLoading ?
                                    <Backdrop open={true}>
                                        <CircularProgress color="inherit" />
                                    </Backdrop>
                                    : ""}
                                <h6>Time until refresh: {this.state.countdownValue} seconds</h6>
                                <Button variant="contained" onClick={() => {
                                    this.fetchPackets()
                                }}>Refresh Packets</Button>
                            </Grid>
                            <MaterialTable
                                isLoading={this.state.isLoading}
                                title="Captured packets"
                                columns={[
                                    { title: 'Time', field: 'timestamp', defaultSort: 'desc' },
                                    { title: 'Ethernet Source', field: 'ether_src' },
                                    { title: 'Ethernet Dest', field: 'ether_dst' },
                                    { title: 'IP Source', field: 'ip_src' },
                                    { title: 'IP Dest', field: 'ip_dst' },
                                    { title: 'Protocol', field: 'protocol' },
                                    { title: 'SPort', field: 'sport' },
                                    { title: 'DPort', field: 'dport' },
                                ]}
                                data={ packets.packets }
                                options={{
                                    sorting: true,
                                    padding: "dense",
                                    pageSize: 10,
                                }}
                                detailPanel={rowData => {
                                    const detail = ['<pre id="json">', rowData.packet_json, '</pre>'].join('')
                                    return (
                                        <Grid container direction="row">
                                            <Grid item style={{width: '50%', padding: '10px'}}>
                                                <pre>
                                                    {rowData.packet_json}
                                                </pre>
                                            </Grid>
                                            <Grid item style={{width: '50%', padding: '10px'}}>
                                                <pre>
                                                    {rowData.packet_hexdump}
                                                </pre>
                                            </Grid>
                                        </Grid>
                                    )
                                }}
                            />
                        </div>
                    </Grid>
                </Grid>
            </Grid>
        );
    }
}

export default Capture;
