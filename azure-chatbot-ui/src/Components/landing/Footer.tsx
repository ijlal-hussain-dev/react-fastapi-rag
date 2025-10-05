const Footer = () => {
  return (
    <footer className="text-center">
      <div className="container">
        <p className="mb-0 text-muted">
          &copy; {new Date().getFullYear()} document Bazaar. All rights reserved.
        </p>
      </div>
    </footer>
  );
};

export default Footer;
