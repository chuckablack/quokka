import React from 'react';
import {makeStyles} from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import MenuItem from "@material-ui/core/MenuItem";
import Menu from "@material-ui/core/Menu";
import Backdrop from "@material-ui/core/Backdrop";
import CircularProgress from "@material-ui/core/CircularProgress";

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

function renderEvents(dashboard) {
    dashboard.setState({show: "events"})
}

function renderCapture(dashboard) {
    dashboard.setState({show: "capture"})
}

function renderWorkers(dashboard) {
    dashboard.setState({show: "workers"})
}

export default function DashboardAppBar(props) {
    const classes = useStyles();
    const dashboard = props.dashboard;
    const [anchorE1, setAnchorEl] = React.useState(null);
    const [isLoading, setIsLoading] = React.useState(null)

    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const fetchReset = (target) => {
        let requestUrl = process.env.REACT_APP_QUOKKA_HOST + '/ui/reset/' + target
        console.log('performing reset:' + requestUrl)
        fetch(requestUrl, {method: 'POST', mode: 'cors'})
            .then(response => {
                console.log(response)
                if (target === "devices") {
                    renderDevices(dashboard);
                } else if (target === "hosts") {
                    renderHosts(dashboard)
                } else if (target === "services") {
                    renderServices(dashboard)
                } else if (target === "events") {
                    renderEvents(dashboard)
                } else if (target === "capture") {
                    renderCapture(dashboard)
                } else if (target === "workers") {
                    renderWorkers(dashboard)
                }

                setIsLoading(false)
            })
    }
    const handleResetDevices = (event) => {
        setIsLoading(true);
        fetchReset("devices");
        setAnchorEl(null);
    };
    const handleResetHosts = (event) => {
        setIsLoading(true);
        fetchReset("hosts");
        setAnchorEl(null);
    };
    const handleResetServices = (event) => {
        setIsLoading(true);
        fetchReset("services");
        setAnchorEl(null);
    };
    const handleResetEvents = (event) => {
        setIsLoading(true);
        fetchReset("events");
        setAnchorEl(null);
    };
    const handleResetCapture = (event) => {
        setIsLoading(true);
        fetchReset("capture");
        setAnchorEl(null);
    };


    const handleClose = () => {
        setAnchorEl(null);
    };

    return (
        <div className={classes.root}>
            <AppBar position="static">
                <Toolbar>
                    <IconButton aria-controls="dash-menu" aria-haspopup="true" color="inherit" onClick={handleClick}>
                        <MenuIcon/>
                    </IconButton>
                    <Menu
                        id="dash-menu"
                        anchorEl={anchorE1}
                        keepMounted
                        open={Boolean(anchorE1)}
                        onClose={handleClose}
                    >
                        <MenuItem onClick={handleResetDevices}>Reset Devices</MenuItem>
                        <MenuItem onClick={handleResetHosts}>Reset Hosts</MenuItem>
                        <MenuItem onClick={handleResetServices}>Reset Services</MenuItem>
                        <MenuItem onClick={handleResetEvents}>Reset Events</MenuItem>
                        <MenuItem onClick={handleResetCapture}>Reset Capture</MenuItem>
                    </Menu>
                    <Typography variant="h6" className={classes.title} style={{paddingLeft: '20px'}}>
                        <b>QUOKKA</b> Dashboard
                    </Typography>
                    <Button color="inherit" onClick={() => renderDevices(dashboard)}>Devices</Button>
                    <Button color="inherit" onClick={() => renderCompliance(dashboard)}>Compliance</Button>
                    <Button color="inherit" onClick={() => renderHosts(dashboard)}>Hosts</Button>
                    <Button color="inherit" onClick={() => renderServices(dashboard)}>Services</Button>
                    <Button color="inherit" onClick={() => renderEvents(dashboard)}>Events</Button>
                    <Button color="inherit" onClick={() => renderCapture(dashboard)}>Capture</Button>
                    <Button color="inherit" onClick={() => renderWorkers(dashboard)}>Workers</Button>
                </Toolbar>
            </AppBar>
            {isLoading ?
                <Backdrop open={true}>
                    <CircularProgress color="inherit"/>
                </Backdrop>
                : ""
            }
        </div>
    );
}