import { useState, useEffect } from "react";
// import { url } from "../../../config/config";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import {Link} from 'react-router-dom'
import { useDispatch } from "react-redux";
import { authActions } from "../store/store";
function Signup() {
  const navigate = useNavigate();
  const [password, setPassword] = useState("");
  const [passwordPassed, setPasswordPassed] = useState(0);
  const [firstName, setFirstName] = useState("");
  const [secondName, setSecondName] = useState("");
  const [email, setEmail] = useState("");
  const [phoneNumber, setPhoneNumber] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");

  const dispatch = useDispatch()

  function isGood(password) {
    const regex = ["[A-Z]", "[a-z]", "[0-9]", "[$@$!%*#?&]"];
    let passed = 0;
    for (let i = 0; i < regex.length; i++) {
      if (new RegExp(regex[i]).test(password)) {
        passed++;
      }
    }

    switch (passed) {
      case 0:
      case 1:
      case 2:
        setPasswordPassed(2);
        break;
      case 3:
        setPasswordPassed(3);
        break;
      case 4:
        setPasswordPassed(4);
        break;
    }
    if (passed <= 2) return false;
    return true;
  }

  const handlePasswordChange = (e) => {
    const newPassword = e.target.value;
    console.log("newPassword", newPassword);
    setPassword(newPassword); // Вне зависимости от условий, обновляем пароль

    if (isGood(newPassword)) {
      // Если пароль соответствует условиям сложности, продолжаем
      if (newPassword !== confirmPassword) {
        document
          .getElementById("confirmPassword")
          .setCustomValidity("Пароли не совпадают");
      } else {
        document.getElementById("confirmPassword").setCustomValidity("");
      }
    }
  };
  const handleConfirmPasswordChange = (e) => {
    const newConfirmPassword = e.target.value;
    setConfirmPassword(newConfirmPassword);

    if (password !== newConfirmPassword) {
      document
        .getElementById("confirmPassword")
        .setCustomValidity("Пароли не совпадают");
    } else {
      document.getElementById("confirmPassword").setCustomValidity("");
    }
  };

  useEffect(() => {
    if (password == "") setPasswordPassed(0);
  }, [password]);
  /* eslint-diable */

  const authHandler = () => {
    dispatch(authActions.login())
  }
  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("email", email);
    console.log("password", password);
    console.log("firstName", firstName);
    console.log("secondName", secondName);

    const authData = {
      email: email,
      password: password,
      first_name: firstName,
      last_name: secondName,
      phonenumber: phoneNumber
    }

    async function makeRequest() {
      return axios.post('http://127.0.0.1/api/register-owner', authData)
      .then((response) => {
        const token = response.data.access;
        localStorage.setItem('token', token);
        axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
        navigate("/panel");
      })
      .catch((error) => {
        setError('Such email already exists');
        console.error("Error. Please contact administrator");
      });
    }

    if (password !== "" && confirmPassword !== "" && passwordPassed >= 3) {
      const data = makeRequest();
      authHandler()
      console.log(data);
    }

  };

  return (
    <>
      <section className="bg-gray-50 h-screen flex-1 text-left" id="body">
        <div className="mx-auto flex flex-col items-center justify-center px-6 py-8 md:h-screen lg:py-0">
          <a
            href="#"
            className="mb-6 flex items-center text-2xl font-semibold text-gray-900"
          >
            <img
              className="mr-2 h-8 w-8 rounded-2xl bg-black"
              src="https://pngfre.com/wp-content/uploads/egg-png-image-pngfre-24-300x278.png"
              alt="logo"
            />
            Brunch
          </a>
          <div className="w-full rounded-lg bg-white shadow sm:max-w-md md:mt-0 xl:p-0">
            <div className="space-y-4 p-6 sm:p-8 md:space-y-6">
              <h1 className="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl">
                Sign up your own
                <span className="rounded bg-black mx-2 px-1 text-xl font-bold text-white">
                  Brunch
                </span>
                account
              </h1>
              <form className="space-y-4 md:space-y-6" action="#">
                <div className="flex gap-8">
                  <div className="flex flex-col gap-4">
                    <div>
                      <label className="mb-2 block text-sm font-medium text-gray-900">
                        Your First name
                      </label>
                      <input
                        type="text"
                        name="firstName"
                        id="firstName"
                        className="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-gray-900 sm:text-sm"
                        placeholder="John"
                        value={firstName}
                        onChange={(e) => {
                          setFirstName(e.target.value);
                        }}
                        required
                      />
                    </div>
                    <div>
                      <label className="mb-2 block text-sm font-medium text-gray-900">
                        Your Second name
                      </label>
                      <input
                        type="text"
                        name="secondName"
                        id="secondName"
                        className="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-gray-900 sm:text-sm"
                        placeholder="Wick"
                        value={secondName}
                        onChange={(e) => {
                          setSecondName(e.target.value);
                        }}
                        required
                      />
                    </div>
                    <div>
                      <label className="mb-2 block text-sm font-medium text-gray-900">
                        Your email
                      </label>
                      <input
                        type="email"
                        name="email"
                        id="email"
                        className="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-gray-900 sm:text-sm"
                        placeholder="name@company.com"
                        value={email}
                        onChange={(e) => {
                          setEmail(e.target.value);
                        }}
                        required
                      />
                    </div>
                  </div>
                  <div className="flex flex-col gap-4">
                    <div>
                      <label className="mb-2 block text-sm font-medium text-gray-900">
                        Phone number
                      </label>
                      <input
                        type="phone"
                        name="phoneNumber"
                        id="phoneNumber"
                        className="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-gray-900 sm:text-sm"
                        placeholder="+7 777 777 77 77"
                        required
                        value={phoneNumber}
                        onChange={(e) => {
                          setPhoneNumber(e.target.value);
                        }}
                      />
                    </div>
                    <div className="relative w-full">
                      <label className="mb-2 block text-sm font-medium text-gray-900">
                        Password
                      </label>
                      <input
                        type="password"
                        name="password"
                        id="password"
                        placeholder="••••••••"
                        className="focus:ring-primary-600 focus:border-primary-600 block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-gray-900 sm:text-sm"
                        required
                        onChange={handlePasswordChange}
                        value={password}
                      />
                      {passwordPassed <= 2 && password !== "" && (
                        <small
                          className="absolute text-xs text-right w-full text-red-600 mt-1 font-bold"
                          // style={{ fontWeight: "bold" }}
                        >
                          Weak
                        </small>
                      )}
                      {passwordPassed === 3 && password !== "" && (
                        <small className="absolute text-xs text-right w-full text-blue-600 mt-1 font-bold">
                          Medium
                        </small>
                      )}
                      {passwordPassed === 4 && password !== "" && (
                        <small className="absolute text-xs text-right w-full text-green-600 mt-1 font-bold">
                          Strong
                        </small>
                      )}
                    </div>

                    <div>
                      <label
                        htmlFor="password"
                        className="mb-2 block text-sm font-medium text-gray-900"
                      >
                        Confirm password
                      </label>
                      <input
                        type="password"
                        name="confirmPassword"
                        id="confirmPassword"
                        placeholder="••••••••"
                        className="focus:ring-primary-600 focus:border-primary-600 block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-gray-900 sm:text-sm"
                        required
                        onChange={handleConfirmPasswordChange}
                        value={confirmPassword}
                      />
                    </div>
                  </div>
                </div>
                {error && <p className="text-[red] text-center">{error}!</p>}
                <button
                  type="submit"
                  className="dark:hover:bg-primary-700 w-full rounded-lg bg-gray-900 px-5 py-2.5 text-center text-sm font-medium text-white hover:bg-gray-700 focus:outline-none focus:ring-4 focus:ring-gray-300"
                  onClick={handleSubmit}
                >
                  {console.log("passwordPassed", passwordPassed)}
                  Sign up
                </button>

                <p className="text-sm font-light text-right text-gray-500">
                  Already have an account? <br />
                  <Link
                    to="/login"
                    className="text-primary-600 font-medium hover:underline"
                  >
                    Log In
                  </Link>
                </p>
              </form>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}

export default Signup;
