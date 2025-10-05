import { Link } from "react-router-dom";

const About = () => {
  return (
    <div className="container my-5">
      {/* Hero Section */}
      <div
        className="p-5 rounded shadow-sm mb-5 text-center"
        style={{
          background: "linear-gradient(135deg, #fff4e5, #ffe9d9)",
        }}
      >
        <h1 className="display-4 fw-bold">About document bazaar</h1>
        <p className="fs-5 text-muted">
          Discover, upload, and share your favorite DOCUMENT from around the world.
        </p>
      </div>

      {/* Content Section */}
      <div className="row align-items-center">
        {/* Image */}
        <div className="col-md-6 mb-4 mb-md-0">
          <img
            src="https://www.wur.nl/upload_mm/1/a/a/00a36c6f-098a-440c-83f3-3ec53099bea5_food_technology_6643fd38_750x400.jpg"
            alt="Cooking"
            className="img-fluid rounded shadow"
            style={{ objectFit: "cover", width: "100%", maxHeight: "400px" }}
          />
        </div>

        {/* Text */}
        <div className="col-md-6">
          <h2 className="fw-bold mb-3">Our Mission</h2>
          <p className="text-muted mb-3">
            Recipe Bazaar was created for food lovers everywhere. Our mission is
            to provide a platform where you can discover new flavors, share your
            culinary creations, and get inspired by home chefs around the world.
          </p>
          <h2 className="fw-bold mb-3">Why Choose Us?</h2>
          <ul className="list-unstyled text-muted">
            <li>✅ Easy-to-follow recipes for all skill levels</li>
            <li>✅ Community-driven content with real feedback</li>
            <li>✅ Discover cuisines from different cultures</li>
            <li>✅ Add and manage your own recipes seamlessly</li>
          </ul>

          <Link to="/recipes" className="btn btn-primary mt-3">
            Explore Recipes
          </Link>
        </div>
      </div>

      {/* Footer Callout */}
      <div
        className="text-center mt-5 p-4 rounded shadow-sm"
        style={{ background: "rgba(255, 244, 229, 0.85)" }}
      >
        <h3 className="fw-bold">Join our foodie community today!</h3>
        <p className="text-muted">
          Create an account and start sharing your favorite recipes.
        </p>
        <Link to="/register" className="btn btn-danger">
          Sign Up
        </Link>
      </div>
    </div>
  );
};

export default About;
