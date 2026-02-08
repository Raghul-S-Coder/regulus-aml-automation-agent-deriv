import { useTheme } from "@/app/hooks/useTheme";

export default function ThemeToggle() {
  const { theme, toggle } = useTheme();

  return (
    <button
      type="button"
      onClick={toggle}
      className="rounded-full border border-border px-3 py-1 text-sm text-text-muted transition hover:border-brand hover:text-brand"
    >
      {theme === "dark" ? "Light" : "Dark"} Mode
    </button>
  );
}
