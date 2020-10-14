import React, {Component} from "react";
import Grid from "@material-ui/core/Grid";
import Button from "@material-ui/core/Button";
import StatusGraphsGrid from "./StatusGraphsGrid";

class ServiceStatus extends Component {

    constructor(props) {
        super(props);
        this.state = {
            serviceData: {service_data: [], service_summary: [], service: {},},
            isLoading: false,
            dashboard: props.dashboard,
            serviceId: props.serviceId,
            countdownValue: process.env.REACT_APP_REFRESH_RATE,
        };
    }

    countdown() {
        this.setState({countdownValue: this.state.countdownValue-1})
        if (this.state.countdownValue === 0) {
            this.fetchServiceStatusData()
        }
    }

    componentDidMount() {
        this.fetchServiceStatusData()
        this.interval = setInterval(() => this.countdown(), 1000)
    }

    componentWillUnmount() {
        clearInterval(this.interval)
    }

    fetchServiceStatusData() {

        const serviceId = this.state.serviceId;

        this.setState({isLoading: true});
        let requestUrl = process.env.REACT_APP_QUOKKA_HOST + '/ui/service/status?serviceid='
                                   + serviceId + '&datapoints=' + process.env.REACT_APP_NUM_DATAPOINTS

        fetch(requestUrl)
            .then(res => res.json())
            .then((data) => {
                console.log(data)
                this.setState({serviceData: data, isLoading: false});
                this.setState({countdownValue: process.env.REACT_APP_REFRESH_RATE})
            })
            .catch((e) => {
                console.log(e)
                this.setState({countdownValue: process.env.REACT_APP_REFRESH_RATE})
            });
    }

    renderServices(dashboard) {
        dashboard.setState({show: "services"})
    }

    render() {

        return (
            <Grid container direction="column">
                <Grid container direction="row" style={{paddingTop: '10px'}}>
                    <Grid item style={{width: '15%', paddingLeft: '10px'}}>
                        <b>SERVICE NAME</b>:<br/>{this.state.serviceData.service.name}
                        <br/><br/>
                        <b>TARGET</b>:<br/>{this.state.serviceData.service.target}
                        <br/><br/>
                        <b>DATA</b>:<br/>{this.state.serviceData.service.data}
                        <br/><br/>
                        <b>LAST HEARD</b>:<br/>{this.state.serviceData.service.last_heard}
                        <br/><br/> <br/><br/>
                        <b>REFRESH IN</b>:<br/>{this.state.countdownValue} seconds
                        <br/><br/> <br/><br/>
                        <Button variant="contained" style={{width: '100%'}} onClick={() => this.renderServices(this.state.dashboard)}>Return to
                            Services</Button>
                    </Grid>

                    <Grid item style={{width: '85%', paddingRight: '10px'}}>
                        <StatusGraphsGrid
                            data={this.state.serviceData.service_data}
                            summary={this.state.serviceData.service_summary}
                            sla={{availability: this.state.serviceData.service.sla_availability,
                                  response_time: this.state.serviceData.service.sla_response_time}}>
                        </StatusGraphsGrid>
                    </Grid>

                </Grid>
            </Grid>
        );
    }
}

export default ServiceStatus

