import { useAuth } from "@/hooks/useAuth";
import { useTheme } from "@/context/ThemeContext";

const SettingsPage = () => {
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();

  return (
    <div className="p-6 max-w-lg space-y-6">
      <h1 className="text-xl font-semibold">Settings</h1>

      <div className="bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl p-5 space-y-3">
        <h2 className="text-sm font-medium text-gray-500 dark:text-gray-400">Account</h2>
        <p className="text-sm">{user?.email ?? "—"}</p>
      </div>

      <div className="bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl p-5 flex items-center justify-between">
        <div>
          <h2 className="text-sm font-medium">Appearance</h2>
          <p className="text-xs text-gray-500 dark:text-gray-400">Currently: {theme}</p>
        </div>
        <button
          onClick={toggleTheme}
          className="text-sm px-3 py-1.5 rounded-lg border border-gray-200 dark:border-gray-700 hover:border-brand-500"
        >
          Toggle
        </button>
      </div>

      <button
        onClick={logout}
        className="text-sm text-red-600 dark:text-red-400 hover:underline"
      >
        Log out
      </button>
    </div>
  );
};

export default SettingsPage;