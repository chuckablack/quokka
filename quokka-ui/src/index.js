import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import DeviceDashboard from './components/DeviceDashboard'

ReactDOM.render(
    <DeviceDashboard deviceName='devnet-nexus-always-on-sandbox' />,
  document.getElementById('root')
);
