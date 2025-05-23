const knex = require("knex")({
    client: "sqlite3",
    connection: {
        filename: "./data.db", // файл базы
    },
    useNullAsDefault: true,
});

module.exports = knex;
