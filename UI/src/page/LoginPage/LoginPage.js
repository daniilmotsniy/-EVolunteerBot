/**
 * Landing page for unauthenticated (random) users
 */

//  import { Container, Grid, Typography } from "@mui/material";
import {
  useState
} from 'react';
import {
  Avatar,
  Button,
  CssBaseline,
  IconButton,
  Snackbar,
  TextField,
  Box,
  Alert,
} from "@mui/material";

import CloseIcon from '@mui/icons-material/Close';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';

import { api } from 'utils/api';
 
 
function LoginPage() {
  const [errorSnackbarOpen, setErrorSnackbarOpen] = useState(false);
  
  function hanldeSnackbarClose(event, reason) {
    if (reason === "clickaway") {
      return;
    }
    setErrorSnackbarOpen(false);
  }

  const handleSubmit = (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const submitData = {
    email: data.get('email'),
    password: data.get('password'),
    };
    api.login(submitData.email, submitData.password)
    .then((response) => {
    //  console.log("Response = ", response);
    })
    .then(() => (window.location.replace("/")))
    .catch(err => {
      setErrorSnackbarOpen(true);
    })
  };
 
  return (
    <>
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <Box
          sx={{
            marginTop: 8,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography component="h1" variant="h5">
            Увійти
          </Typography>
          <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="email"
              label="Адреса електронної пошти"
              name="email"
              autoComplete="email"
              autoFocus
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="Пароль"
              type="password"
              id="password"
              autoComplete="current-password"
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Увійти
            </Button>
          </Box>
        </Box>
      </Container>
      <Snackbar
        open={errorSnackbarOpen}
        autoHideDuration={4000}
        onClose={hanldeSnackbarClose}
      >
        <Alert 
          onClose={hanldeSnackbarClose}
          severity="error"
          variant="filled"
        >Invalid credentials
        </Alert>
      </Snackbar>
    </>
  );
}
export default LoginPage;