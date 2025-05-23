import React from "react";
import DroneRegistrationForm from "./components/DroneRegistrationForm";

export default function App() {
    return (
        <div
            style={{
                fontFamily: "Arial, sans-serif",
                background: "#eef2f7",
                minHeight: "100vh",
                padding: 20,
            }}
        >
            <header style={{ textAlign: "center", marginBottom: 30 }}>
                <h1>UTM Kazakhstan — Регистрация дронов</h1>
            </header>
            <DroneRegistrationForm />
            <footer
                style={{ textAlign: "center", marginTop: 40, color: "#888" }}
            >
                &copy; 2025 UTM Kazakhstan. Все права защищены.
            </footer>
        </div>
    );
}
