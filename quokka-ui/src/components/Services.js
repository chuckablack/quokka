import React, {Component} from 'react';
import Button from '@material-ui/core/Button'
import CircularProgress from "@material-ui/core/CircularProgress";
import Grid from "@material-ui/core/Grid";
import Table from '@material-ui/core/Table'
import TableBody from '@material-ui/core/TableBody'
import TableRow from '@material-ui/core/TableRow'
import TableCell from '@material-ui/core/TableCell'
import 'typeface-roboto'
import Backdrop from "@material-ui/core/Backdrop";
import TableHead from "@material-ui/core/TableHead";
import CheckCircleIcon from '@material-ui/icons/CheckCircle';
import CancelIcon from '@material-ui/icons/Cancel';
import { green, red } from '@material-ui/core/colors';

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

    render() {

        const {services, isLoading} = this.state;

        return (
            <div className="container">
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
                <Table size="small">
                    <TableHead>
                        <TableRow>
                            <TableCell align="center">Availability</TableCell>
                            <TableCell>Name</TableCell>
                            <TableCell>Type</TableCell>
                            <TableCell>Target</TableCell>
                            <TableCell>Data</TableCell>
                            <TableCell align="right">Rsp Time (msec)</TableCell>
                            <TableCell>Last Heard</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {services.services.map((service) => (
                            <TableRow key={service.name}>
                                <TableCell align="center">{service.availability ?
                                    <CheckCircleIcon style={{color: green[500]}}/>
                                    : <CancelIcon  style={{color: red[500]}}/>
                                }</TableCell>
                                <TableCell >{service.name}</TableCell>
                                <TableCell >{service.type}</TableCell>
                                <TableCell >{service.target}</TableCell>
                                <TableCell >{service.data}</TableCell>
                                <TableCell align="right">{service.response_time}</TableCell>
                                <TableCell>{service.last_heard}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </div>
        );
    }
}

export default Services;
