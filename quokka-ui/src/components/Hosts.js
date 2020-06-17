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

class Hosts extends Component {

    constructor(props) {
        super(props);
        this.state = {
            hosts: {hosts: []},
            isLoading: false,
            dashboard: props.dashboard,
        };
    }

    fetchHosts() {

        this.setState({isLoading: true});
        let requestUrl = 'http://127.0.0.1:5000/hosts'
        fetch(requestUrl)
            .then(res => res.json())
            .then((data) => {
                this.setState({hosts: data, isLoading: false})
                console.log(this.state.hosts)
            })
            .catch(console.log)
    }

    componentDidMount() {
        this.fetchHosts()
        this.interval = setInterval(() => this.fetchHosts(), 300000)
    }

    componentWillUnmount() {
        clearInterval(this.interval)
    }

    renderHostTS(hostId) {
        this.state.dashboard.setState({hostId: hostId, show: "hoststatus"})
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
                        },
                        { title: 'Name', field: 'name' },
                        { title: 'IP Address', field: 'ip_address' },
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
                        }
                    ]}

                />
            </div>
        );
    }
}

export default Hosts;
