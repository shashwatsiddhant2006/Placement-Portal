// ==============================================================================
// CAMPUS PLACEMENT PORTAL — TECHNOLOGY-SPECIFIC GRAPH QUERIES (NEO4J CYPHER)
// Course: BACSE202 Database Systems | Phase: DA3 Modern Database Extension
// Database Technology: Neo4j (Graph Database)
// ==============================================================================

// ------------------------------------------------------------------------------
// QUERY 1: Instant Graph-Based Eligibility & Skill Match Percentage
// Purpose: For a target student (e.g. '25BCE5227'), find all jobs where they
//          satisfy min_cgpa, calculate how many required skills they hold,
//          and rank jobs by match percentage.
// Relational Contrast: In SQL, this requires 3 JOINs + COUNT(DISTINCT) + GROUP BY.
//                      In Graph, it is a direct 2-hop pattern traversal.
// ------------------------------------------------------------------------------
MATCH (s:Student {roll_no: "25BCE5227"})
MATCH (j:Job)-[:POSTED_BY]->(c:Company)
WHERE s.cgpa >= j.min_cgpa
OPTIONAL MATCH (j)-[:REQUIRES_SKILL]->(req:Skill)
WITH s, j, c, count(req) AS total_required_skills
OPTIONAL MATCH (s)-[:HAS_SKILL]->(sk:Skill)<-[:REQUIRES_SKILL]-(j)
WITH s, j, c, total_required_skills, count(sk) AS matched_skills, collect(sk.skill_name) AS matching_skill_list
RETURN j.job_id AS JobID,
       j.title AS JobRole,
       c.co_name AS Company,
       j.package_lpa AS PackageLPA,
       j.min_cgpa AS CutoffCGPA,
       s.cgpa AS StudentCGPA,
       matched_skills AS MatchedSkillsCount,
       total_required_skills AS TotalRequiredSkills,
       round(100.0 * matched_skills / total_required_skills, 1) AS MatchPercentage,
       matching_skill_list AS MatchedSkills
ORDER BY MatchPercentage DESC, PackageLPA DESC;

// ------------------------------------------------------------------------------
// QUERY 2: Skill Gap Analysis (Set Difference on Graph Relationships)
// Purpose: Given a target student and a dream role (e.g. Google SDE-I / JOB001),
//          compute the exact missing skill nodes that prevent 100% suitability.
// Relational Contrast: SQL requires complex EXCEPT or NOT EXISTS subqueries.
//                      Graph simply finds required skill nodes NOT linked to Student.
// ------------------------------------------------------------------------------
MATCH (s:Student {roll_no: "25BCE1001"}), (j:Job {job_id: "JOB001"})
MATCH (j)-[:REQUIRES_SKILL]->(needed:Skill)
WHERE NOT (s)-[:HAS_SKILL]->(needed)
RETURN s.name AS StudentName,
       s.roll_no AS RollNo,
       j.title AS DreamJob,
       needed.skill_id AS MissingSkillID,
       needed.skill_name AS MissingSkillName,
       needed.category AS DomainCategory;

// ------------------------------------------------------------------------------
// QUERY 3: Reverse Recruiter Candidate Discovery & Ranking
// Purpose: When a recruiter reviews applicants for their job opening (e.g. JOB003),
//          traverse to eligible students and score them by skill alignment.
// ------------------------------------------------------------------------------
MATCH (j:Job {job_id: "JOB003"})-[:REQUIRES_SKILL]->(req:Skill)
WITH j, count(req) AS total_required
MATCH (s:Student)-[:ENROLLED_IN]->(d:Department)
WHERE s.cgpa >= j.min_cgpa
OPTIONAL MATCH (s)-[:HAS_SKILL]->(sk:Skill)<-[:REQUIRES_SKILL]-(j)
WITH j, s, d, total_required, count(sk) AS matched_count, collect(sk.skill_name) AS shared_skills
WHERE matched_count > 0
RETURN s.roll_no AS RollNo,
       s.name AS CandidateName,
       d.dept_name AS Department,
       s.cgpa AS CGPA,
       matched_count AS MatchedSkills,
       total_required AS TotalRequired,
       round(100.0 * matched_count / total_required, 1) AS FitScorePercent,
       shared_skills AS VerifiedSkills
ORDER BY FitScorePercent DESC, s.cgpa DESC;

// ------------------------------------------------------------------------------
// QUERY 4: Collaborative Peer Skill Similarity (Jaccard Index on Graph)
// Purpose: Find students with highest skill overlap for peer-learning and mock
//          interview pairs, using intersection over union of HAS_SKILL edges.
// Relational Contrast: In SQL, pairwise Jaccard index requires self-joins on millions
//                      of rows, resulting in exponential O(N^2) join overhead.
// ------------------------------------------------------------------------------
MATCH (s1:Student {roll_no: "25BCE5227"})-[:HAS_SKILL]->(sk:Skill)<-[:HAS_SKILL]-(s2:Student)
WHERE s1 <> s2
WITH s1, s2, count(sk) AS intersection_count, collect(sk.skill_name) AS common_skills
MATCH (s1)-[:HAS_SKILL]->(sk1:Skill)
WITH s1, s2, intersection_count, common_skills, count(sk1) AS s1_skills
MATCH (s2)-[:HAS_SKILL]->(sk2:Skill)
WITH s1, s2, intersection_count, common_skills, s1_skills, count(sk2) AS s2_skills
WITH s1, s2, intersection_count, common_skills, (s1_skills + s2_skills - intersection_count) AS union_count
RETURN s2.roll_no AS PeerRollNo,
       s2.name AS PeerName,
       intersection_count AS SharedSkillsCount,
       union_count AS TotalUniqueSkills,
       round(1.0 * intersection_count / union_count, 3) AS JaccardSimilarity,
       common_skills AS SharedSkills
ORDER BY JaccardSimilarity DESC;

// ------------------------------------------------------------------------------
// QUERY 5: End-to-End Application Lifecycle Graph Traversal
// Purpose: Trace the complete multi-hop path from Student through Application,
//          Job, Company, Interview, Recruiter, and Offer in a single expression.
// ------------------------------------------------------------------------------
MATCH (s:Student)-[:SUBMITTED]->(app:Application)-[:FOR_JOB]->(j:Job)-[:POSTED_BY]->(c:Company)
OPTIONAL MATCH (app)-[:MANAGED_BY]->(st:Staff)
OPTIONAL MATCH (app)-[:ADVANCED_TO]->(i:Interview)-[:INTERVIEWED_BY]->(r:Recruiter)
OPTIONAL MATCH (app)-[:RESULTED_IN]->(o:Offer)
RETURN app.app_id AS AppID,
       s.name AS StudentName,
       s.roll_no AS RollNo,
       j.title AS JobRole,
       c.co_name AS Company,
       app.status AS ApplicationStatus,
       st.staff_name AS PlacementOfficer,
       i.mode AS InterviewMode,
       i.result AS InterviewResult,
       r.name AS Interviewer,
       coalesce(o.package_offered, 0.0) AS OfferedPackageLPA,
       coalesce(o.offer_status, "None") AS OfferOutcome
ORDER BY OfferedPackageLPA DESC, AppID ASC;

// ------------------------------------------------------------------------------
// QUERY 6: Market Skill Demand Aggregation (Graph Degree Centrality)
// Purpose: Find which skills are most demanded by visiting companies and compare
//          market demand against student talent pool supply.
// ------------------------------------------------------------------------------
MATCH (sk:Skill)
OPTIONAL MATCH (j:Job)-[:REQUIRES_SKILL]->(sk)
WITH sk, count(j) AS job_demand_count
OPTIONAL MATCH (s:Student)-[:HAS_SKILL]->(sk)
WITH sk, job_demand_count, count(s) AS student_supply_count
RETURN sk.skill_name AS SkillName,
       sk.category AS Domain,
       job_demand_count AS IndustryDemandCount,
       student_supply_count AS StudentSupplyCount,
       (job_demand_count - student_supply_count) AS MarketTalentGap
ORDER BY IndustryDemandCount DESC, StudentSupplyCount DESC;

// ------------------------------------------------------------------------------
// QUERY 7: High-Package Placement Archetype Pattern Mining
// Purpose: Mine common skills and department affiliations among candidates who
//          successfully secured high-paying accepted offers (>= 30 LPA).
// ------------------------------------------------------------------------------
MATCH (s:Student)-[:SUBMITTED]->(app:Application)-[:RESULTED_IN]->(o:Offer)
MATCH (app)-[:FOR_JOB]->(j:Job)-[:POSTED_BY]->(c:Company)
MATCH (s)-[:ENROLLED_IN]->(d:Department)
MATCH (s)-[:HAS_SKILL]->(sk:Skill)
WHERE o.package_offered >= 30.0 AND o.offer_status = 'Accepted'
RETURN sk.skill_name AS HighYieldSkill,
       sk.category AS Category,
       count(DISTINCT s) AS HiredStudentCount,
       collect(DISTINCT s.name) AS StarStudents,
       collect(DISTINCT c.co_name) AS HiringCompanies
ORDER BY HiredStudentCount DESC, HighYieldSkill ASC;

// ------------------------------------------------------------------------------
// QUERY 8: Placement Bottleneck & Lag Detection
// Purpose: Identify applications currently stalled in 'Interviewing' or 'Pending'
//          status that have no scheduled interview or require T&P intervention.
// ------------------------------------------------------------------------------
MATCH (app:Application)
WHERE app.status IN ['Interviewing', 'Pending']
MATCH (s:Student)-[:SUBMITTED]->(app)-[:FOR_JOB]->(j:Job)-[:POSTED_BY]->(c:Company)
OPTIONAL MATCH (app)-[:ADVANCED_TO]->(i:Interview)
OPTIONAL MATCH (app)-[:MANAGED_BY]->(st:Staff)
RETURN app.app_id AS AppID,
       s.name AS StudentName,
       j.title AS JobRole,
       c.co_name AS TargetCompany,
       app.status AS CurrentStatus,
       CASE WHEN i IS NULL THEN "ACTION REQUIRED: No Interview Scheduled"
            ELSE "Interview Logged (" + i.mode + " - " + i.result + ")" END AS OperationalDiagnostic,
       st.staff_name AS AssignedOfficer
ORDER BY app.status DESC, AppID ASC;
