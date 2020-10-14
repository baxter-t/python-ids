const mysql = require("mysql");

const getDbConnection = () => {
    const connection = mysql.createConnection({
        host: "localhost",
        port: "3306",
        user: "user",
        password: "password",
        database: "interests",
    });

    connection.connect();
    connection.query(
        `CREATE TABLE IF NOT EXISTS politicians 
        (
            id int NOT NULL AUTO_INCREMENT, 
            name varchar(255), 
            electorate varchar(255),

            PRIMARY KEY (id)
        )`,
        function (err, result) {
            if (err) throw err;
            console.log("politicians Created");
        }
    );

    connection.query(
        `CREATE TABLE IF NOT EXISTS bills 
        (
            id varchar(255),
            description varchar(1000),
            PRIMARY KEY (id)
        )`,
        function (err, result) {
            if (err) throw err;
            console.log("bills Created");
        }
    );

    connection.query(
        `CREATE TABLE IF NOT EXISTS interests 
        (
            id int NOT NULL AUTO_INCREMENT ,
            name varchar(255),
            PRIMARY KEY (id)
        )`,
        function (err, result) {
            if (err) throw err;
            console.log("interests Created");
        }
    );

    connection.query(
        `CREATE TABLE IF NOT EXISTS politician_interests 
        (
            politician_id int,
            interest_group_id int ,

            FOREIGN KEY (politician_id) REFERENCES politicians(id),
            FOREIGN KEY (interest_group_id) REFERENCES interests(id)
        )`,
        function (err, result) {
            if (err) throw err;
            console.log("politician_interests Created");
        }
    );

    connection.query(
        `CREATE TABLE IF NOT EXISTS bill_interests 
        (
            bill_id varchar(255),
            interest_group_id int,

            FOREIGN KEY (interest_group_id) REFERENCES interests(id),
            FOREIGN KEY (bill_id) REFERENCES bills(id)
        )`,
        function (err, result) {
            if (err) throw err;
            console.log("bills_interests Created");
        }
    );

    return connection;
};

module.exports = { getDbConnection };
