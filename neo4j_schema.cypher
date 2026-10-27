// ==============================================================================
// CAMPUS PLACEMENT PORTAL — NEO4J GRAPH DATABASE SCHEMA (CYPHER DDL)
// Course: BACSE202 Database Systems | Phase: DA3 Modern Database Extension
// Database Technology: Neo4j (Graph Database)
// ==============================================================================

// ------------------------------------------------------------------------------
// 1. UNIQUE NODE CONSTRAINTS (Enforcing Referential Integrity & Graph Uniqueness)
// ------------------------------------------------------------------------------

// Unique constraint on Student roll_no
CREATE CONSTRAINT cst_student_roll IF NOT EXISTS
FOR (s:Student) REQUIRE s.roll_no IS UNIQUE;

// Unique constraint on Student email
CREATE CONSTRAINT cst_student_email IF NOT EXISTS
FOR (s:Student) REQUIRE s.email IS UNIQUE;

// Unique constraint on Department dept_id
CREATE CONSTRAINT cst_department_id IF NOT EXISTS
FOR (d:Department) REQUIRE d.dept_id IS UNIQUE;

// Unique constraint on Department dept_name
CREATE CONSTRAINT cst_department_name IF NOT EXISTS
FOR (d:Department) REQUIRE d.dept_name IS UNIQUE;

// Unique constraint on Address address_id
CREATE CONSTRAINT cst_address_id IF NOT EXISTS
FOR (a:Address) REQUIRE a.address_id IS UNIQUE;

// Unique constraint on Company co_id
CREATE CONSTRAINT cst_company_id IF NOT EXISTS
FOR (c:Company) REQUIRE c.co_id IS UNIQUE;

// Unique constraint on Company co_name
CREATE CONSTRAINT cst_company_name IF NOT EXISTS
FOR (c:Company) REQUIRE c.co_name IS UNIQUE;

// Unique constraint on Skill skill_id
CREATE CONSTRAINT cst_skill_id IF NOT EXISTS
FOR (sk:Skill) REQUIRE sk.skill_id IS UNIQUE;

// Unique constraint on Skill skill_name
CREATE CONSTRAINT cst_skill_name IF NOT EXISTS
FOR (sk:Skill) REQUIRE sk.skill_name IS UNIQUE;

// Unique constraint on Recruiter recruiter_id
CREATE CONSTRAINT cst_recruiter_id IF NOT EXISTS
FOR (r:Recruiter) REQUIRE r.recruiter_id IS UNIQUE;

// Unique constraint on Job posting job_id
CREATE CONSTRAINT cst_job_id IF NOT EXISTS
FOR (j:Job) REQUIRE j.job_id IS UNIQUE;

// Unique constraint on Staff staff_id
CREATE CONSTRAINT cst_staff_id IF NOT EXISTS
FOR (st:Staff) REQUIRE st.staff_id IS UNIQUE;

// Unique constraint on Application app_id
CREATE CONSTRAINT cst_app_id IF NOT EXISTS
FOR (app:Application) REQUIRE app.app_id IS UNIQUE;

// Unique constraint on Interview interview_id
CREATE CONSTRAINT cst_interview_id IF NOT EXISTS
FOR (i:Interview) REQUIRE i.interview_id IS UNIQUE;

// Unique constraint on Offer offer_id
CREATE CONSTRAINT cst_offer_id IF NOT EXISTS
FOR (o:Offer) REQUIRE o.offer_id IS UNIQUE;

// ------------------------------------------------------------------------------
// 2. PERFORMANCE INDEXES (Optimizing High-Frequency Traversal Filters)
// ------------------------------------------------------------------------------

// Index on Student CGPA for rapid range-filtering in eligibility queries
CREATE INDEX idx_student_cgpa IF NOT EXISTS
FOR (s:Student) ON (s.cgpa);

// Index on Job package_lpa for compensation ranking
CREATE INDEX idx_job_package IF NOT EXISTS
FOR (j:Job) ON (j.package_lpa);

// Index on Job min_cgpa for eligibility cutoff checks
CREATE INDEX idx_job_min_cgpa IF NOT EXISTS
FOR (j:Job) ON (j.min_cgpa);

// Index on Application status for lifecycle monitoring
CREATE INDEX idx_app_status IF NOT EXISTS
FOR (app:Application) ON (app.status);

// Index on Skill category for domain-specific taxonomy searches
CREATE INDEX idx_skill_category IF NOT EXISTS
FOR (sk:Skill) ON (sk.category);
