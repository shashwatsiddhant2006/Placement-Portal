// ═══════════════════════════════════════════════════════
// CAMPUS PLACEMENT PORTAL — SHARED DATA STORE
// ═══════════════════════════════════════════════════════

const DB = {
  students: [
    { roll: 'CS21001', name: 'Aditya Sharma',   dept: 'CSE', cgpa: 9.4, skills: ['Python','ML','React'],     status: 'hired',       offer: '₹42 LPA', company: 'Google' },
    { roll: 'CS21002', name: 'Priya Gupta',      dept: 'CSE', cgpa: 9.1, skills: ['Java','DSA','Spring'],    status: 'hired',       offer: '₹32 LPA', company: 'Microsoft' },
    { roll: 'EC21010', name: 'Rohan Mehra',      dept: 'ECE', cgpa: 8.7, skills: ['VLSI','Embedded','C++'], status: 'shortlisted', offer: null,        company: 'Samsung' },
    { roll: 'CS21005', name: 'Sneha Verma',      dept: 'CSE', cgpa: 8.9, skills: ['React','Node','AWS'],     status: 'hired',       offer: '₹28 LPA', company: 'Amazon' },
    { roll: 'ME21003', name: 'Arjun Singh',      dept: 'ME',  cgpa: 7.8, skills: ['AutoCAD','MATLAB'],       status: 'pending',     offer: null,        company: null },
    { roll: 'CS21007', name: 'Kavya Reddy',      dept: 'CSE', cgpa: 9.2, skills: ['ML','TensorFlow','SQL'],  status: 'hired',       offer: '₹35 LPA', company: 'Adobe' },
    { roll: 'EC21015', name: 'Nikhil Joshi',     dept: 'ECE', cgpa: 8.2, skills: ['IoT','Python','Linux'],   status: 'shortlisted', offer: null,        company: 'Qualcomm' },
    { roll: 'CS21012', name: 'Divya Nair',       dept: 'CSE', cgpa: 8.6, skills: ['Go','Docker','K8s'],      status: 'hired',       offer: '₹26 LPA', company: 'Infosys' },
    { roll: 'IT21004', name: 'Rahul Khanna',     dept: 'IT',  cgpa: 8.0, skills: ['SQL','PHP','Laravel'],    status: 'rejected',    offer: null,        company: null },
    { roll: 'CS21020', name: 'Ananya Iyer',      dept: 'CSE', cgpa: 9.5, skills: ['Rust','Algo','Python'],   status: 'hired',       offer: '₹38 LPA', company: 'Goldman Sachs' },
    { roll: 'ME21008', name: 'Varun Tiwari',     dept: 'ME',  cgpa: 7.5, skills: ['SolidWorks','FEA'],       status: 'pending',     offer: null,        company: null },
    { roll: 'CS21018', name: 'Simran Kapoor',    dept: 'CSE', cgpa: 8.8, skills: ['Flutter','Dart','Firebase'], status: 'shortlisted', offer: null,    company: 'Deloitte' },
  ],

  drives: [
    {
      id: 1, company: 'Google', role: 'Software Engineer', ctc: '₹42 LPA',
      type: 'Full-Time', minCgpa: 8.5, depts: ['CSE','IT'],
      deadline: '05 Nov 2026', applicants: 84, capacity: 12,
      description: 'SWE L3/L4 role — Systems & ML team. 3 rounds: DSA + System Design + Behavioural.',
      skills: ['Python','C++','DSA','System Design'],
      status: 'open'
    },
    {
      id: 2, company: 'Microsoft', role: 'SDE II', ctc: '₹32 LPA',
      type: 'Full-Time', minCgpa: 8.0, depts: ['CSE','IT','EC'],
      deadline: '10 Nov 2026', applicants: 120, capacity: 20,
      description: 'Product engineering roles in Azure & Office 365. Strong DSA required.',
      skills: ['Java','C#','Azure','DSA'],
      status: 'open'
    },
    {
      id: 3, company: 'Goldman Sachs', role: 'Technology Analyst', ctc: '₹38 LPA',
      type: 'Full-Time', minCgpa: 8.5, depts: ['CSE','IT','ME'],
      deadline: '08 Nov 2026', applicants: 67, capacity: 8,
      description: 'FinTech engineering — Strats & Quant division. Quantitative aptitude required.',
      skills: ['Python','Quant Finance','SQL'],
      status: 'open'
    },
    {
      id: 4, company: 'Adobe', role: 'MTS — Experience Cloud', ctc: '₹35 LPA',
      type: 'Full-Time', minCgpa: 8.0, depts: ['CSE','IT'],
      deadline: '12 Nov 2026', applicants: 55, capacity: 10,
      description: 'Full-stack engineering on Experience Cloud platform. React & distributed systems.',
      skills: ['React','Node.js','AWS','System Design'],
      status: 'open'
    },
    {
      id: 5, company: 'Samsung R&D', role: 'Staff Engineer', ctc: '₹24 LPA',
      type: 'Full-Time', minCgpa: 7.5, depts: ['ECE','EEE','CSE'],
      deadline: '15 Nov 2026', applicants: 98, capacity: 25,
      description: 'Embedded systems and SoC design. Roles in Bangalore & Noida R&D centres.',
      skills: ['VLSI','Embedded C','Linux'],
      status: 'open'
    },
    {
      id: 6, company: 'McKinsey Digital', role: 'Business Technology Analyst', ctc: '₹18 LPA',
      type: 'Full-Time', minCgpa: 8.0, depts: ['CSE','ME','CE'],
      deadline: '20 Nov 2026', applicants: 40, capacity: 5,
      description: 'Consulting + technology hybrid role. Strong analytical and communication skills.',
      skills: ['Analytics','SQL','Communication'],
      status: 'open'
    },
    {
      id: 7, company: 'Qualcomm', role: 'ASIC Design Engineer', ctc: '₹20 LPA',
      type: 'Full-Time', minCgpa: 7.5, depts: ['ECE','EEE'],
      deadline: '18 Nov 2026', applicants: 62, capacity: 15,
      description: 'Chip design and verification. Focus on 5G baseband and Snapdragon platforms.',
      skills: ['Verilog','SystemVerilog','VLSI'],
      status: 'open'
    },
    {
      id: 8, company: 'Deloitte', role: 'Analyst — USI Tech', ctc: '₹10.5 LPA',
      type: 'Full-Time', minCgpa: 7.0, depts: ['CSE','IT','ME','CE'],
      deadline: '25 Nov 2026', applicants: 210, capacity: 50,
      description: 'Technology consulting and implementation. Business analyst & developer roles.',
      skills: ['SQL','SAP','Communication'],
      status: 'open'
    },
    {
      id: 9, company: 'Amazon', role: 'SDE I', ctc: '₹28 LPA',
      type: 'Full-Time', minCgpa: 8.0, depts: ['CSE','IT'],
      deadline: '03 Nov 2026', applicants: 145, capacity: 18,
      description: 'Core engineering and AWS platform. LP heavy interviews — prepare STAR stories.',
      skills: ['Java','DSA','AWS','System Design'],
      status: 'open'
    },
    {
      id: 10, company: 'Infosys', role: 'Systems Engineer', ctc: '₹8 LPA',
      type: 'Full-Time', minCgpa: 6.5, depts: ['CSE','IT','ME','CE','ECE'],
      deadline: '30 Nov 2026', applicants: 380, capacity: 100,
      description: 'Mass hiring. Service line rotation — Java, .NET, Testing, and Infra tracks.',
      skills: ['Java','.NET','Communication'],
      status: 'open'
    },
    {
      id: 11, company: 'Microsoft', role: 'Research Intern', ctc: '₹2.5L/mo',
      type: 'Internship', minCgpa: 8.5, depts: ['CSE','IT'],
      deadline: '01 Nov 2026', applicants: 32, capacity: 3,
      description: '6-month research internship at MSRI Bangalore. ML systems and AI safety tracks.',
      skills: ['ML','Python','Research'],
      status: 'open'
    },
    {
      id: 12, company: 'Tata Consultancy Services', role: 'Software Developer', ctc: '₹7.5 LPA',
      type: 'Full-Time', minCgpa: 6.0, depts: ['CSE','IT','ME','CE','ECE'],
      deadline: '28 Nov 2026', applicants: 450, capacity: 120,
      description: 'Mass recruiter. Digital and Cloud tracks. Strong aptitude test performance needed.',
      skills: ['Java','SQL','Communication'],
      status: 'open'
    },
  ],

  stats: {
    totalStudents: 847,
    eligible: 712,
    placed: 634,
    offers: 312,
    companies: 47,
    openJobs: 128,
    highestCtc: '₹42 LPA',
    avgCtc: '₹18.4 LPA',
    placementRate: 89,
    topRecruiter: 'Google'
  },

  notifications: [
    { id: 1, date: '27 Oct', title: 'Google Drive Open', desc: 'Applications now open. Deadline: 05 Nov.', type: 'drive' },
    { id: 2, date: '26 Oct', title: 'Shortlist Released', desc: 'Amazon SDE I — 42 students shortlisted for Round 2.', type: 'update' },
    { id: 3, date: '25 Oct', title: 'Offer Letter', desc: 'Congratulations! Aditya Sharma — Google offer confirmed ₹42 LPA.', type: 'offer' },
    { id: 4, date: '24 Oct', title: 'Interview Scheduled', desc: 'Goldman Sachs Tech Interview — 28 Oct, 10:00 AM.', type: 'interview' },
    { id: 5, date: '23 Oct', title: 'New Drive: McKinsey', desc: 'McKinsey Digital — BTA role. Deadline: 20 Nov.', type: 'drive' },
  ]
};
