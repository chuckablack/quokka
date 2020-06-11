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
        fetch('http://127.0.0.1:5000/device?device=' + deviceName + '&info=counters')
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

        const {counters, isLoading} = this.state;

        return (
            <div className="container" style={{maxWidth: "100%"}}>
                <link
                    rel="stylesheet"
                    href="https://fonts.googleapis.com/icon?family=Material+Icons"
                />
                <Grid container direction="row" justify="space-between" alignItems="center">
                    <h2>Counters Table</h2>
                    {/*{isLoading ?*/}
                    {/*    <Backdrop open={true}>*/}
                    {/*        <CircularProgress color="inherit" />*/}
                    {/*    </Backdrop>*/}
                    {/*    : ""}*/}
                    <Button variant="contained" onClick={() => {
                        this.fetchCounters()
                    }}>Refresh Counters</Button>
                </Grid>
                <Grid item>
                    {/*{isLoading ?*/}
                    {/*    <Backdrop open={true}>*/}
                    {/*        <CircularProgress color="inherit" />*/}
                    {/*    </Backdrop>*/}
                    {/*    : ""}*/}
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
                    {/*<Table size="small">*/}
                    {/*    <TableHead>*/}
                    {/*        <TableRow>*/}
                    {/*            <TableCell>Interface</TableCell>*/}
                    {/*            <TableCell align="right">Rx Octets</TableCell>*/}
                    {/*            <TableCell align="right">Tx Octets</TableCell>*/}
                    {/*            <TableCell align="right">Rx Packets</TableCell>*/}
                    {/*            <TableCell align="right">Tx Packets</TableCell>*/}
                    {/*        </TableRow>*/}
                    {/*    </TableHead>*/}
                    {/*    <TableBody>*/}
                    {/*        {Object.keys(counters.counters).map((key, index) => (*/}
                    {/*            <TableRow key={index}>*/}
                    {/*                <TableCell>{key}</TableCell>*/}
                    {/*                <TableCell align="right">{counters.counters[key].rx_octets}</TableCell>*/}
                    {/*                <TableCell align="right">{counters.counters[key].tx_octets}</TableCell>*/}
                    {/*                <TableCell align="right">{counters.counters[key].rx_unicast_packets}</TableCell>*/}
                    {/*                <TableCell align="right">{counters.counters[key].tx_unicast_packets}</TableCell>*/}
                    {/*            </TableRow>*/}
                    {/*        ))}*/}
                    {/*    </TableBody>*/}
                    {/*</Table>*/}
                </Grid>
            </div>
        );
    }
}

export default Counters;
