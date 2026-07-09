// ===========================
// GYMIFY - JavaScript File
// Simple & Minimal JS
// ===========================

// --- LOGIN ROLE TABS ---
// Used on login.html to switch between Admin, Trainer, Member tabs
function switchTab(role) {
    // Remove active from all tabs
    var tabs = document.querySelectorAll('.role-tab');
    tabs.forEach(function(tab) {
        tab.classList.remove('active');
    });

    // Add active to clicked tab
    var clicked = document.getElementById('tab-' + role);
    if (clicked) clicked.classList.add('active');

    // Update hidden role input
    var roleInput = document.getElementById('role-input');
    if (roleInput) roleInput.value = role;

    // Change form title
    var title = document.getElementById('form-title');
    if (title) {
        if (role === 'admin') title.textContent = 'Admin Login';
        if (role === 'trainer') title.textContent = 'Trainer Login';
        if (role === 'member') title.textContent = 'Member Login';
    }
}

// --- LOGIN REDIRECT ---
// Redirects to correct dashboard based on role
function handleLogin() {
    var role = document.getElementById('role-input').value;
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;

    if (!email || !password) {
        alert('Please enter email and password.');
        return;
    }

    // Simple redirect based on role (no real backend here)
    if (role === 'admin') {
        window.location.href = 'admin-dashboard.html';
    } else if (role === 'trainer') {
        window.location.href = 'trainer-dashboard.html';
    } else if (role === 'member') {
        window.location.href = 'member-dashboard.html';
    } else {
        alert('Please select a role (Admin, Trainer, or Member).');
    }
}

// --- LOGOUT ---
function logout() {
    window.location.href = 'index.html';
}

// --- CART SYSTEM (Store Page) ---
var cart = [];

function addToCart(name, price) {
    // Check if item already in cart
    var found = false;
    for (var i = 0; i < cart.length; i++) {
        if (cart[i].name === name) {
            cart[i].qty += 1;
            found = true;
            break;
        }
    }
    if (!found) {
        cart.push({ name: name, price: price, qty: 1 });
    }
    updateCartDisplay();
    alert(name + ' added to cart!');
}

function updateCartDisplay() {
    var total = 0;
    var count = 0;
    cart.forEach(function(item) {
        total += item.price * item.qty;
        count += item.qty;
    });

    // Update cart count in bar
    var countEl = document.getElementById('cart-count');
    if (countEl) countEl.textContent = count;

    var totalEl = document.getElementById('cart-total-bar');
    if (totalEl) totalEl.textContent = 'PKR ' + total.toLocaleString();
}

function openCart() {
    var modal = document.getElementById('cart-modal');
    if (!modal) return;
    modal.style.display = 'block';

    var list = document.getElementById('cart-items');
    var totalEl = document.getElementById('cart-grand-total');
    if (!list) return;

    list.innerHTML = '';
    var total = 0;

    if (cart.length === 0) {
        list.innerHTML = '<p style="color:#858685;font-size:14px;">Your cart is empty.</p>';
    } else {
        cart.forEach(function(item) {
            var div = document.createElement('div');
            div.className = 'cart-item';
            div.innerHTML = '<span class="cart-item-name">' + item.name + ' x' + item.qty + '</span>' +
                            '<span class="cart-item-price">PKR ' + (item.price * item.qty).toLocaleString() + '</span>';
            list.appendChild(div);
            total += item.price * item.qty;
        });
    }

    if (totalEl) totalEl.textContent = 'Total: PKR ' + total.toLocaleString();
}

function closeCart() {
    var modal = document.getElementById('cart-modal');
    if (modal) modal.style.display = 'none';
}

function checkout() {
    var selected = document.querySelector('input[name="payment"]:checked');
    if (!selected) {
        alert('Please select a payment method.');
        return;
    }
    if (cart.length === 0) {
        alert('Your cart is empty!');
        return;
    }
    alert('Order placed successfully!\nPayment via: ' + selected.value + '\nThank you for shopping at GYMIFY!');
    cart = [];
    updateCartDisplay();
    closeCart();
}

// --- CONTACT FORM SUBMIT ---
function submitContact() {
    var name = document.getElementById('contact-name').value;
    var email = document.getElementById('contact-email').value;
    var message = document.getElementById('contact-message').value;

    if (!name || !email || !message) {
        alert('Please fill all fields.');
        return;
    }
    alert('Message sent! We will get back to you soon.');
    document.getElementById('contact-name').value = '';
    document.getElementById('contact-email').value = '';
    document.getElementById('contact-message').value = '';
}

// --- REGISTER FORM ---
function handleRegister() {
    var name = document.getElementById('reg-name').value;
    var email = document.getElementById('reg-email').value;
    var phone = document.getElementById('reg-phone').value;
    var password = document.getElementById('reg-password').value;

    if (!name || !email || !phone || !password) {
        alert('Please fill all fields.');
        return;
    }
    alert('Registration successful! You can now login.');
    window.location.href = 'login.html';
}

// --- ADMIN: Save Member ---
function saveMember() {
    var name = document.getElementById('m-name').value;
    if (!name) { alert('Please enter member name.'); return; }
    alert('Member saved successfully!');
}
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
// --- ADMIN: Save Trainer ---
function saveTrainer() {
    var name = document.getElementById('t-name').value;
    if (!name) { alert('Please enter trainer name.'); return; }
    alert('Trainer saved successfully!');
}

// --- TRAINER: Mark Attendance ---
function markAttendance() {
    var member = document.getElementById('att-member').value;
    var status = document.getElementById('att-status').value;
    if (!member) { alert('Please select a member.'); return; }
    alert('Attendance marked: ' + member + ' - ' + status);
}

// --- MEMBER: Update Profile ---
function updateProfile() {
    alert('Profile updated successfully!');
}
// --- PAYMENT METHOD SWITCH ---
var paymentSelect = document.getElementById('payment-method');
if (paymentSelect) {
    paymentSelect.addEventListener('change', function() {
        var method = this.value;
        var epBox  = document.getElementById('easypaisa-box');
        var jcBox  = document.getElementById('jazzcash-box');
        if (method === 'easypaisa') {
            epBox.style.display = 'block';
            jcBox.style.display = 'none';
        } else {
            epBox.style.display = 'none';
            jcBox.style.display = 'block';
        }
    });
}
// --- PAYMENT PROCESSING ---
function processPayment(event) {
    event.preventDefault();
    event.stopPropagation();

    var overlay = document.getElementById('payment-overlay');
    var form    = document.getElementById('checkout-form');

    if (!overlay || !form) {
        console.log('Elements not found');
        return;
    }

    // Reset screens
    document.getElementById('processing-screen').style.display = 'block';
    document.getElementById('success-screen').style.display   = 'none';

    // Overlay show karo
    overlay.style.display = 'flex';

    // 3 second baad success
    setTimeout(function() {
        document.getElementById('processing-screen').style.display = 'none';
        document.getElementById('success-screen').style.display    = 'block';

        // 2 second baad submit
        setTimeout(function() {
            overlay.style.display = 'none';
            form.onsubmit = null;
            form.submit();
        }, 2000);

    }, 3000);
}