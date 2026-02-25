console.log("JS LOADED");




// Получаем CSRF токен
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Функция для получения уведомлений
async function fetchNotifications() {
    try {
        const response = await fetch("/forum/notifications/unread/");
        if (!response.ok) throw new Error("Network response was not OK");

        const data = await response.json();
        const container = document.getElementById("notification-container");
        if (!container) return;

        container.innerHTML = "";

        if (data.notifications && data.notifications.length > 0) {
            data.notifications.forEach(notification => {

                const li = document.createElement("li");


                const title = document.createElement("strong");
                title.textContent = notification.title;


                const text = document.createElement("span");
                text.textContent =  $notification.text ;


                const date = document.createElement("small");
                date.textContent = $notification.date ;

                li.append(title, text, date, btn);
                container.appendChild(li);
            });
        } else {
            const li = document.createElement("li");
            li.textContent = "No unread notifications.";
            container.appendChild(li);
        }
    } catch (err) {
        console.error("fetchNotifications error:", err);
    }
}



document.addEventListener('click', function(e) {
    if (e.target && e.target.classList.contains('btn-close')) {
        const id = e.target.dataset.id;
        markAsRead(id);
    }
});

function markAsRead(notificationId) {
    fetch(`/forum/notifications/read/${notificationId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        },
    })
    .then(resp => resp.json())
    .then(data => {
        if (data.success) {
            const el = document.getElementById(`notification-${notificationId}`);
            if (el) {
                const alert = bootstrap.Alert.getOrCreateInstance(el);
                alert.close(); // Bootstrap анімація
            }
        } else {
            console.error("Failed to mark as read:", data.error);
        }
    })
    .catch(err => console.error(err));
}


document.addEventListener("DOMContentLoaded", function() {

    document.querySelectorAll("button[data-decision]").forEach(btn => {
        btn.addEventListener("click", function() {
            const requestId = this.dataset.id;
            const decision = this.dataset.decision;

            fetch(`/forum/review-dashboard/review-action/${requestId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie('csrftoken'),
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ decision: decision })
            })
            .then(response => response.json())
            .then(data => {

                document.getElementById(`status-${requestId}`).innerText = data.new_status;
            })
            .catch(err => console.error(err));
        });
    });
});
