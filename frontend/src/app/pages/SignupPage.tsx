import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { signup } from "@/app/api/auth";

type FieldErrors = {
  organization_id?: string;
  username?: string;
  full_name?: string;
  email?: string;
  user_type?: string;
  password?: string;
};

export default function SignupPage() {
  const navigate = useNavigate();
  const [organizationId, setOrganizationId] = useState("ORG-0001");
  const [username, setUsername] = useState("");
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [userType, setUserType] = useState("compliance_manager");
  const [password, setPassword] = useState("");
  const [errors, setErrors] = useState<FieldErrors>({});
  const [formError, setFormError] = useState("");
  const [showSuccess, setShowSuccess] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/;

  const validate = () => {
    const nextErrors: FieldErrors = {};
    if (!organizationId.trim()) {
      nextErrors.organization_id = "Organization ID is required.";
    }
    if (!username.trim()) {
      nextErrors.username = "Username is required.";
    }
    if (!fullName.trim()) {
      nextErrors.full_name = "Full name is required.";
    }
    if (!email.trim()) {
      nextErrors.email = "Email is required.";
    } else if (!emailRegex.test(email)) {
      nextErrors.email = "Enter a valid email address.";
    }
    if (!userType.trim()) {
      nextErrors.user_type = "User type is required.";
    }
    if (!password.trim()) {
      nextErrors.password = "Password is required.";
    } else if (!passwordRegex.test(password)) {
      nextErrors.password =
        "Password must be 8+ chars with uppercase, lowercase, and a number.";
    }
    setErrors(nextErrors);
    return Object.keys(nextErrors).length === 0;
  };

  const onSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setFormError("");
    if (!validate()) {
      return;
    }
    setIsSubmitting(true);
    try {
      await signup({
        organization_id: organizationId,
        username,
        full_name: fullName,
        email,
        user_type: userType,
        password
      });
      setShowSuccess(true);
      navigate("/regulus/login", {
        replace: true,
        state: { signupSuccess: true }
      });
    } catch (error) {
      setFormError("Unable to create account. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-lg rounded-2xl border border-border bg-surface-secondary p-8">
      {showSuccess ? (
        <div className="mb-4 rounded-xl border border-brand/40 bg-brand/10 px-4 py-3 text-sm text-brand">
          Signup successful. Redirecting to login...
        </div>
      ) : null}
      <h2 className="text-2xl font-semibold">Create Account</h2>
      <p className="mt-2 text-text-muted">
        Register a compliance manager account for RegulusAI.
      </p>
      <form className="mt-6 space-y-4" onSubmit={onSubmit}>
        <div className="space-y-2">
          <label className="text-sm font-medium text-text" htmlFor="organizationId">
            Organization ID
          </label>
          <input
            id="organizationId"
            autoComplete="off"
            value={organizationId}
            onChange={(event) => setOrganizationId(event.target.value)}
            className="w-full rounded-xl border border-border bg-surface px-3 py-2 text-sm text-text outline-none transition focus:border-brand"
            placeholder="ORG-0001"
          />
          {errors.organization_id ? (
            <p className="text-xs text-red-500">{errors.organization_id}</p>
          ) : null}
        </div>
        <div className="space-y-2">
          <label className="text-sm font-medium text-text" htmlFor="username">
            Username
          </label>
          <input
            id="username"
            autoComplete="off"
            value={username}
            onChange={(event) => setUsername(event.target.value)}
            className="w-full rounded-xl border border-border bg-surface px-3 py-2 text-sm text-text outline-none transition focus:border-brand"
            placeholder="compliance.manager"
          />
          {errors.username ? <p className="text-xs text-red-500">{errors.username}</p> : null}
        </div>
        <div className="space-y-2">
          <label className="text-sm font-medium text-text" htmlFor="fullName">
            Full name
          </label>
          <input
            id="fullName"
            autoComplete="off"
            value={fullName}
            onChange={(event) => setFullName(event.target.value)}
            className="w-full rounded-xl border border-border bg-surface px-3 py-2 text-sm text-text outline-none transition focus:border-brand"
            placeholder="Ariana Collins"
          />
          {errors.full_name ? <p className="text-xs text-red-500">{errors.full_name}</p> : null}
        </div>
        <div className="space-y-2">
          <label className="text-sm font-medium text-text" htmlFor="email">
            Email
          </label>
          <input
            id="email"
            type="email"
            autoComplete="off"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            className="w-full rounded-xl border border-border bg-surface px-3 py-2 text-sm text-text outline-none transition focus:border-brand"
            placeholder="analyst@regulus.ai"
          />
          {errors.email ? <p className="text-xs text-red-500">{errors.email}</p> : null}
        </div>
        <div className="space-y-2">
          <label className="text-sm font-medium text-text" htmlFor="userType">
            User type
          </label>
          <select
            id="userType"
            value={userType}
            onChange={(event) => setUserType(event.target.value)}
            className="w-full rounded-xl border border-border bg-surface px-3 py-2 text-sm text-text outline-none transition focus:border-brand"
          >
            <option value="compliance_manager">Compliance Manager</option>
            <option value="admin">Admin</option>
          </select>
          {errors.user_type ? <p className="text-xs text-red-500">{errors.user_type}</p> : null}
        </div>
        <div className="space-y-2">
          <label className="text-sm font-medium text-text" htmlFor="password">
            Password
          </label>
          <input
            id="password"
            type="password"
            autoComplete="off"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            className="w-full rounded-xl border border-border bg-surface px-3 py-2 text-sm text-text outline-none transition focus:border-brand"
            placeholder="••••••••"
          />
          {errors.password ? <p className="text-xs text-red-500">{errors.password}</p> : null}
        </div>
        {formError ? <p className="text-xs text-red-500">{formError}</p> : null}
        <button
          type="submit"
          disabled={isSubmitting}
          className="w-full rounded-full bg-brand px-4 py-2.5 text-sm font-semibold text-brand-foreground shadow-soft disabled:opacity-70"
        >
          {isSubmitting ? "Creating..." : "Create Account"}
        </button>
      </form>
      <p className="mt-4 text-xs text-text-muted">
        Already have access?{" "}
        <Link to="/regulus/login" className="text-brand hover:underline">
          Sign in
        </Link>
      </p>
    </div>
  );
}
