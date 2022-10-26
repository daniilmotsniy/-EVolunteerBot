/**
 * Router for unauthenticated users
 */
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { AnonymousLandingPage, LoginPage } from "page";
import { AnonymousTemplate } from "component";

function AnonymousRouter(props) {
  return (
    <BrowserRouter>
      <AnonymousTemplate>
        <Routes>
          <Route path="login" element={<LoginPage />} />
          <Route path="/" element={<AnonymousLandingPage />} />
        </Routes>
      </AnonymousTemplate>
    </BrowserRouter>
  );
};

export default AnonymousRouter;