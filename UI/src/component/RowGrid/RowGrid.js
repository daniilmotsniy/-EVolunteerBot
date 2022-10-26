import { Grid } from "@mui/material";

function RowGrid(props) {
  return (
    <Grid container key={props.insideKey} spacing={1}>
      {props.children instanceof Array ? props.children.map((child, idx) => (
        <Grid key={idx} item>{child}</Grid>
      ))
      :
      (<Grid item>{props.children}</Grid>)
    }
    </Grid>
  )
}

export default RowGrid;