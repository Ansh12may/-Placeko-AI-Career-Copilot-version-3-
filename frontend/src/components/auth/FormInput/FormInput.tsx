import type { LucideIcon } from "lucide-react";

interface FormInputProps {
  label: string;
  type?: "text" | "email" | "password";
  placeholder?: string;
  value: string;
  onChange: (value: string) => void;
  icon?: LucideIcon;
  error?: string;
  required?: boolean;
}

const FormInput = ({
  label,
  type = "text",
  placeholder,
  value,
  onChange,
  icon: Icon,
  error,
  required = true,
}: FormInputProps) => {
  return (
    <div className="w-full">
      <label className="mb-2 block text-sm font-semibold text-slate-700 dark:text-slate-200">
        {label}
        {required && <span className="ml-1 text-red-500">*</span>}
      </label>

      <div className="relative">
        {Icon && (
          <Icon
            size={18}
            className="
              absolute
              left-4
              top-1/2
              -translate-y-1/2
              text-slate-400
            "
          />
        )}

        <input
          type={type}
          value={value}
          placeholder={placeholder}
          onChange={(event) => onChange(event.target.value)}
          className={`
            w-full
            rounded-xl
            border
            bg-slate-50
            py-3
            ${Icon ? "pl-11" : "px-4"}
            pr-4
            text-sm
            text-slate-900
            outline-none
            transition-all
            placeholder:text-slate-400
            focus:ring-2
            dark:bg-slate-800
            dark:text-white
            ${
              error
                ? "border-red-400 focus:border-red-500 focus:ring-red-100"
                : "border-slate-200 focus:border-indigo-500 focus:ring-indigo-100 dark:border-slate-700 dark:focus:border-indigo-500"
            }
          `}
        />
      </div>

      {error && (
        <p className="mt-1.5 text-xs font-medium text-red-500">
          {error}
        </p>
      )}
    </div>
  );
};

export default FormInput;