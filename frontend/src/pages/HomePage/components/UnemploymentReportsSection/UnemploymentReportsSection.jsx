import styles from "./UnemploymentReportsSection.module.scss";
import Reports from "../../../../assets/reports.png";
import Decor from "../../../../assets/decor.png";

function UnemploymentReportsSection() {
  return (
    <div className={styles.sectionContainer}>
      <img src={Reports} alt="Image" className={styles.sectionImage} />
      <div>
        <h1 className={styles.sectionTitile}>Unemployment Reports</h1>
        <p className={styles.sectionDescription}>
          We deliver detailed monthly reports on employment trends, offering
          insights into current economic conditions and future projections. With
          these insights, you can identify emerging trends, evaluate economic
          risks, and make timely adjustments to workforce strategies, ensuring
          your organization stays prepared in a dynamic labor market.
        </p>
      </div>
      <img src={Decor} alt="Decor" className={styles.sectionDecor} />
    </div>
  );
}

export default UnemploymentReportsSection;
