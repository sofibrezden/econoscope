import { cards } from "./constants";
import styles from "./UnemploymentRateMatterSection.module.scss";

function UnemploymentRateMatterSection() {
  return (
    <div>
      <h1 className={styles.sectionTitle}>
        Why does unemployment rate matter?
      </h1>
      <div className={styles.cardContainer}>
        {cards.map((item, index) => (
          <div className={styles.wrapper} key={index}>
            <img src={item.image} alt="Image" height={276} />
            <h3 className={styles.cardTitle}>{item.title}</h3>
            <p className={styles.cardDescription}>{item.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default UnemploymentRateMatterSection;
