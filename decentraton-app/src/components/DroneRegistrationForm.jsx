import React, { useState, useEffect } from "react";

export default function DroneRegistrationForm() {
    const [formData, setFormData] = useState({
        brand: "",
        model: "",
        serial: "",
        pilotId: "",
    });

    const [drones, setDrones] = useState([]);

    useEffect(() => {
        fetch("http://localhost:5000/api/drones")
            .then((res) => res.json())
            .then((data) => setDrones(data))
            .catch((err) => console.error("Ошибка загрузки дронов:", err));
    }, []);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prev) => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const res = await fetch("http://localhost:5000/api/drones", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(formData),
            });

            if (!res.ok) {
                const errorData = await res.json();
                alert("Ошибка: " + errorData.error);
                return;
            }

            alert("Дрон успешно зарегистрирован");

            // Обновляем список дронов
            const updatedList = await fetch(
                "http://localhost:5000/api/drones"
            ).then((res) => res.json());
            setDrones(updatedList);

            setFormData({ brand: "", model: "", serial: "", pilotId: "" });
        } catch (error) {
            console.error(error);
            alert("Ошибка при регистрации дрона");
        }
    };

    return (
        <div
            style={{
                maxWidth: 500,
                margin: "auto",
                padding: 20,
                background: "#f9f9f9",
                borderRadius: 10,
            }}
        >
            <h2>Регистрация дрона</h2>
            <form
                onSubmit={handleSubmit}
                style={{ display: "flex", flexDirection: "column", gap: 12 }}
            >
                <input
                    type="text"
                    name="brand"
                    placeholder="Марка дрона"
                    value={formData.brand}
                    onChange={handleChange}
                    required
                />
                <input
                    type="text"
                    name="model"
                    placeholder="Модель дрона"
                    value={formData.model}
                    onChange={handleChange}
                    required
                />
                <input
                    type="text"
                    name="serial"
                    placeholder="Серийный номер"
                    value={formData.serial}
                    onChange={handleChange}
                    required
                />
                <input
                    type="text"
                    name="pilotId"
                    placeholder="ID пилота"
                    value={formData.pilotId}
                    onChange={handleChange}
                    required
                />
                <button type="submit" style={{ padding: "8px 0" }}>
                    Зарегистрировать дрон
                </button>
            </form>

            <h3 style={{ marginTop: 30 }}>Зарегистрированные дроны:</h3>
            {drones.length === 0 ? (
                <p>Нет зарегистрированных дронов.</p>
            ) : (
                <ul>
                    {drones.map((drone) => (
                        <li key={drone.id} style={{ marginBottom: 10 }}>
                            <strong>Марка:</strong> {drone.brand},{" "}
                            <strong>Модель:</strong> {drone.model},{" "}
                            <strong>Серийный номер:</strong> {drone.serial},{" "}
                            <strong>ID пилота:</strong> {drone.pilotId}
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}
