import {FlexibleXYPlot, HorizontalGridLines, LineMarkSeries, LineSeries, XAxis, YAxis} from 'react-vis'
import React, {Component} from "react";
import Grid from "@material-ui/core/Grid";
import Button from "@material-ui/core/Button";

class WorkerStatus extends Component {

    constructor(props) {
        super(props);
        this.state = {
            workerId: props.workerId,
            workerData: {worker_data: [], worker: {}},
            dashboard: props.dashboard,
            countdownValue: process.env.REACT_APP_REFRESH_RATE,
        };

    }

    countdown() {
        this.setState({countdownValue: this.state.countdownValue-1})
        if (this.state.countdownValue === 0) {
            this.fetchWorkerStatusData()
        }
    }

    componentDidMount() {
        this.fetchWorkerStatusData()
        this.interval = setInterval(() => this.countdown(), 1000)
    }

    componentWillUnmount() {
        clearInterval(this.interval)
    }

    fetchWorkerStatusData() {

        const workerId = this.state.workerId;

        let requestUrl = process.env.REACT_APP_QUOKKA_HOST + '/ui/worker/status?workerid='
                                   + workerId + '&datapoints=' + process.env.REACT_APP_NUM_DATAPOINTS

        fetch(requestUrl)
            .then(res => res.json())
            .then((data) => {
                console.log(data)
                this.setState({workerData: data});
                this.setState({countdownValue: process.env.REACT_APP_REFRESH_RATE})
            })
            .catch((e) => {
                console.log(e)
                this.setState({countdownValue: process.env.REACT_APP_REFRESH_RATE})
            });

    }

    getTSData(measurement) {

        let tsData = [];
        let maxY = 0;
        let yValue = 0;
        const workerData = this.state.workerData.worker_data;

        for (let i = 0; i < workerData.length; i++) {

            if (measurement === "RSP_TIME") {
                yValue = (workerData[i].response_time)/1000;
            } else if (measurement === "AVAILABILITY") {
                yValue = workerData[i].availability ? 100 : 0;
            } else if (measurement === "CPU") {
                yValue = workerData[i].cpu;
            } else if (measurement === "MEMORY") {
                yValue = workerData[i].memory;
            }
            else {
                yValue = 0;
            }

            const tsDataItem = {x: new Date(workerData[i].timestamp), y: yValue};
            tsData.push(tsDataItem);
            if (tsDataItem.y > maxY) {
                maxY = tsDataItem.y;
            }
        }

        // console.log(tsData)
        return {tsData: tsData, maxY: maxY};
    }

    renderWorkers(dashboard) {
        dashboard.setState({show: "workers"})
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
            <Grid container direction="column">
                <Grid container direction="row" style={{paddingTop: '10px'}}>
                    <Grid item style={{width: '15%', paddingLeft: '10px'}}>
                        <b>WORKER NAME</b>:<br />{this.state.workerData.worker.name}
                        <br /><br />
                        <b>Host</b>:<br />{this.state.workerData.worker.host}
                        <br /><br />
                        <b>Worker Type</b>:<br />{this.state.workerData.worker.worker_type}
                        <br /><br />
                        <b>Last heard</b>:<br />{this.state.workerData.worker.last_heard}
                        <br /><br />  <br /><br />
                        <b>REFRESH IN</b>:<br/>{this.state.countdownValue} seconds
                        <br/><br/> <br/><br/>
                        <Button variant="contained" style={{width: '100%'}} onClick={() => this.renderWorkers(this.state.dashboard)}>Return to Workers</Button>
                    </Grid>
                    <Grid item style={{width: '85%', paddingRight: '10px'}}>
                        <h6 align='right'>Time until refresh: {this.state.countdownValue} seconds</h6>
                        <Grid container direction="row">
                            <Grid item style={{width: '50%'}}>
                                <Grid item>
                                    <h5>Response Time</h5>
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
                            <Grid item style={{width: '50%'}}>
                                <Grid item>
                                    <h5>CPU Utilization</h5>
                                    <FlexibleXYPlot
                                        height={300}
                                        xType="time"
                                        yDomain={[0,100]}>
                                        <HorizontalGridLines />
                                        <LineSeries
                                            data={tsCpuData} />
                                        <XAxis title="Time of Day"/>
                                        <YAxis title="CPU"/>
                                    </FlexibleXYPlot>
                                </Grid>
                                <Grid item>
                                    <h5>Memory Utilization</h5>
                                    <FlexibleXYPlot
                                        height={300}
                                        xType="time"
                                        yDomain={[0,100]}>
                                        <HorizontalGridLines />
                                        <LineSeries
                                            data={tsMemoryData} />
                                        <XAxis title="Time of Day"/>
                                        <YAxis title="Memory"/>
                                    </FlexibleXYPlot>
                                </Grid>
                            </Grid>
                        </Grid>
                    </Grid>
                </Grid>
            </Grid>
        );
    }
}

export default WorkerStatus

