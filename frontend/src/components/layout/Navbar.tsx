import { LogOut } from "lucide-react";
import { useAuth } from "@/hooks/useAuth";
import DarkModeToggle from "@/components/ui/DarkModeToggle";

const Navbar = () => {
  const { logout } = useAuth();

  return (
    <header className="h-16 flex items-center justify-between px-6 border-b border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-950">
      <div className="flex items-center gap-2">
        <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-brand-500 to-brand-700 flex items-center justify-center text-white font-bold text-sm">
          QP
        </div>
        <span className="font-semibold text-lg">QueryPilot</span>
      </div>
      <div className="flex items-center gap-3">
        <DarkModeToggle />
        <button
          onClick={logout}
          className="flex items-center gap-1.5 text-sm text-gray-600 dark:text-gray-300 hover:text-red-600 dark:hover:text-red-400 transition-colors"
        >
          <LogOut size={16} />
          Logout
        </button>
      </div>
    </header>
  );
};

export default Navbar;