import SidebarLogo from "./SidebarLogo";
import SidebarMenu from "./SidebarMenu";
import SidebarProfile from "./SidebarProfile";

const Sidebar = () => {
  return (
    <aside

  className="
    flex
    flex-col
    w-[264px]
    flex-shrink-0
    border-r
    border-slate-200
    bg-white
    dark:border-slate-800
    dark:bg-slate-900
    overflow-y-auto

  "

>
      {/* Logo */}

      <SidebarLogo />

      {/* Navigation */}

      <SidebarMenu />

      {/* User Profile */}

      <SidebarProfile />
    </aside>
  );
};

export default Sidebar;