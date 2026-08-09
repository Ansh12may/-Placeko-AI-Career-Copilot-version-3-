import LandingNavbar from "../../components/landing/Navbar/LandingNavbar";
import Hero from "../../components/landing/Hero/Hero";
import InteractiveDemo from "../../components/landing/InteractiveDemo/InteractiveDemo";
import type { NavigationTab } from "../../types";
import Features from "../../components/landing/Features/Features";
import Workflow from "../../components/landing/workflow/Workflow"
import CTA from "../../components/landing/CTA/CTA";
import Footer from "../../components/landing/Footer/Footer";

interface LandingPageProps {
  onNavigate: (tab: NavigationTab) => void;
  isDarkMode: boolean;
  onToggleDarkMode: () => void;
}

function LandingPage({
  onNavigate,
  isDarkMode,
  onToggleDarkMode,
}: LandingPageProps) {
  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 transition-colors">
      <LandingNavbar
        onNavigate={onNavigate}
        isDarkMode={isDarkMode}
        onToggleDarkMode={onToggleDarkMode}
      />

      <Hero
        onGetStarted={() => onNavigate("auth")}
        onExploreDemo={() => onNavigate("dashboard")}
      />

      <InteractiveDemo />
      <Features/>
      <Workflow/>
      <CTA onGetStarted={() => onNavigate("auth")}/>
      <Footer/>

    </div>
  );
}

export default LandingPage;