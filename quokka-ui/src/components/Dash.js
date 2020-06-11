import React, {Component} from 'react';
import 'typeface-roboto'

class Dash extends Component {

    constructor(props) {
        super(props);
        this.state = {
            isLoading: false,
            dashboard: props.dashboard,
        };
    }

    fetchDash() {

        this.setState({isLoading: true});
        let requestUrl = 'http://127.0.0.1:8050/'
        fetch(requestUrl)
            .then(res => res.text())
            .then((data) => {
                this.setState({dash: data, isLoading: false})
                console.log(this.state.dash)
            })
            .catch(console.log)
    }

    componentDidMount() {
        this.fetchDash()
    }

    componentWillUnmount() {
        clearInterval(this.interval)
    }

    render() {

        const {dash, isLoading} = this.state;

        return (
            <div className="container" style={{maxWidth: "100%"}}>
                <div dangerouslySetInnerHTML={{ __html: this.state.dash }} />
            </div>
        );
    }
}

export default Dash;
