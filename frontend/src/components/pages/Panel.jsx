function Panel() {
  return (
    <>
      <section className="bg-gray-50 h-screen w-screen text-left" id="body">
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
          <div className="w-full rounded-lg bg-white text-black text-center shadow sm:max-w-md md:mt-0 xl:p-0">
            <p className="py-10"> поздравляю ты в админ панели ура</p>
          </div>
        </div>
      </section>
    </>
  );
}

export default Panel;
