const knex = require("./db");

async function migrate() {
    const exists = await knex.schema.hasTable("drones");
    if (!exists) {
        await knex.schema.createTable("drones", (table) => {
            table.increments("id").primary();
            table.string("brand").notNullable();
            table.string("model").notNullable();
            table.string("serial").notNullable().unique();
            table.string("pilotId").notNullable();
            table.timestamp("created_at").defaultTo(knex.fn.now());
        });
        console.log("Таблица drones создана");
    } else {
        console.log("Таблица drones уже существует");
    }
    process.exit(0);
}

migrate();
