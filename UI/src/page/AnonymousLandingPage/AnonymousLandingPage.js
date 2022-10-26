/**
 * Landing page for unauthenticated (random) users
 */

import {
  Grid,
  Typography
} from "@mui/material";

function AnonymousLandingPage() {
  return (
    <Grid
      container
      direction="row"
    >
      <Grid item width="100%">
        <br></br>
        <Typography component="h1" variant="h3" textAlign="center">
          Kharkiv.Bayraktar
        </Typography>

        <Typography component="h6" variant="h6" textAlign="right">
          Кожне життя безцінне
        </Typography>
        <Typography component="p" variant="body" textAlign="left">
          Ми допомагаємо рятувати життя, розподіляючи рятівні ресурси серед людей
        </Typography>
      </Grid>
    </Grid>
  )
};
export default AnonymousLandingPage;