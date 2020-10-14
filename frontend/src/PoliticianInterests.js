import React from 'react';
import axios from "axios";

class PoliticianInterests extends React.Component {

        constructor() {
                super();

                this.state = {
                        newName: '',
                        newElectorate: ""
                }

                this.handleNameChange = this.handleNameChange.bind(this);
                this.handleElectorateChange = this.handleElectorateChange.bind(this);
                this.handleSubmit = this.handleSubmit.bind(this);
        }

        handleElectorateChange(event) {
                this.setState({ newElectorate: event.target.value });
        }

        handleNameChange(event) {
                this.setState({ newName: event.target.value });
        }

        handleSubmit(event) {
                axios.post("http://localhost:9000/politician", {
                        name: this.state.newName,
                        electorate: this.state.newElectorate
                });

                event.preventDefault();
        }

        render() {
                return <div className="politicianInterests">
                        <h1>Politician Interests</h1>

                        <form onSubmit={this.handleSubmit}>
                                <h4>New Politician</h4>
                                <input placeholder="Name" value={this.state.newName} onChange={this.handleNameChange}></input>
                                <input placeholder="Electorate" value={this.state.newElectorate} onChange={this.handleElectorateChange}></input>
                                <button type="submit">Add Politician</button>
                        </form>

                        <PoliticianList />
                        <PoliticianInterestList />
                </div>
        }
}

class PoliticianList extends React.Component {

        constructor(props) {
                super(props);

                this.state = { politicians: [] }
                this.refresh = this.refresh.bind(this);
        }

        refresh() {
                this.setState({})
                axios.get("http://localhost:9000/politicians")
                        .then(res => {
                                this.setState({
                                        ...this.state, ...{
                                                politicians: res.data
                                        }
                                })
                        })
        }


        async componentDidMount() {
                axios.get("http://localhost:9000/politicians")
                        .then(res => {
                                this.setState({
                                        ...this.state, ...{
                                                politicians: res.data
                                        }
                                })
                        })
        }

        render() {
                return (
                        <div>
                                <h2>Politicians</h2>
                                <button onClick={this.refresh}>Refresh</button>
                                <Politician name={"Politician"} electorate={"Electorate"} />
                                {this.state.politicians.map((item, index) => (
                                        <Politician name={item.name} electorate={item.electorate} />
                                ))}
                        </div>
                )
        }
}

class Politician extends React.Component {
        constructor(props) {
                super(props);
        }

        render() {
                return (
                        <div className="politician">
                                <p>{this.props.name}</p>
                                <p>{this.props.electorate}</p>
                        </div>
                )
        }
}

class PoliticianInterestList extends React.Component {
        constructor(props) {
                super(props);

                this.state = { politicians: [] }
                this.refresh = this.refresh.bind(this);
                this.handleInterestChange = this.handleInterestChange.bind(this);
                this.handleNameChange = this.handleNameChange.bind(this);
                this.handleSubmit = this.handleSubmit.bind(this);
                this.handleNameSearchChange = this.handleNameSearchChange.bind(this);
                this.handleInterestSearchChange = this.handleInterestSearchChange.bind(this);
        }

        refresh(e) {
                this.setState({})
                axios.get("http://localhost:9000/politician_interests")
                        .then(res => {
                                this.setState({
                                        ...this.state, ...{
                                                politicians: res.data
                                        }
                                })
                        });
                e.preventDefault();
        }


        async componentDidMount() {
                axios.get("http://localhost:9000/politician_interests")
                        .then(res => {
                                this.setState({
                                        ...this.state, ...{
                                                politicians: res.data
                                        }
                                })
                        })
        }

        handleNameChange(event) {
                this.setState({ newName: event.target.value });
        }

        handleInterestChange(event) {
                this.setState({ newInterest: event.target.value });
        }
        handleInterestSearchChange(event) {
                this.setState({ interestSearch: event.target.value });
        }

        handleNameSearchChange(event) {
                this.setState({ billSearch: event.target.value });
        }

        handleSubmit(event) {
                axios.post("http://localhost:9000/politician_interests", {
                        name: this.state.newName,
                        interest: this.state.newInterest
                });

                event.preventDefault();
        }

        render() {
                return (
                        <div>
                                <h2>Politician Interests</h2>
                                <form onSubmit={this.handleSubmit}>
                                        <h4>New Politician Interest</h4>
                                        <input placeholder="Name" value={this.state.newName} onChange={this.handleNameChange}></input>
                                        <input placeholder="Interest" value={this.state.newInterest} onChange={this.handleInterestChange}></input>
                                        <button type="submit">Add Politician Interest</button>
                                </form>
                                <form onSubmit={this.refresh}>
                                        <input placeholder="Politician" value={this.state.billSearch} onChange={this.handlePoliticianSearchChange}></input>
                                        <input placeholder="Interest Group" value={this.state.interestSearch} onChange={this.handleInterestSearchChange}></input>
                                        <button type="submit">Refresh</button>
                                </form>
                                <PoliticianInterest politician_name={"Politician Name"} interest_name={"Interest"} />
                                {this.state.politicians.map((item, index) => (
                                        <PoliticianInterest politician_name={item.politician_name} interest_name={item.interest_name} />
                                ))}
                        </div>
                )
        }
}

class PoliticianInterest extends React.Component {
        constructor(props) {
                super(props);
        }

        render() {
                return (
                        <div className="politician">
                                <p>{this.props.politician_name}</p>
                                <p>{this.props.interest_name}</p>
                        </div>
                )
        }
}


export default PoliticianInterests;
