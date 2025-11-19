// JavaScript for Recruiter Dashboard

const API_BASE = '';
let selectedCandidates = new Set();
let currentJobId = null;
let currentCandidateId = null;

// Navigation
document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', (e) => {
        e.preventDefault();
        const page = item.dataset.page;
        switchPage(page);
    });
});

function switchPage(pageName) {
    // Update nav items
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    document.querySelector(`[data-page="${pageName}"]`).classList.add('active');

    // Update pages
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });
    document.getElementById(`${pageName}-page`).classList.add('active');

    // Update page title
    const titles = {
        'dashboard': { title: 'Dashboard', subtitle: 'Welcome back! Here\'s what\'s happening today.' },
        'candidates': { title: 'Candidates', subtitle: 'Select candidates to optimize for job postings' },
        'optimize': { title: 'Bulk Optimization', subtitle: 'Optimize multiple candidates for a specific job posting' },
        'review': { title: 'Review Queue', subtitle: 'Review and approve optimized resumes' }
    };
    
    if (titles[pageName]) {
        document.getElementById('page-title').textContent = titles[pageName].title;
        document.getElementById('page-subtitle').textContent = titles[pageName].subtitle;
    }

    // Load page data
    if (pageName === 'dashboard') {
        loadDashboard();
    } else if (pageName === 'candidates') {
        loadCandidates();
    } else if (pageName === 'optimize') {
        loadOptimizePage();
    } else if (pageName === 'review') {
        loadReviewPage();
    }
}

// Navigation helper
function navigateToPage(pageName) {
    switchPage(pageName);
}

// Dashboard
async function loadDashboard() {
    try {
        const [analyticsRes, candidatesRes, jobsRes] = await Promise.all([
            fetch(`${API_BASE}/api/recruiter/analytics`),
            fetch(`${API_BASE}/api/recruiter/candidates?limit=1`),
            fetch(`${API_BASE}/api/recruiter/jobs`)
        ]);

        const analytics = await analyticsRes.json();
        const candidates = await candidatesRes.json();
        const jobs = await jobsRes.json();

        if (analytics.success) {
            document.getElementById('stat-candidates').textContent = analytics.analytics.total_candidates;
            document.getElementById('stat-jobs').textContent = analytics.analytics.total_jobs;
            document.getElementById('stat-optimizations').textContent = analytics.analytics.total_optimizations;
            document.getElementById('stat-pending').textContent = analytics.analytics.pending_review;
        }
    } catch (error) {
        showMessage('Error loading dashboard', 'error');
    }
}

// Candidates
async function loadCandidates() {
    try {
        const search = document.getElementById('candidate-search')?.value || '';
        const res = await fetch(`${API_BASE}/api/recruiter/candidates?limit=50&search=${search}`);
        const data = await res.json();

        if (data.success) {
            displayCandidates(data.candidates);
        }
    } catch (error) {
        showMessage('Error loading candidates', 'error');
    }
}

function displayCandidates(candidates) {
    const container = document.getElementById('candidates-list');
    container.innerHTML = candidates.map(candidate => `
        <div class="candidate-card ${selectedCandidates.has(candidate.id) ? 'selected' : ''}" 
             onclick="toggleCandidate(${candidate.id})">
            <input type="checkbox" 
                   ${selectedCandidates.has(candidate.id) ? 'checked' : ''}
                   onclick="event.stopPropagation(); toggleCandidate(${candidate.id})">
            <h3>${candidate.name}</h3>
            <div class="candidate-info">${candidate.email}</div>
            <div class="candidate-info">${candidate.experience?.[0]?.title || 'N/A'} at ${candidate.experience?.[0]?.company || 'N/A'}</div>
            <div class="skills">
                ${candidate.skills?.map(skill => `<span class="skill-tag">${skill}</span>`).join('') || ''}
            </div>
        </div>
    `).join('');
    
    updateSelectedCount();
}

function toggleCandidate(candidateId) {
    if (selectedCandidates.has(candidateId)) {
        selectedCandidates.delete(candidateId);
    } else {
        selectedCandidates.add(candidateId);
    }
    loadCandidates();
    updateSelectedList();
}

async function selectAll() {
    // Get all visible candidates from API
    try {
        const res = await fetch(`${API_BASE}/api/recruiter/candidates?limit=50`);
        const data = await res.json();
        if (data.success) {
            data.candidates.forEach(c => selectedCandidates.add(c.id));
            loadCandidates();
            updateSelectedList();
        }
    } catch (error) {
        console.error('Error selecting all:', error);
    }
}

function deselectAll() {
    selectedCandidates.clear();
    loadCandidates();
    updateSelectedList();
}

function updateSelectedCount() {
    const countEl = document.getElementById('selected-count');
    if (countEl) {
        countEl.textContent = `${selectedCandidates.size} selected`;
    }
}

function updateSelectedList() {
    const container = document.getElementById('selected-candidates-list');
    if (!container) return;
    
    if (selectedCandidates.size === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-inbox"></i>
                <p>No candidates selected. Go to Candidates tab to select.</p>
            </div>
        `;
        return;
    }
    
    // Fetch candidate details for selected ones
    Promise.all(
        Array.from(selectedCandidates).map(id =>
            fetch(`${API_BASE}/api/recruiter/candidates/${id}`)
                .then(r => r.json())
                .then(d => d.candidate)
        )
    ).then(candidates => {
        container.innerHTML = candidates.map(c => `
            <div class="selected-candidate-item" style="display: flex; justify-content: space-between; align-items: center; padding: 0.75rem; background: var(--bg-card); border-radius: 8px; margin-bottom: 0.5rem;">
                <span>${c.name} - ${c.email}</span>
                <button class="btn-modern outline" onclick="toggleCandidate(${c.id})" style="padding: 0.5rem 1rem; font-size: 0.875rem;">
                    <i class="fas fa-times"></i> Remove
                </button>
            </div>
        `).join('');
    });
}

// Optimize Page
async function loadOptimizePage() {
    const jobsRes = await fetch(`${API_BASE}/api/recruiter/jobs`);
    const jobs = await jobsRes.json();
    
    const jobSelect = document.getElementById('optimize-job-select');
    if (jobSelect && jobs.success) {
        jobSelect.innerHTML = '<option value="">-- Select Job --</option>' +
            jobs.jobs.map(j => `<option value="${j.id}">${j.title} - ${j.company}</option>`).join('');
    }
    
    updateSelectedList();
}

async function startBulkOptimization() {
    const jobId = document.getElementById('optimize-job-select').value;
    
    if (!jobId) {
        showMessage('Please select a job posting', 'error');
        return;
    }
    
    if (selectedCandidates.size === 0) {
        showMessage('Please select at least one candidate', 'error');
        return;
    }
    
    const btn = document.getElementById('optimize-btn-text');
    const loader = document.getElementById('optimize-loader');
    const progressDiv = document.getElementById('optimization-progress');
    const resultsDiv = document.getElementById('optimization-results');
    
    btn.style.display = 'none';
    loader.style.display = 'inline-block';
    progressDiv.style.display = 'block';
    resultsDiv.style.display = 'none';
    
    // Simulate progress
    let progress = 0;
    const progressInterval = setInterval(() => {
        progress += 2;
        if (progress > 90) progress = 90;
        document.getElementById('progress-fill').style.width = progress + '%';
        document.getElementById('progress-text').textContent = `Processing ${progress}%...`;
    }, 200);
    
    try {
        const res = await fetch(`${API_BASE}/api/recruiter/optimize/bulk`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                candidate_ids: Array.from(selectedCandidates),
                job_id: parseInt(jobId)
            })
        });
        
        const data = await res.json();
        
        clearInterval(progressInterval);
        document.getElementById('progress-fill').style.width = '100%';
        document.getElementById('progress-text').textContent = 'Complete!';
        
        if (data.success) {
            displayOptimizationResults(data);
            resultsDiv.style.display = 'block';
            showMessage(`Optimized ${data.summary.successful} candidates!`, 'success');
            setTimeout(() => {
                switchPage('review');
                document.getElementById('review-job-select').value = jobId;
                loadReviewQueue();
            }, 2000);
        } else {
            showMessage(data.error || 'Optimization failed', 'error');
        }
    } catch (error) {
        clearInterval(progressInterval);
        showMessage('Error during optimization', 'error');
    } finally {
        btn.style.display = 'inline';
        loader.style.display = 'none';
    }
}

function displayOptimizationResults(data) {
    const container = document.getElementById('optimization-results');
    container.innerHTML = `
        <div class="optimization-summary">
            <h3>Optimization Complete!</h3>
            <div class="summary-stats">
                <div class="summary-stat">
                    <div class="summary-stat-value">${data.summary.successful}</div>
                    <div class="summary-stat-label">Successful</div>
                </div>
                <div class="summary-stat">
                    <div class="summary-stat-value">${data.summary.failed}</div>
                    <div class="summary-stat-label">Failed</div>
                </div>
                <div class="summary-stat">
                    <div class="summary-stat-value">${data.total_candidates}</div>
                    <div class="summary-stat-label">Total</div>
                </div>
            </div>
            <p style="margin-top: 20px;">
                <strong>Next step:</strong> Go to Review Queue to review and approve optimizations.
            </p>
        </div>
    `;
}

// Review Page
async function loadReviewPage() {
    const jobsRes = await fetch(`${API_BASE}/api/recruiter/jobs`);
    const jobs = await jobsRes.json();
    
    const jobSelect = document.getElementById('review-job-select');
    if (jobSelect && jobs.success) {
        jobSelect.innerHTML = '<option value="">-- Select Job --</option>' +
            jobs.jobs.map(j => `<option value="${j.id}">${j.title} - ${j.company}</option>`).join('');
    }
}

async function loadReviewQueue() {
    const jobId = document.getElementById('review-job-select').value;
    if (!jobId) return;
    
    try {
        const res = await fetch(`${API_BASE}/api/recruiter/review/${jobId}`);
        const data = await res.json();
        
        if (data.success) {
            displayReviewQueue(data.candidates, jobId);
        }
    } catch (error) {
        showMessage('Error loading review queue', 'error');
    }
}

function displayReviewQueue(candidates, jobId) {
    const container = document.getElementById('review-queue');
    
    if (candidates.length === 0) {
        container.innerHTML = '<p>No candidates in review queue. Optimize some candidates first!</p>';
        return;
    }
    
    container.innerHTML = candidates.map(c => `
        <div class="review-item">
            <div class="review-item-info">
                <h3>${c.candidate_name}</h3>
                <div class="scores">
                    <span class="score-badge match">Match: ${c.match_score}%</span>
                    <span class="score-badge quality">Quality: ${c.quality_score}/100</span>
                </div>
            </div>
            <div class="item-actions" style="display: flex; gap: 0.75rem;">
                <button class="btn-modern outline" onclick="viewComparison(${c.candidate_id}, ${jobId})">
                    <i class="fas fa-eye"></i> Review
                </button>
                <button class="btn-modern success" onclick="quickApprove(${c.candidate_id}, ${jobId})">
                    <i class="fas fa-check"></i> Approve
                </button>
            </div>
        </div>
    `).join('');
}

async function viewComparison(candidateId, jobId) {
    currentCandidateId = candidateId;
    currentJobId = jobId;
    
    try {
        const res = await fetch(`${API_BASE}/api/recruiter/review/compare/${candidateId}?job_id=${jobId}`);
        const data = await res.json();
        
        if (data.success) {
            document.getElementById('original-content').textContent = data.original;
            document.getElementById('optimized-content').textContent = data.optimized;
            document.getElementById('compare-modal').classList.add('active');
        }
    } catch (error) {
        showMessage('Error loading comparison', 'error');
    }
}

async function approveOptimization() {
    if (!currentCandidateId || !currentJobId) return;
    
    try {
        const res = await fetch(`${API_BASE}/api/recruiter/approve`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                candidate_id: currentCandidateId,
                job_id: currentJobId
            })
        });
        
        const data = await res.json();
        if (data.success) {
            showMessage('Optimization approved!', 'success');
            closeModal('compare-modal');
            loadReviewQueue();
            loadDashboard();
        }
    } catch (error) {
        showMessage('Error approving optimization', 'error');
    }
}

async function quickApprove(candidateId, jobId) {
    try {
        const res = await fetch(`${API_BASE}/api/recruiter/approve`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                candidate_id: candidateId,
                job_id: jobId
            })
        });
        
        const data = await res.json();
        if (data.success) {
            showMessage('Optimization approved!', 'success');
            loadReviewQueue();
            loadDashboard();
        }
    } catch (error) {
        showMessage('Error approving optimization', 'error');
    }
}

function rejectOptimization() {
    showMessage('Optimization rejected', 'success');
    closeModal('compare-modal');
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
}

function showMessage(text, type = 'info') {
    const toast = document.getElementById('toast');
    const toastMessage = toast.querySelector('.toast-message');
    const toastIcon = toast.querySelector('.toast-icon');
    
    toast.className = `toast ${type}`;
    toastMessage.textContent = text;
    
    // Set icon based on type
    if (type === 'success') {
        toastIcon.className = 'toast-icon fas fa-check-circle';
    } else if (type === 'error') {
        toastIcon.className = 'toast-icon fas fa-exclamation-circle';
    } else {
        toastIcon.className = 'toast-icon fas fa-info-circle';
    }
    
    toast.style.display = 'block';
    
    setTimeout(() => {
        toast.style.display = 'none';
    }, 5000);
}

// Search functionality
document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('candidate-search');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(loadCandidates, 300));
    }
    
    loadDashboard();
});

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Close modals on outside click
window.onclick = function(event) {
    if (event.target.classList.contains('modal-overlay')) {
        event.target.classList.remove('active');
    }
}

