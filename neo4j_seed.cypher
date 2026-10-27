// ==============================================================================
// CAMPUS PLACEMENT PORTAL — NEO4J GRAPH DATA INGESTION (CYPHER SEED SCRIPT)
// Course: BACSE202 Database Systems | Phase: DA3 Modern Database Extension
// Database Technology: Neo4j (Graph Database)
// ==============================================================================

// Clear existing graph elements safely (for clean idempotent reload)
MATCH (n) DETACH DELETE n;

// ------------------------------------------------------------------------------
// 1. CREATE CORE ENTITY NODES
// ------------------------------------------------------------------------------

// Departments
CREATE (:Department {dept_id: "DEP001", dept_name: "Computer Science & Engineering", phone: "+91-44-2250-0101"});
CREATE (:Department {dept_id: "DEP002", dept_name: "Information Technology", phone: "+91-44-2250-0102"});
CREATE (:Department {dept_id: "DEP003", dept_name: "Artificial Intelligence & Data Science", phone: "+91-44-2250-0103"});
CREATE (:Department {dept_id: "DEP004", dept_name: "Electronics & Communication Engineering", phone: "+91-44-2250-0104"});
CREATE (:Department {dept_id: "DEP005", dept_name: "Mechanical Engineering", phone: "+91-44-2250-0105"});
CREATE (:Department {dept_id: "DEP006", dept_name: "Electrical & Electronics Engineering", phone: "+91-44-2250-0106"});

// Addresses
CREATE (:Address {address_id: "ADDR001", city: "Bengaluru", state: "Karnataka"});
CREATE (:Address {address_id: "ADDR002", city: "Chennai", state: "Tamil Nadu"});
CREATE (:Address {address_id: "ADDR003", city: "Hyderabad", state: "Telangana"});
CREATE (:Address {address_id: "ADDR004", city: "Pune", state: "Maharashtra"});
CREATE (:Address {address_id: "ADDR005", city: "Mumbai", state: "Maharashtra"});
CREATE (:Address {address_id: "ADDR006", city: "New Delhi", state: "Delhi"});

// Companies
CREATE (:Company {co_id: "CO001", co_name: "Google India", industry: "Information Technology & Cloud"});
CREATE (:Company {co_id: "CO002", co_name: "Microsoft Corporation", industry: "Software & Enterprise Cloud"});
CREATE (:Company {co_id: "CO003", co_name: "Amazon Web Services", industry: "E-Commerce & Cloud Infrastructure"});
CREATE (:Company {co_id: "CO004", co_name: "Oracle India", industry: "Enterprise Database & Applications"});
CREATE (:Company {co_id: "CO005", co_name: "Cisco Systems", industry: "Networking & Telecommunications"});
CREATE (:Company {co_id: "CO006", co_name: "Qualcomm India", industry: "Semiconductors & Embedded Systems"});
CREATE (:Company {co_id: "CO007", co_name: "Tata Consultancy Services", industry: "IT Services & Consulting"});
CREATE (:Company {co_id: "CO008", co_name: "Infosys Limited", industry: "Digital Services & Consulting"});

// Skills
CREATE (:Skill {skill_id: "SK001", skill_name: "Python Programming", category: "Programming"});
CREATE (:Skill {skill_id: "SK002", skill_name: "Java Enterprise", category: "Programming"});
CREATE (:Skill {skill_id: "SK003", skill_name: "C++ System Architecture", category: "Programming"});
CREATE (:Skill {skill_id: "SK004", skill_name: "Relational Database Design & SQL", category: "Database"});
CREATE (:Skill {skill_id: "SK005", skill_name: "Oracle PL/SQL & Stored Logic", category: "Database"});
CREATE (:Skill {skill_id: "SK006", skill_name: "Cloud Architecture (AWS/GCP)", category: "Cloud"});
CREATE (:Skill {skill_id: "SK007", skill_name: "Distributed Systems & Microservices", category: "Cloud"});
CREATE (:Skill {skill_id: "SK008", skill_name: "Machine Learning & Deep Neural Nets", category: "AI/ML"});
CREATE (:Skill {skill_id: "SK009", skill_name: "Data Structures & Algorithms", category: "Programming"});
CREATE (:Skill {skill_id: "SK010", skill_name: "Computer Networks & TCP/IP", category: "Networking"});
CREATE (:Skill {skill_id: "SK011", skill_name: "Embedded C & RTOS", category: "Hardware"});
CREATE (:Skill {skill_id: "SK012", skill_name: "System Verilog & VLSI Design", category: "Hardware"});
CREATE (:Skill {skill_id: "SK013", skill_name: "DevOps & Docker Containers", category: "Cloud"});
CREATE (:Skill {skill_id: "SK014", skill_name: "Technical Communication", category: "Soft Skills"});
CREATE (:Skill {skill_id: "SK015", skill_name: "Leadership & Team Management", category: "Soft Skills"});

// Staff Members
CREATE (:Staff {staff_id: "STF001", staff_name: "Dr. Sundararajan V.", designation: "Director - Training & Placement"});
CREATE (:Staff {staff_id: "STF002", staff_name: "Prof. Kavitha Raman", designation: "Senior Placement Officer - Tier 1 Firms"});
CREATE (:Staff {staff_id: "STF003", staff_name: "Mr. Dinesh Kumar", designation: "Placement Executive - Core Engineering"});
CREATE (:Staff {staff_id: "STF004", staff_name: "Ms. Shalini Murugan", designation: "T&P Compliance & Corporate Liaison"});

// Recruiters
CREATE (:Recruiter {recruiter_id: "REC001", name: "Aravind Swaminathan", phone: "+91-80-6721-5001", co_id: "CO001"});
CREATE (:Recruiter {recruiter_id: "REC002", name: "Deepa Krishnan", phone: "+91-80-4000-6002", co_id: "CO002"});
CREATE (:Recruiter {recruiter_id: "REC003", name: "Harish Nambiar", phone: "+91-80-3000-7003", co_id: "CO003"});
CREATE (:Recruiter {recruiter_id: "REC004", name: "Monica Sen", phone: "+91-80-2200-8004", co_id: "CO004"});
CREATE (:Recruiter {recruiter_id: "REC005", name: "Rajeev Menon", phone: "+91-80-4422-9005", co_id: "CO005"});
CREATE (:Recruiter {recruiter_id: "REC006", name: "Sunita Rao", phone: "+91-22-6778-1001", co_id: "CO007"});
CREATE (:Recruiter {recruiter_id: "REC007", name: "Pradeep Shenoy", phone: "+91-80-2852-0261", co_id: "CO008"});
CREATE (:Recruiter {recruiter_id: "REC008", name: "Karthik Balan", phone: "+91-80-4112-3456", co_id: "CO006"});

// Connect Recruiters to Companies
MATCH (r:Recruiter), (c:Company) WHERE r.co_id = c.co_id
CREATE (r)-[:WORKS_FOR]->(c);

// Job Postings
CREATE (:Job {job_id: "JOB001", title: "Software Development Engineer - I", package_lpa: 42.50, min_cgpa: 8.50, co_id: "CO001"});
CREATE (:Job {job_id: "JOB002", title: "Cloud Systems & AI Engineer", package_lpa: 38.00, min_cgpa: 8.00, co_id: "CO002"});
CREATE (:Job {job_id: "JOB003", title: "Backend SDE (Distributed Systems)", package_lpa: 34.00, min_cgpa: 8.00, co_id: "CO003"});
CREATE (:Job {job_id: "JOB004", title: "Database Kernel Engineer", package_lpa: 28.50, min_cgpa: 7.50, co_id: "CO004"});
CREATE (:Job {job_id: "JOB005", title: "Network Systems Software Engineer", package_lpa: 22.00, min_cgpa: 7.00, co_id: "CO005"});
CREATE (:Job {job_id: "JOB006", title: "Embedded Firmware Engineer", package_lpa: 24.00, min_cgpa: 7.00, co_id: "CO006"});
CREATE (:Job {job_id: "JOB007", title: "Digital Solutions Engineer", package_lpa: 9.50, min_cgpa: 6.50, co_id: "CO007"});
CREATE (:Job {job_id: "JOB008", title: "Systems Analyst Trainee", package_lpa: 7.20, min_cgpa: 6.00, co_id: "CO008"});

// Connect Jobs to Companies
MATCH (j:Job), (c:Company) WHERE j.co_id = c.co_id
CREATE (j)-[:POSTED_BY]->(c);

// Students
CREATE (:Student {roll_no: "25BCE5227", name: "Shashwat Siddhant", email: "shashwat.siddhant2025@campus.edu", cgpa: 9.40, dept_id: "DEP001", address_id: "ADDR001"});
CREATE (:Student {roll_no: "25BCE5392", name: "Srnav Semwal", email: "srnav.semwal2025@campus.edu", cgpa: 9.25, dept_id: "DEP001", address_id: "ADDR002"});
CREATE (:Student {roll_no: "25BAI3003", name: "Priya Sharma", email: "priya.sharma@campus.edu", cgpa: 9.10, dept_id: "DEP003", address_id: "ADDR003"});
CREATE (:Student {roll_no: "25BCE1001", name: "Ananya Iyer", email: "ananya.iyer@campus.edu", cgpa: 8.90, dept_id: "DEP001", address_id: "ADDR004"});
CREATE (:Student {roll_no: "25BIT2015", name: "Neha Kulkarni", email: "neha.kulkarni@campus.edu", cgpa: 8.75, dept_id: "DEP002", address_id: "ADDR005"});
CREATE (:Student {roll_no: "25BIT2002", name: "Rohan Gupta", email: "rohan.gupta@campus.edu", cgpa: 8.50, dept_id: "DEP002", address_id: "ADDR001"});
CREATE (:Student {roll_no: "25BEE6006", name: "Meera Reddy", email: "meera.reddy@campus.edu", cgpa: 8.10, dept_id: "DEP006", address_id: "ADDR003"});
CREATE (:Student {roll_no: "25BEC4004", name: "Vikram Patel", email: "vikram.patel@campus.edu", cgpa: 7.80, dept_id: "DEP004", address_id: "ADDR006"});
CREATE (:Student {roll_no: "25BME5005", name: "Aditya Verma", email: "aditya.verma@campus.edu", cgpa: 7.20, dept_id: "DEP005", address_id: "ADDR004"});
CREATE (:Student {roll_no: "25BCE1010", name: "Kabir Das", email: "kabir.das@campus.edu", cgpa: 6.80, dept_id: "DEP001", address_id: "ADDR002"});

// Connect Students to Departments and Addresses
MATCH (s:Student), (d:Department) WHERE s.dept_id = d.dept_id
CREATE (s)-[:ENROLLED_IN]->(d);

MATCH (s:Student), (a:Address) WHERE s.address_id = a.address_id
CREATE (s)-[:LOCATED_IN]->(a);

// ------------------------------------------------------------------------------
// 2. CONNECT STUDENT SKILLS (HAS_SKILL Relationships)
// ------------------------------------------------------------------------------
UNWIND [
  {roll: "25BCE5227", skill: "SK001"}, {roll: "25BCE5227", skill: "SK004"}, {roll: "25BCE5227", skill: "SK005"}, {roll: "25BCE5227", skill: "SK007"}, {roll: "25BCE5227", skill: "SK009"},
  {roll: "25BCE5392", skill: "SK002"}, {roll: "25BCE5392", skill: "SK004"}, {roll: "25BCE5392", skill: "SK006"}, {roll: "25BCE5392", skill: "SK007"}, {roll: "25BCE5392", skill: "SK009"},
  {roll: "25BAI3003", skill: "SK001"}, {roll: "25BAI3003", skill: "SK008"}, {roll: "25BAI3003", skill: "SK006"}, {roll: "25BAI3003", skill: "SK009"},
  {roll: "25BCE1001", skill: "SK001"}, {roll: "25BCE1001", skill: "SK002"}, {roll: "25BCE1001", skill: "SK004"}, {roll: "25BCE1001", skill: "SK009"},
  {roll: "25BIT2015", skill: "SK002"}, {roll: "25BIT2015", skill: "SK004"}, {roll: "25BIT2015", skill: "SK006"}, {roll: "25BIT2015", skill: "SK013"},
  {roll: "25BIT2002", skill: "SK001"}, {roll: "25BIT2002", skill: "SK004"}, {roll: "25BIT2002", skill: "SK009"},
  {roll: "25BEE6006", skill: "SK001"}, {roll: "25BEE6006", skill: "SK010"}, {roll: "25BEE6006", skill: "SK014"},
  {roll: "25BEC4004", skill: "SK003"}, {roll: "25BEC4004", skill: "SK011"}, {roll: "25BEC4004", skill: "SK012"}
] AS item
MATCH (s:Student {roll_no: item.roll}), (sk:Skill {skill_id: item.skill})
CREATE (s)-[:HAS_SKILL]->(sk);

// ------------------------------------------------------------------------------
// 3. CONNECT JOB REQUIRED SKILLS (REQUIRES_SKILL Relationships)
// ------------------------------------------------------------------------------
UNWIND [
  {job: "JOB001", skill: "SK001"}, {job: "JOB001", skill: "SK007"}, {job: "JOB001", skill: "SK009"},
  {job: "JOB002", skill: "SK001"}, {job: "JOB002", skill: "SK006"}, {job: "JOB002", skill: "SK008"},
  {job: "JOB003", skill: "SK002"}, {job: "JOB003", skill: "SK006"}, {job: "JOB003", skill: "SK007"}, {job: "JOB003", skill: "SK009"},
  {job: "JOB004", skill: "SK003"}, {job: "JOB004", skill: "SK004"}, {job: "JOB004", skill: "SK005"},
  {job: "JOB005", skill: "SK003"}, {job: "JOB005", skill: "SK010"},
  {job: "JOB006", skill: "SK003"}, {job: "JOB006", skill: "SK011"}, {job: "JOB006", skill: "SK012"},
  {job: "JOB007", skill: "SK001"}, {job: "JOB007", skill: "SK004"}, {job: "JOB007", skill: "SK014"},
  {job: "JOB008", skill: "SK002"}, {job: "JOB008", skill: "SK004"}
] AS req
MATCH (j:Job {job_id: req.job}), (sk:Skill {skill_id: req.skill})
CREATE (j)-[:REQUIRES_SKILL]->(sk);

// ------------------------------------------------------------------------------
// 4. CREATE APPLICATIONS & PIPELINE RELATIONSHIPS
// ------------------------------------------------------------------------------
UNWIND [
  {app_id: "APP001", roll: "25BCE5227", job: "JOB001", staff: "STF002", status: "Hired"},
  {app_id: "APP002", roll: "25BCE5392", job: "JOB003", staff: "STF002", status: "Hired"},
  {app_id: "APP003", roll: "25BAI3003", job: "JOB002", staff: "STF002", status: "Hired"},
  {app_id: "APP004", roll: "25BCE1001", job: "JOB001", staff: "STF002", status: "Interviewing"},
  {app_id: "APP005", roll: "25BIT2002", job: "JOB003", staff: "STF002", status: "Interviewing"},
  {app_id: "APP006", roll: "25BIT2015", job: "JOB002", staff: "STF002", status: "Shortlisted"},
  {app_id: "APP007", roll: "25BCE5227", job: "JOB004", staff: "STF002", status: "Shortlisted"},
  {app_id: "APP008", roll: "25BEC4004", job: "JOB005", staff: "STF003", status: "Shortlisted"},
  {app_id: "APP009", roll: "25BEE6006", job: "JOB007", staff: "STF003", status: "Hired"},
  {app_id: "APP010", roll: "25BME5005", job: "JOB007", staff: "STF003", status: "Interviewing"},
  {app_id: "APP011", roll: "25BCE1010", job: "JOB007", staff: "STF003", status: "Pending"},
  {app_id: "APP012", roll: "25BEC4004", job: "JOB006", staff: "STF003", status: "Pending"}
] AS app_data
MATCH (s:Student {roll_no: app_data.roll})
MATCH (j:Job {job_id: app_data.job})
MATCH (st:Staff {staff_id: app_data.staff})
CREATE (app:Application {app_id: app_data.app_id, status: app_data.status})
CREATE (s)-[:SUBMITTED]->(app)
CREATE (app)-[:FOR_JOB]->(j)
CREATE (app)-[:MANAGED_BY]->(st);

// ------------------------------------------------------------------------------
// 5. CREATE INTERVIEWS & CONDUCTED_BY RELATIONSHIPS
// ------------------------------------------------------------------------------
UNWIND [
  {interview_id: "INT001", app_id: "APP001", rec_id: "REC001", mode: "Online", result: "Cleared"},
  {interview_id: "INT002", app_id: "APP002", rec_id: "REC003", mode: "Online", result: "Cleared"},
  {interview_id: "INT003", app_id: "APP003", rec_id: "REC002", mode: "Online", result: "Cleared"},
  {interview_id: "INT004", app_id: "APP004", rec_id: "REC001", mode: "In-Person", result: "Pending"},
  {interview_id: "INT005", app_id: "APP005", rec_id: "REC003", mode: "Online", result: "Pending"},
  {interview_id: "INT006", app_id: "APP009", rec_id: "REC006", mode: "In-Person", result: "Cleared"}
] AS int_data
MATCH (app:Application {app_id: int_data.app_id})
MATCH (r:Recruiter {recruiter_id: int_data.rec_id})
CREATE (i:Interview {interview_id: int_data.interview_id, mode: int_data.mode, result: int_data.result})
CREATE (app)-[:ADVANCED_TO]->(i)
CREATE (i)-[:INTERVIEWED_BY]->(r);

// ------------------------------------------------------------------------------
// 6. CREATE OFFERS & RESULTED_IN RELATIONSHIPS
// ------------------------------------------------------------------------------
UNWIND [
  {offer_id: "OFR001", app_id: "APP001", package_offered: 42.50, status: "Accepted"},
  {offer_id: "OFR002", app_id: "APP002", package_offered: 34.00, status: "Accepted"},
  {offer_id: "OFR003", app_id: "APP003", package_offered: 38.00, status: "Accepted"},
  {offer_id: "OFR004", app_id: "APP009", package_offered: 9.50, status: "Accepted"}
] AS ofr_data
MATCH (app:Application {app_id: ofr_data.app_id})
CREATE (o:Offer {offer_id: ofr_data.offer_id, package_offered: ofr_data.package_offered, offer_status: ofr_data.status})
CREATE (app)-[:RESULTED_IN]->(o);
