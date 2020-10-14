import React from 'react';
import axios from "axios";
import BACKEND from "./backend";

class BillInterests extends React.Component {

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
                axios.post(BACKEND + ":9000/bill", {
                        id: this.state.newId,
                        description: this.state.newDescription
                });

                event.preventDefault();
        }

        render() {
                return <div className="billInterests">
                        <h1>Bills</h1>

                        <form onSubmit={this.handleSubmit}>
                                <h4>New Bill</h4>
                                <input placeholder="ID" value={this.state.newId} onChange={this.handleIdChange}></input>
                                <input placeholder="Description" value={this.state.newDescription} onChange={this.handleDescriptionChange}></input>
                                <button type="submit">Add Bill</button>
                        </form>

                        <BillList />
                        <h1>Bill Interests</h1>
                        <BillInterestList />
                </div>
        }
}

class BillList extends React.Component {

        constructor(props) {
                super(props);

                this.state = { bills: [], search: "" }
                this.refresh = this.refresh.bind(this);
                this.handleSearchChange = this.handleSearchChange.bind(this);
        }

        refresh(e) {
                this.setState({})
                axios.get(`http://localhost:9000/bills${this.state.search ? "?search=" + this.state.search : ""}`)
                        .then(res => {
                                this.setState({
                                        ...this.state, ...{
                                                bills: res.data
                                        }
                                })
                        });

                e.preventDefault();
        }


        async componentDidMount() {
                axios.get(BACKEND + ":9000/bills")
                        .then(res => {
                                this.setState({
                                        ...this.state, ...{
                                                bills: res.data
                                        }
                                })
                        })
        }

        handleSearchChange(event) {
                this.setState({ search: event.target.value });
        }

        render() {
                return (
                        <div>
                                <form onSubmit={this.refresh}>
                                        <input placeholder="Search" value={this.state.search} onChange={this.handleSearchChange}></input>
                                        <button type="submit">Refresh</button>
                                </form>
                                {this.state.bills.map((item, index) => (
                                        <Bill id={item.id} description={item.description} />
                                ))}
                        </div>
                )
        }
}

class Bill extends React.Component {
        constructor(props) {
                super(props);
        }

        render() {
                return (
                        <div className="bill">
                                <p>{this.props.id}</p>
                                <p>{this.props.description}</p>
                        </div>
                )
        }
}

class BillInterestList extends React.Component {
        constructor(props) {
                super(props);

                this.state = { bills: [], billSearch: "", interestSearch: "" }
                this.refresh = this.refresh.bind(this);
                this.handleBillSearchChange = this.handleBillSearchChange.bind(this);
                this.handleInterestSearchChange = this.handleInterestSearchChange.bind(this);
                this.handleIdChange = this.handleIdChange.bind(this);
                this.handleInterestChange = this.handleInterestChange.bind(this);
                this.handleSubmit = this.handleSubmit.bind(this);
        }

        refresh(e) {
                var params = {}
                if (this.state.billSearch !== "") {
                        params.bill = this.state.billSearch
                }
                if (this.state.interestSearch !== "") {
                        params.interest = this.state.interestSearch
                }

                this.setState({})
                axios.get(BACKEND + ":9000/bill_interests", { params: params })
                        .then(res => {
                                this.setState({
                                        ...this.state, ...{
                                                bills: res.data
                                        }
                                })
                        })

                e.preventDefault();
        }


        async componentDidMount() {
                axios.get(BACKEND + ":9000/bill_interests")
                        .then(res => {
                                console.log(res);
                                this.setState({
                                        ...this.state, ...{
                                                bills: res.data
                                        }
                                })
                        })
        }

        handleInterestSearchChange(event) {
                this.setState({ interestSearch: event.target.value });
        }

        handleBillSearchChange(event) {
                this.setState({ billSearch: event.target.value });
        }

        handleIdChange(event) {
                this.setState({ newId: event.target.value });
        }

        handleInterestChange(event) {
                this.setState({ newInterest: event.target.value });
        }

        handleSubmit(event) {
                axios.post(BACKEND + ":9000/bill_interests", {
                        bill: this.state.newId,
                        interest: this.state.newInterest
                });

                event.preventDefault();
        }

        render() {
                return (
                        <div>
                                <h2>Bill Interests</h2>
                                <form onSubmit={this.handleSubmit}>
                                        <h4>New Bill Interest</h4>
                                        <input placeholder="ID" value={this.state.newId} onChange={this.handleIdChange}></input>
                                        <input placeholder="Interest" value={this.state.newInterest} onChange={this.handleInterestChange}></input>
                                        <button type="submit">Add Bill Interest</button>
                                </form>
                                <form onSubmit={this.refresh}>
                                        <input placeholder="Bill Id" value={this.state.billSearch} onChange={this.handleBillSearchChange}></input>
                                        <input placeholder="Interest Group" value={this.state.interestSearch} onChange={this.handleInterestSearchChange}></input>
                                        <button type="submit">Refresh</button>
                                </form>
                                {this.state.bills.map((item, index) => (
                                        <BillInterest bill_id={item.id} bill_description={item.description} interest_group={item.name} />
                                ))}
                        </div>
                )
        }
}

class BillInterest extends React.Component {
        constructor(props) {
                super(props);
        }

        render() {
                return (
                        <div className="bill">
                                <p>{this.props.bill_id}</p>
                                <p>{this.props.interest_group}</p>
                                <p>{this.props.bill_description}</p>
                        </div>
                )
        }
}


export default BillInterests;
