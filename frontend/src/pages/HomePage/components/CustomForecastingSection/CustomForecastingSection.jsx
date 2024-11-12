import styles from "./CustomForecastingSection.module.scss";
import Forecasting from "../../../../assets/forecasting.png";

function CustomForecastingSection() {
  return (
    <div className={styles.sectionContainer}>
      <div>
        <h1 className={styles.sectionTitle}>Custom Forecasting Models</h1>
        <p className={styles.sectionDescription}>
          Our custom forecasting models are designed to fit the unique
          requirements of your business, ensuring you receive the most relevant
          data. This enables your organization to prepare for potential shifts
          in employment rates, optimize workforce planning, and make informed
          strategic decisions that align with current and future labor market
          trends.
        </p>
      </div>
      <img
        src={Forecasting}
        alt="Forecasting"
        className={styles.sectionImage}
      />
    </div>
  );
}

export default CustomForecastingSection;
