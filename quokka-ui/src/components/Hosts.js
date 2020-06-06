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

    render() {

        const {hosts, isLoading} = this.state;

        return (
            <div className="container">
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
                <Table size="small">
                    <TableHead>
                        <TableRow>
                            <TableCell align="center">Availability</TableCell>
                            <TableCell>Name</TableCell>
                            <TableCell>IP Address</TableCell>
                            <TableCell>MAC Address</TableCell>
                            <TableCell align="right">Rsp Time (msec)</TableCell>
                            <TableCell>Last Heard</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {hosts.hosts.map((host) => (
                            <TableRow key={host.name}>
                                <TableCell align="center">{host.availability ?
                                    <CheckCircleIcon style={{color: green[500]}}/>
                                    : <CancelIcon  style={{color: red[500]}}/>
                                }</TableCell>
                                <TableCell >{host.name}</TableCell>
                                <TableCell>{host.ip_address}</TableCell>
                                <TableCell>{host.mac_address}</TableCell>
                                <TableCell align="right">{host.response_time}</TableCell>
                                <TableCell>{host.last_heard}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </div>
        );
    }
}

export default Hosts;
