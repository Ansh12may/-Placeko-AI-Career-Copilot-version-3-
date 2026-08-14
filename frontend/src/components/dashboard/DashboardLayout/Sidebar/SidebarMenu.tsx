import {
  LayoutDashboard,
  FileText,
  Briefcase,
  ClipboardList,
  Mic,
  History,
  User,
  Settings,
  Sparkles,
} from "lucide-react";

import SidebarItem from "./SidebarItem";

const mainMenuItems = [
  {
    label: "Dashboard",
    icon: LayoutDashboard,
    path: "/dashboard",
  },
  {
    label: "Resume Library",
    icon: FileText,
    path: "/resume",
    
  },
  {
    label: "Resume Analysis",
    icon: Sparkles,
    path: "/resume-analysis",
  },
  {
    label: "Recommended Jobs",
    icon: Briefcase,
    path: "/jobs",
    
  },
  {
    label: "Applications Pipeline",
    icon: ClipboardList,
    path: "/applications",
    
  },
  {
    label: "AI Mock Interview",
    icon: Mic,
    path: "/interview",
  },
  {
    label: "Interview History",
    icon: History,
    path: "/interview/history",
  },
  
];

const accountMenuItems = [
  {
    label: "Candidate Profile",
    icon: User,
    path: "/profile",
  },
  {
    label: "Settings",
    icon: Settings,
    path: "/settings",
  },
];

const SidebarMenu = () => {
  return (
    <nav className="flex flex-1 flex-col px-4 py-6">

      <p className="mb-3 px-3 text-[11px] font-bold uppercase tracking-wider text-slate-400">
        Main Navigation
      </p>

      <div className="flex flex-col gap-2">
        {mainMenuItems.map((item) => (
          <SidebarItem
            key={item.label}
            icon={item.icon}
            label={item.label}
            path={item.path}
           
          />
        ))}
      </div>

      <p className="mb-3 mt-8 px-3 text-[11px] font-bold uppercase tracking-wider text-slate-400">
        Account & System
      </p>

      <div className="flex flex-col gap-2">
        {accountMenuItems.map((item) => (
          <SidebarItem
            key={item.label}
            icon={item.icon}
            label={item.label}
            path={item.path}
          />
        ))}
      </div>

    </nav>
  );
};

export default SidebarMenu;