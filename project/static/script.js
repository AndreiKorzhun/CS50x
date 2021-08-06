function passwordVisibility() {
    /* Shows or hides the values in the password input in LogIn and Registration */

    let p = document.getElementById("inputPassword");
    if (p.type === "password") {
        p.type = "text";
        document.getElementById("password-visibility-toggle").innerHTML="hide";
    } else {
        p.type = "password";
        document.getElementById("password-visibility-toggle").innerHTML="show";
    }
}


function messageLengthError(input, error, num = 40) {
    /* Display a message when exceeding the text in the input field */

    let str = "The Input " + (document.getElementById(input).name) + " must contain no more than " + num + " characters.";
    document.getElementById(error).innerHTML = str;
}


function checkLoginRegistrationForm() {
    /* Check the length of the input value in Login or Registration Form */

    const form = document.getElementById("personal_info");

    // Permission to submit the form
    let flag = false;

    // When open Registration Form
    if (document.getElementById("inputName")) {

        // Check the values input in Name
        document.getElementById("inputName").onkeyup = function () {
            // Name length
            let name_length = document.getElementById("inputName").value.length;

            if (name_length > 40) {
                // Error message output
                messageLengthError("inputName", "name_value_error");
                flag = false;
            }
            else {
                // Hide error message
                document.getElementById("name_value_error").innerHTML = "";
                flag = true;
            }
        };
    }

    // Check the values input in Password
    document.getElementById("inputPassword").onkeyup = function () {
        // Password length
        let password_length = document.getElementById("inputPassword").value.length;

        // Check Password length
        if (password_length < 6) {
            let str = "The password you provided must have at least 6 characters.";
            document.getElementById("password_value_error").innerHTML = str;

            flag = false;
        }
        else if (password_length > 40) {
            // Error message output
            messageLengthError("inputPassword", "password_value_error");
            flag = false;
        }
        else {
            // Hide error message
            document.getElementById("password_value_error").innerHTML = "";
            flag = true;
        }
    };

    // Submit button pressed
    form.addEventListener('submit', function (evt) {
        // Stop submitting the form
        evt.preventDefault();
        if (flag) {
            this.submit();
        }
    });
}


function checkAddTaskForm() {
    /* Check the length of the input value in Add Task Form */

    // Enable or disable submit button of Add Task Form
    document.getElementById("inputTask").onkeyup = function () {
        let task_value = document.getElementById("inputTask").value;
        let submit = document.getElementById("submitTask");

        if (task_value === "") {
            // Disabling the form submit button
            submit.disabled = true;
        }
        else {
            submit.disabled = false;
        }
        if (task_value.length > 100) {
            // Disabling the form submit button
            submit.disabled = true;
            // Error message output
            messageLengthError("inputTask", "name_value_error", 100);
        }
    };
}


document.addEventListener("DOMContentLoaded", function() {
    /* The event fires when the initial HTML document has been completely loaded and parsed */

    if (document.getElementById("personal_info")) {
        checkLoginRegistrationForm();
    }
    else if (document.getElementById("inputTask")) {
        checkAddTaskForm();
    }
});