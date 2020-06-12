import {FlexibleXYPlot, HorizontalGridLines, LineSeries, XAxis, YAxis} from 'react-vis'
import React, {Component} from "react";
import Grid from "@material-ui/core/Grid";

class DeviceTS extends Component {

    constructor(props) {
        super(props);
        this.state = {
            deviceName: props.deviceName,
            deviceData: {device_data: []},
            data: [],
            isLoading: false,
            dashboard: props.dashboard,
        };

    }

    componentDidMount() {
        this.fetchDeviceTsData()
        this.interval = setInterval(() => this.fetchDeviceTsData(), 60000)
    }

    componentWillUnmount() {
        clearInterval(this.interval)
    }

    fetchDeviceTsData() {

        const deviceName = this.state.deviceName;

        this.setState({isLoading: true});
        let requestUrl = 'http://127.0.0.1:5000/device/ts?device=' + deviceName + '&datapoints=24'

        fetch(requestUrl)
            .then(res => res.json())
            .then((data) => {
                 this.setState({deviceData: data, isLoading: false});
            })
            .catch(console.log);

    }

    getTSData(measurement) {

        let tsData = [];
        let maxY = 0;
        let yValue = 0;
        const deviceData = this.state.deviceData.device_data;
        console.log(deviceData);

        for (let i = 0; i < deviceData.length; i++) {

            if (measurement === "RSP_TIME") {
                yValue = deviceData[i].response_time;
            } else if (measurement === "AVAILABILITY") {
                yValue = deviceData[i].availability ? 100 : 0;
            } else if (measurement === "CPU") {
                yValue = deviceData[i].cpu;
            } else if (measurement === "MEMORY") {
                yValue = deviceData[i].memory;
            }
            else {
                yValue = 0;
            }

            const tsDataItem = {x: new Date(deviceData[i].timestamp), y: yValue};
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
        data = this.getTSData("CPU");
        const tsCpuData = data.tsData;
        const maxYCpu = data.maxY;
        data = this.getTSData("MEMORY");
        const tsMemoryData = data.tsData;
        const maxYMemory = data.maxY;
        return (
            <div className="container">
                <Grid container direction="row" style={{paddingTop: "10px"}}>
                    <Grid item style={{width: '50%'}}>
                        <Grid item>
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
                        </Grid>
                        <Grid item>
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
                        </Grid>
                    </Grid>
                    <Grid item style={{width: '50%'}}>
                        <Grid item>
                            <h5>CPU Utilization</h5>
                            <FlexibleXYPlot
                                height={300}
                                xType="time"
                                yDomain={[0,maxYCpu+(maxYCpu/5)]}>
                                <HorizontalGridLines />
                                <LineSeries
                                    data = {tsCpuData} />
                                <XAxis title="Time of Day"/>
                                <YAxis title="Cpu"/>
                            </FlexibleXYPlot>
                        </Grid>
                        <Grid item>
                            <h5>Memory Utilization</h5>
                            <FlexibleXYPlot
                                height={300}
                                xType="time"
                                yDomain={[0,maxYMemory+(maxYMemory/5)]}>
                                <HorizontalGridLines />
                                <LineSeries
                                    data = {tsMemoryData} />
                                <XAxis title="Time of Day"/>
                                <YAxis title="Memory"/>
                            </FlexibleXYPlot>
                        </Grid>
                    </Grid>
                </Grid>
            </div>
        );
    }
}

export default DeviceTS

