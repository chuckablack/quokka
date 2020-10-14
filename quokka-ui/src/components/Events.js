import React, {Component} from 'react';
import Button from '@material-ui/core/Button'
import CircularProgress from "@material-ui/core/CircularProgress";
import Grid from "@material-ui/core/Grid";
import 'typeface-roboto'
import Backdrop from "@material-ui/core/Backdrop";
import MaterialTable from "material-table";

class Events extends Component {

    constructor(props) {
        super(props);
        this.state = {
            events: {events: []},
            isLoading: false,
            dashboard: props.dashboard,
            countdownValue: process.env.REACT_APP_REFRESH_RATE,
        };
    }

    countdown() {
        this.setState({countdownValue: this.state.countdownValue-1})
        if (this.state.countdownValue === 0) {
            this.fetchEvents()
        }
    }

    fetchEvents() {

        this.setState({isLoading: true});
        let requestUrl = process.env.REACT_APP_QUOKKA_HOST + '/ui/events'
        fetch(requestUrl)
            .then(res => res.json())
            .then((data) => {
                console.log(data)
                this.setState({events: data, isLoading: false})
                this.setState({countdownValue: process.env.REACT_APP_REFRESH_RATE})
            })
            .catch((e) => {
                console.log(e)
                this.setState({countdownValue: process.env.REACT_APP_REFRESH_RATE})
            });
    }

    componentDidMount() {
        this.fetchEvents()
        this.interval = setInterval(() => this.countdown(), 1000)
    }

    componentWillUnmount() {
        clearInterval(this.interval)
    }

    render() {

        const {events, isLoading} = this.state;

        return (
            <div className="container" style={{maxWidth: "100%"}}>
                <link
                    rel="stylesheet"
                    href="https://fonts.googleapis.com/icon?family=Material+Icons"
                />
                <Grid container direction="row" justify="space-between" alignItems="center">
                    <h2>Events Table</h2>
                    {isLoading ?
                        <Backdrop open={true}>
                            <CircularProgress color="inherit" />
                        </Backdrop>
                        : ""}
                    <h6>Time until refresh: {this.state.countdownValue} seconds</h6>
                    <Button variant="contained" onClick={() => {
                        this.fetchEvents()
                    }}>Refresh Events</Button>
                </Grid>
                <MaterialTable
                    isLoading={this.state.isLoading}
                    title="Events Log"
                    columns={[
                        { title: 'Time', field: 'time', defaultSort: 'desc' },
                        { title: 'Severity', field: 'severity' },
                        { title: 'Source Type', field: 'source_type' },
                        { title: 'Source', field: 'source' },
                        { title: 'Info', field: 'info' },
                    ]}
                    data={ events.events }
                    options={{
                        sorting: true,
                        padding: "dense",
                        pageSize: 10,
                    }}
                />
            </div>
        );
    }
}

export default Events;
