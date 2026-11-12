function validateAverage() {
    const minAvgSelect = document.getElementById("vote_average.gte");
    const maxAvgSelect = document.getElementById("vote_average.lte");
    const submitBtn = document.getElementById("submitBtn");

    function validateRating() {
        const minAvg = parseInt(minAvgSelect.value) || 0;
        const maxAvg = parseInt(maxAvgSelect.value) || 10;

        if (minAvg > maxAvg) {
            maxAvgSelect.value = "";
            showToast(
                message="Минимальный рейтинг не может быть больше максимального",
                toastSelectorId="toastAvg"
            );
        }
    }

    function showToast(message, toastSelectorId) {
        const toast = document.getElementById(toastSelectorId);
        if (!toast) return;

        toast.textContent = message;
        toast.style.display = "block";

        setTimeout(() => {
            toast.style.display = "none";
        }, 3500);
    }

    submitBtn.addEventListener("click", function(event) {
        const minDateSelect = document.getElementById("primary_release_date.gte");
        const maxDateSelect = document.getElementById("primary_release_date.lte");
        const minDate = Date.parse(minDateSelect.value);
        const maxDate = Date.parse(maxDateSelect.value);

        if (minDate && maxDate && minDate > maxDate) {
            event.preventDefault();
            showToast(
                message="Минимальная дата не может быть больше максимальной",
                toastSelectorId="toastDate"
            );
            maxDateSelect.value = ""
        }
    });

    minAvgSelect.addEventListener("change", validateRating);
    maxAvgSelect.addEventListener("change", validateRating);
}

function resetForm() {
    const formElements = document.querySelector('form').querySelectorAll('input, select')
    function resetFields(formElements) {

        formElements.forEach(elem => {
            if (elem.tagName === "SELECT") {
                if (elem.multiple) {
                    elem.selectedIndex = -1;
                } else {
                    for (const option of elem.options) {
                        if (elem.name == "genre_types") {
                            console.log(option.value === "|")
                            option.selected = option.value === "|";
                        } else {
                            option.selected = option.value === null;
                        }
                    }
                }
            } else {
                elem.value = '';
            }
        });
    }
    const resetBtn = document.getElementById("resetBtn");

    resetBtn.addEventListener("click", function(event) {
        resetFields(formElements)
    });
}

function hideAlerts () {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
          const bsAlert = new bootstrap.Alert(alert);
          bsAlert.close();
        }, 5000);
    });
}

document.addEventListener("DOMContentLoaded", validateAverage);
document.addEventListener("DOMContentLoaded", resetForm);
document.addEventListener("DOMContentLoaded", hideAlerts);