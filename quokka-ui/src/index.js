import React from 'react';
import ReactDOM from 'react-dom';
import Arp from './components/Arp'
import Facts from './components/Facts'
import Counters from './components/Counters'
import './index.css';

ReactDOM.render(
    <div>
        <Facts />
        <Arp />
        <Counters />
    </div>,
  document.getElementById('root')
);
