import React, {Component} from 'react';
import Grid from "@material-ui/core/Grid";
import 'typeface-roboto'
import Facts from "./Facts";
import Arp from "./Arp";
import Counters from "./Counters";
import DeviceAppBar from "./DeviceAppBar";
import Button from "@material-ui/core/Button";

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
        }

        return (
            <Grid container direction="column">
                <DeviceAppBar deviceName="devnet-csr-always-on-sandbox"/>
                <Grid container direction="row">
                    <Grid item>
                        <Grid container direction="column">
                            <Button color="primary" onClick={() => {this.setState({show:"facts"})}}>Facts</Button>
                            <Button color="primary" onClick={() => {this.setState({show:"arp"})}}>Arp</Button>
                            <Button color="primary" onClick={() => {this.setState({show:"counters"})}}>Counters</Button>
                        </Grid>
                    </Grid>
                    <Grid item>
                        {info}
                    </Grid>
                </Grid>
            </Grid>
        );
    }
}

export default DeviceDashboard;
