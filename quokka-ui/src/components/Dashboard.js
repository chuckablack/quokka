import React, {Component} from 'react';
import Grid from "@material-ui/core/Grid";
import Button from "@material-ui/core/Button";
import 'typeface-roboto'

import DashboardAppBar from "./DashboardAppBar";
import Facts from "./Facts";
import Arp from "./Arp";
import Counters from "./Counters";
import Config from "./Config";
import Devices from "./Devices";
import Hosts from "./Hosts";
import Compliance from "./Compliance"
import Services from "./Services"
import HostStatus from "./HostStatus"
import DeviceDashboard from "./DeviceDashboard"
import ServiceStatus from "./ServiceStatus";

class Dashboard extends Component {

    constructor(props) {
        super(props);
        this.state = {
            deviceName: this.props.deviceName,
            hostId: this.props.hostId,
            show: "devices",
        };
    }

    render() {
        const {deviceName, show, hostId, serviceId} = this.state

        let info;

        if (show === "devices") {
            info = <Devices dashboard={this}/>;
        } else if (show === "hosts") {
            info = <Hosts dashboard={this}/>;
        } else if (show === "compliance") {
            info = <Compliance dashboard={this}/>;
        } else if (show === "services") {
            info = <Services dashboard={this}/>;
        } else if (show === "hoststatus") {
            info = <HostStatus hostId={hostId} dashboard={this}/>;
        } else if (show === "servicestatus") {
            info = <ServiceStatus serviceId={serviceId} dashboard={this}/>;
        } else if (show === "devicestatus") {
            info = <DeviceDashboard deviceName={deviceName} dashboard={this}/>;
        }

        return (
            <Grid container direction="column">
                <DashboardAppBar dashboard={this}/>
                <Grid container direction="row" style={{paddingTop: "10px"}}>
                    <Grid item style={{width: '100%'}}>
                        {info}
                    </Grid>
                </Grid>
            </Grid>
        );
    }
}

export default Dashboard;
