import React, {Component} from 'react';
import Button from '@material-ui/core/Button'
import CircularProgress from "@material-ui/core/CircularProgress";
import Grid from "@material-ui/core/Grid";
import Table from '@material-ui/core/Table'
import TableBody from '@material-ui/core/TableBody'
import TableRow from '@material-ui/core/TableRow'
import TableCell from '@material-ui/core/TableCell'
import TableHead from '@material-ui/core/TableHead'
import 'typeface-roboto'
import Backdrop from "@material-ui/core/Backdrop";

class Config extends Component {

    constructor(props) {
        super(props);
        this.state = {
            deviceName: props.deviceName,
            config: "",
            isLoading: false,
        };
    }

    fetchConfig() {
        this.setState({isLoading: true});
        const deviceName = this.state.deviceName
        fetch('http://127.0.0.1:5000/device?device=' + deviceName + '&info=config')
            .then(res => res.json())
            .then((data) => {
                this.setState({
                    config: data.config.running.split('\n').map((item, i) => {
                        return <li key={i}>{item}</li>;
                    }), isLoading: false
                })
                console.log(this.state.config)
            })
            .catch(console.log)
    }

    componentDidMount() {
        this.fetchConfig()
    }

    render() {

        const {config, isLoading} = this.state;

        return (
            <div className="container">
                <Grid container direction="row" justify="space-between" alignItems="center">
                    <h1>Configuration</h1>
                    {isLoading ?
                        <Backdrop open={true}>
                            <CircularProgress color="inherit"/>
                        </Backdrop>
                        : ""}
                    <Button variant="contained" onClick={() => {
                        this.fetchConfig()
                    }}>Refresh Config</Button>
                </Grid>
                <p>Here is the running configuration:</p>
                <ul style={{listStyleType:"none"}}>{config}</ul>
            </div>
        );
    }
}

export default Config;
