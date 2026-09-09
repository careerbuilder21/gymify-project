// GYMIFY - JavaScript File

// --- LOGIN TAB SWITCH ---
function switchTab(role) {
    var tabs = document.querySelectorAll('.role-tab');
    tabs.forEach(function(tab) {
        tab.classList.remove('active');
    });
    var clicked = document.getElementById('tab-' + role);
    if (clicked) clicked.classList.add('active');
    var roleInput = document.getElementById('role-input');
    if (roleInput) roleInput.value = role;
    var title = document.getElementById('form-title');
    if (title) {
        if (role === 'admin')   title.textContent = 'Admin Login';
        if (role === 'trainer') title.textContent = 'Trainer Login';
        if (role === 'member')  title.textContent = 'Member Login';
    }
}

// --- CONTACT FORM ---
function submitContact() {
    var name    = document.getElementById('contact-name').value;
    var email   = document.getElementById('contact-email').value;
    var message = document.getElementById('contact-message').value;
    if (!name || !email || !message) {
        alert('Please fill all fields.');
        return;
    }
    alert('Message sent! We will get back to you soon.');
}

// --- PAYMENT PROCESSING ---
function processPayment(event) {
    event.preventDefault();
    event.stopPropagation();
    var overlay = document.getElementById('payment-overlay');
    var form    = document.getElementById('checkout-form');
    if (!overlay || !form) return;
    document.getElementById('processing-screen').style.display = 'block';
    document.getElementById('success-screen').style.display   = 'none';
    overlay.style.display = 'flex';
    setTimeout(function() {
        document.getElementById('processing-screen').style.display = 'none';
        document.getElementById('success-screen').style.display    = 'block';
        setTimeout(function() {
            overlay.style.display = 'none';
            form.onsubmit = null;
            form.submit();
        }, 2000);
    }, 3000);
}

// --- PASSWORD SHOW/HIDE (Login) ---
function togglePassword() {
    var field = document.getElementById('password-field');
    var icon  = document.getElementById('eye-icon');
    if (field.type === 'password') {
        field.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
        icon.style.color = '#E63946';
    } else {
        field.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
        icon.style.color = '#858685';
    }
}

// --- PASSWORD SHOW/HIDE (Register) ---
function toggleRegPassword() {
    var field = document.getElementById('reg-password-field');
    var icon  = document.getElementById('reg-eye-icon');
    if (field.type === 'password') {
        field.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
        icon.style.color = '#E63946';
    } else {
        field.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
        icon.style.color = '#858685';
    }
}

// --- EDIT MEMBER MODAL ---
function openEditModal(id, name, phone, age, weight, plan, trainerId) {
    document.getElementById('edit_member_id').value = id;
    document.getElementById('edit_name').value = name;
    document.getElementById('edit_phone').value = phone;
    document.getElementById('edit_age').value = age;
    document.getElementById('edit_weight').value = weight;

    var planSelect = document.getElementById('edit_plan');
    for (var i = 0; i < planSelect.options.length; i++) {
        if (planSelect.options[i].value === plan) {
            planSelect.selectedIndex = i;
            break;
        }
    }

    var trainerSelect = document.getElementById('edit_trainer');
    for (var j = 0; j < trainerSelect.options.length; j++) {
        if (trainerSelect.options[j].value === trainerId) {
            trainerSelect.selectedIndex = j;
            break;
        }
    }

    document.getElementById('editModal').style.display = 'block';
}

function closeEditModal() {
    document.getElementById('editModal').style.display = 'none';
}

// --- EDIT TRAINER MODAL ---
function openTrainerModal(id, name, phone, spec, salary, security) {
    document.getElementById('edit_trainer_id').value = id;
    document.getElementById('edit_trainer_name').value = name;
    document.getElementById('edit_trainer_phone').value = phone;
    document.getElementById('edit_trainer_security').value = security;
    document.getElementById('edit_trainer_salary').value = salary;

    var specSelect = document.getElementById('edit_trainer_spec');
    for (var i = 0; i < specSelect.options.length; i++) {
        if (specSelect.options[i].value === spec) {
            specSelect.selectedIndex = i;
            break;
        }
    }

    document.getElementById('trainerModal').style.display = 'block';
}

function closeTrainerModal() {
    document.getElementById('trainerModal').style.display = 'none';
}
// --- EDIT COURSE MODAL ---
function openCourseModal(id, title, trainerId, level, duration, desc) {
    document.getElementById('edit_course_id').value = id;
    document.getElementById('edit_course_title').value = title;
    document.getElementById('edit_course_duration').value = duration;
    document.getElementById('edit_course_desc').value = desc;

    var levelSelect = document.getElementById('edit_course_level');
    for (var i = 0; i < levelSelect.options.length; i++) {
        if (levelSelect.options[i].value === level) {
            levelSelect.selectedIndex = i;
            break;
        }
    }

    var trainerSelect = document.getElementById('edit_course_trainer');
    for (var j = 0; j < trainerSelect.options.length; j++) {
        if (trainerSelect.options[j].value === trainerId) {
            trainerSelect.selectedIndex = j;
            break;
        }
    }

    document.getElementById('courseModal').style.display = 'block';
}

function closeCourseModal() {
    document.getElementById('courseModal').style.display = 'none';
}

// --- EDIT PRODUCT MODAL ---
function openProductModal(id, name, category, price, stock, desc) {
    document.getElementById('edit_product_id').value = id;
    document.getElementById('edit_product_name').value = name;
    document.getElementById('edit_product_price').value = price;
    document.getElementById('edit_product_stock').value = stock;
    document.getElementById('edit_product_desc').value = desc;

    var catSelect = document.getElementById('edit_product_category');
    for (var i = 0; i < catSelect.options.length; i++) {
        if (catSelect.options[i].value === category) {
            catSelect.selectedIndex = i;
            break;
        }
    }

    document.getElementById('productModal').style.display = 'block';
}

function closeProductModal() {
    document.getElementById('productModal').style.display = 'none';
}