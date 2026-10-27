// ═══════════════════════════════════════════════════════
// CAMPUS PLACEMENT PORTAL — SHARED APP LOGIC
// ═══════════════════════════════════════════════════════

// ── Helpers ──
const $ = id => document.getElementById(id);
const currentRole = () => localStorage.getItem('cpp-role') || 'student';

function switchRole(role) {
  localStorage.setItem('cpp-role', role);
  const r = $('role-select');
  if (r) r.value = role;
  showRoleBanner(role);
  showToast(`Role switched to: ${role.toUpperCase()}`);
  setTimeout(() => location.reload(), 500);
}

function showRoleBanner(role) {
  let banner = document.querySelector('.role-banner');
  if (!banner) {
    banner = document.createElement('div');
    banner.className = 'role-banner';
    document.body.insertBefore(banner, document.body.firstChild);
  }
  const msgs = {
    student: '🎓 STUDENT VIEW — Browse drives, apply, and track your application status.',
    recruiter: '🏢 RECRUITER VIEW — Post jobs, review applicants, schedule interviews, extend offers.',
    staff: '⚙️ STAFF / ADMIN VIEW — Oversee all drives, verify applications, and view full analytics.'
  };
  banner.textContent = msgs[role] || '';
  banner.classList.add('visible');
}

function showToast(msg) {
  let t = document.querySelector('.toast');
  if (!t) { t = document.createElement('div'); t.className = 'toast'; document.body.appendChild(t); }
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 3200);
}

// ── Status badges ──
function statusBadge(s) {
  const map = { hired:'status-hired', shortlisted:'status-shortlisted', pending:'status-pending', rejected:'status-rejected' };
  return `<span class="status-badge ${map[s]||''}">${s}</span>`;
}

// ── Drive card HTML ──
function driveCardHTML(d, full = false) {
  const pct = Math.round((d.applicants / (d.capacity * 8)) * 100);
  return `
    <div class="drive-card" onclick="openDriveModal(${d.id})">
      <span class="drive-tag open">● OPEN</span>
      <div>
        <div class="drive-company">${d.company}</div>
        <div class="drive-role">${d.role}</div>
      </div>
      <div class="drive-ctc">${d.ctc}</div>
      <div class="drive-meta">
        <span>Min CGPA: <strong>${d.minCgpa}</strong></span><br>
        <span>Depts: ${d.depts.join(', ')}</span>
      </div>
      <div>
        <div class="drive-deadline-label">Application Deadline</div>
        <div class="drive-deadline-val">${d.deadline}</div>
      </div>
      <div class="drive-applicants">${d.applicants} applicants · ${d.capacity} seats</div>
      <div class="drive-bar"><div class="drive-bar-fill" style="width:${Math.min(pct,100)}%"></div></div>
    </div>`;
}

// ── Student row HTML ──
function studentRowHTML(s, i) {
  const skillsHtml = s.skills.map(sk => `<span class="skill-chip">${sk}</span>`).join('');
  const cgpaClass = s.cgpa >= 9.0 ? 'cgpa-high' : '';
  return `
    <tr onclick="openStudentModal('${s.roll}')" style="cursor:pointer">
      <td style="font-size:11px;color:#aaa;">${String(i+1).padStart(2,'0')}</td>
      <td><span class="student-roll">${s.roll}</span></td>
      <td><span class="student-name">${s.name}</span></td>
      <td><span class="student-dept-badge">${s.dept}</span></td>
      <td><span class="cgpa-val ${cgpaClass}">${s.cgpa}</span></td>
      <td><div class="skills-list">${skillsHtml}</div></td>
      <td>${statusBadge(s.status)}</td>
    </tr>`;
}

// ── Drive Modal ──
function openDriveModal(id) {
  const d = DB.drives.find(x => x.id === id);
  if (!d) return;
  const role = currentRole();
  const skillsHtml = d.skills.map(s => `<span class="skill-chip">${s}</span>`).join('');

  let actionBtn = '';
  if (role === 'student') {
    actionBtn = `<button class="btn-primary" onclick="applyToDrive(${d.id})">Apply Now →</button>`;
  } else if (role === 'recruiter') {
    actionBtn = `<button class="btn-primary" onclick="showToast('Opening applicant list…')">View Applicants →</button>`;
  } else {
    actionBtn = `<button class="btn-primary" onclick="showToast('Drive statistics loaded.')">Drive Analytics →</button>`;
  }

  const html = `
    <div class="modal-overlay open" id="drive-modal" onclick="closeModal('drive-modal')">
      <div class="modal" onclick="event.stopPropagation()">
        <div class="modal-header">
          <div>
            <div style="font-size:11px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#999;margin-bottom:4px">${d.company}</div>
            <div class="modal-title">${d.role}</div>
          </div>
          <div class="modal-close" onclick="closeModal('drive-modal')">✕</div>
        </div>
        <div class="modal-body">
          <div class="modal-kpi-row">
            <div class="modal-kpi"><div class="modal-kpi-label">Package</div><div class="modal-kpi-val" style="color:var(--red)">${d.ctc}</div></div>
            <div class="modal-kpi"><div class="modal-kpi-label">Min CGPA</div><div class="modal-kpi-val">${d.minCgpa}</div></div>
            <div class="modal-kpi"><div class="modal-kpi-label">Seats</div><div class="modal-kpi-val">${d.capacity}</div></div>
          </div>
          <p style="font-size:13px;line-height:1.7;color:#444;margin-bottom:20px">${d.description}</p>
          <div style="margin-bottom:20px">
            <div style="font-size:9px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#888;margin-bottom:8px">Required Skills</div>
            <div class="skills-list">${skillsHtml}</div>
          </div>
          <div style="display:flex;gap:12px;margin-bottom:20px">
            <div>
              <div style="font-size:9px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#888">Deadline</div>
              <div style="font-size:16px;font-weight:700;margin-top:4px">${d.deadline}</div>
            </div>
            <div style="margin-left:40px">
              <div style="font-size:9px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#888">Type</div>
              <div style="font-size:16px;font-weight:700;margin-top:4px">${d.type}</div>
            </div>
            <div style="margin-left:40px">
              <div style="font-size:9px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#888">Eligible Depts</div>
              <div style="font-size:13px;font-weight:500;margin-top:4px">${d.depts.join(' · ')}</div>
            </div>
          </div>
          ${actionBtn}
        </div>
      </div>
    </div>`;
  document.body.insertAdjacentHTML('beforeend', html);
}

function applyToDrive(id) {
  const d = DB.drives.find(x => x.id === id);
  closeModal('drive-modal');
  showToast(`Application submitted for ${d.role} at ${d.company}!`);
}

// ── Student Modal ──
function openStudentModal(roll) {
  const s = DB.students.find(x => x.roll === roll);
  if (!s) return;
  const role = currentRole();
  const skillsHtml = s.skills.map(sk => `<span class="skill-chip">${sk}</span>`).join('');

  let actionSection = '';
  if (role === 'staff' || role === 'recruiter') {
    actionSection = `
      <div style="border-top:1px solid #111;padding-top:20px;margin-top:20px;display:flex;gap:12px">
        <button class="btn-primary" onclick="showToast('Application shortlisted.')">Shortlist</button>
        <button class="btn-secondary" onclick="showToast('Interview scheduled.')">Schedule Interview</button>
        <button class="btn-secondary" onclick="showToast('Offer extended.')">Extend Offer</button>
      </div>`;
  }

  const html = `
    <div class="modal-overlay open" id="student-modal" onclick="closeModal('student-modal')">
      <div class="modal" onclick="event.stopPropagation()">
        <div class="modal-header">
          <div>
            <div style="font-size:11px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#999;margin-bottom:4px">${s.roll} · ${s.dept}</div>
            <div class="modal-title">${s.name}</div>
          </div>
          <div class="modal-close" onclick="closeModal('student-modal')">✕</div>
        </div>
        <div class="modal-body">
          <div class="modal-kpi-row">
            <div class="modal-kpi"><div class="modal-kpi-label">CGPA</div><div class="modal-kpi-val" style="color:var(--red)">${s.cgpa}</div></div>
            <div class="modal-kpi"><div class="modal-kpi-label">Status</div><div style="margin-top:8px">${statusBadge(s.status)}</div></div>
            <div class="modal-kpi"><div class="modal-kpi-label">Offer</div><div class="modal-kpi-val">${s.offer || '—'}</div></div>
          </div>
          ${s.company ? `<p style="font-size:13px;font-weight:600;color:#444;margin-bottom:16px">Company: <span style="color:var(--red)">${s.company}</span></p>` : ''}
          <div style="margin-bottom:20px">
            <div style="font-size:9px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#888;margin-bottom:8px">Skills</div>
            <div class="skills-list">${skillsHtml}</div>
          </div>
          ${actionSection}
        </div>
      </div>
    </div>`;
  document.body.insertAdjacentHTML('beforeend', html);
}

function closeModal(id) {
  const el = $(id);
  if (el) el.remove();
}

// ── Page init ──
document.addEventListener('DOMContentLoaded', () => {
  const role = currentRole();
  const rs = $('role-select');
  if (rs) rs.value = role;

  // Highlight active nav link
  const path = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-link').forEach(a => {
    a.classList.toggle('active', a.getAttribute('href') === path);
  });

  // ── HOME PAGE ──
  const drivesContainer = $('drives-container');
  if (drivesContainer) {
    drivesContainer.innerHTML = DB.drives.slice(0,4).map(d => driveCardHTML(d)).join('');
  }

  const tbody = $('students-tbody');
  if (tbody) {
    tbody.innerHTML = DB.students.slice(0,8).map((s,i) => studentRowHTML(s,i)).join('');
  }

  // ── DASHBOARD PAGE ──
  const kpiRow = $('dash-kpi-row');
  if (kpiRow) renderDashboard();

  // ── DRIVES PAGE ──
  const drivesFullGrid = $('drives-full-grid');
  if (drivesFullGrid) renderDrivesPage();

  // ── STUDENTS PAGE ──
  const studentsFullTable = $('students-full-tbody');
  if (studentsFullTable) renderStudentsPage();

  // ── ANALYTICS PAGE ──
  const analyticsMain = $('analytics-main');
  if (analyticsMain) renderAnalyticsPage();
});

// ════════════════════════════════
// DASHBOARD
// ════════════════════════════════
function renderDashboard() {
  const s = DB.stats;
  $('dash-kpi-row').innerHTML = `
    <div class="dash-kpi red"><div class="dash-kpi-label">Highest CTC</div><div class="dash-kpi-val">${s.highestCtc}</div><div class="dash-kpi-sub">Google — Batch 2026</div></div>
    <div class="dash-kpi"><div class="dash-kpi-label">Avg. CTC</div><div class="dash-kpi-val">${s.avgCtc}</div><div class="dash-kpi-sub">+12% vs Batch 2025</div></div>
    <div class="dash-kpi"><div class="dash-kpi-label">Placed</div><div class="dash-kpi-val">${s.placed}</div><div class="dash-kpi-sub">of ${s.eligible} eligible</div></div>
    <div class="dash-kpi"><div class="dash-kpi-label">Offers</div><div class="dash-kpi-val">${s.offers}</div><div class="dash-kpi-sub">Total offers extended</div></div>
    <div class="dash-kpi"><div class="dash-kpi-label">Companies</div><div class="dash-kpi-val">${s.companies}</div><div class="dash-kpi-sub">Registered for 2026</div></div>
    <div class="dash-kpi"><div class="dash-kpi-label">Open Jobs</div><div class="dash-kpi-val">${s.openJobs}</div><div class="dash-kpi-sub">Active postings</div></div>
  `;

  $('dash-timeline').innerHTML = DB.notifications.map(n => `
    <div class="timeline-item">
      <div class="tl-date">${n.date}</div>
      <div class="tl-dot ${n.type==='offer'?'red':''}"></div>
      <div class="tl-content">
        <div class="tl-title">${n.title}</div>
        <div class="tl-sub">${n.desc}</div>
      </div>
    </div>`).join('');

  const funnelData = [
    { label: 'Registered', count: 847, max: 847 },
    { label: 'Eligible', count: 712, max: 847 },
    { label: 'Applied', count: 598, max: 847 },
    { label: 'Shortlisted', count: 380, max: 847 },
    { label: 'Interviewed', count: 290, max: 847 },
    { label: 'Offered', count: 312, max: 847 },
    { label: 'Placed', count: 634, max: 847 },
  ];
  $('dash-funnel').innerHTML = funnelData.map(f => `
    <div class="funnel-row">
      <div class="funnel-label">${f.label}</div>
      <div class="funnel-bar-outer"><div class="funnel-bar-inner" style="width:${(f.count/f.max*100).toFixed(0)}%"></div></div>
      <div class="funnel-count">${f.count}</div>
    </div>`).join('');

  // Recent drives table in dashboard
  const dtbody = $('dash-drives-tbody');
  if (dtbody) {
    dtbody.innerHTML = DB.drives.slice(0,5).map(d => `
      <tr onclick="openDriveModal(${d.id})" style="cursor:pointer">
        <td style="font-weight:700">${d.company}</td>
        <td>${d.role}</td>
        <td style="color:var(--red);font-weight:700">${d.ctc}</td>
        <td>${d.deadline}</td>
        <td>${d.applicants}</td>
        <td><span class="drive-tag open" style="font-size:9px">OPEN</span></td>
      </tr>`).join('');
  }
}

// ════════════════════════════════
// DRIVES PAGE
// ════════════════════════════════
function renderDrivesPage(filter = 'all') {
  let drives = DB.drives;
  if (filter !== 'all') drives = drives.filter(d =>
    filter === 'internship' ? d.type === 'Internship' : d.depts.includes(filter.toUpperCase())
  );
  $('drives-full-grid').innerHTML = drives.map(d => driveCardHTML(d, true)).join('');
}

function setDriveFilter(btn, filter) {
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  renderDrivesPage(filter);
}

// ════════════════════════════════
// STUDENTS PAGE
// ════════════════════════════════
function renderStudentsPage(query = '') {
  const tbody = $('students-full-tbody');
  let students = DB.students;
  if (query) {
    const q = query.toLowerCase();
    students = students.filter(s =>
      s.name.toLowerCase().includes(q) ||
      s.roll.toLowerCase().includes(q) ||
      s.dept.toLowerCase().includes(q) ||
      s.skills.some(sk => sk.toLowerCase().includes(q))
    );
  }
  tbody.innerHTML = students.length
    ? students.map((s,i) => studentRowHTML(s,i)).join('')
    : `<tr><td colspan="7" style="text-align:center;padding:48px;color:#aaa;font-size:13px">No students match your search.</td></tr>`;
}

function doSearch() {
  const q = $('student-search').value.trim();
  renderStudentsPage(q);
}

// ════════════════════════════════
// ANALYTICS PAGE
// ════════════════════════════════
function renderAnalyticsPage() {
  // Dept grid already in HTML, animated via CSS
}
