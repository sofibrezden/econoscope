import styles from "./KeyFeaturesSection.module.scss";
import ManCoins from "../../../../assets/man_coins.png";
import { cards } from "./constants";

function HeroSection() {
  return (
      <div id="keyFeature">
          <h1 className={styles.sectionTitle}>Key Features</h1>
          <div className={styles.sectionContainer}>
              <div>
                  <p className={styles.sectionSubTitle}>
                      Our model leverages state-of-the-art machine learning techniques to
                      forecast the US unemployment rate. It uses a combination of
                      macroeconomic data, labor market indicators, and internet search
                      data to predict future unemployment rates.
                  </p>
                  <button className={styles.viewDocumentation}>
                      View Documentation
                  </button>
              </div>
              <img src={ManCoins} alt="Man" className={styles.sectionImage}/>
          </div>
          <div className={styles.cardContainer}>
              {cards.map((item, index) => (
                  <div className={styles.wrapper} key={index}>
                      <img src={item.icon} alt="Icon" width={20} height={20}/>
                      <h3 className={styles.cardTitle}>{item.title}</h3>
                      <p className={styles.cardDescription}>{item.description}</p>
                  </div>
              ))}
          </div>
      </div>
  );
}

export default HeroSection;
