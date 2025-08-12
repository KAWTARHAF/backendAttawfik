-- Force UTF-8 decoding on import
SET client_encoding = 'UTF8';

-- UUID generator
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- ---------- ENUMS ----------
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'user_role') THEN
    CREATE TYPE user_role AS ENUM ('admin', 'manager', 'leader', 'user');
  END IF;

  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'project_status') THEN
    CREATE TYPE project_status AS ENUM ('planned', 'in_progress', 'done', 'risk');
  END IF;

  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'risk_level') THEN
    CREATE TYPE risk_level AS ENUM ('low', 'medium', 'high');
  END IF;

  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'export_format') THEN
    CREATE TYPE export_format AS ENUM ('pdf', 'excel');
  END IF;
END$$;

-- ---------- TABLES ----------
CREATE TABLE IF NOT EXISTS departments (
  id   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS services (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name          TEXT NOT NULL,
  department_id UUID REFERENCES departments(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS users (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name          TEXT NOT NULL,
  email         TEXT UNIQUE NOT NULL,
  role          user_role NOT NULL,
  department_id UUID REFERENCES departments(id) ON DELETE SET NULL,
  service_id    UUID REFERENCES services(id) ON DELETE SET NULL,
  created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS projects (
  id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name           TEXT NOT NULL,
  owner_id       UUID REFERENCES users(id) ON DELETE SET NULL,
  department_id  UUID REFERENCES departments(id) ON DELETE SET NULL,
  service_id     UUID REFERENCES services(id) ON DELETE SET NULL,
  type           TEXT,
  planned_start  DATE NOT NULL,
  planned_end    DATE NOT NULL,
  actual_start   DATE,
  actual_end     DATE,
  budget_planned DOUBLE PRECISION NOT NULL,
  budget_actual  DOUBLE PRECISION,
  status         project_status DEFAULT 'planned',
  created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS predictions (
  id                 UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id         UUID UNIQUE REFERENCES projects(id) ON DELETE CASCADE,
  delay_probability  DOUBLE PRECISION CHECK (delay_probability >= 0 AND delay_probability <= 1),
  budget_overrun_est DOUBLE PRECISION,
  risk_level         risk_level,
  shap_values        JSONB,
  created_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS project_history (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id    UUID REFERENCES projects(id) ON DELETE CASCADE,
  status        project_status,
  budget_actual DOUBLE PRECISION,
  timestamp     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  notes         TEXT
);

CREATE TABLE IF NOT EXISTS exports (
  id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id      UUID REFERENCES users(id) ON DELETE SET NULL,
  filters_used JSONB,
  format       export_format,
  timestamp    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS audit_logs (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id    UUID REFERENCES users(id) ON DELETE SET NULL,
  project_id UUID REFERENCES projects(id) ON DELETE SET NULL,
  action     TEXT NOT NULL,
  timestamp  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ---------- INDEXES (useful) ----------
CREATE INDEX IF NOT EXISTS idx_services_department_id  ON services(department_id);
CREATE INDEX IF NOT EXISTS idx_users_department_id     ON users(department_id);
CREATE INDEX IF NOT EXISTS idx_users_service_id        ON users(service_id);
CREATE INDEX IF NOT EXISTS idx_projects_owner_id       ON projects(owner_id);
CREATE INDEX IF NOT EXISTS idx_projects_department_id  ON projects(department_id);
CREATE INDEX IF NOT EXISTS idx_projects_service_id     ON projects(service_id);
CREATE INDEX IF NOT EXISTS idx_predictions_project_id  ON predictions(project_id);
CREATE INDEX IF NOT EXISTS idx_history_project_id      ON project_history(project_id);
CREATE INDEX IF NOT EXISTS idx_audit_user_id           ON audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_project_id        ON audit_logs(project_id);
