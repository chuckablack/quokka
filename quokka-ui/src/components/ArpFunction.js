import React, {useEffect, useState} from 'react';
import Button from '@material-ui/core/Button'

function ArpFunction(props) {

    const [arpTable, setArpTable] = useState({arp: []});
    const [isLoading, setIsLoading] = useState(false);

    const fetchArp = () => {
        setIsLoading(true);
        fetch(process.env.REACT_APP_QUOKKA_HOST + '/ui/device?device=devnet-csr-always-on-sandbox&info=arp')
            .then(res => res.json())
            .then((data) => {
                setArpTable(data);
                setIsLoading(false);
                console.log(arpTable)
            })
            .catch(console.log)
    }

    useEffect(() => {
        fetchArp()
    }, []);

    if (isLoading) {
        return (
            <div className="container">
                <h2>ARP Table</h2>
                <p>Loading ...</p>
            </div>
        );
    }
    return (
        <div className="container">
            <h2>ARP Table</h2>
            <Button onClick={() => {fetchArp()}}>Refresh Arp Information</Button>
            <table>
                <tbody>
                <tr>
                    <th>IP Address</th>
                    <th>MAC Address</th>
                    <th>Interface</th>
                </tr>
                {arpTable.arp.map((arp_entry) => (
                    <tr key={arp_entry.mac}>
                        <td>{arp_entry.ip}</td>
                        <td>{arp_entry.mac}</td>
                        <td>{arp_entry.interface}</td>
                    </tr>
                ))}
                </tbody>
            </table>
        </div>
    );
}

export default ArpFunction;
