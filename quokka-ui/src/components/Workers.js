import React, {Component} from 'react';
import Button from '@material-ui/core/Button'
import Grid from "@material-ui/core/Grid";
import 'typeface-roboto'
import CheckCircleIcon from "@material-ui/icons/CheckCircle";
import {green, red} from "@material-ui/core/colors";
import CancelIcon from "@material-ui/icons/Cancel";
import MaterialTable from "material-table";
import AccountTreeTwoToneIcon from '@material-ui/icons/AccountTreeTwoTone'
import Dialog from "@material-ui/core/Dialog";
import DialogTitle from "@material-ui/core/DialogTitle";
import DialogContent from "@material-ui/core/DialogContent";
import DialogActions from "@material-ui/core/DialogActions";

class Workers extends Component {

    constructor(props) {
        super(props);
        this.state = {
            workers: {workers: []},
            dashboard: props.dashboard,
            countdownValue: process.env.REACT_APP_REFRESH_RATE,
            openConfigDiffDialog: false,
            workerId: '',
            openTraceRouteDialog: false,
            target: '',
            traceRouteResults: {traceroute_output: ''},
            token: '',
        };
    }

    countdown() {
        this.setState({countdownValue: this.state.countdownValue-1})
        if (this.state.countdownValue === 0) {
            this.fetchWorkers()
        }
    }

    fetchWorkers() {

        let requestUrl = process.env.REACT_APP_QUOKKA_HOST + '/ui/workers'
        fetch(requestUrl)
            .then(res => res.json())
            .then((data) => {
                console.log(data)
                this.setState({workers: data})
                this.setState({countdownValue: process.env.REACT_APP_REFRESH_RATE})
            })
            .catch((e) => {
                console.log(e)
                this.setState({countdownValue: process.env.REACT_APP_REFRESH_RATE})
            });
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
        this.fetchWorkers(false)
        this.interval = setInterval(() => this.countdown(), 1000)
    }

    componentWillUnmount() {
        clearInterval(this.interval)
    }

    renderWorkersStatus(workerId) {
        this.state.dashboard.setState({workerId: workerId, show: "workerstatus"})
    }

    renderCapture(ip) {
        if(ip === 'localhost') {
            return;
        }
        this.state.dashboard.setState({ip: ip, protocol: null, port: null, show: "capture"})
    }

    handleCloseTraceRouteDialog(parent) {
        parent.setState({openTraceRouteDialog: false})
    }

    renderTraceRouteDialog(target) {
        if(target === 'localhost') {
            return;
        }
        this.initiateTraceRoute(target)
        this.setState({openTraceRouteDialog: true, target: target})
    }

    render() {

        const {workers} = this.state;

        return (
            <div className="container" style={{maxWidth: "100%"}}>
                <link
                    rel="stylesheet"
                    href="https://fonts.googleapis.com/icon?family=Material+Icons"
                />
                <Grid container direction="row" justify="space-between" alignItems="center">
                    <h2>Workers Table</h2>
                    <h6>Time until refresh: {this.state.countdownValue} seconds</h6>
                    <Button variant="contained" onClick={() => {
                        this.fetchWorkers()
                    }}>Refresh Workers</Button>
                </Grid>
                <MaterialTable
                    title="Workers Status"
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
                        { title: 'Host', field: 'host', defaultSort: 'asc' },
                        { title: 'Worker Type', field: 'worker_type' },
                        { title: 'Connection Type', field: 'connection_type' },
                        { title: 'CPU%', field: 'cpu' },
                        { title: 'Memory%', field: 'memory' },
                        { title: 'Rsp Time', render: rowData => (rowData.response_time)/1000 },
                        { title: 'Last Checked', field: 'last_heard' },
                    ]}
                    data={ workers.workers }
                    options={{
                        sorting: true,
                        padding: "dense",
                        pageSize: 10,
                    }}
                    actions={[
                        {
                            icon: 'dns',
                            tooltip: 'Display Worker Status',
                            onClick: (event, rowData) => {
                                this.renderWorkersStatus(rowData.id)
                            }
                        },
                        {
                            icon: 'pageview',
                            tooltip: 'Capture packets for worker',
                            onClick: (event, rowData) => {
                                this.renderCapture(rowData.host)
                            },
                        },
                        {
                            icon: AccountTreeTwoToneIcon,
                            tooltip: 'Trace-route to worker',
                            onClick: (event, rowData) => {
                                this.renderTraceRouteDialog(rowData.host)
                            },
                        }
                    ]}
                />
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

export default Workers;
