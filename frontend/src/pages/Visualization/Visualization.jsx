import React from "react";
import Header from "../HomePage/components/Header/Header";
import { API_Graphs_URL } from "../../config";

function Visualization() {
    return (
        <>
            <Header />
            <div style={{ width: "100%", height: "calc(100vh - 80px)" }}>
                <iframe
                    src={`${API_Graphs_URL}/?token=${localStorage.getItem('authToken')}`}
                    title="Dash Visualization"
                    width="100%"
                    height="100%"
                    style={{ border: "none" }}
                />
            </div>
        </>
    );
}

export default Visualization;
