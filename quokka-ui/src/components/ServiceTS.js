import {FlexibleXYPlot, HorizontalGridLines, LineSeries, VerticalBarSeries, XAxis, YAxis} from 'react-vis'
import React, {Component} from "react";

class ServiceTS extends Component {

    constructor(props) {
        super(props);
        this.state = {
            serviceData: {service_data: []},
            isLoading: false,
            dashboard: props.dashboard,
            serviceId: props.serviceId,
        };

    }

    componentDidMount() {
        this.fetchServiceTsData()
    }

    fetchServiceTsData() {

        const serviceId = this.state.serviceId;

        this.setState({isLoading: true});
        let requestUrl = 'http://127.0.0.1:5000/service/ts?serviceid=' + serviceId + '&datapoints=24'

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
                yValue = serviceData[i].response_time;
            } else if (measurement === "AVAILABILITY") {
                yValue = serviceData[i].availability ? 100 : 0;
            }
            else {
                const yValue = 0;
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

    render() {

        let data = this.getTSData("RSP_TIME");
        const tsRspTimeData = data.tsData;
        const maxYRspTime = data.maxY;
        data = this.getTSData("AVAILABILITY");
        const tsAvailabilityData = data.tsData;
        const maxYAvailability = data.maxY;
        return (
            <div className="container">
                <h5>Response Time</h5>
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
                <h5>Availability</h5>
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

export default ServiceTS

