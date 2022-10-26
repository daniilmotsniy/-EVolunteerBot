import * as React from 'react';
import {
  Box,
  AppBar,
  Container,
  Toolbar,
  Typography,
  Button
} from '@mui/material';
import { Link } from 'react-router-dom';
import { Footer } from "component";



function AnonymousTemplate(props) {

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        minHeight: '100vh',
      }}
    >
      <AppBar position="static">
        <Toolbar>
          
          <Link to="/" style={{textDecoration: "none"}}>
            <Typography
            color="secondary"
            variant="h4"
            >Kharkiv.Bayraktar</Typography>
          </Link>
          <Box sx={{ flexGrow: 1 }} />
          <Box sx={{ display: { xs: 'flex', md: 'flex' } }}>
            <Link to="/login" >
              <Button
                variant="contained"
                color="secondary"
              >Увійти</Button>
            </Link>
          </Box>

        </Toolbar>
      </AppBar>

      <Container component="main" sx={{ mt: 8, mb: 2 }} maxWidth="md">
        {props.children}
      </Container>

      <Footer />
    </Box>
  )
};

export default AnonymousTemplate;