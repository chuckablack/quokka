import {FlexibleXYPlot, HorizontalGridLines, LineSeries, VerticalBarSeries, XAxis, YAxis} from 'react-vis'
import React, {Component} from "react";

class HostTS extends Component {

    constructor(props) {
        super(props);
        this.state = {
            hostData: {host_data: []},
            isLoading: false,
            dashboard: props.dashboard,
            hostId: props.hostId,
        };

    }

    componentDidMount() {
        this.fetchHostTsData()
    }

    fetchHostTsData() {

        const hostId = this.state.hostId;

        this.setState({isLoading: true});
        let requestUrl = 'http://127.0.0.1:5000/host/ts?hostid=' + hostId + '&datapoints=24'

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
                yValue = hostData[i].response_time;
            } else if (measurement === "AVAILABILITY") {
                yValue = hostData[i].availability ? 100 : 0;
            }
            else {
                const yValue = 0;
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

    render() {

        let data = this.getTSData("RSP_TIME");
        const tsRspTimeData = data.tsData;
        const maxYRspTime = data.maxY;
        data = this.getTSData("AVAILABILITY");
        const tsAvailabilityData = data.tsData;
        const maxYAvailability = data.maxY;
        return (
            <div className="container">
                <h2>Host Time Series Data: Response Time</h2>
                <FlexibleXYPlot
                    height={300}
                    xType="time"
                    yDomain={[0,maxYRspTime+(maxYRspTime/5)]}>
                    <HorizontalGridLines />
                    <LineSeries
                        data = {tsRspTimeData} />
                    <XAxis title="Time of Day"/>
                    <YAxis title="Response Time"/>
                </FlexibleXYPlot>
                <h2>Host Time Series Data: Availability</h2>
                <FlexibleXYPlot
                    height={300}
                    xType="time"
                    yDomain={[0,maxYAvailability]}>
                    <HorizontalGridLines />
                    <LineSeries
                        data = {tsAvailabilityData} />
                    <XAxis title="Time of Day"/>
                    <YAxis title="Availability"/>
                </FlexibleXYPlot>
            </div>
        );
    }
}

export default HostTS

