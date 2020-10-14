const express = require("express");
const db = require("./db");
const app = express();
const port = 9000;
const mysql = require("mysql");
const bodyParser = require("body-parser");

const connection = db.getDbConnection();

const INSERT_POLITICIAN = "INSERT INTO politicians VALUES (DEFAULT, ?, ?)";
const INSERT_BILL = "INSERT INTO bills VALUES (?, ?)";
const INSERT_POLITICIAN_INTERESTS =
    "INSERT INTO politician_interests VALUES (?, ?)";
const INSERT_BILL_INTERESTS = "INSERT INTO bill_interests VALUES (?, ?)";

app.use(express.json());

app.use(function (req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "*");
    next();
});

app.get("/", (req, res) => {
    res.send("Hello World 2!");
});

app.post("/politician", (req, res) => {
    connection.query(
        INSERT_POLITICIAN,
        [req.body.name, req.body.electorate],
        (err, results, fields) => {
            if (err) throw err;

            console.log("New Politician: " + results.insertId);
        }
    );

    res.json({});
});

app.get("/politicians", (req, res) => {
    if (req.query.search) {
        connection.query(
            `SELECT * FROM politicians WHERE politicians.name LIKE '%${req.query.search}%'`,
            (err, results, fields) => {
                if (err) throw err;

                res.json(results);
            }
        );
    } else {
        connection.query(
            "SELECT * FROM politicians",
            (err, results, fields) => {
                if (err) throw err;

                res.json(results);
            }
        );
    }
});

app.post("/bill", (req, res) => {
    connection.query(
        INSERT_BILL,
        [req.body.id, req.body.description],
        (err, results, fields) => {
            if (err) throw err;

            console.log("New Bill: " + results.insertId);
        }
    );

    res.json({});
});

app.get("/bills", (req, res) => {
    console.log(req.query.search);
    if (req.query.search) {
        connection.query(
            `SELECT * FROM bills WHERE bills.id LIKE '%${req.query.search}%'`,
            (err, results, fields) => {
                if (err) throw err;

                res.json(results);
            }
        );
    } else {
        connection.query("SELECT * FROM bills", (err, results, fields) => {
            if (err) throw err;

            res.json(results);
        });
    }
});

app.post("/interest", (req, res) => {
    connection.query(
        INSERT_INTERESTS,
        [req.body.name],
        (err, results, fields) => {
            if (err) throw err;

            console.log("New Interest: " + results.insertId);
        }
    );

    res.json({});
});

app.get("/interests", (req, res) => {
    connection.query("SELECT * FROM interests", (err, results, fields) => {
        if (err) throw err;

        res.json(results);
    });
});

app.get("/politician_interests", (req, res) => {
    connection.query(
        "SELECT p.name as politician_name, i.name as interest_name FROM politicians p JOIN politician_interests pi ON p.id = pi.politician_id JOIN interests i ON pi.interest_group_id=i.id",
        (err, results, fields) => {
            if (err) throw err;

            res.json(results);
        }
    );
});

app.post("/politician_interests", (req, res) => {
    connection.query(
        "INSERT INTO interests VALUES (DEFAULT, ?)",
        [req.body.interest],
        (err, results, fields) => {
            if (err) throw err;

            connection.query(
                "SELECT id FROM interests WHERE name = '" +
                    req.body.interest +
                    "'",
                (err, results, fields) => {
                    if (err) throw err;

                    interest_id = results[0].id;

                    connection.query(
                        "SELECT id FROM politicians WHERE name = '" +
                            req.body.name +
                            "'",
                        (err, results, fields) => {
                            if (err) throw err;
                            politician_id = results[0].id;

                            connection.query(
                                INSERT_POLITICIAN_INTERESTS,
                                [politician_id, interest_id],
                                (err, results, fields) => {
                                    if (err) throw err;
                                }
                            );
                        }
                    );
                }
            );
        }
    );

    res.json({});
});

app.post("/bill_interests", (req, res) => {
    connection.query(
        "INSERT INTO interests VALUES (DEFAULT, ?)",
        [req.body.interest],
        (err, results, fields) => {
            if (err) throw err;

            connection.query(
                "SELECT id FROM interests WHERE name = '" +
                    req.body.interest +
                    "'",
                (err, results, fields) => {
                    if (err) throw err;

                    interest_id = results[0].id;

                    connection.query(
                        INSERT_BILL_INTERESTS,
                        [req.body.bill, interest_id],
                        (err, results, fields) => {
                            if (err) throw err;
                        }
                    );
                }
            );
        }
    );

    res.json({});
});

app.get("/bill_interests", (req, res) => {
    const defaultSelect =
        "SELECT b.id, b.description, i.name FROM bill_interests bi JOIN bills b ON bi.bill_id = b.id JOIN interests i ON bi.interest_group_id = i.id";
    const billSearch = ` WHERE b.id LIKE '%${req.query.bill}%' `;
    const interestSearch = ` i.name LIKE '%${req.query.interest}%' `;

    var query = defaultSelect;
    if (req.query.bill) {
        query = query + billSearch;
    }
    if (req.query.interest) {
        if (req.query.bill) {
            query = query + " AND ";
        } else {
            query = query + " WHERE ";
        }

        query = query + interestSearch;
    }

    connection.query(query, (err, results, fields) => {
        if (err) throw err;

        res.json(results);
    });
});

app.get("/conflicts", (req, res) => {
    var defaultQuery = `
            SELECT DISTINCT b.id, b.description, i.name, p.name, i.name as interest_group
            FROM bills b 
            JOIN bill_interests bi ON b.id = bi.bill_id
            JOIN interests i ON bi.interest_group_id = i.id
            JOIN politician_interests pi ON pi.interest_group_id=i.id
            JOIN politicians p ON p.id = pi.politician_id`;

    const politicianSearch = ` WHERE p.name LIKE '%${req.query.name}%'`;
    const billSearch = ` b.id LIKE '%${req.query.id}%'`;

    if (req.query.name) {
        defaultQuery += politicianSearch;
    }

    if (req.query.id) {
        if (req.query.name) {
            defaultQuery += " AND ";
        } else {
            defaultQuery += " WHERE ";
        }
        defaultQuery += billSearch;
    }

    connection.query(defaultQuery, (err, results, fields) => {
        if (err) throw err;

        res.json(results);
    });
});

app.get("/conflicts/:bill_id", (req, res) => {
    connection.query(
        `
            SELECT DISTINCT bills.id, bills.description, interests.name, politicians.name
            FROM bills JOIN bill_interests JOIN interests JOIN politician_interests JOIN politicians
            WHERE bills.id = 
            ` +
            "'" +
            req.params.bill_id +
            "'",

        (err, results, fields) => {
            if (err) throw err;

            res.json(results);
        }
    );
});

app.listen(port, () => {
    console.log(`Example app listening at http://localhost:${port}`);
});
