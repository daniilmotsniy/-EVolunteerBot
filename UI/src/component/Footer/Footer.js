/**
 * The whole application footer
 */


import { Link } from "react-router-dom";
import {
  Box,
  Container,
  Typography,
} from "@mui/material";


function Copyright() {
  return (
    <Typography variant="body2" color="text.secondary" textAlign="center">
      {'Copyright © '}
      {/* redirect to https://www.linkedin.com/company/kharkivbayraktar */}
      <Link color="inherit" to="/">
        Bayraktar Team
      </Link>{' '}
      {new Date().getFullYear()}
    </Typography>
  );
};

function Footer() {
  return (
    <Box
      component="footer"
      sx={{
        py: 3,
        px: 2,
        mt: 'auto',
        backgroundColor: (theme) =>
          theme.palette.mode === 'light'
            ? theme.palette.grey[200]
            : theme.palette.grey[800],
      }}
    >
      <Container maxWidth="sm">
        <Typography variant="body1" textAlign="center">
          From Ukraine with love 🇺🇦❤️
        </Typography>
        <Copyright />
      </Container>
    </Box>
  )
}

export default Footer;