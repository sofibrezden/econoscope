import styles from "./UnemploymentPredictorSection.module.scss";
import Dollars from "../../../../assets/dollars.png";

function UnemploymentRateSection() {
  return (
    <div className={styles.sectionContainer}>
      <img src={Dollars} alt="Dollars" className={styles.dollarsImage} />
      <div>
        <h1 className={styles.sectionTitle}>Unemployment Rate Predictor</h1>
        <p className={styles.sectionSubTitle}>
          Welcome! Curious about unemployment trends? Our platform helps you
          track and predict unemployment trends across demographics and regions.
          Powered by advanced machine learning models, it offers insights based
          on age, gender, and country, allowing users to explore data
          visualizations and forecasts. Designed for policymakers, researchers,
          and analysts, this tool supports data-driven decisions for economic
          and social planning.
        </p>
      </div>
    </div>
  );
}

export default UnemploymentRateSection;
