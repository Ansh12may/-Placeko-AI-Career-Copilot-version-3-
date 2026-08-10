import { FaGithub, FaLinkedin } from "react-icons/fa";
import {
  Mail,
  Heart,
} from "lucide-react";

const Footer = () => {
  return (
    <footer className="bg-slate-950 text-slate-400">
      <div className="mx-auto max-w-7xl px-6 py-16">

        {/* Top Section */}

        <div className="grid gap-12 md:grid-cols-4">

          {/* Brand */}

          <div className="space-y-5">
            <h2 className="text-3xl font-black text-white">
              Placeko
            </h2>

            <p className="leading-7">
              AI Career Copilot helping students build stronger resumes,
              prepare for interviews, discover better jobs, and land
              their dream careers.
            </p>
          </div>

          {/* Product */}

          <div>
            <h3 className="mb-5 text-lg font-bold text-white">
              Product
            </h3>

            <ul className="space-y-3">

              <li><a href="#" className="hover:text-white">Dashboard</a></li>

              <li><a href="#" className="hover:text-white">Resume Analysis</a></li>

              <li><a href="#" className="hover:text-white">Job Matching</a></li>

              <li><a href="#" className="hover:text-white">Mock Interview</a></li>

              <li><a href="#" className="hover:text-white">Application Tracking</a></li>

            </ul>
          </div>

          {/* Resources */}

          <div>
            <h3 className="mb-5 text-lg font-bold text-white">
              Resources
            </h3>

            <ul className="space-y-3">

              <li><a href="#" className="hover:text-white">Documentation</a></li>

              <li><a href="#" className="hover:text-white">Help Center</a></li>

              <li><a href="#" className="hover:text-white">Privacy Policy</a></li>

              <li><a href="#" className="hover:text-white">Terms of Service</a></li>

              <li><a href="#" className="hover:text-white">Contact</a></li>

            </ul>
          </div>

          {/* Connect */}

          <div>
            <h3 className="mb-5 text-lg font-bold text-white">
              Connect
            </h3>

            <div className="space-y-4">

              <a
                href="#"
                className="flex items-center gap-3 hover:text-white"
              >
                <FaGithub size={20} />
                GitHub
              </a>

              <a
                href="#"
                className="flex items-center gap-3 hover:text-white"
              >
                <FaLinkedin size={20} />
                LinkedIn
              </a>

              <a
                href="#"
                className="flex items-center gap-3 hover:text-white"
              >
                <Mail size={20} />
                Email
              </a>

            </div>
          </div>

        </div>

        {/* Divider */}

        <div className="my-10 h-px bg-slate-800" />

        {/* Bottom */}

        <div className="flex flex-col items-center justify-between gap-4 md:flex-row">

          <p className="text-sm">
            © 2026 Placeko. All rights reserved.
          </p>

          <div className="flex items-center gap-2 text-sm">
            Built with
            <Heart
              size={16}
              className="fill-red-500 text-red-500"
            />
            by Ashutosh Kushwaha
          </div>

        </div>

      </div>
    </footer>
  );
};

export default Footer;