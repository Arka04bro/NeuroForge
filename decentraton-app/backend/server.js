const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");
const knex = require("./db");

const app = express();
const PORT = 5000;

app.use(cors());
app.use(bodyParser.json());

// Получить список дронов
app.get("/api/drones", async (req, res) => {
    try {
        const drones = await knex("drones")
            .select("*")
            .orderBy("created_at", "desc");
        res.json(drones);
    } catch (err) {
        res.status(500).json({ error: "Ошибка сервера" });
    }
});

// Зарегистрировать новый дрон
app.post("/api/drones", async (req, res) => {
    const { brand, model, serial, pilotId } = req.body;
    if (!brand || !model || !serial || !pilotId) {
        return res.status(400).json({ error: "Все поля обязательны" });
    }

    try {
        await knex("drones").insert({ brand, model, serial, pilotId });
        res.status(201).json({ message: "Дрон зарегистрирован" });
    } catch (err) {
        if (err.code === "SQLITE_CONSTRAINT") {
            res.status(400).json({
                error: "Дрон с таким серийным номером уже зарегистрирован",
            });
        } else {
            res.status(500).json({ error: "Ошибка сервера" });
        }
    }
});

app.listen(PORT, () => {
    console.log(`Backend запущен на http://localhost:${PORT}`);
});
