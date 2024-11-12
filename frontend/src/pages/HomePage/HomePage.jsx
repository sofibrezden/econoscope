import HeroSection from "./components/HeroSection/HeroSection";
import UnemploymentRateSection from "./components/UnempoymentPredictorSection/UnempoymentPredictorSection";
import KeyFeaturesSection from "./components/KeyFeaturesSection/KeyFeaturesSection";
import HowItWorksSection from "./components/HowItWorksSection/HowItWorksSection";
import UnemploymentRateMatterSection from "./components/UnemploymentRateMatterSection/UnemploymentRateMatterSection";
import EconomicImpactSection from "./components/EconomicImpactSection/EconomicImpactSection";
import UnemploymentReportsSection from "./components/UnemploymentReportsSection/UnemploymentReportsSection";
import CustomForecastingSection from "./components/CustomForecastingSection/CustomForecastingSection";
import Footer from "./components/Footer/Footer";
import Header from "./components/Header/Header";

function HomePage() {
  return (
    <>
      <Header />
      <HeroSection />
      <UnemploymentRateSection />
      <KeyFeaturesSection />
      <HowItWorksSection />
      <UnemploymentRateMatterSection />
      <EconomicImpactSection />
      <CustomForecastingSection />
      <UnemploymentReportsSection />
      <Footer />
    </>
  );
}

export default HomePage;
