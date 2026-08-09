interface RoleSelectorProps {
  selectedRole: string;
  onRoleChange: (role: string) => void;
}

const roles = [
  "Frontend Engineer",
  "Backend Engineer",
  "AI Engineer",
  "Full Stack Developer",
];

const RoleSelector = ({
  selectedRole,
  onRoleChange,
}: RoleSelectorProps) => {
  return (
    <div className="flex flex-wrap gap-3">
      {roles.map((role) => (
        <button
          key={role}
          onClick={() => onRoleChange(role)}
          className={`
            rounded-lg
            px-4
            py-2
            text-sm
            font-semibold
            transition-all
            duration-300

            ${
              selectedRole === role
                ? "bg-indigo-600 text-white shadow-md"
                : "bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700"
            }
          `}
        >
          {role}
        </button>
      ))}
    </div>
  );
};

export default RoleSelector;