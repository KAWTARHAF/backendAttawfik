-- =========================================
-- RESET AND RECREATE DATABASE STRUCTURE
-- =========================================

-- Step 1: Drop tables in dependency order
DROP TABLE IF EXISTS audit_logs CASCADE;
DROP TABLE IF EXISTS exports CASCADE;
DROP TABLE IF EXISTS project_history CASCADE;
DROP TABLE IF EXISTS predictions CASCADE;
DROP TABLE IF EXISTS projects CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS services CASCADE;
DROP TABLE IF EXISTS departments CASCADE;

-- Step 2: Drop ENUM types
DROP TYPE IF EXISTS user_role CASCADE;
DROP TYPE IF EXISTS project_status CASCADE;
DROP TYPE IF EXISTS risk_level CASCADE;
DROP TYPE IF EXISTS export_format CASCADE;

-- Step 3: Recreate ENUM types
CREATE TYPE user_role AS ENUM ('admin', 'manager', 'leader', 'user');
CREATE TYPE project_status AS ENUM ('planned', 'in_progress', 'done', 'risk');
CREATE TYPE risk_level AS ENUM ('low', 'medium', 'high');
CREATE TYPE export_format AS ENUM ('pdf', 'excel');

-- Step 4: Recreate tables

-- Departments
CREATE TABLE departments (
  id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL
);

-- Services
CREATE TABLE services (
  id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  department_id BIGINT REFERENCES departments(id) ON DELETE SET NULL
);

-- Users
CREATE TABLE users (
  id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  role user_role NOT NULL,
  department_id BIGINT REFERENCES departments(id) ON DELETE SET NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Projects
CREATE TABLE projects (
  id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  owner_id BIGINT REFERENCES users(id) ON DELETE SET NULL,
  department_id BIGINT REFERENCES departments(id) ON DELETE SET NULL,
  service_id BIGINT REFERENCES services(id) ON DELETE SET NULL,
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

-- Predictions
CREATE TABLE predictions (
  id BIGSERIAL PRIMARY KEY,
  project_id BIGINT UNIQUE REFERENCES projects(id) ON DELETE CASCADE,
  delay_probability FLOAT CHECK (delay_probability >= 0 AND delay_probability <= 1),
  budget_overrun_est FLOAT,
  risk_level risk_level,
  shap_values JSONB,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Project History
CREATE TABLE project_history (
  id BIGSERIAL PRIMARY KEY,
  project_id BIGINT REFERENCES projects(id) ON DELETE CASCADE,
  status project_status,
  budget_actual FLOAT,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  notes TEXT
);

-- Exports
CREATE TABLE exports (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT REFERENCES users(id) ON DELETE SET NULL,
  filters_used JSONB,
  format export_format,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Audit Logs
CREATE TABLE audit_logs (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT REFERENCES users(id) ON DELETE SET NULL,
  project_id BIGINT REFERENCES projects(id) ON DELETE SET NULL,
  action TEXT NOT NULL,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
