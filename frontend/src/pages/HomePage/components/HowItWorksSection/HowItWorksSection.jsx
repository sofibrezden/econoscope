import { cards } from "./constants";
import styles from "./HowItWorksSection.module.scss";

function HowItWorksSection() {
  return (
    <div>
      <h1 className={styles.sectionTitle}>How It Works</h1>
      <div className={styles.cardContainer}>
        {cards.map((item, index) => (
          <div className={styles.wrapper} key={index}>
            <img src={item.image} alt="Image" height={206} />
            <h3 className={styles.cardTitle}>{item.title}</h3>
            <p className={styles.cardDescription}>{item.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default HowItWorksSection;
