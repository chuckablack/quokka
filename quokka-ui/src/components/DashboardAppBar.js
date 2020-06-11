import React from 'react';
import {makeStyles} from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';

const useStyles = makeStyles((theme) => ({
    root: {
        flexGrow: 1,
    },
    menuButton: {
        marginRight: theme.spacing(2),
    },
    title: {
        flexGrow: 1,
    },
}));

function renderHosts(dashboard) {
    dashboard.setState({show: "hosts"})
}
function renderDevices(dashboard) {
    dashboard.setState({show: "devices"})
}
function renderCompliance(dashboard) {
    dashboard.setState({show: "compliance"})
}
function renderServices(dashboard) {
    dashboard.setState({show: "services"})
}
function renderDash(dashboard) {
    dashboard.setState({show: "dash"})
}
function renderChartTest(dashboard) {
    dashboard.setState({show: "charttest"})
}
function renderVis(dashboard) {
    dashboard.setState({show: "vis"})
}


export default function DashboardAppBar(props) {
    const classes = useStyles();
    const dashboard = props.dashboard;

    return (
        <div className={classes.root}>
            <AppBar position="static">
                <Toolbar>
                    <IconButton edge="start" className={classes.menuButton} color="inherit" aria-label="menu">
                        <MenuIcon />
                    </IconButton>
                    <Typography variant="h6" className={classes.title}>
                        Dashboard {props.deviceName}
                    </Typography>
                    <Button color="inherit" onClick={() => renderHosts(dashboard)}>Hosts</Button>
                    <Button color="inherit" onClick={() => renderDevices(dashboard)}>Devices</Button>
                    <Button color="inherit" onClick={() => renderCompliance(dashboard)}>Compliance</Button>
                    <Button color="inherit" onClick={() => renderServices(dashboard)}>Services</Button>
                    <Button color="inherit" onClick={() => renderDash(dashboard)}>Dash</Button>
                    <Button color="inherit" onClick={() => renderChartTest(dashboard)}>Chart</Button>
                    <Button color="inherit" onClick={() => renderVis(dashboard)}>Vis</Button>
                </Toolbar>
            </AppBar>
        </div>
    );
}