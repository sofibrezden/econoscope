import styles from "./Header.module.scss";
import EconoscopeLogo from "../../../../assets/econoscope_logo.png";
import EconoscopeTitle from "../../../../assets/econoscope_title.png";

function Header() {
  return (
    <div className={styles.headerContainer}>
      <div className={styles.logoContainer}>
        <img src={EconoscopeLogo} className={styles.logo} />
        <img src={EconoscopeTitle} className={styles.title} />
      </div>
      <div className={styles.buttonsContainer}>
        <a href="/predict">Predict</a>
        <button className={styles.signInButton}>Sign in</button>
        <button className={styles.signUpButton}>Sign up</button>
      </div>
    </div>
  );
}

export default Header;
