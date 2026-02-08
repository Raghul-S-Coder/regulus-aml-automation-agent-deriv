import { useEffect, useMemo, useState } from "react";

type ThemeMode = "light" | "dark";

const storageKey = "regulus_theme";

export function useTheme() {
  const [theme, setTheme] = useState<ThemeMode>("dark");

  useEffect(() => {
    const stored = localStorage.getItem(storageKey) as ThemeMode | null;
    if (stored === "light" || stored === "dark") {
      setTheme(stored);
      return;
    }

    setTheme("dark");
  }, []);

  useEffect(() => {
    const root = document.documentElement;
    if (theme === "dark") {
      root.classList.add("dark");
    } else {
      root.classList.remove("dark");
    }
    localStorage.setItem(storageKey, theme);
  }, [theme]);

  const toggle = useMemo(() => () => setTheme((prev) => (prev === "dark" ? "light" : "dark")), []);

  return { theme, setTheme, toggle };
}
