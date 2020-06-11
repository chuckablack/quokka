import {FlexibleXYPlot, HorizontalGridLines, LineSeries, XAxis, YAxis} from 'react-vis'
import React, {Component} from "react";

class Vis extends Component {

    constructor(props) {
        super(props);
        this.state = {
            hostData: {host_data: []},
            data: [],
            isLoading: false,
            dashboard: props.dashboard,
        };

    }

    componentDidMount() {
        this.fetchHostTsData()
    }

    fetchHostTsData() {

        this.setState({isLoading: true});
        let requestUrl = 'http://127.0.0.1:5000/hosts/ts?hostid=1&datapoints=24'

        fetch(requestUrl)
            .then(res => res.json())
            .then((data) => {
                 this.setState({hostData: data, isLoading: false});
            })
            .catch(console.log);

        // const host_data = state.hostData.host_data;
        //
        // this.setState({data:ts_data});

        // this.state.hostData.host_data.map(host_data => (
        //     console.log(ts_data)
        // ))
    }

    getTsData() {

        let ts_data = [];
        const host_data = this.state.hostData.host_data;
        console.log(host_data);

        for (let i = 0; i < host_data.length; i++) {
            const ts_data_item = {x: new Date(host_data[i].timestamp), y: host_data[i].response_time};
            ts_data.push(ts_data_item);
        }

        console.log(ts_data)
        return ts_data;
    }

    render() {

        let ts_data = this.getTsData();
        return (
            <FlexibleXYPlot
                // width={300}
                height={300}
                xType="time"
                yDomain={[0,2000]}>
                <HorizontalGridLines />
                <LineSeries
                    data = {ts_data} />
                <XAxis title="Time of Day"/>
                <YAxis title="Response Time"/>
            </FlexibleXYPlot>
        );
    }
}

export default Vis

