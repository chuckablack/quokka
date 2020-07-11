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
        };
    }

    fetchEvents() {

        this.setState({isLoading: true});
        let requestUrl = 'http://' + process.env.REACT_APP_QUOKKA_HOST + ':5000/events'
        fetch(requestUrl)
            .then(res => res.json())
            .then((data) => {
                this.setState({events: data, isLoading: false})
                console.log(this.state.events)
            })
            .catch(console.log)
    }

    componentDidMount() {
        this.fetchEvents()
        this.interval = setInterval(() => this.fetchEvents(), 60000)
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
