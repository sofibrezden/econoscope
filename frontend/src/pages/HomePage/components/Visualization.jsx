    import React from "react";
    import Header from "./Header/Header";

    function Visualization() {
        return (
            <>
                <Header/>
                <div style={{width: "100%", height: "calc(100vh - 80px)"}}>
                    <iframe
                        src={`http://127.0.0.1:8050/?token=${localStorage.getItem('authToken')}`}
                        title="Dash Visualization"
                        width="100%"
                        height="100%"
                        style={{border: "none"}}
                    />

                </div>
            </>
        );
    }

    export default Visualization;
