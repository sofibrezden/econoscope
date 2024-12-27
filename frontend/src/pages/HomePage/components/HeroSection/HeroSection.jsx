import styles from "./HeroSection.module.scss";
import CoinsLeaves from "../../../../assets/coins_leaves.png";
import {useNavigate} from 'react-router-dom';

function HeroSection() {
    const navigate = useNavigate();

    const handleGetStartedClick = () => {
        navigate('/predict');
    }

    const handleLearnMoreClick = () => {
        const section = document.getElementById('keyFeature');
        if (section) {
            section.scrollIntoView({behavior: 'smooth'});
        }
    }

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
                    <button className={styles.getStarted} onClick={handleGetStartedClick}>
                        Get Started
                    </button>
                    <button className={styles.learnMore} onClick={handleLearnMoreClick}>
                        Learn More
                    </button>
                </div>
            </div>
            <img src={CoinsLeaves} alt="Coins" className={styles.heroSectionImage}/>
        </div>
    );
}

export default HeroSection;
