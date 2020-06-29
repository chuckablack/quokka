import {
    FlexibleXYPlot,
    LineMarkSeries,
    LineSeries,
    HorizontalGridLines,
    XAxis,
    YAxis
} from 'react-vis'
import React, {Component} from "react";
import Grid from "@material-ui/core/Grid";
import Button from "@material-ui/core/Button";

class HostStatus extends Component {

    constructor(props) {
        super(props);
        this.state = {
            hostData: {host_data: [], host: {},},
            isLoading: false,
            dashboard: props.dashboard,
            hostId: props.hostId,
        };

    }

    componentDidMount() {
        this.fetchHostTsData()
        this.interval = setInterval(() => this.fetchHostTsData(), 60000)
    }

    componentWillUnmount() {
        clearInterval(this.interval)
    }

    fetchHostTsData() {

        const hostId = this.state.hostId;

        this.setState({isLoading: true});
        let requestUrl = 'http://' + process.env.REACT_APP_QUOKKA_HOST + ':5000/host/ts?hostid=' + hostId + '&datapoints=24'

        fetch(requestUrl)
            .then(res => res.json())
            .then((data) => {
                 this.setState({hostData: data, isLoading: false});
            })
            .catch(console.log);

    }

    getTSData(measurement) {

        let tsData = [];
        let maxY = 0;
        let yValue = 0;
        const hostData = this.state.hostData.host_data;
        console.log(hostData);

        for (let i = 0; i < hostData.length; i++) {

            if (measurement === "RSP_TIME") {
                yValue = (hostData[i].response_time)/1000;
            } else if (measurement === "AVAILABILITY") {
                yValue = hostData[i].availability ? 100 : 0;
            }
            else {
                yValue = 0;
            }

            const tsDataItem = {x: new Date(hostData[i].timestamp), y: yValue};
            tsData.push(tsDataItem);
            if (tsDataItem.y > maxY) {
                maxY = tsDataItem.y;
            }
        }

        console.log(tsData)
        return {tsData: tsData, maxY: maxY};
    }

    renderHosts(dashboard) {
        dashboard.setState({show: "hosts"})
    }

    render() {

        let data = this.getTSData("RSP_TIME");
        const tsRspTimeData = data.tsData;
        const maxYRspTime = data.maxY;
        data = this.getTSData("AVAILABILITY");
        const tsAvailabilityData = data.tsData;
        const maxYAvailability = data.maxY;
        return (
                <Grid container direction="row">
                    <Grid item style={{width: '15%', padding: '10px'}}>
                        <b>HOST NAME</b>:<br />{this.state.hostData.host.name}
                        <br /><br />
                        <b>IP address</b>:<br />{this.state.hostData.host.ip_address}
                        <br /><br />
                        <b>MAC address</b>:<br />{this.state.hostData.host.mac_address}
                        <br /><br />
                        <b>Last heard</b>:<br />{this.state.hostData.host.last_heard}
                        <br /><br />  <br /><br />
                        <Button variant="contained" onClick={() => this.renderHosts(this.state.dashboard)}>Return to Hosts</Button>
                    </Grid>
                    <Grid item style={{width: '85%', padding: '10px'}}>
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
        );
    }
}

export default HostStatus

