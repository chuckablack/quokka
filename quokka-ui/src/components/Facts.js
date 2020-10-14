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

class Facts extends Component {

    constructor(props) {
        super(props);
        this.state = {
            deviceName: props.deviceName,
            facts: {facts: {}},
            isLoading: false,
        };
    }

    fetchFacts(getLive) {
        const deviceName = this.state.deviceName

        this.setState({isLoading: true});
        let requestUrl = process.env.REACT_APP_QUOKKA_HOST + '/ui/device?device=' + deviceName + '&info=facts'
        if (getLive) {
            requestUrl += '&live=true'
        }
        fetch(requestUrl)
            .then(res => res.json())
            .then((data) => {
                this.setState({facts: data, isLoading: false})
                console.log(this.state.facts)
            })
            .catch(console.log)
    }

    componentDidMount() {
        this.fetchFacts(false)
    }

    render() {

        const {facts, isLoading} = this.state;

        return (
            <div className="container">
                <Grid container direction="row" justify="space-between" alignItems="center">
                    <h2>Facts</h2>
                    {isLoading ?
                        <Backdrop open={true}>
                            <CircularProgress color="inherit" />
                        </Backdrop>
                        : ""}
                    <Button variant="contained" onClick={() => {this.fetchFacts(true)}}>Refresh Facts Live</Button>
                </Grid>
                <Table size="small">
                    <TableBody>
                    <TableRow>
                        <TableCell style={{ fontWeight:'bold' }}>FQDN</TableCell>
                        <TableCell>{facts.facts.fqdn}</TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell style={{ fontWeight:'bold' }}>Hostname</TableCell>
                        <TableCell>{facts.facts.hostname}</TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell style={{ fontWeight:'bold' }}>Model</TableCell>
                        <TableCell>{facts.facts.model}</TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell style={{ fontWeight:'bold' }}>OS Version</TableCell>
                        <TableCell>{facts.facts.os_version}</TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell style={{ fontWeight:'bold' }}>Serial</TableCell>
                        <TableCell>{facts.facts.serial_number}</TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell style={{ fontWeight:'bold' }}>Vendor</TableCell>
                        <TableCell>{facts.facts.vendor}</TableCell>
                    </TableRow>
                        <TableRow>
                            <TableCell style={{ fontWeight:'bold' }}>Uptime</TableCell>
                            <TableCell>{facts.facts.uptime}</TableCell>
                        </TableRow>
                    </TableBody>
                </Table>
            </div>
        );
    }
}

export default Facts;
