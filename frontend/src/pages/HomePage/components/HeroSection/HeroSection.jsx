import styles from "./HeroSection.module.scss";
import CoinsLeaves from "../../../../assets/coins_leaves.png";

function HeroSection() {
  return (
    <div className={styles.sectionContainer}>
      <div>
        <h1 className={styles.sectionTitle}>Stay Ahead In Employment Trends</h1>
        <p className={styles.sectionSubTitle}>
          Plan for the future with comprehensive data on global job markets and
          unemployment rates. Gain valuable insights into economic shifts and
          workforce trends to make better decisions in a competitive landscape.
        </p>
        <div className={styles.buttonsContainer}>
          <button className={styles.getStarted}>Get Started</button>
          <button className={styles.learnMore}>Learn More</button>
        </div>
      </div>
      <img src={CoinsLeaves} alt="Coins" className={styles.heroSectionImage} />
    </div>
  );
}

export default HeroSection;
