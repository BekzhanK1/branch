import "./Login.css";
import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";
import axios from "axios";
import { url } from "../../../config/config";

function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);

  const handleLogin = (e) => {
    e.preventDefault();
    axios
      .post(`${url}/api/login`, {
        email: email,
        password: password,
      })
      .then((response) => {
        const token = response.data.access; // access and refresh tokens === jwt
        axios.defaults.headers.common["Authorization"] = `Bearer ${token}`; //bearer !== jwt bearer === another authorization method.
        navigate("/panel");
      })
      .catch((error) => {
        switch (error.response ? error.response.status : null) {
          case 400:
            console.error("Incorrect login or password");
            setError("Incorrect login or password");
            break;
          case 401:
            console.error("Unauthorized access");
            setError("Unauthorized access");
            break;
          default:
            if (error.request) {
              console.error(
                "Timeout. The server is unavailable. Please contact the administrator"
              );
              setError(
                "Timeout. The server is unavailable. Please contact the administrator"
              );
            } else {
              console.error("Authentication error:", error);
              setError("Authentication error");
            }
            break;
        }
      });
  };

  return (
    <>
      <section className="bg-gray-50 h-screen w-screen" id="body">
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
                Sign in to your account
              </h1>
              <form
                className="space-y-4 md:space-y-6 text-left"
                onSubmit={handleLogin}
              >
                <div>
                  <label className="mb-2 block text-sm font-medium text-gray-900">
                    Your email
                  </label>
                  <input
                    type="email"
                    name="email"
                    id="email"
                    className="focus:ring-primary-600 focus:border-primary-600 block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-gray-900 sm:text-sm"
                    placeholder="name@company.com"
                    required=""
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                  />
                </div>
                <div>
                  <label className="mb-2 block text-sm font-medium text-gray-900">
                    Password
                  </label>
                  <input
                    type="password"
                    name="password"
                    id="password"
                    placeholder="••••••••"
                    className="focus:ring-primary-600 focus:border-primary-600 block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-gray-900 sm:text-sm"
                    required=""
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                  />
                </div>
                <button
                  type="submit"
                  className="dark:hover:bg-primary-700 w-full rounded-lg bg-gray-900 px-5 py-2.5 text-center text-sm font-medium text-white hover:bg-gray-700 focus:outline-none focus:ring-4 focus:ring-gray-300"
                  onClick={handleLogin}
                >
                  Sign in
                </button>

                {error && <p className="text-red-500">{error}</p>}
                <p className="text-sm font-light text-right text-gray-500">
                  Don’t have an account yet? <br />
                  <Link
                    to="/signup"
                    className="text-primary-600 font-medium hover:underline"
                  >
                    Sign up
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

export default Login;
