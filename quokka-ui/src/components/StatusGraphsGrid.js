import {FlexibleXYPlot, HorizontalGridLines, LineMarkSeries, LineSeries, XAxis, YAxis} from 'react-vis'
import React, {Component} from "react";
import Grid from "@material-ui/core/Grid";
import Button from "@material-ui/core/Button";
import getStatusData from "./util"

class StatusGraphsGrid extends Component {

    constructor(props) {
        super(props);
        this.state = {
            isLoading: false,
        };
    }

    render() {

        let data = getStatusData("RSP_TIME", this.props.data);
        const tsRspTimeData = data.tsData;
        const maxYRspTime = data.maxY;
        data = getStatusData("AVAILABILITY", this.props.data);
        const tsAvailabilityData = data.tsData;
        let summaryData = getStatusData("RSP_TIME", this.props.summary);
        const summaryRspTimeData = summaryData.tsData;
        const summaryMaxYRspTime = summaryData.maxY;
        summaryData = getStatusData("AVAILABILITY_SUMMARY", this.props.summary);
        const summaryAvailabilityData = summaryData.tsData;

        return (
            <Grid container direction="row">
                <Grid item style={{width: '50%', padding: '10px'}}>
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
                                yDomain={[0,100]}>
                                <HorizontalGridLines />
                                <LineMarkSeries
                                    color="green"
                                    data={tsAvailabilityData} />
                                <XAxis title="Time of Day"/>
                                <YAxis title="Availability"/>
                            </FlexibleXYPlot>
                        </Grid>
                </Grid>
                <Grid item style={{width: '50%', padding: '10px'}}>
                    <Grid item>
                        <h5>Response Time: Summary</h5>
                        <FlexibleXYPlot
                            height={300}
                            xType="time"
                            yDomain={[0,summaryMaxYRspTime+(summaryMaxYRspTime/5)]}>
                            <HorizontalGridLines />
                            <LineSeries
                                data={summaryRspTimeData} />
                            <XAxis title="Time of Day"/>
                            <YAxis title="Response Time"/>
                        </FlexibleXYPlot>
                    </Grid>
                    <Grid item>
                        <h5>Availability: Summary</h5>
                        <FlexibleXYPlot
                            height={300}
                            xType="time"
                            yDomain={[0,100]}>
                            <HorizontalGridLines />
                            <LineMarkSeries
                                color="green"
                                data={summaryAvailabilityData} />
                            <XAxis title="Time of Day"/>
                            <YAxis title="Availability"/>
                        </FlexibleXYPlot>
                    </Grid>
                </Grid>
            </Grid>
         );
    }
}

export default StatusGraphsGrid;

