import { Route, Routes } from "react-router-dom";
import Documents from "./document/Documents";
import About from "../pages/About";
import SemanticSearch from "../pages/SemanticSearch";
import SuggestSearch from "../pages/SuggestSearch";

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<Documents />} />
      <Route path="/documents" element={<Documents />} />
      <Route path="/sementaic" element={<SemanticSearch />} />
      <Route path="/suggestions" element={<SuggestSearch />} />
      <Route path="/about" element={<About />} />
    </Routes>
  );
};

export default AppRoutes;
