/**
 * Router for authenticated users
 */
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { CoordinatorListPage } from "page";
import { AuthenticatedTemplate } from "component";

function AuthenticatedRouter(props) {
  return (
    <BrowserRouter>
      <AuthenticatedTemplate>
        <Routes>
          <Route path="/" element={<CoordinatorListPage />} />
        </Routes>
      </AuthenticatedTemplate>
    </BrowserRouter>
  );
};

export default AuthenticatedRouter;