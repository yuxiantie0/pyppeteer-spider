// Cookie状态切换
function toggleCookieStatus(id) {
    fetch(`/cookie/toggle/${id}`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // 更新开关状态
                const checkbox = document.querySelector(`#cookie-toggle-${id}`);
                checkbox.checked = data.is_valid;
                
                // 更新状态标签
                const statusLabel = document.querySelector(`#cookie-status-${id}`);
                statusLabel.textContent = data.is_valid ? '有效' : '无效';
                statusLabel.className = data.is_valid ? 'badge bg-success' : 'badge bg-secondary';
            } else {
                alert('更新状态失败');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('操作失败');
        });
}

// 确认删除
function confirmDelete(type, id, name) {
    if (confirm(`确定要删除${type} "${name}" 吗？`)) {
        window.location.href = `/${type}/delete/${id}`;
    }
}

// 复制Cookie值
function copyToClipboard(text) {
    navigator.clipboard.writeText(text)
        .then(() => {
            alert('已复制到剪贴板');
        })
        .catch(err => {
            console.error('复制失败:', err);
            alert('复制失败');
        });
}

// 格式化JSON显示
function formatJson(json) {
    try {
        const obj = JSON.parse(json);
        return JSON.stringify(obj, null, 2);
    } catch (e) {
        return json;
    }
}

// 表单验证
function validateForm() {
    const requiredFields = document.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Cookie值JSON验证
function validateCookieJson(value) {
    try {
        JSON.parse(value);
        return true;
    } catch (e) {
        alert('Cookie值必须是有效的JSON格式');
        return false;
    }
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    // 初始化所有开关状态
    document.querySelectorAll('.cookie-toggle').forEach(toggle => {
        toggle.addEventListener('change', function() {
            toggleCookieStatus(this.dataset.id);
        });
    });
    
    // 初始化所有表单验证
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm()) {
                e.preventDefault();
            }
        });
    });
    
    // 初始化所有Cookie值输入验证
    document.querySelectorAll('.cookie-value').forEach(input => {
        input.addEventListener('change', function() {
            validateCookieJson(this.value);
        });
    });
}); 