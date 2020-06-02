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

        let info;
        if (this.state.show==="facts") {
            info = <Facts deviceName={deviceName} />;
        } else if (this.state.show==="arp") {
            info = <Arp deviceName={deviceName} />;
        } else if (this.state.show==="counters") {
            info = <Counters deviceName={deviceName} />;
        } else if (this.state.show==="config") {
            info = <Config deviceName={deviceName} />;
        } else if (this.state.show==="devices") {
            info = <Devices dashboard={this}/>;
        } else if (this.state.show==="hosts") {
            info = <Hosts dashboard={this}/>;
        }


        return (
            <Grid container direction="column">
                <DashboardAppBar dashboard={this}/>
                <Grid container direction="row">
                    <Grid item style={{ width: '10%' }}>
                        <Grid container direction="column">
                            {/*<Button color="primary" onClick={() => {this.setState({show:"devices"})}}>Devices</Button>*/}
                            {/*<Button color="primary" onClick={() => {this.setState({show:"hosts"})}}>Hosts</Button>*/}
                            <Button color="primary" onClick={() => {this.setState({show:"facts"})}}>Facts</Button>
                            <Button color="primary" onClick={() => {this.setState({show:"arp"})}}>Arp</Button>
                            <Button color="primary" onClick={() => {this.setState({show:"counters"})}}>Counters</Button>
                            <Button color="primary" onClick={() => {this.setState({show:"config"})}}>Config</Button>
                        </Grid>
                    </Grid>
                    <Grid item style={{ width: '90%' }}>
                        {info}
                    </Grid>
                </Grid>
            </Grid>
        );
    }
}

export default Dashboard;
