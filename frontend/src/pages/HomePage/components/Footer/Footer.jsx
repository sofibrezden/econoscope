import styles from "./Footer.module.scss";
import Instagram from "../../../../assets/icons/instagram.png";
import LinkedIn from "../../../../assets/icons/linkedin.png";
import Facebook from "../../../../assets/icons/facebook.png";
import YouTube from "../../../../assets/icons/youtube.png";

function Footer() {
  return (
    <div className={styles.footer}>
      <div className={styles.contacts}>
        <h3 className={styles.getInTouch}>Get In Touch</h3>
        <p>
          <b>Email:</b> econo_scope@gmail.com
        </p>
        <p>
          <b>Tel:</b> +380 98 756 28 74
        </p>
      </div>

      <div className={styles.socialMedia}>
        <h3 className={styles.followUs}>Follow us</h3>
        <div className={styles.iconsContainer}>
          <img src={Instagram} alt="Instagram" />
          <img src={LinkedIn} alt="LinkedIn" />
          <img src={Facebook} alt="Facebook" />
          <img src={YouTube} alt="YouTube" />
        </div>
      </div>

      <div className={styles.newsletterContainer}>
        <p className={styles.newsletterTitle}>
          Join our online community for free. No spam{" "}
        </p>
        <div className={styles.wrapper}>
          <input type="text" placeholder="Enter your email..." />
          <button className={styles.subscribe}>Subscribe</button>
        </div>
      </div>
    </div>
  );
}

export default Footer;
