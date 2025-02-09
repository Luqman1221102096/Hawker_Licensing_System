function updateDiv(button) {
    const buttonId = button.id
    fetch(`/get-content/?my_variable=${encodeURIComponent(buttonId)}`)
        .then(response => response.text())  // Use .text() to handle HTML
        .then(data => {
            document.getElementById('login').innerHTML = data;
        })
        .catch(error => console.error('Error:', error));
}
function login(event, form) {
    event.preventDefault();  // Prevent form from reloading the page

    let formData = new FormData(form);

    fetch(form.action, {  // Use the form action URL
        method: "POST",
        body: formData,
    })
    .then(response => response.text())  
    .then(data => {
        if (data.includes("success")) { 
            window.location.href = "/dashBoard/";  // Redirect if login is successful
        } else {
            document.getElementById("loginResponse").innerHTML = 
                `<span style="color: red;">${data}</span>`;
        }
    })
    .catch(error => console.error("Error:", error));
}
function register(event, form) {
    event.preventDefault();  // Prevent form from reloading the page

    let formData = new FormData(form);

    fetch(form.action, {  // Use the form action URL
        method: "POST",
        body: formData,
    })
    .then(response => response.text())  
    .then(data => {
        if (data.includes("success")) { 
            window.location.href = "/dashBoard/";  // Redirect if login is successful
        } else {
            document.getElementById("registerResponse").innerHTML = 
                `<span style="color: red;">${data}</span>`;
        }
    })
    .catch(error => console.error("Error:", error));
}  
function report(event, form) {
    alert("Script called");
    event.preventDefault();  // Prevent form from reloading the page

    let formData = new FormData(form);

    fetch(form.action, {  // Use the form action URL
        method: "POST",
        body: formData,
    })
    .then(response => response.text())  
    .then(data => {
        if (data.includes("success")) { 
            document.getElementById("uploadResponse").innerHTML = 
                `<span style="color: green;">Successful upload</span>`;
        } else {
            document.getElementById("uploadResponse").innerHTML = 
                `<span style="color: red;">Failed Upload</span>`;
        }
    })
    .catch(error => console.error("Error:", error));
} 