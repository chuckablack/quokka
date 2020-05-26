import React, {Component} from 'react';
import Grid from "@material-ui/core/Grid";
import Button from "@material-ui/core/Button";
import 'typeface-roboto'

import DeviceAppBar from "./DeviceAppBar";
import Facts from "./Facts";
import Arp from "./Arp";
import Counters from "./Counters";
import Config from "./Config";

class DeviceDashboard extends Component {

    constructor(props) {
        super(props);
        this.state = {
            show: "facts",
        };
    }

    render() {

        let info;
        if (this.state.show==="facts") {
            info = <Facts deviceName={"devnet-csr-always-on-sandbox"}/>;
        } else if (this.state.show==="arp") {
            info = <Arp />;
        } else if (this.state.show==="counters") {
            info = <Counters />;
        } else if (this.state.show==="config") {
            info = <Config />;
        }



        return (
            <Grid container direction="column">
                <DeviceAppBar deviceName="devnet-csr-always-on-sandbox"/>
                <Grid container direction="row">
                    <Grid item style={{ width: '10%' }}>
                        <Grid container direction="column">
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

export default DeviceDashboard;
