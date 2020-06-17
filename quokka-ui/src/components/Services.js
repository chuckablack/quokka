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
            isLoading: false,
            dashboard: props.dashboard,
        };
    }

    fetchServices() {

        this.setState({isLoading: true});
        let requestUrl = 'http://127.0.0.1:5000/services'
        fetch(requestUrl)
            .then(res => res.json())
            .then((data) => {
                this.setState({services: data, isLoading: false})
                console.log(this.state.services)
            })
            .catch(console.log)
    }

    componentDidMount() {
        this.fetchServices()
        this.interval = setInterval(() => this.fetchServices(), 300000)
    }

    componentWillUnmount() {
        clearInterval(this.interval)
    }

    renderServiceTS(serviceId) {
        this.state.dashboard.setState({serviceId: serviceId, show: "servicestatus"})
    }

    render() {

        const {services, isLoading} = this.state;

        return (
            <div className="container" style={{maxWidth: "100%"}}>
                <link
                    rel="stylesheet"
                    href="https://fonts.googleapis.com/icon?family=Material+Icons"
                />
                <Grid container direction="row" justify="space-between" alignItems="center">
                    <h2>Services Table</h2>
                    {isLoading ?
                        <Backdrop open={true}>
                            <CircularProgress color="inherit" />
                        </Backdrop>
                        : ""}
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
                            render: rowData =>
                                rowData.availability ?
                                    <CheckCircleIcon style={{color: green[500]}}/>
                                    : <CancelIcon style={{color: red[500]}}/>

                        },
                        { title: 'Name', field: 'name' },
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
                        }
                    ]}
                />
            </div>
        );
    }
}

export default Services;
