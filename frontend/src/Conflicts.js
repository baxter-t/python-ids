import React from 'react';
import axios from "axios";

class Conflicts extends React.Component {

        constructor() {
                super();

                this.state = {
                        newId: '',
                        newDescription: ""
                }

                this.handleIdChange = this.handleIdChange.bind(this);
                this.handleDescriptionChange = this.handleDescriptionChange.bind(this);
                this.handleSubmit = this.handleSubmit.bind(this);
        }

        handleDescriptionChange(event) {
                this.setState({ newDescription: event.target.value });
        }

        handleIdChange(event) {
                this.setState({ newId: event.target.value });
        }

        handleSubmit(event) {
                axios.post("http://localhost:9000/conflict", {
                        name: this.state.newId,
                        electorate: this.state.newDescription
                });

                event.preventDefault();
        }

        render() {
                return <div className="conflicts">
                        <h1>Conflict Interests</h1>
                        <ConflictList />
                </div>
        }
}

class ConflictList extends React.Component {

        constructor(props) {
                super(props);

                this.state = { conflicts: [] }
                this.refresh = this.refresh.bind(this);

                this.handleBillSearchChange = this.handleBillSearchChange.bind(this);
                this.handlePoliticianSearchChange = this.handlePoliticianSearchChange.bind(this);
        }

        refresh(e) {
                var params = {}
                if (this.state.politicianSearch) {
                        params = { name: this.state.politicianSearch };
                }
                if (this.state.billSearch) {
                        params = { id: this.state.billSearch };
                }

                this.setState({})
                axios.get("http://localhost:9000/conflicts", { params: params })
                        .then(res => {
                                this.setState({
                                        ...this.state, ...{
                                                conflicts: res.data
                                        }
                                })
                        });
                e.preventDefault();
        }

        handlePoliticianSearchChange(e) {
                this.setState({ politicianSearch: e.target.value })
        }

        handleBillSearchChange(e) {
                this.setState({ billSearch: e.target.value })
        }

        async componentDidMount() {
                axios.get("http://localhost:9000/conflicts")
                        .then(res => {
                                this.setState({
                                        ...this.state, ...{
                                                conflicts: res.data
                                        }
                                })
                        })
        }

        render() {
                return (
                        <div>
                                <h2>Conflicts</h2>
                                <form onSubmit={this.refresh}>
                                        <input placeholder="Politician" value={this.state.politicianSearch} onChange={this.handlePoliticianSearchChange}></input>
                                        <input placeholder="Bill" value={this.state.billSearch} onChange={this.handleBillSearchChange}></input>
                                        <button type="submit">Refresh</button>
                                </form>
                                <Conflict heading={true} name={"Politician"} id={"Conflicted Bill"} description={"Bill Description"} interest_group={"Conflict"} />
                                {this.state.conflicts.map((item, index) => (
                                        <Conflict name={item.name} id={item.id} interest_group={item.interest_group} description={item.description} />
                                ))}
                        </div>
                )
        }
}

class Conflict extends React.Component {
        constructor(props) {
                super(props);
        }

        render() {
                return (
                        <div className={`conflict ${this.heading ? "list-heading" : ""}`}>
                                <p>{this.props.name}</p>
                                <p>{this.props.id}</p>
                                <p>{this.props.description}</p>
                                <p>{this.props.interest_group}</p>
                        </div>
                )
        }
}

export default Conflicts;
