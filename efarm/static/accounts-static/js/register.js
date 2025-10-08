const register = document.getElementById('register-form');
const username = document.getElementById('username');
const lname = document.getElementById('lname');
const fname = document.getElementById('fname');
const email = document.getElementById('email');
// const form = document.querySelector('.form');
// const username = document.querySelector('.username');
const pass_field = document.querySelector('.pass-key');
const conf_pass_field = document.querySelector('.confirm-pass-key');




register.addEventListener('submit', e => {

    
    
    var validPassword = passwordValidate();

    

    var validateConfPassword = confPassValidate();

    var validateFname = fnameValidate();
    // alert(validateFname)

    var validateLname = lnameValidate();
    
    var validateEmail = emailValidate();

    var validUserName1 = validateUserName1();
    // alert(validUserName1)


    // alert(validUserName);
    // console.log(validateConfPassword);
    // console.log(validateFname);
    // console.log(validateLname);
    // console.log(validateEmail);

    if (validUserName1 == true && validPassword == true && validateFname == true && validateEmail == true && validateLname == true && validateConfPassword == true) {
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

const isValidEmail = email => {
    const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}


// alert(usernameValue.value);
const validateUserName1 = () => {
    const usernameValue = username.value;
    // alert(usernameValue);
    if (usernameValue === '') {
        setError(username, "Username is required");
        return false;
    } else {
        setSuccess(username);
        return true;
    }
}


const passwordValidate = () => {
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

const fnameValidate = () => {
    const fnameValue = fname.value;

    if (fnameValue === '') {
        setError(fname, "First Name is required");
        return false;
    } else {
        setSuccess(fname);
        return true;
    }
}

const lnameValidate = () => {
    const lnameValue = lname.value;
    console.log(lnameValue);


    if (lnameValue === '') {
        setError(lname, "Last Name is required");
        return false;
    } else {
        setSuccess(lname);
        return true;
    }
}

const emailValidate = () => {
    const emailValue = email.value;



    if (emailValue === '') {
        setError(email, 'Email is required');
        return false;
    } else if (!isValidEmail(emailValue)) {
        setError(email, 'Provide a valid email address');
        return false;
    } else {
        setSuccess(email);
        return true;
    }
}


const confPassValidate = () => {
    const password2Value = conf_pass_field.value;
    const passwordValue = pass_field.value;
    console.log(password2Value);


    if (password2Value === '') {
        setError(conf_pass_field, 'Please confirm your password');
        return false;
    } else if (password2Value != passwordValue) {
        setError(conf_pass_field, "Passwords doesn't match");
        return false;
    } else {
        setSuccess(conf_pass_field);
        return true;
    }
}