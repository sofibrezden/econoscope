import styles from "./EconomicImpactSection.module.scss";
import Economic from "../../../../assets/economic.png";
import Decor from "../../../../assets/decor.png";

function EconomicImpactSection() {
  return (
    <div className={styles.sectionContainer}>
      <img src={Economic} alt="Image" className={styles.sectionImage} />
      <div>
        <h1 className={styles.sectionTitile}>Economic Impact Assessments</h1>
        <p className={styles.sectionDescription}>
          We conduct comprehensive analyses to determine how unemployment trends
          could impact your business, helping you build effective strategies. By
          forecasting unemployment rates based on age, gender, country, and
          year, our tool provides tailored insights that highlight potential
          risks and opportunities in the job market.
        </p>
      </div>
      <img src={Decor} alt="Decor" className={styles.sectionDecor} />
    </div>
  );
}

export default EconomicImpactSection;
