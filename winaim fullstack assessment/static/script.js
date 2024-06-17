document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('employeeForm')) {
        document.getElementById('employeeForm').onsubmit = async function(event) {
            event.preventDefault();
            const formData = new FormData(event.target);
            const data = {};
            formData.forEach((value, key) => data[key] = value);
            const response = await fetch('/employees', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify(data)
            });
            const result = await response.json();
            alert(result.message);
            loadEmployees();
        };
    }

    if (document.getElementById('loginForm')) {
        document.getElementById('loginForm').onsubmit = async function(event) {
            event.preventDefault();
            const formData = new FormData(event.target);
            const data = {};
            formData.forEach((value, key) => data[key] = value);
            const response = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            const result = await response.json();
            if (result.access_token) {
                localStorage.setItem('token', result.access_token);
                window.location.href = '/';
            } else {
                alert(result.message);
            }
        };
    }

    if (document.getElementById('registerForm')) {
        document.getElementById('registerForm').onsubmit = async function(event) {
            event.preventDefault();
            const formData = new FormData(event.target);
            const data = {};
            formData.forEach((value, key) => data[key] = value);
            const response = await fetch('/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            const result = await response.json();
            alert(result.message);
            if (response.status === 201) {
                window.location.href = '/login';
            }
        };
    }

    async function loadEmployees() {
        const response = await fetch('/employees', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        const employees = await response.json();
        const employeeDiv = document.getElementById('employees');
        employeeDiv.innerHTML = '';
        employees.forEach(employee => {
            const employeeElement = document.createElement('div');
            employeeElement.textContent = `${employee.first_name} ${employee.last_name} (${employee.email})`;
            employeeDiv.appendChild(employeeElement);
        });
    }

    if (localStorage.getItem('token') && window.location.pathname === '/') {
        loadEmployees();
    }
});
