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

class Dashboard extends Component {

    constructor(props) {
        super(props);
        this.state = {
            deviceName: this.props.deviceName,
            show: "devices",
        };
    }

    render() {
        const deviceName = this.state.deviceName
        const show = this.state.show

        let info;
        if (show === "facts") {
            info = <Facts deviceName={deviceName}/>;
        } else if (show === "arp") {
            info = <Arp deviceName={deviceName}/>;
        } else if (show === "counters") {
            info = <Counters deviceName={deviceName}/>;
        } else if (show === "config") {
            info = <Config deviceName={deviceName}/>;
        } else if (show === "devices") {
            info = <Devices dashboard={this}/>;
        } else if (show === "hosts") {
            info = <Hosts dashboard={this}/>;
        } else if (show === "compliance") {
            info = <Compliance dashboard={this}/>;
        } else if (show === "services") {
            info = <Services dashboard={this}/>;
        }


        return (
            <Grid container direction="column">
                <DashboardAppBar dashboard={this}/>
                <Grid container direction="row" style={{paddingTop:"10px"}}>
                    {(show !== "devices" && show !== "hosts" && show !== "compliance"&& show !== "services") &&
                        <Grid item style={{width: '10%'}}>
                            <Grid container direction="column">
                                <Button color="primary" onClick={() => {
                                    this.setState({show: "facts"})
                                }}>Facts</Button>
                                <Button color="primary" onClick={() => {
                                    this.setState({show: "arp"})
                                }}>Arp</Button>
                                <Button color="primary" onClick={() => {
                                    this.setState({show: "counters"})
                                }}>Counters</Button>
                                <Button color="primary" onClick={() => {
                                    this.setState({show: "config"})
                                }}>Config</Button>
                            </Grid>
                        </Grid>
                    }
                    {(show !== "devices" && show !== "hosts" && show !== "compliance" && show !== "services") ?
                        <Grid item style={{width: '90%'}}>
                            {info}
                        </Grid>
                        :
                        <Grid item style={{width: '100%'}}>
                            {info}
                        </Grid>
                    }
                </Grid>
            </Grid>
        );
    }
}

export default Dashboard;
