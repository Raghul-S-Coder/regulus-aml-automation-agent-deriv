import { useEffect, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { login } from "@/app/api/auth";
import { ApiError } from "@/app/api/client";

type FieldErrors = {
  username?: string;
  password?: string;
};

export default function LoginPage() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errors, setErrors] = useState<FieldErrors>({});
  const [formError, setFormError] = useState("");
  const [userNotFound, setUserNotFound] = useState(false);
  const [signupSuccess, setSignupSuccess] = useState(false);

  const location = useLocation();

  useEffect(() => {
    const state = location.state as { signupSuccess?: boolean } | null;
    if (!signupSuccess && state?.signupSuccess) {
      setSignupSuccess(true);
      window.history.replaceState({}, document.title);
    }
  }, [location.state, signupSuccess]);

  const validate = () => {
    const nextErrors: FieldErrors = {};
    if (!username.trim()) {
      nextErrors.username = "Username is required.";
    }
    if (!password.trim()) {
      nextErrors.password = "Password is required.";
    }
    setErrors(nextErrors);
    return Object.keys(nextErrors).length === 0;
  };

  const onSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setFormError("");
    setUserNotFound(false);
    if (!validate()) {
      return;
    }

    try {
      await login({ username, password });
      navigate("/regulus/monitoring", { replace: true });
    } catch (error) {
      if (error instanceof ApiError && error.code === "AML0902") {
        setUserNotFound(true);
        setFormError("");
      } else {
        setFormError("Unable to sign in. Please try again.");
      }
    }
  };

  return (
    <div className="max-w-md rounded-2xl border border-border bg-surface-secondary p-8">
      <h2 className="text-2xl font-semibold">Compliance Login</h2>
      <p className="mt-2 text-text-muted">
        Access the RegulusAI monitoring console.
      </p>
      {signupSuccess ? (
        <div className="mt-4 rounded-xl border border-brand/40 bg-brand/10 px-4 py-3 text-sm text-brand">
          Signup successful. Please sign in.
        </div>
      ) : null}
      {userNotFound ? (
        <div className="mt-4 rounded-xl border border-amber-500/40 bg-amber-500/10 px-4 py-3 text-sm text-amber-700">
          User not found. Please sign up for access.
        </div>
      ) : null}
      <form className="mt-6 space-y-4" onSubmit={onSubmit}>
        <div className="space-y-2">
          <label className="text-sm font-medium text-text" htmlFor="username">
            Username
          </label>
          <input
            id="username"
            name="username"
            type="text"
            autoComplete="off"
            value={username}
            onChange={(event) => setUsername(event.target.value)}
            className="w-full rounded-xl border border-border bg-surface px-3 py-2 text-sm text-text outline-none transition focus:border-brand"
            placeholder="compliance.manager"
          />
          {errors.username ? (
            <p className="text-xs text-red-500">{errors.username}</p>
          ) : null}
        </div>
        <div className="space-y-2">
          <label className="text-sm font-medium text-text" htmlFor="password">
            Password
          </label>
          <input
            id="password"
            name="password"
            type="password"
            autoComplete="off"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            className="w-full rounded-xl border border-border bg-surface px-3 py-2 text-sm text-text outline-none transition focus:border-brand"
            placeholder="••••••••"
          />
          {errors.password ? (
            <p className="text-xs text-red-500">{errors.password}</p>
          ) : null}
        </div>
        {formError ? <p className="text-xs text-red-500">{formError}</p> : null}
        <button
          type="submit"
          className="w-full rounded-full bg-brand px-4 py-2.5 text-sm font-semibold text-brand-foreground shadow-soft"
        >
          Sign in
        </button>
      </form>
      <p className="mt-4 text-xs text-text-muted">
        Need access?{" "}
        <Link to="/regulus/signup" className="text-brand hover:underline">
          Create an account
        </Link>
      </p>
    </div>
  );
}
