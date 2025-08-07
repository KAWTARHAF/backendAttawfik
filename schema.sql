-- ENUM types for roles, statuses, risks, and formats
CREATE TYPE user_role AS ENUM ('admin', 'manager', 'leader', 'user');
CREATE TYPE project_status AS ENUM ('planned', 'in_progress', 'done', 'risk');
CREATE TYPE risk_level AS ENUM ('low', 'medium', 'high');
CREATE TYPE export_format AS ENUM ('pdf', 'excel');

-- Departments table (e.g., Finance, IT)
CREATE TABLE departments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL
);

-- Services table (e.g., Infrastructure under IT)
CREATE TABLE services (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  department_id UUID REFERENCES departments(id) ON DELETE SET NULL
);

-- Users table with role and access level
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  role user_role NOT NULL,
  department_id UUID REFERENCES departments(id) ON DELETE SET NULL,
  service_id UUID REFERENCES services(id) ON DELETE SET NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Projects table (core dataset)
CREATE TABLE projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  owner_id UUID REFERENCES users(id) ON DELETE SET NULL,
  department_id UUID REFERENCES departments(id) ON DELETE SET NULL,
  service_id UUID REFERENCES services(id) ON DELETE SET NULL,
  type TEXT, -- e.g., "Bus scolaire", "FORASS"
  planned_start DATE NOT NULL,
  planned_end DATE NOT NULL,
  actual_start DATE,
  actual_end DATE,
  budget_planned FLOAT NOT NULL,
  budget_actual FLOAT,
  status project_status DEFAULT 'planned',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Predictions (one-to-one with projects)
CREATE TABLE predictions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id UUID UNIQUE REFERENCES projects(id) ON DELETE CASCADE,
  delay_probability FLOAT CHECK (delay_probability >= 0 AND delay_probability <= 1),
  budget_overrun_est FLOAT,
  risk_level risk_level,
  shap_values JSONB, -- for explainability using SHAP
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Historical project snapshots (for audit trail)
CREATE TABLE project_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
  status project_status,
  budget_actual FLOAT,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  notes TEXT
);

-- Exported report logs
CREATE TABLE exports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE SET NULL,
  filters_used JSONB,
  format export_format,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Audit logs for system interactions
CREATE TABLE audit_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE SET NULL,
  project_id UUID REFERENCES projects(id) ON DELETE SET NULL,
  action TEXT NOT NULL,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
