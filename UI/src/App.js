// import logo from './logo.svg';
import './App.css';

import { useEffect, useReducer } from 'react';

import { AuthenticatedRouter, AnonymousRouter } from "router";
import { API, api } from "utils/api";
import { createTheme } from '@mui/material';
import { ThemeProvider } from '@emotion/react';

import { userReducer, initialState } from 'reducer/userReducer';
import UserContext from 'context/userContext';



const theme = createTheme({
  palette: {
    primary: {
      main: "#0057b7",
      contrastText: "#ffd700",
    },
    secondary: {
      main: "#ffd700",
      contrastText: "#0057b7",
    }
  }
})


function App() {
  const authenticated = API.isAuthenticated;
  const [state, dispatch] = useReducer(userReducer, initialState);

  let refreshPresentAndRelevant = API.isTokenPresentAndRelevant("refresh");

  const Router = refreshPresentAndRelevant ? AuthenticatedRouter : AnonymousRouter;


  function fetchUser() {
    api.getUser()
    .then(userData => {
        dispatch({type: "setUser", user: userData.data});
    });
  }

  useEffect(() => {
    if (refreshPresentAndRelevant){
      fetchUser();
    }
  }, []);

  return (
    <ThemeProvider theme={theme}>
      <UserContext.Provider
        value={{
          user: state.user
        }}
      >
        <Router />
      </UserContext.Provider>
    </ThemeProvider>
  );
}

export default App;
