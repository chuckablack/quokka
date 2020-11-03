import React, {Component} from 'react';
import Grid from "@material-ui/core/Grid";
import 'typeface-roboto'

import DashboardAppBar from "./DashboardAppBar";
import Devices from "./Devices";
import Hosts from "./Hosts";
import Compliance from "./Compliance";
import Services from "./Services";
import HostStatus from "./HostStatus";
import DeviceDashboard from "./DeviceDashboard";
import ServiceStatus from "./ServiceStatus";
import Events from "./Events";
import Capture from "./Capture";
import Workers from "./Workers";
import WorkerStatus from "./WorkerStatus"

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
        const {deviceName, show, hostId, serviceId, workerId, ip, protocol, port} = this.state

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
        } else if (show === "events") {
            info = <Events dashboard={this}/>;
        } else if (show === "capture") {
            info = <Capture ip={ip} protocol={protocol} port={port} dashboard={this}/>;
        } else if (show === "workers") {
            info = <Workers dashboard={this}/>;
        } else if (show === "workerstatus") {
            info = <WorkerStatus workerId={workerId} dashboard={this}/>;
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
