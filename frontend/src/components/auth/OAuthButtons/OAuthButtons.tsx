
interface OAuthButtonsProps {
  onGoogle: () => void;
  onGithub: () => void;
}

const OAuthButtons = ({
  onGoogle,
  
}: OAuthButtonsProps) => {
  return (
    <div className="space-y-3">

      {/* Google */}

      <button
        type="button"
        onClick={onGoogle}
        className="
          flex
          w-full
          items-center
          justify-center
          gap-3
          rounded-xl
          border
          border-slate-200
          bg-white
          px-4
          py-3
          text-sm
          font-semibold
          text-slate-700
          transition-all
          hover:bg-slate-50
          hover:shadow-sm
          dark:border-slate-700
          dark:bg-slate-800
          dark:text-slate-200
          dark:hover:bg-slate-700
        "
      >
        <span className="text-lg font-bold">G</span>

        Continue with Google
      </button>

      
    </div>
  );
};

export default OAuthButtons;