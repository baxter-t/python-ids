import React from 'react';
import {
    BrowserRouter as Router,
    Switch,
    Link,
    Route
} from "react-router-dom";
import logo from './logo.svg';
import './App.css';
import PoliticianInterests from "./PoliticianInterests";
import BillInterests from "./BillInterests";
import Conflicts from "./Conflicts";

function App() {
    return (
        <Router>
            <Switch>
                <Route path="/politicians">
                    <PoliticianInterests />
                </Route>
                <Route path="/bills">
                    <BillInterests />
                </Route>
                <Route path="/conflicts">
                    <Conflicts />
                </Route>
            </Switch>
        </Router>
    );
}

export default App;
