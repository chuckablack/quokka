import React, {Component} from "react";
import Grid from "@material-ui/core/Grid";
import Button from "@material-ui/core/Button";
import Facts from "./Facts";
import Arp from "./Arp";
import Counters from "./Counters";
import Config from "./Config";
import DeviceStatus from "./DeviceStatus";

class DeviceDashboard extends Component {

    constructor(props) {
        super(props);
        this.state = {
            deviceName: props.deviceName,
            dashboard: props.dashboard,
            show: "status"
        };

    }

    renderDevices(dashboard) {
        dashboard.setState({show: "devices"})
    }

    renderCompliance(dashboard) {
        dashboard.setState({show: "compliance"})
    }

    render() {
        const {show, deviceName} = this.state;

        let info;
        if (show === "facts") {
            info = <Facts deviceName={deviceName}/>;
        } else if (show === "arp") {
            info = <Arp deviceName={deviceName}/>;
        } else if (show === "counters") {
            info = <Counters deviceName={deviceName}/>;
        } else if (show === "config") {
            info = <Config deviceName={deviceName}/>;
        } else if (show === "status") {
            info = <DeviceStatus deviceName={deviceName}/>
        }

        return (
            <Grid container direction="row">
                <Grid item style={{width: '15%', padding: '10px'}}>
                    <Grid container direction="column">
                        <b>Device Name:</b>{this.state.deviceName}
                        <br/><br/>
                        <Button variant="contained" color="primary" onClick={() => {
                            this.setState({show: "status"})
                        }}>Status</Button>
                        <Button variant="contained" color="primary" onClick={() => {
                            this.setState({show: "facts"})
                        }}>Facts</Button>
                        <Button variant="contained" color="primary" onClick={() => {
                            this.setState({show: "arp"})
                        }}>Arp</Button>
                        <Button variant="contained" color="primary" onClick={() => {
                            this.setState({show: "counters"})
                        }}>Counters</Button>
                        <Button variant="contained" color="primary" onClick={() => {
                            this.setState({show: "config"})
                        }}>Config</Button>
                        <br/><br/> <br/><br/>
                        <Button variant="contained" style={{width: '100%'}} onClick={() => this.renderDevices(this.state.dashboard)}>
                            Return to Devices
                        </Button>
                        <Button variant="contained" style={{width: '100%'}} onClick={() => this.renderCompliance(this.state.dashboard)}>
                            Return to Compliance
                        </Button>
                    </Grid>
                </Grid>
                <Grid item style={{width: '85%', padding: '10px'}}>
                    {info}
                </Grid>
            </Grid>
        );
    }
}

export default DeviceDashboard

