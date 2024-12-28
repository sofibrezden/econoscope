import React from "react";
import Header from "../HomePage/components/Header/Header";
import { API_Graphs_URL } from "../../config";
import styles from "./Visualization.module.scss";

function Visualization() {
  return (
    <>
      <Header />
      <div className={styles.container}>
        <iframe
          src={`${API_Graphs_URL}/?token=${localStorage.getItem("authToken")}`}
          title="Dash Visualization"
          width="100%"
          height="100%"
          className={styles.frame}
        />
      </div>
    </>
  );
}

export default Visualization;
