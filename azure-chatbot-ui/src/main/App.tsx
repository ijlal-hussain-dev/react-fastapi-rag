import { BrowserRouter } from "react-router-dom";
import "./App.css";
import Footer from "../Components/landing/Footer";
import Header from "../Components/landing/Header";
import AppRoutes from "../Components/AppRoutes";

function App() {
  return (
    <BrowserRouter>
      <div className="page-container">
        <Header subHeader="Upload documents from anywhere"></Header>
        <div className="content-wrap">
          <AppRoutes />
        </div>
        <Footer />
      </div>
    </BrowserRouter>
  );
}

export default App;
