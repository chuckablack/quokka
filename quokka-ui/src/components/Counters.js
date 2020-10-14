import React, {Component} from 'react';
import Button from '@material-ui/core/Button'
import Grid from "@material-ui/core/Grid";
import 'typeface-roboto'
import MaterialTable from "material-table";

class Counters extends Component {

    constructor(props) {
        super(props);
        this.state = {
            deviceName: props.deviceName,
            counters: {counters: {}},
            isLoading: false,
        };
    }

    fetchCounters() {
        const deviceName = this.state.deviceName
        this.setState({isLoading: true});
        fetch(process.env.REACT_APP_QUOKKA_HOST + '/ui/device?device=' + deviceName + '&info=counters')
            .then(res => res.json())
            .then((data) => {
                this.setState({counters: data, isLoading: false})
                console.log(this.state.counters)
            })
            .catch(console.log)
    }

    transformData(data) {
        var listData = [];
        for (var key in data) {
            data[key]["interface"] = key
            listData.push( data[key] );
        }
        return listData;
    }

    componentDidMount() {
        this.fetchCounters()
    }

    render() {

        const {counters} = this.state;

        return (
            <div className="container" style={{maxWidth: "100%"}}>
                <link
                    rel="stylesheet"
                    href="https://fonts.googleapis.com/icon?family=Material+Icons"
                />
                <Grid container direction="row" justify="space-between" alignItems="center">
                    <h2>Counters Table</h2>
                    <Button variant="contained" onClick={() => {
                        this.fetchCounters()
                    }}>Refresh Counters</Button>
                </Grid>
                <Grid item>
                    <MaterialTable
                        isLoading={!!this.state.isLoading}
                        title={"Counters: " + this.state.deviceName}
                        columns={[
                            { title: 'Interface', field: 'interface' },
                            { title: 'Rx Octets', field: 'rx_octets' },
                            { title: 'Tx Octets', field: 'tx_octets' },
                            { title: 'Rx Packets', field: 'rx_unicast_packets' },
                            { title: 'Tx Packets', field: 'tx_unicast_packets' },
                        ]}
                        data={ this.transformData(counters.counters) }
                        options={{
                            sorting: true,
                            padding: "dense",
                            pageSize: 10,
                        }}
                    />
                </Grid>
            </div>
        );
    }
}

export default Counters;
