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

class Services extends Component {

    constructor(props) {
        super(props);
        this.state = {
            services: {services: []},
            dashboard: props.dashboard,
            countdownValue: process.env.REACT_APP_REFRESH_RATE,
        };
    }

    countdown() {
        this.setState({countdownValue: this.state.countdownValue-1})
        if (this.state.countdownValue === 0) {
            this.fetchServices()
        }
    }

    fetchServices() {

        let requestUrl = 'http://' + process.env.REACT_APP_QUOKKA_HOST + ':5000/ui/services'
        fetch(requestUrl)
            .then(res => res.json())
            .then((data) => {
                this.setState({services: data})
                console.log(this.state.services)
                this.setState({countdownValue: process.env.REACT_APP_REFRESH_RATE})
            })
            .catch((e) => {
                console.log(e)
                this.setState({countdownValue: process.env.REACT_APP_REFRESH_RATE})
            });
    }

    componentDidMount() {
        this.fetchServices()
        this.interval = setInterval(() => this.countdown(), 1000)
    }

    componentWillUnmount() {
        clearInterval(this.interval)
    }

    renderServiceTS(serviceId) {
        this.state.dashboard.setState({serviceId: serviceId, show: "servicestatus"})
    }

    renderCapture(protocol) {
        this.state.dashboard.setState({ip: null, protocol: protocol, port: null, show: "capture"})
    }

    render() {

        const {services} = this.state;

        return (
            <div className="container" style={{maxWidth: "100%"}}>
                <link
                    rel="stylesheet"
                    href="https://fonts.googleapis.com/icon?family=Material+Icons"
                />
                <Grid container direction="row" justify="space-between" alignItems="center">
                    <h2>Services Table</h2>
                    <h6>Time until refresh: {this.state.countdownValue} seconds</h6>
                    <Button variant="contained" onClick={() => {
                        this.fetchServices()
                    }}>Refresh Services</Button>
                </Grid>
                <MaterialTable
                    title="Services Availability and Response Time"
                    columns={[
                        {
                            title: 'Availability',
                            field: 'availability',
                            headerStyle: {textAlign: 'right'},
                            cellStyle: {textAlign: 'center'},
                            render: rowData =>
                                rowData.availability ?
                                    <CheckCircleIcon style={{color: green[500]}}/>
                                    : <CancelIcon style={{color: red[500]}}/>

                        },
                        { title: 'Name', field: 'name', defaultSort: 'asc' },
                        { title: 'Type', field: 'type' },
                        { title: 'Target', field: 'target' },
                        { title: 'Data', field: 'data' },
                        { title: 'Rsp Time', field: 'response_time' },
                        { title: 'Last Heard', field: 'last_heard' },
                    ]}
                    data={ services.services }
                    options={{
                        sorting: true,
                        padding: "dense",
                        pageSize: 10,
                    }}
                    actions={[
                        {
                            icon: 'poll',
                            tooltip: 'Display Time-Series for Service',
                            onClick: (event, rowData) => {
                                this.renderServiceTS(rowData.id)
                            }
                        },
                        {
                            icon: 'pageview',
                            tooltip: 'Capture packets for service',
                            onClick: (event, rowData) => {
                                this.renderCapture(rowData.type)
                            }
                        }
                    ]}
                />
            </div>
        );
    }
}

export default Services;
