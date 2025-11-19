// JavaScript for Database-Enabled Resume Optimizer

const API_BASE = '';

// Navigation
document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', (e) => {
        e.preventDefault();
        const page = item.dataset.page;
        switchPage(page);
    });
});

function switchPage(pageName) {
    // Update nav
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    document.querySelector(`[data-page="${pageName}"]`).classList.add('active');

    // Update pages
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });
    document.getElementById(`${pageName}-page`).classList.add('active');

    // Load page data
    if (pageName === 'dashboard') {
        loadDashboard();
    } else if (pageName === 'resumes') {
        loadResumes();
    } else if (pageName === 'jobs') {
        loadJobs();
    } else if (pageName === 'optimize') {
        loadOptimizePage();
    } else if (pageName === 'history') {
        loadHistory();
    }
}

// Dashboard
async function loadDashboard() {
    try {
        const [analyticsRes, optimizationsRes] = await Promise.all([
            fetch(`${API_BASE}/api/analytics`),
            fetch(`${API_BASE}/api/optimizations`)
        ]);

        const analytics = await analyticsRes.json();
        const optimizations = await optimizationsRes.json();

        if (analytics.success) {
            document.getElementById('stat-resumes').textContent = analytics.analytics.total_resumes;
            document.getElementById('stat-jobs').textContent = analytics.analytics.total_jobs;
            document.getElementById('stat-optimizations').textContent = analytics.analytics.total_optimizations;
            document.getElementById('stat-match').textContent = `${analytics.analytics.avg_match_score}%`;
        }

        if (optimizations.success) {
            displayRecentOptimizations(optimizations.optimizations.slice(0, 5));
        }
    } catch (error) {
        showMessage('Error loading dashboard', 'error');
    }
}

function displayRecentOptimizations(optimizations) {
    const container = document.getElementById('recent-optimizations');
    if (optimizations.length === 0) {
        container.innerHTML = '<p>No optimizations yet. Start optimizing your resume!</p>';
        return;
    }

    container.innerHTML = optimizations.map(opt => `
        <div class="item-card">
            <div class="item-info">
                <h3>Optimization #${opt.id}</h3>
                <p>Match Score: ${opt.match_score || 'N/A'}% | Quality: ${opt.quality_score || 'N/A'}/100</p>
                <p><small>${new Date(opt.created_at).toLocaleString()}</small></p>
            </div>
            <div class="item-actions">
                <button class="btn-secondary" onclick="viewOptimization(${opt.id})">View</button>
            </div>
        </div>
    `).join('');
}

// Resumes
async function loadResumes() {
    try {
        const res = await fetch(`${API_BASE}/api/resumes`);
        const data = await res.json();

        if (data.success) {
            displayResumes(data.resumes);
        } else {
            showMessage('Error loading resumes', 'error');
        }
    } catch (error) {
        showMessage('Error loading resumes', 'error');
    }
}

function displayResumes(resumes) {
    const container = document.getElementById('resumes-list');
    if (resumes.length === 0) {
        container.innerHTML = '<p>No resumes uploaded yet. Upload your first resume!</p>';
        return;
    }

    container.innerHTML = resumes.map(resume => `
        <div class="item-card">
            <div class="item-info">
                <h3>${resume.name}</h3>
                <p>${resume.filename} | ${resume.word_count || 0} words | ${resume.file_type || 'unknown'}</p>
                <p><small>Uploaded: ${new Date(resume.created_at).toLocaleString()}</small></p>
            </div>
            <div class="item-actions">
                <button class="btn-secondary" onclick="viewResume(${resume.id})">View</button>
                <button class="btn-danger" onclick="deleteResume(${resume.id})">Delete</button>
            </div>
        </div>
    `).join('');
}

// Jobs
async function loadJobs() {
    try {
        const res = await fetch(`${API_BASE}/api/jobs`);
        const data = await res.json();

        if (data.success) {
            displayJobs(data.jobs);
        } else {
            showMessage('Error loading jobs', 'error');
        }
    } catch (error) {
        showMessage('Error loading jobs', 'error');
    }
}

function displayJobs(jobs) {
    const container = document.getElementById('jobs-list');
    if (jobs.length === 0) {
        container.innerHTML = '<p>No job descriptions added yet. Add your first job!</p>';
        return;
    }

    container.innerHTML = jobs.map(job => `
        <div class="item-card">
            <div class="item-info">
                <h3>${job.title}</h3>
                <p>${job.company || 'Company not specified'}</p>
                <p>${job.content}</p>
                <p><small>Added: ${new Date(job.created_at).toLocaleString()}</small></p>
            </div>
            <div class="item-actions">
                <button class="btn-secondary" onclick="viewJob(${job.id})">View</button>
                <button class="btn-danger" onclick="deleteJob(${job.id})">Delete</button>
            </div>
        </div>
    `).join('');
}

// Upload Resume
document.getElementById('upload-resume-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('file', document.getElementById('resume-file').files[0]);
    formData.append('name', document.getElementById('resume-name').value || document.getElementById('resume-file').files[0].name);

    try {
        const res = await fetch(`${API_BASE}/api/resumes`, {
            method: 'POST',
            body: formData
        });
        const data = await res.json();

        if (data.success) {
            showMessage('Resume uploaded successfully!', 'success');
            closeModal('upload-resume-modal');
            document.getElementById('upload-resume-form').reset();
            loadResumes();
        } else {
            showMessage(data.error || 'Upload failed', 'error');
        }
    } catch (error) {
        showMessage('Error uploading resume', 'error');
    }
});

// Add Job
document.getElementById('add-job-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {
        title: document.getElementById('job-title').value,
        company: document.getElementById('job-company').value,
        content: document.getElementById('job-content').value,
        source_url: document.getElementById('job-url').value || null
    };

    try {
        const res = await fetch(`${API_BASE}/api/jobs`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const result = await res.json();

        if (result.success) {
            showMessage('Job description added successfully!', 'success');
            closeModal('add-job-modal');
            document.getElementById('add-job-form').reset();
            loadJobs();
        } else {
            showMessage(result.error || 'Failed to add job', 'error');
        }
    } catch (error) {
        showMessage('Error adding job', 'error');
    }
});

// Optimize Page
async function loadOptimizePage() {
    const [resumesRes, jobsRes] = await Promise.all([
        fetch(`${API_BASE}/api/resumes`),
        fetch(`${API_BASE}/api/jobs`)
    ]);

    const resumes = await resumesRes.json();
    const jobs = await jobsRes.json();

    const resumeSelect = document.getElementById('optimize-resume-select');
    const jobSelect = document.getElementById('optimize-job-select');

    resumeSelect.innerHTML = '<option value="">-- Select Resume --</option>' +
        (resumes.success ? resumes.resumes.map(r => 
            `<option value="${r.id}">${r.name}</option>`
        ).join('') : '');

    jobSelect.innerHTML = '<option value="">-- Select Job --</option>' +
        (jobs.success ? jobs.jobs.map(j => 
            `<option value="${j.id}">${j.title} - ${j.company || 'Unknown'}</option>`
        ).join('') : '');
}

document.getElementById('use-groq').addEventListener('change', (e) => {
    document.getElementById('groq-key-group').style.display = e.target.checked ? 'block' : 'none';
});

async function runOptimization() {
    const resumeId = document.getElementById('optimize-resume-select').value;
    const jobId = document.getElementById('optimize-job-select').value;
    const optType = document.getElementById('optimize-type').value;
    const useGroq = document.getElementById('use-groq').checked;
    const groqKey = document.getElementById('groq-api-key').value;

    if (!resumeId || !jobId) {
        showMessage('Please select both resume and job description', 'error');
        return;
    }

    const btn = document.getElementById('optimize-btn-text');
    const loader = document.getElementById('optimize-loader');
    const resultsDiv = document.getElementById('optimize-results');

    btn.style.display = 'none';
    loader.style.display = 'inline-block';
    resultsDiv.style.display = 'none';

    try {
        const res = await fetch(`${API_BASE}/api/optimize`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                resume_id: parseInt(resumeId),
                job_id: parseInt(jobId),
                optimization_type: optType,
                use_groq: useGroq,
                groq_api_key: groqKey || null
            })
        });

        const data = await res.json();

        if (data.success) {
            displayOptimizationResults(data);
            resultsDiv.style.display = 'block';
            showMessage('Optimization complete!', 'success');
            loadHistory();
            loadDashboard();
        } else {
            showMessage(data.error || 'Optimization failed', 'error');
        }
    } catch (error) {
        showMessage('Error during optimization', 'error');
    } finally {
        btn.style.display = 'inline';
        loader.style.display = 'none';
    }
}

function displayOptimizationResults(data) {
    const container = document.getElementById('optimize-results');
    const analysis = data.analysis || {};
    const quality = analysis.resume_quality || {};
    const match = analysis.job_match || {};

    container.innerHTML = `
        <div class="optimization-result">
            <h2>Optimization Results</h2>
            <div class="result-scores">
                <div class="result-score">
                    <h4>Quality Score</h4>
                    <div class="result-score-value">${quality.quality_score || 'N/A'}/100</div>
                </div>
                <div class="result-score">
                    <h4>Match Score</h4>
                    <div class="result-score-value">${match.score ? match.score.toFixed(1) : 'N/A'}%</div>
                </div>
            </div>
            ${data.optimized_resume ? `
                <h3>Optimized Resume</h3>
                <div class="optimized-resume-content">${escapeHtml(data.optimized_resume)}</div>
                <button class="btn-primary" onclick="downloadText('${escapeHtml(data.optimized_resume)}', 'optimized_resume.txt')" style="margin-top: 15px;">Download</button>
            ` : ''}
            ${analysis.suggestions && analysis.suggestions.length > 0 ? `
                <h3>Suggestions</h3>
                <ul>
                    ${analysis.suggestions.map(s => `<li>${escapeHtml(s)}</li>`).join('')}
                </ul>
            ` : ''}
        </div>
    `;
}

// History
async function loadHistory() {
    try {
        const res = await fetch(`${API_BASE}/api/optimizations`);
        const data = await res.json();

        if (data.success) {
            displayHistory(data.optimizations);
        }
    } catch (error) {
        showMessage('Error loading history', 'error');
    }
}

function displayHistory(optimizations) {
    const container = document.getElementById('history-list');
    if (optimizations.length === 0) {
        container.innerHTML = '<p>No optimization history yet.</p>';
        return;
    }

    container.innerHTML = optimizations.map(opt => `
        <div class="item-card">
            <div class="item-info">
                <h3>Optimization #${opt.id}</h3>
                <p>Type: ${opt.optimization_type} | Provider: ${opt.api_provider}</p>
                <p>Match: ${opt.match_score || 'N/A'}% | Quality: ${opt.quality_score || 'N/A'}/100</p>
                <p><small>${new Date(opt.created_at).toLocaleString()}</small></p>
            </div>
            <div class="item-actions">
                <button class="btn-secondary" onclick="viewOptimization(${opt.id})">View</button>
                <button class="btn-danger" onclick="deleteOptimization(${opt.id})">Delete</button>
            </div>
        </div>
    `).join('');
}

// View functions
async function viewResume(id) {
    const res = await fetch(`${API_BASE}/api/resumes/${id}`);
    const data = await res.json();
    if (data.success) {
        showModal('view-item-modal', `
            <h2>${data.resume.name}</h2>
            <p><strong>File:</strong> ${data.resume.filename}</p>
            <p><strong>Words:</strong> ${data.resume.word_count}</p>
            <h3>Content</h3>
            <div class="optimized-resume-content">${escapeHtml(data.resume.content)}</div>
        `);
    }
}

async function viewJob(id) {
    const res = await fetch(`${API_BASE}/api/jobs/${id}`);
    const data = await res.json();
    if (data.success) {
        showModal('view-item-modal', `
            <h2>${data.job.title}</h2>
            <p><strong>Company:</strong> ${data.job.company || 'Not specified'}</p>
            <h3>Description</h3>
            <div class="optimized-resume-content">${escapeHtml(data.job.content)}</div>
        `);
    }
}

async function viewOptimization(id) {
    const res = await fetch(`${API_BASE}/api/optimizations/${id}`);
    const data = await res.json();
    if (data.success) {
        const opt = data.optimization;
        showModal('view-item-modal', `
            <h2>Optimization #${opt.id}</h2>
            <p><strong>Type:</strong> ${opt.optimization_type} | <strong>Provider:</strong> ${opt.api_provider}</p>
            <p><strong>Match Score:</strong> ${opt.match_score || 'N/A'}% | <strong>Quality:</strong> ${opt.quality_score || 'N/A'}/100</p>
            ${opt.optimized_resume ? `
                <h3>Optimized Resume</h3>
                <div class="optimized-resume-content">${escapeHtml(opt.optimized_resume)}</div>
            ` : ''}
            ${opt.suggestions && opt.suggestions.length > 0 ? `
                <h3>Suggestions</h3>
                <ul>${opt.suggestions.map(s => `<li>${escapeHtml(s)}</li>`).join('')}</ul>
            ` : ''}
        `);
    }
}

// Delete functions
async function deleteResume(id) {
    if (!confirm('Are you sure you want to delete this resume?')) return;
    const res = await fetch(`${API_BASE}/api/resumes/${id}`, { method: 'DELETE' });
    const data = await res.json();
    if (data.success) {
        showMessage('Resume deleted', 'success');
        loadResumes();
    }
}

async function deleteJob(id) {
    if (!confirm('Are you sure you want to delete this job description?')) return;
    const res = await fetch(`${API_BASE}/api/jobs/${id}`, { method: 'DELETE' });
    const data = await res.json();
    if (data.success) {
        showMessage('Job description deleted', 'success');
        loadJobs();
    }
}

async function deleteOptimization(id) {
    if (!confirm('Are you sure you want to delete this optimization?')) return;
    const res = await fetch(`${API_BASE}/api/optimizations/${id}`, { method: 'DELETE' });
    const data = await res.json();
    if (data.success) {
        showMessage('Optimization deleted', 'success');
        loadHistory();
    }
}

// Modal functions
function showModal(modalId, content) {
    document.getElementById('view-item-content').innerHTML = content;
    document.getElementById(modalId).classList.add('active');
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
}

function showUploadResumeModal() {
    document.getElementById('upload-resume-modal').classList.add('active');
}

function showAddJobModal() {
    document.getElementById('add-job-modal').classList.add('active');
}

// Utility functions
function showMessage(text, type) {
    const msg = document.getElementById('message');
    msg.textContent = text;
    msg.className = `message ${type}`;
    msg.style.display = 'block';
    setTimeout(() => {
        msg.style.display = 'none';
    }, 5000);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function downloadText(text, filename) {
    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
}

// Close modals on outside click
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.classList.remove('active');
    }
}

// Initialize
loadDashboard();

