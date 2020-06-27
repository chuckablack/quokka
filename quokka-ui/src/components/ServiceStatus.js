import {FlexibleXYPlot, HorizontalGridLines, LineMarkSeries, LineSeries, XAxis, YAxis} from 'react-vis'
import React, {Component} from "react";
import Grid from "@material-ui/core/Grid";
import Button from "@material-ui/core/Button";

class ServiceStatus extends Component {

    constructor(props) {
        super(props);
        this.state = {
            serviceData: {service_data: [], service: {},},
            isLoading: false,
            dashboard: props.dashboard,
            serviceId: props.serviceId,
        };

    }

    componentDidMount() {
        this.fetchServiceTsData()
        this.interval = setInterval(() => this.fetchServiceTsData(), 6000)
    }

    componentWillUnmount() {
        clearInterval(this.interval)
    }

    fetchServiceTsData() {

        const serviceId = this.state.serviceId;

        this.setState({isLoading: true});
        let requestUrl = 'http://' + process.env.REACT_APP_QUOKKA_HOST + ':5000/service/ts?serviceid=' + serviceId + '&datapoints=24'

        fetch(requestUrl)
            .then(res => res.json())
            .then((data) => {
                 this.setState({serviceData: data, isLoading: false});
            })
            .catch(console.log);

    }

    getTSData(measurement) {

        let tsData = [];
        let maxY = 0;
        let yValue = 0;
        const serviceData = this.state.serviceData.service_data;
        console.log(serviceData);

        for (let i = 0; i < serviceData.length; i++) {

            if (measurement === "RSP_TIME") {
                yValue = (serviceData[i].response_time)/1000;
            } else if (measurement === "AVAILABILITY") {
                yValue = serviceData[i].availability ? 100 : 0;
            }
            else {
                yValue = 0;
            }

            const tsDataItem = {x: new Date(serviceData[i].timestamp), y: yValue};
            tsData.push(tsDataItem);
            if (tsDataItem.y > maxY) {
                maxY = tsDataItem.y;
            }
        }

        console.log(tsData)
        return {tsData: tsData, maxY: maxY};
    }

    renderServices(dashboard) {
        dashboard.setState({show: "services"})
    }

    render() {

        let data = this.getTSData("RSP_TIME");
        const tsRspTimeData = data.tsData;
        const maxYRspTime = data.maxY;
        data = this.getTSData("AVAILABILITY");
        const tsAvailabilityData = data.tsData;
        const maxYAvailability = data.maxY;
        return (
            <Grid container direction="column">
                <Grid container direction="row" style={{paddingTop: '10px'}}>
                    <Grid item style={{width: '25%', paddingLeft: '10px'}}>
                        <b>SERVICE NAME</b>:<br />{this.state.serviceData.service.name}
                        <br /><br />
                        <b>TARGET</b>:<br />{this.state.serviceData.service.target}
                        <br /><br />
                        <b>DATA</b>:<br />{this.state.serviceData.service.data}
                        <br /><br />
                        <b>LAST HEARD</b>:<br />{this.state.serviceData.service.last_heard}
                        <br /><br />  <br /><br />
                        <Button variant="contained" onClick={() => this.renderServices(this.state.dashboard)}>Return to Services</Button>
                    </Grid>
                    <Grid item style={{width: '75%', paddingRight: '10px'}}>
                        <h5>Response Time</h5>
                        <Grid item>
                            <FlexibleXYPlot
                                height={300}
                                xType="time"
                                yDomain={[0,maxYRspTime+(maxYRspTime/5)]}>
                                <HorizontalGridLines />
                                <LineSeries
                                    data={tsRspTimeData} />
                                <XAxis title="Time of Day"/>
                                <YAxis title="Response Time"/>
                            </FlexibleXYPlot>
                        </Grid>
                        <Grid item>
                            <h5>Availability</h5>
                            <FlexibleXYPlot
                                height={300}
                                xType="time"
                                yDomain={[0,maxYAvailability]}>
                                <HorizontalGridLines />
                                <LineMarkSeries
                                    color="green"
                                    data={tsAvailabilityData} />
                                <XAxis title="Time of Day"/>
                                <YAxis title="Availability"/>
                            </FlexibleXYPlot>
                        </Grid>
                    </Grid>
                </Grid>
            </Grid>
        );
    }
}

export default ServiceStatus

