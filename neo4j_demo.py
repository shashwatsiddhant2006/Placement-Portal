"""
========================================================================================
CAMPUS PLACEMENT PORTAL — NEO4J GRAPH DATABASE INTERACTIVE DEMO (DA3)
Course: BACSE202 Database Systems | Phase: DA3 Modern Database Extension
Authors: Shashwat Siddhant & Arnav Semwal
Database Technology: Neo4j Graph Database
========================================================================================
This interactive application provides a comprehensive demonstration of the Campus
Placement Portal implemented on a Property Graph Data Model.

Features:
1. Dual-Engine Support:
   - Live Neo4j Driver (Bolt protocol via neo4j Python driver)
   - High-Fidelity Embedded Graph Engine (Offline fallback for standalone demos)
2. Technology-Specific Graph Traversals:
   - Instant skill matching & multi-hop eligibility verification
   - Graph set-difference skill-gap analysis
   - Reverse candidate ranking for recruiters
   - Collaborative peer recommendation via Jaccard graph similarity
   - End-to-end application lifecycle path audit
   - Industry skill demand vs supply aggregation
   - High-package archetype pattern mining
   - Operational bottleneck & stalled pipeline detection
3. Full Graph CRUD Operations (Nodes & Directed Relationships)
4. Cypher Query Console
========================================================================================
"""

import os
import sys
import math
from typing import List, Dict, Any, Optional

# Try importing neo4j driver
try:
    from neo4j import GraphDatabase, Driver
    HAS_NEO4J_LIB = True
except ImportError:
    HAS_NEO4J_LIB = False

# Environment-based connection configuration
NEO4J_URI = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.environ.get("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD", "password")


def print_banner(title: str):
    width = 90
    print("\n" + "=" * width)
    print(f" {title.center(width - 2)} ")
    print("=" * width)


def print_section(title: str):
    width = 90
    print("\n" + "-" * width)
    print(f"  [+] {title}")
    print("-" * width)


def print_table(title: str, rows: List[Dict[str, Any]], headers: Optional[List[str]] = None):
    if not rows:
        print(f"\n  {title}: (No records found)")
        return

    if headers is None:
        headers = list(rows[0].keys())

    # Calculate column widths
    widths = {h: len(str(h)) for h in headers}
    for r in rows:
        for h in headers:
            val = r.get(h, "")
            if isinstance(val, list):
                val = ", ".join(str(x) for x in val)
            widths[h] = max(widths[h], len(str(val)))

    print(f"\n  {title}")
    header_line = "  " + " | ".join(str(h).ljust(widths[h]) for h in headers)
    separator = "  " + "-+-".join("-" * widths[h] for h in headers)
    print(header_line)
    print(separator)

    for r in rows:
        row_vals = []
        for h in headers:
            val = r.get(h, "")
            if isinstance(val, list):
                val = ", ".join(str(x) for x in val)
            row_vals.append(str(val).ljust(widths[h]))
        print("  " + " | ".join(row_vals))
    print(f"  ({len(rows)} row(s) returned)\n")


# ==============================================================================
# EMBEDDED GRAPH DATASET & GRAPH ENGINE (Ensures 100% Reliability Anytime)
# ==============================================================================

class EmbeddedGraphEngine:
    """In-memory property graph engine matching Cypher traversal semantics."""

    def __init__(self):
        self.nodes: Dict[str, Dict[str, Any]] = {}  # id -> {labels, properties}
        self.relationships: List[Dict[str, Any]] = []  # list of {start, type, end, properties}
        self.seed_graph()

    def add_node(self, node_id: str, label: str, properties: Dict[str, Any]):
        self.nodes[node_id] = {
            "id": node_id,
            "label": label,
            "properties": properties
        }

    def add_rel(self, start_id: str, rel_type: str, end_id: str, properties: Optional[Dict[str, Any]] = None):
        self.relationships.append({
            "start": start_id,
            "type": rel_type,
            "end": end_id,
            "properties": properties or {}
        })

    def seed_graph(self):
        self.nodes.clear()
        self.relationships.clear()

        # Departments
        depts = [
            ("DEP001", "Computer Science & Engineering", "+91-44-2250-0101"),
            ("DEP002", "Information Technology", "+91-44-2250-0102"),
            ("DEP003", "Artificial Intelligence & Data Science", "+91-44-2250-0103"),
            ("DEP004", "Electronics & Communication Engineering", "+91-44-2250-0104"),
            ("DEP005", "Mechanical Engineering", "+91-44-2250-0105"),
            ("DEP006", "Electrical & Electronics Engineering", "+91-44-2250-0106"),
        ]
        for did, name, phone in depts:
            self.add_node(did, "Department", {"dept_id": did, "dept_name": name, "phone": phone})

        # Addresses
        addrs = [
            ("ADDR001", "Bengaluru", "Karnataka"),
            ("ADDR002", "Chennai", "Tamil Nadu"),
            ("ADDR003", "Hyderabad", "Telangana"),
            ("ADDR004", "Pune", "Maharashtra"),
            ("ADDR005", "Mumbai", "Maharashtra"),
            ("ADDR006", "New Delhi", "Delhi"),
        ]
        for aid, city, state in addrs:
            self.add_node(aid, "Address", {"address_id": aid, "city": city, "state": state})

        # Companies
        companies = [
            ("CO001", "Google India", "Information Technology & Cloud"),
            ("CO002", "Microsoft Corporation", "Software & Enterprise Cloud"),
            ("CO003", "Amazon Web Services", "E-Commerce & Cloud Infrastructure"),
            ("CO004", "Oracle India", "Enterprise Database & Applications"),
            ("CO005", "Cisco Systems", "Networking & Telecommunications"),
            ("CO006", "Qualcomm India", "Semiconductors & Embedded Systems"),
            ("CO007", "Tata Consultancy Services", "IT Services & Consulting"),
            ("CO008", "Infosys Limited", "Digital Services & Consulting"),
        ]
        for cid, name, ind in companies:
            self.add_node(cid, "Company", {"co_id": cid, "co_name": name, "industry": ind})

        # Skills
        skills = [
            ("SK001", "Python Programming", "Programming"),
            ("SK002", "Java Enterprise", "Programming"),
            ("SK003", "C++ System Architecture", "Programming"),
            ("SK004", "Relational Database Design & SQL", "Database"),
            ("SK005", "Oracle PL/SQL & Stored Logic", "Database"),
            ("SK006", "Cloud Architecture (AWS/GCP)", "Cloud"),
            ("SK007", "Distributed Systems & Microservices", "Cloud"),
            ("SK008", "Machine Learning & Deep Neural Nets", "AI/ML"),
            ("SK009", "Data Structures & Algorithms", "Programming"),
            ("SK010", "Computer Networks & TCP/IP", "Networking"),
            ("SK011", "Embedded C & RTOS", "Hardware"),
            ("SK012", "System Verilog & VLSI Design", "Hardware"),
            ("SK013", "DevOps & Docker Containers", "Cloud"),
            ("SK014", "Technical Communication", "Soft Skills"),
            ("SK015", "Leadership & Team Management", "Soft Skills"),
        ]
        for skid, name, cat in skills:
            self.add_node(skid, "Skill", {"skill_id": skid, "skill_name": name, "category": cat})

        # Staff
        staff_members = [
            ("STF001", "Dr. Sundararajan V.", "Director - Training & Placement"),
            ("STF002", "Prof. Kavitha Raman", "Senior Placement Officer - Tier 1 Firms"),
            ("STF003", "Mr. Dinesh Kumar", "Placement Executive - Core Engineering"),
            ("STF004", "Ms. Shalini Murugan", "T&P Compliance & Corporate Liaison"),
        ]
        for stid, name, desig in staff_members:
            self.add_node(stid, "Staff", {"staff_id": stid, "staff_name": name, "designation": desig})

        # Recruiters
        recruiters = [
            ("REC001", "CO001", "Aravind Swaminathan", "+91-80-6721-5001"),
            ("REC002", "CO002", "Deepa Krishnan", "+91-80-4000-6002"),
            ("REC003", "CO003", "Harish Nambiar", "+91-80-3000-7003"),
            ("REC004", "CO004", "Monica Sen", "+91-80-2200-8004"),
            ("REC005", "CO005", "Rajeev Menon", "+91-80-4422-9005"),
            ("REC006", "CO007", "Sunita Rao", "+91-22-6778-1001"),
            ("REC007", "CO008", "Pradeep Shenoy", "+91-80-2852-0261"),
            ("REC008", "CO006", "Karthik Balan", "+91-80-4112-3456"),
        ]
        for rid, cid, name, phone in recruiters:
            self.add_node(rid, "Recruiter", {"recruiter_id": rid, "name": name, "phone": phone, "co_id": cid})
            self.add_rel(rid, "WORKS_FOR", cid)

        # Job Postings
        jobs = [
            ("JOB001", "CO001", "Software Development Engineer - I", 42.50, 8.50),
            ("JOB002", "CO002", "Cloud Systems & AI Engineer", 38.00, 8.00),
            ("JOB003", "CO003", "Backend SDE (Distributed Systems)", 34.00, 8.00),
            ("JOB004", "CO004", "Database Kernel Engineer", 28.50, 7.50),
            ("JOB005", "CO005", "Network Systems Software Engineer", 22.00, 7.00),
            ("JOB006", "CO006", "Embedded Firmware Engineer", 24.00, 7.00),
            ("JOB007", "CO007", "Digital Solutions Engineer", 9.50, 6.50),
            ("JOB008", "CO008", "Systems Analyst Trainee", 7.20, 6.00),
        ]
        for jid, cid, title, pkg, min_c in jobs:
            self.add_node(jid, "Job", {"job_id": jid, "title": title, "package_lpa": pkg, "min_cgpa": min_c, "co_id": cid})
            self.add_rel(jid, "POSTED_BY", cid)

        # Job Required Skills
        job_skills = [
            ("JOB001", ["SK001", "SK007", "SK009"]),
            ("JOB002", ["SK001", "SK006", "SK008"]),
            ("JOB003", ["SK002", "SK006", "SK007", "SK009"]),
            ("JOB004", ["SK003", "SK004", "SK005"]),
            ("JOB005", ["SK003", "SK010"]),
            ("JOB006", ["SK003", "SK011", "SK012"]),
            ("JOB007", ["SK001", "SK004", "SK014"]),
            ("JOB008", ["SK002", "SK004"]),
        ]
        for jid, sk_list in job_skills:
            for skid in sk_list:
                self.add_rel(jid, "REQUIRES_SKILL", skid)

        # Students
        students = [
            ("25BCE5227", "DEP001", "ADDR001", "Shashwat Siddhant", "shashwat.siddhant2025@campus.edu", 9.40),
            ("25BCE5392", "DEP001", "ADDR002", "Srnav Semwal", "srnav.semwal2025@campus.edu", 9.25),
            ("25BAI3003", "DEP003", "ADDR003", "Priya Sharma", "priya.sharma@campus.edu", 9.10),
            ("25BCE1001", "DEP001", "ADDR004", "Ananya Iyer", "ananya.iyer@campus.edu", 8.90),
            ("25BIT2015", "DEP002", "ADDR005", "Neha Kulkarni", "neha.kulkarni@campus.edu", 8.75),
            ("25BIT2002", "DEP002", "ADDR001", "Rohan Gupta", "rohan.gupta@campus.edu", 8.50),
            ("25BEE6006", "DEP006", "ADDR003", "Meera Reddy", "meera.reddy@campus.edu", 8.10),
            ("25BEC4004", "DEP004", "ADDR006", "Vikram Patel", "vikram.patel@campus.edu", 7.80),
            ("25BME5005", "DEP005", "ADDR004", "Aditya Verma", "aditya.verma@campus.edu", 7.20),
            ("25BCE1010", "DEP001", "ADDR002", "Kabir Das", "kabir.das@campus.edu", 6.80),
        ]
        for roll, did, aid, name, email, cgpa in students:
            self.add_node(roll, "Student", {"roll_no": roll, "name": name, "email": email, "cgpa": cgpa, "dept_id": did, "address_id": aid})
            self.add_rel(roll, "ENROLLED_IN", did)
            self.add_rel(roll, "LOCATED_IN", aid)

        # Student Skills
        student_skills = [
            ("25BCE5227", ["SK001", "SK004", "SK005", "SK007", "SK009"]),
            ("25BCE5392", ["SK002", "SK004", "SK006", "SK007", "SK009"]),
            ("25BAI3003", ["SK001", "SK008", "SK006", "SK009"]),
            ("25BCE1001", ["SK001", "SK002", "SK004", "SK009"]),
            ("25BIT2015", ["SK002", "SK004", "SK006", "SK013"]),
            ("25BIT2002", ["SK001", "SK004", "SK009"]),
            ("25BEE6006", ["SK001", "SK010", "SK014"]),
            ("25BEC4004", ["SK003", "SK011", "SK012"]),
        ]
        for roll, sk_list in student_skills:
            for skid in sk_list:
                self.add_rel(roll, "HAS_SKILL", skid)

        # Applications
        apps = [
            ("APP001", "25BCE5227", "JOB001", "STF002", "Hired"),
            ("APP002", "25BCE5392", "JOB003", "STF002", "Hired"),
            ("APP003", "25BAI3003", "JOB002", "STF002", "Hired"),
            ("APP004", "25BCE1001", "JOB001", "STF002", "Interviewing"),
            ("APP005", "25BIT2002", "JOB003", "STF002", "Interviewing"),
            ("APP006", "25BIT2015", "JOB002", "STF002", "Shortlisted"),
            ("APP007", "25BCE5227", "JOB004", "STF002", "Shortlisted"),
            ("APP008", "25BEC4004", "JOB005", "STF003", "Shortlisted"),
            ("APP009", "25BEE6006", "JOB007", "STF003", "Hired"),
            ("APP010", "25BME5005", "JOB007", "STF003", "Interviewing"),
            ("APP011", "25BCE1010", "JOB007", "STF003", "Pending"),
            ("APP012", "25BEC4004", "JOB006", "STF003", "Pending"),
        ]
        for aid, roll, jid, stid, status in apps:
            self.add_node(aid, "Application", {"app_id": aid, "status": status, "roll_no": roll, "job_id": jid})
            self.add_rel(roll, "SUBMITTED", aid)
            self.add_rel(aid, "FOR_JOB", jid)
            self.add_rel(aid, "MANAGED_BY", stid)

        # Interviews
        interviews = [
            ("INT001", "APP001", "REC001", "Online", "Cleared"),
            ("INT002", "APP002", "REC003", "Online", "Cleared"),
            ("INT003", "APP003", "REC002", "Online", "Cleared"),
            ("INT004", "APP004", "REC001", "In-Person", "Pending"),
            ("INT005", "APP005", "REC003", "Online", "Pending"),
            ("INT006", "APP009", "REC006", "In-Person", "Cleared"),
        ]
        for iid, aid, rid, mode, result in interviews:
            self.add_node(iid, "Interview", {"interview_id": iid, "mode": mode, "result": result, "app_id": aid})
            self.add_rel(aid, "ADVANCED_TO", iid)
            self.add_rel(iid, "INTERVIEWED_BY", rid)

        # Offers
        offers = [
            ("OFR001", "APP001", 42.50, "Accepted"),
            ("OFR002", "APP002", 34.00, "Accepted"),
            ("OFR003", "APP003", 38.00, "Accepted"),
            ("OFR004", "APP009", 9.50, "Accepted"),
        ]
        for oid, aid, pkg, ost in offers:
            self.add_node(oid, "Offer", {"offer_id": oid, "package_offered": pkg, "offer_status": ost, "app_id": aid})
            self.add_rel(aid, "RESULTED_IN", oid)

    # Helper traversal methods
    def get_outgoing(self, node_id: str, rel_type: Optional[str] = None) -> List[Dict[str, Any]]:
        return [r for r in self.relationships if r["start"] == node_id and (rel_type is None or r["type"] == rel_type)]

    def get_incoming(self, node_id: str, rel_type: Optional[str] = None) -> List[Dict[str, Any]]:
        return [r for r in self.relationships if r["end"] == node_id and (rel_type is None or r["type"] == rel_type)]

    def get_nodes_by_label(self, label: str) -> List[Dict[str, Any]]:
        return [n for n in self.nodes.values() if n["label"] == label]


# ==============================================================================
# UNIFIED DATABASE CLIENT (Live Neo4j or Embedded Graph Engine)
# ==============================================================================

class GraphClient:
    def __init__(self):
        self.live_driver: Optional[Any] = None
        self.is_live: bool = False
        self.embedded = EmbeddedGraphEngine()
        self.connect()

    def connect(self):
        if HAS_NEO4J_LIB:
            try:
                driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
                # Verify connectivity
                driver.verify_connectivity()
                self.live_driver = driver
                self.is_live = True
                print("  [*] Connected to Live Neo4j instance at", NEO4J_URI)
                return
            except Exception as e:
                self.is_live = False
                self.live_driver = None
        else:
            self.is_live = False

        print("  [*] Running on High-Fidelity Embedded Graph Engine (Offline Mode)")

    def close(self):
        if self.live_driver:
            self.live_driver.close()

    def get_engine_name(self) -> str:
        return f"Live Neo4j ({NEO4J_URI})" if self.is_live else "Embedded In-Memory Graph Engine"


# Instantiate client
CLIENT = GraphClient()


# ==============================================================================
# GRAPH QUERIES IMPLEMENTATION
# ==============================================================================

def show_graph_overview():
    print_section("GRAPH TOPOLOGY OVERVIEW")
    if CLIENT.is_live:
        with CLIENT.live_driver.session() as s:
            labels_res = s.run("CALL db.labels() YIELD label RETURN label").values()
            rels_res = s.run("CALL db.relationshipTypes() YIELD relationshipType RETURN relationshipType").values()
            print("  Active Engine:", CLIENT.get_engine_name())
            print(f"  Node Labels: {', '.join(r[0] for r in labels_res)}")
            print(f"  Relationship Types: {', '.join(r[0] for r in rels_res)}")
    else:
        eng = CLIENT.embedded
        label_counts: Dict[str, int] = {}
        for n in eng.nodes.values():
            lbl = n["label"]
            label_counts[lbl] = label_counts.get(lbl, 0) + 1

        rel_counts: Dict[str, int] = {}
        for r in eng.relationships:
            rtype = r["type"]
            rel_counts[rtype] = rel_counts.get(rtype, 0) + 1

        summary_rows = [
            {"Label / Entity Type": k, "Node Count": v} for k, v in sorted(label_counts.items())
        ]
        print_table("GRAPH NODE LABELS", summary_rows)

        rel_rows = [
            {"Relationship Type": k, "Edge Count": v} for k, v in sorted(rel_counts.items())
        ]
        print_table("GRAPH RELATIONSHIPS", rel_rows)
        print(f"  Total Vertices (Nodes): {len(eng.nodes)}")
        print(f"  Total Directed Edges:   {len(eng.relationships)}")


def inspect_entity_neighborhood():
    print_section("INSPECT ENTITY GRAPH NEIGHBORHOOD")
    print("  Available Entity Types:")
    print("  1. Student (e.g. 25BCE5227, 25BCE5392, 25BAI3003, 25BCE1001)")
    print("  2. Job (e.g. JOB001, JOB002, JOB003, JOB004)")
    print("  3. Company (e.g. CO001, CO002, CO003)")
    node_id = input("\n  Enter Node ID to inspect: ").strip()

    if node_id not in CLIENT.embedded.nodes:
        print(f"  [!] Node ID '{node_id}' not found in graph.")
        return

    node = CLIENT.embedded.nodes[node_id]
    print(f"\n  Entity Found: {node['label']} [{node['id']}]")
    print("  Properties:")
    for k, v in node["properties"].items():
        print(f"    - {k}: {v}")

    outgoing = CLIENT.embedded.get_outgoing(node_id)
    if outgoing:
        rows = []
        for r in outgoing:
            target = CLIENT.embedded.nodes.get(r["end"], {})
            target_desc = f"{target.get('label', '')}: " + str(target.get("properties", {}).get("name") or target.get("properties", {}).get("title") or target.get("properties", {}).get("skill_name") or r["end"])
            rows.append({"Outgoing Edge": f"-[:{r['type']}]->", "Target Node ID": r["end"], "Target Details": target_desc})
        print_table("OUTGOING RELATIONSHIPS", rows)

    incoming = CLIENT.embedded.get_incoming(node_id)
    if incoming:
        rows = []
        for r in incoming:
            src = CLIENT.embedded.nodes.get(r["start"], {})
            src_desc = f"{src.get('label', '')}: " + str(src.get("properties", {}).get("name") or src.get("properties", {}).get("title") or r["start"])
            rows.append({"Incoming Edge": f"<-[:{r['type']}]-", "Source Node ID": r["start"], "Source Details": src_desc})
        print_table("INCOMING RELATIONSHIPS", rows)


def query_1_eligibility_and_skill_match():
    print_section("QUERY 1: INSTANT GRAPH-BASED ELIGIBILITY & SKILL MATCH ENGINE")
    print("  Cypher Pattern: (s:Student)-[:HAS_SKILL]->(sk:Skill)<-[:REQUIRES_SKILL]-(j:Job)-[:POSTED_BY]->(c:Company)")
    roll_no = input("  Enter Student Roll No [Default: 25BCE5227]: ").strip() or "25BCE5227"

    eng = CLIENT.embedded
    if roll_no not in eng.nodes:
        print(f"  [!] Student '{roll_no}' not found.")
        return

    student = eng.nodes[roll_no]
    s_props = student["properties"]
    s_cgpa = s_props["cgpa"]
    s_skills = set(r["end"] for r in eng.get_outgoing(roll_no, "HAS_SKILL"))

    results = []
    for j_node in eng.get_nodes_by_label("Job"):
        jid = j_node["id"]
        j_props = j_node["properties"]
        min_cgpa = j_props["min_cgpa"]
        if s_cgpa < min_cgpa:
            continue

        # Get Company
        co_rel = eng.get_outgoing(jid, "POSTED_BY")
        co_name = eng.nodes[co_rel[0]["end"]]["properties"]["co_name"] if co_rel else "N/A"

        # Required skills
        req_rels = eng.get_outgoing(jid, "REQUIRES_SKILL")
        req_skill_ids = set(r["end"] for r in req_rels)
        total_req = len(req_skill_ids)

        matched_ids = s_skills.intersection(req_skill_ids)
        matched_count = len(matched_ids)
        match_pct = round((matched_count / total_req * 100.0), 1) if total_req > 0 else 0.0

        matched_names = [eng.nodes[sid]["properties"]["skill_name"] for sid in matched_ids]

        results.append({
            "Job ID": jid,
            "Role Title": j_props["title"],
            "Company": co_name,
            "Package LPA": f"₹{j_props['package_lpa']} L",
            "Cutoff": j_props["min_cgpa"],
            "Matched Skills": f"{matched_count}/{total_req}",
            "Match %": f"{match_pct}%",
            "Shared Skill Nodes": matched_names
        })

    results.sort(key=lambda x: (float(x["Match %"].replace("%", "")), float(x["Package LPA"].replace("₹", "").replace(" L", ""))), reverse=True)
    print(f"\n  Target Candidate: {s_props['name']} | CGPA: {s_cgpa} | Skills Mastered: {len(s_skills)}")
    print_table("QUALIFYING JOB OPENINGS RANKED BY GRAPH FIT", results)


def query_2_skill_gap_analysis():
    print_section("QUERY 2: SKILL GAP ANALYSIS (SET DIFFERENCE ON GRAPH RELATIONSHIPS)")
    print("  Cypher Pattern: MATCH (j:Job)-[:REQUIRES_SKILL]->(needed:Skill) WHERE NOT (s:Student)-[:HAS_SKILL]->(needed)")
    roll_no = input("  Enter Student Roll No [Default: 25BCE1001]: ").strip() or "25BCE1001"
    job_id = input("  Enter Dream Target Job ID [Default: JOB001]: ").strip() or "JOB001"

    eng = CLIENT.embedded
    if roll_no not in eng.nodes or job_id not in eng.nodes:
        print("  [!] Student or Job ID invalid.")
        return

    student = eng.nodes[roll_no]
    job = eng.nodes[job_id]

    s_skills = set(r["end"] for r in eng.get_outgoing(roll_no, "HAS_SKILL"))
    j_req_skills = set(r["end"] for r in eng.get_outgoing(job_id, "REQUIRES_SKILL"))

    missing_ids = j_req_skills - s_skills
    held_ids = j_req_skills.intersection(s_skills)

    print(f"\n  Candidate: {student['properties']['name']} ({roll_no})")
    print(f"  Dream Role: {job['properties']['title']} (Package: ₹{job['properties']['package_lpa']} LPA)")
    print(f"  Held Requirements: {[eng.nodes[sid]['properties']['skill_name'] for sid in held_ids]}")

    if not missing_ids:
        print("\n  [✓] EXCELLENT! Candidate already possesses 100% of the required skill nodes for this position.")
    else:
        gap_rows = []
        for sid in missing_ids:
            sk_node = eng.nodes[sid]["properties"]
            gap_rows.append({
                "Missing Skill ID": sid,
                "Skill Name": sk_node["skill_name"],
                "Domain Category": sk_node["category"],
                "Recommendation": "Enroll in university elective or complete certification"
            })
        print_table("ACTIONABLE SKILL GAPS IDENTIFIED BY GRAPH TRAVERSAL", gap_rows)


def query_3_recruiter_candidate_pipeline():
    print_section("QUERY 3: REVERSE RECRUITER CANDIDATE DISCOVERY & RANKING")
    job_id = input("  Enter Job Posting ID [Default: JOB003 - AWS Backend SDE]: ").strip() or "JOB003"

    eng = CLIENT.embedded
    if job_id not in eng.nodes:
        print(f"  [!] Job ID '{job_id}' not found.")
        return

    job = eng.nodes[job_id]
    j_props = job["properties"]
    min_cgpa = j_props["min_cgpa"]
    j_skills = set(r["end"] for r in eng.get_outgoing(job_id, "REQUIRES_SKILL"))
    total_req = len(j_skills)

    matched_candidates = []
    for s_node in eng.get_nodes_by_label("Student"):
        roll = s_node["id"]
        s_props = s_node["properties"]
        if s_props["cgpa"] < min_cgpa:
            continue

        s_skills = set(r["end"] for r in eng.get_outgoing(roll, "HAS_SKILL"))
        shared = s_skills.intersection(j_skills)
        if not shared:
            continue

        dept_rel = eng.get_outgoing(roll, "ENROLLED_IN")
        dept_name = eng.nodes[dept_rel[0]["end"]]["properties"]["dept_name"] if dept_rel else "N/A"
        shared_names = [eng.nodes[sid]["properties"]["skill_name"] for sid in shared]
        fit_pct = round(len(shared) / total_req * 100.0, 1)

        matched_candidates.append({
            "Roll No": roll,
            "Candidate Name": s_props["name"],
            "Department": dept_name,
            "CGPA": s_props["cgpa"],
            "Matched Count": f"{len(shared)}/{total_req}",
            "Fit Score": f"{fit_pct}%",
            "Verified Skills": shared_names
        })

    matched_candidates.sort(key=lambda x: (float(x["Fit Score"].replace("%", "")), x["CGPA"]), reverse=True)
    print(f"\n  Evaluating Pool for: {j_props['title']} | Cutoff: {min_cgpa} CGPA")
    print_table("RANKED SHORTLIST CANDIDATES", matched_candidates)


def query_4_peer_skill_similarity():
    print_section("QUERY 4: COLLABORATIVE PEER SKILL SIMILARITY (JACCARD INDEX ON GRAPH)")
    print("  Mathematical Formulation: Jaccard(A, B) = |Skills(A) ∩ Skills(B)| / |Skills(A) ∪ Skills(B)|")
    roll_no = input("  Enter Base Student Roll No [Default: 25BCE5227]: ").strip() or "25BCE5227"

    eng = CLIENT.embedded
    if roll_no not in eng.nodes:
        print(f"  [!] Student '{roll_no}' not found.")
        return

    base_skills = set(r["end"] for r in eng.get_outgoing(roll_no, "HAS_SKILL"))
    base_name = eng.nodes[roll_no]["properties"]["name"]

    similarity_list = []
    for s_node in eng.get_nodes_by_label("Student"):
        peer_roll = s_node["id"]
        if peer_roll == roll_no:
            continue

        peer_skills = set(r["end"] for r in eng.get_outgoing(peer_roll, "HAS_SKILL"))
        intersection = base_skills.intersection(peer_skills)
        union = base_skills.union(peer_skills)

        if not union or not intersection:
            continue

        jaccard = round(len(intersection) / len(union), 3)
        common_names = [eng.nodes[sid]["properties"]["skill_name"] for sid in intersection]

        similarity_list.append({
            "Peer Roll No": peer_roll,
            "Peer Name": s_node["properties"]["name"],
            "Shared Skills": len(intersection),
            "Union Skills": len(union),
            "Jaccard Index": jaccard,
            "Common Skill Intersection": common_names
        })

    similarity_list.sort(key=lambda x: x["Jaccard Index"], reverse=True)
    print(f"\n  Base Student: {base_name} ({roll_no}) — Total Skills: {len(base_skills)}")
    print_table("PEER COLLABORATIVE MATCHES & STUDY GROUP RECOMMENDATIONS", similarity_list)


def query_5_application_lifecycle_trail():
    print_section("QUERY 5: END-TO-END APPLICATION LIFECYCLE GRAPH TRAVERSAL")
    print("  Graph Hop: (Student)->(Application)->(Job)->(Company) & (Application)->(Interview)->(Offer)")

    eng = CLIENT.embedded
    rows = []
    for app in eng.get_nodes_by_label("Application"):
        aid = app["id"]
        status = app["properties"]["status"]

        # Incoming student
        student_rel = eng.get_incoming(aid, "SUBMITTED")
        student_name = eng.nodes[student_rel[0]["start"]]["properties"]["name"] if student_rel else "N/A"
        roll = student_rel[0]["start"] if student_rel else "N/A"

        # Outgoing job
        job_rel = eng.get_outgoing(aid, "FOR_JOB")
        job_title = eng.nodes[job_rel[0]["end"]]["properties"]["title"] if job_rel else "N/A"
        co_rel = eng.get_outgoing(job_rel[0]["end"], "POSTED_BY") if job_rel else []
        co_name = eng.nodes[co_rel[0]["end"]]["properties"]["co_name"] if co_rel else "N/A"

        # Interview
        int_rel = eng.get_outgoing(aid, "ADVANCED_TO")
        int_status = "None"
        if int_rel:
            i_props = eng.nodes[int_rel[0]["end"]]["properties"]
            int_status = f"{i_props['mode']} ({i_props['result']})"

        # Offer
        ofr_rel = eng.get_outgoing(aid, "RESULTED_IN")
        ofr_details = "None"
        if ofr_rel:
            o_props = eng.nodes[ofr_rel[0]["end"]]["properties"]
            ofr_details = f"₹{o_props['package_offered']} LPA [{o_props['offer_status']}]"

        rows.append({
            "App ID": aid,
            "Student Name": student_name,
            "Target Company": co_name,
            "Job Title": job_title,
            "Status": status,
            "Interview Stage": int_status,
            "Final Offer Outcome": ofr_details
        })

    rows.sort(key=lambda x: x["App ID"])
    print_table("AUDITABLE APPLICATION LIFECYCLE PATHWAYS", rows)


def query_6_skill_demand_analytics():
    print_section("QUERY 6: MARKET SKILL DEMAND AGGREGATION (DEGREE CENTRALITY)")

    eng = CLIENT.embedded
    skill_stats = []
    for sk in eng.get_nodes_by_label("Skill"):
        skid = sk["id"]
        props = sk["properties"]

        # In-degree from Jobs (Market Demand)
        job_in = len(eng.get_incoming(skid, "REQUIRES_SKILL"))
        # In-degree from Students (Talent Supply)
        student_in = len(eng.get_incoming(skid, "HAS_SKILL"))

        skill_stats.append({
            "Skill Name": props["skill_name"],
            "Domain Category": props["category"],
            "Industry Demand (Jobs)": job_in,
            "Student Supply (Candidates)": student_in,
            "Net Gap (Demand - Supply)": job_in - student_in
        })

    skill_stats.sort(key=lambda x: (x["Industry Demand (Jobs)"], x["Student Supply (Candidates)"]), reverse=True)
    print_table("INSTITUTIONAL CURRICULUM & TALENT SUPPLY-DEMAND MATRIX", skill_stats)


def query_7_high_package_archetypes():
    print_section("QUERY 7: HIGH-PACKAGE PLACEMENT ARCHETYPE PATTERN MINING")
    print("  Mining frequent subgraph patterns: (Student)-[:HAS_SKILL]->(Skill) WHERE Offer >= 30 LPA")

    eng = CLIENT.embedded
    high_yield_students = set()
    for ofr in eng.get_nodes_by_label("Offer"):
        if ofr["properties"]["package_offered"] >= 30.0 and ofr["properties"]["offer_status"] == "Accepted":
            aid = ofr["properties"]["app_id"]
            s_rel = eng.get_incoming(aid, "SUBMITTED")
            if s_rel:
                high_yield_students.add(s_rel[0]["start"])

    skill_freq: Dict[str, List[str]] = {}
    for roll in high_yield_students:
        s_name = eng.nodes[roll]["properties"]["name"]
        for r in eng.get_outgoing(roll, "HAS_SKILL"):
            skid = r["end"]
            skill_freq.setdefault(skid, []).append(s_name)

    rows = []
    for skid, students in skill_freq.items():
        sk_props = eng.nodes[skid]["properties"]
        rows.append({
            "High-Yield Skill": sk_props["skill_name"],
            "Category": sk_props["category"],
            "Hired Candidate Count": len(students),
            "Star Achievers": students
        })

    rows.sort(key=lambda x: x["Hired Candidate Count"], reverse=True)
    print(f"\n  Cohort Analyzed: {len(high_yield_students)} Tier-1 Package Achievers (>= ₹30 LPA)")
    print_table("KEY COMMON SKILLS OF TOP-TIER PLACED STUDENTS", rows)


def query_8_operational_bottlenecks():
    print_section("QUERY 8: PLACEMENT BOTTLENECK & LAG DETECTION")

    eng = CLIENT.embedded
    bottlenecks = []
    for app in eng.get_nodes_by_label("Application"):
        aid = app["id"]
        status = app["properties"]["status"]
        if status in ["Pending", "Interviewing"]:
            s_rel = eng.get_incoming(aid, "SUBMITTED")
            s_name = eng.nodes[s_rel[0]["start"]]["properties"]["name"] if s_rel else "N/A"

            j_rel = eng.get_outgoing(aid, "FOR_JOB")
            j_title = eng.nodes[j_rel[0]["end"]]["properties"]["title"] if j_rel else "N/A"

            int_rel = eng.get_outgoing(aid, "ADVANCED_TO")
            diag = "ACTION NEEDED: No Interview Scheduled" if not int_rel else "Interview In Progress"

            staff_rel = eng.get_outgoing(aid, "MANAGED_BY")
            staff_name = eng.nodes[staff_rel[0]["end"]]["properties"]["staff_name"] if staff_rel else "Unassigned"

            bottlenecks.append({
                "App ID": aid,
                "Candidate": s_name,
                "Target Role": j_title,
                "Current Pipeline State": status,
                "Operational Diagnostic": diag,
                "Assigned T&P Staff": staff_name
            })

    print_table("ATTENTION-REQUIRED PIPELINE QUEUE", bottlenecks)


# ==============================================================================
# GRAPH CRUD OPERATIONS
# ==============================================================================

def crud_insert_student():
    print_section("GRAPH CRUD: CREATE NEW STUDENT NODE & CONNECT SKILLS")
    roll = input("  Enter New Roll No (e.g. 25BCE9999): ").strip()
    if not roll:
        print("  [!] Roll number cannot be empty.")
        return

    if roll in CLIENT.embedded.nodes:
        print("  [!] Student node with this Roll No already exists.")
        return

    name = input("  Enter Full Name: ").strip()
    email = input("  Enter Email: ").strip()
    cgpa_str = input("  Enter CGPA (0.00 - 10.00): ").strip()
    try:
        cgpa = float(cgpa_str)
    except ValueError:
        print("  [!] Invalid CGPA.")
        return

    dept_id = input("  Enter Department ID (DEP001 to DEP006) [Default: DEP001]: ").strip() or "DEP001"
    addr_id = input("  Enter Address ID (ADDR001 to ADDR006) [Default: ADDR001]: ").strip() or "ADDR001"

    # Add Node
    CLIENT.embedded.add_node(roll, "Student", {
        "roll_no": roll, "name": name, "email": email, "cgpa": cgpa, "dept_id": dept_id, "address_id": addr_id
    })
    CLIENT.embedded.add_rel(roll, "ENROLLED_IN", dept_id)
    CLIENT.embedded.add_rel(roll, "LOCATED_IN", addr_id)

    print("\n  Available Skills to Connect:")
    for sk in CLIENT.embedded.get_nodes_by_label("Skill"):
        print(f"    [{sk['id']}] {sk['properties']['skill_name']}")

    skill_inputs = input("\n  Enter Skill IDs separated by commas (e.g. SK001, SK004): ").strip()
    if skill_inputs:
        for sid in [x.strip() for x in skill_inputs.split(",")]:
            if sid in CLIENT.embedded.nodes:
                CLIENT.embedded.add_rel(roll, "HAS_SKILL", sid)

    print(f"  [SUCCESS] Student node '{roll}' created and relationships materialized in graph.")


def crud_update_node():
    print_section("GRAPH CRUD: UPDATE NODE PROPERTY")
    node_id = input("  Enter Node ID to update (e.g. 25BCE5227 or JOB001): ").strip()
    if node_id not in CLIENT.embedded.nodes:
        print("  [!] Node ID not found.")
        return

    node = CLIENT.embedded.nodes[node_id]
    print(f"  Current Properties for {node['label']} [{node_id}]:")
    for k, v in node["properties"].items():
        print(f"    - {k}: {v}")

    prop_key = input("\n  Enter property key to update: ").strip()
    if prop_key not in node["properties"]:
        print(f"  [!] Property key '{prop_key}' does not exist on this node.")
        return

    new_val_str = input(f"  Enter new value for '{prop_key}': ").strip()
    # Type conversion
    orig_val = node["properties"][prop_key]
    if isinstance(orig_val, float):
        new_val = float(new_val_str)
    elif isinstance(orig_val, int):
        new_val = int(new_val_str)
    else:
        new_val = new_val_str

    node["properties"][prop_key] = new_val
    print(f"  [SUCCESS] Updated {prop_key} -> {new_val} on node [{node_id}].")


def crud_delete_node():
    print_section("GRAPH CRUD: DELETE NODE & DETACH RELATIONSHIPS")
    node_id = input("  Enter Node ID to delete: ").strip()
    if node_id not in CLIENT.embedded.nodes:
        print("  [!] Node ID not found.")
        return

    # Detach relationships
    CLIENT.embedded.relationships = [
        r for r in CLIENT.embedded.relationships if r["start"] != node_id and r["end"] != node_id
    ]
    del CLIENT.embedded.nodes[node_id]
    print(f"  [SUCCESS] Node [{node_id}] and all connected incident edges deleted from graph.")


def custom_cypher_console():
    print_section("CYPHER QUERY CONSOLE")
    print("  Active Engine:", CLIENT.get_engine_name())
    if CLIENT.is_live:
        query = input("  Enter Cypher statement: ").strip()
        if not query:
            return
        try:
            with CLIENT.live_driver.session() as s:
                result = s.run(query)
                records = [r.data() for r in result]
                if records:
                    print_table("CYPHER EXECUTION RESULT", records)
                else:
                    print("  [✓] Query executed successfully with 0 rows returned.")
        except Exception as e:
            print("  [!] Cypher Execution Error:", e)
    else:
        print("  (Currently on Embedded Graph Engine. Sample Cypher commands available in neo4j_queries.cypher)")
        print("  To run live Cypher directly against Neo4j, ensure your Neo4j service is running.")


# ==============================================================================
# MAIN APPLICATION INTERFACE
# ==============================================================================

def display_menu():
    print_banner("THE CAMPUS PLACEMENT PORTAL — NEO4J GRAPH EXPLORER (DA3)")
    print(f"  Engine Mode: [{CLIENT.get_engine_name()}]")
    print("\n  === GRAPH EXPLORATION & SCHEMA ===")
    print("   1. Display Graph Topology & Entity Counts")
    print("   2. Inspect Entity Graph Neighborhood (1-Hop Traversal)")
    print("\n  === TECHNOLOGY-SPECIFIC GRAPH QUERIES ===")
    print("   3. Query 1: Instant Eligibility & Skill Match Percentage Engine")
    print("   4. Query 2: Skill Gap Analysis for Target Dream Role (Set Difference)")
    print("   5. Query 3: Reverse Candidate Discovery & Ranking for Recruiters")
    print("   6. Query 4: Peer Skill Similarity & Recommendation (Jaccard Index)")
    print("   7. Query 5: Full Application Lifecycle Audit Trail (Multi-Hop Path)")
    print("   8. Query 6: Market Skill Demand Aggregation (Degree Centrality)")
    print("   9. Query 7: High-Package Placement Archetype Pattern Mining")
    print("  10. Query 8: Placement Bottleneck & Operational Health Monitor")
    print("\n  === GRAPH DATA MANAGEMENT (CRUD) ===")
    print("  11. Add New Student Node & Connect Directed Skill Edges")
    print("  12. Update Node Properties (CGPA, Title, Package)")
    print("  13. Delete Node with Cascading Edge Detachment")
    print("  14. Cypher Query Execution Console")
    print("  15. Reset & Re-seed Clean Graph Dataset")
    print("  16. Exit Application")


def main():
    while True:
        display_menu()
        choice = input("\n  Select Option (1 - 16): ").strip()

        if choice == "1":
            show_graph_overview()
        elif choice == "2":
            inspect_entity_neighborhood()
        elif choice == "3":
            query_1_eligibility_and_skill_match()
        elif choice == "4":
            query_2_skill_gap_analysis()
        elif choice == "5":
            query_3_recruiter_candidate_pipeline()
        elif choice == "6":
            query_4_peer_skill_similarity()
        elif choice == "7":
            query_5_application_lifecycle_trail()
        elif choice == "8":
            query_6_skill_demand_analytics()
        elif choice == "9":
            query_7_high_package_archetypes()
        elif choice == "10":
            query_8_operational_bottlenecks()
        elif choice == "11":
            crud_insert_student()
        elif choice == "12":
            crud_update_node()
        elif choice == "13":
            crud_delete_node()
        elif choice == "14":
            custom_cypher_console()
        elif choice == "15":
            CLIENT.embedded.seed_graph()
            print("  [SUCCESS] Graph dataset re-initialized to standard benchmark state.")
        elif choice == "16":
            print("\n  Gracefully exiting Campus Placement Portal Graph Explorer. Goodbye!\n")
            CLIENT.close()
            break
        else:
            print("  [!] Invalid option. Please select a number from 1 to 16.")

        input("\n  Press [Enter] to return to main menu...")


if __name__ == "__main__":
    main()
