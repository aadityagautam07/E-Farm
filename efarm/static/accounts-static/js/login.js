const login = document.getElementById('login-form');
const username = document.getElementById('username');
// const form = document.querySelector('.form');
// const username = document.querySelector('.username');
const pass_field = document.querySelector('.pass-key');


login.addEventListener('submit', e => {
    var validUserName = validateUserName();
    var validPassword = validatePassword();


    if (validUserName == true && validPassword == true) {
        $(this).submit();
    } else {
        e.preventDefault();
    }
});


const setError = (element, message) => {
    const inputControl = element.parentElement;
    const errorDisplay = inputControl.querySelector('.error');

    errorDisplay.innerText = message;
    inputControl.classList.add('error');
    inputControl.classList.remove('success');

}

setSuccess = element => {
    const inputControl = element.parentElement;
    const errorDisplay = inputControl.querySelector('.error');

    errorDisplay.innerText = '';
    inputControl.classList.add('success');
    inputControl.classList.remove('error');
};


// alert(usernameValue.value);
const validateUserName = () => {
    const usernameValue = username.value;
    if (usernameValue === '') {
        setError(username, "Username is required");
        return false;
    } else {
        setSuccess(username);
        return true;
    }
}



const validatePassword = () => {
    const passwordValue = pass_field.value;
    console.log("Password: ", passwordValue);
    if (passwordValue === '') {
        setError(pass_field, "Password is required");
        return false;
    } else if (passwordValue.length < 8) {
        setError(pass_field, "Password must be at least 8 character");
        return false;
    } else {
        setSuccess(pass_field);
        return true;
    }
}
