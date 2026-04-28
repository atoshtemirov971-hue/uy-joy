// ═══ UY-JOY PLATFORM — MAIN JS ═══

// ═══ 1. TOAST XABARNOMALAR ═══
function showToast(message, type = 'success') {
    const toastContainer = document.getElementById('toastContainer');
    if (!toastContainer) {
        const div = document.createElement('div');
        div.id = 'toastContainer';
        div.style.cssText = 'position:fixed;top:20px;right:20px;z-index:9999;display:flex;flex-direction:column;gap:10px;';
        document.body.appendChild(div);
    }
    const colors = {
        success: '#10b981',
        danger: '#ef4444',
        info: '#2563eb',
        warning: '#f59e0b'
    };
    const icons = {
        success: 'fa-check-circle',
        danger: 'fa-times-circle',
        info: 'fa-info-circle',
        warning: 'fa-exclamation-circle'
    };
    const toast = document.createElement('div');
    toast.style.cssText = `
        background:white;
        border-left:4px solid ${colors[type]};
        border-radius:12px;
        padding:14px 20px;
        box-shadow:0 8px 30px rgba(0,0,0,0.12);
        display:flex;
        align-items:center;
        gap:12px;
        min-width:280px;
        animation:slideIn 0.3s ease;
        font-weight:500;
    `;
    toast.innerHTML = `
        <i class="fas ${icons[type]}" style="color:${colors[type]};font-size:1.1rem;"></i>
        <span>${message}</span>
        <button onclick="this.parentElement.remove()"
            style="margin-left:auto;background:none;border:none;cursor:pointer;color:#94a3b8;font-size:1.1rem;">
            <i class="fas fa-times"></i>
        </button>
    `;
    document.getElementById('toastContainer').appendChild(toast);
    setTimeout(() => toast.remove(), 4000);
}

// ═══ 2. LOADING SPINNER ═══
function showLoading(text = 'Yuklanmoqda...') {
    const overlay = document.createElement('div');
    overlay.id = 'loadingOverlay';
    overlay.style.cssText = `
        position:fixed;top:0;left:0;width:100%;height:100%;
        background:rgba(255,255,255,0.85);
        display:flex;flex-direction:column;
        align-items:center;justify-content:center;
        z-index:9999;backdrop-filter:blur(4px);
    `;
    overlay.innerHTML = `
        <div style="width:50px;height:50px;border:4px solid #e2e8f0;border-top-color:#2563eb;border-radius:50%;animation:spin 0.8s linear infinite;margin-bottom:16px;"></div>
        <p style="color:#2563eb;font-weight:600;">${text}</p>
    `;
    document.body.appendChild(overlay);
}

function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) overlay.remove();
}

// ═══ 3. DISTRICT FILTER ═══
document.addEventListener('DOMContentLoaded', function() {
    const regionSelect = document.getElementById('id_region');
    const districtSelect = document.getElementById('id_district');

    if (regionSelect && districtSelect) {
        regionSelect.addEventListener('change', function() {
            const regionId = this.value;
            if (!regionId) {
                districtSelect.innerHTML = '<option value="">Tuman tanlang</option>';
                return;
            }
            fetch(`/api/districts/?region=${regionId}`)
                .then(r => r.json())
                .then(data => {
                    districtSelect.innerHTML = '<option value="">Tuman tanlang</option>';
                    data.forEach(d => {
                        districtSelect.innerHTML += `<option value="${d.id}">${d.name}</option>`;
                    });
                })
                .catch(() => showToast('Tumanlar yuklanmadi', 'danger'));
        });
    }
});

// ═══ 4. RASM PREVIEW ═══
function previewImages(input) {
    const preview = document.getElementById('imagePreview');
    if (!preview) return;
    preview.innerHTML = '';
    Array.from(input.files).forEach((file, index) => {
        const reader = new FileReader();
        reader.onload = e => {
            const wrap = document.createElement('div');
            wrap.style.cssText = 'position:relative;display:inline-block;margin:4px;';
            wrap.innerHTML = `
                <img src="${e.target.result}"
                    style="width:100px;height:80px;object-fit:cover;border-radius:8px;border:2px solid #e2e8f0;">
                <button onclick="removeImage(this, ${index})"
                    style="position:absolute;top:-6px;right:-6px;background:#ef4444;color:white;border:none;border-radius:50%;width:20px;height:20px;font-size:0.65rem;cursor:pointer;display:flex;align-items:center;justify-content:center;">
                    <i class="fas fa-times"></i>
                </button>
            `;
            preview.appendChild(wrap);
        };
        reader.readAsDataURL(file);
    });
}

// ═══ 5. NARX FORMATLASH ═══
function formatPrice(input) {
    let value = input.value.replace(/\D/g, '');
    input.value = Number(value).toLocaleString('uz-UZ');
}

// ═══ 6. SAQLASH TUGMASI ═══
function toggleSave(listingId) {
    const token = localStorage.getItem('access_token');
    fetch(`/api/listings/${listingId}/save_listing/`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(r => r.json())
    .then(data => {
        const btn = document.getElementById(`saveBtn_${listingId}`);
        if (data.status === 'saved') {
            btn.innerHTML = '<i class="fas fa-heart me-1"></i>Saqlandi';
            btn.classList.remove('btn-outline-danger');
            btn.classList.add('btn-danger');
            showToast("E'lon saqlandi!", 'success');
        } else {
            btn.innerHTML = '<i class="far fa-heart me-1"></i>Saqlash';
            btn.classList.remove('btn-danger');
            btn.classList.add('btn-outline-danger');
            showToast("E'lon saqlanganlardan olib tashlandi", 'info');
        }
    })
    .catch(() => showToast('Xatolik yuz berdi', 'danger'));
}

// ═══ 7. CSRF TOKEN ═══
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        document.cookie.split(';').forEach(cookie => {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
            }
        });
    }
    return cookieValue;
}

// ═══ 8. PAROL KO'RSATISH ═══
function togglePassword(inputId, iconId) {
    const input = document.getElementById(inputId);
    const icon = document.getElementById(iconId);
    if (input.type === 'password') {
        input.type = 'text';
        icon.className = 'fas fa-eye-slash';
    } else {
        input.type = 'password';
        icon.className = 'fas fa-eye';
    }
}

// ═══ 9. SCROLL TO TOP ═══
window.addEventListener('scroll', function() {
    const btn = document.getElementById('scrollTopBtn');
    if (btn) {
        btn.style.display = window.scrollY > 400 ? 'flex' : 'none';
    }
});

function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ═══ 10. CSS ANIMATIONS ═══
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { opacity:0; transform:translateX(20px); }
        to { opacity:1; transform:translateX(0); }
    }
    @keyframes spin {
        to { transform:rotate(360deg); }
    }
    @keyframes fadeInUp {
        from { opacity:0; transform:translateY(20px); }
        to { opacity:1; transform:translateY(0); }
    }
    .card { animation: fadeInUp 0.4s ease forwards; }
`;
document.head.appendChild(style);

// ═══ 11. SCROLL TO TOP BUTTON ═══
document.addEventListener('DOMContentLoaded', function() {
    const btn = document.createElement('button');
    btn.id = 'scrollTopBtn';
    btn.onclick = scrollToTop;
    btn.style.cssText = `
        position:fixed;bottom:30px;right:30px;
        width:44px;height:44px;
        background:#2563eb;color:white;
        border:none;border-radius:50%;
        display:none;align-items:center;justify-content:center;
        cursor:pointer;z-index:999;
        box-shadow:0 4px 14px rgba(37,99,235,0.4);
        font-size:1rem;transition:transform 0.2s;
    `;
    btn.innerHTML = '<i class="fas fa-arrow-up"></i>';
    btn.onmouseenter = () => btn.style.transform = 'scale(1.1)';
    btn.onmouseleave = () => btn.style.transform = 'scale(1)';
    document.body.appendChild(btn);
});