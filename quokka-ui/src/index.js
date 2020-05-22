import React from 'react';
import ReactDOM from 'react-dom';
import ArpClass from './components/ArpClass'
import Facts from './components/Facts'
import Counters from './components/Counters'
import './index.css';

ReactDOM.render(
    <div>
        <Facts />
        <ArpClass />
        <Counters />
    </div>,
  document.getElementById('root')
);
